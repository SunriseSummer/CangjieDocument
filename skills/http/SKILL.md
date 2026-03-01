---
name: cangjie-http
description: "仓颉语言 HTTP 编程。当需要了解仓颉语言的HTTP服务端(ServerBuilder)、HTTP客户端(ClientBuilder)、请求与响应处理、Cookie管理、分块传输、HTTPS/TLS配置、HTTP/2等特性时，应使用此 Skill。"
---

# 仓颉语言 HTTP 编程 Skill

## 1. 概述

- 依赖包 `stdx.net.http`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 支持 HTTP/1.0、1.1、2.0（RFC 9110/9112/9113/9218/7541）
- HTTP/2 需 TLS + ALPN `h2` 配置

---

## 2. 服务端

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

### 2.1 核心组件
- `ServerBuilder`：配置 `addr`、`port`、`tlsConfig`、`transportConfig`、`distributor`
- `HttpContext`：包含 `request`（`HttpRequest`）和 `responseBuilder`（`HttpResponseBuilder`）
- `HttpRequestHandler`：请求处理接口，可用 Lambda 或 `FuncHandler` 实现
- 内置 Handler：`NotFoundHandler`、`RedirectHandler(url, status)`、`FileHandler`
- `server.afterBind(callback)` — 绑定端口后的回调（用于同步）
- `server.port` — 获取实际监听端口（`port(0)` 时获取随机端口）
- `server.close()` — 关闭服务器

### 2.2 自定义分发器

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

### 2.3 分块传输与 Trailer

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

```cangjie
import stdx.net.http.*
import std.io.*

main() {
    let client: Client = ClientBuilder().build()

    // GET 请求
    let rsp = client.get("http://example.com/hello")
    let buf = Array<UInt8>(1024, repeat: 0)
    let n = rsp.body.read(buf)
    println(String.fromUtf8(buf[..n]))

    client.close()
}
```

### 3.1 ClientBuilder 配置
- `httpProxy(url)` — HTTP 代理
- `tlsConfig(TlsClientConfig)` — TLS 配置
- `cookieJar(CookieJar)` — Cookie 管理
- `enablePush(bool)` — HTTP/2 服务端推送
- `connector(func)` — 自定义 TCP 连接函数

### 3.2 自定义请求

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

### 3.3 Cookie 管理
- 服务端设置：`responseBuilder.header("Set-Cookie", cookie.toSetCookieString())`
- 客户端自动管理：`ClientBuilder` 默认启用 `CookieJar`
- `Cookie(name, value, maxAge, domain, path)` — 构造 Cookie

---

## 4. HTTPS（HTTP + TLS）

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

### 4.1 关键配置
- `server.updateCert(certPath, keyPath)` — 热更新证书
- `server.updateCA(caPath)` — 热更新 CA

---

## 5. 关键规则速查

1. HTTP Handler 通过 `httpContext.responseBuilder.body(...)` 设置响应体
2. `server.serve()` 是阻塞调用，需在新线程中启动或放在 main 末尾
3. 客户端使用完毕后调用 `client.close()` 释放连接
4. HTTP/2 需 TLS + ALPN `h2` 配置
