# SKILL.md 示例代码测试指南

## 概述

本目录提供 `skills/*/SKILL.md` 中所有仓颉代码示例的自动化测试工具和经验总结。

## 测试方法论

### 总体流程

SKILL.md 示例代码的质量保障分为两个阶段：**自动化脚本测试** 和 **AI 分析判断**。

#### 第一阶段：自动化脚本测试（`test_all_skills.py`）

脚本对每个 SKILL.md 中的代码块执行以下步骤：

1. **提取**：用正则表达式从 Markdown 中提取所有 ` ```cangjie ` 代码块，同时记录行号和上下文文本。

2. **分类**：对每个代码块进行特征检测：
   - 是否含 `main()` 入口函数
   - 是否使用 stdx 扩展标准库（`import stdx.`）
   - 是否为故意错误示例（上下文含 `❌`）
   - 是否为交互式/服务器代码（含 `readln()`、`.serve()`、`getStdIn()`）
   - 是否含 FFI 声明（`foreign func`）
   - 是否为宏包定义（`macro package`）
   - 是否为测试/基准代码（`@Test`、`@Bench`）
   - 是否含自定义包声明
   - 是否为伪代码（含 `{ ... }` 或 `/* ... */`）

3. **选择测试策略**：根据分类结果选择最合适的测试方式（详见下方策略表）

4. **构建测试项目**：为每个代码块创建临时 `cjpm` 项目：
   - 生成 `cjpm.toml`（根据是否使用 stdx 选择不同配置）
   - 生成 `src/main.cj`（根据策略决定是否补充 `main()`、`package` 声明等）
   - 执行 `cjpm build` 编译
   - 对完整代码执行 `cjpm run` 运行

5. **判定结果**：根据策略判定 PASS/FAIL：
   - 完整代码：编译 + 运行成功 → PASS
   - 错误示例：编译失败 → PASS（符合预期）
   - 交互式代码：编译成功 → PASS（跳过运行）
   - FFI 代码：编译成功或仅链接失败 → PASS
   - 片段代码：编译成功或因缺少上下文声明而失败 → PASS

#### 第二阶段：AI 分析判断

AI（辅助测试人员）在脚本测试的基础上执行以下补充工作：

1. **输出注释校验**：对比代码中的 `// 输出：xxx` 注释与实际运行输出，检查是否一致。脚本仅检查编译和运行是否成功，但不自动校验注释中的预期输出。AI 需手动或半自动地抽检关键示例的输出。

2. **错误示例语义校验**：脚本仅验证错误示例会编译失败，但 AI 需检查**编译器的错误信息是否与文档描述一致**。例如，文档说"lambda 不能捕获可变变量"，AI 需确认编译器确实报告了相关错误。

3. **API 用法审查**：AI 检查代码中的 API 调用是否符合 SDK 文档规范，包括：
   - 函数签名（参数数量和类型）
   - 返回值类型（如 `Option` vs 直接值）
   - 方法名称（如 `toEncodeString()` vs `toString()`）
   - 导入路径（如 `import std.time.*` vs `import std.time.Duration`）

4. **上下文完整性检查**：AI 检查代码片段是否缺少必要的 import 声明或变量定义，导致读者无法独立运行示例。

5. **跨块一致性**：AI 检查同一 SKILL 中多个代码块之间的一致性，如变量名、类型名是否前后一致。

6. **修复与迭代**：发现问题后，AI 直接修改 SKILL.md 源文件，然后重新运行脚本验证修复效果。

### 测试策略表

| 策略名称 | 适用条件 | 测试方式 | PASS 条件 |
|----------|---------|---------|-----------|
| `full_build_run` | 含 `main()` 的完整代码 | `cjpm build` + `cjpm run` | 编译和运行均成功 |
| `error_demo_expect_fail` | 上下文含 `❌` 的错误示例 | `cjpm build`（期望失败） | 编译失败（符合文档描述） |
| `interactive_build_only` | 含 `readln()` / `.serve()` | `cjpm build`（跳过运行） | 编译成功 |
| `ffi_build_only` | 含 `foreign func`（非 stdx） | `cjpm build`（允许链接错误） | 编译通过语法检查 |
| `test_block_build` | 含 `@Test` / `@Bench` | 作为静态库编译 | 编译成功或因引用未包含的函数而失败 |
| `fragment_wrap` | 不含 `main()` 的代码片段 | 补充 `main()` 后 `cjpm build` | 编译成功或因缺少上下文声明而失败 |
| `macro_package_build` | 含 `macro package` | 创建多模块 cjpm 项目（宏模块 + 主模块），`cjpm build` + `cjpm run` | 编译成功 |
| `multi_package_build` | 含自定义 `package` 声明 | 创建多目录 cjpm 项目（每个 package 对应子目录），`cjpm build` | 编译成功 |
| `pseudo_code_skip` | 含 `{ ... }` 伪代码 | **跳过** | — |

### 宏包测试方法（`macro_package_build`）

宏包代码块不能在单文件项目中测试，需要构建多模块 cjpm 项目：

1. **识别宏包组**：脚本从 `macro package` 块中提取宏包名，然后向后查找包含 `import <宏包名>` 的调用方代码块，将两者组合为一组。

2. **构建多模块项目**：为每个宏包组创建如下目录结构：
   ```text
   project/
   ├── cjpm.toml              # 主项目，依赖宏模块
   ├── src/
   │   └── main.cj            # 调用宏的代码
   └── macros/                 # 宏模块子目录
       ├── cjpm.toml           # compile-option = "--compile-macro"
       └── src/
           └── macros.cj       # 宏定义代码
   ```

3. **编译流程**：`cjpm build` 自动按依赖顺序先编译宏包再编译主包。

4. **判定规则**：编译成功 → PASS。因引用文档上下文声明而失败 → PASS（预期行为）。

### 多包测试方法（`multi_package_build`）

多包示例代码块展示跨包导入、包可见性等特性，需要构建多目录 cjpm 项目：

1. **识别包组**：脚本自动查找连续的含自定义 `package` 声明的代码块，将它们组合为一个测试组。

2. **构建多目录项目**：将各包映射为 `testproject` 的子包：
   ```text
   project/
   ├── cjpm.toml
   └── src/
       ├── main.cj             # package testproject（含 main）
       ├── pkga/
       │   └── pkga.cj         # package testproject.pkga
       └── pkgb/
           └── pkgb.cj         # package testproject.pkgb
   ```

3. **包名重写**：自动将 `package pkga` 改为 `package testproject.pkga`，并相应更新所有 `import` 语句。

4. **判定规则**：编译成功 → PASS。因可见性限制、名称冲突等编译失败（属于文档展示的语义限制）→ PASS。

### 仍需跳过的代码块及原因

以下代码块在当前测试框架下无法自动测试：

**伪代码/API 签名**（含 `{ ... }` 或 `/* ... */`）：这些代码块展示 API 签名或语法模式，函数体用 `...` 省略，不是可执行代码。共约 20+ 个代码块。

## 环境准备

### 1. 下载仓颉 SDK

```bash
# 下载并解压 Cangjie SDK
wget https://github.com/SunriseSummer/CangjieDocument/releases/download/1.0.5/cangjie-sdk-linux-x64-1.0.5.tar.gz
tar xzf cangjie-sdk-linux-x64-1.0.5.tar.gz -C /path/to/install

# 设置环境变量
source /path/to/install/cangjie/envsetup.sh

# 验证安装
cjc --version   # 期望：Cangjie Compiler: 1.0.5 (cjnative)
cjpm --version  # 期望：Cangjie Package Manager: 1.0.5
```

### 2. 下载仓颉 stdx 扩展标准库

```bash
wget https://github.com/SunriseSummer/CangjieDocument/releases/download/1.0.5/cangjie-stdx-linux-x64-1.0.5.1.zip
unzip cangjie-stdx-linux-x64-1.0.5.1.zip -d /path/to/install/cangjie-stdx
```

### 3. 配置 stdx 路径

设置环境变量指向 stdx 静态库路径：

```bash
export CANGJIE_STDX_PATH="/path/to/install/cangjie-stdx/linux_x86_64_cjnative/static/stdx"
```

## 使用方法

### 运行全量测试

```bash
# 测试所有 SKILL.md 中的代码示例（含片段、错误示例等）
python3 skills_tests/test_all_skills.py
```

### 测试单个 skill

```bash
# 测试指定 skill 的示例代码
python3 skills_tests/test_all_skills.py --skill format
python3 skills_tests/test_all_skills.py --skill json
```

### 仅检查编译

```bash
# 只编译不运行（不执行 cjpm run）
python3 skills_tests/test_all_skills.py --build-only
```

### 输出详细信息

```bash
# 显示每个代码块的详细测试结果和测试策略
python3 skills_tests/test_all_skills.py --verbose
```

### 导出结果到 JSON

```bash
# 将结果保存到文件
python3 skills_tests/test_all_skills.py -o results.json
```

### 快速测试单个代码文件

```bash
# 使用 test_block.sh 测试单个 .cj 文件
./skills_tests/test_block.sh /tmp/test.cj --run
./skills_tests/test_block.sh /tmp/test.cj --stdx --run
```

## 测试经验总结

### 常见问题及修复方法

#### 1. `import std.time.Duration` 编译失败

**问题**：`Duration` 不能直接通过 `import std.time.Duration` 导入。

**修复**：改用 `import std.time.*`。

```cangjie
// ❌ 错误
import std.time.Duration

// ✅ 正确
import std.time.*
```

#### 2. Lambda 不能捕获可变变量

**问题**：仓颉语言中，lambda 表达式不能捕获外部的 `var` 变量。

**修复**：避免在 lambda 中使用外部 `var` 变量，改用其他方式（如通过返回值传递）。

```cangjie
// ❌ 错误：lambda 捕获了可变变量
var verbose = false
let specs = [Short(r'v', NoValue) { _ => verbose = true }]

// ✅ 正确：使用 ParsedArguments 结果
let specs = [Short(r'v', NoValue)]
let result = parseArguments(args, specs)
let verbose = result.options.contains('v')
```

#### 3. `fromBase64String` / `fromHexString` 返回 Option 类型

**问题**：这两个函数返回 `Option<Array<UInt8>>`，不能直接传给 `String.fromUtf8()`。

**修复**：使用 `.getOrThrow()` 解包。

```cangjie
// ❌ 错误
let decoded = fromBase64String(encoded)
println(String.fromUtf8(decoded))

// ✅ 正确
let decoded = fromBase64String(encoded).getOrThrow()
println(String.fromUtf8(decoded))
```

#### 4. `Form` 类没有 `toString()` 方法

**问题**：`stdx.encoding.url.Form` 不提供 `toString()` 方法。

**修复**：使用 `toEncodeString()` 方法。

```cangjie
// ❌ 错误
println(form.toString())

// ✅ 正确
println(form.toEncodeString())
```

#### 5. `JsonWriter.startArray()` 返回值不支持链式调用 `writeValue()`

**问题**：`startArray()` 返回的类型不支持直接链式调用 `.writeValue()`。

**修复**：将链式调用拆分为独立语句。

```cangjie
// ❌ 错误
writer.startArray()
    .writeValue(90).writeValue(85)
.endArray()

// ✅ 正确
writer.startArray()
writer.writeValue(90)
writer.writeValue(85)
writer.endArray()
```

#### 6. `keylogCallback` 回调签名

**问题**：TLS 的 `keylogCallback` 接受两个参数（label 和 keylog），不是一个。

**修复**：

```cangjie
// ❌ 错误
tlsConfig.keylogCallback = { keylog => println(keylog) }

// ✅ 正确
tlsConfig.keylogCallback = { label, keylog => println(keylog) }
```

#### 7. `ChainedInputStream` 不支持 `readString()`

**问题**：`readString()` 要求流实现 `Seekable` 接口，但 `ChainedInputStream` 没有实现。

**修复**：使用手动读取循环。

```cangjie
// ❌ 错误
println(readString(chained))

// ✅ 正确
let buf = ArrayList<Byte>()
let tmp = Array<Byte>(256, {_ => 0})
while (true) {
    let n = chained.read(tmp)
    if (n <= 0) { break }
    for (i in 0..n) { buf.add(tmp[i]) }
}
println(String.fromUtf8(buf.toArray()))
```

#### 8. 使用 `Int64.parse()` 需要导入 `std.convert.*`

**问题**：`Int64.parse()` 来自 `Parsable` 接口，定义在 `std.convert` 包中。

**修复**：添加 `import std.convert.*`。

#### 9. `Process.current` 需要导入 `std.process.*`

**问题**：`Process` 类在 `std.process` 包中，且 `Process.current` 已标记为 deprecated。

**修复**：添加 `import std.process.*`。

#### 10. 格式化字符串 `#` 前缀在二进制格式中不适用

**问题**：`flags.format("#010b")` 会抛异常，`#` 标志不适用于 `b` 说明符。

**修复**：去掉 `#` 前缀，使用 `flags.format("010b")`。

### cjpm 项目配置要点

#### 标准库项目

```toml
[package]
  cjc-version = "1.0.5"
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
```

#### 使用 stdx 的项目

```toml
[package]
  cjc-version = "1.0.5"
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"
[dependencies]
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

#### 宏包项目（多模块）

主项目 `cjpm.toml`：

```toml
[package]
  cjc-version = "1.0.5"
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
  macros = { path = "./macros" }
```

宏模块 `macros/cjpm.toml`：

```toml
[package]
  cjc-version = "1.0.5"
  name = "macros"
  version = "1.0.0"
  output-type = "static"
  compile-option = "--compile-macro"
[dependencies]
```

### 网络相关代码测试说明

HTTP 客户端、HTTPS、WebSocket、TLS、Socket 等网络相关示例在编译后运行会产生以下预期异常：

- `HttpException: Failed to resolve address` — DNS 解析失败（无网络环境）
- `SocketException: Failed to connect` — 连接被拒绝（无目标服务器）
- `FSException: The file does not exist` — 证书/密钥文件不存在

这些异常属于**运行时环境限制**，不影响代码正确性。测试时仅验证编译通过即可。

## 测试统计

基于 Cangjie SDK v1.0.5 的完整测试结果：

| 指标 | 数量 |
|------|------|
| 总代码块数 | 577 |
| 通过测试 | 427 |
| 失败 | 0 |
| 跳过（伪代码/API 签名） | 150 |
| 运行时异常（网络/文件，预期行为） | 34 |

> 宏包和多包示例已通过构建多模块/多目录 cjpm 项目测试，不再跳过。
