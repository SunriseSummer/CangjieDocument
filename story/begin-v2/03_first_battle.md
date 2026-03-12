# 第三章：初次试炼 (流程控制)

> 你遇到了第一只怪物——史莱姆。它挡在通往下一层的楼梯口。你需要根据战况做出决策：攻击、防御还是逃跑？这就是"条件分支"在策略中的体现。

## 本章目标

*   掌握条件分支与循环控制的基础语法。
*   理解 `break`/`continue` 在战斗流程中的作用。
*   学会用逻辑表达清晰的游戏规则。

## 1. 战斗决策 (if-else)

史莱姆看起来很弱，但也可能暗藏杀机。你需要判断它的颜色。

<!-- check:run -->
```cangjie
main() {
    let slimeColor = "Red" // 红色史莱姆是狂暴的

    print("前方发现一只 ${slimeColor} 史莱姆！行动: ")

    if (slimeColor == "Red") {
        println("🔥 释放火球术！(它看起来怕火)")
    } else if (slimeColor == "Blue") {
        println("❄️ 释放冰冻术！")
    } else {
        println("⚔️ 直接物理攻击！")
    }
}
```
<!-- expected_output:
前方发现一只 Red 史莱姆！行动: 🔥 释放火球术！(它看起来怕火)
-->

## 2. 持续战斗 (while 循环)

一只史莱姆倒下了，但更多的史莱姆涌了上来。你需要战斗直到它们全部消失。

<!-- check:run -->
```cangjie
main() {
    var slimeCount = 3
    var energy = 100

    println("=== 遭遇史莱姆群！数量: ${slimeCount} ===")

    while (slimeCount > 0) {
        if (energy < 10) {
            println("⚠️ 精力耗尽！必须逃跑！")
            break
        }

        println("⚔️ 击败一只史莱姆！")
        slimeCount = slimeCount - 1
        energy = energy - 30
    }

    if (slimeCount == 0) {
        println("🎉 战斗胜利！前往下一层。")
    }
}
```
<!-- expected_output:
=== 遭遇史莱姆群！数量: 3 ===
⚔️ 击败一只史莱姆！
⚔️ 击败一只史莱姆！
⚔️ 击败一只史莱姆！
🎉 战斗胜利！前往下一层。
-->

## 3. 搜刮战利品 (for-in 循环)

战斗结束后，地上掉落了几个宝箱。你需要逐一打开它们。

<!-- check:run -->
```cangjie
main() {
    println("=== 搜刮战利品 ===")
    // 宝箱编号 1 到 3
    for (boxId in 1..=3) {
        // 偶数宝箱通常有陷阱，跳过
        if (boxId % 2 == 0) {
            println("宝箱 ${boxId}: 感觉有诈，跳过。")
            continue
        }
        println("宝箱 ${boxId}: 获得 [生命药水]！")
    }
}
```
<!-- expected_output:
=== 搜刮战利品 ===
宝箱 1: 获得 [生命药水]！
宝箱 2: 感觉有诈，跳过。
宝箱 3: 获得 [生命药水]！
-->
通过逻辑控制，你成功通过了初次试炼。

## 工程化提示

*   复杂判断可以先提取为布尔变量，提高可读性。
*   循环前务必明确退出条件，避免"无限战斗"。
*   对用户输入的选项要做校验，避免异常路径。

## 小试身手

1. 为战斗循环增加"药水恢复"分支，并在能量过低时触发。
2. 将战利品掉落改为数组遍历，并统计总价值。
