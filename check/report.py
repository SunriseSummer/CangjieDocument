"""
测试报告生成模块

在输出目录下生成人类友好的 report.md 测试报告。
"""

import textwrap
from datetime import datetime, timezone
from pathlib import Path


def generate_report(
    output_dir: Path,
    scan_dir: str,
    all_results: list,
    unannotated_warnings: list,
    skipped: int,
    md_files: list,
) -> Path:
    """在输出目录下生成测试报告 report.md。

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

        lines.append('| 指标 | 数量 |')
        lines.append('|------|------|')
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
            file_fail = sum(1 for r in results if r['status'] == 'FAIL')
            file_icon = '✅' if file_fail == 0 else '❌'
            lines.append(f'### {file_icon} `{src_file}`\n')
            lines.append('| 测试用例 | 类型 | 结果 |')
            lines.append('|----------|------|------|')
            for r in results:
                icon = '✅' if r['status'] == 'PASS' else '❌'
                directive = r['directive']
                name_display = (
                    r['heading'] if r['heading'] != 'unknown'
                    else r['name']
                )
                lines.append(
                    f'| {name_display} | `{directive}` '
                    f'| {icon} {r["status"]} |'
                )
            lines.append('')

    # 失败详情
    failed_results = [r for r in all_results if r['status'] == 'FAIL']
    if failed_results:
        lines.append('## 失败详情\n')
        for r in failed_results:
            lines.append(f'### ❌ {r["name"]}\n')
            lines.append(
                f'- **来源**: `{r["source_file"]}` > {r["heading"]}'
            )
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
        lines.append(
            '以下代码块缺少 `<!-- check:xxx -->` 标注，请补全：\n'
        )
        lines.append('| 文件 | 行号 | 章节 | 代码预览 |')
        lines.append('|------|------|------|----------|')
        for filepath, line_no, heading, preview in unannotated_warnings:
            safe_preview = (
                (preview or '')
                .replace('|', '\\|')
                .replace('\n', ' ')
                .replace('`', "'")[:60]
            )
            lines.append(
                f'| `{filepath}` | {line_no} | {heading} '
                f'| `{safe_preview}` |'
            )
        lines.append('')

    report_path = output_dir / 'report.md'
    report_path.write_text('\n'.join(lines), encoding='utf-8')
    return report_path
