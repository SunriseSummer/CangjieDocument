"""
命令行接口模块

定义命令行参数、摘要输出和文件查找功能。
"""

import argparse
import json
import subprocess
import sys
import textwrap
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器"""
    parser = argparse.ArgumentParser(
        description='仓颉 Markdown 文档示例代码提取、构建和验证工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''\
            标注格式:
              <!-- check:run -->                 编译并运行，应当成功
              <!-- check:compile_error -->        预期编译失败
              <!-- check:runtime_error -->        预期运行时错误
              <!-- check:build_only -->           仅编译，不运行
              <!-- check:ast -->                  使用 tree-sitter 做语法解析检查
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
        'dir', nargs='?', default='.',
        help='文档目录路径 (默认: 当前目录)',
    )
    parser.add_argument(
        '-o', '--output-dir', default='check_output',
        help='提取的示例代码存放路径 (默认: check_output)',
    )
    parser.add_argument(
        '-f', '--file', action='append',
        help='只处理指定的文档文件（可多次指定）',
    )
    parser.add_argument(
        '-s', '--subdir',
        help='只处理指定的子目录（如 begin, begin-v2）',
    )
    parser.add_argument(
        '--clean', action='store_true',
        help='测试完成后清理生成的项目目录',
    )
    parser.add_argument(
        '--extract-only', action='store_true',
        help='仅提取代码，不构建运行',
    )
    parser.add_argument(
        '--skip-ast', action='store_true',
        help='跳过 check:ast 语法解析检查',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='显示详细输出',
    )
    parser.add_argument(
        '--json', metavar='FILE',
        help='将测试结果输出为 JSON 文件',
    )
    return parser


def check_cjpm_available():
    """检查 cjpm 是否可用"""
    try:
        subprocess.run(['cjpm', '--help'], capture_output=True, timeout=10)
    except FileNotFoundError:
        print(
            "Error: cjpm 命令不可用。"
            "请先 source envsetup.sh 配置环境。",
            file=sys.stderr,
        )
        sys.exit(1)


def find_md_files(base_dir: str) -> list:
    """查找目录下所有 Markdown 文件"""
    files = []
    base_path = Path(base_dir)
    if not base_path.exists():
        print(
            f"Error: directory '{base_dir}' not found",
            file=sys.stderr,
        )
        sys.exit(1)
    for md_file in sorted(base_path.rglob('*.md')):
        files.append(str(md_file))
    return files


def print_summary(args, total, passed, failed, skipped, errors,
                  unannotated_warnings, unannotated_total):
    """输出测试摘要信息"""
    print(f"\n{'='*60}")
    if args.extract_only:
        print(f"📊 提取完成: {total} 个测试用例已创建")
        if skipped:
            print(f"   ⏭️  跳过: {skipped} 个代码块")
    else:
        print(
            f"📊 测试结果: {passed} 通过 / {failed} 失败 "
            f"/ {skipped} 跳过 (共 {total} 个)"
        )

        if errors:
            print(f"\n{'='*60}")
            print("❌ 失败详情:\n")
            for r in errors:
                print(f"  [{r['directive']}] {r['name']}")
                print(
                    f"    来源: {r['source_file']} > {r['heading']}"
                )
                print(f"    错误: {r['error']}")
                if r['build_output'] and not r['build_ok']:
                    print(
                        f"    编译输出:\n"
                        f"{textwrap.indent(r['build_output'], '      ')}"
                    )
                print()

    if unannotated_warnings:
        print(f"\n{'='*60}")
        print(
            f"⚠️  发现 {unannotated_total} "
            f"个未标注的 cangjie 代码块:\n"
        )
        for filepath, line_no, heading, preview in unannotated_warnings:
            print(f"  {filepath}:{line_no}  (章节: {heading})")
            if preview:
                print(f"    {preview}")
        print(
            f"\n   请为这些代码块添加 <!-- check:xxx --> 标注。"
        )


def save_json(args, all_results, unannotated_warnings):
    """保存 JSON 格式的测试结果"""
    if args.json:
        json_data = {
            'results': all_results,
            'unannotated': [
                {'file': f, 'line': ln, 'heading': h, 'preview': p}
                for f, ln, h, p in unannotated_warnings
            ],
        }
        with open(args.json, 'w', encoding='utf-8') as jf:
            json.dump(json_data, jf, ensure_ascii=False, indent=2)
        print(f"\n📋 测试结果已保存到: {args.json}")
