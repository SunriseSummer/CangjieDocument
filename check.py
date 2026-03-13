#!/usr/bin/env python3
"""
check.py — Story 文档示例代码提取、构建和验证工具

从 story/ 目录下的 Markdown 文档中提取带有 <!-- check:xxx --> 标注的仓颉代码块，
自动生成 cjpm 项目并编译运行，验证示例代码的正确性。

用法:
    python3 check.py [选项]

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


@dataclass
class TestCase:
    """一个可执行的测试用例（对应一个 cjpm 项目）"""
    name: str                   # 项目名
    directive: str              # run / compile_error / runtime_error
    files: dict                 # {relative_path: code_content}
    expected_output: Optional[str]
    source_file: str
    heading: str
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


def extract_code_blocks(md_path: str) -> list:
    """从 Markdown 文件中提取所有带标注的代码块"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = []
    lines = content.split('\n')
    i = 0
    block_index = 0

    while i < len(lines):
        line = lines[i]

        # 查找 check 标注
        ann_match = CHECK_ANNOTATION_RE.search(line)
        if ann_match:
            directive = ann_match.group('directive')
            options = parse_options(ann_match.group('options') or '')
            project = options.get('project')
            file_path = options.get('file')

            # 向后查找紧跟的 cangjie 代码块
            j = i + 1
            # 跳过空行
            while j < len(lines) and lines[j].strip() == '':
                j += 1

            if j < len(lines) and lines[j].strip().startswith('```cangjie'):
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
                ))

                i = k + 1
                continue
        i += 1

    return blocks


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

        # 组装文件
        files = {}
        if any(b.file_path for b in proj_blocks):
            # 多文件模式
            for b in proj_blocks:
                fp = b.file_path or 'src/main.cj'
                files[fp] = b.code
        else:
            # 合并模式：所有代码块合到一个文件
            combined = '\n\n'.join(b.code for b in proj_blocks)
            files['src/main.cj'] = combined

        name = _make_project_name(md_path, proj_blocks[0].heading, proj_blocks[0].block_index, proj_name)
        testcases.append(TestCase(
            name=name,
            directive=directive,
            files=files,
            expected_output=expected_output,
            source_file=proj_blocks[0].source_file,
            heading=proj_blocks[0].heading,
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
  output-type = "executable"

[dependencies]
"""


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

    toml_content = CJPM_TOML_TEMPLATE.format(name=pkg_name)
    (proj_dir / 'cjpm.toml').write_text(toml_content, encoding='utf-8')

    # 写代码文件
    for rel_path, code in tc.files.items():
        file_path = proj_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # 自动添加 package 声明（如果代码中没有）
        if not re.search(r'^\s*package\s+', code, re.MULTILINE):
            # 根据文件路径确定包名
            if rel_path == 'src/main.cj' or rel_path.startswith('src/'):
                code = f'package {pkg_name}\n\n' + code
            else:
                code = f'package {pkg_name}\n\n' + code

        file_path.write_text(code, encoding='utf-8')

    tc.project_dir = proj_dir
    return proj_dir


def run_testcase(tc: TestCase, timeout_build: int = 60, timeout_run: int = 30) -> dict:
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
# 主流程
# ============================================================

def find_story_files(story_dir: str) -> list:
    """查找 story 目录下所有 Markdown 文件"""
    files = []
    story_path = Path(story_dir)
    if not story_path.exists():
        print(f"Error: story directory '{story_dir}' not found", file=sys.stderr)
        sys.exit(1)
    for md_file in sorted(story_path.rglob('*.md')):
        files.append(str(md_file))
    return files


def main():
    parser = argparse.ArgumentParser(
        description='Story 文档示例代码提取、构建和验证工具',
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
        ''')
    )

    parser.add_argument(
        '-d', '--story-dir',
        default='story',
        help='story 文档目录路径 (默认: story)',
    )
    parser.add_argument(
        '-o', '--output-dir',
        default='story_tests',
        help='提取的示例代码存放路径 (默认: story_tests)',
    )
    parser.add_argument(
        '-f', '--file',
        action='append',
        help='只处理指定的文档文件（可多次指定）',
    )
    parser.add_argument(
        '-s', '--story',
        help='只处理指定的 story 子目录（如 begin, begin-v2）',
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

    # 确定 story 目录
    story_dir = args.story_dir
    if args.story:
        story_dir = os.path.join(args.story_dir, args.story)

    # 收集要处理的文件
    if args.file:
        md_files = args.file
    else:
        md_files = find_story_files(story_dir)

    if not md_files:
        print(f"No markdown files found in '{story_dir}'")
        sys.exit(0)

    # 创建输出目录
    output_base = Path(args.output_dir)
    output_base.mkdir(parents=True, exist_ok=True)

    # 统计
    total = 0
    passed = 0
    failed = 0
    skipped = 0
    errors = []
    all_results = []

    print(f"📖 扫描文档目录: {story_dir}")
    print(f"📁 输出目录: {output_base}")
    print(f"📄 找到 {len(md_files)} 个文档文件\n")

    for md_file in md_files:
        # 提取代码块
        blocks = extract_code_blocks(md_file)
        if not blocks:
            continue

        # 计算相对路径以保持目录结构
        try:
            rel = Path(md_file).relative_to(args.story_dir)
        except ValueError:
            rel = Path(md_file).name
        doc_output_dir = output_base / rel.parent

        # 组装测试用例
        testcases = blocks_to_testcases(blocks, md_file)

        if not testcases:
            continue

        rel_display = str(rel)
        skip_count = sum(1 for b in blocks if b.directive == 'skip')
        if skip_count > 0:
            skipped += skip_count

        print(f"  📄 {rel_display}: {len(testcases)} 个测试用例" +
              (f" ({skip_count} 个跳过)" if skip_count else ""))

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

    # 输出 JSON
    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"\n📋 测试结果已保存到: {args.json}")

    # 清理
    if args.clean and output_base.exists():
        shutil.rmtree(output_base)
        print(f"\n🧹 已清理输出目录: {output_base}")

    # 退出码
    if not args.extract_only and failed > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
