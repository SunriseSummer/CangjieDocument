"""
Markdown 解析模块

从 Markdown 文件中提取带标注的代码块，解析标注选项，检测未标注的代码块。
"""

import re

from .models import (
    CodeBlock,
    CHECK_ANNOTATION_RE,
    EXPECTED_OUTPUT_RE,
    HEADING_RE,
)


def parse_options(option_str: str) -> dict:
    """解析标注中的 key=value 选项"""
    opts = {}
    if not option_str:
        return opts
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
    annotated_line_set = set()

    while i < len(lines):
        line = lines[i]

        ann_match = CHECK_ANNOTATION_RE.search(line)
        if ann_match:
            directive = ann_match.group('directive')
            options = parse_options(ann_match.group('options') or '')
            project = options.get('project')
            file_path = options.get('file')
            block_lang = options.get('lang', 'cangjie')
            block_type = options.get('type')

            # 向后查找紧跟的代码块
            j = i + 1
            while j < len(lines) and lines[j].strip() == '':
                j += 1

            detected_lang = None
            if j < len(lines):
                fence_line = lines[j].strip()
                if fence_line.startswith('```cangjie'):
                    detected_lang = 'cangjie'
                elif fence_line.startswith('```c'):
                    detected_lang = 'c'

            if detected_lang:
                if detected_lang != 'cangjie':
                    block_lang = detected_lang
                annotated_line_set.add(j)
                code_lines = []
                k = j + 1
                while k < len(lines) and lines[k].strip() != '```':
                    code_lines.append(lines[k])
                    k += 1
                code = '\n'.join(code_lines)

                # 查找紧跟代码块后的 expected_output
                expected_output = None
                m = k + 1
                while m < len(lines) and lines[m].strip() == '':
                    m += 1
                if m < len(lines):
                    remaining = '\n'.join(lines[m:])
                    eo_match = EXPECTED_OUTPUT_RE.match(remaining)
                    if eo_match:
                        expected_output = eo_match.group('output')
                        expected_output = expected_output.rstrip('\n')

                heading = find_heading_for_position(
                    content, sum(len(l) + 1 for l in lines[:i])
                )
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

    # 第二遍扫描：找出未标注的 cangjie 代码块
    line_offsets = []
    offset = 0
    for l in lines:
        line_offsets.append(offset)
        offset += len(l) + 1

    for idx, line in enumerate(lines):
        if line.strip().startswith('```cangjie') and idx not in annotated_line_set:
            heading = find_heading_for_position(content, line_offsets[idx])
            preview = ''
            k = idx + 1
            while k < len(lines) and lines[k].strip() != '```':
                if lines[k].strip() and not preview:
                    preview = lines[k].strip()[:60]
                k += 1
            unannotated.append((idx + 1, heading, preview))

    return blocks, unannotated
