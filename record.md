# record.md — 本次改造记录

## 一、改造背景

根据任务要求，对 `check.py` 文档示例代码测试框架进行增强，并对以下两个目录中的文档进行测试和修复：

- `libs/standard/std/ast/ast_samples`
- `language/source_zh_cn/package`

## 二、check.py 框架增强

### 2.1 新增宏包项目支持 (`type=macro_def`)

**问题**：原框架只支持单模块 cjpm 项目，无法处理文档中"宏定义包 + 宏调用包"的多模块示例（如 `context.md`、`report.md`）。

**方案**：新增 `type=macro_def` 标注参数。标记为 `type=macro_def` 的代码块会被识别为宏定义代码，框架自动创建多模块 cjpm 项目结构：

```
project_dir/
├── cjpm.toml                 # 主项目，path 依赖宏模块
├── src/
│   └── main.cj               # 宏调用代码
└── macro_definition/          # 宏子模块（名称从 macro package 声明提取）
    ├── cjpm.toml              # compile-option = "--compile-macro"
    └── src/
        └── macros.cj          # 宏定义代码
```

**改动点**：
- `CodeBlock` 数据类新增 `lang` 和 `block_type` 字段
- `TestCase` 数据类新增 `has_macro_def` 和 `c_files` 字段
- `blocks_to_testcases()` 中自动分离宏定义块和主代码块
- `create_cjpm_project()` 中新增宏项目多模块生成逻辑
- 新增 `_extract_macro_package_name()` 辅助函数

### 2.2 新增 C 代码/FFI 支持 (`lang=c`)

**问题**：文档中可能包含 C 语言互操作（FFI）示例，需要先编译 C 代码再构建仓颉项目。

**方案**：
- 支持 `` ```c `` 代码围栏的自动识别
- C 代码块通过 `project` 参数与仓颉代码关联
- 编译优先使用 `clang`，不可用时回退到 `gcc`
- C 代码编译为静态库（`.a`），在 `cjpm build` 前完成

**改动点**：
- 代码块检测逻辑扩展为支持 `cangjie` 和 `c` 两种语言
- 新增 `_find_c_compiler()` 函数（优先 clang）
- 新增 `_compile_c_files()` 函数处理 C 编译流程
- `run_testcase()` 在 cjpm build 前执行 C 编译

### 2.3 自动检测 output-type

**问题**：原框架固定使用 `output-type = "executable"`，导致无 `main()` 函数的代码块（如只声明类型和函数的库代码）编译失败。

**方案**：自动检测代码中是否包含 `main()` 函数：
- 有 `main()` → `output-type = "executable"`
- `build_only` 或 `compile_error` 指令且无 `main()` → `output-type = "static"`

**改动点**：
- 新增 `_has_main_function()` 辅助函数
- `CJPM_TOML_TEMPLATE` 改为动态 `output_type` 参数
- `create_cjpm_project()` 中根据代码内容自动选择

### 2.4 自动匹配 package 名称

**问题**：文档示例中常有显式的 `package xxx` 声明，但框架自动生成的 cjpm 项目名与之不匹配，导致编译失败。

**方案**：从源代码中提取 `package` 声明的根包名，作为 `cjpm.toml` 的项目名。

**改动点**：
- 新增 `_extract_package_name()` 辅助函数（排除 `macro package`）
- `create_cjpm_project()` 中优先使用源码中的包名

## 三、文档标注修复

### 3.1 ast_samples 目录（6 个文件）

| 文件 | 修改内容 |
|------|----------|
| `dump.md` | `<!-- verify -->` → `<!-- check:run -->` |
| `operate.md` | `<!-- verify -->` → `<!-- check:run -->`，新增 `<!-- expected_output -->` |
| `parse.md` | 第一个块 `<!-- verify -->` → `<!-- check:run -->`；第二个块 `<!-- compile -->` → `<!-- check:skip -->`（依赖外部文件） |
| `traverse.md` | `<!-- verify -->` → `<!-- check:run -->`，新增 `<!-- expected_output -->` |
| `context.md` | 重写标注：示例 1 使用 `compile_error project=ctx1 type=macro_def`；示例 2 使用 `run project=ctx2 type=macro_def`；移除调用代码中冗余的 `package` 声明；新增运行时 `expected_output` |
| `report.md` | 重写标注：示例 1 使用 `compile_error project=rpt1 type=macro_def`；示例 2 使用 `check:run`；移除调用代码中冗余的 `package` 声明 |

### 3.2 package 目录（5 个文件）

| 文件 | 修改内容 |
|------|----------|
| `entry.md` | `<!-- run -->` → `<!-- check:run -->`；`<!-- compile.error -->` → `<!-- check:compile_error -->` |
| `import.md` | 所有代码片段和多文件示例标注为 `<!-- check:skip -->`；最后的 `compile.error` 块改为 `<!-- check:compile_error -->` |
| `package_name.md` | 移除旧的 `<!-- compile.error -->` 和 `<!-- cfg=... -->` 标注；所有代码块标注为 `<!-- check:skip -->`（均为多文件/跨包示例） |
| `toplevel_access.md` | `<!-- compile -->` → `<!-- check:build_only -->`；`<!-- compile.error -->` → `<!-- check:compile_error -->`；`<!-- compile -toplevel-->` → `<!-- check:build_only -->`；最后两个跨文件示例使用 `compile_error project=priv_a file=...` 合并为一个项目 |
| `package_overview.md` | 无代码块，无需修改 |

## 四、check.md 文档更新

- **2.2 节**：新增可选参数表（`project`、`file`、`type`、`lang`）
- **2.6 节**（新增）：宏包项目使用方法及生成结构示例
- **2.7 节**（新增）：C 代码/FFI 项目使用方法示例
- **2.8 节**：更新标注规则总结，新增宏包和 C 代码说明
- **3.1 节**：更新项目生成步骤描述
- **3.3 节**：更新自动处理机制，新增 package 匹配、output-type 检测、宏项目结构、C 编译说明

## 五、测试结果

### ast_samples 目录
- 测试用例：8 个（2 宏项目 + 5 独立项目 + 1 跳过）
- 未标注代码块：0 个（全部已标注）

### package 目录
- 测试用例：15 个（5 entry + 1 import + 9 toplevel）
- 跳过：24 个（多文件/跨包示例和代码片段）
- 未标注代码块：0 个（全部已标注）

## 六、安全扫描

- CodeQL 扫描结果：0 个告警，无安全问题
