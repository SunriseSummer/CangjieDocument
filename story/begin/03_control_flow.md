# 03. 流程控制：猜数字游戏

光有数据是不够的，程序需要逻辑。本节我们通过编写一个“猜数字”游戏的逻辑核心，学习控制流，并体验“根据状态做决策”的过程。

## 本章目标

*   掌握 `if/else` 的条件分支与表达式化写法。
*   理解 `while`/`for` 循环与 `break`/`continue` 的控制方式。
*   学会用简单逻辑组织业务流程。

## 1. 游戏规则逻辑 (if-else)

我们需要根据玩家猜测的数字与目标数字的大小关系，给出提示，并明确每种提示对应的业务分支。

<!-- check:run -->
```cangjie
main() {
    let targetNumber = 42
    let playerGuess = 30 // 假设玩家输入了 30

    print("玩家猜了 ${playerGuess} -> ")

    if (playerGuess == targetNumber) {
        println("🎉 恭喜！猜对了！")
    } else if (playerGuess < targetNumber) {
        println("太小了，再试一次。")
    } else {
        println("太大了，再试一次。")
    }
}
```

<!-- expected_output:
玩家猜了 30 -> 太小了，再试一次。
-->

`if-else` 不仅可以控制流程，在仓颉中它还是表达式，可以直接返回值：

<!-- check:ast -->
```cangjie
let resultMsg = if (playerGuess == targetNumber) { "Win" } else { "Try Again" }
```

## 2. 持续挑战 (while 循环)

游戏通常不会猜一次就结束。我们需要一个循环，直到玩家猜对为止。为了演示，我们模拟几次猜测过程，并记录尝试次数。

<!-- check:run -->
```cangjie
main() {
    let target = 7
    var guess = 0
    var attempts = 0

    println("=== 游戏开始：目标数字是 0-10 之间 ===")

    // 模拟玩家猜测序列: 2, 9, 7
    let guesses = [2, 9, 7]
    var index = 0

    while (guess != target) {
        attempts = attempts + 1
        guess = guesses[index] // 模拟读取输入
        index = index + 1

        println("第 ${attempts} 次尝试: ${guess}")

        if (guess == target) {
            println("✅ 胜利！你用了 ${attempts} 次机会。")
            break // 跳出循环
        } else {
            println("❌ 错啦。")
        }
    }
}
```

## 3. 遍历道具 (for-in 循环)

在 RPG 游戏中，我们经常需要查看背包里的物品。

<!-- check:run -->
```cangjie
main() {
    // 定义一个区间，模拟背包格子编号
    println("检查背包格子 1 到 5:")

    for (slot in 1..=5) {
        // 偶数格子放药水，奇数格子放装备
        if (slot % 2 == 0) {
            println("格子 ${slot}: [生命药水]")
        } else {
            println("格子 ${slot}: [铁剑]")
        }
    }
}
```

*   `1..=5`: 表示闭区间 [1, 5]。
*   `break`: 提前结束循环。
*   `continue`: 跳过本次循环剩余代码，直接进入下一次。

通过这些控制流，你的程序开始具备了“思考”的能力。

## 工程化提示

*   条件判断建议写成“先处理异常/边界，再处理主流程”，降低分支复杂度。
*   循环中要明确退出条件，避免潜在的死循环。
*   对用户输入应增加校验与限制，保持流程稳定。

## 小试身手

1. 为猜数字逻辑添加“最多尝试次数”的限制。
2. 在遍历背包时统计药水和装备的数量，并输出汇总。
