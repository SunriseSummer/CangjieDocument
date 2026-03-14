# check — 仓颉文档示例代码测试框架

本文档介绍 `check` 测试框架的设计方案与使用方法，包括文档中的标注约定、工作机制和命令行用法。

---

## 一、设计目标

Markdown 文档中常包含仓颉代码示例。为保证这些示例代码的正确性，本框架提供：

1. **标注约定** — 在 Markdown 文档中用 HTML 注释标注每个代码块的预期行为。
2. **自动提取** — `check` 解析文档，提取所有带标注的仓颉代码块。
3. **统一构建** — 每个代码块（或多个代码块组合）生成一个独立的 `cjpm` 项目。
4. **自动验证** — 编译、运行并校验输出，支持正向示例和负向示例（编译错误 / 运行错误）。
5. **未标注检测** — 自动发现文档中缺少标注的代码块，提醒开发者整改。

---

## 二、标注约定

### 2.1 基本格式

在每个 ` ```cangjie ` 代码块的**正上方**，添加一行 HTML 注释作为标注：

```markdown
<!-- check:DIRECTIVE [key=value ...] -->
```

其中 `DIRECTIVE` 是指令名，`key=value` 是可选参数。

### 2.2 指令列表

| 指令 | 含义 | 说明 |
|------|------|------|
| `run` | 编译并运行 | 预期编译成功、运行成功。可选配 `expected_output` 校验输出 |
| `compile_error` | 预期编译失败 | 用于展示错误用法的负向示例 |
| `runtime_error` | 预期运行时错误 | 编译成功但运行时应抛出异常 |
| `build_only` | 仅编译 | 编译成功即通过，不执行运行（适合含死循环/服务端代码） |
| `ast` | 语法检查 | 使用 tree-sitter 仓颉插件做语法解析检查，不需要编译器环境 |
| `skip` | 跳过 | 不提取、不测试（仅用于包含多文件合并的伪代码片段等无法独立解析的场景） |

可选参数：

| 参数 | 含义 | 说明 |
|------|------|------|
| `project=NAME` | 项目分组 | 同名 project 的代码块合并为一个项目 |
| `file=PATH` | 指定文件路径 | 多文件项目中指定代码块的文件路径 |
| `type=macro` | 宏包标记 | 标记该代码块为宏包定义，框架自动创建多模块结构 |
| `lang=c` | 语言标记 | 标记该代码块为 C 语言代码（也可通过 ` ```c ` 自动识别） |

### 2.3 标注示例

#### 基本运行示例

```markdown
<!-- check:run -->
` ``cangjie
main() {
    println("Hello, Cangjie!")
}
` ``
```

#### 带期望输出的示例

在代码块**之后**紧跟 `expected_output` 注释，框架会自动比对运行输出：

```markdown
<!-- check:run -->
` ``cangjie
main() {
    println("Hello")
    println("World")
}
` ``

<!-- expected_output:
Hello
World
-->
```

#### 预期编译错误的负向示例

```markdown
<!-- check:compile_error -->
` ``cangjie
main() {
    let x: Int64 = "not a number" // 类型不匹配
}
` ``
```

#### 预期运行时错误的负向示例

```markdown
<!-- check:runtime_error -->
` ``cangjie
main() {
    throw Exception("boom")
}
` ``
```

#### 跳过不可独立解析的片段

```markdown
<!-- check:skip -->
` ``cangjie
// 多文件合并的伪代码片段，无法独立解析
// file1.cj
package a
func f() {}
// file2.cj
package b
func g() {}
` ``
```

#### 语法解析检查（无需编译器）

```markdown
<!-- check:ast -->
` ``cangjie
// 使用 tree-sitter 检查语法正确性，适合代码片段和不可编译但语法正确的示例
import std.math.*

class MyClass {
    var x: Int64
}
` ``
```

#### 仅编译（不运行）

```markdown
<!-- check:build_only -->
` ``cangjie
main() {
    while (true) {
        sleep(Duration.second)  // 服务端循环，不应实际运行
    }
}
` ``
```

### 2.4 多代码块项目 (`project` 参数)

当一个章节的多个代码块需要合并为一个项目时，使用 `project=NAME` 参数。**同名 project 的所有代码块**会被合并到同一个 `src/main.cj` 文件中（按文档中出现的顺序拼接）。

```markdown
## 1. 定义接口

<!-- check:run project=payment -->
` ``cangjie
interface PaymentGateway {
    func pay(amount: Float64): Unit
}
` ``

## 2. 实现类

<!-- check:run project=payment -->
` ``cangjie
class AliPay <: PaymentGateway {
    public func pay(amount: Float64) {
        println("支付: ${amount}")
    }
}

main() {
    let pay = AliPay()
    pay.pay(99.9)
}
` ``

<!-- expected_output:
支付: 99.900000
-->
```

上例中两个代码块会被合并为一个 `cjpm` 项目进行编译运行。`expected_output` 放在最后一个代码块之后即可。

### 2.5 多文件项目 (`file` 参数)

如果项目需要多个源文件，使用 `file=PATH` 指定每个代码块对应的文件路径：

```markdown
<!-- check:run project=myapp file=src/utils.cj -->
` ``cangjie
func greet(name: String) {
    println("Hello, ${name}!")
}
` ``

<!-- check:run project=myapp file=src/main.cj -->
` ``cangjie
main() {
    greet("World")
}
` ``
```

### 2.6 宏包项目 (`type=macro` 参数)

当文档中的示例涉及宏定义和宏调用时，使用 `type=macro` 标记宏定义代码块。框架会自动创建多模块 `cjpm` 项目结构：

- 宏定义代码块放入独立的宏子模块（自动从 `macro package XXX` 提取模块名）
- 宏调用代码块放入主项目
- 主项目通过 `path` 依赖引用宏子模块

```markdown
## 宏定义

<!-- check:run project=macro_demo type=macro -->
` ``cangjie
macro package my_macros

import std.ast.*

public macro MyMacro(input: Tokens): Tokens {
    return input
}
` ``

## 宏调用

<!-- check:run project=macro_demo -->
` ``cangjie
import my_macros.*

main() {
    @MyMacro var x = 42
    println(x)
}
` ``
```

生成的项目结构：

```
project_dir/
├── cjpm.toml                 # 主项目，依赖宏模块
├── src/
│   └── main.cj               # 宏调用代码
└── my_macros/                 # 宏子模块
    ├── cjpm.toml              # compile-option = "--compile-macro"
    └── src/
        └── macros.cj          # 宏定义代码
```

对于预期编译失败的宏项目（如宏调用不合法的负向示例），使用 `compile_error` 指令：

```markdown
<!-- check:compile_error project=bad_macro type=macro -->
` ``cangjie
macro package my_macros
// 宏定义...
` ``

<!-- check:compile_error project=bad_macro -->
` ``cangjie
import my_macros.*
// 错误的宏调用...
` ``
```

### 2.7 C 代码 / FFI 项目 (`lang=c`)

当文档中的示例涉及 C 语言互操作（FFI）时，可以标注 C 代码块。C 代码块使用 ` ```c ` 代码围栏，框架会自动识别语言类型。

C 代码必须与仓颉代码在同一个 `project` 中，框架会：

1. 使用 C 编译器（优先 `clang`，其次 `gcc`）编译 C 源文件
2. 将编译产物链接到 `cjpm` 项目中

```markdown
<!-- check:run project=ffi_demo -->
` ``c
// helper.c
int add(int a, int b) {
    return a + b;
}
` ``

<!-- check:run project=ffi_demo -->
` ``cangjie
foreign func add(a: Int32, b: Int32): Int32

main() {
    println(add(1, 2))
}
` ``
```

### 2.8 标注规则总结

1. **每个 ` ```cangjie ` 代码块都应有标注**。没有标注的代码块会被检测并发出警告。
2. 标注必须在代码块的**正上方**（中间允许有空行）。
3. `expected_output` 必须在代码块的**正下方**（中间允许有空行）。
4. 同一个 `project` 中只需要在最后一个代码块后写 `expected_output`。
5. 标注使用 HTML 注释 `<!-- ... -->`，不会在渲染后的文档中显示。
6. 宏定义代码块使用 `type=macro` 参数，框架自动创建多模块项目。
7. C 代码块使用 ` ```c ` 代码围栏，框架自动编译和链接。
8. 优先使用 `check:ast` 做语法检查，仅在多文件合并等无法独立解析的场景使用 `check:skip`。

---

## 三、工作机制

### 3.1 处理流程

```
文档扫描 → 标注解析 → 代码提取 → 未标注检测 → 项目生成 → 编译构建 → 运行验证 → 结果汇总
```

详细步骤：

1. **文档扫描**：递归扫描指定目录下的所有 `.md` 文件。
2. **标注解析**：逐行查找 `<!-- check:xxx -->` 注释，提取指令、选项和紧随的代码块。
3. **代码提取**：将代码块按 `project` 分组（无 `project` 的为独立用例）。
4. **未标注检测**：扫描文档中所有 ` ```cangjie ` 代码块，标记没有 `<!-- check:xxx -->` 标注的代码块，在测试报告中输出警告。
5. **项目生成**：为每个测试用例创建独立的 `cjpm` 项目目录，包括：
   - 自动生成 `cjpm.toml` 配置文件
   - 自动添加 `package` 声明（如果代码中没有）
   - 自动检测源代码中的 `package` 声明并匹配 `cjpm.toml` 项目名
   - 自动检测 `main()` 函数，无 `main()` 的 `build_only` / `compile_error` 项目使用 `output-type = "static"`
   - 源代码写入 `src/main.cj`（或按 `file` 参数指定的路径）
   - 宏项目（含 `type=macro`）自动创建多模块结构
   - C 代码文件使用 `clang`（或 `gcc`）编译并链接
6. **编译构建**：调用 `cjpm build` 编译项目。
7. **运行验证**：
   - `run` 指令：调用 `cjpm run` 并比对输出（如有 `expected_output`）
   - `compile_error` 指令：确认编译失败
   - `runtime_error` 指令：确认运行时出错（通过检查 stderr 中的异常信息）
   - `build_only` 指令：编译成功即通过
8. **结果汇总**：输出 PASS/FAIL 统计和未标注代码块警告，失败项显示详细信息。

### 3.2 项目目录结构

生成的测试项目保存在输出目录中（默认 `check_output/`），目录结构与文档结构一致：

```
check_output/
├── subdir_a/
│   ├── 01_hello__2_章节标题__block1/
│   │   ├── cjpm.toml
│   │   └── src/
│   │       └── main.cj
│   └── ...
├── subdir_b/
│   └── ...
└── ...
```

项目目录名由 `文档名__章节标题__block序号[__project名]` 组成，方便从目录名直接定位到文档中的位置。

### 3.3 自动处理机制

- **package 声明**：如果代码中没有 `package` 声明，框架会自动在文件头部添加，包名根据项目名生成。如果代码已有 `package` 声明，框架会提取包名作为 `cjpm.toml` 的项目名，确保两者一致。
- **项目配置**：`cjpm.toml` 使用 `cjc-version = "1.0.5"` 的标准配置。`output-type` 根据代码自动判断：有 `main()` 函数用 `executable`，`build_only` 或 `compile_error` 指令且无 `main()` 时用 `static`。
- **宏项目结构**：含 `type=macro` 的项目自动创建多模块结构，宏子模块的 `cjpm.toml` 包含 `compile-option = "--compile-macro"`，主项目通过 `path` 依赖引用宏模块。
- **AST 语法检查**：`check:ast` 指令使用 tree-sitter 仓颉插件对代码做语法解析检查，不需要编译器环境，适合代码片段和不可编译但语法正确的示例。
- **C 代码编译**：含 C 代码块的项目会在 `cjpm build` 之前自动编译 C 源文件。优先使用 `clang`，如不可用则使用 `gcc`。
- **输出过滤**：运行结果会自动过滤 `cjpm run finished` 等框架输出，只比对程序实际输出。
- **运行时错误检测**：由于 `cjpm run` 在未捕获异常时仍返回退出码 0，框架通过检查 stderr 中是否包含 `An exception has occurred` 来判断运行时错误。
- **超时控制**：编译超时 60 秒，运行超时 30 秒。

### 3.4 未标注代码块检测

框架会自动扫描文档中所有 ` ```cangjie ` 代码块。如果某个代码块上方没有 `<!-- check:xxx -->` 标注，会在测试报告末尾输出警告，包括：

- 文件路径和行号
- 所在章节标题
- 代码首行预览

开发者可根据警告信息补全标注，确保所有代码块都被纳入验证范围。

### 3.5 测试报告

测试完成后，框架会在输出目录下自动生成 `report.md` 测试报告文件（`--extract-only` 模式除外）。报告内容包括：

- **总览**：测试总数、通过/失败/跳过/未标注的统计表格
- **文件详情**：按来源文件分组列出每个测试用例的名称、类型和结果
- **失败详情**：失败的测试用例的来源、错误信息和编译输出
- **未标注代码块**：缺少标注的代码块位置和代码预览

报告路径为 `<output-dir>/report.md`（默认 `check_output/report.md`），便于在 CI/CD 流程中归档或在浏览器中直接查看。

---

## 四、命令行用法

### 4.1 基本用法

```bash
# 环境准备（需要先配置仓颉 SDK）
source /path/to/cangjie/envsetup.sh

# 测试当前目录下的所有文档
python3 -m check

# 测试指定目录下的文档
python3 -m check path/to/docs

# 测试指定的子目录
python3 -m check path/to/docs -s subdir_name

# 测试指定文件
python3 -m check -f path/to/file.md

# 显示详细输出
python3 -m check -v
```

### 4.2 完整参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `dir` (位置参数) | 文档目录路径 | `.`（当前目录） |
| `-o, --output-dir DIR` | 提取的示例代码存放路径 | `check_output` |
| `-f, --file FILE` | 只处理指定的文档文件（可多次指定） | — |
| `-s, --subdir NAME` | 只处理指定的子目录 | — |
| `--clean` | 测试完成后清理生成的项目目录 | 不清理 |
| `--extract-only` | 仅提取代码，不构建运行 | — |
| `--skip-ast` | 跳过 check:ast 语法解析检查 | — |
| `-v, --verbose` | 显示详细输出 | — |
| `--json FILE` | 将测试结果输出为 JSON 文件 | — |

### 4.3 示例

```bash
# 仅提取代码，不编译运行（用于检查提取是否正确）
python3 -m check docs/ --extract-only -v

# 测试后清理项目目录
python3 -m check docs/ -s chapter1 --clean

# 输出 JSON 格式的测试结果
python3 -m check docs/ --json results.json

# 指定自定义输出目录
python3 -m check docs/ -o /tmp/my_tests -s chapter2

# 同时测试多个文件
python3 -m check -f docs/01_intro.md -f docs/02_basics.md
```

### 4.4 输出示例

正常运行时：

```
📖 扫描文档目录: docs
📁 输出目录: check_output
📄 找到 10 个文档文件

  📄 01_hello_world.md: (1 个测试用例)
    ✅ PASS: 01_hello_world__章节标题__block1
  📄 02_variables.md: (2 个测试用例, 1 个跳过)
    ✅ PASS: 02_variables__定义变量__block1
    ✅ PASS: 02_variables__类型安全__block2
  ...

============================================================
📊 测试结果: 19 通过 / 0 失败 / 2 跳过 (共 19 个)
```

当有未标注代码块时：

```
============================================================
⚠️  发现 3 个未标注的 cangjie 代码块:

  docs/05_advanced.md:42  (章节: 高级用法)
    func helper() { ... }
  docs/05_advanced.md:78  (章节: 扩展示例)
    let config = loadConfig()
  docs/06_tips.md:15  (章节: 小技巧)
    // 代码片段

   请为这些代码块添加 <!-- check:xxx --> 标注。
```

当测试失败时：

```
❌ 失败详情:

  [run] 07_collections__block1
    来源: docs/07_collections.md > 泛型播放列表
    错误: Build failed unexpectedly
    编译输出:
      error: expected '{', found 'items'
```

---

## 五、退出码

| 退出码 | 含义 |
|--------|------|
| `0` | 所有测试通过（或 `--extract-only` 模式） |
| `1` | 存在测试失败 |

---

## 六、注意事项

1. **运行前必须配置仓颉 SDK 环境**：执行 `source envsetup.sh` 确保 `cjpm` 命令可用。
2. **代码不做修改**：从文档提取的代码原样写入项目，不做任何自动修改（`package` 声明除外），以确保测试能真实反映代码质量。
3. **默认保留测试项目**：生成的 `cjpm` 项目默认不删除，方便调试。使用 `--clean` 可在测试后清理。
4. **通用设计**：本工具不绑定特定目录结构，可用于检查任何包含仓颉 Markdown 文档的目录。
5. **并发输出不确定性**：包含并发代码（`spawn`）的示例，输出顺序可能不固定，此类示例建议不设置 `expected_output`。
6. **未标注警告**：未标注的代码块不会导致测试失败（退出码仍为 0），但会在报告中输出警告，便于开发者持续整改。
