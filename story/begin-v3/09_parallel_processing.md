# 第九章：并行处理 (并发编程)

> 智能家居系统需要同时处理多件事：一边采集温湿度，一边监控安防摄像头，还要响应用户的语音指令。如果按顺序一件件做，系统会卡顿。我们需要并发 (`Concurrency`) 来解耦时间轴。

## 本章目标

*   掌握并发任务的启动与同步流程。
*   理解共享资源保护与原子操作的价值。
*   学会将独立任务拆分为可并行模块。

## 1. 多任务并行 (Spawn)

我们需要同时启动温度监控和安防监控。

```cangjie
import std.time.*
import std.sync.*

func monitorTemperature() {
    println("🌡️ 温度监控服务已启动...")
    sleep(Duration.millisecond * 500) // 模拟耗时任务
    println("🌡️ 温度数据采集完成")
}

func monitorSecurity() {
    println("📹 安防监控服务已启动...")
    sleep(Duration.millisecond * 800)
    println("📹 安防画面无异常")
}

main() {
    println(">>> 系统服务并行启动中...")

    // 启动独立线程，不阻塞主程序
    let t1 = spawn { monitorTemperature() }
    let t2 = spawn { monitorSecurity() }

    println(">>> 主线程: 等待子系统就绪...")

    // 等待任务完成
    t1.get()
    t2.get()

    println(">>> 所有子系统启动完毕")
}
```

## 2. 共享资源保护 (Atomic)

假设有多个传感器同时向一个“总能耗计数器”上报数据。如果没有保护，计数会出错。

```cangjie
import std.sync.*
import std.collection.*

main() {
    // 全屋总能耗 (原子变量，线程安全)
    let totalPowerUsage = AtomicInt64(0)
    let tasks = ArrayList<Future<Unit>>()

    println("开始统计全屋能耗...")

    // 模拟 10 个设备同时上报能耗，每个消耗 50W
    for (i in 0..10) {
        let f = spawn {
            sleep(Duration.millisecond * 10)
            totalPowerUsage.fetchAdd(50) // 原子加法
        }
        tasks.append(f)
    }

    // 等待统计完成
    for (f in tasks) { f.get() }

    println("当前实时总功率: ${totalPowerUsage.load()} W") // 结果应为 500
}
```

## 语言特性与应用解读

`spawn` 会返回 `Future<Unit>`，`get()` 用于等待任务完成，构成最基础的并发同步模型。
并发块内的闭包可以捕获外部变量（如 `totalPowerUsage`），使任务之间共享状态成为可能，但也因此需要原子或锁保护。
`AtomicInt64.fetchAdd` 提供无锁的原子更新，适合高频计数场景。

## 工程化提示

*   并发任务应设置超时与失败回调，避免阻塞主流程。
*   共享资源计数可用原子变量，复杂状态请使用锁或消息队列。
*   并发输出日志可能乱序，建议采用统一日志队列。

## 小试身手

1. 为温度监控加入“采集次数”返回值，并在主线程汇总。
2. 将能耗统计改为“加/减”混合场景，验证最终结果。
