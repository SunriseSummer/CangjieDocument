# record.md — 本次改造记录

## 一、改造背景

根据任务要求，对 `check.py` 文档示例代码测试框架进行增强，并对以下两个目录中的文档进行测试和修复：

- `libs/standard/std/ast/ast_samples`
- `language/source_zh_cn/package`

## 二、check.py 框架增强

### 2.1 新增宏包项目支持 (`type=macro`)

**问题**：原框架只支持单模块 cjpm 项目，无法处理文档中"宏定义包 + 宏调用包"的多模块示例（如 `context.md`、`report.md`）。

**方案**：新增 `type=macro` 标注参数。标记为 `type=macro` 的代码块会被识别为宏定义代码，框架自动创建多模块 cjpm 项目结构：

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

### 2.3 新增 `check:ast` 指令（tree-sitter 语法检查）

**问题**：许多代码片段无法编译（如仅含 import 语句的片段、依赖外部文件的示例），原来只能标记为 `check:skip`，缺乏语法层面的验证。

**方案**：新增 `check:ast` 指令，使用 tree-sitter 仓颉插件对代码做语法解析检查：
- 不需要编译器环境（不依赖 cjpm/cjc），始终执行
- 能检测语法错误并报告具体行号和列号
- 适合代码片段、不可编译但语法正确的示例
- 替代 `check:skip`，提供更好的代码看护

**改动点**：
- 新增 `_get_ts_parser()` 延迟初始化 tree-sitter 解析器
- 新增 `_find_ts_errors()` 递归查找语法树中的错误节点
- 新增 `check_ast()` 公共函数执行语法检查
- 代码末尾自动补充换行符，避免 tree-sitter 误报
- 主流程中 `ast` 块独立处理，不生成 cjpm 项目

### 2.4 自动检测 output-type

**问题**：原框架固定使用 `output-type = "executable"`，导致无 `main()` 函数的代码块编译失败。

**方案**：自动检测代码中是否包含 `main()` 函数：
- 有 `main()` → `output-type = "executable"`
- `build_only` 或 `compile_error` 指令且无 `main()` → `output-type = "static"`

### 2.5 自动匹配 package 名称

**问题**：文档示例中常有显式的 `package xxx` 声明，但框架自动生成的 cjpm 项目名与之不匹配。

**方案**：从源代码中提取 `package` 声明的根包名，作为 `cjpm.toml` 的项目名。

## 三、文档标注修复

### 3.1 ast_samples 目录（6 个文件）

| 文件 | 修改内容 |
|------|----------|
| `dump.md` | `<!-- verify -->` → `<!-- check:run -->` |
| `operate.md` | `<!-- verify -->` → `<!-- check:run -->`，新增 `<!-- expected_output -->` |
| `parse.md` | 第一个块 `<!-- verify -->` → `<!-- check:run -->`；第二个块 `<!-- compile -->` → `<!-- check:ast -->`（依赖外部文件，但语法正确） |
| `traverse.md` | `<!-- verify -->` → `<!-- check:run -->`，新增 `<!-- expected_output -->` |
| `context.md` | 重写标注：示例 1 使用 `compile_error project=ctx1 type=macro`；示例 2 使用 `run project=ctx2 type=macro`；新增 `expected_output` |
| `report.md` | 重写标注：示例 1 使用 `compile_error project=rpt1 type=macro`；示例 2 使用 `check:run` |

### 3.2 package 目录（5 个文件）

| 文件 | 修改内容 |
|------|----------|
| `entry.md` | `<!-- run -->` → `<!-- check:run -->`；`<!-- compile.error -->` → `<!-- check:compile_error -->`；第二个代码块新增 `<!-- expected_output -->` |
| `import.md` | 语法正确的独立片段改为 `<!-- check:ast -->`；多文件合并的片段保留 `<!-- check:skip -->`；重导出示例 3 个块改为 `build_only project=reexport` 多文件项目；最后的块保持 `<!-- check:compile_error -->` |
| `package_name.md` | 语法正确的独立片段改为 `<!-- check:ast -->`（6 个）；多文件/多包声明片段保留 `<!-- check:skip -->`（3 个） |
| `toplevel_access.md` | `<!-- compile -->` → `<!-- check:build_only -->`；`<!-- compile.error -->` → `<!-- check:compile_error -->`；最后两个跨文件示例使用 `compile_error project=priv_a file=...` 合并为一个项目 |
| `package_overview.md` | 无代码块，无需修改 |

## 四、模块化拆分

原 `check.py`（1196 行）拆分为 `check/` 目录下 8 个模块文件，每个文件不超过 250 行：

| 文件 | 行数 | 职责 |
|------|------|------|
| `__init__.py` | 1 | 包初始化 |
| `__main__.py` | 4 | `python3 -m check` 入口 |
| `models.py` | 79 | 数据模型（CodeBlock、TestCase）和正则常量 |
| `parser.py` | 144 | Markdown 解析，代码块提取 |
| `assembler.py` | 124 | 测试用例组装（代码块→TestCase） |
| `project.py` | 248 | cjpm 项目生成（含宏项目、标准项目） |
| `runner.py` | 224 | 测试执行、tree-sitter AST 检查 |
| `report.py` | 141 | 测试报告生成 |
| `cli.py` | 164 | 命令行参数解析和摘要输出 |
| `main.py` | 222 | 主流程调度 |

新增选项：
- `--skip-ast`：跳过 `check:ast` 语法解析检查

原 `check.md` 移至 `check/readme.md`，内容中的命令引用更新为 `python3 -m check`。

## 五、check/readme.md 文档更新

- 命令行用法从 `check.py` 改为 `python3 -m check`
- 新增 `--skip-ast` 参数说明
- 文档结构保持不变

## 六、测试结果

### ast_samples 目录
- 测试用例：9 个（2 宏项目 + 6 独立项目 + 1 语法检查）
- 未标注代码块：0 个

### package 目录
- 测试用例：31 个（16 个编译测试 + 15 个语法检查）
- 跳过：6 个（多文件/多包声明合并片段，无法独立解析）
- 未标注代码块：0 个

### story 目录
- 测试用例：86 个
- 跳过：7 个
- 未标注代码块：0 个

## 七、安全扫描

- CodeQL 扫描结果：0 个告警，无安全问题
