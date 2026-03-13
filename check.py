#!/usr/bin/env python3
"""
check.py — 仓颉 Markdown 文档示例代码提取、构建和验证工具

从指定目录下的 Markdown 文档中提取带有 <!-- check:xxx --> 标注的仓颉代码块，
自动生成 cjpm 项目并编译运行，验证示例代码的正确性。
对于未标注的代码块会发出警告，提醒开发者补全标注。

用法:
    python3 check.py [选项] [目录]

详细说明参见 check.md。
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ============================================================
# 数据模型
# ============================================================

@dataclass
class CodeBlock:
    """一个带标注的仓颉代码块"""
    directive: str          # run / compile_error / runtime_error / skip
    code: str               # 代码内容
    project: Optional[str]  # 项目分组名（多代码块合并时使用）
    file_path: Optional[str]  # 多文件项目中的文件路径
    expected_output: Optional[str]  # 期望的输出（可为 None 表示不检查）
    source_file: str        # 来源文档路径
    heading: str            # 所在章节标题
    block_index: int        # 在文档中的序号
    lang: str = 'cangjie'   # 代码块语言（cangjie / c）
    block_type: Optional[str] = None  # 代码块类型（如 macro_def 表示宏定义包）


@dataclass
class TestCase:
    """一个可执行的测试用例（对应一个 cjpm 项目）"""
    name: str                   # 项目名
    directive: str              # run / compile_error / runtime_error
    files: dict                 # {relative_path: code_content}
    expected_output: Optional[str]
    source_file: str
    heading: str
    has_macro_def: bool = False      # 是否包含宏定义代码块
    c_files: dict = field(default_factory=dict)  # C 源文件 {path: code}
    project_dir: Optional[Path] = None  # 生成的项目目录


# ============================================================
# 标注解析
# ============================================================

# 匹配 <!-- check:DIRECTIVE [key=value ...] -->
CHECK_ANNOTATION_RE = re.compile(
    r'<!--\s*check\s*:\s*'
    r'(?P<directive>\w+)'
    r'(?:\s+(?P<options>[^>]*?))?'
    r'\s*-->'
)

# 匹配 <!-- expected_output: ... -->（可多行）
EXPECTED_OUTPUT_RE = re.compile(
    r'<!--\s*expected_output\s*:\s*\n(?P<output>.*?)\s*-->',
    re.DOTALL
)

# 匹配代码块
CODE_BLOCK_RE = re.compile(
    r'```cangjie\s*\n(?P<code>.*?)```',
    re.DOTALL
)

# 匹配带语言标记的代码块（cangjie 或 c）
CODE_BLOCK_LANG_RE = re.compile(
    r'```(?P<lang>cangjie|c)\s*\n(?P<code>.*?)```',
    re.DOTALL
)

# 匹配 Markdown 标题
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)


def parse_options(option_str: str) -> dict:
    """解析标注中的 key=value 选项"""
    opts = {}
    if not option_str:
        return opts
    # 匹配 key=value 或 key="value with spaces"
    for m in re.finditer(r'(\w+)=(?:"([^"]*?)"|(\S+))', option_str):
        key = m.group(1)
        val = m.group(2) if m.group(2) is not None else m.group(3)
        opts[key] = val
    return opts


def find_heading_for_position(content: str, pos: int) -> str:
    """找到给定位置所属的最近标题"""
    best = "unknown"
    for m in HEADING_RE.finditer(content):
        if m.start() <= pos:
            best = m.group(2).strip()
        else:
            break
    return best


def extract_code_blocks(md_path: str) -> tuple:
    """从 Markdown 文件中提取所有带标注的代码块，同时记录未标注的代码块。

    返回 (annotated_blocks, unannotated_blocks)，其中 unannotated_blocks 是
    [(line_number, heading, first_line_of_code), ...] 列表。
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = []
    unannotated = []
    lines = content.split('\n')
    i = 0
    block_index = 0
    # 记录已被标注关联的代码块起始行号
    annotated_line_set = set()

    while i < len(lines):
        line = lines[i]

        # 查找 check 标注
        ann_match = CHECK_ANNOTATION_RE.search(line)
        if ann_match:
            directive = ann_match.group('directive')
            options = parse_options(ann_match.group('options') or '')
            project = options.get('project')
            file_path = options.get('file')
            block_lang = options.get('lang', 'cangjie')
            block_type = options.get('type')

            # 向后查找紧跟的 cangjie 或 c 代码块
            j = i + 1
            # 跳过空行
            while j < len(lines) and lines[j].strip() == '':
                j += 1

            # 匹配 ```cangjie 或 ```c 代码块
            detected_lang = None
            if j < len(lines):
                fence_line = lines[j].strip()
                if fence_line.startswith('```cangjie'):
                    detected_lang = 'cangjie'
                elif fence_line.startswith('```c') and not fence_line.startswith('```cangjie'):
                    detected_lang = 'c'

            if detected_lang:
                if detected_lang != 'cangjie':
                    block_lang = detected_lang
                annotated_line_set.add(j)
                # 找代码块结束
                code_lines = []
                k = j + 1
                while k < len(lines) and lines[k].strip() != '```':
                    code_lines.append(lines[k])
                    k += 1
                code = '\n'.join(code_lines)

                # 查找紧跟代码块后的 expected_output 标注
                expected_output = None
                m = k + 1
                # 跳过空行
                while m < len(lines) and lines[m].strip() == '':
                    m += 1
                # 收集可能的多行 expected_output 注释
                if m < len(lines):
                    remaining = '\n'.join(lines[m:])
                    eo_match = EXPECTED_OUTPUT_RE.match(remaining)
                    if eo_match:
                        expected_output = eo_match.group('output')
                        # 去除尾部空行但保留行间格式
                        expected_output = expected_output.rstrip('\n')

                heading = find_heading_for_position(content, sum(len(l) + 1 for l in lines[:i]))
                block_index += 1

                blocks.append(CodeBlock(
                    directive=directive,
                    code=code,
                    project=project,
                    file_path=file_path,
                    expected_output=expected_output,
                    source_file=md_path,
                    heading=heading,
                    block_index=block_index,
                    lang=block_lang,
                    block_type=block_type,
                ))

                i = k + 1
                continue
        i += 1

    # 第二遍扫描：找出所有未标注的 cangjie 代码块
    # 预计算行偏移量
    line_offsets = []
    offset = 0
    for l in lines:
        line_offsets.append(offset)
        offset += len(l) + 1

    for idx, line in enumerate(lines):
        if line.strip().startswith('```cangjie') and idx not in annotated_line_set:
            heading = find_heading_for_position(content, line_offsets[idx])
            # 取代码块的第一行（非空）作为预览
            preview = ''
            k = idx + 1
            while k < len(lines) and lines[k].strip() != '```':
                if lines[k].strip() and not preview:
                    preview = lines[k].strip()[:60]
                k += 1
            unannotated.append((idx + 1, heading, preview))  # 1-based line number

    return blocks, unannotated


# ============================================================
# 测试用例组装
# ============================================================

def blocks_to_testcases(blocks: list, md_path: str) -> list:
    """将代码块组装成测试用例"""
    testcases = []
    # 按 project 分组
    project_blocks = {}  # project_name -> [blocks]
    standalone_blocks = []

    for b in blocks:
        if b.directive == 'skip':
            continue
        if b.project:
            project_blocks.setdefault(b.project, []).append(b)
        else:
            standalone_blocks.append(b)

    # 处理独立代码块
    for b in standalone_blocks:
        name = _make_project_name(md_path, b.heading, b.block_index)
        if b.lang == 'c':
            # 独立的 C 代码块不能单独构成测试用例，跳过
            continue
        testcases.append(TestCase(
            name=name,
            directive=b.directive,
            files={'src/main.cj': b.code},
            expected_output=b.expected_output,
            source_file=b.source_file,
            heading=b.heading,
        ))

    # 处理项目组
    for proj_name, proj_blocks in project_blocks.items():
        # 确定指令：使用最后一个有具体指令（非skip）的块
        directive = 'run'
        expected_output = None
        for b in proj_blocks:
            if b.directive != 'skip':
                directive = b.directive
            if b.expected_output is not None:
                expected_output = b.expected_output

        # 分离 Cangjie 代码块和 C 代码块、宏定义块
        cj_blocks = [b for b in proj_blocks if b.lang == 'cangjie']
        c_blocks = [b for b in proj_blocks if b.lang == 'c']
        has_macro_def = any(b.block_type == 'macro_def' for b in proj_blocks)

        # 组装 Cangjie 文件
        files = {}
        if has_macro_def:
            # 宏项目：宏定义块和非宏块需要分开
            macro_cj_blocks = [b for b in cj_blocks if b.block_type == 'macro_def']
            main_cj_blocks = [b for b in cj_blocks if b.block_type != 'macro_def']

            # 宏定义块合并到 macro_def_code（由 create_cjpm_project 放入宏子模块）
            if any(b.file_path for b in macro_cj_blocks):
                for b in macro_cj_blocks:
                    fp = b.file_path or 'src/macros.cj'
                    files[fp] = b.code
            else:
                macro_combined = '\n\n'.join(b.code for b in macro_cj_blocks)
                files['__macro_src__'] = macro_combined

            # 主代码块
            if any(b.file_path for b in main_cj_blocks):
                for b in main_cj_blocks:
                    fp = b.file_path or 'src/main.cj'
                    files[fp] = b.code
            elif main_cj_blocks:
                main_combined = '\n\n'.join(b.code for b in main_cj_blocks)
                files['src/main.cj'] = main_combined
        elif any(b.file_path for b in cj_blocks):
            # 多文件模式
            for b in cj_blocks:
                fp = b.file_path or 'src/main.cj'
                files[fp] = b.code
        else:
            # 合并模式：所有 Cangjie 代码块合到一个文件
            combined = '\n\n'.join(b.code for b in cj_blocks)
            files['src/main.cj'] = combined

        # 组装 C 文件
        c_files = {}
        for b in c_blocks:
            fp = b.file_path or 'src/helper.c'
            c_files[fp] = b.code

        name = _make_project_name(md_path, proj_blocks[0].heading, proj_blocks[0].block_index, proj_name)
        testcases.append(TestCase(
            name=name,
            directive=directive,
            files=files,
            expected_output=expected_output,
            source_file=proj_blocks[0].source_file,
            heading=proj_blocks[0].heading,
            has_macro_def=has_macro_def,
            c_files=c_files,
        ))

    return testcases


def _sanitize(s: str) -> str:
    """将字符串转为安全的目录名"""
    # 移除 markdown 标记和特殊字符
    s = re.sub(r'[^\w\u4e00-\u9fff-]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s[:60] if s else 'unnamed'


def _make_project_name(md_path: str, heading: str, index: int, project: str = None) -> str:
    """生成项目目录名"""
    # 从文件名获取基础名
    base = Path(md_path).stem  # e.g. 01_hello_world
    parts = [base]
    if heading and heading != 'unknown':
        parts.append(_sanitize(heading))
    parts.append(f'block{index}')
    if project:
        parts.append(_sanitize(project))
    return '__'.join(parts)


# ============================================================
# 项目生成与测试
# ============================================================

CJPM_TOML_TEMPLATE = """\
[package]
  cjc-version = "1.0.5"
  name = "{name}"
  version = "1.0.0"
  output-type = "{output_type}"

[dependencies]
"""

CJPM_TOML_MACRO_MODULE_TEMPLATE = """\
[package]
  cjc-version = "1.0.5"
  name = "{name}"
  version = "1.0.0"
  output-type = "static"
  compile-option = "--compile-macro"

[dependencies]
"""

CJPM_TOML_WITH_MACRO_DEP_TEMPLATE = """\
[package]
  cjc-version = "1.0.5"
  name = "{name}"
  version = "1.0.0"
  output-type = "executable"

[dependencies]
  [dependencies.{macro_module}]
    path = "./{macro_module}"
"""


def _find_c_compiler() -> Optional[str]:
    """查找 C 编译器，优先使用 clang"""
    for compiler in ['clang', 'gcc']:
        if shutil.which(compiler):
            return compiler
    return None


def _compile_c_files(proj_dir: Path, c_files: dict) -> tuple:
    """编译 C 源文件为共享库。返回 (success, output_message)"""
    cc = _find_c_compiler()
    if cc is None:
        return False, 'No C compiler found (need clang or gcc)'

    all_output = []
    for rel_path, code in c_files.items():
        c_file_path = proj_dir / rel_path
        c_file_path.parent.mkdir(parents=True, exist_ok=True)
        c_file_path.write_text(code, encoding='utf-8')

        # 编译为 .o 文件
        obj_path = c_file_path.with_suffix('.o')
        try:
            result = subprocess.run(
                [cc, '-c', '-fPIC', '-o', str(obj_path), str(c_file_path)],
                cwd=str(proj_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )
            all_output.append(result.stdout + result.stderr)
            if result.returncode != 0:
                return False, f'C compilation failed:\n' + result.stderr
        except subprocess.TimeoutExpired:
            return False, 'C compilation timed out'
        except Exception as e:
            return False, str(e)

    # 如果有多个 .o 文件，链接为共享库
    obj_files = list(proj_dir.rglob('*.o'))
    if obj_files:
        lib_path = proj_dir / 'libffi_helper.a'
        try:
            result = subprocess.run(
                ['ar', 'rcs', str(lib_path)] + [str(o) for o in obj_files],
                cwd=str(proj_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )
            all_output.append(result.stdout + result.stderr)
            if result.returncode != 0:
                return False, f'ar failed:\n' + result.stderr
        except Exception as e:
            return False, str(e)

    return True, '\n'.join(all_output)


def _extract_macro_package_name(code: str) -> Optional[str]:
    """从宏定义代码中提取 macro package 名称"""
    m = re.search(r'^\s*macro\s+package\s+(\w+)', code, re.MULTILINE)
    if m:
        return m.group(1)
    return None


def _extract_package_name(code: str) -> Optional[str]:
    """从代码中提取 package 声明的包名（不含 macro package）"""
    m = re.search(r'^\s*(?!macro\s)package\s+([\w.]+)', code, re.MULTILINE)
    if m:
        return m.group(1).split('.')[0]  # 取根包名
    return None


def _has_main_function(files: dict) -> bool:
    """检查代码文件中是否包含 main 函数"""
    all_code = '\n'.join(files.values())
    return bool(re.search(r'^\s*main\s*\(', all_code, re.MULTILINE))


def create_cjpm_project(tc: TestCase, output_dir: Path) -> Path:
    """为测试用例创建 cjpm 项目"""
    proj_dir = output_dir / tc.name
    proj_dir.mkdir(parents=True, exist_ok=True)

    # 写 cjpm.toml
    pkg_name = re.sub(r'[^a-zA-Z0-9_]', '_', tc.name)[:40]
    # cjpm 项目名只能用小写字母、数字、下划线
    pkg_name = pkg_name.lower()
    if not pkg_name[0].isalpha():
        pkg_name = 'p_' + pkg_name

    # 尝试从源代码中提取 package 名称，以匹配 cjpm.toml 的项目名
    # 跳过宏定义文件（__macro_src__ 和 macro package 声明的文件）
    for rel_path, code in tc.files.items():
        if rel_path == '__macro_src__':
            continue
        if _extract_macro_package_name(code):
            continue
        src_pkg = _extract_package_name(code)
        if src_pkg:
            pkg_name = src_pkg
            break

    if tc.has_macro_def:
        # 宏项目：需要创建多模块结构
        # 从文件中分离宏定义和主代码
        macro_module_name = None
        macro_files = {}
        main_files = {}

        for rel_path, code in tc.files.items():
            if rel_path == '__macro_src__' or _extract_macro_package_name(code):
                # 这是宏定义代码
                if not macro_module_name:
                    macro_module_name = _extract_macro_package_name(code) or 'macro_mod'
                macro_files['src/macros.cj'] = code
            else:
                main_files[rel_path] = code

        if not macro_module_name:
            macro_module_name = 'macro_mod'

        # 创建宏模块
        macro_dir = proj_dir / macro_module_name
        macro_dir.mkdir(parents=True, exist_ok=True)

        macro_toml = CJPM_TOML_MACRO_MODULE_TEMPLATE.format(name=macro_module_name)
        (macro_dir / 'cjpm.toml').write_text(macro_toml, encoding='utf-8')

        for rel_path, code in macro_files.items():
            file_path = macro_dir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(code, encoding='utf-8')

        # 创建主项目
        main_toml = CJPM_TOML_WITH_MACRO_DEP_TEMPLATE.format(
            name=pkg_name,
            macro_module=macro_module_name,
        )
        (proj_dir / 'cjpm.toml').write_text(main_toml, encoding='utf-8')

        # 写主项目代码文件
        for rel_path, code in main_files.items():
            file_path = proj_dir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # 自动添加 package 声明（如果代码中没有）
            if not re.search(r'^\s*package\s+', code, re.MULTILINE):
                code = f'package {pkg_name}\n\n' + code

            file_path.write_text(code, encoding='utf-8')
    else:
        # 标准项目
        # 自动检测 output-type：有 main() 用 executable，否则用 static
        if _has_main_function(tc.files):
            output_type = 'executable'
        elif tc.directive in ('build_only', 'compile_error'):
            output_type = 'static'
        else:
            output_type = 'executable'

        toml_content = CJPM_TOML_TEMPLATE.format(name=pkg_name, output_type=output_type)
        (proj_dir / 'cjpm.toml').write_text(toml_content, encoding='utf-8')

        # 写代码文件
        for rel_path, code in tc.files.items():
            file_path = proj_dir / rel_path
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # 自动添加 package 声明（如果代码中没有）
            if not re.search(r'^\s*(macro\s+)?package\s+', code, re.MULTILINE):
                # 根据文件路径确定包名
                code = f'package {pkg_name}\n\n' + code

            file_path.write_text(code, encoding='utf-8')

    tc.project_dir = proj_dir
    return proj_dir


def run_testcase(tc: TestCase, timeout_build: int = 60, timeout_run: int = 30,
                 verbose: bool = False) -> dict:
    """执行测试用例，返回结果字典"""
    result = {
        'name': tc.name,
        'directive': tc.directive,
        'source_file': tc.source_file,
        'heading': tc.heading,
        'status': 'unknown',
        'build_ok': False,
        'run_ok': False,
        'build_output': '',
        'run_output': '',
        'error': '',
        'expected_output': tc.expected_output,
        'output_match': None,
    }

    if tc.project_dir is None:
        result['status'] = 'error'
        result['error'] = 'Project directory not created'
        return result

    proj_dir = tc.project_dir

    # 编译 C 文件（如果有）
    if tc.c_files:
        c_ok, c_output = _compile_c_files(proj_dir, tc.c_files)
        if not c_ok:
            result['build_output'] = c_output
            result['status'] = 'FAIL'
            result['error'] = f'C compilation failed: {c_output}'
            return result
        if verbose:
            result['build_output'] = c_output + '\n'

    # 编译
    try:
        build_proc = subprocess.run(
            ['cjpm', 'build'],
            cwd=str(proj_dir),
            capture_output=True,
            text=True,
            timeout=timeout_build,
        )
        result['build_output'] = (build_proc.stdout + build_proc.stderr).strip()
        result['build_ok'] = (build_proc.returncode == 0)
    except subprocess.TimeoutExpired:
        result['build_output'] = 'Build timed out'
        result['build_ok'] = False
    except Exception as e:
        result['build_output'] = str(e)
        result['build_ok'] = False

    # 根据指令判断结果
    if tc.directive == 'compile_error':
        if result['build_ok']:
            result['status'] = 'FAIL'
            result['error'] = 'Expected compile error but build succeeded'
        else:
            result['status'] = 'PASS'
        return result

    if not result['build_ok']:
        result['status'] = 'FAIL'
        result['error'] = 'Build failed unexpectedly'
        return result

    # 运行
    if tc.directive in ('run', 'runtime_error'):
        try:
            run_proc = subprocess.run(
                ['cjpm', 'run'],
                cwd=str(proj_dir),
                capture_output=True,
                text=True,
                timeout=timeout_run,
            )
            # 提取实际运行输出（去除 cjpm 自身的消息）
            stdout_lines = run_proc.stdout.strip().split('\n')
            # cjpm run 最后一行通常是 "cjpm run finished"
            actual_lines = []
            for line in stdout_lines:
                if line.strip() in ('cjpm run finished', ''):
                    continue
                actual_lines.append(line)
            actual_output = '\n'.join(actual_lines)

            result['run_output'] = actual_output
            stderr_text = run_proc.stderr.strip()
            has_runtime_exception = 'An exception has occurred' in stderr_text
            result['run_ok'] = (run_proc.returncode == 0) and not has_runtime_exception

            if tc.directive == 'runtime_error':
                if not has_runtime_exception and run_proc.returncode == 0:
                    result['status'] = 'FAIL'
                    result['error'] = 'Expected runtime error but run succeeded'
                else:
                    result['status'] = 'PASS'
                return result

            if not result['run_ok']:
                result['status'] = 'FAIL'
                result['error'] = f'Run failed: {stderr_text}'
                return result

            # 检查输出
            if tc.expected_output is not None:
                expected = tc.expected_output.strip()
                actual = actual_output.strip()
                if expected == actual:
                    result['output_match'] = True
                    result['status'] = 'PASS'
                else:
                    result['output_match'] = False
                    result['status'] = 'FAIL'
                    result['error'] = f'Output mismatch:\n  Expected:\n{textwrap.indent(expected, "    ")}\n  Actual:\n{textwrap.indent(actual, "    ")}'
            else:
                result['status'] = 'PASS'

        except subprocess.TimeoutExpired:
            result['run_output'] = 'Run timed out'
            result['run_ok'] = False
            result['status'] = 'FAIL'
            result['error'] = 'Run timed out'
        except Exception as e:
            result['run_output'] = str(e)
            result['run_ok'] = False
            result['status'] = 'FAIL'
            result['error'] = str(e)
    elif tc.directive == 'build_only':
        # 只编译，不运行
        result['status'] = 'PASS'
    else:
        result['status'] = 'PASS'

    return result


# ============================================================
# 测试报告生成
# ============================================================

def generate_report(
    output_dir: Path,
    scan_dir: str,
    all_results: list,
    unannotated_warnings: list,
    skipped: int,
    md_files: list,
) -> Path:
    """在输出目录下生成人类友好的测试报告 report.md。

    参数:
        output_dir: 输出目录
        scan_dir: 扫描的文档目录路径
        all_results: run_testcase() 返回的结果列表
        unannotated_warnings: [(file, line, heading, preview), ...]
        skipped: 跳过的代码块数量
        md_files: 处理的文档文件列表

    返回:
        生成的 report.md 路径
    """
    from datetime import datetime, timezone

    total = len(all_results)
    passed = sum(1 for r in all_results if r['status'] == 'PASS')
    failed = sum(1 for r in all_results if r['status'] == 'FAIL')
    unannotated_total = len(unannotated_warnings)

    # 按来源文件分组
    file_results = {}
    for r in all_results:
        src = r['source_file']
        file_results.setdefault(src, []).append(r)

    lines = []

    # 标题
    lines.append('# 测试报告\n')

    # 元信息
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    lines.append(f'- **扫描目录**: `{scan_dir}`')
    lines.append(f'- **生成时间**: {now}')
    lines.append(f'- **文档文件数**: {len(md_files)}')
    lines.append('')

    # 总览
    lines.append('## 总览\n')
    if total == 0 and unannotated_total == 0:
        lines.append('未发现可测试的代码块。\n')
    else:
        if failed == 0 and unannotated_total == 0:
            status_emoji = '✅'
        else:
            status_emoji = '❌'

        lines.append(f'| 指标 | 数量 |')
        lines.append(f'|------|------|')
        lines.append(f'| {status_emoji} 测试总数 | {total} |')
        lines.append(f'| ✅ 通过 | {passed} |')
        lines.append(f'| ❌ 失败 | {failed} |')
        lines.append(f'| ⏭️ 跳过 | {skipped} |')
        lines.append(f'| ⚠️ 未标注 | {unannotated_total} |')
        lines.append('')

    # 按文件分列的详情
    if file_results:
        lines.append('## 文件详情\n')
        for src_file in sorted(file_results.keys()):
            results = file_results[src_file]
            file_pass = sum(1 for r in results if r['status'] == 'PASS')
            file_fail = sum(1 for r in results if r['status'] == 'FAIL')
            file_icon = '✅' if file_fail == 0 else '❌'
            lines.append(f'### {file_icon} `{src_file}`\n')
            lines.append(f'| 测试用例 | 类型 | 结果 |')
            lines.append(f'|----------|------|------|')
            for r in results:
                icon = '✅' if r['status'] == 'PASS' else '❌'
                directive = r['directive']
                name_display = r['heading'] if r['heading'] != 'unknown' else r['name']
                lines.append(f'| {name_display} | `{directive}` | {icon} {r["status"]} |')
            lines.append('')

    # 失败详情
    failed_results = [r for r in all_results if r['status'] == 'FAIL']
    if failed_results:
        lines.append('## 失败详情\n')
        for r in failed_results:
            lines.append(f'### ❌ {r["name"]}\n')
            lines.append(f'- **来源**: `{r["source_file"]}` > {r["heading"]}')
            lines.append(f'- **类型**: `{r["directive"]}`')
            lines.append(f'- **错误**: {r["error"]}')
            if r.get('build_output') and not r.get('build_ok'):
                lines.append('')
                lines.append('编译输出:')
                lines.append('')
                lines.append('```')
                lines.append(r['build_output'])
                lines.append('```')
            lines.append('')

    # 未标注代码块
    if unannotated_warnings:
        lines.append('## 未标注的代码块\n')
        lines.append('以下代码块缺少 `<!-- check:xxx -->` 标注，请补全：\n')
        lines.append('| 文件 | 行号 | 章节 | 代码预览 |')
        lines.append('|------|------|------|----------|')
        for filepath, line_no, heading, preview in unannotated_warnings:
            # 转义可能破坏表格的特殊字符
            safe_preview = (preview or '').replace('|', '\\|').replace('\n', ' ').replace('`', "'")[:60]
            lines.append(f'| `{filepath}` | {line_no} | {heading} | `{safe_preview}` |')
        lines.append('')

    report_path = output_dir / 'report.md'
    report_path.write_text('\n'.join(lines), encoding='utf-8')
    return report_path


# ============================================================
# 主流程
# ============================================================

def find_md_files(base_dir: str) -> list:
    """查找目录下所有 Markdown 文件"""
    files = []
    base_path = Path(base_dir)
    if not base_path.exists():
        print(f"Error: directory '{base_dir}' not found", file=sys.stderr)
        sys.exit(1)
    for md_file in sorted(base_path.rglob('*.md')):
        files.append(str(md_file))
    return files


def main():
    parser = argparse.ArgumentParser(
        description='仓颉 Markdown 文档示例代码提取、构建和验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            标注格式:
              <!-- check:run -->                 编译并运行，应当成功
              <!-- check:compile_error -->        预期编译失败
              <!-- check:runtime_error -->        预期运行时错误
              <!-- check:build_only -->           仅编译，不运行
              <!-- check:skip -->                 跳过此代码块
              <!-- check:run project=NAME -->     多代码块项目的一部分

            期望输出（放在代码块之后）:
              <!-- expected_output:
              line1
              line2
              -->

            未标注的 cangjie 代码块会被报告为警告，提示开发者补全标注。
        ''')
    )

    parser.add_argument(
        'dir',
        nargs='?',
        default='.',
        help='文档目录路径 (默认: 当前目录)',
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='check_output',
        help='提取的示例代码存放路径 (默认: check_output)',
    )
    parser.add_argument(
        '-f', '--file',
        action='append',
        help='只处理指定的文档文件（可多次指定）',
    )
    parser.add_argument(
        '-s', '--subdir',
        help='只处理指定的子目录（如 begin, begin-v2）',
    )
    parser.add_argument(
        '--clean',
        action='store_true',
        help='测试完成后清理生成的项目目录',
    )
    parser.add_argument(
        '--extract-only',
        action='store_true',
        help='仅提取代码，不构建运行',
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='显示详细输出',
    )
    parser.add_argument(
        '--json',
        metavar='FILE',
        help='将测试结果输出为 JSON 文件',
    )

    args = parser.parse_args()

    # 检查 cjpm 是否可用
    if not args.extract_only:
        try:
            subprocess.run(['cjpm', '--help'], capture_output=True, timeout=10)
        except FileNotFoundError:
            print("Error: cjpm 命令不可用。请先 source envsetup.sh 配置环境。", file=sys.stderr)
            sys.exit(1)

    # 确定扫描目录
    scan_dir = args.dir
    if args.subdir:
        scan_dir = os.path.join(args.dir, args.subdir)

    # 收集要处理的文件
    if args.file:
        md_files = args.file
    else:
        md_files = find_md_files(scan_dir)

    if not md_files:
        print(f"No markdown files found in '{scan_dir}'")
        sys.exit(0)

    # 创建输出目录
    output_base = Path(args.output_dir)
    output_base.mkdir(parents=True, exist_ok=True)

    # 统计
    total = 0
    passed = 0
    failed = 0
    skipped = 0
    unannotated_total = 0
    unannotated_warnings = []  # [(file, line, heading, preview), ...]
    errors = []
    all_results = []

    print(f"📖 扫描文档目录: {scan_dir}")
    print(f"📁 输出目录: {output_base}")
    print(f"📄 找到 {len(md_files)} 个文档文件\n")

    for md_file in md_files:
        # 提取代码块
        blocks, unannotated = extract_code_blocks(md_file)

        # 记录未标注代码块
        if unannotated:
            unannotated_total += len(unannotated)
            for line_no, heading, preview in unannotated:
                unannotated_warnings.append((md_file, line_no, heading, preview))

        if not blocks and not unannotated:
            continue

        # 计算相对路径以保持目录结构
        try:
            rel = Path(md_file).relative_to(args.dir)
        except ValueError:
            rel = Path(md_file).name
        doc_output_dir = output_base / rel.parent

        # 组装测试用例
        testcases = blocks_to_testcases(blocks, md_file)

        rel_display = str(rel)
        skip_count = sum(1 for b in blocks if b.directive == 'skip')
        if skip_count > 0:
            skipped += skip_count

        unannotated_count = len(unannotated) if unannotated else 0
        info_parts = []
        if testcases:
            info_parts.append(f"{len(testcases)} 个测试用例")
        if skip_count:
            info_parts.append(f"{skip_count} 个跳过")
        if unannotated_count:
            info_parts.append(f"{unannotated_count} 个未标注")

        detail = f" ({', '.join(info_parts)})" if info_parts else ""
        print(f"  📄 {rel_display}:{detail}")

        for tc in testcases:
            total += 1

            # 创建 cjpm 项目
            create_cjpm_project(tc, doc_output_dir)

            if args.extract_only:
                if args.verbose:
                    print(f"    ✅ 已提取: {tc.name}")
                continue

            # 运行测试
            result = run_testcase(tc)
            all_results.append(result)

            if result['status'] == 'PASS':
                passed += 1
                if args.verbose:
                    print(f"    ✅ PASS: {tc.name}")
            else:
                failed += 1
                errors.append(result)
                print(f"    ❌ FAIL: {tc.name}")
                if args.verbose:
                    print(f"       {result['error']}")

    # 输出摘要
    print(f"\n{'='*60}")
    if args.extract_only:
        print(f"📊 提取完成: {total} 个测试用例已创建")
        if skipped:
            print(f"   ⏭️  跳过: {skipped} 个代码块")
    else:
        print(f"📊 测试结果: {passed} 通过 / {failed} 失败 / {skipped} 跳过 (共 {total} 个)")

        if errors:
            print(f"\n{'='*60}")
            print("❌ 失败详情:\n")
            for r in errors:
                print(f"  [{r['directive']}] {r['name']}")
                print(f"    来源: {r['source_file']} > {r['heading']}")
                print(f"    错误: {r['error']}")
                if r['build_output'] and not r['build_ok']:
                    print(f"    编译输出:\n{textwrap.indent(r['build_output'], '      ')}")
                print()

    # 报告未标注代码块
    if unannotated_warnings:
        print(f"\n{'='*60}")
        print(f"⚠️  发现 {unannotated_total} 个未标注的 cangjie 代码块:\n")
        for filepath, line_no, heading, preview in unannotated_warnings:
            print(f"  {filepath}:{line_no}  (章节: {heading})")
            if preview:
                print(f"    {preview}")
        print(f"\n   请为这些代码块添加 <!-- check:xxx --> 标注。")

    # 输出 JSON
    if args.json:
        json_data = {
            'results': all_results,
            'unannotated': [
                {'file': f, 'line': ln, 'heading': h, 'preview': p}
                for f, ln, h, p in unannotated_warnings
            ],
        }
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"\n📋 测试结果已保存到: {args.json}")

    # 生成测试报告
    if not args.extract_only:
        report_path = generate_report(
            output_dir=output_base,
            scan_dir=scan_dir,
            all_results=all_results,
            unannotated_warnings=unannotated_warnings,
            skipped=skipped,
            md_files=md_files,
        )
        print(f"\n📝 测试报告已生成: {report_path}")

    # 清理
    if args.clean and output_base.exists():
        shutil.rmtree(output_base)
        print(f"\n🧹 已清理输出目录: {output_base}")

    # 退出码
    if not args.extract_only and failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
