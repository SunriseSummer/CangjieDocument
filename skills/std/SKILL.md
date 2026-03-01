---
name: cangjie-std-libs
description: "仓颉标准库使用指南。当需要了解仓颉标准库的包结构、常用包的核心 API（集合、I/O、文件系统、网络、并发同步、时间日期、数学运算、正则表达式、进程管理、随机数、排序、格式化、环境变量等），以及最佳实践时，应使用此 Skill。需要详细 API 信息时请参阅 libs/standard/std 目录下的原始文档。"
---

# 仓颉标准库使用指南 Skill

## 1. 标准库概述

### 1.1 基本信息
- 标准库（std）随 SDK 一起发布，开箱即用
- 由若干**包（package）**组成，每个包可单独编译
- 核心包 `std.core` 自动导入，无需显式 `import`
- 其他包需使用 `import std.xxx.*` 导入

### 1.2 导入语法
```cangjie
import std.collection.*                    // 导入整个包
import std.collection.ArrayList            // 导入单个类型
import std.collection.{ArrayList, HashMap} // 导入多个类型
```

---

## 2. 标准库所有包功能清单

> 需要了解某个包的详细 API 时，请查阅 `libs/standard/std/<包名>/` 目录下的原始文档。

| 包名 | 功能简介 |
|------|----------|
| **core** | 核心包（自动导入）。提供基本类型（Int/Float/Bool/String/Array/Range/Option 等）、print/println/readln、Iterable/Iterator/Comparable/Hashable/ToString 等核心接口、Duration、Thread/Future/spawn、异常基类等 |
| **collection** | 常用集合数据结构：ArrayList、HashMap、HashSet、TreeMap、LinkedList、ArrayDeque、ArrayQueue、ArrayStack，以及 List/Map/Set/Queue/Stack 接口和丰富的函数式迭代操作（map/filter/reduce/fold 等） |
| **collection.concurrent** | 并发安全集合：ConcurrentHashMap、ConcurrentLinkedQueue、ArrayBlockingQueue、LinkedBlockingQueue |
| **io** | I/O 流抽象：InputStream/OutputStream 接口、BufferedInputStream/BufferedOutputStream 缓冲流、StringReader/StringWriter 字符串流、ByteBuffer、ChainedInputStream、MultiOutputStream |
| **fs** | 文件系统操作：File（读写/创建/追加）、Directory（目录操作）、Path（路径处理）、FileInfo（元数据）、exists/copy/rename/remove 等工具函数 |
| **env** | 进程环境：getStdIn/getStdOut/getStdErr 标准流、环境变量读写、工作目录、进程 ID、exit 退出 |
| **net** | 网络通信：TcpSocket/TcpServerSocket（TCP）、UdpSocket（UDP）、UnixSocket（Unix Domain）、IP 地址处理 |
| **sync** | 并发同步：Atomic 原子操作（整数/布尔/引用）、Mutex 互斥锁、Monitor 监视器、Timer 定时器、SyncCounter 同步计数器 |
| **time** | 时间日期：DateTime（日期时间）、Duration（时间间隔）、MonoTime（单调时间）、TimeZone（时区）、格式化与解析 |
| **math** | 数学运算：三角函数、绝对值、平方根、幂、对数、取整、GCD/LCM、位操作等 |
| **math.numeric** | 扩展数值类型：BigInt（任意精度整数）、Decimal（任意精度十进制数） |
| **random** | 伪随机数生成：Random 类 |
| **regex** | 正则表达式：Regex 类，支持查找/分割/替换/验证 |
| **sort** | 排序函数：对 Array/ArrayList/List 进行稳定/不稳定排序 |
| **convert** | 类型转换与格式化：字符串解析为数值（Parsable 接口）、格式化输出（Formattable 接口） |
| **console** | ⚠️ **已弃用**，请使用 std.env 代替 |
| **process** | 进程管理：创建子进程（execute/launch）、获取标准流、进程等待与信息查询 |
| **reflect** | 反射：TypeInfo 获取类型信息、动态访问成员变量/属性/函数 |
| **ast** | 语法树：仓颉源码解析器和 AST 节点，主要用于宏编程 |
| **argopt** | 命令行参数解析：parseArguments 函数，支持短选项/长选项/组合选项 |
| **binary** | 二进制端序转换：BigEndianOrder/LittleEndianOrder 接口 |
| **crypto.digest** | 摘要算法：MD5、SHA1/224/256/384/512、HMAC、SM3 |
| **crypto.cipher** | 对称加解密通用接口 |
| **database.sql** | 数据库接口：连接、查询、事务控制 |
| **deriving** | 自动派生宏：@Derive 自动生成 ToString/Hashable/Equatable/Comparable 实现 |
| **unicode** | Unicode 字符处理 |
| **overflow** | 整数溢出处理：四种策略（Option 返回/饱和/抛异常/截断） |
| **ref** | 弱引用：WeakRef 类，用于缓存和对象池 |
| **objectpool** | 对象池：ObjectPool 缓存与复用对象 |
| **posix** | POSIX 系统调用封装 |
| **runtime** | 运行时环境控制与监视 |
| **unittest** | 单元测试框架（详见 unittest Skill） |
| **unittest.mock** | Mock 测试框架（详见 unittest Skill） |
| **unittest.testmacro** | 单元测试宏 |
| **unittest.mock.mockmacro** | Mock 框架宏 |
| **unittest.common** | 单元测试通用类型 |
| **unittest.diff** | 测试差异对比 |
| **unittest.prop_test** | 参数化测试 |

---

## 3. 核心包（std.core）— 自动导入

### 3.1 常用全局函数
```cangjie
print("hello")              // 输出（不换行）
println("hello")            // 输出（换行）
eprint("error")             // 输出到 stderr
eprintln("error")           // 输出到 stderr（换行）
let line = readln()         // 读取一行标准输入，返回 ?String
let m = min(a, b)           // 返回较小值
let n = max(a, b)           // 返回较大值
sleep(Duration.second * 2)  // 当前线程休眠
```

### 3.2 核心类型别名
```cangjie
// Byte = UInt8，Int = Int64，UInt = UInt64
let b: Byte = 0xFF
let i: Int = 42
```

### 3.3 核心接口
| 接口 | 用途 |
|------|------|
| `ToString` | 提供 `toString()` 方法 |
| `Hashable` | 提供 `hashCode()` 方法 |
| `Equatable<T>` | 提供 `==`/`!=` 比较 |
| `Comparable<T>` | 提供 `<`/`>`/`<=`/`>=` 比较 |
| `Iterable<E>` | 提供 `iterator()` 方法，支持 for-in |
| `Collection<T>` | 集合基础接口 |
| `Resource` | 提供 `isClosed()`/`close()` 方法，用于 try-with-resources |
| `Any` | 所有类型的父接口 |

### 3.4 异常类层次
```
Error（系统错误，不应手动抛出）
  ├── OutOfMemoryError
  └── StackOverflowError

Exception（可捕获处理）
  ├── ArithmeticException
  ├── IllegalArgumentException
  ├── IllegalStateException
  ├── IndexOutOfBoundsException
  ├── NegativeArraySizeException
  ├── NoneValueException
  ├── NullPointerException
  ├── OverflowException
  ├── ConcurrentModificationException
  ├── UnsupportedException
  └── TimeoutException
```

### 3.5 Duration（时间间隔）
```cangjie
let d = Duration.second * 5         // 5 秒
let d2 = 100 * Duration.millisecond // 100 毫秒
// 常用单位：Duration.nanosecond, Duration.microsecond, Duration.millisecond, Duration.second, Duration.minute, Duration.hour
```

### 3.6 StringBuilder
```cangjie
let sb = StringBuilder()
sb.append("Hello")
sb.append(", ")
sb.append("World!")
let s = sb.toString()  // "Hello, World!"
```
- `append()` 支持的参数类型：`String`、`Rune`、`Bool`、`Int8`/`Int16`/`Int32`/`Int64`、`UInt8`/`UInt16`/`UInt32`/`UInt64`、`Float16`/`Float32`/`Float64`、`Array<Rune>`、`StringBuilder`、`CString`， 以及任何实现 `ToString` 接口的泛型类型
- **注意**：所有 `append()` 方法返回 `Unit`

---

## 4. 集合（std.collection）

**导入**：`import std.collection.*`

### 4.1 ArrayList — 动态数组
```cangjie
let list = ArrayList<Int64>()
list.add(1)
list.add(2)
list.add(3)
list[0] = 10                       // 下标修改
let val = list[1]                   // 下标访问
list.add(0, at: 0)                  // 在索引 0 处插入
list.remove(at: 2)                  // 按索引删除
println(list.size)                  // 元素个数
for (item in list) { println(item) }
```

### 4.2 HashMap — 哈希映射
```cangjie
let map = HashMap<String, Int64>()
map.add("a", 1)                     // 添加/更新，返回 Option<V>（旧值或 None）
map["b"] = 2                        // 下标添加/更新
let v = map["a"]                    // 下标访问（键不存在抛 NoneValueException）
let safe = map.get("a")             // 安全访问，返回 ?V（键不存在返回 None）
if (map.contains("a")) {            // 另一种安全方式：先检查再取值
    let v2 = map["a"]
}
let has = map.contains("a")         // 检查键是否存在
map.remove("b")                     // 按键删除
for ((k, v) in map) { println("${k}: ${v}") }
```
- `K` 须实现 `Hashable` 和 `Equatable<K>`

### 4.3 HashSet — 哈希集合（无序、去重）
```cangjie
let set = HashSet<Int64>()
set.add(1)
set.add(2)
set.add(1)                          // 已存在，无效果
let has = set.contains(1)           // 检查元素
set.remove(2)                       // 按值删除
for (item in set) { println(item) } // 遍历顺序不保证
```
- `T` 须实现 `Hashable` 和 `Equatable<T>`

### 4.4 其他集合类型
| 类型 | 说明 |
|------|------|
| `TreeMap<K, V>` | 基于红黑树的有序映射（`K` 须实现 `Comparable<K>`） |
| `LinkedList<T>` | 双向链表，高效的头尾增删 |
| `ArrayDeque<T>` | 双端队列 |
| `ArrayQueue<T>` | 环形队列（尾部插入、头部删除） |
| `ArrayStack<T>` | 栈（后进先出） |

### 4.5 函数式迭代操作
```cangjie
import std.collection.*

let list = ArrayList<Int64>([1, 2, 3, 4, 5])
// 通过迭代器使用函数式操作
let result = list
    |> filter { v => v % 2 == 1 }
    |> map { v => v.toString() }
    |> collectArrayList
```

常用迭代函数（应用于 `Iterator<T>`）：
| 函数 | 说明 |
|------|------|
| `filter` | 过滤元素 |
| `map` | 转换元素 |
| `flatMap` | 转换并展平 |
| `fold` | 累积计算（带初始值） |
| `reduce` | 累积计算（无初始值） |
| `forEach` | 遍历执行 |
| `count` | 计数 |
| `any` / `all` / `none` | 谓词检查 |
| `first` / `last` | 获取首/尾元素 |
| `take` / `skip` | 取前 n 个 / 跳过前 n 个 |
| `enumerate` | 带索引遍历 |
| `zip` | 配对两个迭代器 |
| `concat` | 连接两个迭代器 |
| `collectArrayList` / `collectHashMap` / `collectHashSet` | 收集为集合 |

---

## 5. I/O 流（std.io）

**导入**：`import std.io.*`

### 5.1 核心接口
```cangjie
// 输入流
interface InputStream {
    func read(buffer: Array<Byte>): Int64  // 返回实际读取的字节数
}
// 输出流
interface OutputStream {
    func write(buffer: Array<Byte>): Unit
    func flush(): Unit
}
```

### 5.2 缓冲流
```cangjie
import std.io.*
import std.fs.*

// 使用 BufferedOutputStream 写文件
try (file = File.create("output.txt")) {
    let bos = BufferedOutputStream(file)
    let sw = StringWriter(bos)
    sw.writeln("Hello, World!")
    sw.flush()  // 必须 flush 确保数据写入
}

// 使用 BufferedInputStream 读文件
try (file = File("output.txt", OpenMode.Read)) {
    let bis = BufferedInputStream(file)
    let sr = StringReader(bis)
    let line = sr.readln()  // 读取一行
}
```

### 5.3 StringReader / StringWriter
```cangjie
// StringWriter：将字符串/数值写入输出流
let sw = StringWriter(outputStream)
sw.write("text")
sw.writeln("line")
sw.write(42)           // 写入数值的字符串表示

// StringReader：从输入流读取字符串
let sr = StringReader(inputStream)
let line = sr.readln()  // 按行读取，返回 ?String
```

---

## 6. 文件系统（std.fs）

**导入**：`import std.fs.*`

### 6.1 文件操作
```cangjie
// 检查文件是否存在
let exist = exists("test.txt")

// 快捷读写（适合小文件）
File.writeTo("test.txt", "Hello World".toArray())
let content = File.readFrom("test.txt")

// 流式读写（适合大文件）
try (file = File("data.txt", OpenMode.Read)) {
    let buf = Array<Byte>(1024, repeat: 0)
    let n = file.read(buf)  // 读取数据
}

try (file = File.create("output.txt")) {
    file.write("Hello".toArray())
}

// 文件操作工具
copy("src.txt", "dst.txt")
rename("old.txt", "new.txt")
remove("temp.txt")
```

### 6.2 打开模式
| 模式 | 说明 |
|------|------|
| `OpenMode.Read` | 只读（文件须存在） |
| `OpenMode.Write` | 只写（文件不存在则创建，存在则截断为空） |
| `OpenMode.Append` | 追加写入（文件不存在则创建） |
| `OpenMode.ReadWrite` | 读写（文件不存在则创建，不截断） |

### 6.3 目录操作
```cangjie
Directory.create("new_dir")                  // 创建目录
Directory.create("a/b/c", recursive: true)   // 递归创建
let entries = Directory.list(".")            // 列出目录内容
Directory.delete("empty_dir")               // 删除空目录
```

---

## 7. 环境与标准流（std.env）

**导入**：`import std.env.*`

```cangjie
// 标准流（比 print/println 更灵活，支持缓冲）
let stdin = getStdIn()       // ConsoleReader
let stdout = getStdOut()     // ConsoleWriter
let stderr = getStdErr()     // ConsoleWriter
stdout.write("hello")
stdout.flush()               // 显式刷新缓冲区

// 环境变量
let home = getVariable("HOME")   // 返回 ?String
setVariable("MY_VAR", "value")

// 目录信息
let cwd = getWorkingDirectory()
let home = getHomeDirectory()
let tmp = getTempDirectory()

// 进程控制
let pid = getProcessId()
exit(0)                           // 退出进程
```

---

## 8. 并发同步（std.sync）

**导入**：`import std.sync.*`

### 8.1 原子操作
```cangjie
let counter = AtomicInt64(0)
counter.store(10)
let val = counter.load()              // 10
counter.fetchAdd(5)                   // 返回旧值 10，新值为 15
let ok = counter.compareAndSwap(15, 20) // CAS 操作
```

### 8.2 互斥锁与 synchronized
```cangjie
let mtx = Mutex()

// 方式一：手动加锁/解锁
mtx.lock()
// ... 临界区 ...
mtx.unlock()

// 方式二：synchronized 自动加锁/解锁（推荐）
let result = synchronized(mtx) {
    // 临界区，退出时自动解锁（包括异常退出）
    computeResult()
}
```

### 8.3 条件变量
```cangjie
let mtx = Mutex()
let cond = mtx.condition()

// 等待线程
synchronized(mtx) {
    while (!ready) {
        cond.wait()          // 等待通知
    }
}

// 通知线程
synchronized(mtx) {
    ready = true
    cond.notifyAll()         // 唤醒所有等待线程
}
```

### 8.4 并发安全集合
```cangjie
import std.collection.concurrent.*

let cmap = ConcurrentHashMap<String, Int64>()
cmap.put("key", 42)
let v = cmap.get("key")     // 返回 ?Int64
```

---

## 9. 时间日期（std.time）

**导入**：`import std.time.*`

```cangjie
// 获取当前时间
let now = DateTime.now()
println(now.toString())

// 构造时间
let dt = DateTime.of(year: 2024, month: 6, dayOfMonth: 15, hour: 10, minute: 30)

// 格式化
let formatted = now.toString("yyyy-MM-dd HH:mm:ss")

// 时间计算
let later = now + Duration.hour * 2
let diff = later - now           // Duration

// 单调时间（用于计时，不受系统时间调整影响）
let start = MonoTime.now()
// ... 执行操作 ...
let elapsed = MonoTime.now() - start  // Duration
```

---

## 10. 数学运算（std.math）

**导入**：`import std.math.*`

```cangjie
let a = abs(-5)              // 5
let s = sqrt(16.0)           // 4.0
let p = pow(2.0, 10.0)       // 1024.0
let l = log(100.0)           // 自然对数
let c = ceil(3.2)            // 4.0
let f = floor(3.8)           // 3.0
let g = gcd(12, 18)          // 6
let l = lcm(4, 6)            // 12
let clamped = clamp(15, 0, 10) // 10（限制在范围内）
// 三角函数：sin, cos, tan, asin, acos, atan
```

### 扩展数值类型（std.math.numeric）
```cangjie
import std.math.numeric.*

let big = BigInt("123456789012345678901234567890")
let sum = big + BigInt("1")

let d = Decimal("3.14159265358979323846")
let product = d * Decimal("2")
```

---

## 11. 正则表达式（std.regex）

**导入**：`import std.regex.*`

```cangjie
let re = Regex(#"(\d{4})-(\d{2})-(\d{2})"#)

// 查找匹配
let m = re.find("Date: 2024-06-15")
if (let Some(mat) <- m) {
    println(mat.matchStr())        // "2024-06-15"
    println(mat.group(1))          // "2024"
}

// 查找所有匹配
let allMatches = re.findAll("2024-01-01 and 2024-06-15")

// 替换
let result = re.replace("2024-06-15", "****-**-**")

// 分割
let parts = Regex(#"\s+"#).split("hello   world   foo")

// 验证
let isValid = re.fullMatch("2024-06-15")  // 完整匹配检查
```

---

## 12. 随机数（std.random）

**导入**：`import std.random.*`

```cangjie
let rng = Random()
let rng2 = Random(42)          // 指定种子，可复现

let i = rng.nextInt64()        // 随机 Int64
let u = rng.nextUInt64()       // 随机 UInt64
let f = rng.nextFloat64()      // [0.0, 1.0) 之间的随机浮点数
let b = rng.nextBool()         // 随机布尔值
```

---

## 13. 排序（std.sort）

**导入**：`import std.sort.*`

```cangjie
// Array 排序（元素须实现 Comparable）
var arr = [3, 1, 4, 1, 5, 9, 2, 6]
sort(arr)                           // 原地升序排序

// 自定义比较器排序
sort(arr) { a, b => b - a }        // 降序排序

// ArrayList 排序
let list = ArrayList<Int64>([3, 1, 2])
sort(list)
```

---

## 14. 进程管理（std.process）

**导入**：`import std.process.*`

```cangjie
// 执行命令并等待完成
let status = execute("ls", ["-la"])

// 执行命令并捕获输出
let (status, stdout, stderr) = executeWithOutput("echo", ["hello"])

// 异步启动子进程
let proc = launch("long_running_command", [])
// ... 做其他工作 ...
let exitCode = proc.wait()
```

---

## 15. 类型转换与格式化（std.convert）

**导入**：`import std.convert.*`

### 15.1 字符串解析为数值（Parsable 接口）
```cangjie
import std.convert.*

// parse：解析失败抛 IllegalArgumentException
let n = Int64.parse("42")           // 42
let f = Float64.parse("3.14")      // 3.14
let b = Bool.parse("true")         // true

// tryParse：解析失败返回 None
let opt = Float64.tryParse("abc")  // None
let val = Int64.tryParse("42")     // Some(42)
```
- `parse(value: String): T` — 解析失败抛出 `IllegalArgumentException`
- `tryParse(value: String): Option<T>` — 解析失败返回 `None`
- 支持的类型：`Bool`、`Int8`/`Int16`/`Int32`/`Int64`、`UInt8`/`UInt16`/`UInt32`/`UInt64`、`Float16`/`Float32`/`Float64`、`Rune`

### 15.2 格式化输出（Formattable 接口）
```cangjie
import std.convert.*  // format 方法需要导入此包

let hex = UInt32(255).format("x")     // "ff"（十六进制）
let padded = 42.format(">10")         // "        42"（右对齐，宽度 10）
```
- **`format()` 方法由 `Formattable` 接口提供，需要 `import std.convert.*`**
- 支持的类型：所有整数类型、所有浮点类型、`Rune`
- 也可使用字符串插值格式化：
  ```cangjie
  let hex = "${255:x}"                // "ff"
  let padded = "${42:>10}"            // "        42"
  ```

---

## 16. 网络通信（std.net）

**导入**：`import std.net.*`

### TCP 服务端
```cangjie
let server = TcpServerSocket(bindAt: 8080)
server.bind()
let client = server.accept()        // 阻塞等待连接
let buf = Array<Byte>(1024, repeat: 0)
let n = client.read(buf)
client.write("Hello".toArray())
client.close()
server.close()
```

### TCP 客户端
```cangjie
let socket = TcpSocket("127.0.0.1", 8080)
socket.connect()
socket.write("Hello".toArray())
let buf = Array<Byte>(1024, repeat: 0)
let n = socket.read(buf)
socket.close()
```

---

## 17. 自动派生（std.deriving）

**导入**：`import std.deriving.*`

### 17.1 基本用法
```cangjie
import std.deriving.*

@Derive[ToString, Hashable, Equatable]
struct Point {
    let x: Int64
    let y: Int64
    public init(x: Int64, y: Int64) {
        this.x = x
        this.y = y
    }
}
// 自动生成 toString()、hashCode()、==、!= 实现
```

### 17.2 支持派生的接口
| 接口 | 自动生成 |
|------|----------|
| `ToString` | `toString()` 方法 |
| `Hashable` | `hashCode()` 方法 |
| `Equatable` | `==`、`!=` 运算符 |
| `Comparable` | `<`、`>`、`<=`、`>=` 比较（自动包含 `Equatable`） |

### 17.3 适用类型
- `@Derive` 可用于 `struct`、`class` 和 `enum` 类型
- **枚举类型默认不支持 `==` 比较**，须使用 `@Derive[Equatable]` 派生：
  ```cangjie
  import std.deriving.*
  
  @Derive[Equatable]
  enum TokenKind {
      | Number | Plus | Minus | Eof
  }
  // 现在可以使用 == 比较 TokenKind 值
  ```

### 17.4 辅助宏
- `@DeriveExclude`：排除某些成员不参与派生
- `@DeriveInclude`：指定仅包含某些成员参与派生
- `@DeriveOrder`：指定成员参与派生的顺序

---

## 18. 最佳实践

### 18.1 资源管理
- **始终**使用 `try-with-resources` 管理 File 等实现 `Resource` 接口的对象
```cangjie
try (file = File("data.txt", OpenMode.Read)) {
    // 使用 file，退出时自动关闭
}
```

### 18.2 集合选择
| 场景 | 推荐类型 |
|------|----------|
| 固定大小、频繁随机访问 | `Array<T>` |
| 动态增删、随机访问 | `ArrayList<T>` |
| 键值映射、快速查找 | `HashMap<K, V>` |
| 键值映射、需有序遍历 | `TreeMap<K, V>` |
| 去重集合 | `HashSet<T>` |
| 频繁头尾操作 | `LinkedList<T>` 或 `ArrayDeque<T>` |
| 并发安全映射 | `ConcurrentHashMap<K, V>` |
| 并发安全队列 | `ConcurrentLinkedQueue<T>` 或阻塞队列 |

### 18.3 并发编程
- 使用 `synchronized(mtx) { ... }` 代替手动 `lock()/unlock()`，避免忘记解锁
- 对简单计数器等场景优先使用 `Atomic` 类型而非互斥锁
- 使用 `Future<T>.get()` 等待线程结果，注意 `get()` 位置影响并行度
- 并发安全集合（`std.collection.concurrent`）适用于多线程共享数据

### 18.4 错误处理
- 使用 `Option<T>`（`?T`）表示可能缺失的值，而非返回特殊值或抛异常
- 使用 `??` 提供默认值：`let name = getName() ?? "unknown"`
- 使用 `?.` 进行安全链式调用：`user?.address?.city`
- 仅在真正异常情况下使用 `throw`/`try-catch`

### 18.5 I/O 性能
- 使用 `BufferedInputStream`/`BufferedOutputStream` 包装原始流以减少系统调用
- 写入完成后**务必**调用 `flush()` 确保数据写入
- 使用 `StringReader`/`StringWriter` 进行字符串级别的 I/O

### 18.6 字符串处理
- 使用字符串插值 `"${expr}"` 代替字符串拼接
- 大量拼接时使用 `StringBuilder` 提高性能
- 使用 `std.regex` 进行复杂文本匹配和处理
- **注意**：`String` 实现了 `Collection<Byte>`，`for (c in s)` 迭代的是 UTF-8 编码字节（`UInt8`），而非字符。使用 `for (c in s.runes())` 迭代 Unicode 字符（`Rune`）
