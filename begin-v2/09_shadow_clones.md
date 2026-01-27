# 第九章：影分身之术 (并发编程)

> 第 90 层是无尽的回廊。为了在规定时间内通过，你学会了“影分身之术” (Spawn)。你可以同时派出多个分身去探索不同的房间。

## 1. 派出分身 (Spawn)

你需要同时探索“左边房间”和“右边房间”。

```cangjie
import std.time.*
import std.sync.*

// 探索任务
func explore(roomName: String): Int64 {
    println("👻 分身进入了 [${roomName}]...")
    sleep(Duration.millisecond * 500) // 模拟探索耗时
    println("👻 [${roomName}] 探索完毕！")
    return 100 // 获得经验值
}

main() {
    println("本体：开始结印！影分身之术！")

    // 两个分身同时出发，不会阻塞本体
    let cloneA = spawn { explore("左室") }
    let cloneB = spawn { explore("右室") }

    println("本体：在原地休息喝茶...")

    // 回收分身（获取结果）
    let expA = cloneA.get()
    let expB = cloneB.get()

    println("本体：分身回归。获得总经验: ${expA + expB}")
}
```

## 2. 共享能量库 (Atomic)

你的所有分身共享同一个能量池。如果它们同时抽取能量，可能会导致能量紊乱。你需要“原子护盾”来保护能量池。

```cangjie
import std.sync.*
import std.collection.*

main() {
    // 共有能量：1000 点
    let energyPool = AtomicInt64(1000)
    let clones = ArrayList<Future<Unit>>()

    println("初始能量: ${energyPool.load()}")

    // 10 个分身同时释放技能
    for (i in 0..10) {
        let f = spawn {
            // 安全地扣除 50 点能量
            energyPool.fetchSub(50)
        }
        clones.append(f)
    }

    // 等待所有分身施法完毕
    for (f in clones) { f.get() }

    println("剩余能量: ${energyPool.load()}") // 应该是 500
}
```
