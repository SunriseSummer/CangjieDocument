# 03. 调度规则：流程控制

> 星港的夜间订单优先级差异极大。高优先级货物必须优先出库，低优先级可以延后。你需要用流程控制写出清晰的调度规则。

## 本章目标

*   掌握 `if/else` 条件分支与循环控制。
*   让业务规则具备“可解释”的逻辑结构。
*   形成“先处理关键路径，再处理常规路径”的习惯。

## 1. 优先级规则

```cangjie
struct Order {
    let id: String
    let weight: Float64
    let priority: Int64
}

func decideLane(order: Order): String {
    if (order.priority >= 9) {
        return "应急通道"
    } else if (order.priority >= 5) {
        return "标准通道"
    } else {
        return "低优先通道"
    }
}
```

## 2. 批量调度

```cangjie
main() {
    let orders = [
        Order("O-001", 120.0, 10),
        Order("O-002", 40.0, 6),
        Order("O-003", 15.0, 3)
    ]

    for (order in orders) {
        let lane = decideLane(order)
        println("订单 ${order.id} -> ${lane}")
    }
}
```

## 语言特性与应用解读

`if/else` 在仓颉中可直接返回字符串，让规则函数保持“输入 -> 输出”的清晰映射。
数组字面量 `[]` 让样例数据创建更紧凑，配合类型推断简化测试用例。
`for (order in orders)` 基于可迭代协议遍历集合，使批量调度逻辑更易读。

## 工程化提示

*   条件判断应先处理异常或关键路径，减少分支嵌套。
*   批量规则建议抽成函数，避免主流程臃肿。
*   规则变更频繁时，可将阈值配置化。

## 实践挑战

1. 为低优先级订单添加“延迟出库”提示。
2. 在循环中统计进入“应急通道”的订单数量。
