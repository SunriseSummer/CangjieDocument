"""
数据模型与常量定义

包含 CodeBlock、TestCase 数据类，以及标注解析所需的正则表达式常量。
"""

import re
from dataclasses import dataclass, field
from typing import Optional


# ============================================================
# 正则常量
# ============================================================

# 访问修饰符的正则匹配模式（用于 package 声明检测）
_ACCESS_MOD_RE = r'(?:(?:public|protected|internal|private)\s+)?'

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


# ============================================================
# 数据模型
# ============================================================

@dataclass
class CodeBlock:
    """一个带标注的仓颉代码块"""
    directive: str          # run / compile_error / runtime_error / skip / ast
    code: str               # 代码内容
    project: Optional[str]  # 项目分组名（多代码块合并时使用）
    file_path: Optional[str]  # 多文件项目中的文件路径
    expected_output: Optional[str]  # 期望的输出（可为 None 表示不检查）
    source_file: str        # 来源文档路径
    heading: str            # 所在章节标题
    block_index: int        # 在文档中的序号
    lang: str = 'cangjie'   # 代码块语言（cangjie / c）
    block_type: Optional[str] = None  # 代码块类型（如 macro 表示宏定义包）


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
    project_dir: Optional['Path'] = None  # 生成的项目目录
