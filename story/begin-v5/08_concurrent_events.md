# 08. 并发事件：实时调度

> 每一分钟都有车辆到站、订单入库、道路事件触发。调度系统必须并发处理多路事件。

## 本章目标

*   使用 `spawn` 并发执行任务。
*   通过 `Future` 汇总并发结果。
*   用原子变量统计共享指标。

## 1. 并行事件处理

```cangjie
import std.sync.*
import std.time.*
import std.collection.*

func handleDockEvent(name: String): Int64 {
    println("处理到站事件: ${name}")
    sleep(Duration.millisecond * 200)
    return 1
}

main() {
    let futures = ArrayList<Future<Int64>>()

    futures.append(spawn { handleDockEvent("Dock-A") })
    futures.append(spawn { handleDockEvent("Dock-B") })

    var total = 0
    for (f in futures) { total = total + f.get() }
    println("处理事件总数: ${total}")
}
```

## 2. 共享计数器

```cangjie
main() {
    let totalOrders = AtomicInt64(0)

    for (i in 0..10) {
        spawn { totalOrders.fetchAdd(1) }
    }

    sleep(Duration.millisecond * 300)
    println("累计订单: ${totalOrders.load()}")
}
```

## 语言特性与应用解读

`spawn { handleDockEvent("Dock-A") }` 返回 `Future<Int64>`，表明并发任务也可以带返回值。
通过遍历 `futures` 并调用 `get()` 汇总结果，体现“并发执行 + 同步汇总”的常用模式。
`AtomicInt64.fetchAdd` 让共享指标在并发场景中保持准确，避免手动加锁的开销。

## 工程化提示

*   并发任务应设置超时和失败回调，避免任务悬挂。
*   原子计数适用于简单指标，复杂状态需使用锁或消息队列。
*   并发输出日志可能乱序，建议引入统一日志队列。

## 实践挑战

1. 为 `handleDockEvent` 增加失败分支并统计失败次数。
2. 将并发事件改为“按优先级顺序汇总结果”。
