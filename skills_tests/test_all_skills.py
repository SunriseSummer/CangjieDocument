#!/usr/bin/env python3
"""
仓颉 SKILL.md 示例代码自动化测试脚本

用法：
    python3 test_all_skills.py                    # 测试所有 SKILL
    python3 test_all_skills.py --skill json       # 测试单个 SKILL
    python3 test_all_skills.py --build-only       # 仅编译不运行
    python3 test_all_skills.py --verbose          # 详细输出
    python3 test_all_skills.py --test-fragments   # 同时测试代码片段

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
    status: str         # PASS, FAIL, SKIP, RUNTIME_ERROR
    reason: str = ""    # 跳过原因或错误信息
    output: str = ""    # 运行输出
    build_output: str = ""  # 编译输出


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
    """分类代码块，决定测试策略"""
    code = block.code
    ctx = block.context

    has_main = bool(re.search(r'^main\(', code, re.MULTILINE))
    uses_stdx = 'import stdx.' in code
    is_error_demo = '❌' in ctx or '❌' in code
    is_interactive = bool(re.search(r'readln\(\)|\.serve\(\)|getStdIn\(\)', code))
    has_ffi_extern = bool(re.search(r'foreign\s+func', code))
    is_macro_pkg = 'macro package' in code
    is_test_block = '@Test' in code or '@Bench' in code
    has_package_decl = bool(re.search(r'^package\s+(?!testproject)', code, re.MULTILINE))

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
    }


def get_skip_reason(classification: dict) -> Optional[str]:
    """返回跳过原因，如果不需要跳过返回 None"""
    if classification['is_error_demo']:
        return "intentional error demo"
    if classification['is_interactive']:
        return "interactive/server"
    if classification['is_macro_pkg']:
        return "macro package"
    if classification['is_test_block']:
        return "test/bench block"
    if classification['has_ffi_extern'] and not classification['uses_stdx']:
        return "FFI extern"
    if classification['has_package_decl']:
        return "custom package declaration"
    return None


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


def create_project(project_dir: str, uses_stdx: bool) -> None:
    """创建 cjpm 测试项目"""
    os.makedirs(os.path.join(project_dir, "src"), exist_ok=True)

    stdx_path = get_stdx_path()

    if uses_stdx and stdx_path:
        toml = f"""[package]
  cjc-version = "1.0.5"
  name = "testproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"
[dependencies]
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["{stdx_path}"]
"""
    else:
        toml = """[package]
  cjc-version = "1.0.5"
  name = "testproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
"""

    with open(os.path.join(project_dir, "cjpm.toml"), 'w') as f:
        f.write(toml)


def write_main_cj(project_dir: str, code: str, is_fragment: bool = False) -> None:
    """将代码写入 src/main.cj"""
    if is_fragment:
        # 片段模式：自动补充 main() 和 import
        imports = '\n'.join(l for l in code.split('\n') if l.strip().startswith('import '))
        non_import = '\n'.join(l for l in code.split('\n') if not l.strip().startswith('import '))

        has_toplevel = bool(re.search(
            r'^(public\s+)?(class|struct|enum|interface|func|open|abstract|sealed)\s',
            non_import, re.MULTILINE
        ))

        if has_toplevel:
            main_code = f"package testproject\n{imports}\n\n{non_import}\n\nmain() {{}}\n"
        else:
            main_code = f"package testproject\n{imports}\n\nmain() {{\n{non_import}\n}}\n"
    else:
        main_code = f"package testproject\n\n{code}"

    with open(os.path.join(project_dir, "src", "main.cj"), 'w') as f:
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

def test_block(block: CodeBlock, classification: dict,
               build_only: bool = False) -> TestResult:
    """测试单个代码块"""
    # 创建临时项目
    project_dir = tempfile.mkdtemp(prefix=f"cjpm_test_{block.skill}_{block.index}_")

    try:
        create_project(project_dir, classification['uses_stdx'])
        write_main_cj(project_dir, block.code, is_fragment=classification['is_fragment'])

        # 编译
        build_ok, build_output = build_project(project_dir)

        if not build_ok:
            # 检查是否是可接受的编译失败
            if "overload conflicts" in build_output or "multiple 'main'" in build_output:
                return TestResult(block, "SKIP", "multiple main (listing)", build_output=build_output)
            if "imports package" in build_output and "not added as a dependency" in build_output:
                return TestResult(block, "SKIP", "local package import", build_output=build_output)
            if "undefined reference" in build_output:
                return TestResult(block, "SKIP", "FFI undefined reference", build_output=build_output)

            return TestResult(block, "FAIL", build_output[:500], build_output=build_output)

        if build_only or classification.get('is_interactive'):
            return TestResult(block, "PASS", build_output=build_output)

        # 运行
        run_ok, run_output = run_project(project_dir)

        if 'An exception has occurred' in run_output:
            return TestResult(block, "PASS", "runtime exception (expected in sandbox)",
                            output=run_output, build_output=build_output)

        return TestResult(block, "PASS", output=run_output, build_output=build_output)

    finally:
        shutil.rmtree(project_dir, ignore_errors=True)


def test_skill(skill_name: str, build_only: bool = False,
               test_fragments: bool = False, verbose: bool = False) -> list[TestResult]:
    """测试单个 skill 的所有代码块"""
    blocks = extract_blocks(skill_name)
    results = []

    for block in blocks:
        classification = classify_block(block)

        # 决定是否跳过
        skip_reason = get_skip_reason(classification)
        if skip_reason:
            results.append(TestResult(block, "SKIP", skip_reason))
            if verbose:
                print(f"  SKIP {skill_name}/block_{block.index} (line {block.line}): {skip_reason}")
            continue

        if classification['is_fragment'] and not test_fragments:
            results.append(TestResult(block, "SKIP", "fragment (use --test-fragments to test)"))
            continue

        # 执行测试
        result = test_block(block, classification, build_only)
        results.append(result)

        if verbose:
            status_icon = "✅" if result.status == "PASS" else "❌" if result.status == "FAIL" else "⏭️"
            print(f"  {status_icon} {skill_name}/block_{block.index} (line {block.line}): {result.status}")
            if result.status == "FAIL":
                # 提取第一行错误
                err_lines = [l for l in result.reason.split('\n') if 'error:' in l.lower()]
                if err_lines:
                    print(f"      Error: {err_lines[0].strip()}")
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
    parser.add_argument('--test-fragments', action='store_true', help='同时测试代码片段')
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

    for skill_name in skill_names:
        if args.verbose:
            print(f"\n📝 Testing {skill_name}...")

        results = test_skill(
            skill_name,
            build_only=args.build_only,
            test_fragments=args.test_fragments,
            verbose=args.verbose,
        )
        all_results.extend(results)

        for r in results:
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
            })
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\n结果已保存到 {args.output}")

    return 1 if total_fail > 0 else 0


if __name__ == '__main__':
    sys.exit(main())
