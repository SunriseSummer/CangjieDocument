# 仓颉标准库精炼总结

> 本文档面向 AI 工具，精炼覆盖仓颉（Cangjie）标准库的核心功能与常用 API。文末附完整包清单，供需要了解详细或次要内容时查阅源文档。

---

## 1. std.core — 核心包（自动导入，无需 import）

### 1.1 常用函数

| 函数 | 签名 | 说明 |
|------|------|------|
| `print` | `print(value, flush!: Bool = false)` | 输出到 stdout，支持所有基础类型及 `ToString` |
| `println` | `println(value)` / `println()` | 输出并换行 |
| `eprint` / `eprintln` | 同上，输出到 stderr | 标准错误输出 |
| `readln` | `readln(): String` | 从控制台读取一行 |
| `sleep` | `sleep(dur: Duration)` | 阻塞当前线程 |
| `max` / `min` | `max<T>(a, b, ...others)` | 返回最大/最小值，`T <: Comparable<T>` |
| `refEq` | `refEq(a: Object, b: Object): Bool` | 判断两个对象是否为同一内存地址 |
| `sizeOf<T>` / `alignOf<T>` | 返回 `UIntNative` | C 类型的大小/对齐，`T <: CType` |
| `zeroValue<T>` | `zeroValue<T>(): T` | 返回类型 T 的零值实例 |
| `ifSome` / `ifNone` | `ifSome(opt, action)` | 对 Option 值执行条件操作 |

### 1.2 类型别名

```cangjie
type Byte = UInt8
type Int  = Int64
type UInt = UInt64
```

### 1.3 核心接口

| 接口 | 说明 |
|------|------|
| `Any` | 所有类型的父类型 |
| `ToString` | `toString(): String` |
| `Hashable` | `hashCode(): Int64` |
| `Equatable<T>` | `==` / `!=`，继承自 `Equal<T>` & `NotEqual<T>` |
| `Comparable<T>` | `compare(that: T): Ordering`，继承自 `Equatable` + `Less` + `Greater` + `LessOrEqual` + `GreaterOrEqual` |
| `Iterable<E>` | `iterator(): Iterator<E>`，支持 `for-in` |
| `Collection<T>` | 继承 `Iterable<T>`，提供 `size` 属性和 `isEmpty()`/`toArray()` |
| `Resource` | `close(): Unit` + `isClosed(): Bool`，支持 try-with-resources |
| `Countable<T>` | `next(right: Int64): T` + `position(): Int64` |
| `CType` | 密封接口，标记 C 互操作兼容类型 |
| `Hasher` | 哈希组合操作 |
| `ThreadContext` | 线程上下文控制 |

### 1.4 核心类

| 类 | 说明 |
|----|------|
| `Object` | 所有类的父类 |
| `Iterator<T>` | 迭代器基类，提供 50+ 扩展方法（见下） |
| `Future<T>` | 线程结果，`get()`/`tryGet()`/`cancel()` |
| `Thread` | 线程对象，`currentThread`/`hasPendingCancellation` |
| `Box<T>` | 值包装类（引用语义） |
| `StringBuilder` | 可变字符串构建器，支持多类型 `append` |
| `StackTraceElement` | 异常栈帧信息 |

**Iterator 常用扩展方法**：
- 转换：`map`、`flatMap`、`filterMap`
- 过滤：`filter`、`skip`、`take`、`step`
- 聚合：`fold`、`reduce`、`count`、`all`、`any`、`none`
- 查找：`first`、`last`、`at`、`contains`（需 `Equatable`）
- 组合：`concat`、`zip`、`enumerate`、`intersperse`
- 统计：`max`、`min`（需 `Comparable`）
- 消费：`forEach`、`isEmpty`
- 调试：`inspect`

### 1.5 核心结构体

| 结构体 | 说明 |
|--------|------|
| `Array<T>` | 固定长度数组（可变元素），支持切片/拼接/克隆/映射 |
| `String` | 不可变 UTF-8 字符串，50+ 方法（`split`/`replace`/`trim`/`indexOf`/`contains`/`join` 等） |
| `Range<T>` | 区间类型，支持迭代 |
| `Duration` | 时间间隔，静态常量 `day`/`hour`/`minute`/`second`/`millisecond`/`microsecond`/`nanosecond` |
| `DefaultHasher` | 默认哈希器实现 |
| `LibC` | C 互操作辅助：`malloc<T>`/`free`/`mallocCString` |
| `CPointerHandle<T>` | C 指针句柄 |

### 1.6 核心枚举

| 枚举 | 说明 |
|------|------|
| `Option<T>` | `Some(T)` \| `None`，提供 `map`/`flatMap`/`filter`/`getOrDefault`/`getOrThrow`/`isSome`/`isNone` |
| `Ordering` | `LT` \| `EQ` \| `GT` |
| `Endian` | `Big` \| `Little`，`Platform` 属性获取平台字节序 |
| `AnnotationKind` | 注解可应用位置 |

### 1.7 常见异常

| 异常 | 说明 |
|------|------|
| `Exception` | 所有可捕获异常基类 |
| `Error` | 系统错误基类（不可手动 throw） |
| `IllegalArgumentException` | 非法参数 |
| `IndexOutOfBoundsException` | 越界 |
| `NoneValueException` | Option 为 None 时 getOrThrow |
| `ArithmeticException` / `OverflowException` | 算术/溢出错误 |
| `IllegalStateException` | 非法状态 |
| `TimeoutException` | 超时 |
| `SpawnException` | 线程创建异常 |
| `OutOfMemoryError` / `StackOverflowError` | 内存/栈溢出（Error 子类） |

---

## 2. std.collection — 集合

`import std.collection.*`

| 类型 | 说明 |
|------|------|
| `ArrayList<T>` | 动态数组，支持增删改查 |
| `LinkedList<T>` | 双向链表 |
| `ArrayDeque<T>` | 双端循环队列 |
| `ArrayQueue<T>` | 循环队列 |
| `ArrayStack<T>` | 栈（LIFO） |
| `HashMap<K,V>` | 哈希表（K 需 `Hashable` + `Equatable`） |
| `HashSet<T>` | 哈希集合（唯一元素） |
| `TreeMap<K,V>` | 红黑树有序映射 |
| `TreeSet<T>` | 有序集合 |

**核心接口**：`List<T>`、`Map<K,V>`、`Set<T>`、`Queue<T>`、`Stack<T>`、`Deque<T>`、`ReadOnlyList<T>`、`ReadOnlyMap<K,V>`、`ReadOnlySet<T>`

**迭代器函数**（全局）：`all`、`any`、`at`、`collect*`（ArrayList/Array/HashMap/HashSet/String）、`concat`、`contains`、`count`、`enumerate`、`filter`、`filterMap`、`first`、`flatMap`、`flatten`、`fold`、`forEach`、`inspect`、`isEmpty`、`last`、`map`、`max`、`min`、`none`、`reduce`、`skip`、`step`、`take`、`zip`

---

## 3. std.collection.concurrent — 并发安全集合

`import std.collection.concurrent.*`

| 类型 | 说明 |
|------|------|
| `ConcurrentHashMap<K,V>` | 线程安全哈希表 |
| `ConcurrentLinkedQueue<E>` | 无锁队列 |
| `ArrayBlockingQueue<E>` | 有界阻塞队列 |
| `LinkedBlockingQueue<E>` | 阻塞队列 |

---

## 4. std.sync — 同步与并发

`import std.sync.*`

| 类型 | 说明 |
|------|------|
| `Mutex` | 可重入互斥锁，配合 `synchronized(mutex) { ... }` |
| `ReadWriteLock` | 读写锁 |
| `Barrier` | 屏障同步 |
| `Semaphore` | 信号量 |
| `Condition` | 条件变量 |
| `SyncCounter` | 倒计数同步器 |
| `Timer` | 定时器 |
| `AtomicInt8/16/32/64` | 原子整数操作：`load`/`store`/`swap`/`compareAndSwap`/`fetchAdd`/`fetchSub` |
| `AtomicBool` | 原子布尔：`read`/`write`/`swap` |
| `AtomicReference<T>` | 原子引用 |

---

## 5. std.io — I/O 流

`import std.io.*`

| 类型 | 说明 |
|------|------|
| `InputStream` / `OutputStream` / `IOStream` | 输入/输出/双向流接口 |
| `Seekable` | 游标定位接口 |
| `BufferedInputStream` / `BufferedOutputStream` | 缓冲流 |
| `ByteBuffer` | 字节缓冲区 |
| `ChainedInputStream` | 链式输入流 |
| `MultiOutputStream` | 多路输出流 |
| `StringReader` / `StringWriter` | 字符串读写流 |

**函数**：`copy`（流到流）、`readString`、`readToEnd`

---

## 6. std.fs — 文件系统

`import std.fs.*`

| 类型 | 说明 |
|------|------|
| `File` | 文件打开/创建/读写/关闭 |
| `Directory` | 目录创建/遍历/属性查询 |
| `Path` | 路径操作与查询 |
| `FileInfo` | 文件元数据 |
| `HardLink` / `SymbolicLink` | 硬链接/符号链接 |

**全局函数**：`canonicalize`、`copy`、`exists`、`rename`、`remove`、`removeIfExists`

**文件打开模式**：`OpenMode.Read` / `Write` / `Append` / `ReadWrite`

```cangjie
try (file = File("data.txt", OpenMode.Read)) {
    let content = readString(file)
}
```

---

## 7. std.net — 网络

`import std.net.*`

| 类型 | 说明 |
|------|------|
| `TcpSocket` / `TcpServerSocket` | TCP 客户端/服务端 |
| `UdpSocket` | UDP 套接字 |
| `UnixSocket` / `UnixServerSocket` | Unix 域流套接字 |
| `UnixDatagramSocket` | Unix 域数据报 |
| `IPAddress` / `IPv4Address` / `IPv6Address` | IP 地址 |
| `IPSocketAddress` / `UnixSocketAddress` | 套接字地址 |
| `SocketOptions` | 套接字选项配置 |

---

## 8. std.time — 时间

`import std.time.*`

| 类型 | 说明 |
|------|------|
| `DateTime` | 日期时间，支持运算/比较/格式化/解析 |
| `TimeZone` | 时区 |
| `DateTimeFormat` | 时间格式化器 |
| `DayOfWeek` / `Month` | 星期/月份枚举 |
| `Duration` | 时间间隔（在 core 包中定义） |

**格式化字母**：`y`（年）、`M`（月）、`d`（日）、`H`（24 时）、`h`（12 时）、`m`（分）、`s`（秒）、`S`（亚秒）、`z`（时区名）、`Z`（UTC 偏移）、`a`（AM/PM）

---

## 9. std.math — 数学运算

`import std.math.*`

**函数分类**：

| 类别 | 函数 |
|------|------|
| 绝对值 | `abs`、`checkedAbs` |
| 三角函数 | `sin`、`cos`、`tan`、`asin`、`acos`、`atan`、`atan2` |
| 双曲函数 | `sinh`、`cosh`、`tanh`、`asinh`、`acosh`、`atanh` |
| 指数/对数 | `exp`、`exp2`、`log`、`log2`、`log10`、`logBase` |
| 幂/根 | `pow`、`sqrt`、`cbrt` |
| 取整 | `ceil`、`floor`、`round`、`trunc`、`clamp` |
| 整数数学 | `gcd`、`lcm` |
| 位操作 | `countOnes`、`leadingZeros`、`trailingZeros`、`reverse`、`rotate` |
| 其他 | `erf`、`gamma`、`fmod` |

**核心接口**：`FloatingPoint<T>`、`Integer<T>`、`Number<T>`、`MaxMinValue<T>`

---

## 10. std.env — 环境与进程

`import std.env.*`

| 函数 | 说明 |
|------|------|
| `getStdIn()` / `getStdOut()` / `getStdErr()` | 标准流 |
| `getVariable(name)` / `setVariable(name, value)` | 环境变量 |
| `getProcessId()` | 进程 ID |
| `getWorkingDirectory()` / `getHomeDirectory()` / `getTempDirectory()` | 目录路径 |
| `getCommand()` / `getCommandLine()` | 命令信息 |
| `atExit(callback)` | 注册退出回调 |
| `exit(code)` | 退出进程 |

---

## 11. std.regex — 正则表达式

`import std.regex.*`

- **核心类**：`Regex`（编译正则）
- **结果结构体**：`MatchData`（匹配结果）、`Position`（匹配位置）
- **支持语法**：`^$.*+?|[]` 基础、`\d\D\s\S\w\W\b\B` 转义、`{n,m}` 量词、`(?:)` 非捕获组、`(?=)(?!)(?<=)(?<!)` 前后向断言、`(?i)` 不区分大小写、最多 63 个捕获组
- **注意**：不限制 `{n,m}` 重复次数（存在 ReDos 风险），字符串不可含 `\0`

---

## 12. std.sort — 排序

`import std.sort.*`

```cangjie
sort<T>(array, stable!: Bool = true, ascending!: Bool = true)  // T <: Comparable<T>
sort<T>(array, comparator, stable!, ascending!)                 // 自定义比较函数
sort<T, K>(array, keyExtractor, stable!, ascending!)            // 按键排序
```

支持 `Array<T>`、`ArrayList<T>`、`List<T>`。

---

## 13. std.convert — 类型转换与格式化

`import std.convert.*`

| 接口 | 说明 |
|------|------|
| `Parsable<T>` | 从字符串解析类型 |
| `RadixConvertible<T>` | 按进制解析 |
| `Formattable` | 自定义格式化输出 |

**格式规范**：`[flags][width][.precision][specifier]`
- 标志：`-`（左对齐）、`+`（显示符号）、`#`（进制前缀）、`0`（补零）
- 说明符：`b/B`（二进制）、`o/O`（八进制）、`x/X`（十六进制）、`e/E`（科学计数）、`g/G`（通用浮点）

---

## 14. std.process — 进程管理

`import std.process.*`

| 函数 | 说明 |
|------|------|
| `execute(cmd, args, ...)` | 创建子进程，等待完成，返回退出状态 |
| `executeWithOutput(...)` | 同上，并返回 stdout/stderr |
| `launch(cmd, args, ...)` | 创建子进程，返回 `SubProcess` 实例 |
| `findProcess(pid)` | 绑定已有进程 |

- `SubProcess` 提供 `stdin`/`stdout`/`stderr` 管道和 `wait()` 方法。

---

## 15. std.random — 随机数

`import std.random.*`

- **核心类**：`Random`，提供伪随机数生成。

---

## 16. std.reflect — 反射

`import std.reflect.*`

- `TypeInfo.of(instance)` / `TypeInfo.of<T>()` / `TypeInfo.get("module.package.type")`
- 仅 `public` 成员可见；支持 Linux、Windows（不支持 macOS）
- 类型信息类：`ClassTypeInfo`、`InterfaceTypeInfo`、`StructTypeInfo`、`PrimitiveTypeInfo`
- 成员信息：`ConstructorInfo`、`InstanceFunctionInfo`、`StaticFunctionInfo`、`InstanceVariableInfo`、`InstancePropertyInfo` 等

---

## 17. 其他常用包简介

| 包 | 说明 |
|----|------|
| `std.math.numeric` | 大数类型 `BigInt`（任意精度整数）和 `Decimal`（任意精度小数） |
| `std.overflow` | 整数溢出策略接口：`CheckedOp`（返回 Option）、`SaturatingOp`（饱和）、`ThrowingOp`（抛异常）、`WrappingOp`（截断） |
| `std.binary` | 字节序转换接口：`BigEndianOrder<T>`、`LittleEndianOrder<T>`、`SwapEndianOrder<T>` |
| `std.argopt` | 命令行参数解析：`parseArguments()` 函数，支持短/长选项、组合选项 |
| `std.deriving` | 自动派生宏 `@Derive`，支持自动实现 `ToString`/`Hashable`/`Equatable`/`Comparable` |
| `std.unicode` | Unicode 字符处理，扩展 `Rune` 和 `String` 的 Unicode 属性查询 |
| `std.ref` | 弱引用 `WeakRef<T>`，支持 `EAGER`/`DEFERRED` 回收策略 |
| `std.objectpool` | 对象池 `ObjectPool<T>`（已弃用），线程间对象缓存复用 |
| `std.runtime` | 运行时交互：`gc()`、堆内存指标、线程信息、`blackBox<T>()`（防止编译优化） |
| `std.posix` | POSIX 系统调用封装（文件操作、系统信息、进程操作） |
| `std.ast` | 源码解析为 AST：`cangjieLex()`、`parseProgram()`、`parseDecl()`、`parseExpr()` 等，100+ 节点类型 |
| `std.database.sql` | 数据库访问接口：`Driver`、`Connection`、`Statement`、`Transaction`、`QueryResult`；需数据库驱动 |
| `std.crypto.digest` | 摘要算法：MD5、SHA1/224/256/384/512、HMAC、SM3 |
| `std.crypto.cipher` | 对称加密接口 `BlockCipher` |
| `std.console` | 标准 I/O 交互（已弃用，使用 `std.env` 替代） |

---

## 18. 标准库完整包清单

> 以下为仓颉标准库所有包的功能简介。详细 API 请查阅 `libs/standard/std/<包名>/` 下的源文档。

| 包全名 | 功能简介 |
|--------|---------|
| `std.core` | 核心包：内置类型、常用函数（print/println/readln）、核心接口（ToString/Hashable/Equatable/Comparable/Iterable/Collection/Resource）、Array/String/Range/Duration/Option/Iterator 等基础类型和异常类。自动导入 |
| `std.argopt` | 命令行参数解析 |
| `std.ast` | 源码词法分析与语法解析，AST 节点操作，宏上下文 API |
| `std.binary` | 基本数据类型的字节序（大端/小端）转换 |
| `std.collection` | 数据结构集合：ArrayList、LinkedList、ArrayDeque、ArrayQueue、ArrayStack、HashMap、HashSet、TreeMap、TreeSet 及相关接口 |
| `std.collection.concurrent` | 线程安全集合：ConcurrentHashMap、ConcurrentLinkedQueue、ArrayBlockingQueue、LinkedBlockingQueue |
| `std.console` | 标准 I/O 交互（已弃用） |
| `std.convert` | 字符串与类型互转、格式化输出 |
| `std.crypto.cipher` | 对称加密/解密通用接口 |
| `std.crypto.digest` | 摘要算法（MD5、SHA 系列、HMAC、SM3） |
| `std.database.sql` | 数据库访问接口（SQL/CLI 标准） |
| `std.deriving` | 自动派生宏（ToString/Hashable/Equatable/Comparable） |
| `std.env` | 进程环境：标准流、环境变量、目录路径、进程信息 |
| `std.fs` | 文件系统操作：文件/目录/路径/链接 |
| `std.io` | I/O 流抽象：缓冲流、字节缓冲、字符串读写流 |
| `std.math` | 数学运算：三角函数、指数对数、取整、GCD/LCM、位操作 |
| `std.math.numeric` | 扩展数值类型：BigInt（任意精度整数）、Decimal（任意精度小数） |
| `std.net` | 网络通信：TCP/UDP/Unix 域套接字 |
| `std.objectpool` | 对象缓存池（已弃用） |
| `std.overflow` | 整数溢出处理策略接口 |
| `std.posix` | POSIX 系统调用（文件、系统信息、进程） |
| `std.process` | 进程管理：创建/执行/等待子进程 |
| `std.random` | 伪随机数生成 |
| `std.ref` | 弱引用（WeakRef） |
| `std.reflect` | 运行时反射（类型信息、成员访问/调用） |
| `std.regex` | 正则表达式匹配/替换/分割 |
| `std.runtime` | 运行时环境交互：GC 控制、堆内存指标、CPU profiling |
| `std.sort` | 数组/列表排序（稳定/不稳定） |
| `std.sync` | 并发同步：Mutex、ReadWriteLock、Barrier、Semaphore、Condition、原子操作、Timer |
| `std.time` | 日期时间：DateTime、TimeZone、DateTimeFormat、Duration |
| `std.unicode` | Unicode 字符属性查询与大小写转换 |
| `std.unittest` | 单元测试框架（详见 unittest.md） |
| `std.unittest.common` | 单元测试公共工具 |
| `std.unittest.diff` | 测试比较差异打印 |
| `std.unittest.mock` | Mock 测试框架 |
| `std.unittest.mock.mockmacro` | Mock 框架宏 |
| `std.unittest.prop_test` | 属性测试/参数化测试 |
| `std.unittest.testmacro` | 单元测试宏 |
