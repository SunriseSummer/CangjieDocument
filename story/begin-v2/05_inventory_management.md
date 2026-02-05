# 第五章：背包系统 (结构体与类)

> 你的行囊里塞满了杂乱的物品。为了更好地管理装备和道具，你需要使用“空间魔法”来构建有序的背包系统。

## 本章目标

*   理解结构体与类在语义和使用场景上的差异。
*   学会通过初始化器与方法封装数据行为。
*   认识引用共享带来的状态变化。

## 1. 物品定义 (Struct)

普通的材料（如草药、矿石）是大量存在的，属性简单，适合用轻量级的 `struct`。

```cangjie
struct Material {
    let name: String
    var count: Int64

    public init(name: String, count: Int64) {
        this.name = name
        this.count = count
    }

    public func desc() {
        println("📦 材料: ${name} x${count}")
    }
}
```

## 2. 装备锻造 (Class)

传说级装备拥有独特的灵魂（引用），即使名字相同，它们也是独一无二的。

```cangjie
class Weapon {
    let name: String
    var durability: Int64 // 耐久度

    public init(name: String) {
        this.name = name
        this.durability = 100
    }

    public func attack() {
        if (durability > 0) {
            durability = durability - 10
            println("⚔️ ${name} 挥砍！(耐久剩余: ${durability})")
        } else {
            println("❌ ${name} 已损坏，无法攻击！")
        }
    }
}

main() {
    // 整理背包
    let herb = Material("月光草", 5)
    herb.desc()

    // 装备武器
    let excalibur = Weapon("誓约胜利之剑")
    excalibur.attack()
    excalibur.attack()

    // 引用特性：把剑借给队友
    let teamSword = excalibur
    teamSword.attack() // 队友用了一次

    // 再次检查自己的剑
    println("我的剑耐久: ${excalibur.durability}") // 变成了 70，因为是同一把剑
}
```

## 工程化提示

*   值类型适合“轻量数据”，引用类型适合“有生命周期的对象”。
*   对可变状态（如耐久）要明确更新路径，防止并发修改。
*   装备与材料的行为可分层设计，避免类职责过大。

## 小试身手

1. 为 `Weapon` 增加 `repair()` 方法，恢复部分耐久。
2. 新增 `Potion` 结构体，并写一个统一的 `printItem` 函数。
