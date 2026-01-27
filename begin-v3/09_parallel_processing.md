# 第九章：并行处理 (并发编程)

> 智能家居系统需要同时处理多件事：一边采集温湿度，一边监控安防摄像头，还要响应用户的语音指令。如果按顺序一件件做，系统会卡顿。我们需要并发 (`Concurrency`)。

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
