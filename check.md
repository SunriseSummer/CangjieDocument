# check.md — Story 示例代码测试框架

本文档介绍 `check.py` 测试框架的设计方案与使用方法，包括文档中的标注约定、工作机制和命令行用法。

---

## 一、设计目标

`story/` 目录下的教程文档包含大量仓颉代码示例。为了保证这些示例代码的正确性，本框架提供：

1. **标注约定** — 在 Markdown 文档中用 HTML 注释标注每个代码块的预期行为。
2. **自动提取** — `check.py` 解析文档，提取所有带标注的代码块。
3. **统一构建** — 每个代码块（或多个代码块组合）生成一个独立的 `cjpm` 项目。
4. **自动验证** — 编译、运行并校验输出，支持正向示例和负向示例（编译错误 / 运行错误）。

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
| `skip` | 跳过 | 不提取、不测试（用于代码片段、伪代码、纯注释等） |

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

#### 跳过不可执行的片段

```markdown
<!-- check:skip -->
` ``cangjie
// 这只是一个代码片段，不是完整程序
let x = if (condition) { a } else { b }
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

### 2.6 标注规则总结

1. **每个 ` ```cangjie ` 代码块必须有标注**。没有标注的代码块会被忽略。
2. 标注必须在代码块的**正上方**（中间允许有空行）。
3. `expected_output` 必须在代码块的**正下方**（中间允许有空行）。
4. 同一个 `project` 中只需要在最后一个代码块后写 `expected_output`。
5. 标注使用 HTML 注释 `<!-- ... -->`，不会在渲染后的文档中显示。

---

## 三、check.py 工作机制

### 3.1 处理流程

```
文档扫描 → 标注解析 → 代码提取 → 项目生成 → 编译构建 → 运行验证 → 结果汇总
```

详细步骤：

1. **文档扫描**：递归扫描 `story/` 目录下的所有 `.md` 文件。
2. **标注解析**：逐行查找 `<!-- check:xxx -->` 注释，提取指令、选项和紧随的代码块。
3. **代码提取**：将代码块按 `project` 分组（无 `project` 的为独立用例）。
4. **项目生成**：为每个测试用例创建独立的 `cjpm` 项目目录，包括：
   - 自动生成 `cjpm.toml` 配置文件
   - 自动添加 `package` 声明（如果代码中没有）
   - 源代码写入 `src/main.cj`（或按 `file` 参数指定的路径）
5. **编译构建**：调用 `cjpm build` 编译项目。
6. **运行验证**：
   - `run` 指令：调用 `cjpm run` 并比对输出（如有 `expected_output`）
   - `compile_error` 指令：确认编译失败
   - `runtime_error` 指令：确认运行时出错
   - `build_only` 指令：编译成功即通过
7. **结果汇总**：输出 PASS/FAIL 统计，失败项显示详细信息。

### 3.2 项目目录结构

生成的测试项目保存在输出目录中（默认 `story_tests/`），目录结构与文档结构一致：

```
story_tests/
├── begin/
│   ├── 01_hello_world__2_你的第一行魔法咒语__block1/
│   │   ├── cjpm.toml
│   │   └── src/
│   │       └── main.cj
│   ├── 02_variables_and_types__1_定义角色属性__block1/
│   │   ├── cjpm.toml
│   │   └── src/
│   │       └── main.cj
│   └── ...
├── begin-v2/
│   └── ...
└── ...
```

项目目录名由 `文档名__章节标题__block序号[__project名]` 组成，方便从目录名直接定位到文档中的位置。

### 3.3 自动处理机制

- **package 声明**：如果代码中没有 `package` 声明，框架会自动在文件头部添加，包名根据项目名生成。
- **项目配置**：`cjpm.toml` 使用 `cjc-version = "1.0.5"`、`output-type = "executable"` 的标准配置。
- **输出过滤**：运行结果会自动过滤 `cjpm run finished` 等框架输出，只比对程序实际输出。
- **超时控制**：编译超时 60 秒，运行超时 30 秒。

---

## 四、命令行用法

### 4.1 基本用法

```bash
# 环境准备（需要先配置仓颉 SDK）
source /path/to/cangjie/envsetup.sh

# 测试所有 story 文档
python3 check.py

# 测试指定的 story 子目录
python3 check.py -s begin
python3 check.py -s begin-v2

# 测试指定文件
python3 check.py -f story/begin/01_hello_world.md

# 显示详细输出
python3 check.py -v
python3 check.py -s begin -v
```

### 4.2 完整参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-d, --story-dir DIR` | story 文档目录路径 | `story` |
| `-o, --output-dir DIR` | 提取的示例代码存放路径 | `story_tests` |
| `-f, --file FILE` | 只处理指定的文档文件（可多次指定） | — |
| `-s, --story NAME` | 只处理指定的 story 子目录 | — |
| `--clean` | 测试完成后清理生成的项目目录 | 不清理 |
| `--extract-only` | 仅提取代码，不构建运行 | — |
| `-v, --verbose` | 显示详细输出 | — |
| `--json FILE` | 将测试结果输出为 JSON 文件 | — |

### 4.3 示例

```bash
# 仅提取代码，不编译运行（用于检查提取是否正确）
python3 check.py --extract-only -v

# 测试后清理项目目录
python3 check.py -s begin --clean

# 输出 JSON 格式的测试结果
python3 check.py --json results.json

# 指定自定义输出目录
python3 check.py -o /tmp/my_tests -s begin-v3

# 同时测试多个文件
python3 check.py -f story/begin/01_hello_world.md -f story/begin/02_variables_and_types.md
```

### 4.4 输出示例

```
📖 扫描文档目录: story/begin
📁 输出目录: story_tests
📄 找到 10 个文档文件

  📄 begin/01_hello_world.md: 1 个测试用例
    ✅ PASS: 01_hello_world__2_你的第一行魔法咒语__block1
  📄 begin/02_variables_and_types.md: 1 个测试用例 (1 个跳过)
    ✅ PASS: 02_variables_and_types__1_定义角色属性_变量与常量__block1
  ...

============================================================
📊 测试结果: 19 通过 / 0 失败 / 2 跳过 (共 19 个)
```

失败时会输出详细错误信息：

```
❌ 失败详情:

  [run] 07_collections__block1
    来源: story/begin/07_collections.md > 泛型播放列表
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
4. **输出目录已加入 `.gitignore`**：`story_tests/` 目录不会被提交到仓库。
5. **并发输出不确定性**：包含并发代码（`spawn`）的示例，输出顺序可能不固定，此类示例建议不设置 `expected_output`。
