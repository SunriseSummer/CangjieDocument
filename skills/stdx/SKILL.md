---
name: cangjie-stdx
description: "仓颉扩展标准库（stdx）使用指南。当需要了解 stdx 的下载配置、HTTP 服务/客户端、JSON 编解码、Base64/Hex 编码、URL 处理、TLS 安全通信、加密解密、数字证书、日志、序列化、压缩、面向切面编程、模糊测试等能力时，应使用此 Skill。"
---

# 仓颉扩展标准库（stdx）使用指南 Skill

## 1. stdx 概述

### 1.1 简介

stdx 是仓颉编程语言的**扩展标准库**（非核心标准库），提供标准库之外的更多实用能力，涵盖：

| 模块 | 包名 | 功能 |
|------|------|------|
| **HTTP** | `stdx.net.http` | HTTP/1.1、HTTP/2 客户端与服务端、WebSocket |
| **TLS** | `stdx.net.tls` | TLS 1.2/1.3 安全传输 |
| **JSON** | `stdx.encoding.json` | JSON 解析、构建与转换 |
| **JSON Stream** | `stdx.encoding.json.stream` | JSON 流式序列化与反序列化 |
| **Base64** | `stdx.encoding.base64` | Base64 编码与解码 |
| **Hex** | `stdx.encoding.hex` | 十六进制编码与解码 |
| **URL** | `stdx.encoding.url` | URL 解析与编解码 |
| **加密** | `stdx.crypto.crypto` | 安全随机数、SM4 对称加密 |
| **摘要** | `stdx.crypto.digest` | MD5/SHA/SM3/HMAC 哈希 |
| **非对称密钥** | `stdx.crypto.keys` | RSA/SM2/ECDSA 非对称加密与签名 |
| **证书** | `stdx.crypto.x509` | X509 数字证书解析与验证 |
| **日志 API** | `stdx.log` | 抽象日志接口 |
| **日志实现** | `stdx.logger` | SimpleLogger/TextLogger/JsonLogger |
| **序列化** | `stdx.serialization` | 序列化/反序列化框架 |
| **压缩** | `stdx.compress.zlib` | zlib/gzip 压缩与解压缩 |
| **AOP** | `stdx.aspectCJ` | 面向切面编程注解 |
| **模糊测试** | `stdx.fuzz` | 覆盖率引导的模糊测试 |
| **测试数据** | `stdx.unittest.data` | 参数化测试数据加载 |

### 1.2 与标准库的区别

- **标准库（std）**：随 SDK 一起发布，开箱即用
- **扩展标准库（stdx）**：需要**单独下载**并配置，不随 SDK 自带

---

## 2. 下载与配置

### 2.1 下载 stdx

**发行版下载页面**：https://gitcode.com/Cangjie/cangjie_stdx/releases

根据操作系统和架构选择对应的发行版（如 `linux_x86_64_cjnative`、`windows_x86_64_cjnative` 等），下载并解压。

解压后目录结构示例：

```text
stdx/
├── dynamic/       # 动态库
│   └── stdx/
└── static/        # 静态库
    └── stdx/
```

### 2.2 配置 cjpm.toml

在仓颉项目的 `cjpm.toml` 文件中添加 `bin-dependencies` 配置：

**步骤 1**：获取系统架构信息

```shell
cjc -v
# 输出示例：
# Cangjie Compiler: 0.60.5 (cjnative)
# Target: x86_64-unknown-linux-gnu
```

**步骤 2**：在 `cjpm.toml` 中添加配置

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = ""

[dependencies]

# Linux x86_64 示例
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]  # 替换为实际 stdx 路径

# Windows x86_64 示例
# [target.x86_64-w64-mingw32]
#   [target.x86_64-w64-mingw32.bin-dependencies]
#     path-option = ["D:\\path\\to\\stdx\\dynamic\\stdx"]

# macOS aarch64 示例
# [target.aarch64-apple-darwin]
#   [target.aarch64-apple-darwin.bin-dependencies]
#     path-option = ["/path/to/stdx/dynamic/stdx"]
```

> **说明**：
> - 动态库和静态库二选一，通过 `path-option` 指向对应目录
> - 使用 crypto 和 net 包的**静态库**时，Linux 需额外添加 `compile-option = "-ldl"`，Windows 需额外添加 `compile-option = "-lcrypt32"`
> - crypto 和 net 模块依赖 OpenSSL 3

### 2.3 导入使用

```cangjie
import stdx.net.http.*           // HTTP 包
import stdx.encoding.json.*     // JSON 包
import stdx.encoding.base64.*   // Base64 包
import stdx.log.*               // 日志 API 包
import stdx.crypto.digest.*     // 摘要算法包
// 等等...
```

---

## 3. HTTP 服务与客户端（stdx.net.http）— 详细介绍

**导入**：`import stdx.net.http.*`

支持 HTTP/1.1、HTTP/2 协议和 WebSocket。

### 3.1 创建 HTTP 服务端

```cangjie
import stdx.net.http.*

main() {
    // 1. 构建 Server
    let server = ServerBuilder()
                    .addr("127.0.0.1")
                    .port(8080)
                    .build()

    // 2. 注册路由处理器
    server.distributor.register("/hello", {httpContext =>
        httpContext.responseBuilder.body("Hello 仓颉!")
    })

    server.distributor.register("/json", {httpContext =>
        httpContext.responseBuilder
            .header("Content-Type", "application/json")
            .body("{\"msg\": \"ok\"}")
    })

    // 3. 启动服务
    server.serve()
}
```

#### ServerBuilder 常用配置

```cangjie
let server = ServerBuilder()
    .addr("0.0.0.0")                    // 监听地址
    .port(8080)                          // 监听端口
    .readTimeout(Duration.second * 30)   // 读超时
    .writeTimeout(Duration.second * 30)  // 写超时
    .maxRequestBodySize(10 * 1024 * 1024) // 最大请求体 10MB
    .build()
```

#### 关闭服务

```cangjie
server.close()              // 立即关闭
server.closeGracefully()    // 优雅关闭（等待进行中的请求完成）
```

### 3.2 创建 HTTP 客户端

```cangjie
import stdx.net.http.*

main() {
    // 1. 构建 Client
    let client = ClientBuilder().build()

    // 2. 发送 GET 请求
    let response = client.get("http://127.0.0.1:8080/hello")
    println(response.status)  // 200

    // 3. 读取响应体
    let body = StringReader(response.body).readToEnd()
    println(body)  // "Hello 仓颉!"

    // 4. 发送 POST 请求
    let postResp = client.post("http://127.0.0.1:8080/api",
                               "{\"name\": \"test\"}")

    // 5. 自定义请求
    let req = HttpRequestBuilder()
        .url("http://127.0.0.1:8080/api")
        .method("PUT")
        .header("Content-Type", "application/json")
        .body("{\"key\": \"value\"}")
        .build()
    let resp = client.send(req)

    client.close()
}
```

#### ClientBuilder 常用配置

```cangjie
let client = ClientBuilder()
    .readTimeout(Duration.second * 10)   // 读超时
    .writeTimeout(Duration.second * 10)  // 写超时
    .autoRedirect(true)                  // 自动跟随重定向
    .cookieJar(CookieJar())             // Cookie 管理
    .httpProxy("http://proxy:3128")      // HTTP 代理
    .build()
```

### 3.3 WebSocket

```cangjie
import stdx.net.http.*

// 客户端 WebSocket 连接
let client = ClientBuilder().build()
let (ws, headers) = WebSocket.upgradeFromClient(
    client,
    URL.parse("ws://127.0.0.1:8080/ws"),
    HTTP1_1,
    ArrayList<String>(),
    HttpHeaders()
)

// 发送文本帧
ws.write(TextWebFrame, "Hello WebSocket".toArray())

// 读取帧
let frame = ws.read()
println(String.fromUtf8(frame.payload))

// 关闭连接
ws.writeCloseFrame(status: 1000)
```

### 3.4 HTTPS（TLS 配置）

```cangjie
import stdx.net.http.*
import stdx.net.tls.*

// 服务端 HTTPS
let server = ServerBuilder()
    .addr("0.0.0.0")
    .port(443)
    .tlsConfig(TlsServerConfig(
        certFilePath: "/path/to/cert.pem",
        keyFilePath: "/path/to/key.pem"
    ))
    .build()

// 客户端 HTTPS
let client = ClientBuilder()
    .tlsConfig(TlsClientConfig(
        caCertFilePath: "/path/to/ca.pem"
    ))
    .build()
```

---

## 4. JSON 编解码（stdx.encoding.json / json.stream）— 详细介绍

### 4.1 JSON 解析与构建（stdx.encoding.json）

**导入**：`import stdx.encoding.json.*`

#### 解析 JSON 字符串

```cangjie
import stdx.encoding.json.*

// 从字符串解析
let jsonStr = """{"name": "Alice", "age": 30, "scores": [90, 85]}"""
let jsonVal = JsonValue.fromStr(jsonStr)

// 访问字段
let obj = jsonVal.asObject()
let name = obj["name"].asString().getValue()     // "Alice"
let age = obj["age"].asInt().getValue()           // 30
let scores = obj["scores"].asArray()
let first = scores[0].asInt().getValue()          // 90
```

#### 构建 JSON

```cangjie
import stdx.encoding.json.*

let obj = JsonObject()
obj.put("name", JsonString("Bob"))
obj.put("age", JsonInt(25))
obj.put("active", JsonBool(true))

let arr = JsonArray()
arr.add(JsonInt(1))
arr.add(JsonInt(2))
obj.put("tags", arr)

// 序列化为字符串
let jsonStr = obj.toJsonString()
// {"name": "Bob", "age": 25, "active": true, "tags": [1, 2]}
```

#### JsonValue 类型体系

| 类型 | 对应 JSON | 获取值方法 |
|------|-----------|------------|
| `JsonObject` | `{...}` | `get(key)`, `operator[]` |
| `JsonArray` | `[...]` | `get(index)`, `operator[]` |
| `JsonString` | `"..."` | `getValue(): String` |
| `JsonInt` | 整数 | `getValue(): Int64` |
| `JsonFloat` | 浮点数 | `getValue(): Float64` |
| `JsonBool` | `true/false` | `getValue(): Bool` |
| `JsonNull` | `null` | — |

#### 类型判断

```cangjie
let val = JsonValue.fromStr(jsonStr)
match (val.kind()) {
    case JsObject => let obj = val.asObject()
    case JsArray => let arr = val.asArray()
    case JsString => let s = val.asString().getValue()
    case JsInt => let i = val.asInt().getValue()
    case JsFloat => let f = val.asFloat().getValue()
    case JsBool => let b = val.asBool().getValue()
    case JsNull => // null
}
```

### 4.2 JSON 流式序列化（stdx.encoding.json.stream）

**导入**：`import stdx.encoding.json.stream.*`

适合将自定义类型与 JSON 进行互转。

#### 序列化（对象 → JSON 流）

```cangjie
import stdx.encoding.json.stream.*
import std.io.*

let output = ByteArrayOutputStream()
let writer = JsonWriter(output)

writer.startObject()
    .writeName("name").writeValue("Alice")
    .writeName("age").writeValue(30)
    .writeName("scores")
    .startArray()
        .writeValue(90).writeValue(85)
    .endArray()
.endObject()
writer.flush()

let jsonStr = String.fromUtf8(output.toByteArray())
// {"name":"Alice","age":30,"scores":[90,85]}
```

#### 反序列化（JSON 流 → 对象）

```cangjie
import stdx.encoding.json.stream.*
import std.io.*

let input = ByteArrayInputStream(jsonStr.toArray())
let reader = JsonReader(input)

reader.startObject()
while (reader.peek() != None) {
    let key = reader.readName()
    match (key) {
        case "name" => let name: String = reader.readValue<String>()
        case "age" => let age: Int64 = reader.readValue<Int64>()
        case _ => reader.skip()
    }
}
reader.endObject()
```

#### 自定义类型序列化

```cangjie
import stdx.encoding.json.stream.*

class Person <: JsonSerializable & JsonDeserializable<Person> {
    var name: String
    var age: Int64

    public func toJson(writer: JsonWriter): Unit {
        writer.startObject()
            .writeName("name").writeValue(name)
            .writeName("age").writeValue(age)
        .endObject()
    }

    public static func fromJson(reader: JsonReader): Person {
        let p = Person()
        reader.startObject()
        while (reader.peek() != None) {
            match (reader.readName()) {
                case "name" => p.name = reader.readValue<String>()
                case "age" => p.age = reader.readValue<Int64>()
                case _ => reader.skip()
            }
        }
        reader.endObject()
        return p
    }
}
```

---

## 5. 编码工具（stdx.encoding）— 详细介绍

### 5.1 Base64（stdx.encoding.base64）

**导入**：`import stdx.encoding.base64.*`

```cangjie
import stdx.encoding.base64.*

// 编码
let encoded = toBase64String([77, 97, 110])  // "TWFu"

// 解码
let decoded = fromBase64String("TWFu")        // [77, 97, 110]

// 常用场景：二进制数据转文本传输
let data = "Hello".toArray()
let b64 = toBase64String(data)
let original = fromBase64String(b64)
```

### 5.2 Hex（stdx.encoding.hex）

**导入**：`import stdx.encoding.hex.*`

```cangjie
import stdx.encoding.hex.*

// 编码
let hexStr = toHexString([65, 66, 94, 97])  // "41425e61"

// 解码
let bytes = fromHexString("41425e61")        // [65, 66, 94, 97]
```

### 5.3 URL（stdx.encoding.url）

**导入**：`import stdx.encoding.url.*`

```cangjie
import stdx.encoding.url.*

// 解析 URL
let url = URL.parse("https://example.com:8080/api/v1?key=value#section")
println(url.scheme)    // "https"
println(url.host)      // "example.com"
println(url.port)      // 8080
println(url.path)      // "/api/v1"
println(url.query)     // "key=value"
println(url.fragment)  // "section"

// URL 表单参数处理
let form = Form()
form.add("name", "张三")
form.add("age", "30")
let encoded = form.toString()  // URL 编码后的参数字符串
```

---

## 6. 加密与安全（stdx.crypto）— 简略介绍

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/crypto/` 目录下的原始文档。

### 6.1 消息摘要（stdx.crypto.digest）

**导入**：`import stdx.crypto.digest.*`

支持算法：MD5、SHA1、SHA224、SHA256、SHA384、SHA512、SM3、HMAC

```cangjie
import stdx.crypto.digest.*

// SHA256 摘要
let sha = SHA256()
sha.update("Hello".toArray())
let hash = sha.finish()  // 返回摘要字节数组

// HMAC
let hmac = HMAC(SHA256(), key)
hmac.update("message".toArray())
let mac = hmac.finish()
```

### 6.2 对称加密（stdx.crypto.crypto）

**导入**：`import stdx.crypto.crypto.*`

- **SM4** 对称加密（中国国密标准）
- **SecureRandom** 安全随机数生成
- 支持 ECB、CBC、CTR 等操作模式

### 6.3 非对称加密与签名（stdx.crypto.keys）

**导入**：`import stdx.crypto.keys.*`

- **RSA**：公钥加密/私钥解密、私钥签名/公钥验签，支持 OAEP 和 PSS 填充
- **SM2**：中国国密非对称加密算法
- **ECDSA**：椭圆曲线数字签名，支持多种曲线（P256、P384、P521 等）

### 6.4 数字证书（stdx.crypto.x509）

**导入**：`import stdx.crypto.x509.*`

- X509 证书解析（PEM/DER 格式）
- 证书验证与证书链构建
- 证书签名请求（CSR）创建
- 自签名证书生成

---

## 7. TLS 安全通信（stdx.net.tls）— 简略介绍

**导入**：`import stdx.net.tls.*`

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/net/tls/` 目录下的原始文档。

- 支持 TLS 1.2 和 TLS 1.3
- `TlsSocket` — 加密套接字通信
- `TlsClientConfig` / `TlsServerConfig` — 客户端/服务端 TLS 配置
- 支持会话恢复（Session Resumption）
- 支持多种证书验证模式和签名算法
- 通常通过 HTTP 模块的 `tlsConfig()` 集成使用（见第 3 节 HTTPS 配置）

---

## 8. 日志（stdx.log + stdx.logger）— 详细介绍

### 8.1 日志 API（stdx.log）

**导入**：`import stdx.log.*`

提供抽象日志接口，不依赖具体实现。

```cangjie
import stdx.log.*

// 获取全局 Logger
let logger = getGlobalLogger()

// 设置全局 Logger
setGlobalLogger(myLogger)

// 日志级别：TRACE < DEBUG < INFO < WARN < ERROR < FATAL < OFF
```

### 8.2 日志实现（stdx.logger）

**导入**：`import stdx.logger.*`

提供三种内置 Logger：

```cangjie
import stdx.log.*
import stdx.logger.*

// 1. SimpleLogger — 简单文本格式
let logger = SimpleLogger("MyApp")
setGlobalLogger(logger)
logger.info("Server started", ("port", 8080))
// 输出：2025-04-15T10:30:00Z INFO Server started port=8080

// 2. TextLogger — 键值对文本格式
let textLogger = TextLogger("MyApp")
textLogger.info("Request received", ("method", "GET"), ("path", "/api"))
// 输出：time=2025-04-15T10:30:00Z level=INFO msg="Request received" method=GET path=/api

// 3. JsonLogger — JSON 格式
let jsonLogger = JsonLogger("MyApp")
jsonLogger.info("Event", ("user", "alice"))
// 输出：{"time":"...","level":"INFO","msg":"Event","user":"alice"}
```

#### 日志方法

```cangjie
logger.trace("详细跟踪信息")
logger.debug("调试信息")
logger.info("一般信息", ("key", "value"))
logger.warn("警告信息")
logger.error("错误信息", ("error", errMsg))
logger.fatal("致命错误")

// 惰性求值（仅在日志级别启用时计算）
logger.trace({=> "expensive computation: ${compute()}"})
```

---

## 9. 序列化（stdx.serialization）— 简略介绍

**导入**：`import stdx.serialization.*`

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/serialization/` 目录下的原始文档。

提供通用序列化框架，通过中间层 `DataModel` 实现对象与各种格式的互转。

### 核心概念

- **`Serializable<T>` 接口** — 自定义类型实现此接口支持序列化
  - `serialize(): DataModel` — 对象 → DataModel
  - `deserialize(DataModel): T` — DataModel → 对象（静态方法）
- **DataModel 类型体系**：`DataModelBool`、`DataModelInt`、`DataModelFloat`、`DataModelString`、`DataModelNull`、`DataModelSeq`（序列）、`DataModelStruct`（结构体）

```cangjie
import stdx.serialization.*

class Person <: Serializable<Person> {
    var name: String
    var age: Int64

    public func serialize(): DataModel {
        DataModelStruct()
            .add(field("name", DataModelString(name)))
            .add(field("age", DataModelInt(age)))
    }

    public static func deserialize(dm: DataModel): Person {
        // 从 DataModel 还原对象
        ...
    }
}
```

---

## 10. 压缩（stdx.compress.zlib）— 简略介绍

**导入**：`import stdx.compress.zlib.*`

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/compress/zlib/` 目录下的原始文档。

支持 deflate-raw 和 gzip 格式。

### 核心类

| 类 | 说明 |
|------|------|
| `CompressInputStream` | 压缩输入流 |
| `CompressOutputStream` | 压缩输出流 |
| `DecompressInputStream` | 解压输入流 |
| `DecompressOutputStream` | 解压输出流 |

### 压缩级别

- `CompressLevel.Fast` — 速度优先
- `CompressLevel.Default` — 默认平衡
- `CompressLevel.High` — 压缩率优先

### 数据格式

- `WrapType.DeflateFormat` — deflate-raw 格式
- `WrapType.GzipFormat` — gzip 格式

```cangjie
import stdx.compress.zlib.*

// 压缩
let compressed = CompressInputStream(inputStream, wrap: GzipFormat)

// 解压
let decompressed = DecompressInputStream(compressedStream, wrap: GzipFormat)
```

---

## 11. 面向切面编程（stdx.aspectCJ）— 简略介绍

**导入**：`import stdx.aspectCJ.*`

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/aspectCJ/` 目录下的原始文档。

通过编译器插件实现 AOP 能力。

### 核心注解

| 注解 | 说明 |
|------|------|
| `@InsertAtEntry` | 在方法入口插入函数调用 |
| `@InsertAtExit` | 在方法出口插入函数调用 |
| `@ReplaceFuncBody` | 替换方法体为指定函数 |

### 使用要求

需要编译器插件支持：
- `libcollect-aspects.so`（收集阶段插件）
- `libwave-aspects.so`（织入阶段插件）

---

## 12. 模糊测试（stdx.fuzz）— 简略介绍

**导入**：`import stdx.fuzz.*`

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/fuzz/` 目录下的原始文档。

提供覆盖率引导的模糊测试引擎。

### 核心类

| 类 | 说明 |
|------|------|
| `Fuzzer` | 模糊测试引擎 |
| `FuzzerBuilder` | 构建器模式配置 Fuzzer |
| `FuzzDataProvider` | 将变异字节转换为标准类型 |
| `DebugDataProvider` | 带调试信息的数据提供者 |

### 平台要求

仅支持 Linux 和 macOS，依赖 LLVM 的 `libclang_rt.fuzzer_no_main.a`。

---

## 13. 测试数据加载（stdx.unittest.data）— 简略介绍

**导入**：`import stdx.unittest.data.*`

> 详细 API 请参阅 `libs/standard-extension/libs_stdx/unittest/data/` 目录下的原始文档。

为参数化测试提供外部数据加载能力。

### 支持格式

| 函数 | 说明 |
|------|------|
| `json<T>()` | 从 JSON 文件加载测试数据 |
| `csv<T>()` | 从 CSV 文件加载测试数据 |
| `tsv<T>()` | 从 TSV 文件加载测试数据 |

---

## 14. 快速上手示例

### 14.1 HTTP 服务 + JSON 响应

```cangjie
import stdx.net.http.*
import stdx.encoding.json.*

main() {
    let server = ServerBuilder()
        .addr("127.0.0.1")
        .port(8080)
        .build()

    server.distributor.register("/api/user", {ctx =>
        let obj = JsonObject()
        obj.put("name", JsonString("Alice"))
        obj.put("age", JsonInt(30))
        ctx.responseBuilder
            .header("Content-Type", "application/json")
            .body(obj.toJsonString())
    })

    server.serve()
}
```

### 14.2 HTTP 客户端请求 + JSON 解析

```cangjie
import stdx.net.http.*
import stdx.encoding.json.*
import std.io.*

main() {
    let client = ClientBuilder().build()
    let resp = client.get("http://127.0.0.1:8080/api/user")
    let body = StringReader(resp.body).readToEnd()
    let json = JsonValue.fromStr(body)
    let name = json.asObject()["name"].asString().getValue()
    println("Name: ${name}")
    client.close()
}
```

### 14.3 日志记录

```cangjie
import stdx.log.*
import stdx.logger.*

main() {
    let logger = SimpleLogger("MyApp")
    setGlobalLogger(logger)
    logger.info("Application started", ("version", "1.0.0"))
    logger.debug("Processing request", ("path", "/api"))
    logger.error("Something went wrong", ("code", 500))
}
```

---

## 15. 注意事项

| 要点 | 说明 |
|------|------|
| **版本兼容性** | stdx 后续版本可能存在不兼容变更，不承诺跨版本 API/ABI 兼容性 |
| **OpenSSL 依赖** | crypto 和 net 模块依赖 OpenSSL 3 库 |
| **平台支持** | 支持 Ubuntu/macOS（x86_64, aarch64），Windows 部分功能受限 |
| **静态库额外配置** | 使用静态库时，Linux 需 `-ldl`，Windows 需 `-lcrypt32` |
| **源码构建** | 如需从源码构建：`git clone https://gitcode.com/Cangjie/cangjie_stdx.git`，然后使用 `python3 build.py` 构建 |
