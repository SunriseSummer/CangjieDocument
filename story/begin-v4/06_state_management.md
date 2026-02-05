# 第六章：状态管理 (枚举与模式匹配)

> Web 应用通常需要管理复杂的状态（如订单状态、用户登录态）。枚举和模式匹配是处理状态机的最佳利器。

## 本章目标

*   学会用枚举表达有限状态集合。
*   理解模式匹配在状态流转校验中的作用。
*   建立“合法流转 + 明确兜底”的状态机思维。

## 1. 状态定义 (Enum)

一个订单的生命周期。

```cangjie
enum OrderState {
    | Created
    | Paid(Float64) // 携带支付金额
    | Shipped(String) // 携带快递单号
    | Completed
    | Cancelled(String) // 携带取消原因
}
```

## 2. 状态流转 (Pattern Matching)

根据当前状态决定下一步操作，防止非法流转（例如从 Created 直接变 Completed）。

```cangjie
class OrderManager {
    public func process(state: OrderState) {
        match (state) {
            case Created =>
                println("订单已创建，等待支付...")

            case Paid(amount) =>
                println("订单已支付 ¥${amount}，准备发货...")

            case Shipped(trackingNo) =>
                println("订单已发货，单号: ${trackingNo}")

            case Completed =>
                println("订单完成。")

            case Cancelled(reason) =>
                println("订单取消，原因: ${reason}")
        }
    }

    // 状态机转换检查
    public func next(current: OrderState, action: String): OrderState {
        match ((current, action)) {
            // (当前状态, 动作) => 新状态
            case (Created, "pay") => Paid(100.0)
            case (Paid(_), "ship") => Shipped("SF123456")
            case (Shipped(_), "receive") => Completed
            case (_, "cancel") => Cancelled("用户主动取消")
            case _ =>
                println("❌ 非法状态流转！")
                current // 保持原状
        }
    }
}

main() {
    let manager = OrderManager()

    var state = Created
    manager.process(state)

    // 支付
    state = manager.next(state, "pay")
    manager.process(state)

    // 尝试非法操作：未发货直接收货
    state = manager.next(state, "receive")
}
```

## 工程化提示

*   状态机应集中管理流转规则，避免散落在多处业务逻辑。
*   对外暴露的动作建议使用枚举而不是字符串，减少拼写错误。
*   状态变更需要记录操作日志，便于审计与回溯。

## 小试身手

1. 增加 `Refunded` 状态，并补充对应流转逻辑。
2. 将 `action` 改为枚举类型，减少非法输入。
