# 仓颉语言基本输入输出 Skill

## 1. I/O 流概述

### 1.1 流模型
- 仓颉将所有 I/O 建模为**流**
- `InputStream` 提供 `read(buffer: Array<Byte>): Int64`
- `OutputStream` 提供 `write(buffer: Array<Byte>): Unit` 和 `flush()`（默认空实现）
- 最小数据单元为 `Byte`

### 1.2 流分类
- **源流**（节点流）：由外部资源（文件/网络）支撑
- **处理流**（代理流）：代理其他流，如缓冲流/字符串流

---

## 2. 处理流

### 2.1 BufferedInputStream / BufferedOutputStream
- 用内部缓冲区包装另一个流以减少磁盘 I/O 频率
- 构造时传入输入/输出流和可选的 `capacity`
- `BufferedOutputStream` 写完所有数据后须显式调用 `flush()`

### 2.2 StringReader / StringWriter
- 在字节流上添加字符串处理能力
- `StringReader` 支持 `readln()`（按行读取）和过滤读取
- `StringWriter` 支持 `write(String)`、`writeln(String)` 和 `write(numeric)`
- 二者均包装已有流
- 导入：`import std.io.*`

---

## 3. 源流（节点流）

### 3.1 标准流
- `getStdIn()` → `ConsoleReader`
- `getStdOut()` / `getStdErr()` → `ConsoleWriter`
- 来自 `std.env.*`
- `ConsoleReader`/`ConsoleWriter` 是**并发安全**的
- 支持基于字符串的操作，性能优于原始 `print`
- `ConsoleWriter` 使用缓冲 — 调用 `flush()` 确保输出

### 3.2 文件流
- 来自 `std.fs.*`
- 静态工具：`exists()`、`copy()`、`rename()`、`remove()`、`File.readFrom()`、`File.writeTo()`
- `File` 实现 `Resource & IOStream & Seekable`
- 构造：`File.create()`（只写）或 `File(path, OpenMode)`
- 打开模式：`Read`、`Write`、`Append`、`ReadWrite`
- 使用 `try-with-resource` 自动清理：
```cangjie
try (file = File(path, OpenMode.Read)) {
    // 使用 file
}
```
