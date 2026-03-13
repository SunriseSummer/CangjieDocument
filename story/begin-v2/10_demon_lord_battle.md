# 第十章：决战魔王 (综合实战)

> 终于，你来到了第 100 层。魔王"Bug"端坐在王座之上。它拥有无穷的血量和变幻莫测的攻击。你需要运用你学到的所有知识——结构体、集合、并发、策略——来编写一个自动战斗系统击败它，并持续记录关键战斗指标。

## 本章目标

*   综合运用并发、集合与结构体构建完整场景。
*   理解共享状态的同步策略与日志记录方式。
*   体验从"模型设计"到"流程编排"的完整闭环。

## 1. 战场模拟系统

我们需要模拟一场宏大的 Boss 战。
*   **Boss**: 拥有海量 HP，会随机释放技能。
*   **Hero Party**: 一个英雄小队，并发进行攻击。
*   **Log System**: 记录战斗日志。

<!-- check:run -->
```cangjie
import std.sync.*
import std.collection.*

// === 1. 实体定义 ===

class Boss {
    let name: String
    var hp: AtomicInt64 // 线程安全的血量

    public init(name: String, maxHp: Int64) {
        this.name = name
        this.hp = AtomicInt64(maxHp)
    }

    public func takeDamage(amount: Int64) {
        let current = hp.fetchSub(amount)
        if (current > 0) {
            // 简单的血量条打印逻辑 (模拟)
            // print("Boss 受伤: -${amount}\n")
        }
    }

    public func isDead(): Bool {
        return hp.load() <= 0
    }
}

struct Skill {
    let name: String
    let damage: Int64
    let castTime: Int64 // 毫秒

    public init(name: String, damage: Int64, castTime: Int64) {
        this.name = name
        this.damage = damage
        this.castTime = castTime
    }
}

// === 2. 英雄行为 (并发任务) ===

func heroAction(name: String, boss: Boss, skills: Array<Skill>) {
    while (!boss.isDead()) {
        // 简单模拟随机选择技能 (这里固定轮询)
        for (skill in skills) {
            if (boss.isDead()) { break }

            // 模拟吟唱
            sleep(Duration.millisecond * skill.castTime)

            // 造成伤害
            boss.takeDamage(skill.damage)
            println("⚔️ [${name}] 释放了 [${skill.name}]! Boss 剩余 HP: ${boss.hp.load()}")

            // 模拟技能冷却
            sleep(Duration.millisecond * 200)
        }
    }
    println("🏆 [${name}] 停止攻击，胜利在望！")
}

// === 3. 战斗主循环 ===

main() {
    println("🔥 最终决战开始！挑战魔王 Bug 🔥")

    let demonLord = Boss("魔王 Bug", 5000)

    // 定义技能库
    let warriorSkills = [Skill("烈火剑", 150, 500), Skill("旋风斩", 100, 300)]
    let mageSkills = [Skill("炎爆", 300, 1000), Skill("冰枪", 80, 200)]

    // 组建小队 (并发)
    let partyFutures = ArrayList<Future<Unit>>()

    // 战士进场
    partyFutures.add(spawn { heroAction("亚瑟", demonLord, warriorSkills) })

    // 法师进场
    partyFutures.add(spawn { heroAction("梅林", demonLord, mageSkills) })

    // 射手进场
    partyFutures.add(spawn {
        heroAction("罗宾", demonLord, [Skill("连射", 50, 100)])
    })

    // 监控战斗
    while (!demonLord.isDead()) {
        sleep(Duration.second)
        println("... 战斗激烈进行中 ...")
    }

    // 等待所有英雄收刀
    for (f in partyFutures) { f.get() }

    println("\n🎆🎆🎆 恭喜！魔王已被击败！ 🎆🎆🎆")
    println("你已成功登顶仓颉魔塔。")
    println("但这只是开始，更广阔的编程世界在等着你。")
}
```

## 终章：新的旅途

你看着魔王倒下，手中的代码法杖发出了耀眼的光芒。
你不再是那个站在塔底的懵懂新手，你已经掌握了：
*   **变量与类型** (属性)
*   **流程控制** (战术)
*   **函数与类** (法术与装备)
*   **集合与泛型** (图鉴)
*   **并发编程** (分身术)

带上这份智慧，去创造属于你的世界吧！

## 工程化提示

*   实际战斗系统会有更复杂的状态机与伤害计算，本例仅示意流程。
*   并发写日志容易产生交错输出，建议使用统一的日志管道。
*   随机数、技能冷却等依赖库需以标准库实现为准。

## 小试身手

1. 为 `Boss` 增加阶段状态（如 70%/30% 血量触发新技能）。
2. 将英雄技能列表抽取为配置结构，并在主流程中加载。
