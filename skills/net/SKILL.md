---
name: cangjie-net
description: "仓颉语言网络编程。当需要了解仓颉语言的TCP/UDP Socket编程、HTTP服务端与客户端(ServerBuilder/ClientBuilder)、WebSocket编程等特性时，应使用此 Skill。"
---

# 仓颉语言网络编程 Skill

## 1. 网络概述

### 1.1 分层
- **传输层**（`std.net` 包）：`DatagramSocket`（不可靠，如 UDP → `UdpSocket`）和 `StreamSocket`（可靠，如 TCP → `TcpSocket`）
- 也支持 Unix Domain socket
- **应用层**：HTTP/1.0、1.1、2.0 和 WebSocket

### 1.2 关键规则
- 网络操作在仓颉线程级别是**阻塞**的，但不阻塞 OS 线程（仓颉线程让出）

---

## 2. Socket 编程

### 2.1 TCP
- **服务端**：创建 `TcpServerSocket(bindAt: port)` → `bind()` → `accept()`（阻塞）
- **客户端**：创建 `TcpSocket(host, port)` → `connect()` → `read()`/`write()`
- 双方均使用 `try-with-resource` 进行清理

### 2.2 UDP
- 双方均创建 `UdpSocket(bindAt: port)` → `bind()`
- 发送：`sendTo(IPSocketAddress, data)`
- 接收：`receiveFrom(buffer)` 返回 `(clientAddr, count)`
- 可选 `connect()` 到远端以限制发送者并简化发送

---

## 3. HTTP 编程

- 需要导入 `stdx.net.http`，关于扩展标准库 `stdx` 的配置用法，请参阅 `cangjie-stdx` Skill

### 3.1 服务端
```cangjie
ServerBuilder().addr(...).port(...).build()
server.distributor.register(path, handler_lambda)
server.serve()
```
- Handler 接收 `HttpContext`，通过 `httpContext.responseBuilder.body(...)` 设置响应

### 3.2 客户端
```cangjie
ClientBuilder().build()
client.get(url)
response.body  // 读取响应体
```

### 3.3 支持的协议
- HTTP 1.0/1.1/2.0，遵循 RFC 9110/9112/9113/9218/7541

---

## 4. WebSocket 编程

- 需要导入 `stdx.net.http`

### 4.1 帧类型
- **控制帧**：Close、Ping、Pong
- **数据帧**：Text、Binary、Continuation
- 帧具有 `fin`、`frameType`、`payload` 属性

### 4.2 服务端升级
- `WebSocket.upgradeFromServer(ctx, subProtocols, userFunc)`

### 4.3 客户端升级
- `WebSocket.upgradeFromClient(client, url, subProtocols, headers)` 返回 `(WebSocket, HttpHeaders)`

### 4.4 读写帧
- `websocket.read()` 读取帧
- `websocket.write(frameType, data)` 写入帧

### 4.5 关闭连接
- `writeCloseFrame(status)` + 读取关闭响应 + `closeConn()`
