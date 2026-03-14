"""
测试用例组装模块

将解析得到的 CodeBlock 列表组装成可执行的 TestCase 列表。
"""

import re
from pathlib import Path
from typing import Optional

from .models import CodeBlock, TestCase


def _sanitize(s: str) -> str:
    """将字符串转为安全的目录名"""
    s = re.sub(r'[^\w\u4e00-\u9fff-]', '_', s)
    s = re.sub(r'_+', '_', s).strip('_')
    return s[:60] if s else 'unnamed'


def make_project_name(md_path: str, heading: str, index: int,
                      project: str = None) -> str:
    """生成项目目录名"""
    base = Path(md_path).stem
    parts = [base]
    if heading and heading != 'unknown':
        parts.append(_sanitize(heading))
    parts.append(f'block{index}')
    if project:
        parts.append(_sanitize(project))
    return '__'.join(parts)


def blocks_to_testcases(blocks: list, md_path: str) -> list:
    """将代码块组装成测试用例"""
    testcases = []
    project_blocks = {}
    standalone_blocks = []

    for b in blocks:
        if b.directive in ('skip', 'ast'):
            continue
        if b.project:
            project_blocks.setdefault(b.project, []).append(b)
        else:
            standalone_blocks.append(b)

    # 处理独立代码块
    for b in standalone_blocks:
        name = make_project_name(md_path, b.heading, b.block_index)
        if b.lang == 'c':
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
        directive = 'run'
        expected_output = None
        for b in proj_blocks:
            if b.directive != 'skip':
                directive = b.directive
            if b.expected_output is not None:
                expected_output = b.expected_output

        cj_blocks = [b for b in proj_blocks if b.lang == 'cangjie']
        c_blocks = [b for b in proj_blocks if b.lang == 'c']
        has_macro_def = any(b.block_type == 'macro' for b in proj_blocks)

        files = {}
        if has_macro_def:
            macro_cj_blocks = [b for b in cj_blocks if b.block_type == 'macro']
            main_cj_blocks = [b for b in cj_blocks if b.block_type != 'macro']

            if any(b.file_path for b in macro_cj_blocks):
                for b in macro_cj_blocks:
                    fp = b.file_path or 'src/macros.cj'
                    files[fp] = b.code
            else:
                macro_combined = '\n\n'.join(b.code for b in macro_cj_blocks)
                files['__macro_src__'] = macro_combined

            if any(b.file_path for b in main_cj_blocks):
                for b in main_cj_blocks:
                    fp = b.file_path or 'src/main.cj'
                    files[fp] = b.code
            elif main_cj_blocks:
                main_combined = '\n\n'.join(b.code for b in main_cj_blocks)
                files['src/main.cj'] = main_combined
        elif any(b.file_path for b in cj_blocks):
            for b in cj_blocks:
                fp = b.file_path or 'src/main.cj'
                files[fp] = b.code
        else:
            combined = '\n\n'.join(b.code for b in cj_blocks)
            files['src/main.cj'] = combined

        c_files = {}
        for b in c_blocks:
            fp = b.file_path or 'src/helper.c'
            c_files[fp] = b.code

        name = make_project_name(
            md_path, proj_blocks[0].heading,
            proj_blocks[0].block_index, proj_name
        )
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
