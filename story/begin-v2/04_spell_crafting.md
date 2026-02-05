# 第四章：符文工坊 (函数与闭包)

> 为了应对更高层的挑战，简单的平砍已经不够用了。你来到“符文工坊”，这里可以让你将复杂的魔法动作封装成“法术卷轴”（函数），并统一技能的输入/输出。

## 本章目标

*   掌握函数定义与参数返回值的写法。
*   理解高阶函数与闭包在自定义行为中的价值。
*   学会用函数封装重复逻辑，提升可维护性。

## 1. 铭刻法术 (定义函数)

你需要一个能计算伤害的法术。

```cangjie
// 定义法术：火球术
// 参数：基础伤害 (base), 增幅倍率 (multiplier)
// 返回：最终伤害
func castFireball(base: Int64, multiplier: Int64): Int64 {
    let totalDamage = base * multiplier
    println("🔥 火球术爆发！造成 ${totalDamage} 点伤害。")
    return totalDamage
}

main() {
    let dmg = castFireball(50, 2)
    println("怪物剩余 HP: ${100 - dmg}")
}
```

## 2. 魔法融合 (高阶函数)

工坊大师教给你一种秘术：将法术本身作为材料进行融合。

```cangjie
// 这是一个“法术增强器”，它接收一个具体的法术逻辑 (Func)
func amplifySpell(power: Int64, spell: (Int64) -> Int64): Int64 {
    println("✨ 正在注入魔力...")
    return spell(power) * 2 // 最终效果翻倍！
}

main() {
    // 现场创造一个闪电法术 (Lambda)
    let lightning = { power: Int64 =>
        println("⚡ 闪电链！")
        return power + 20
    }

    // 将闪电法术放入增强器
    let finalDmg = amplifySpell(100, lightning)
    println("最终伤害: ${finalDmg}")
}
```

现在，你可以随心所欲地组合和创造新的魔法了。

## 工程化提示

*   真实项目的技能/算法参数要有范围校验，避免异常值。
*   高阶函数签名尽量简洁清晰，避免调用侧困惑。
*   将通用计算抽离为独立函数，便于复用与测试。

## 小试身手

1. 编写 `castHeal` 治疗技能，并复用 `amplifySpell` 增强效果。
2. 为 `castFireball` 增加暴击概率参数，返回最终伤害。
