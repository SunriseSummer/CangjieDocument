# 09. 并发编程：虚拟证券交易所

金融市场瞬息万变，成千上万的交易并发进行。如果处理不好并发，可能会导致“钱变负数”的灾难。本节我们用仓颉的 `spawn` (轻量级线程) 来模拟一个高频交易系统。

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
