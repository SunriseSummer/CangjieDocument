# 第七章：并发 Worker 模型 (并发编程)

> Web 服务器必须能同时处理成千上万个请求。虽然仓颉的 `main` 是单线程的，但通过 `spawn` 我们可以实现高并发，并将耗时任务分发给 Worker。

## 本章目标

*   理解并发 Worker 的调度与同步方式。
*   学会用原子变量统计共享指标。
*   建立“异步处理 + 主线程协作”的工程认知。

## 1. 请求处理 Worker

模拟一个能够并发处理请求的 Worker 池。

```cangjie
import std.sync.*
import std.time.*
import std.collection.*

// 模拟耗时的业务逻辑
func handleRequest(id: Int64) {
    let processTime = Duration.millisecond * (id * 100) // 模拟不同耗时
    println("Worker [${id}]: 开始处理 (预计 ${id * 100}ms)")
    sleep(processTime)
    println("Worker [${id}]: 完成 ✅")
}

main() {
    println(">>> Web 服务器启动，准备接收并发请求...")

    let futures = ArrayList<Future<Unit>>()

    // 模拟瞬间涌入 5 个请求
    for (i in 1..=5) {
        // spawn 启动轻量级线程
        let f = spawn {
            handleRequest(i)
        }
        futures.append(f)
    }

    println(">>> 主线程：所有请求已分发，继续监听新请求...")

    // 模拟主线程做其他事
    sleep(Duration.second)

    // 等待所有请求完成 (实际 Server 不需要等，这里为了演示)
    for (f in futures) { f.get() }
    println(">>> 所有请求处理完毕。")
}
```

## 2. 线程安全计数器 (Atomic)

统计服务器的总请求数 (QPS)，必须保证线程安全。

```cangjie
main() {
    let totalRequests = AtomicInt64(0)

    // 并发增加计数
    for (i in 0..100) {
        spawn {
            totalRequests.fetchAdd(1)
        }
    }

    sleep(Duration.millisecond * 500)
    println("总请求数: ${totalRequests.load()}")
}
```

## 语言特性与应用解读

`spawn` 启动轻量线程并返回 `Future<Unit>`，结合 `for (f in futures) { f.get() }` 实现最基础的同步等待。
`Duration.millisecond * (id * 100)` 展示了时间单位的可读表达方式，便于描述 SLA 与性能测试。
`AtomicInt64.fetchAdd` 适合高并发下的计数统计，不需要额外锁即可保证一致性。

## 工程化提示

*   真实服务会使用线程池或协程框架，本例仅演示核心概念。
*   计数器更新应考虑高并发下的性能瓶颈。
*   请求处理建议添加超时与异常捕获机制。

## 小试身手

1. 为 `handleRequest` 增加失败分支，并统计失败次数。
2. 将 `totalRequests` 统计改为“成功/失败”双计数。
