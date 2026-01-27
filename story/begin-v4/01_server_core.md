# 第一章：Web 服务内核 (Hello World)

> 现代互联网的基石是 Web 服务器。作为架构师，你的第一步是构建能够监听网络端口、响应客户端请求的核心服务。

## 1. 启动监听 (Hello Server)

我们不使用现成的框架，而是从 `main` 函数开始，模拟一个 Web 服务器的启动过程。

```cangjie
// file: web_core.cj
import std.net.* // 假设存在网络库
import std.time.*

main() {
    println(">>> [CangjieWeb] 框架内核正在初始化...")

    // 模拟绑定端口
    let port = 8080
    println(">>> 正在监听端口: ${port}")
    println(">>> 服务启动成功！等待连接...")

    // 模拟服务器主循环
    while (true) {
        // 在真实场景中，这里会 accept() 一个 socket 连接
        // 为了演示，我们暂停一下模拟空转
        sleep(Duration.second * 5)
        println("... [Heartbeat] 服务运行中 ...")
    }
}
```

## 2. 编译与运行

```bash
cjc web_core.cj -o server
./server
```

虽然它现在还不能处理真正的 HTTP 请求，但它已经具备了作为一个守护进程（Daemon）的基本形态。这是所有高性能服务器的起点。
