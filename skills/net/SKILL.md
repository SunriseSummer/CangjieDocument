---
name: cangjie-net
description: "仓颉语言网络编程。当需要了解仓颉语言的TCP/UDP Socket编程、Socket选项与超时、Unix Domain Socket、IP地址工具、HTTP服务端与客户端(ServerBuilder/ClientBuilder)、WebSocket编程、TLS/SSL加密通信等特性时，应使用此 Skill。"
---

# 仓颉语言网络编程 Skill

## 1. 网络概述

### 1.1 分层
- **传输层**（`std.net` 包）：TCP（`TcpSocket`）、UDP（`UdpSocket`）、Unix Domain Socket
- **应用层**（`stdx.net.http` 包）：HTTP/1.0、1.1、2.0 和 WebSocket
- **安全层**（`stdx.net.tls` 包）：TLS 1.2/1.3 加密传输

### 1.2 关键规则
- 网络操作在仓颉线程级别是**阻塞**的，但不阻塞 OS 线程（仓颉线程让出）
- 所有 Socket 均实现 `Resource`，使用 `try-with-resource` 自动清理

### 1.3 地址类型
- `SocketAddress`（抽象基类）→ `IPSocketAddress`（IP+端口）、`UnixSocketAddress`（文件路径）
- `IPAddress`（抽象）→ `IPv4Address`、`IPv6Address`
  - `IPAddress.parse(str)` / `IPAddress.tryParse(str)` — 解析地址
  - `IPAddress.resolve(hostname)` — DNS 解析
  - 常用判断：`isLoopback()`、`isPrivate()`、`isMulticast()`

---

## 2. TCP 编程

### 2.1 服务端
- `TcpServerSocket(bindAt: port)` → `bind()` → `accept()`（阻塞等待连接）
- `accept(timeout)` — 带超时的接受连接
- 属性：`backlogSize`、`reuseAddress`、`reusePort`、`receiveBufferSize`、`sendBufferSize`

### 2.2 客户端
- `TcpSocket(host, port)` → `connect()` → `read()`/`write()`
- `connect(timeout)` — 带超时连接
- 超时配置：`readTimeout`、`writeTimeout`（`Duration` 类型）
- TCP 调优：`noDelay`（TCP_NODELAY）、`keepAlive`（`SocketKeepAliveConfig`）、`linger`

### 2.3 完整示例

```cangjie
import std.net.*
import std.sync.*

let SERVER_PORT: UInt16 = 33333
let ready = SyncCounter(1)

func runServer() {
    try (server = TcpServerSocket(bindAt: SERVER_PORT)) {
        server.bind()
        ready.dec()
        try (client = server.accept()) {
            let buf = Array<Byte>(10, repeat: 0)
            let n = client.read(buf)
            println("Server read ${n} bytes: ${buf}")
        }
    }
}

main(): Int64 {
    let fut = spawn { runServer() }
    ready.waitUntilZero()

    try (socket = TcpSocket("127.0.0.1", SERVER_PORT)) {
        socket.connect()
        socket.write([1, 2, 3])
    }
    fut.get()
    return 0
}
```

---

## 3. UDP 编程

- `UdpSocket(bindAt: port)` → `bind()`
- 发送：`sendTo(IPSocketAddress, data)` 或连接后 `send(data)`
- 接收：`receiveFrom(buffer)` → `(SocketAddress, count)`，或连接后 `receive(buffer)`
- 可选 `connect(addr)` 锁定远端地址（之后可用 `send`/`receive`）
- `disconnect()` — 解除连接
- **限制**：单包最大 64KB
- 超时：`receiveTimeout`、`sendTimeout`

```cangjie
import std.net.*
import std.sync.*
import std.time.*

let SERVER_PORT: UInt16 = 33333
let barrier = Barrier(2)

func runUdpServer() {
    try (server = UdpSocket(bindAt: SERVER_PORT)) {
        server.bind()
        barrier.wait()
        let buf = Array<Byte>(3, repeat: 0)
        let (addr, n) = server.receiveFrom(buf)
        println("Received ${n} bytes: ${buf}")
    }
}

main(): Int64 {
    let fut = spawn { runUdpServer() }
    barrier.wait()

    try (sock = UdpSocket(bindAt: 0)) {
        sock.sendTimeout = Duration.second * 2
        sock.bind()
        sock.sendTo(IPSocketAddress("127.0.0.1", SERVER_PORT), [1, 2, 3])
    }
    fut.get()
    return 0
}
```

---

## 4. Socket 选项与超时

### 4.1 通用选项
| 属性 | 说明 |
|------|------|
| `readTimeout` / `writeTimeout` | 读写超时（`Duration` 类型），超时抛 `SocketTimeoutException` |
| `reuseAddress` / `reusePort` | 地址/端口复用 |
| `receiveBufferSize` / `sendBufferSize` | 收发缓冲区大小 |

### 4.2 TCP 专有
| 属性 | 说明 |
|------|------|
| `noDelay` | 禁用 Nagle 算法（降低延迟） |
| `keepAlive` | `SocketKeepAliveConfig(interval, count)` — TCP 保活配置 |
| `linger` | SO_LINGER — 关闭时等待数据发送完毕 |

### 4.3 底层选项访问
- `getSocketOptionIntNative(level, name)` / `setSocketOptionIntNative(level, name, value)`
- `OptionLevel`：`TCP`、`SOCKET` 等
- `SocketOptions`：`TCP_NODELAY`、`SO_KEEPALIVE`、`SO_REUSEADDR` 等常量

```cangjie
import std.net.*
import std.time.*

main() {
    try (sock = TcpSocket("127.0.0.1", 80)) {
        sock.readTimeout = Duration.second
        sock.noDelay = true
        sock.linger = Duration.minute
        sock.keepAlive = SocketKeepAliveConfig(
            interval: Duration.second * 7,
            count: 15
        )
    }
}
```

---

## 5. Unix Domain Socket

- 基于文件路径的进程间通信（IPC），不经过网络栈
- **不支持 Windows**，路径最大 108 字节
- 流式：`UnixServerSocket(bindAt: path)` + `UnixSocket(path)`
- 数据报式：`UnixDatagramSocket(bindAt: path)`
- 使用后需手动 `remove(path)` 清理 socket 文件

```cangjie
import std.net.*
import std.sync.*
import std.fs.*

let SOCK_PATH = "/tmp/cj_demo.sock"
let barrier = Barrier(2)

func runServer() {
    try (server = UnixServerSocket(bindAt: SOCK_PATH)) {
        server.bind()
        barrier.wait()
        try (client = server.accept()) {
            client.write("hello".toArray())
        }
    }
}

main(): Int64 {
    let fut = spawn { runServer() }
    barrier.wait()
    try (sock = UnixSocket(SOCK_PATH)) {
        sock.connect()
        let buf = Array<Byte>(5, repeat: 0)
        sock.read(buf)
        println(String.fromUtf8(buf))  // "hello"
    }
    fut.get()
    remove(SOCK_PATH)
    return 0
}
```

---

## 6. HTTP 编程

- 导入 `stdx.net.http`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill
- 支持 HTTP/1.0、1.1、2.0（RFC 9110/9112/9113/9218/7541）
- HTTP/2 需 TLS + ALPN `h2` 配置

### 6.1 服务端

```cangjie
import stdx.net.http.*

main() {
    let server = ServerBuilder().addr("127.0.0.1").port(8080).build()

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

#### 核心组件
- `ServerBuilder`：配置 `addr`、`port`、`tlsConfig`、`transportConfig`、`distributor`
- `HttpContext`：包含 `request`（`HttpRequest`）和 `responseBuilder`（`HttpResponseBuilder`）
- `HttpRequestHandler`：请求处理接口，可用 Lambda 或 `FuncHandler` 实现
- 内置 Handler：`NotFoundHandler`、`RedirectHandler(url, status)`、`FileHandler`
- `server.afterBind(callback)` — 绑定端口后的回调（用于同步）
- `server.port` — 获取实际监听端口（`port(0)` 时获取随机端口）
- `server.close()` — 关闭服务器

#### 自定义分发器

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

#### 分块传输与 Trailer

```cangjie
import stdx.net.http.*

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
```

### 6.2 客户端

```cangjie
import stdx.net.http.*
import std.io.*

main() {
    let client = ClientBuilder().build()

    // GET 请求
    let rsp = client.get("http://example.com/hello")
    let buf = Array<UInt8>(1024, repeat: 0)
    let n = rsp.body.read(buf)
    println(String.fromUtf8(buf[..n]))

    client.close()
}
```

#### ClientBuilder 配置
- `httpProxy(url)` — HTTP 代理
- `tlsConfig(TlsClientConfig)` — TLS 配置
- `cookieJar(CookieJar)` — Cookie 管理
- `enablePush(bool)` — HTTP/2 服务端推送
- `connector(func)` — 自定义 TCP 连接函数

#### 自定义请求

```cangjie
import stdx.net.http.*

let client = ClientBuilder().build()
let req = HttpRequestBuilder()
    .method("POST")
    .url("http://example.com/api")
    .header("Content-Type", "application/json")
    .body("{\"key\": \"value\"}")
    .build()
let rsp = client.send(req)
```

### 6.3 Cookie 管理
- 服务端设置：`responseBuilder.header("Set-Cookie", cookie.toSetCookieString())`
- 客户端自动管理：`ClientBuilder` 默认启用 `CookieJar`
- `Cookie(name, value, maxAge, domain, path)` — 构造 Cookie

---

## 7. WebSocket 编程

- 导入 `stdx.net.http`
- 帧类型：**控制帧**（`CloseWebFrame`、`PingWebFrame`、`PongWebFrame`）、**数据帧**（`TextWebFrame`、`BinaryWebFrame`、`ContinuationWebFrame`）
- 帧属性：`fin`（是否最后一帧）、`frameType`、`payload`

### 7.1 服务端升级
```cangjie
server.distributor.register("/ws", {
    ctx =>
    let ws = WebSocket.upgradeFromServer(
        ctx,
        subProtocols: ArrayList<String>(["proto1"]),
        userFunc: { req =>
            let headers = HttpHeaders()
            headers.add("rsp", "ok")
            headers
        }
    )
    // 读取消息
    let frame = ws.read()
    println(String.fromUtf8(frame.payload))
    // 发送消息
    ws.write(TextWebFrame, "echo".toArray())
    // 关闭
    ws.writeCloseFrame(status: 1000)
    let _ = ws.read()  // 读取关闭响应
    ws.closeConn()
})
```

### 7.2 客户端升级
```cangjie
import stdx.net.http.*
import stdx.encoding.url.*
import std.collection.*

let client = ClientBuilder().build()
let url = URL.parse("ws://127.0.0.1:8080/ws")
let (ws, headers) = WebSocket.upgradeFromClient(
    client, url,
    subProtocols: ArrayList<String>(["proto1"]),
    headers: HttpHeaders()
)

// 发送
ws.write(TextWebFrame, "hello".toArray())
// 接收
let frame = ws.read()
println(String.fromUtf8(frame.payload))

// 关闭流程：发送 CloseFrame → 读取 CloseFrame → 关闭底层连接
ws.writeCloseFrame(status: 1000)
let _ = ws.read()
ws.closeConn()
client.close()
```

### 7.3 消息接收循环（处理分片）
```cangjie
let data = ArrayList<UInt8>()
var frame = ws.read()
while (true) {
    match (frame.frameType) {
        case TextWebFrame | BinaryWebFrame =>
            data.add(all: frame.payload)
            if (frame.fin) { break }
        case ContinuationWebFrame =>
            data.add(all: frame.payload)
            if (frame.fin) { break }
        case CloseWebFrame =>
            ws.write(CloseWebFrame, frame.payload)
            break
        case PingWebFrame => ws.writePongFrame(frame.payload)
        case _ => ()
    }
    frame = ws.read()
}
```

---

## 8. TLS/SSL 加密通信

- 导入 `stdx.net.tls`，需要 **OpenSSL 3** 动态库
- 支持 TLS 1.2、TLS 1.3

### 8.1 TLS 服务端
```cangjie
import std.net.*
import std.io.*
import std.fs.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.tls.*

main() {
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let key = String.fromUtf8(readToEnd(File("./server.key", Read)))
    let config = TlsServerConfig(
        X509Certificate.decodeFromPem(pem),
        PrivateKey.decodeFromPem(key)
    )

    try (server = TcpServerSocket(bindAt: 8443)) {
        server.bind()
        while (true) {
            let client = server.accept()
            spawn {
                try (tls = TlsSocket.server(client, serverConfig: config)) {
                    tls.handshake()
                    let buf = Array<Byte>(100, repeat: 0)
                    tls.read(buf)
                    tls.write("OK".toArray())
                } finally {
                    client.close()
                }
            }
        }
    }
}
```

### 8.2 TLS 客户端
```cangjie
import std.net.TcpSocket
import stdx.net.tls.*

main() {
    var config = TlsClientConfig()
    config.verifyMode = TrustAll         // 或 CustomCA(cert)
    config.alpnProtocolsList = ["h2"]    // ALPN 协议协商

    try (sock = TcpSocket("127.0.0.1", 8443)) {
        sock.connect()
        try (tls = TlsSocket.client(sock, clientConfig: config)) {
            tls.handshake()
            tls.write("Hello TLS".toArray())
        }
    }
}
```

### 8.3 HTTPS 服务端（HTTP + TLS）
```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import stdx.crypto.x509.{X509Certificate, PrivateKey}

// 配置 TLS
var tlsConfig = TlsServerConfig(cert, key)
tlsConfig.supportedAlpnProtocols = ["h2"]  // 启用 HTTP/2

let server = ServerBuilder()
    .addr("127.0.0.1").port(8443)
    .tlsConfig(tlsConfig)
    .build()
server.distributor.register("/", { ctx => ctx.responseBuilder.body("Secure!") })
server.serve()
```

### 8.4 关键配置
- `TlsServerConfig(cert, privateKey)` — 服务端证书配置
- `TlsClientConfig` — 客户端配置
  - `verifyMode`：`TrustAll`（不校验）、`CustomCA(cert)`（自定义 CA）
  - `alpnProtocolsList` — ALPN 协议列表
- `TlsSessionContext.fromName(name)` — 会话恢复上下文
- `server.updateCert(certPath, keyPath)` — 热更新证书
- `server.updateCA(caPath)` — 热更新 CA

---

## 9. 异常类型

| 异常 | 说明 |
|------|------|
| `SocketException` | 通用 Socket 错误 |
| `SocketTimeoutException` | Socket 操作超时 |

---

## 10. 关键规则速查

1. 所有 Socket/Server 使用 `try-with-resource` 自动清理
2. TCP 服务端模式：`TcpServerSocket` → `bind()` → 循环 `accept()`
3. UDP 单包最大 64KB
4. HTTP Handler 通过 `httpContext.responseBuilder.body(...)` 设置响应体
5. WebSocket 关闭需三步：`writeCloseFrame` → `read` 关闭响应 → `closeConn`
6. TLS 需要先建立 TCP 连接，再在其上创建 `TlsSocket` 并 `handshake()`
7. HTTP/2 需 TLS + ALPN `h2` 配置
