---
name: cangjie-common
description: "仓颉语言核心知识速查。本Skill包含仓颉开发最高频使用的关键知识，涵盖构建运行、语法要点、类型系统、错误处理、并发、集合、I/O等。如果本Skill信息不足以指导开发，再按需引用其他Skill。"
---

# 仓颉语言核心知识速查

- **构建运行**：`cjpm init --name myapp` 初始化项目，`cjpm build` 构建，`cjpm run` 运行，`cjpm test` 测试，`cjpm clean` 清理；单文件编译用 `cjc hello.cj && ./main`
- **入口函数**：程序入口为顶层 `main() { ... }`，无需类包裹；`main` 函数可接受 `Array<String>` 参数获取命令行参数
- **变量声明**：`let` 声明不可变绑定，`var` 声明可变变量；类型可推断也可显式标注，如 `let x: Int64 = 42`
- **基本类型**：整数 `Int8/16/32/64`、`UInt8/16/32/64`（默认 `Int64`），浮点 `Float16/32/64`（默认 `Float64`），`Bool`，`Char`（Unicode 字符），`Unit`（无返回值），`Nothing`（永不返回），`String`（UTF-8 不可变字符串，支持 `${}` 插值），`Byte` 是 `UInt8` 的别名
- **函数定义**：`func name(param: Type, ...): ReturnType { ... }`；支持命名参数 `func f(x!: Int64 = 0)` 调用时 `f(x: 10)`；lambda 表达式为 `{ params => body }`
- **类与结构体**：`class` 引用类型支持继承，`struct` 值类型不支持继承；构造函数用 `init(...) { ... }`；成员默认 `private`，用 `public` 修饰导出；`prop` 定义属性（getter/setter）
- **接口与扩展**：`interface I { ... }` 定义接口，类/结构体通过 `<: I` 实现；`extend Type <: Interface { ... }` 为已有类型添加接口实现或方法
- **枚举**：`enum Color { Red | Green | Blue }` 定义枚举；支持构造器参数 `enum Expr { Lit(Int64) | Add(Expr, Expr) }`；用 `match` 解构
- **模式匹配**：`match (expr) { case pattern => body ... case _ => default }` 支持值模式、类型模式、解构模式、通配符 `_`；`if-let` 可用于 `Option` 解包
- **Option 类型**：可空值用 `?Type` 或 `Option<Type>` 表示；`Some(value)` 和 `None` 两种取值；用 `match`、`if-let`、`getOrThrow()` 等方式解包
- **错误处理**：`try { ... } catch (e: ExceptionType) { ... } finally { ... }` 捕获异常；`throw` 抛出异常；资源管理用 `try (resource = ...) { ... }` 自动调用 `close()`
- **集合类型**：`Array<T>(size, init)` 定长数组；`ArrayList<T>()` 动态列表，支持 `append()`、`remove()`；`HashMap<K, V>()` 哈希表，支持 `put()`、`get()`、`contains()`；遍历用 `for (item in collection)`
- **字符串操作**：`String` 支持 `+` 拼接、`"text ${expr}"` 插值、`.size` 长度、`.isEmpty()` 判空、`.split()`、`.replace()`、`.startsWith()`、`.contains()`、`.toArray()` 转 UTF-8 字节数组；`String.fromUtf8(bytes)` 从字节构建
- **并发编程**：`spawn { => ... }` 创建并发任务；`Future<T>` 获取异步结果（`future.get()`）；`sync.Mutex` 互斥锁保护共享资源；`sync.channel` 提供通道通信
- **包与导入**：源文件顶部 `package mypackage` 声明包；`import std.collection.*` 导入包，`*` 导入所有公开符号；子包对应子目录，目录须包含 `.cj` 文件才是有效包
- **文件与 I/O**：`import std.fs.*` 和 `import std.io.*`；`File(path, OpenOption)` 打开文件，`OpenOption` 包括 `Read`、`Create()`、`Append`；`readToEnd(file)` 读取全部内容；`StringReader/StringWriter` 用于字符串流
- **项目配置**：`cjpm.toml` 中 `[package]` 设置 `name`、`version`、`output-type`（`executable`/`static`/`dynamic`）；`[dependencies]` 配置依赖（`path` 或 `git` 来源）；`[target.<arch>.bin-dependencies]` 配置平台特定的二进制库依赖
- **类型系统要点**：仓颉是静态强类型语言；支持泛型 `func f<T>(x: T)` 和泛型约束 `<T> where T <: Comparable`；所有类型的共同父类型是 `Any`；`is` 判断类型、`as` 类型转换
- **测试**：测试文件命名为 `xxx_test.cj`，与被测源文件同目录；使用 `@Test` 标注测试函数，`@BeforeAll/@AfterAll/@BeforeEach/@AfterEach` 标注生命周期函数；断言用 `@Assert(cond)`、`@ExpectThrow<E>(expr)`；运行 `cjpm test`
- **扩展标准库 stdx**：stdx 需单独下载，从 <https://gitcode.com/Cangjie/cangjie_stdx/releases> 获取；在 `cjpm.toml` 中通过 `bin-dependencies` 配置；crypto/net 模块依赖 **OpenSSL 3**
