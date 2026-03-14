"""
测试执行模块

执行测试用例（编译/运行），进行 tree-sitter AST 语法检查。
"""

import subprocess
import textwrap
from pathlib import Path

from .models import TestCase
from .project import compile_c_files


# ============================================================
# tree-sitter AST 语法检查
# ============================================================

_ts_parser = None


def _get_ts_parser():
    """延迟初始化 tree-sitter 仓颉解析器"""
    global _ts_parser
    if _ts_parser is not None:
        return _ts_parser
    try:
        import tree_sitter_cangjie as tsc
        import tree_sitter
        lang = tsc.language()
        _ts_parser = tree_sitter.Parser(tree_sitter.Language(lang))
        return _ts_parser
    except ImportError:
        return None


def _find_ts_errors(node) -> list:
    """递归查找语法树中的 ERROR 节点"""
    errors = []
    if node.type == 'ERROR' or node.is_missing:
        errors.append((
            node.start_point[0] + 1,
            node.start_point[1],
            node.end_point[0] + 1,
            node.end_point[1],
        ))
    for child in node.children:
        errors.extend(_find_ts_errors(child))
    return errors


def check_ast(code: str) -> tuple:
    """使用 tree-sitter 对仓颉代码做语法解析检查。

    返回 (ok, errors)：
        ok: bool — 语法是否正确
        errors: list — [(line, col, end_line, end_col), ...]
    """
    parser = _get_ts_parser()
    if parser is None:
        return True, []
    tree = parser.parse(code.encode('utf-8'))
    if not tree.root_node.has_error:
        return True, []
    errors = _find_ts_errors(tree.root_node)
    return False, errors


# ============================================================
# 测试执行
# ============================================================

def run_testcase(tc: TestCase, timeout_build: int = 60,
                 timeout_run: int = 30, verbose: bool = False) -> dict:
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
        c_ok, c_output = compile_c_files(proj_dir, tc.c_files)
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
        result['build_output'] = (
            build_proc.stdout + build_proc.stderr
        ).strip()
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
        _execute_run(tc, result, proj_dir, timeout_run)
    elif tc.directive == 'build_only':
        result['status'] = 'PASS'
    else:
        result['status'] = 'PASS'

    return result


def _execute_run(tc: TestCase, result: dict, proj_dir: Path,
                 timeout_run: int):
    """执行 cjpm run 并校验输出"""
    try:
        run_proc = subprocess.run(
            ['cjpm', 'run'],
            cwd=str(proj_dir),
            capture_output=True,
            text=True,
            timeout=timeout_run,
        )
        stdout_lines = run_proc.stdout.strip().split('\n')
        actual_lines = []
        for line in stdout_lines:
            if line.strip() in ('cjpm run finished', ''):
                continue
            actual_lines.append(line)
        actual_output = '\n'.join(actual_lines)

        result['run_output'] = actual_output
        stderr_text = run_proc.stderr.strip()
        has_runtime_exception = 'An exception has occurred' in stderr_text
        result['run_ok'] = (
            (run_proc.returncode == 0) and not has_runtime_exception
        )

        if tc.directive == 'runtime_error':
            if not has_runtime_exception and run_proc.returncode == 0:
                result['status'] = 'FAIL'
                result['error'] = (
                    'Expected runtime error but run succeeded'
                )
            else:
                result['status'] = 'PASS'
            return

        if not result['run_ok']:
            result['status'] = 'FAIL'
            result['error'] = f'Run failed: {stderr_text}'
            return

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
                result['error'] = (
                    f'Output mismatch:\n'
                    f'  Expected:\n{textwrap.indent(expected, "    ")}\n'
                    f'  Actual:\n{textwrap.indent(actual, "    ")}'
                )
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
