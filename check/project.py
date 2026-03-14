"""
cjpm 项目生成模块

根据 TestCase 创建 cjpm 项目目录结构，包括标准项目和宏项目的多模块结构。
"""

import re
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from .models import TestCase, _ACCESS_MOD_RE


# ============================================================
# cjpm.toml 模板
# ============================================================

CJPM_TOML_TEMPLATE = """\
[package]
  cjc-version = "1.0.5"
  name = "{name}"
  version = "1.0.0"
  output-type = "{output_type}"

[dependencies]
"""

CJPM_TOML_MACRO_MODULE_TEMPLATE = """\
[package]
  cjc-version = "1.0.5"
  name = "{name}"
  version = "1.0.0"
  output-type = "static"
  compile-option = "--compile-macro"

[dependencies]
"""

CJPM_TOML_WITH_MACRO_DEP_TEMPLATE = """\
[package]
  cjc-version = "1.0.5"
  name = "{name}"
  version = "1.0.0"
  output-type = "executable"

[dependencies]
  [dependencies.{macro_module}]
    path = "./{macro_module}"
"""


# ============================================================
# 辅助函数
# ============================================================

def _extract_macro_package_name(code: str) -> Optional[str]:
    """从宏定义代码中提取 macro package 名称"""
    m = re.search(r'^\s*macro\s+package\s+(\w+)', code, re.MULTILINE)
    if m:
        return m.group(1)
    return None


def _extract_package_name(code: str) -> Optional[str]:
    """从代码中提取 package 声明的包名（不含 macro package）"""
    m = re.search(
        rf'^\s*{_ACCESS_MOD_RE}(?!macro\s+package\b)package\s+([\w.]+)',
        code, re.MULTILINE
    )
    if m:
        return m.group(1).split('.')[0]
    return None


def _has_main_function(files: dict) -> bool:
    """检查代码文件中是否包含 main 函数"""
    all_code = '\n'.join(files.values())
    return bool(re.search(r'^\s*main\s*\(', all_code, re.MULTILINE))


# ============================================================
# C 编译支持
# ============================================================

def find_c_compiler() -> Optional[str]:
    """查找 C 编译器，优先使用 clang"""
    for compiler in ['clang', 'gcc']:
        if shutil.which(compiler):
            return compiler
    return None


def compile_c_files(proj_dir: Path, c_files: dict) -> tuple:
    """编译 C 源文件为静态库。返回 (success, output_message)"""
    cc = find_c_compiler()
    if cc is None:
        return False, 'No C compiler found (need clang or gcc)'

    all_output = []
    for rel_path, code in c_files.items():
        c_file_path = proj_dir / rel_path
        c_file_path.parent.mkdir(parents=True, exist_ok=True)
        c_file_path.write_text(code, encoding='utf-8')

        obj_path = c_file_path.with_suffix('.o')
        try:
            result = subprocess.run(
                [cc, '-c', '-fPIC', '-o', str(obj_path), str(c_file_path)],
                cwd=str(proj_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )
            all_output.append(result.stdout + result.stderr)
            if result.returncode != 0:
                return False, f'C compilation failed:\n' + result.stderr
        except subprocess.TimeoutExpired:
            return False, 'C compilation timed out'
        except Exception as e:
            return False, str(e)

    obj_files = list(proj_dir.rglob('*.o'))
    if obj_files:
        lib_path = proj_dir / 'libffi_helper.a'
        try:
            result = subprocess.run(
                ['ar', 'rcs', str(lib_path)] + [str(o) for o in obj_files],
                cwd=str(proj_dir),
                capture_output=True,
                text=True,
                timeout=30,
            )
            all_output.append(result.stdout + result.stderr)
            if result.returncode != 0:
                return False, f'ar failed:\n' + result.stderr
        except Exception as e:
            return False, str(e)

    return True, '\n'.join(all_output)


# ============================================================
# 项目创建
# ============================================================

def create_cjpm_project(tc: TestCase, output_dir: Path) -> Path:
    """为测试用例创建 cjpm 项目"""
    proj_dir = output_dir / tc.name
    proj_dir.mkdir(parents=True, exist_ok=True)

    pkg_name = re.sub(r'[^a-zA-Z0-9_]', '_', tc.name)[:40]
    pkg_name = pkg_name.lower()
    if not pkg_name[0].isalpha():
        pkg_name = 'p_' + pkg_name

    # 从源码提取 package 名称
    for rel_path, code in tc.files.items():
        if rel_path == '__macro_src__':
            continue
        if _extract_macro_package_name(code):
            continue
        src_pkg = _extract_package_name(code)
        if src_pkg:
            pkg_name = src_pkg
            break

    if tc.has_macro_def:
        _create_macro_project(tc, proj_dir, pkg_name)
    else:
        _create_standard_project(tc, proj_dir, pkg_name)

    tc.project_dir = proj_dir
    return proj_dir


def _create_macro_project(tc: TestCase, proj_dir: Path, pkg_name: str):
    """创建宏项目的多模块结构"""
    macro_module_name = None
    macro_files = {}
    main_files = {}

    for rel_path, code in tc.files.items():
        if rel_path == '__macro_src__' or _extract_macro_package_name(code):
            if not macro_module_name:
                macro_module_name = (
                    _extract_macro_package_name(code) or 'macro_mod'
                )
            macro_files['src/macros.cj'] = code
        else:
            main_files[rel_path] = code

    if not macro_module_name:
        macro_module_name = 'macro_mod'

    # 创建宏模块
    macro_dir = proj_dir / macro_module_name
    macro_dir.mkdir(parents=True, exist_ok=True)

    macro_toml = CJPM_TOML_MACRO_MODULE_TEMPLATE.format(
        name=macro_module_name
    )
    (macro_dir / 'cjpm.toml').write_text(macro_toml, encoding='utf-8')

    for rel_path, code in macro_files.items():
        file_path = macro_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(code, encoding='utf-8')

    # 创建主项目
    main_toml = CJPM_TOML_WITH_MACRO_DEP_TEMPLATE.format(
        name=pkg_name,
        macro_module=macro_module_name,
    )
    (proj_dir / 'cjpm.toml').write_text(main_toml, encoding='utf-8')

    for rel_path, code in main_files.items():
        file_path = proj_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not re.search(r'^\s*package\s+', code, re.MULTILINE):
            code = f'package {pkg_name}\n\n' + code
        file_path.write_text(code, encoding='utf-8')


def _create_standard_project(tc: TestCase, proj_dir: Path, pkg_name: str):
    """创建标准 cjpm 项目"""
    if _has_main_function(tc.files):
        output_type = 'executable'
    elif tc.directive in ('build_only', 'compile_error'):
        output_type = 'static'
    else:
        output_type = 'executable'

    toml_content = CJPM_TOML_TEMPLATE.format(
        name=pkg_name, output_type=output_type
    )
    (proj_dir / 'cjpm.toml').write_text(toml_content, encoding='utf-8')

    for rel_path, code in tc.files.items():
        file_path = proj_dir / rel_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        if not re.search(
            rf'^\s*{_ACCESS_MOD_RE}(?:macro\s+)?package\s+',
            code, re.MULTILINE
        ):
            code = f'package {pkg_name}\n\n' + code
        file_path.write_text(code, encoding='utf-8')
