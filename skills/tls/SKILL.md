---
name: cangjie-tls
description: "仓颉语言 TLS 安全通信。当需要了解仓颉 stdx.net.tls 包的 TLS 核心功能、客户端/服务端配置（TlsClientConfig/TlsServerConfig）、TlsSocket 用法、证书验证模式、会话恢复、各平台 OpenSSL 编译构建等信息时，应使用此 Skill。"
---

# 仓颉语言 TLS 安全通信 Skill

## 1. 概述

`stdx.net.tls` 包提供 TLS（Transport Layer Security）安全加密网络通信能力：

- 支持 **TLS 1.2** 和 **TLS 1.3** 协议
- 基于 `TlsSocket` 在客户端和服务端之间建立加密传输通道
- 支持证书验证、会话恢复、ALPN 协议协商等
- 依赖 **OpenSSL 3** 动态库
- 通常与 HTTP 模块（`stdx.net.http`）集成使用，也可独立用于 TCP 层 TLS 加密

**导入**：`import stdx.net.tls.*`

关于扩展标准库 `stdx` 的下载与配置，请参阅 `cangjie-stdx` Skill。

---

## 2. OpenSSL 依赖与编译构建

使用 `stdx.net.tls` 包需要外部依赖 OpenSSL 3 的 `ssl` 和 `crypto` 动态库。不同平台的安装和配置方式如下：

### 2.1 Linux

**方式一：包管理器安装（推荐）**

```bash
# Ubuntu 22.04+
sudo apt install libssl-dev
```

确保系统安装目录下存在以下动态库文件：
- `libssl.so`、`libssl.so.3`
- `libcrypto.so`、`libcrypto.so.3`

**方式二：源码编译安装**

下载 OpenSSL 3.x.x 源码编译安装，确保安装目录下包含上述动态库文件。

- 如果系统未安装 OpenSSL，选择安装到系统路径
- 如果安装在自定义目录，将库文件所在目录添加到环境变量：

```bash
export LD_LIBRARY_PATH=/path/to/openssl/lib:$LD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/openssl/lib:$LIBRARY_PATH
```

**静态库编译额外配置**：使用 crypto 和 net 包的静态库时，需在 `cjpm.toml` 中添加：

```toml
compile-option = "-ldl"
```

### 2.2 Windows

1. 下载 OpenSSL 3.x.x 源码编译安装 x64 架构软件包，或下载第三方预编译的 OpenSSL 3.x.x 开发包
2. 确保安装目录下包含以下库文件：
   - `libssl.dll.a`（或 `libssl.lib`）、`libssl-3-x64.dll`
   - `libcrypto.dll.a`（或 `libcrypto.lib`）、`libcrypto-3-x64.dll`
3. 配置环境变量：
   - 将 `.dll.a`（或 `.lib`）文件所在目录添加到 `LIBRARY_PATH`
   - 将 `.dll` 文件所在目录添加到 `PATH`

**静态库编译额外配置**：

```toml
compile-option = "-lcrypt32"
```

### 2.3 macOS

**方式一：Homebrew 安装（推荐）**

```bash
brew install openssl@3
```

确保系统安装目录下存在 `libcrypto.dylib` 和 `libcrypto.3.dylib`。

**方式二：源码编译安装**

下载 OpenSSL 3.x.x 源码编译安装，确保安装目录下包含上述动态库文件。

- 如果安装在自定义目录，将库文件所在目录添加到环境变量：

```bash
export DYLD_LIBRARY_PATH=/path/to/openssl/lib:$DYLD_LIBRARY_PATH
export LIBRARY_PATH=/path/to/openssl/lib:$LIBRARY_PATH
```

### 2.4 cjpm.toml 配置示例

```toml
[package]
  name = "my-tls-app"
  version = "1.0.0"
  output-type = "executable"

[dependencies]

# Linux x86_64
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["/path/to/stdx/dynamic/stdx"]

# macOS aarch64
# [target.aarch64-apple-darwin]
#   [target.aarch64-apple-darwin.bin-dependencies]
#     path-option = ["/path/to/stdx/dynamic/stdx"]

# Windows x86_64
# [target.x86_64-w64-mingw32]
#   [target.x86_64-w64-mingw32.bin-dependencies]
#     path-option = ["D:\\path\\to\\stdx\\dynamic\\stdx"]
```

> **注意**：如果未安装 OpenSSL 3 或安装了低版本，程序运行时会抛出 `TlsException: Can not load openssl library or function xxx`。

---

## 3. 核心类型

### 3.1 类型总览

| 类型 | 分类 | 说明 |
|------|------|------|
| `TlsSocket` | 类 | 加密传输通道，用于 TLS 握手和加密数据收发 |
| `TlsSessionContext` | 类 | 服务端会话上下文，用于 session 恢复 |
| `TlsClientConfig` | 结构体 | 客户端 TLS 配置 |
| `TlsServerConfig` | 结构体 | 服务端 TLS 配置 |
| `TlsSession` | 结构体 | 客户端会话 ID，用于会话复用 |
| `CipherSuite` | 结构体 | TLS 密码套件 |
| `CertificateVerifyMode` | 枚举 | 证书验证模式 |
| `TlsVersion` | 枚举 | TLS 协议版本 |
| `TlsClientIdentificationMode` | 枚举 | 服务端对客户端证书的认证模式 |
| `TlsException` | 异常 | TLS 处理异常 |

### 3.2 TlsSocket

| 方法 / 属性 | 签名 | 说明 |
|-------------|------|------|
| `client` (静态) | `TlsSocket.client(StreamingSocket, clientConfig: TlsClientConfig, session!: ?TlsSession): TlsSocket` | 创建客户端 TLS 套接字 |
| `server` (静态) | `TlsSocket.server(StreamingSocket, serverConfig: TlsServerConfig, sessionContext!: ?TlsSessionContext): TlsSocket` | 创建服务端 TLS 套接字 |
| `handshake` | `handshake(timeout!: ?Duration): Unit` | 执行 TLS 握手（仅调用一次） |
| `read` | `read(Array<Byte>): Int64` | 读取解密数据 |
| `write` | `write(Array<Byte>): Unit` | 发送加密数据 |
| `close` | `close(): Unit` | 关闭 TLS 连接 |
| `isClosed` | `isClosed(): Bool` | 检查连接状态 |
| `session` | `session: ?TlsSession` | 获取会话 ID（用于会话恢复） |
| `tlsVersion` | `tlsVersion: TlsVersion` | 协商的 TLS 版本 |
| `cipherSuite` | `cipherSuite: CipherSuite` | 协商的密码套件 |
| `alpnProtocolName` | `alpnProtocolName: ?String` | 协商的 ALPN 协议 |
| `peerCertificate` | `peerCertificate: ?X509Certificate` | 对端证书 |

### 3.3 TlsClientConfig

| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `verifyMode` | `CertificateVerifyMode` | `Default` | 证书验证模式 |
| `domain` | `?String` | `None` | 服务端主机名（SNI） |
| `alpnProtocolsList` | `Array<String>` | `[]` | ALPN 协议列表（如 `["h2"]`） |
| `clientCertificate` | `?(X509Certificate, PrivateKey)` | `None` | 客户端证书和私钥（双向认证时使用） |
| `cipherSuitesV1_2` | `?Array<CipherSuite>` | `None` | TLS 1.2 密码套件 |
| `cipherSuitesV1_3` | `?Array<CipherSuite>` | `None` | TLS 1.3 密码套件 |
| `minVersion` | `TlsVersion` | `V1_2` | 最低 TLS 版本 |
| `maxVersion` | `TlsVersion` | `V1_3` | 最高 TLS 版本 |
| `securityLevel` | `Int32` | `2` | 安全级别（0-5） |
| `signatureAlgorithms` | `?Array<SignatureAlgorithm>` | `None` | 签名算法偏好 |
| `keylogCallback` | `?(String) -> Unit` | `None` | TLS 密钥日志回调（调试用） |

### 3.4 TlsServerConfig

| 属性 / 构造 | 类型 | 说明 |
|-------------|------|------|
| 构造函数 | `TlsServerConfig(X509Certificate, PrivateKey)` | 必须提供服务端证书链和私钥 |
| `clientIdentityRequired` | `TlsClientIdentificationMode` | 客户端证书认证模式 |
| `verifyMode` | `CertificateVerifyMode` | 证书验证模式 |
| `supportedAlpnProtocols` | `Array<String>` | 支持的 ALPN 协议 |
| `cipherSuitesV1_2` / `V1_3` | `?Array<CipherSuite>` | 密码套件配置 |
| `minVersion` / `maxVersion` | `TlsVersion` | TLS 版本范围 |
| `securityLevel` | `Int32` | 安全级别（0-5） |
| `dhParameters` | `?DhParameters` | DH 密钥交换参数 |

### 3.5 证书验证模式（CertificateVerifyMode）

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `Default` | 使用系统 CA 验证证书 | 生产环境（默认） |
| `CustomCA(Array<X509Certificate>)` | 使用自定义 CA 列表验证 | 自签名证书或私有 CA |
| `TrustAll` | 信任所有证书，不验证 | **仅限开发测试** |

### 3.6 客户端认证模式（TlsClientIdentificationMode）

| 模式 | 说明 |
|------|------|
| `Disabled` | 不要求客户端证书（单向认证，默认） |
| `Optional` | 客户端可选提供证书 |
| `Required` | 客户端必须提供证书（双向认证） |

---

## 4. 使用示例

### 4.1 TLS 客户端（TrustAll 模式 — 快速测试）

```cangjie
import std.net.TcpSocket
import stdx.net.tls.*

main() {
    var config = TlsClientConfig()
    config.verifyMode = TrustAll           // 跳过证书验证（仅测试用）
    config.alpnProtocolsList = ["h2"]      // 可选：协商 ALPN 协议

    try (socket = TcpSocket("127.0.0.1", 8443)) {
        socket.connect()
        try (tls = TlsSocket.client(socket, clientConfig: config)) {
            tls.handshake()
            tls.write("Hello, TLS!\n".toArray())

            let buf = Array<Byte>(1024, repeat: 0)
            let n = tls.read(buf)
            println(String.fromUtf8(buf[..n]))
        }
    }
}
```

### 4.2 TLS 客户端（自定义 CA）

```cangjie
import std.net.TcpSocket
import std.io.*
import std.fs.*
import stdx.crypto.x509.X509Certificate
import stdx.net.tls.*

main() {
    let caPem = String.fromUtf8(readToEnd(File("./ca.crt", Read)))
    let caCerts = X509Certificate.decodeFromPem(caPem)

    var config = TlsClientConfig()
    config.verifyMode = CustomCA(caCerts)
    config.domain = "myserver.example.com"

    try (socket = TcpSocket("myserver.example.com", 8443)) {
        socket.connect()
        try (tls = TlsSocket.client(socket, clientConfig: config)) {
            tls.handshake()
            tls.write("GET / HTTP/1.1\r\nHost: myserver.example.com\r\n\r\n".toArray())

            let buf = Array<Byte>(4096, repeat: 0)
            let n = tls.read(buf)
            println(String.fromUtf8(buf[..n]))
        }
    }
}
```

### 4.3 TLS 服务端

```cangjie
import std.io.*
import std.fs.*
import std.net.{TcpServerSocket, TcpSocket}
import stdx.crypto.x509.{X509Certificate, PrivateKey}
import stdx.net.tls.*

main() {
    // 解析证书和私钥
    let pem = String.fromUtf8(readToEnd(File("./server.crt", Read)))
    let keyText = String.fromUtf8(readToEnd(File("./server.key", Read)))
    let certificate = X509Certificate.decodeFromPem(pem)
    let privateKey = PrivateKey.decodeFromPem(keyText)

    let config = TlsServerConfig(certificate, privateKey)

    // 可选：启用会话恢复
    let sessions = TlsSessionContext.fromName("my-server")

    try (server = TcpServerSocket(bindAt: 8443)) {
        server.bind()
        println("TLS server listening on port 8443")

        while (true) {
            let clientSocket = server.accept()
            spawn { =>
                try (tls = TlsSocket.server(clientSocket, serverConfig: config, sessionContext: sessions)) {
                    tls.handshake()
                    let buf = Array<Byte>(1024, repeat: 0)
                    let n = tls.read(buf)
                    println("Received: ${String.fromUtf8(buf[..n])}")
                    tls.write("Hello from TLS server!\n".toArray())
                } catch (e: Exception) {
                    println("TLS error: ${e}")
                } finally {
                    clientSocket.close()
                }
            }
        }
    }
}
```

### 4.4 会话恢复（减少握手开销）

```cangjie
import std.net.TcpSocket
import stdx.net.tls.*

main() {
    var config = TlsClientConfig()
    config.verifyMode = TrustAll

    var lastSession: ?TlsSession = None

    // 多次连接复用会话
    for (i in 0..3) {
        try (socket = TcpSocket("127.0.0.1", 8443)) {
            socket.connect()
            try (tls = TlsSocket.client(socket, clientConfig: config, session: lastSession)) {
                try {
                    tls.handshake()
                    lastSession = tls.session  // 保存会话用于下次复用
                    tls.write("Request ${i}\n".toArray())
                } catch (e: Exception) {
                    lastSession = None         // 握手失败则清除会话
                    throw e
                }
            }
        } catch (e: Exception) {
            println("Connection ${i} failed: ${e}")
        }
    }
}
```

### 4.5 与 HTTP 模块集成使用

TLS 通常通过 HTTP 模块的 `tlsConfig()` 方法集成使用，而非直接操作 `TlsSocket`：

```cangjie
import stdx.net.http.*
import stdx.net.tls.*
import std.io.*

main() {
    // HTTPS 客户端（TrustAll 快速测试）
    var tlsConfig = TlsClientConfig()
    tlsConfig.verifyMode = TrustAll

    let client = ClientBuilder()
        .tlsConfig(tlsConfig)
        .build()

    let resp = client.get("https://127.0.0.1:8443/api")
    let body = StringReader(resp.body).readToEnd()
    println(body)

    client.close()
}
```

---

## 5. 快速参考

| 需求 | 做法 |
|------|------|
| 跳过证书验证（测试） | `config.verifyMode = TrustAll` |
| 使用系统 CA 验证 | `config.verifyMode = Default`（默认） |
| 使用自定义 CA | `config.verifyMode = CustomCA(certs)` |
| 启用 HTTP/2 ALPN | `config.alpnProtocolsList = ["h2"]`（客户端）或 `config.supportedAlpnProtocols = ["h2"]`（服务端） |
| 会话恢复 | 保存 `tls.session`，下次连接时传入 `session` 参数 |
| 双向认证 | 服务端设置 `config.clientIdentityRequired = Required`，客户端设置 `config.clientCertificate` |
| 安装 OpenSSL 3 | Linux: `apt install libssl-dev`，macOS: `brew install openssl@3`，Windows: 下载预编译包 |
| 静态库额外链接 | Linux: `-ldl`，Windows: `-lcrypt32` |
