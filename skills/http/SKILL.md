---
name: cangjie-http
description: "仓颉语言 HTTP 编程。当需要了解仓颉语言的HTTP服务端(ServerBuilder)、HTTP客户端(ClientBuilder)、请求与响应处理、Cookie管理、分块传输、HTTPS/TLS配置、HTTP/2等特性时，应使用此 Skill。"
---

# 仓颉语言 HTTP 编程 Skill

## 1. 概述

- 依赖包 `stdx.net.http`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 支持 HTTP/1.0、1.1、2.0（RFC 9110/9112/9113/9218/7541）
- HTTP/2 需 TLS + ALPN `h2` 配置
- 依赖 OpenSSL 3（libssl + libcrypto），使用前需安装

---

## 2. 服务端

### 2.1 基本用法

```cangjie
import stdx.net.http.*

main() {
    let server: Server = ServerBuilder().addr("127.0.0.1").port(8080).build()

    // 注册请求处理器
    server.distributor.register("/hello", {
        ctx => ctx.responseBuilder.body("Hello 仓颉!")
    })

    // 多路径注册
    server.distributor.register("/json", {
        ctx =>
        ctx.responseBuilder
            .header("Content-Type", "application/json")
            .body("{\"msg\": \"ok\"}")
    })

    server.serve()  // 阻塞运行
}
```

### 2.2 ServerBuilder 配置接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `addr` | `addr(String): ServerBuilder` | 监听地址 |
| `port` | `port(UInt16): ServerBuilder` | 监听端口（0 表示随机端口） |
| `tlsConfig` | `tlsConfig(TlsServerConfig): ServerBuilder` | TLS 配置（启用 HTTPS） |
| `distributor` | `distributor(HttpRequestDistributor): ServerBuilder` | 自定义请求分发器 |
| `readTimeout` | `readTimeout(Duration): ServerBuilder` | 读超时 |
| `writeTimeout` | `writeTimeout(Duration): ServerBuilder` | 写超时 |
| `readHeaderTimeout` | `readHeaderTimeout(Duration): ServerBuilder` | 读取请求头超时 |
| `httpKeepAliveTimeout` | `httpKeepAliveTimeout(Duration): ServerBuilder` | Keep-Alive 超时 |
| `logger` | `logger(Logger): ServerBuilder` | 自定义日志 |
| `build` | `build(): Server` | 构建 Server 实例 |

### 2.3 Server 接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `serve` | `serve(): Unit` | 阻塞运行服务 |
| `close` | `close(): Unit` | 立即关闭 |
| `closeGracefully` | `closeGracefully(): Unit` | 优雅关闭（等待进行中请求完成） |
| `distributor` | `distributor: HttpRequestDistributor` | 获取分发器，用于注册路由 |
| `port` | `port: UInt16` | 获取实际监听端口 |
| `afterBind` | `afterBind(() -> Unit): Unit` | 绑定端口后的回调 |
| `onShutdown` | `onShutdown(() -> Unit): Unit` | 关闭时回调 |
| `updateCert` | `updateCert(String, String): Unit` | 热更新证书（证书路径, 密钥路径） |
| `updateCA` | `updateCA(String): Unit` | 热更新 CA 证书 |

### 2.4 内置 Handler

| Handler | 说明 |
|---------|------|
| `NotFoundHandler()` | 返回 404 |
| `RedirectHandler(url, status)` | 重定向 |
| `FileHandler` | 静态文件服务 |

### 2.5 自定义分发器

```cangjie
import stdx.net.http.*
import std.collection.HashMap

class MyDistributor <: HttpRequestDistributor {
    let map = HashMap<String, HttpRequestHandler>()
    public func register(path: String, handler: HttpRequestHandler): Unit {
        map.add(path, handler)
    }
    public func distribute(path: String): HttpRequestHandler {
        map.get(path) ?? NotFoundHandler()
    }
}
```

### 2.6 分块传输与 Trailer

```cangjie
import stdx.net.http.*

main() {
    let server: Server = ServerBuilder().addr("127.0.0.1").port(8080).build()

    // 使用 HttpResponseWriter 实现分块响应
    server.distributor.register("/stream", {
        ctx =>
        ctx.responseBuilder.header("transfer-encoding", "chunked")
        ctx.responseBuilder.header("trailer", "checkSum")
        let writer = HttpResponseWriter(ctx)
        for (i in 0..10) {
            writer.write("chunk ${i}\n".toArray())
        }
        ctx.responseBuilder.trailer("checkSum", "abc123")
    })

    server.serve()
}
```

---

## 3. 客户端

### 3.1 基本用法

```cangjie
import stdx.net.http.*
import std.io.*

main() {
    let client: Client = ClientBuilder().build()

    // GET 请求
    let rsp = client.get("http://example.com/hello")
    let body = StringReader(rsp.body).readToEnd()
    println(body)

    client.close()
}
```

### 3.2 ClientBuilder 配置接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `build` | `build(): Client` | 构建 Client 实例 |
| `tlsConfig` | `tlsConfig(TlsClientConfig): ClientBuilder` | TLS 配置（启用 HTTPS） |
| `httpProxy` | `httpProxy(String): ClientBuilder` | HTTP 代理 |
| `httpsProxy` | `httpsProxy(String): ClientBuilder` | HTTPS 代理 |
| `cookieJar` | `cookieJar(?CookieJar): ClientBuilder` | Cookie 管理 |
| `autoRedirect` | `autoRedirect(Bool): ClientBuilder` | 自动跟随重定向 |
| `readTimeout` | `readTimeout(Duration): ClientBuilder` | 读超时 |
| `writeTimeout` | `writeTimeout(Duration): ClientBuilder` | 写超时 |
| `enablePush` | `enablePush(Bool): ClientBuilder` | HTTP/2 服务端推送 |
| `poolSize` | `poolSize(Int64): ClientBuilder` | 连接池大小 |
| `logger` | `logger(Logger): ClientBuilder` | 自定义日志 |
| `connector` | `connector(...): ClientBuilder` | 自定义 TCP 连接函数 |

### 3.3 Client 常用方法

| 方法 | 签名 | 说明 |
|------|------|------|
| `get` | `get(String): HttpResponse` | 发送 GET 请求 |
| `post` | `post(String, String): HttpResponse` | 发送 POST 请求（字符串体） |
| `post` | `post(String, Array<UInt8>): HttpResponse` | 发送 POST 请求（字节体） |
| `put` | `put(String, String): HttpResponse` | 发送 PUT 请求 |
| `delete` | `delete(String): HttpResponse` | 发送 DELETE 请求 |
| `head` | `head(String): HttpResponse` | 发送 HEAD 请求 |
| `options` | `options(String): HttpResponse` | 发送 OPTIONS 请求 |
| `send` | `send(HttpRequest): HttpResponse` | 发送自定义请求 |
| `close` | `close(): Unit` | 关闭客户端，释放连接 |

### 3.4 自定义请求

```cangjie
import stdx.net.http.*

main() {
    let client: Client = ClientBuilder().build()
    let req = HttpRequestBuilder()
        .method("POST")
        .url("http://example.com/api")
        .header("Content-Type", "application/json")
        .body("{\"key\": \"value\"}")
        .build()
    let rsp = client.send(req)
    println(rsp)
    client.close()
}
```

### 3.5 HttpRequestBuilder 接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `url` | `url(String): HttpRequestBuilder` | 设置请求 URL |
| `method` | `method(String): HttpRequestBuilder` | 设置 HTTP 方法 |
| `header` | `header(String, String): HttpRequestBuilder` | 添加请求头 |
| `body` | `body(String): HttpRequestBuilder` | 设置请求体（字符串） |
| `body` | `body(Array<UInt8>): HttpRequestBuilder` | 设置请求体（字节） |
| `version` | `version(Protocol): HttpRequestBuilder` | 指定协议版本 |
| `build` | `build(): HttpRequest` | 构建 HttpRequest 实例 |

### 3.6 HttpResponseBuilder 接口

| 方法 | 签名 | 说明 |
|------|------|------|
| `status` | `status(UInt16): HttpResponseBuilder` | 设置状态码 |
| `header` | `header(String, String): HttpResponseBuilder` | 添加响应头 |
| `body` | `body(String): HttpResponseBuilder` | 设置响应体 |
| `trailer` | `trailer(String, String): HttpResponseBuilder` | 设置 Trailer |
| `build` | `build(): HttpResponse` | 构建 HttpResponse |

### 3.7 Cookie 管理

- 服务端设置：`responseBuilder.header("Set-Cookie", cookie.toSetCookieString())`
- 客户端自动管理：`ClientBuilder` 默认启用 `CookieJar`
- `Cookie(name, value, maxAge, domain, path)` — 构造 Cookie

---

## 4. HTTPS（HTTP + TLS）

### 4.1 HTTPS 服务端

```cangjie
import std.io.*
import std.fs.*
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

main() {
    // 配置 TLS
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    var tlsConfig = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )
    tlsConfig.supportedAlpnProtocols = ["h2"]  // 启用 HTTP/2

    let server = ServerBuilder()
        .addr("127.0.0.1").port(8443)
        .tlsConfig(tlsConfig)
        .build()
    server.distributor.register("/", { ctx => ctx.responseBuilder.body("Secure!") })
    server.serve()
}
```

### 4.2 HTTPS 客户端（TrustAll 模式 — 快速上手）

在开发测试阶段，可使用 `verifyMode = TrustAll` 跳过证书验证，方便快速调试 HTTPS 接口。**生产环境不应使用此模式**。

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.*

main() {
    // 配置 TLS 客户端，使用 TrustAll 模式跳过证书验证
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = TrustAll

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    // 发送 HTTPS 请求
    let resp = client.get("https://127.0.0.1:8443/")
    let body = StringReader(resp.body).readToEnd()
    println(body)

    client.close()
}
```

### 4.3 HTTPS 客户端（自定义 CA 证书）

在生产环境中，应使用 `Default`（系统 CA）或 `CustomCA` 模式验证服务端证书：

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.X509Certificate
import std.io.*
import std.fs.*

main() {
    // 加载自定义 CA 证书
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))
    let caCerts = X509Certificate.decodeFromPem(caPem)

    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = CustomCA(caCerts)

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://myserver.example.com/api")
    let body = StringReader(resp.body).readToEnd()
    println(body)

    client.close()
}
```

### 4.4 关键配置说明

| 配置项 | 说明 |
|--------|------|
| `TlsClientConfig.verifyMode` | 证书验证模式：`Default`（系统 CA）、`TrustAll`（信任所有，仅测试用）、`CustomCA(certs)`（自定义 CA） |
| `TlsServerConfig.supportedAlpnProtocols` | ALPN 协议列表，设置 `["h2"]` 启用 HTTP/2 |
| `server.updateCert(certPath, keyPath)` | 热更新服务端证书 |
| `server.updateCA(caPath)` | 热更新 CA 证书 |

---

## 5. 关键规则速查

| 规则 | 说明 |
|------|------|
| 设置响应体 | 通过 `httpContext.responseBuilder.body(...)` 设置 |
| 阻塞调用 | `server.serve()` 阻塞当前线程，需在新线程中启动或放在 main 末尾 |
| 释放连接 | 客户端使用完毕后调用 `client.close()` |
| HTTP/2 | 需 TLS + ALPN `h2` 配置 |
| 读取响应体 | 使用 `StringReader(resp.body).readToEnd()` 读取字符串 |
| HTTPS 快速测试 | 客户端设置 `tlsConfig.verifyMode = TrustAll` |
