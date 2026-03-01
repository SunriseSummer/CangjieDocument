---
name: cangjie-stdx
description: "仓颉扩展标准库（stdx）能力查询入口与项目配置指南。当需要了解 stdx 的下载配置与构建运行（含不同平台和静/动态依赖）、或需要快速查询 stdx 各包的接口、类型和函数时，应使用此 Skill。HTTP/JSON/TLS/WebSocket 等核心包的详细用法，请参考对应的细分 Skill。"
---

# 仓颉扩展标准库（stdx）能力查询与项目配置指南

> **定位**：本 Skill 是 stdx 的**能力查询入口**与**项目配置指南**。各核心包（HTTP、JSON、TLS、WebSocket 等）已有独立细分 Skill 提供详细使用指导，本文不重复，仅以表格速查各包的接口、类型和函数。

---

## 1. stdx 项目配置、构建与运行

### 1.1 stdx 与标准库的区别

- **标准库（std）**：随 SDK 一起发布，开箱即用。
- **扩展标准库（stdx）**：需要**单独下载**并配置，不随 SDK 自带。

### 1.2 下载 stdx

**发行版下载页面**：<https://gitcode.com/Cangjie/cangjie_stdx/releases>

根据操作系统和架构选择对应的发行版：

| 平台 | 发行版名称示例 |
|------|----------------|
| Linux x86_64 | `linux_x86_64_cjnative` |
| Linux aarch64 | `linux_aarch64_cjnative` |
| macOS x86_64 | `macos_x86_64_cjnative` |
| macOS aarch64 | `macos_aarch64_cjnative` |
| Windows x86_64 | `windows_x86_64_cjnative` |

下载并解压后，目录结构如下：

```text
stdx/
├── dynamic/       # 动态库（含动态链接文件、cjo、bc 文件）
│   └── stdx/
└── static/        # 静态库（含静态链接文件、cjo、bc 文件）
    └── stdx/
```

动态库和静态库**二选一**使用。

### 1.3 获取系统架构信息

在配置前，先确认编译器目标架构：

```shell
cjc -v
# 输出示例：
# Cangjie Compiler: 0.60.5 (cjnative)
# Target: x86_64-unknown-linux-gnu
```

其中 `Target` 后的字符串（如 `x86_64-unknown-linux-gnu`）即为后续配置所需的架构标识。

### 1.4 使用 cjpm 构建（推荐）

#### 1.4.1 动态库配置

在项目 `cjpm.toml` 中添加 `bin-dependencies` 配置，`path-option` 指向 `dynamic/stdx` 目录：

**Linux x86_64**：

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = ""

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**macOS aarch64**：

```toml
[target.aarch64-apple-darwin]
  [target.aarch64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]
```

**Windows x86_64**：

```toml
[target.x86_64-w64-mingw32]
  [target.x86_64-w64-mingw32.bin-dependencies]
    path-option = ["D:\\path\\to\\stdx\\dynamic\\stdx"]
```

构建与运行：

```shell
cjpm build
cjpm run
```

运行前需设置动态库搜索路径：

| 操作系统 | 环境变量 | 示例 |
|----------|----------|------|
| Linux | `LD_LIBRARY_PATH` | `export LD_LIBRARY_PATH=/path/to/stdx/dynamic/stdx:$LD_LIBRARY_PATH` |
| macOS | `DYLD_LIBRARY_PATH` | `export DYLD_LIBRARY_PATH=/path/to/stdx/dynamic/stdx:$DYLD_LIBRARY_PATH` |
| Windows | `PATH` | 将 stdx 动态库目录添加到 `PATH` 中 |

#### 1.4.2 静态库配置

将 `path-option` 指向 `static/stdx` 目录。使用 crypto 和 net 包的静态库时，由于依赖系统符号，需要额外添加 `compile-option`：

**Linux x86_64（静态库 + crypto/net）**：

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"

[dependencies]

[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

**Windows x86_64（静态库 + crypto/net）**：

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-lcrypt32"

[target.x86_64-w64-mingw32]
  [target.x86_64-w64-mingw32.bin-dependencies]
    path-option = ["D:\\path\\to\\stdx\\static\\stdx"]
```

**macOS aarch64（静态库）**：macOS 下使用静态库无需额外 `compile-option`。

```toml
[package]
  name = "myproject"
  version = "1.0.0"
  output-type = "executable"

[target.aarch64-apple-darwin]
  [target.aarch64-apple-darwin.bin-dependencies]
    path-option = ["/path/to/stdx/static/stdx"]
```

静态库编译的产物无需设置动态库搜索路径，可直接运行：

```shell
cjpm build
cjpm run
```

#### 1.4.3 静态库与动态库选择指南

| 维度 | 动态库 | 静态库 |
|------|--------|--------|
| 产物体积 | 小（运行时加载 .so/.dll/.dylib） | 大（链接进可执行文件） |
| 部署便利性 | 需随产物分发动态库或配置搜索路径 | 单文件部署，无外部依赖 |
| 额外配置 | 运行前设置 `LD_LIBRARY_PATH` 等 | Linux 需 `-ldl`，Windows 需 `-lcrypt32`（仅 crypto/net） |

### 1.5 使用 cjc 直接编译

如果不使用 cjpm，可通过 `cjc` 命令直接编译，需手动指定库路径和链接选项。

**设置 stdx 路径**：

```shell
# Linux / macOS
export CANGJIE_STDX_PATH=/path/to/stdx/dynamic/stdx

# Windows (PowerShell)
$env:CANGJIE_STDX_PATH = "D:\path\to\stdx\dynamic\stdx"
```

**Linux / macOS 编译命令**：

```shell
cjc main.cj -L $CANGJIE_STDX_PATH \
  -lstdx.net.http -lstdx.net.tls -lstdx.logger -lstdx.log \
  -lstdx.encoding.url -lstdx.encoding.json -lstdx.encoding.json.stream \
  -lstdx.encoding.base64 -lstdx.encoding.hex \
  -lstdx.crypto.keys -lstdx.crypto.x509 -lstdx.crypto.crypto -lstdx.crypto.digest \
  -lstdx.serialization.serialization -lstdx.compress.zlib -lstdx.compress \
  -lstdx.aspectCJ \
  -ldl \
  --import-path $CANGJIE_STDX_PATH \
  -o main.out
```

**Windows 编译命令**（将 `-ldl` 替换为 `-lcrypt32`）：

```shell
cjc main.cj -L %CANGJIE_STDX_PATH% ^
  -lstdx.net.http -lstdx.net.tls -lstdx.logger -lstdx.log ^
  -lstdx.encoding.url -lstdx.encoding.json -lstdx.encoding.json.stream ^
  -lstdx.encoding.base64 -lstdx.encoding.hex ^
  -lstdx.crypto.keys -lstdx.crypto.x509 -lstdx.crypto.crypto -lstdx.crypto.digest ^
  -lstdx.serialization.serialization -lstdx.compress.zlib -lstdx.compress ^
  -lstdx.aspectCJ ^
  -lcrypt32 ^
  --import-path %CANGJIE_STDX_PATH% ^
  -o main.exe
```

> **说明**：按需链接使用的包即可，无需全部链接。链接顺序需遵循依赖关系（被依赖的包放在后面）。使用静态库时将路径指向 `static/stdx`。

**运行前设置动态库搜索路径**（使用动态库时）：

```shell
# Linux
export LD_LIBRARY_PATH=$CANGJIE_STDX_PATH:$LD_LIBRARY_PATH
./main.out

# macOS
export DYLD_LIBRARY_PATH=$CANGJIE_STDX_PATH:$DYLD_LIBRARY_PATH
./main.out

# Windows — 将 stdx 路径添加到 PATH
```

### 1.6 包依赖关系

使用 cjc 直接编译时需注意包的依赖关系。使用 cjpm 则无需关注。

| 导入包 | 传递依赖 |
|--------|----------|
| `stdx.aspectCJ` | （无） |
| `stdx.compress.zlib` | （无） |
| `stdx.encoding.base64` | （无） |
| `stdx.encoding.hex` | （无） |
| `stdx.encoding.url` | （无） |
| `stdx.encoding.json` | `stdx.serialization.serialization` |
| `stdx.encoding.json.stream` | （无） |
| `stdx.log` | （无） |
| `stdx.logger` | （无） |
| `stdx.serialization.serialization` | （无） |
| `stdx.fuzz.fuzz` | （无） |
| `stdx.unittest.data` | `stdx.encoding.json`、`stdx.serialization.serialization` |
| `stdx.crypto.digest` | （无） |
| `stdx.crypto.crypto` | `stdx.crypto.digest` |
| `stdx.crypto.x509` | `stdx.encoding.hex`、`stdx.crypto.crypto`、`stdx.crypto.digest`、`stdx.encoding.base64` |
| `stdx.crypto.keys` | `stdx.crypto.x509`、`stdx.encoding.hex`、`stdx.crypto.crypto`、`stdx.crypto.digest`、`stdx.encoding.base64` |
| `stdx.net.tls` | `stdx.crypto.x509`、`stdx.encoding.hex`、`stdx.crypto.crypto`、`stdx.crypto.digest`、`stdx.encoding.base64` |
| `stdx.net.http` | `stdx.net.tls`、`stdx.logger`、`stdx.log`、`stdx.encoding.url`、`stdx.encoding.json.stream`、`stdx.crypto.x509`、`stdx.encoding.hex`、`stdx.crypto.crypto`、`stdx.crypto.digest`、`stdx.encoding.base64` |

### 1.7 OpenSSL 依赖

crypto 和 net 模块依赖 **OpenSSL 3** 库，需确保系统已安装：

| 操作系统 | 安装方式 |
|----------|----------|
| Ubuntu/Debian | `sudo apt install libssl-dev` |
| macOS | `brew install openssl@3` |
| Windows | 下载 OpenSSL 3 安装包并配置 PATH |

### 1.8 从源码构建 stdx

```shell
git clone https://gitcode.com/Cangjie/cangjie_stdx.git
cd cangjie_stdx
source <cangjie sdk 路径>/envsetup.sh    # 配置 Cangjie SDK 环境，如 source /opt/cangjie/envsetup.sh
python3 build.py clean
python3 build.py build -t release --target-lib=<openssl lib 路径>  # 如 --target-lib=/usr/lib/x86_64-linux-gnu
python3 build.py install     # 产物输出到 target 目录
```

### 1.9 导入使用

```cangjie
import stdx.net.http.*           // HTTP 包
import stdx.encoding.json.*     // JSON 包
import stdx.encoding.base64.*   // Base64 包
import stdx.log.*               // 日志 API 包
import stdx.crypto.digest.*     // 摘要算法包
// 按需导入其他包...
```

---

## 2. stdx 包功能总表

| 包名 | 功能 | 导入语句 |
|------|------|----------|
| `stdx.net.http` | HTTP/1.1、HTTP/2 客户端与服务端、WebSocket | `import stdx.net.http.*` |
| `stdx.net.tls` | TLS 1.2/1.3 安全传输 | `import stdx.net.tls.*` |
| `stdx.encoding.json` | JSON 解析、构建与转换 | `import stdx.encoding.json.*` |
| `stdx.encoding.json.stream` | JSON 流式序列化与反序列化 | `import stdx.encoding.json.stream.*` |
| `stdx.encoding.base64` | Base64 编码与解码 | `import stdx.encoding.base64.*` |
| `stdx.encoding.hex` | 十六进制编码与解码 | `import stdx.encoding.hex.*` |
| `stdx.encoding.url` | URL 解析与编解码 | `import stdx.encoding.url.*` |
| `stdx.crypto.crypto` | 安全随机数、SM4 对称加密 | `import stdx.crypto.crypto.*` |
| `stdx.crypto.digest` | MD5/SHA/SM3/HMAC 消息摘要 | `import stdx.crypto.digest.*` |
| `stdx.crypto.keys` | RSA/SM2/ECDSA 非对称加密与签名 | `import stdx.crypto.keys.*` |
| `stdx.crypto.x509` | X509 数字证书解析与验证 | `import stdx.crypto.x509.*` |
| `stdx.log` | 抽象日志接口 | `import stdx.log.*` |
| `stdx.logger` | SimpleLogger/TextLogger/JsonLogger 日志实现 | `import stdx.logger.*` |
| `stdx.serialization.serialization` | 通用序列化/反序列化框架 | `import stdx.serialization.serialization.*` |
| `stdx.compress.zlib` | zlib/gzip 压缩与解压缩 | `import stdx.compress.zlib.*` |
| `stdx.aspectCJ` | 面向切面编程（AOP）注解 | `import stdx.aspectCJ.*` |
| `stdx.fuzz.fuzz` | 覆盖率引导的模糊测试 | `import stdx.fuzz.fuzz.*` |
| `stdx.unittest.data` | 参数化测试数据加载（JSON/CSV/TSV） | `import stdx.unittest.data.*` |

---

## 3. stdx.net.http — HTTP 服务与客户端

> 详细用法请参考 `cangjie-http` / `cangjie-websocket` Skill。

### 3.1 接口

| 接口 | 说明 |
|------|------|
| `HttpRequestHandler` | HTTP 请求处理器 |
| `HttpRequestDistributor` | 请求分发器（路由） |
| `CookieJar` | Cookie 存储管理 |
| `ProtocolServiceFactory` | 协议服务工厂 |

### 3.2 类

| 类 | 构造 / 工厂方法 | 说明 |
|------|----------------|------|
| `ServerBuilder` | `ServerBuilder()` | 服务端构建器，链式调用 `.addr()` `.port()` `.build()` |
| `Server` | 由 `ServerBuilder.build()` 创建 | HTTP 服务端，`.serve()` 启动、`.close()` / `.closeGracefully()` 关闭 |
| `ClientBuilder` | `ClientBuilder()` | 客户端构建器，链式调用 `.readTimeout()` `.build()` |
| `Client` | 由 `ClientBuilder.build()` 创建 | HTTP 客户端，`.get(url)` `.post(url, body)` `.send(req)` |
| `HttpRequestBuilder` | `HttpRequestBuilder()` | 请求构建器，`.url()` `.method()` `.header()` `.body()` `.build()` |
| `HttpRequest` | 由 Builder 或服务端接收 | HTTP 请求对象 |
| `HttpResponseBuilder` | 由 `HttpContext.responseBuilder` 获取 | 响应构建器 |
| `HttpResponse` | 由客户端请求返回 | HTTP 响应对象 |
| `HttpContext` | 由服务端框架提供 | 请求上下文，含 `request` 和 `responseBuilder` |
| `HttpHeaders` | `HttpHeaders()` | HTTP 头部管理 |
| `Cookie` | `Cookie(name: String, value: String)` | Cookie 对象 |
| `WebSocket` | `WebSocket.upgradeFromClient(...)` / `WebSocket.upgradeFromServer(...)` | WebSocket 连接 |
| `WebSocketFrame` | 由 `WebSocket.read()` 返回 | WebSocket 帧 |
| `FuncHandler` | `FuncHandler((HttpContext) -> Unit)` | 函数式请求处理器 |
| `FileHandler` | `FileHandler(String, FileHandlerType)` | 文件上传/下载处理器 |
| `RedirectHandler` | `RedirectHandler(String)` | 重定向处理器 |
| `NotFoundHandler` | `NotFoundHandler()` | 404 处理器 |
| `OptionsHandler` | `OptionsHandler()` | OPTIONS 请求处理器 |
| `HttpResponsePusher` | 由 HTTP/2 服务端提供 | HTTP/2 Server Push |
| `HttpResponseWriter` | 由框架提供 | 流式响应写入 |
| `ProtocolService` | 由框架提供 | 协议服务实例 |

### 3.3 枚举

| 枚举 | 值 | 说明 |
|------|------|------|
| `Protocol` | `HTTP1_1`, `HTTP2` | HTTP 协议版本 |
| `WebSocketFrameType` | `TextWebFrame`, `BinaryWebFrame`, `PingWebFrame`, `PongWebFrame`, `CloseWebFrame` | WebSocket 帧类型 |
| `FileHandlerType` | `Upload`, `Download` | 文件处理类型 |

### 3.4 结构体

| 结构体 | 说明 |
|--------|------|
| `HttpStatusCode` | HTTP 状态码常量（如 `HttpStatusCode.OK`、`HttpStatusCode.NOT_FOUND`） |
| `ServicePoolConfig` | 服务线程池配置 |
| `TransportConfig` | 传输层配置 |

### 3.5 异常

| 异常 | 说明 |
|------|------|
| `HttpException` | HTTP 通用异常 |
| `HttpStatusException` | HTTP 状态码异常 |
| `HttpTimeoutException` | HTTP 超时异常 |
| `ConnectionException` | 连接异常 |
| `WebSocketException` | WebSocket 异常 |
| `CoroutinePoolRejectException` | 协程池拒绝异常 |

### 3.6 函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `upgrade` | `upgrade(...)` | WebSocket 升级辅助 |
| `notFound` | `notFound(...)` | 返回 404 响应 |
| `handleError` | `handleError(...)` | 错误处理辅助 |

---

## 4. stdx.net.tls — TLS 安全传输

> 详细用法请参考 `cangjie-tls` Skill。

### 4.1 类

| 类 | 工厂方法 | 说明 |
|------|----------|------|
| `TlsSocket` | `TlsSocket.client(socket, session?, clientConfig?)` / `TlsSocket.server(socket, sessionContext?, serverConfig)` | 加密套接字通信 |
| `TlsSessionContext` | `TlsSessionContext.fromName(name: String)` | 服务端会话恢复上下文 |

### 4.2 枚举

| 枚举 | 值 | 说明 |
|------|------|------|
| `TlsVersion` | `TLS12`, `TLS13` | TLS 版本 |
| `CertificateVerifyMode` | `Default`, `NoVerify`, `CustomVerify` 等 | 证书验证模式 |
| `SignatureAlgorithm` | RSA/ECDSA/SM2 等 | 签名算法 |
| `SignatureType` | 具体签名类型 | 签名类型 |
| `SignatureSchemeType` | 签名方案类型 | 签名方案 |
| `TlsClientIdentificationMode` | 客户端认证模式 | 是否要求客户端证书 |

### 4.3 结构体

| 结构体 | 构造方式 | 说明 |
|--------|----------|------|
| `TlsClientConfig` | `TlsClientConfig(...)` | 客户端 TLS 配置（CA 证书、验证模式等） |
| `TlsServerConfig` | `TlsServerConfig(...)` | 服务端 TLS 配置（证书、私钥等） |
| `CipherSuite` | — | 密码套件 |
| `TlsSession` | — | TLS 会话信息（用于会话恢复） |

### 4.4 异常

| 异常 | 说明 |
|------|------|
| `TlsException` | TLS 通信异常 |

---

## 5. stdx.encoding.json — JSON 解析与构建

> 详细用法请参考 `cangjie-json` Skill。

### 5.1 接口

| 接口 | 说明 |
|------|------|
| `ToJson` | JsonValue 与 DataModel 之间的互转 |

### 5.2 类

| 类 | 构造函数 | 说明 |
|------|----------|------|
| `JsonValue` | `JsonValue.fromStr(s: String): JsonValue` | JSON 值基类，从字符串解析 |
| `JsonObject` | `JsonObject()` / `JsonObject(map: HashMap<String, JsonValue>)` | JSON 对象，`.put(key, val)` `.get(key)` `operator[]` |
| `JsonArray` | `JsonArray()` / `JsonArray(list: ArrayList<JsonValue>)` / `JsonArray(list: Array<JsonValue>)` | JSON 数组，`.add(val)` `.get(idx)` `operator[]` |
| `JsonString` | `JsonString(value: String)` | JSON 字符串，`.getValue(): String` |
| `JsonInt` | `JsonInt(value: Int64)` | JSON 整数，`.getValue(): Int64` |
| `JsonFloat` | `JsonFloat(value: Float64)` | JSON 浮点数，`.getValue(): Float64` |
| `JsonBool` | `JsonBool(value: Bool)` | JSON 布尔值，`.getValue(): Bool` |
| `JsonNull` | `JsonNull()` | JSON null |

### 5.3 枚举

| 枚举 | 值 | 说明 |
|------|------|------|
| `JsonKind` | `JsObject`, `JsArray`, `JsString`, `JsInt`, `JsFloat`, `JsBool`, `JsNull` | JSON 值类型标识，通过 `.kind()` 获取 |

### 5.4 异常

| 异常 | 说明 |
|------|------|
| `JsonException` | JSON 解析/操作异常 |

---

## 6. stdx.encoding.json.stream — JSON 流式序列化

> 详细用法请参考 `cangjie-json` Skill。

### 6.1 接口

| 接口 | 关键方法 | 说明 |
|------|----------|------|
| `JsonSerializable` | `toJson(writer: JsonWriter): Unit` | 对象 → JSON 流 |
| `JsonDeserializable<T>` | `static fromJson(reader: JsonReader): T` | JSON 流 → 对象 |

### 6.2 类

| 类 | 构造函数 | 关键方法 | 说明 |
|------|----------|----------|------|
| `JsonWriter` | `JsonWriter(out: OutputStream)` | `.startObject()` `.endObject()` `.startArray()` `.endArray()` `.writeName(String)` `.writeValue(...)` `.flush()` | JSON 流式写入 |
| `JsonReader` | `JsonReader(inputStream: InputStream)` | `.startObject()` `.endObject()` `.startArray()` `.endArray()` `.readName()` `.readValue<T>()` `.peek()` `.skip()` | JSON 流式读取 |

### 6.3 枚举

| 枚举 | 值 | 说明 |
|------|------|------|
| `JsonToken` | `BeginArray`, `EndArray`, `BeginObject`, `EndObject`, `Name`, `Value`, `None` | JSON 流 Token 类型 |

### 6.4 结构体

| 结构体 | 说明 |
|--------|------|
| `WriteConfig` | 序列化格式控制（紧凑 / 美化），`WriteConfig.compact` / `WriteConfig.pretty` |

---

## 7. stdx.encoding.base64 — Base64 编解码

### 函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `toBase64String` | `toBase64String(data: Array<Byte>): String` | 字节数组 → Base64 字符串 |
| `fromBase64String` | `fromBase64String(str: String): Array<Byte>` | Base64 字符串 → 字节数组 |

---

## 8. stdx.encoding.hex — 十六进制编解码

### 函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `toHexString` | `toHexString(data: Array<Byte>): String` | 字节数组 → 十六进制字符串 |
| `fromHexString` | `fromHexString(str: String): Array<Byte>` | 十六进制字符串 → 字节数组 |

---

## 9. stdx.encoding.url — URL 处理

### 9.1 类

| 类 | 构造函数 | 关键属性/方法 | 说明 |
|------|----------|--------------|------|
| `URL` | `URL(scheme!: String, hostName!: String, path!: String)` / `URL.parse(rawUrl: String): URL` | `.scheme` `.host` `.port` `.path` `.query` `.fragment` `.userInfo` | URL 解析与构建 |
| `Form` | `Form()` / `Form(queryComponent: String)` | `.add(key, value)` `.get(key)` `.toString()` | URL 表单参数处理 |
| `UserInfo` | `UserInfo()` / `UserInfo(userName: String)` / `UserInfo(userName: String, passWord: String)` | `.userName` `.passWord` | URL 用户信息 |

### 9.2 异常

| 异常 | 说明 |
|------|------|
| `UrlSyntaxException` | URL 格式错误 |

---

## 10. stdx.crypto.digest — 消息摘要

### 10.1 类

| 类 | 构造函数 | 通用方法 | 说明 |
|------|----------|----------|------|
| `MD5` | `MD5()` | `update(Array<Byte>)` `finish(): Array<Byte>` `reset()` | MD5 摘要 |
| `SHA1` | `SHA1()` | 同上 | SHA-1 摘要 |
| `SHA224` | `SHA224()` | 同上 | SHA-224 摘要 |
| `SHA256` | `SHA256()` | 同上 | SHA-256 摘要 |
| `SHA384` | `SHA384()` | 同上 | SHA-384 摘要 |
| `SHA512` | `SHA512()` | 同上 | SHA-512 摘要 |
| `SM3` | `SM3()` | 同上 | 国密 SM3 摘要 |
| `HMAC` | `HMAC(key: Array<Byte>, digest: () -> Digest)` / `HMAC(key: Array<Byte>, algorithm: HashType)` | 同上 | HMAC 消息认证码 |

### 10.2 结构体

| 结构体 | 说明 |
|--------|------|
| `HashType` | 哈希算法类型标识（`HashType.MD5` / `HashType.SHA256` 等） |

### 10.3 异常

| 异常 | 说明 |
|------|------|
| `CryptoException` | 加密操作异常 |

---

## 11. stdx.crypto.crypto — 对称加密与安全随机数

### 11.1 类

| 类 | 构造函数 | 关键方法 | 说明 |
|------|----------|----------|------|
| `SM4` | `SM4(optMode: OperationMode, key: Array<Byte>, iv!: Array<Byte>, paddingMode!: PaddingMode, aad!: Array<Byte>, tagSize!: Int64)` | `.encrypt(Array<Byte>): Array<Byte>` `.decrypt(Array<Byte>): Array<Byte>` | SM4 对称加密 |
| `SecureRandom` | `SecureRandom(priv!: Bool = false)` | `.nextBytes(Array<Byte>)` `.nextUInt64()` | 安全随机数生成 |

### 11.2 结构体

| 结构体 | 说明 |
|--------|------|
| `OperationMode` | 操作模式（`OperationMode.ECB` / `.CBC` / `.CTR` / `.GCM` 等） |
| `PaddingMode` | 填充模式（`PaddingMode.PKCS7Padding` / `.NoPadding`） |

### 11.3 异常

| 异常 | 说明 |
|------|------|
| `SecureRandomException` | 安全随机数异常 |

---

## 12. stdx.crypto.keys — 非对称加密与签名

### 12.1 类

| 类 | 构造函数 | 关键方法 | 说明 |
|------|----------|----------|------|
| `RSAPrivateKey` | `RSAPrivateKey(bits: Int32)` / `RSAPrivateKey(bits: Int32, e: BigInt)` | `.decrypt(...)` `.sign(...)` `.encodeToPem()` | RSA 私钥 |
| `RSAPublicKey` | `RSAPublicKey(pri: RSAPrivateKey)` | `.encrypt(...)` `.verify(...)` `.encodeToPem()` | RSA 公钥 |
| `SM2PrivateKey` | `SM2PrivateKey()` | `.decrypt(...)` `.sign(...)` | SM2 私钥 |
| `SM2PublicKey` | `SM2PublicKey(pri: SM2PrivateKey)` | `.encrypt(...)` `.verify(...)` | SM2 公钥 |
| `ECDSAPrivateKey` | `ECDSAPrivateKey(curve: Curve)` | `.sign(...)` `.encodeToPem()` | ECDSA 私钥 |
| `ECDSAPublicKey` | `ECDSAPublicKey(pri: ECDSAPrivateKey)` | `.verify(...)` `.encodeToPem()` | ECDSA 公钥 |

### 12.2 枚举

| 枚举 | 值 | 说明 |
|------|------|------|
| `Curve` | `P224`, `P256`, `P384`, `P521` 等 | 椭圆曲线类型 |
| `PadOption` | `OAEP`, `PKCS1` 等 | RSA 填充选项 |

### 12.3 结构体

| 结构体 | 说明 |
|--------|------|
| `OAEPOption` | OAEP 填充配置 |
| `PSSOption` | PSS 签名配置 |

---

## 13. stdx.crypto.x509 — 数字证书

### 13.1 接口

| 接口 | 说明 |
|------|------|
| `Key` | 密钥基接口 |
| `PrivateKey` | 私钥接口 |
| `PublicKey` | 公钥接口 |
| `DHParameters` | DH 参数接口 |

### 13.2 类

| 类 | 构造函数 | 关键方法 | 说明 |
|------|----------|----------|------|
| `X509Certificate` | `X509Certificate(certificateInfo, parent?, publicKey?, privateKey?, signatureAlgorithm?)` / `X509Certificate.decodeFromPem(pem)` / `X509Certificate.decodeFromDer(der)` | `.verify()` `.subject` `.issuer` `.serialNumber` `.notBefore` `.notAfter` | X509 证书 |
| `X509CertificateRequest` | — | `.subject` `.publicKey` `.verify()` | 证书签名请求（CSR） |
| `X509Name` | — | `.commonName` `.organization` `.country` | 证书主体/颁发者名称 |

### 13.3 枚举

| 枚举 | 说明 |
|------|------|
| `PublicKeyAlgorithm` | 公钥算法（RSA / ECDSA / SM2 等） |
| `SignatureAlgorithm` | 签名算法 |

### 13.4 结构体

| 结构体 | 说明 |
|--------|------|
| `DerBlob` | DER 编码数据 |
| `Pem` | PEM 编码数据 |
| `PemEntry` | PEM 条目 |
| `KeyUsage` | 密钥用途 |
| `ExtKeyUsage` | 扩展密钥用途 |
| `SerialNumber` | 证书序列号 |
| `Signature` | 签名数据 |
| `VerifyOption` | 证书验证选项 |
| `X509CertificateInfo` | 证书创建信息 |
| `X509CertificateRequestInfo` | CSR 创建信息 |

### 13.5 异常

| 异常 | 说明 |
|------|------|
| `X509Exception` | 证书操作异常 |

---

## 14. stdx.log — 日志 API

### 14.1 函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `getGlobalLogger` | `getGlobalLogger(attrs: Array<Attr>): Logger` | 获取全局 Logger |
| `setGlobalLogger` | `setGlobalLogger(logger: Logger): Unit` | 设置全局 Logger |

### 14.2 接口

| 接口 | 关键方法 | 说明 |
|------|----------|------|
| `LogValue` | 序列化到日志输出 | 日志值类型接口 |

### 14.3 类

| 类 | 构造函数 | 关键方法 | 说明 |
|------|----------|----------|------|
| `Logger`（抽象） | — | `.trace(...)` `.debug(...)` `.info(...)` `.warn(...)` `.error(...)` `.fatal(...)` `.level` | 抽象日志基类 |
| `LogRecord` | — | `.message` `.level` `.attrs` | 日志记录 |
| `LogWriter` | — | 序列化日志到目标 | 日志写入器 |
| `NoopLogger` | `NoopLogger()` | 所有方法空实现 | 空日志实现 |

### 14.4 结构体

| 结构体 | 常量 | 说明 |
|--------|------|------|
| `LogLevel` | `TRACE` < `DEBUG` < `INFO` < `WARN` < `ERROR` < `FATAL` < `OFF` | 日志级别 |

### 14.5 类型别名

| 别名 | 定义 | 说明 |
|------|------|------|
| `Attr` | `(String, LogValue)` | 日志属性键值对 |

### 14.6 异常

| 异常 | 说明 |
|------|------|
| `LogException` | 日志操作异常 |

---

## 15. stdx.logger — 日志实现

### 类

| 类 | 构造函数 | 输出格式 | 说明 |
|------|----------|----------|------|
| `SimpleLogger` | `SimpleLogger(output: OutputStream)` | `2025-04-15T10:30:00Z INFO msg key=value` | 简单文本格式 |
| `TextLogger` | `TextLogger(output: OutputStream)` | `time=... level=INFO msg="..." key=value` | 键值对文本格式 |
| `JsonLogger` | `JsonLogger(output: OutputStream)` | `{"time":"...","level":"INFO","msg":"..."}` | JSON 格式 |

---

## 16. stdx.serialization.serialization — 序列化框架

### 16.1 接口

| 接口 | 关键方法 | 说明 |
|------|----------|------|
| `Serializable<T>` | `serialize(): DataModel` / `static deserialize(DataModel): T` | 序列化/反序列化接口 |

### 16.2 类

| 类 | 构造函数 | 说明 |
|------|----------|------|
| `DataModel`（抽象） | — | 中间数据模型基类 |
| `DataModelBool` | `DataModelBool(bv: Bool)` | 布尔值 |
| `DataModelInt` | `DataModelInt(iv: Int64)` | 整数值 |
| `DataModelFloat` | `DataModelFloat(fv: Float64)` / `DataModelFloat(v: Int64)` | 浮点值 |
| `DataModelString` | `DataModelString(sv: String)` | 字符串值 |
| `DataModelNull` | `DataModelNull()` | 空值 |
| `DataModelSeq` | `DataModelSeq()` / `DataModelSeq(list: ArrayList<DataModel>)` | 序列（数组） |
| `DataModelStruct` | `DataModelStruct()` / `DataModelStruct(list: ArrayList<Field>)` | 结构体（键值映射） |
| `Field` | `Field(name: String, data: DataModel)` | 结构体字段 |

### 16.3 函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `field` | `field<T>(name: String, data: T): Field` | 创建 Field 的辅助函数 |

### 16.4 异常

| 异常 | 说明 |
|------|------|
| `DataModelException` | 数据模型操作异常 |

---

## 17. stdx.compress.zlib — 压缩与解压缩

### 17.1 类

| 类 | 构造函数 | 实现接口 | 说明 |
|------|----------|----------|------|
| `CompressInputStream` | `CompressInputStream(inputStream: InputStream, wrap!: WrapType = DeflateFormat, compressLevel!: CompressLevel = DefaultCompression, bufLen!: Int64 = 512)` | `InputStream` | 压缩输入流 |
| `CompressOutputStream` | `CompressOutputStream(outputStream: OutputStream, wrap!: WrapType = DeflateFormat, compressLevel!: CompressLevel = DefaultCompression, bufLen!: Int64 = 512)` | `OutputStream` | 压缩输出流 |
| `DecompressInputStream` | `DecompressInputStream(inputStream: InputStream, wrap!: WrapType = DeflateFormat, bufLen!: Int64 = 512)` | `InputStream` | 解压输入流 |
| `DecompressOutputStream` | `DecompressOutputStream(outputStream: OutputStream, wrap!: WrapType = DeflateFormat, bufLen!: Int64 = 512)` | `OutputStream` | 解压输出流 |

### 17.2 枚举

| 枚举 | 值 | 说明 |
|------|------|------|
| `CompressLevel` | `DefaultCompression`, 其他级别 | 压缩级别 |
| `WrapType` | `DeflateFormat`（deflate-raw）, `GzipFormat`（gzip） | 数据格式 |

### 17.3 异常

| 异常 | 说明 |
|------|------|
| `ZlibException` | 压缩/解压异常 |

---

## 18. stdx.aspectCJ — 面向切面编程

### 类（注解）

| 注解类 | 说明 |
|--------|------|
| `InsertAtEntry` | 在方法入口插入函数调用 |
| `InsertAtExit` | 在方法出口插入函数调用 |
| `ReplaceFuncBody` | 替换方法体为指定函数 |

> 需要编译器插件 `libcollect-aspects.so`（收集阶段）和 `libwave-aspects.so`（织入阶段）。

---

## 19. stdx.fuzz.fuzz — 模糊测试

### 19.1 类

| 类 | 构造函数 | 关键方法 | 说明 |
|------|----------|----------|------|
| `FuzzerBuilder` | `FuzzerBuilder()` | `.build(): Fuzzer` | 构建器模式配置 Fuzzer |
| `Fuzzer` | 由 `FuzzerBuilder.build()` 创建 | `.startFuzz(...)` | 模糊测试引擎 |
| `FuzzDataProvider` | — | `.consumeInt64()` `.consumeString()` `.consumeBool()` `.consumeBytes(Int64)` | 将变异字节转换为标准类型 |
| `DebugDataProvider` | — | 继承 FuzzDataProvider 的所有方法 | 带调试信息的数据提供者 |

### 19.2 异常

| 异常 | 说明 |
|------|------|
| `ExhaustedException` | 数据不足以完成类型转换 |

> 仅支持 Linux 和 macOS，依赖 LLVM `libclang_rt.fuzzer_no_main.a`。

---

## 20. stdx.unittest.data — 参数化测试数据

### 20.1 函数

| 函数 | 原型 | 说明 |
|------|------|------|
| `json<T>` | `json<T>(filePath: String): SerializableProvider<T> where T: Serializable` | 从 JSON 文件加载测试数据 |
| `csv<T>` | `csv<T>(filePath: String, delimiter!: Rune, quote!: Rune, escape!: Rune, commentChar!: Option<Rune>, headers!: Option<Array<String>>, includeRows!: Array<UInt64>, excludeRows!: Array<UInt64>, hasHeader!: Bool): SerializableProvider<T> where T: Serializable` | 从 CSV 文件加载测试数据 |
| `tsv<T>` | `tsv<T>(filePath: String, quote!: Rune, escape!: Rune, commentChar!: Option<Rune>, headers!: Option<Array<String>>, includeRows!: Array<UInt64>, excludeRows!: Array<UInt64>, hasHeader!: Bool): SerializableProvider<T> where T: Serializable` | 从 TSV 文件加载测试数据 |

### 20.2 类

| 类 | 说明 |
|------|------|
| `SerializableProvider<T>` | DataProvider 接口实现，提供测试数据迭代 |
| `JsonStrategy` | JSON 格式序列化策略 |
| `CsvStrategy` | CSV 格式序列化策略 |

---

## 21. 注意事项

| 要点 | 说明 |
|------|------|
| **版本兼容性** | stdx 后续版本可能存在不兼容变更，不承诺跨版本 API/ABI 兼容性 |
| **OpenSSL 依赖** | crypto 和 net 模块依赖 OpenSSL 3 库 |
| **平台支持** | 支持 Ubuntu/macOS（x86_64, aarch64），Windows 部分功能受限 |
| **静态库额外配置** | 使用 crypto/net 静态库时，Linux 需 `-ldl`，Windows 需 `-lcrypt32` |
| **动态库搜索路径** | 使用动态库时运行前需设置 `LD_LIBRARY_PATH`（Linux）/ `DYLD_LIBRARY_PATH`（macOS）/ `PATH`（Windows） |
| **模糊测试平台** | `stdx.fuzz` 仅支持 Linux 和 macOS |
