# 第七章：怪物图鉴 (集合与泛型)

> 你击败的怪物越来越多，记忆已经不够用了。你需要一本魔法图鉴（Collection）来记录它们，并能快速按层数、类型检索。为了让图鉴能记录各种奇奇怪怪的生物，你需要用到“万能容器”（Generics）。

## 本章目标

*   认识泛型在复用数据结构中的价值。
*   熟悉哈希表与动态数组的使用场景。
*   学会根据访问模式选择合适容器。

## 1. 万能笼子 (Generic Class)

你想要一个笼子，既能关住“哥布林”，也能关住“巨龙”。

```cangjie
class Cage<T> {
    var content: Option<T> = None

    public func capture(monster: T) {
        content = Some(monster)
        println("捕获成功！笼子里现在有东西了。")
    }

    public func release() {
        content = None
        println("笼子已清空。")
    }
}

struct Goblin { let name = "小哥布林" }
struct Dragon { let name = "红龙" }

main() {
    // 制造一个关哥布林的笼子
    let smallCage = Cage<Goblin>()
    smallCage.capture(Goblin())

    // 制造一个关龙的笼子
    let hugeCage = Cage<Dragon>()
    hugeCage.capture(Dragon())
}
```

## 2. 怪物分布图 (HashMap)

你需要知道每层塔分布着什么怪物。

```cangjie
import std.collection.*

main() {
    // Key: 层数 (Int64), Value: 怪物名 (String)
    let towerMap = HashMap<Int64, String>()

    towerMap[1] = "史莱姆"
    towerMap[10] = "骷髅王"
    towerMap[50] = "炎魔"

    let currentLevel = 10
    if (towerMap.contains(currentLevel)) {
        println("警报！第 ${currentLevel} 层探测到: ${towerMap[currentLevel]}")
    }
}
```

## 3. 猎杀清单 (ArrayList)

公会发布了今日悬赏，这是一个动态变化的列表。

```cangjie
import std.collection.*

main() {
    let bountyList = ArrayList<String>()

    bountyList.append("吸血鬼")
    bountyList.append("狼人")

    println("今日任务: ${bountyList.size} 个")

    // 完成了一个
    println("击杀: " + bountyList[0])
    bountyList.remove(0)

    println("剩余任务: ")
    for (target in bountyList) {
        println("- " + target)
    }
}
```

## 工程化提示

*   容器的访问复杂度不同，查询频繁的数据适合用哈希表。
*   示例集合 API 以标准库实现为准，实际项目请参考官方文档。
*   为集合操作编写单元测试，避免边界错误。

## 小试身手

1. 为 `Cage` 增加 `isEmpty()` 方法，并在释放后判断状态。
2. 统计 `bountyList` 中任务数量，并输出剩余奖励总数。
