# SKILL.md 示例代码测试指南

## 概述

本目录提供 `skills/*/SKILL.md` 中所有仓颉代码示例的自动化测试工具和经验总结。

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
# 测试所有 SKILL.md 中的代码示例
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
# 只编译不运行
python3 skills_tests/test_all_skills.py --build-only
```

### 输出详细信息

```bash
# 显示每个代码块的详细测试结果
python3 skills_tests/test_all_skills.py --verbose
```

## 代码块分类

测试脚本将 SKILL.md 中的代码块分为以下类别：

| 类别 | 说明 | 测试方式 |
|------|------|----------|
| **完整代码** | 含 `main()` 函数的独立可运行代码 | 完整编译 + 运行 |
| **代码片段** | 不含 `main()` 的代码片段（API 签名、表达式示例等） | 补充 `main()` 后尝试编译 |
| **错误示例** | 以 `// ❌ 错误` 标注的故意错误代码 | 验证编译错误信息与文档描述一致 |
| **交互式代码** | 含 `readln()`、`.serve()` 等需要交互的代码 | 仅编译，跳过运行 |
| **FFI 代码** | 含 `foreign func` 的 C 互操作代码 | 仅编译（需 C 库链接） |
| **多包代码** | 涉及多个 package 的示例 | 跳过（需特殊项目结构） |
| **宏代码** | 含 `macro package` 的宏定义代码 | 跳过（需宏包编译链） |

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
| 编译测试（含 main） | 122 |
| 编译通过 | 122 |
| 编译失败 | 0 |
| 跳过（片段/交互/FFI 等） | 455 |
| 运行时异常（网络/文件，预期中） | 34 |
| 错误示例（验证编译器报错正确） | 2 |
