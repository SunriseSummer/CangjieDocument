# 第六章：公会契约 (接口与扩展)

> 你来到了第 20 层的“冒险者公会”。这里汇聚了战士、法师、盗贼。公会发布任务时，不管你是什么职业，只要签了“契约”，就必须执行。

## 1. 签订契约 (Interface)

公会规定：所有战斗职业必须会“攻击”和“防御”。

```cangjie
interface Combatant {
    func attack(): Unit
    func defend(): Unit
}
```

## 2. 职业履行 (Implementation)

战士和法师用不同的方式履行契约。

```cangjie
class Warrior <: Combatant {
    public func attack() { println("战士: 强力重击！") }
    public func defend() { println("战士: 举盾格挡！") }
}

class Mage <: Combatant {
    public func attack() { println("法师: 炎爆术！") }
    public func defend() { println("法师: 寒冰护体！") }
}
```

## 3. 组队出征 (多态)

队长不需要知道你是谁，只要你是 `Combatant`，就可以加入队伍。

```cangjie
func startRaid(member: Combatant) {
    member.attack()
    member.defend()
}

main() {
    let arthur = Warrior()
    let merlin = Mage()

    println("--- 团队副本开始 ---")
    startRaid(arthur)
    startRaid(merlin)
}
```

## 4. 自身强化 (Extensions)

你发现自己的生命值显示不够直观。你决定给系统的整数类型加个“血条显示”功能。

```cangjie
extend Int64 {
    func showHP() {
        print("HP: [")
        for (i in 0..this/10) { print("█") }
        println("] ${this}")
    }
}

main() {
    let currentHP = 80
    currentHP.showHP() // 输出血条
}
```
