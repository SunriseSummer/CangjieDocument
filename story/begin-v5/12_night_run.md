# 12. 综合实战：夜间高峰调度

> 夜间 22:00，城市订单暴增，部分道路出现事故。你需要综合前面所有能力，完成一次高峰调度演练。

## 本章目标

*   综合运用建模、策略、并发与状态管理。
*   形成完整的调度流程思维。
*   通过清晰日志与指标输出构建可观测系统。

## 1. 简化版综合流程

```cangjie
import std.collection.*
import std.sync.*
import std.time.*

struct Order {
    let id: String
    let weight: Float64
    let priority: Int64
}

class Vehicle {
    let id: String
    var capacity: Float64
    var load: Float64

    public init(id: String, capacity: Float64) {
        this.id = id
        this.capacity = capacity
        this.load = 0.0
    }

    public func canLoad(weight: Float64): Bool {
        return load + weight <= capacity
    }
}

func decideLane(order: Order): String {
    if (order.priority >= 9) { return "应急通道" }
    if (order.priority >= 5) { return "标准通道" }
    return "低优先通道"
}

main() {
    let orders = [
        Order("O-301", 30.0, 9),
        Order("O-302", 20.0, 5),
        Order("O-303", 10.0, 2)
    ]

    let vehicle = Vehicle("V-01", 60.0)
    let futures = ArrayList<Future<Unit>>()
    let dispatchCount = AtomicInt64(0)
    let lock = Mutex()

    for (order in orders) {
        let f = spawn {
            synchronized(lock) {
                if (vehicle.canLoad(order.weight)) {
                    vehicle.load = vehicle.load + order.weight
                    dispatchCount.fetchAdd(1)
                    println("调度订单 ${order.id} -> ${decideLane(order)}")
                } else {
                    println("订单 ${order.id} 超载，进入人工复核")
                }
            }
        }
        futures.append(f)
    }

    for (f in futures) { f.get() }
    println("完成调度数: ${dispatchCount.load()}")
}
```

## 2. 复盘清单

*   是否记录了调度失败原因？
*   是否能追踪每条订单的状态流转？
*   是否能快速定位瓶颈与异常？

## 工程化提示

*   真实系统中需要分离读写线程，避免共享状态冲突。
*   调度失败要进入重试或人工复核队列。
*   综合演练要输出关键指标，便于复盘。

## 实践挑战

1. 为订单调度增加“失败重试一次”的逻辑。
2. 为每条订单输出 `traceId` 并保持一致。
