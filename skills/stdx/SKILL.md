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

根据操作系统和架构选择对应的发行版，下载并解压。解压后包含 `dynamic/stdx/`（动态库）和 `static/stdx/`（静态库）两个目录。

### 2.2 配置 cjpm.toml

在仓颉项目的 `cjpm.toml` 文件中添加 `bin-dependencies` 配置。先运行 `cjc -v` 获取系统架构信息（如 `x86_64-unknown-linux-gnu`），然后添加：

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
# 根据 cjc -v 输出的 Target 选择对应的 target 段
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]  # 替换为实际 stdx 路径
# Windows 使用 x86_64-w64-mingw32，macOS 使用 aarch64-apple-darwin
```

> **说明**：
> - 动态库和静态库二选一，通过 `path-option` 指向对应目录
> - 使用 crypto 和 net 包的**静态库**时，Linux 需额外添加 `compile-option = "-ldl"`，Windows 需额外添加 `compile-option = "-lcrypt32"`
> - crypto 和 net 模块依赖 OpenSSL 3

### 2.3 导入使用

```cangjie
import stdx.net.http.*        // HTTP
import stdx.encoding.json.*   // JSON
import stdx.log.*             // 日志
// 其他包类似：stdx.encoding.base64.*, stdx.crypto.digest.* 等
```

---

## 3. HTTP 服务与客户端（stdx.net.http）— 详细介绍

**导入**：`import stdx.net.http.*`

支持 HTTP/1.1、HTTP/2 协议和 WebSocket。

### 3.1 创建 HTTP 服务端

```cangjie
import stdx.net.http.*
main() {
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()
    server.distributor.register("/hello", {httpContext =>
        httpContext.responseBuilder.body("Hello 仓颉!")
    })
    server.serve()
}
```

ServerBuilder 还支持 `readTimeout`、`writeTimeout`、`maxRequestBodySize` 等配置。关闭服务使用 `server.close()` 或 `server.closeGracefully()`（优雅关闭）。

### 3.2 创建 HTTP 客户端

```cangjie
import stdx.net.http.*
main() {
    let client = ClientBuilder().build()
    let response = client.get("http://127.0.0.1:8080/hello")
    let body = StringReader(response.body).readToEnd()
    let postResp = client.post("http://127.0.0.1:8080/api", "{\"name\": \"test\"}")
    // 自定义请求（PUT/DELETE 等）使用 HttpRequestBuilder
    let req = HttpRequestBuilder()
        .url("http://127.0.0.1:8080/api").method("PUT")
        .header("Content-Type", "application/json")
        .body("{\"key\": \"value\"}").build()
    let resp = client.send(req)
    client.close()
}
```

ClientBuilder 还支持 `readTimeout`、`writeTimeout`、`autoRedirect`、`cookieJar`、`httpProxy` 等配置选项。

### 3.3 WebSocket

```cangjie
import stdx.net.http.*

let client = ClientBuilder().build()
let (ws, headers) = WebSocket.upgradeFromClient(
    client, URL.parse("ws://127.0.0.1:8080/ws"),
    HTTP1_1, ArrayList<String>(), HttpHeaders()
)
ws.write(TextWebFrame, "Hello WebSocket".toArray())  // 发送
let frame = ws.read()                                 // 接收
ws.writeCloseFrame(status: 1000)                      // 关闭
```

### 3.4 HTTPS（TLS 配置）

```cangjie
import stdx.net.http.*
import stdx.net.tls.*

// 服务端 HTTPS — 通过 tlsConfig 配置证书
let server = ServerBuilder().addr("0.0.0.0").port(443)
    .tlsConfig(TlsServerConfig(certFilePath: "/path/to/cert.pem", keyFilePath: "/path/to/key.pem"))
    .build()

// 客户端 HTTPS — 配置 CA 证书
let client = ClientBuilder()
    .tlsConfig(TlsClientConfig(caCertFilePath: "/path/to/ca.pem"))
    .build()
```

---

## 4. JSON 编解码（stdx.encoding.json / json.stream）— 详细介绍

### 4.1 JSON 解析与构建（stdx.encoding.json）

**导入**：`import stdx.encoding.json.*`

#### 解析 JSON 字符串

```cangjie
import stdx.encoding.json.*
let jsonStr = """{"name": "Alice", "age": 30, "scores": [90, 85]}"""
let obj = JsonValue.fromStr(jsonStr).asObject()
let name = obj["name"].asString().getValue()     // "Alice"
let age = obj["age"].asInt().getValue()           // 30
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
obj.put("tags", arr)
let jsonStr = obj.toJsonString()  // {"name":"Bob","age":25,"active":true,"tags":[1]}
```

#### JsonValue 类型体系

类型：`JsonObject`（`{...}`）、`JsonArray`（`[...]`）、`JsonString`、`JsonInt`、`JsonFloat`、`JsonBool`、`JsonNull`。各类型通过 `getValue()` 获取原始值，通过 `get(key)`/`operator[]` 访问子元素。

通过 `val.kind()` 判断类型（`JsObject`、`JsArray`、`JsString`、`JsInt`、`JsFloat`、`JsBool`、`JsNull`），然后用 `match` 进行分支处理，调用对应的 `asObject()`、`asArray()` 等方法转换。

### 4.2 JSON 流式序列化（stdx.encoding.json.stream）

**导入**：`import stdx.encoding.json.stream.*`

适合将自定义类型与 JSON 进行互转。

#### 序列化（JsonWriter：对象 → JSON 流）

```cangjie
import stdx.encoding.json.stream.*
import std.io.*
let output = ByteArrayOutputStream()
let writer = JsonWriter(output)
writer.startObject()
    .writeName("name").writeValue("Alice")
    .writeName("age").writeValue(30)
    .writeName("scores").startArray().writeValue(90).writeValue(85).endArray()
.endObject()
writer.flush()
// 结果：{"name":"Alice","age":30,"scores":[90,85]}
```

#### 反序列化（JsonReader：JSON 流 → 对象）

```cangjie
let input = ByteArrayInputStream(jsonStr.toArray())
let reader = JsonReader(input)
reader.startObject()
while (reader.peek() != None) {
    match (reader.readName()) {
        case "name" => let name: String = reader.readValue<String>()
        case "age" => let age: Int64 = reader.readValue<Int64>()
        case _ => reader.skip()
    }
}
reader.endObject()
```

自定义类型可通过实现 `JsonSerializable` 和 `JsonDeserializable<T>` 接口支持序列化，在 `toJson(writer)` 和 `fromJson(reader)` 方法中使用上述 `JsonWriter`/`JsonReader` API 进行读写。

---

## 5. 编码工具（stdx.encoding）— 详细介绍

### 5.1 Base64（stdx.encoding.base64）

**导入**：`import stdx.encoding.base64.*`

```cangjie
import stdx.encoding.base64.*
let encoded = toBase64String("Hello".toArray())  // 编码为 Base64 字符串
let decoded = fromBase64String(encoded)           // 解码回字节数组
```

### 5.2 Hex（stdx.encoding.hex）

**导入**：`import stdx.encoding.hex.*`

```cangjie
import stdx.encoding.hex.*
let hexStr = toHexString([65, 66, 94, 97])  // "41425e61"
let bytes = fromHexString("41425e61")        // [65, 66, 94, 97]
```

### 5.3 URL（stdx.encoding.url）

**导入**：`import stdx.encoding.url.*`

```cangjie
import stdx.encoding.url.*
let url = URL.parse("https://example.com:8080/api/v1?key=value#section")
// 可访问 url.scheme、url.host、url.port、url.path、url.query、url.fragment
let form = Form()
form.add("name", "张三")
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
let sha = SHA256()
sha.update("Hello".toArray())
let hash = sha.finish()               // SHA256 摘要
let hmac = HMAC(SHA256(), key)
hmac.update("message".toArray())
let mac = hmac.finish()               // HMAC 摘要
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

提供抽象日志接口。通过 `getGlobalLogger()` / `setGlobalLogger(myLogger)` 管理全局 Logger。日志级别：TRACE < DEBUG < INFO < WARN < ERROR < FATAL < OFF。

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

所有 Logger 支持 `trace`、`debug`、`info`、`warn`、`error`、`fatal` 方法，可附带键值对属性。支持惰性求值：`logger.trace({=> "expensive: ${compute()}"})`.

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
        DataModelStruct().add(field("name", DataModelString(name))).add(field("age", DataModelInt(age)))
    }
    public static func deserialize(dm: DataModel): Person { /* 从 DataModel 还原对象 */ }
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

### 压缩级别与格式

- 压缩级别：`CompressLevel.Fast`（速度优先）、`Default`（默认）、`High`（压缩率优先）
- 数据格式：`WrapType.DeflateFormat`（deflate-raw）、`WrapType.GzipFormat`（gzip）

```cangjie
import stdx.compress.zlib.*

let compressed = CompressInputStream(inputStream, wrap: GzipFormat)     // 压缩
let decompressed = DecompressInputStream(compressedStream, wrap: GzipFormat)  // 解压
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

## 14. 注意事项

| 要点 | 说明 |
|------|------|
| **版本兼容性** | stdx 后续版本可能存在不兼容变更，不承诺跨版本 API/ABI 兼容性 |
| **OpenSSL 依赖** | crypto 和 net 模块依赖 OpenSSL 3 库 |
| **平台支持** | 支持 Ubuntu/macOS（x86_64, aarch64），Windows 部分功能受限 |
| **静态库额外配置** | 使用静态库时，Linux 需 `-ldl`，Windows 需 `-lcrypt32` |
| **源码构建** | 如需从源码构建：`git clone https://gitcode.com/Cangjie/cangjie_stdx.git`，然后使用 `python3 build.py` 构建 |
