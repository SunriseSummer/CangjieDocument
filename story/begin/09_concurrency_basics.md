# 09. 并发编程：虚拟证券交易所

金融市场瞬息万变，成千上万的交易并发进行。如果处理不好并发，可能会导致“钱变负数”的灾难。本节我们用仓颉的 `spawn` (轻量级线程) 来模拟一个高频行情采集与交易系统。

## 本章目标

*   理解并发任务的创建与结果获取方式。
*   认识共享状态的风险与原子操作的作用。
*   建立“并发需要明确同步策略”的工程意识。

## 1. 股票价格实时更新 (Spawn)

每个股票都是独立的实体，它的价格应该独立波动。

```cangjie
import std.time.*
import std.sync.*
import std.collection.*

// 模拟获取股票最新价格
func fetchStockPrice(stockCode: String): Float64 {
    // 模拟网络延迟
    sleep(Duration.millisecond * 200)
    // 模拟价格：随机波动 (这里简化为固定值演示)
    if (stockCode == "CJTech") { return 102.5 }
    if (stockCode == "BioHealth") { return 58.0 }
    return 0.0
}

main() {
    println("--- 交易所开市 ---")

    // 同时查询两只股票，互不阻塞
    let futureA = spawn { fetchStockPrice("CJTech") }
    let futureB = spawn { fetchStockPrice("BioHealth") }

    println("正在从远端服务器获取数据...")

    // 获取结果
    let priceA = futureA.get()
    let priceB = futureB.get()

    println("CJTech 当前价: $${priceA}")
    println("BioHealth 当前价: $${priceB}")
}
```

## 2. 账户余额安全 (Atomic)

假设有 100 个交易机器人同时操作同一个账户，如何保证余额不会出错？原子操作是关键。

```cangjie
main() {
    // 初始资金 1000 元
    let balance = AtomicInt64(1000)

    let robots = ArrayList<Future<Unit>>()

    println("初始余额: ${balance.load()}")

    // 启动 50 个机器人，每个机器人花掉 10 元
    for (i in 0..50) {
        let f = spawn {
            // 模拟交易耗时
            sleep(Duration.millisecond * 10)
            // 原子减法：安全！
            balance.fetchSub(10)
        }
        robots.append(f)
    }

    // 等待所有机器人完成
    for (f in robots) { f.get() }

    let finalBalance = balance.load()
    println("最终余额: ${finalBalance}")

    if (finalBalance == 500) {
        println("✅ 账目核对无误！")
    } else {
        println("❌ 严重事故：账目错误！")
    }
}
```

在没有原子操作的情况下，多个线程同时读取和修改余额，会导致严重的“竞态条件”。仓颉的 `Atomic` 类型帮我们规避了这一风险。

## 工程化提示

*   示例中的 `spawn`/`Future` API 以标准库定义为准，使用时应关注错误处理与超时。
*   不要在并发任务中访问不安全的共享可变数据，必要时使用锁或消息队列。
*   并发逻辑最好配合监控与告警，及时发现延迟与资源消耗问题。

## 小试身手

1. 为 `fetchStockPrice` 增加错误分支，并在主流程中输出失败原因。
2. 将账户余额逻辑改为“充值 + 扣款”混合，观察最终余额是否符合预期。
