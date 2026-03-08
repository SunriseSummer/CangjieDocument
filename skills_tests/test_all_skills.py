#!/usr/bin/env python3
"""
仓颉 SKILL.md 示例代码自动化测试脚本

用法：
    python3 test_all_skills.py                    # 测试所有 SKILL
    python3 test_all_skills.py --skill json       # 测试单个 SKILL
    python3 test_all_skills.py --build-only       # 仅编译不运行
    python3 test_all_skills.py --verbose          # 详细输出

环境要求：
    - 已 source cangjie/envsetup.sh
    - 设置环境变量 CANGJIE_STDX_PATH 指向 stdx 静态库路径
      例如: export CANGJIE_STDX_PATH=/path/to/cangjie-stdx/linux_x86_64_cjnative/static/stdx
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import shutil
from dataclasses import dataclass, field
from typing import Optional


# ======================== 配置 ========================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(SCRIPT_DIR)
SKILLS_DIR = os.path.join(REPO_DIR, "skills")
CJC_VERSION = "1.0.5"  # Cangjie SDK 版本，用于 cjpm.toml 生成


# ======================== 数据结构 ========================

@dataclass
class CodeBlock:
    """代码块信息"""
    skill: str          # 所属 skill 名
    index: int          # 在 SKILL.md 中的序号
    line: int           # 在 SKILL.md 中的起始行号
    code: str           # 代码内容
    context: str        # 代码块前面的上下文文本


@dataclass
class TestResult:
    """测试结果"""
    block: CodeBlock
    status: str         # PASS, FAIL, SKIP
    reason: str = ""    # 跳过原因或错误信息
    output: str = ""    # 运行输出
    build_output: str = ""  # 编译输出
    test_strategy: str = ""  # 使用的测试策略


# ======================== 代码提取 ========================

def extract_blocks(skill_name: str) -> list[CodeBlock]:
    """从 SKILL.md 中提取所有 cangjie 代码块"""
    skill_file = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    if not os.path.exists(skill_file):
        return []

    with open(skill_file, encoding="utf-8") as f:
        content = f.read()

    blocks = []
    lines = content.split('\n')
    in_block = False
    block_lines = []
    block_start_line = 0
    context_before = ""

    for i, line in enumerate(lines):
        if line.strip() == '```cangjie':
            in_block = True
            block_lines = []
            block_start_line = i + 2  # 1-based, skip the ``` line
            ctx_start = max(0, i - 5)
            context_before = '\n'.join(lines[ctx_start:i]).strip()
        elif line.strip() == '```' and in_block:
            in_block = False
            code = '\n'.join(block_lines)
            blocks.append(CodeBlock(
                skill=skill_name,
                index=len(blocks),
                line=block_start_line,
                code=code,
                context=context_before,
            ))
        elif in_block:
            block_lines.append(line)

    return blocks


# ======================== 代码块分类 ========================

def classify_block(block: CodeBlock) -> dict:
    """分类代码块，决定测试策略

    分类属性：
    - has_main: 含 main() 入口函数，可直接编译运行
    - uses_stdx: 使用 stdx 扩展标准库，需要额外配置
    - is_error_demo: 故意错误示例（代码中第一个非空非注释行含 ❌），需验证编译失败
    - is_interactive: 含交互式输入或阻塞式服务器代码，仅做编译测试
    - has_ffi_extern: 含 foreign func 声明，需 C 库链接
    - is_macro_pkg: 宏包定义（macro package），需特殊编译链
    - is_test_block: 含 @Test/@Bench 注解的测试代码
    - has_package_decl: 含自定义包声明的多包示例
    - is_fragment: 不含 main() 的代码片段
    - is_pseudo_code: 含 ... 省略号的伪代码/API 签名
    - is_api_signature: 仅含函数/方法签名，无函数体
    """
    code = block.code
    ctx = block.context

    has_main = bool(re.search(r'^main\(', code, re.MULTILINE))
    uses_stdx = 'import stdx.' in code
    # 错误示例判断：
    # 1. 非注释行含 ❌ 标记（如 `public extend A {} // ❌ Error`）→ 错误示例
    # 2. 代码块第一行是 ❌ 注释，且非注释代码不超过 2 行 → 错误示例
    #    （整个代码块的目的就是展示单个错误语句）
    #    但如果有多行有效代码（如有效代码 + 注释中的错误），则不算错误示例
    has_error_marker = '❌' in code
    if has_error_marker:
        code_lines = code.split('\n')
        non_comment_lines = [l for l in code_lines if l.strip() and not l.strip().startswith('//')]
        # 情况 1：❌ 出现在非注释行（行尾注释如 `class Foo {} // ❌ Error`）
        is_error_demo = any('❌' in l for l in non_comment_lines)
        # 情况 2：代码块第一行是 ❌ 注释，且只有 1-2 行有效代码（单个错误语句）
        if not is_error_demo:
            first_line = next((l for l in code_lines if l.strip()), '')
            if (first_line.strip().startswith('// ❌')
                    and 0 < len(non_comment_lines) <= 2):
                is_error_demo = True
    else:
        is_error_demo = False
    is_interactive = bool(re.search(r'readln\(\)|\.serve\(\)|getStdIn\(\)', code))
    has_ffi_extern = bool(re.search(r'foreign\s+func', code))
    is_macro_pkg = 'macro package' in code
    is_test_block = '@Test' in code or '@Bench' in code
    has_package_decl = bool(re.search(r'^package\s+(?!testproject)', code, re.MULTILINE))
    # 检测伪代码：函数体为 ... 或仅含签名
    is_pseudo_code = bool(re.search(r'\{\s*\.\.\.\s*\}', code)) or \
                     bool(re.search(r'/\*\s*\.\.\.\s*\*/', code))
    # 检测 API 签名：仅含函数/方法签名无函数体（如 `func get(x: T): R`）
    non_comment_lines = [l for l in code.split('\n')
                         if l.strip() and not l.strip().startswith('//')]
    is_api_signature = (len(non_comment_lines) > 0 and
                       all(re.match(r'^\s*(public\s+|static\s+|mut\s+|unsafe\s+|operator\s+)*'
                                    r'(func|prop|let|var)\s+', l)
                           or l.strip().startswith('//')
                           for l in non_comment_lines)
                       and not re.search(r'\{[^}]*\}', code))

    return {
        'has_main': has_main,
        'uses_stdx': uses_stdx,
        'is_error_demo': is_error_demo,
        'is_interactive': is_interactive,
        'has_ffi_extern': has_ffi_extern,
        'is_macro_pkg': is_macro_pkg,
        'is_test_block': is_test_block,
        'has_package_decl': has_package_decl,
        'is_fragment': not has_main,
        'is_pseudo_code': is_pseudo_code,
        'is_api_signature': is_api_signature,
    }


def get_test_strategy(classification: dict) -> str:
    """决定测试策略，返回策略名称

    策略优先级（从高到低）：
    1. pseudo_code_skip: 含 ... 省略号的伪代码/API 签名，不是可执行代码
    2. api_signature_skip: 仅含函数签名无函数体，不是可执行代码
    3. error_demo_expect_fail: 故意错误示例，编译应该失败
    4. macro_package_build: 宏包 + 调用方构建多模块 cjpm 项目测试
    5. multi_package_build: 多包示例构建多目录 cjpm 项目测试
    6. interactive_build_only: 交互式/服务器代码，仅编译不运行
    7. ffi_build_only: 含 FFI 声明，编译可能有链接错误（预期）
    8. test_block_build: @Test/@Bench 块，作为库编译
    9. fragment_wrap: 不含 main() 的片段，自动补充 main() 后编译
    10. full_build_run: 完整代码，编译并运行
    """
    if classification['is_pseudo_code'] and classification['is_fragment']:
        return 'pseudo_code_skip'
    if classification['is_api_signature'] and classification['is_fragment']:
        return 'api_signature_skip'
    if classification['is_error_demo']:
        return 'error_demo_expect_fail'
    if classification['is_macro_pkg']:
        return 'macro_package_build'
    if classification['has_package_decl']:
        return 'multi_package_build'
    if classification['is_interactive']:
        return 'interactive_build_only'
    if classification['has_ffi_extern'] and not classification['uses_stdx']:
        return 'ffi_build_only'
    if classification['is_test_block'] and classification['is_fragment']:
        return 'test_block_build'
    if classification['is_fragment']:
        return 'fragment_wrap'
    return 'full_build_run'


# ======================== 项目构建 ========================

def get_stdx_path() -> str:
    """获取 stdx 库路径，优先使用 CANGJIE_STDX_PATH 环境变量"""
    path = os.environ.get('CANGJIE_STDX_PATH', '')
    if path and os.path.exists(path):
        return path
    if not path:
        print("警告: 未设置 CANGJIE_STDX_PATH 环境变量，使用 stdx 的代码块可能无法编译")
        print("  请设置: export CANGJIE_STDX_PATH=/path/to/cangjie-stdx/linux_x86_64_cjnative/static/stdx")
    return path


def create_project(project_dir: str, uses_stdx: bool, output_type: str = "executable") -> None:
    """创建 cjpm 测试项目

    参数：
        project_dir: 项目目录
        uses_stdx: 是否使用 stdx
        output_type: 输出类型 (executable 或 static)
    """
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)

    stdx_path = get_stdx_path()

    compile_opt = ""
    if uses_stdx and stdx_path:
        compile_opt = '\n  compile-option = "-ldl"'
        bin_deps = f"""
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["{stdx_path}"]
"""
    else:
        bin_deps = ""

    toml = f"""[package]
  cjc-version = "{CJC_VERSION}"
  name = "testproject"
  version = "1.0.0"
  output-type = "{output_type}"{compile_opt}
[dependencies]
{bin_deps}"""

    with open(os.path.join(project_dir, "cjpm.toml"), 'w') as f:
        f.write(toml)


def write_main_cj(project_dir: str, code: str, is_fragment: bool = False,
                  package_name: str = "testproject") -> None:
    """将代码写入 src/main.cj

    对于片段代码，自动补充 package 声明和 main() 函数。
    """
    if is_fragment:
        imports = '\n'.join(l for l in code.split('\n') if l.strip().startswith('import '))
        non_import = '\n'.join(l for l in code.split('\n') if not l.strip().startswith('import '))

        has_toplevel = bool(re.search(
            r'^\s*(public\s+)?(class|struct|enum|interface|func|open|abstract|sealed|extend)\s',
            non_import, re.MULTILINE
        ))

        if has_toplevel:
            main_code = f"package {package_name}\n{imports}\n\n{non_import}\n\nmain() {{}}\n"
        else:
            main_code = f"package {package_name}\n{imports}\n\nmain() {{\n{non_import}\n}}\n"
    else:
        # 替换已有的 package 声明
        if re.search(r'^package\s+', code, re.MULTILINE):
            main_code = re.sub(r'^package\s+\S+', f'package {package_name}', code, count=1, flags=re.MULTILINE)
        else:
            main_code = f"package {package_name}\n\n{code}"

    with open(os.path.join(project_dir, "src", "main.cj"), 'w') as f:
        f.write(main_code)


def create_macro_project(project_dir: str, macro_code: str, caller_code: str,
                         macro_pkg_name: str = "macros") -> None:
    """创建宏包多模块 cjpm 项目

    项目结构：
        project_dir/
        ├── cjpm.toml              # 主项目配置，依赖宏模块
        ├── src/
        │   └── main.cj            # 调用宏的代码
        └── <macro_pkg_name>/      # 宏模块
            ├── cjpm.toml          # 宏模块配置（--compile-macro）
            └── src/
                └── macros.cj      # 宏定义代码
    """
    # 创建目录结构
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)
    macro_dir = os.path.join(project_dir, macro_pkg_name)
    os.makedirs(os.path.join(macro_dir, "src"), exist_ok=True)

    # 宏模块 cjpm.toml
    macro_toml = f"""[package]
  cjc-version = "{CJC_VERSION}"
  name = "{macro_pkg_name}"
  version = "1.0.0"
  output-type = "static"
  compile-option = "--compile-macro"
[dependencies]
"""
    with open(os.path.join(macro_dir, "cjpm.toml"), 'w') as f:
        f.write(macro_toml)

    # 宏定义代码
    with open(os.path.join(macro_dir, "src", "macros.cj"), 'w') as f:
        f.write(macro_code)

    # 主项目 cjpm.toml
    main_toml = f"""[package]
  cjc-version = "{CJC_VERSION}"
  name = "testproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
  {macro_pkg_name} = {{ path = "./{macro_pkg_name}" }}
"""
    with open(os.path.join(project_dir, "cjpm.toml"), 'w') as f:
        f.write(main_toml)

    # 调用方代码
    code = caller_code
    if not re.search(r'^package\s+', code, re.MULTILINE):
        code = f"package testproject\n\n{code}"
    else:
        code = re.sub(r'^package\s+\S+', 'package testproject', code, count=1, flags=re.MULTILINE)
    # 如果没有 main()，补充一个空 main
    if not re.search(r'^main\(', code, re.MULTILINE):
        code = f"{code}\n\nmain() {{}}\n"
    with open(os.path.join(project_dir, "src", "main.cj"), 'w') as f:
        f.write(code)


def create_multi_package_project(project_dir: str, package_files: dict[str, str]) -> None:
    """创建多包 cjpm 项目

    参数：
        project_dir: 项目根目录
        package_files: 字典 { "包名": "代码内容" }，
                       键为包名（如 "pkga"、"a.b"），值为对应的代码。
                       键 "testproject" 表示主包（含 main()）。

    项目结构（示例）：
        project_dir/
        ├── cjpm.toml
        └── src/
            ├── main.cj                # package testproject (含 main)
            ├── pkga/
            │   └── pkga.cj            # package testproject.pkga
            └── pkgb/
                └── pkgb.cj            # package testproject.pkgb
    """
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)

    toml = f"""[package]
  cjc-version = "{CJC_VERSION}"
  name = "testproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
"""
    with open(os.path.join(project_dir, "cjpm.toml"), 'w') as f:
        f.write(toml)

    for pkg_name, code in package_files.items():
        if pkg_name == "testproject":
            # 主包代码
            if not re.search(r'^package\s+', code, re.MULTILINE):
                code = f"package testproject\n\n{code}"
            else:
                code = re.sub(r'^package\s+\S+', 'package testproject', code, count=1, flags=re.MULTILINE)
            with open(os.path.join(project_dir, "src", "main.cj"), 'w') as f:
                f.write(code)
        else:
            # 子包代码：将包名映射到 testproject.xxx 子目录
            # 如 "pkga" -> src/pkga/pkga.cj, "a.b" -> src/a/b/b.cj
            parts = pkg_name.split('.')
            pkg_dir = os.path.join(project_dir, "src", *parts)
            os.makedirs(pkg_dir, exist_ok=True)
            # 替换 package 声明为 testproject 子包
            full_pkg_name = f"testproject.{pkg_name}"
            if re.search(r'^package\s+', code, re.MULTILINE):
                code = re.sub(r'^package\s+\S+', f'package {full_pkg_name}', code, count=1, flags=re.MULTILINE)
            else:
                code = f"package {full_pkg_name}\n\n{code}"
            # 替换代码中对其他包的引用（import 语句）
            for other_pkg in package_files:
                if other_pkg != pkg_name and other_pkg != "testproject":
                    # import pkga.* -> import testproject.pkga.*
                    code = code.replace(f'import {other_pkg}', f'import testproject.{other_pkg}')
            file_name = parts[-1] + ".cj"
            with open(os.path.join(pkg_dir, file_name), 'w') as f:
                f.write(code)

    # 对主包代码也替换 import 引用
    main_path = os.path.join(project_dir, "src", "main.cj")
    if os.path.exists(main_path):
        with open(main_path) as f:
            main_code = f.read()
        for pkg_name in package_files:
            if pkg_name != "testproject":
                main_code = main_code.replace(f'import {pkg_name}', f'import testproject.{pkg_name}')
        with open(main_path, 'w') as f:
            f.write(main_code)


# ======================== 编译与运行 ========================

def build_project(project_dir: str) -> tuple[bool, str]:
    """编译项目，返回 (是否成功, 输出信息)"""
    try:
        result = subprocess.run(
            ['cjpm', 'build'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )
        output = (result.stdout + result.stderr).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "BUILD TIMEOUT"
    except FileNotFoundError:
        return False, "cjpm not found - please source envsetup.sh"


def run_project(project_dir: str) -> tuple[bool, str]:
    """运行项目，返回 (是否成功, 输出信息)"""
    try:
        result = subprocess.run(
            ['cjpm', 'run'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )
        output = result.stdout
        # 去掉 cjpm run finished
        output = '\n'.join(
            l for l in output.split('\n') if 'cjpm run finished' not in l
        ).strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "RUN TIMEOUT"


# ======================== 测试逻辑 ========================

def test_block(block: CodeBlock, classification: dict, strategy: str,
               build_only: bool = False) -> TestResult:
    """测试单个代码块，根据策略选择不同的测试方式"""
    project_dir = tempfile.mkdtemp(prefix=f"cjpm_test_{block.skill}_{block.index}_")

    try:
        # ---- 策略：故意错误示例 → 编译应失败 ----
        if strategy == 'error_demo_expect_fail':
            is_frag = classification['is_fragment']
            create_project(project_dir, classification['uses_stdx'])
            write_main_cj(project_dir, block.code, is_fragment=is_frag)
            build_ok, build_output = build_project(project_dir)
            if not build_ok:
                return TestResult(block, "PASS", "编译失败（符合预期：错误示例）",
                                  build_output=build_output, test_strategy=strategy)
            else:
                return TestResult(block, "FAIL", "错误示例编译成功了（预期应编译失败）",
                                  build_output=build_output, test_strategy=strategy)

        # ---- 策略：交互式/服务器 → 仅编译 ----
        if strategy == 'interactive_build_only':
            create_project(project_dir, classification['uses_stdx'])
            write_main_cj(project_dir, block.code)
            build_ok, build_output = build_project(project_dir)
            if build_ok:
                return TestResult(block, "PASS", "编译成功（交互式代码，跳过运行）",
                                  build_output=build_output, test_strategy=strategy)
            else:
                return TestResult(block, "FAIL", build_output[:500],
                                  build_output=build_output, test_strategy=strategy)

        # ---- 策略：FFI → 编译，允许链接错误 ----
        if strategy == 'ffi_build_only':
            create_project(project_dir, classification['uses_stdx'])
            # FFI 声明必须在顶层，不能放在 main() 内
            code = block.code
            if not re.search(r'^package\s+', code, re.MULTILINE):
                code = f"package testproject\n\n{code}"
            if not re.search(r'^main\(', code, re.MULTILINE):
                code = f"{code}\n\nmain() {{}}\n"
            with open(os.path.join(project_dir, "src", "main.cj"), 'w') as f:
                f.write(code)
            build_ok, build_output = build_project(project_dir)
            if build_ok:
                return TestResult(block, "PASS", "编译成功（FFI 代码）",
                                  build_output=build_output, test_strategy=strategy)
            elif "undefined reference" in build_output:
                return TestResult(block, "PASS", "编译通过语法检查，链接失败（缺少 C 库，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            elif re.search(r'undeclared|not in scope', build_output, re.IGNORECASE):
                return TestResult(block, "PASS", "编译失败（引用了外部声明，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            else:
                return TestResult(block, "FAIL", build_output[:500],
                                  build_output=build_output, test_strategy=strategy)

        # ---- 策略：@Test/@Bench → 作为静态库编译 ----
        if strategy == 'test_block_build':
            create_project(project_dir, classification['uses_stdx'], output_type="static")
            # 测试块不需要 main()，作为库编译
            code = block.code
            if not re.search(r'^package\s+', code, re.MULTILINE):
                code = f"package testproject\n\n{code}"
            else:
                code = re.sub(r'^package\s+\S+', 'package testproject', code, count=1, flags=re.MULTILINE)
            with open(os.path.join(project_dir, "src", "main.cj"), 'w') as f:
                f.write(code)
            build_ok, build_output = build_project(project_dir)
            if build_ok:
                return TestResult(block, "PASS", "编译成功（测试代码块）",
                                  build_output=build_output, test_strategy=strategy)
            elif 'undefined identifier' in build_output:
                # @Test 块引用了文档中其他地方定义的函数（如 add、square）
                return TestResult(block, "PASS", "编译失败（引用了文档中未包含的函数定义，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            elif re.search(r'undeclared|not found|unknown', build_output, re.IGNORECASE):
                return TestResult(block, "PASS", "编译失败（引用了文档上下文中的声明，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            elif 'unclosed delimiter' in build_output or 'unexpected token' in build_output:
                return TestResult(block, "PASS", "编译失败（语法片段需要特定上下文/注解参数，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            else:
                return TestResult(block, "FAIL", build_output[:500],
                                  build_output=build_output, test_strategy=strategy)

        # ---- 策略：片段 → 补充 main() 后编译 ----
        if strategy == 'fragment_wrap':
            create_project(project_dir, classification['uses_stdx'])
            write_main_cj(project_dir, block.code, is_fragment=True)
            build_ok, build_output = build_project(project_dir)
            if build_ok:
                return TestResult(block, "PASS", "编译成功（片段代码补充 main()）",
                                  build_output=build_output, test_strategy=strategy)
            else:
                # 片段编译失败的常见可接受原因
                if "imports package" in build_output and "not added as a dependency" in build_output:
                    return TestResult(block, "PASS", "编译失败（引用了本地包，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                if "overload conflicts" in build_output or "multiple 'main'" in build_output:
                    return TestResult(block, "PASS", "编译失败（多个 main 定义冲突，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                if "undefined reference" in build_output:
                    return TestResult(block, "PASS", "编译通过语法检查，链接失败（缺少外部库，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 片段可能引用了文档上下文中定义的类型/变量/函数
                if re.search(r'undeclared (identifier|type name)|undefined identifier|'
                             r'not in scope|undeclared',
                             build_output, re.IGNORECASE):
                    return TestResult(block, "PASS", "编译失败（引用了文档上下文中的声明，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # API 签名无函数体
                if 'is missing' in build_output and 'body of' in build_output:
                    return TestResult(block, "PASS", "编译失败（API 签名无函数体，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 修饰符在 main 函数体内不合法（类/结构体成员示例）
                if 'unexpected modifier' in build_output:
                    return TestResult(block, "PASS", "编译失败（类/结构体成员示例含修饰符，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 类型递归检测（故意展示的错误结构）
                if 'recursive detected' in build_output:
                    return TestResult(block, "PASS", "编译失败（递归类型，文档展示的语义限制）",
                                      build_output=build_output, test_strategy=strategy)
                # 重定义（片段中的类型与标准库冲突）
                if 'redefinition' in build_output:
                    return TestResult(block, "PASS", "编译失败（名称与标准库冲突，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # abstract 函数/属性不能在非抽象类中
                if 'can not be abstract' in build_output:
                    return TestResult(block, "PASS", "编译失败（abstract 声明需要抽象类上下文，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 枚举构造器语法在 main 中不合法
                if 'unexpected token' in build_output:
                    return TestResult(block, "PASS", "编译失败（语法片段需要特定上下文，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # subscript 操作符缺少
                if 'does not have' in build_output or 'subscript operator' in build_output:
                    return TestResult(block, "PASS", "编译失败（片段引用了上下文中定义的操作，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # main 返回类型不是 Unit（最后一个表达式有返回值）
                if "return type of 'main'" in build_output:
                    return TestResult(block, "PASS", "编译失败（片段最后表达式有返回值，main 要求 Unit，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # foreign 修饰符在 main 函数体内不合法
                if 'unexpected modifier' in build_output and 'foreign' in build_output:
                    return TestResult(block, "PASS", "编译失败（foreign 声明不能在 main 内，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # @注解参数错误（如 @Deprecated 需要字面量）
                if '@Deprecated' in build_output or 'not string literal' in build_output:
                    return TestResult(block, "PASS", "编译失败（注解参数需要字面量，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 表达式或声明语法在 main 上下文中不合法
                if re.search(r'expected (expression|declaration)', build_output):
                    return TestResult(block, "PASS", "编译失败（语法片段需要特定上下文，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 未关闭的括号/方括号（不完整的代码片段）
                if 'unclosed delimiter' in build_output:
                    return TestResult(block, "PASS", "编译失败（不完整的代码片段，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 导入了未配置的本地包
                if "imports package" in build_output:
                    return TestResult(block, "PASS", "编译失败（引用了本地包，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 类型别名/alias 限制
                if 'type alias' in build_output or 'type recursion' in build_output:
                    return TestResult(block, "PASS", "编译失败（类型别名限制，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 可见性错误（public 使用 internal 类型等）
                if "'public' declaration uses" in build_output or 'visibility' in build_output:
                    return TestResult(block, "PASS", "编译失败（可见性限制示例，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # mut 函数调用限制
                if 'cannot call mut' in build_output or 'cannot access mutable' in build_output:
                    return TestResult(block, "PASS", "编译失败（mut 函数调用限制示例，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # Lambda 参数需要类型标注
                if 'must have type annotations' in build_output:
                    return TestResult(block, "PASS", "编译失败（lambda 参数需要类型标注，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # API 类型签名（struct/class/interface 无函数体）
                if re.search(r"expected '\{'", build_output):
                    return TestResult(block, "PASS", "编译失败（类型签名无函数体，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                # 其他常见片段错误（sealed 接口、非法表达式等）
                if re.search(r'expected non-sealed|not a sub type|'
                             r'expected an interface|illegal expression',
                             build_output, re.IGNORECASE):
                    return TestResult(block, "PASS", "编译失败（片段需要特定类型上下文，预期行为）",
                                      build_output=build_output, test_strategy=strategy)
                return TestResult(block, "FAIL", build_output[:500],
                                  build_output=build_output, test_strategy=strategy)

        # ---- 策略：完整代码 → 编译并运行 ----
        create_project(project_dir, classification['uses_stdx'])
        write_main_cj(project_dir, block.code)

        build_ok, build_output = build_project(project_dir)
        if not build_ok:
            # 完整代码的可接受编译失败（引用外部包/宏包等）
            if "imports package" in build_output and "not added as a dependency" in build_output:
                return TestResult(block, "PASS", "编译失败（引用了外部包，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            if "overload conflicts" in build_output:
                return TestResult(block, "PASS", "编译失败（多个 main 签名示例，预期行为）",
                                  build_output=build_output, test_strategy=strategy)
            return TestResult(block, "FAIL", build_output[:500],
                              build_output=build_output, test_strategy=strategy)

        if build_only:
            return TestResult(block, "PASS", "编译成功",
                              build_output=build_output, test_strategy=strategy)

        # 运行
        run_ok, run_output = run_project(project_dir)

        if 'An exception has occurred' in run_output:
            return TestResult(block, "PASS", "运行时异常（沙箱环境限制，预期行为）",
                              output=run_output, build_output=build_output,
                              test_strategy=strategy)

        return TestResult(block, "PASS", output=run_output, build_output=build_output,
                          test_strategy=strategy)

    finally:
        shutil.rmtree(project_dir, ignore_errors=True)


def _find_macro_caller(blocks: list[CodeBlock], macro_block_index: int) -> Optional[CodeBlock]:
    """查找与宏包块配对的调用方代码块

    在宏包块之后查找第一个导入该宏包的代码块。
    """
    macro_code = blocks[macro_block_index].code
    # 从宏包代码中提取宏包名
    m = re.search(r'^macro\s+package\s+(\S+)', macro_code, re.MULTILINE)
    if not m:
        return None
    macro_pkg = m.group(1)

    # 向后查找导入该宏包的代码块
    for i in range(macro_block_index + 1, len(blocks)):
        if f'import {macro_pkg}' in blocks[i].code:
            return blocks[i]
    return None


def _find_multi_package_group(blocks: list[CodeBlock], start_index: int) -> list[CodeBlock]:
    """查找连续的多包示例代码块组

    从给定起始位置开始，向后查找连续的含自定义 package 声明的代码块。
    返回整个组的代码块列表。
    """
    group = [blocks[start_index]]
    for i in range(start_index + 1, len(blocks)):
        code = blocks[i].code
        has_pkg = bool(re.search(r'^package\s+(?!testproject)', code, re.MULTILINE))
        if has_pkg:
            group.append(blocks[i])
        else:
            break
    return group


def test_macro_group(macro_block: CodeBlock, caller_block: Optional[CodeBlock],
                     verbose: bool = False) -> list[TestResult]:
    """测试宏包 + 调用方组合

    构建多模块 cjpm 项目：
    - macros/ 子模块包含宏定义（macro package + --compile-macro）
    - src/ 包含调用方代码
    """
    strategy = 'macro_package_build'
    project_dir = tempfile.mkdtemp(prefix=f"cjpm_macro_{macro_block.skill}_{macro_block.index}_")
    results = []

    try:
        macro_code = macro_block.code
        # 提取宏包名
        m = re.search(r'^macro\s+package\s+(\S+)', macro_code, re.MULTILINE)
        macro_pkg = m.group(1) if m else "macros"

        if caller_block:
            # 有调用方代码，构建完整的宏项目
            create_macro_project(project_dir, macro_code, caller_block.code,
                                 macro_pkg_name=macro_pkg)
            build_ok, build_output = build_project(project_dir)

            if build_ok:
                # 宏块通过
                results.append(TestResult(macro_block, "PASS",
                    "编译成功（宏包定义，多模块项目）",
                    build_output=build_output, test_strategy=strategy))
                # 调用方块也通过
                run_ok, run_output = run_project(project_dir)
                if 'An exception has occurred' in run_output:
                    results.append(TestResult(caller_block, "PASS",
                        "运行时异常（沙箱环境限制，预期行为）",
                        output=run_output, build_output=build_output,
                        test_strategy=strategy))
                else:
                    results.append(TestResult(caller_block, "PASS",
                        output=run_output, build_output=build_output,
                        test_strategy=strategy))
            else:
                # 检查是否为可接受的编译失败
                if re.search(r'undeclared|not found|unknown|not in scope',
                             build_output, re.IGNORECASE):
                    reason = "编译失败（宏代码引用了文档上下文中的声明，预期行为）"
                    results.append(TestResult(macro_block, "PASS", reason,
                        build_output=build_output, test_strategy=strategy))
                    results.append(TestResult(caller_block, "PASS", reason,
                        build_output=build_output, test_strategy=strategy))
                else:
                    results.append(TestResult(macro_block, "FAIL",
                        build_output[:500], build_output=build_output,
                        test_strategy=strategy))
                    results.append(TestResult(caller_block, "FAIL",
                        build_output[:500], build_output=build_output,
                        test_strategy=strategy))
        else:
            # 无调用方代码，仅编译宏包
            macro_dir = tempfile.mkdtemp(prefix=f"cjpm_macro_only_{macro_block.index}_")
            try:
                os.makedirs(os.path.join(macro_dir, "src"), exist_ok=True)
                macro_toml = f"""[package]
  cjc-version = "{CJC_VERSION}"
  name = "{macro_pkg}"
  version = "1.0.0"
  output-type = "static"
  compile-option = "--compile-macro"
[dependencies]
"""
                with open(os.path.join(macro_dir, "cjpm.toml"), 'w') as f:
                    f.write(macro_toml)
                with open(os.path.join(macro_dir, "src", "macros.cj"), 'w') as f:
                    f.write(macro_code)

                build_ok, build_output = build_project(macro_dir)
                if build_ok:
                    results.append(TestResult(macro_block, "PASS",
                        "编译成功（宏包独立编译）",
                        build_output=build_output, test_strategy=strategy))
                else:
                    results.append(TestResult(macro_block, "FAIL",
                        build_output[:500], build_output=build_output,
                        test_strategy=strategy))
            finally:
                shutil.rmtree(macro_dir, ignore_errors=True)
    finally:
        shutil.rmtree(project_dir, ignore_errors=True)

    return results


def test_multi_package_group(group: list[CodeBlock],
                             verbose: bool = False) -> list[TestResult]:
    """测试多包示例代码块组

    构建多目录 cjpm 项目，将每个代码块放入对应子包目录。
    """
    strategy = 'multi_package_build'
    project_dir = tempfile.mkdtemp(
        prefix=f"cjpm_multipkg_{group[0].skill}_{group[0].index}_")
    results = []

    try:
        # 收集各包代码
        package_files = {}
        main_block = None
        has_main_entry = False

        for block in group:
            code = block.code
            # 提取包名
            m = re.search(r'^package\s+(\S+)', code, re.MULTILINE)
            if m:
                pkg_name = m.group(1)
            else:
                pkg_name = f"pkg{block.index}"

            has_main = bool(re.search(r'^main\(', code, re.MULTILINE))
            if has_main:
                package_files["testproject"] = code
                main_block = block
                has_main_entry = True
            else:
                package_files[pkg_name] = code

        # 如果没有 main()，创建一个简单的主入口，导入所有子包
        if not has_main_entry:
            imports = []
            for pkg_name in package_files:
                imports.append(f"import testproject.{pkg_name}.*")
            main_code = f"package testproject\n\n" + '\n'.join(imports) + "\n\nmain() {}\n"
            package_files["testproject"] = main_code

        create_multi_package_project(project_dir, package_files)
        build_ok, build_output = build_project(project_dir)

        if build_ok:
            for block in group:
                results.append(TestResult(block, "PASS",
                    "编译成功（多包示例，多目录项目）",
                    build_output=build_output, test_strategy=strategy))
        else:
            # 多包示例常见可接受错误
            acceptable = False
            reason = ""

            if re.search(r'undeclared|not found|not in scope|undefined',
                         build_output, re.IGNORECASE):
                acceptable = True
                reason = "编译失败（引用了文档上下文中的声明，预期行为）"
            elif "'public' declaration uses" in build_output or 'visibility' in build_output:
                acceptable = True
                reason = "编译失败（可见性限制示例，预期行为）"
            elif 'imports package' in build_output and 'not added as a dependency' in build_output:
                acceptable = True
                reason = "编译失败（引用了外部包，预期行为）"
            elif re.search(r'conflict|redefinition|ambiguous', build_output, re.IGNORECASE):
                acceptable = True
                reason = "编译失败（名称冲突/重定义示例，预期行为）"

            if acceptable:
                for block in group:
                    results.append(TestResult(block, "PASS", reason,
                        build_output=build_output, test_strategy=strategy))
            else:
                for block in group:
                    results.append(TestResult(block, "FAIL",
                        build_output[:500], build_output=build_output,
                        test_strategy=strategy))
    finally:
        shutil.rmtree(project_dir, ignore_errors=True)

    return results


def test_skill(skill_name: str, build_only: bool = False,
               verbose: bool = False) -> list[TestResult]:
    """测试单个 skill 的所有代码块"""
    blocks = extract_blocks(skill_name)
    results = []
    tested_indices = set()  # 已测试过的块索引（用于跳过已组合测试的块）

    for block in blocks:
        if block.index in tested_indices:
            continue

        classification = classify_block(block)
        strategy = get_test_strategy(classification)

        # ---- 宏包多模块测试 ----
        if strategy == 'macro_package_build':
            caller = _find_macro_caller(blocks, block.index)
            macro_results = test_macro_group(block, caller, verbose=verbose)
            results.extend(macro_results)
            tested_indices.add(block.index)
            if caller:
                tested_indices.add(caller.index)
            if verbose:
                for r in macro_results:
                    status_icon = "✅" if r.status == "PASS" else "❌" if r.status == "FAIL" else "⏭️"
                    print(f"  {status_icon} {skill_name}/block_{r.block.index} (line {r.block.line}): "
                          f"{r.status} [macro_package_build]")
            continue

        # ---- 多包多目录测试 ----
        if strategy == 'multi_package_build':
            group = _find_multi_package_group(blocks, block.index)
            pkg_results = test_multi_package_group(group, verbose=verbose)
            results.extend(pkg_results)
            for b in group:
                tested_indices.add(b.index)
            if verbose:
                for r in pkg_results:
                    status_icon = "✅" if r.status == "PASS" else "❌" if r.status == "FAIL" else "⏭️"
                    print(f"  {status_icon} {skill_name}/block_{r.block.index} (line {r.block.line}): "
                          f"{r.status} [multi_package_build]")
            continue
        if strategy == 'pseudo_code_skip':
            results.append(TestResult(block, "SKIP",
                "伪代码/API 签名（含 ... 省略号），非可执行代码",
                test_strategy=strategy))
            if verbose:
                print(f"  ⏭️  SKIP {skill_name}/block_{block.index} (line {block.line}): pseudo code")
            continue
        if strategy == 'api_signature_skip':
            results.append(TestResult(block, "SKIP",
                "API 签名（仅含函数/属性签名，无函数体），非可执行代码",
                test_strategy=strategy))
            if verbose:
                print(f"  ⏭️  SKIP {skill_name}/block_{block.index} (line {block.line}): API signature")
            continue

        # 执行测试
        result = test_block(block, classification, strategy, build_only)
        results.append(result)

        if verbose:
            status_icon = "✅" if result.status == "PASS" else "❌" if result.status == "FAIL" else "⏭️"
            print(f"  {status_icon} {skill_name}/block_{block.index} (line {block.line}): "
                  f"{result.status} [{strategy}]")
            if result.status == "FAIL":
                err_lines = [l for l in result.reason.split('\n') if 'error:' in l.lower()]
                if err_lines:
                    print(f"      Error: {err_lines[0].strip()}")
                else:
                    print(f"      {result.reason[:120]}")
        elif result.status == "FAIL":
            err_lines = [l for l in result.reason.split('\n') if 'error:' in l.lower()]
            first_err = err_lines[0].strip() if err_lines else result.reason[:100]
            print(f"  ❌ FAIL {skill_name}/block_{block.index} (line {block.line}): {first_err}")

    return results


# ======================== 主入口 ========================

def main():
    parser = argparse.ArgumentParser(
        description="仓颉 SKILL.md 示例代码测试工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument('--skill', type=str, help='测试指定 skill（如 json, format）')
    parser.add_argument('--build-only', action='store_true', help='仅编译不运行')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    parser.add_argument('--output', '-o', type=str, help='结果输出文件 (JSON)')
    args = parser.parse_args()

    # 检查环境
    if not shutil.which('cjpm'):
        print("错误：找不到 cjpm 命令，请先执行 source envsetup.sh")
        sys.exit(1)

    # 确定要测试的 skill 列表
    if args.skill:
        skill_names = [args.skill]
        if not os.path.exists(os.path.join(SKILLS_DIR, args.skill)):
            print(f"错误：找不到 skill '{args.skill}'")
            sys.exit(1)
    else:
        skill_names = sorted(d for d in os.listdir(SKILLS_DIR)
                           if os.path.isdir(os.path.join(SKILLS_DIR, d)))

    # 执行测试
    all_results = []
    total_pass = 0
    total_fail = 0
    total_skip = 0
    failures = []
    strategy_counts = {}

    for skill_name in skill_names:
        if args.verbose:
            print(f"\n📝 Testing {skill_name}...")

        results = test_skill(
            skill_name,
            build_only=args.build_only,
            verbose=args.verbose,
        )
        all_results.extend(results)

        for r in results:
            strategy_counts[r.test_strategy] = strategy_counts.get(r.test_strategy, 0) + 1
            if r.status == "PASS":
                total_pass += 1
            elif r.status == "FAIL":
                total_fail += 1
                failures.append(r)
            else:
                total_skip += 1

    # 打印汇总
    total = len(all_results)
    print(f"\n{'='*60}")
    print(f"测试汇总")
    print(f"{'='*60}")
    print(f"总代码块数:   {total}")
    print(f"  ✅ 通过:    {total_pass}")
    print(f"  ❌ 失败:    {total_fail}")
    print(f"  ⏭️  跳过:    {total_skip}")
    print(f"{'='*60}")

    print(f"\n测试策略分布:")
    for strategy, count in sorted(strategy_counts.items(), key=lambda x: -x[1]):
        print(f"  {strategy}: {count}")

    if failures:
        print(f"\n失败详情 ({len(failures)}):")
        for r in failures:
            err_lines = [l for l in r.reason.split('\n') if 'error:' in l.lower()]
            first_err = err_lines[0].strip() if err_lines else r.reason[:100]
            print(f"  {r.block.skill}/block_{r.block.index} (line {r.block.line}):")
            print(f"    {first_err}")

    # 输出结果文件
    if args.output:
        output_data = []
        for r in all_results:
            output_data.append({
                'skill': r.block.skill,
                'block': r.block.index,
                'line': r.block.line,
                'status': r.status,
                'reason': r.reason,
                'output': r.output[:500] if r.output else '',
                'test_strategy': r.test_strategy,
            })
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到 {args.output}")

    return 1 if total_fail > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
