#!/usr/bin/env python3
"""
check/main.py — 仓颉 Markdown 文档示例代码提取、构建和验证工具

从指定目录下的 Markdown 文档中提取带有 <!-- check:xxx --> 标注的仓颉代码块，
自动生成 cjpm 项目并编译运行，验证示例代码的正确性。

用法:
    python3 -m check [选项] [目录]

详细说明参见 check/readme.md。
"""

import os
import shutil
import sys
from pathlib import Path

from .cli import (
    build_parser, check_cjpm_available, find_md_files,
    print_summary, save_json,
)
from .parser import extract_code_blocks
from .assembler import blocks_to_testcases, make_project_name
from .project import create_cjpm_project
from .runner import run_testcase, check_ast
from .report import generate_report


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.extract_only:
        check_cjpm_available()

    scan_dir = args.dir
    if args.subdir:
        scan_dir = os.path.join(args.dir, args.subdir)

    if args.file:
        md_files = args.file
    else:
        md_files = find_md_files(scan_dir)

    if not md_files:
        print(f"No markdown files found in '{scan_dir}'")
        sys.exit(0)

    output_base = Path(args.output_dir)
    output_base.mkdir(parents=True, exist_ok=True)

    total = 0
    passed = 0
    failed = 0
    skipped = 0
    unannotated_total = 0
    unannotated_warnings = []
    errors = []
    all_results = []

    print(f"📖 扫描文档目录: {scan_dir}")
    print(f"📁 输出目录: {output_base}")
    print(f"📄 找到 {len(md_files)} 个文档文件\n")

    for md_file in md_files:
        blocks, unannotated = extract_code_blocks(md_file)

        if unannotated:
            unannotated_total += len(unannotated)
            for line_no, heading, preview in unannotated:
                unannotated_warnings.append(
                    (md_file, line_no, heading, preview)
                )

        if not blocks and not unannotated:
            continue

        try:
            rel = Path(md_file).relative_to(args.dir)
        except ValueError:
            rel = Path(md_file).name
        doc_output_dir = output_base / rel.parent

        testcases = blocks_to_testcases(blocks, md_file)

        rel_display = str(rel)
        skip_count = sum(1 for b in blocks if b.directive == 'skip')
        ast_blocks = [b for b in blocks if b.directive == 'ast']
        if skip_count > 0:
            skipped += skip_count

        unannotated_count = len(unannotated) if unannotated else 0
        info_parts = []
        if testcases:
            info_parts.append(f"{len(testcases)} 个测试用例")
        if ast_blocks:
            if args.skip_ast:
                info_parts.append(
                    f"{len(ast_blocks)} 个语法检查(已跳过)"
                )
                skipped += len(ast_blocks)
            else:
                info_parts.append(f"{len(ast_blocks)} 个语法检查")
        if skip_count:
            info_parts.append(f"{skip_count} 个跳过")
        if unannotated_count:
            info_parts.append(f"{unannotated_count} 个未标注")

        detail = (
            f" ({', '.join(info_parts)})" if info_parts else ""
        )
        print(f"  📄 {rel_display}:{detail}")

        # AST 语法检查
        if not args.skip_ast:
            for b in ast_blocks:
                total += 1
                ast_name = make_project_name(
                    md_file, b.heading, b.block_index
                )
                ast_ok, ast_errors = check_ast(b.code)
                ast_result = {
                    'name': ast_name,
                    'directive': 'ast',
                    'source_file': b.source_file,
                    'heading': b.heading,
                    'status': 'PASS' if ast_ok else 'FAIL',
                    'build_ok': ast_ok,
                    'run_ok': False,
                    'build_output': '',
                    'run_output': '',
                    'error': '',
                    'expected_output': None,
                    'output_match': None,
                }
                if not ast_ok:
                    error_details = '; '.join(
                        f'line {ln}:{col}'
                        for ln, col, _, _ in ast_errors
                    )
                    ast_result['error'] = (
                        f'Syntax errors found: {error_details}'
                    )
                    ast_result['build_output'] = (
                        f'tree-sitter detected '
                        f'{len(ast_errors)} syntax error(s):\n'
                        + '\n'.join(
                            f'  line {ln}:{col} - line {eln}:{ecol}'
                            for ln, col, eln, ecol in ast_errors
                        )
                    )

                all_results.append(ast_result)
                if ast_result['status'] == 'PASS':
                    passed += 1
                    if args.verbose:
                        print(f"    ✅ AST PASS: {ast_name}")
                else:
                    failed += 1
                    errors.append(ast_result)
                    print(f"    ❌ AST FAIL: {ast_name}")
                    if args.verbose:
                        print(f"       {ast_result['error']}")

        # 构建运行测试用例
        for tc in testcases:
            total += 1
            create_cjpm_project(tc, doc_output_dir)

            if args.extract_only:
                if args.verbose:
                    print(f"    ✅ 已提取: {tc.name}")
                continue

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
    print_summary(
        args, total, passed, failed, skipped, errors,
        unannotated_warnings, unannotated_total,
    )

    # 输出 JSON
    save_json(args, all_results, unannotated_warnings)

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
