# 09. 状态机：运单生命周期

> 运单从“创建”到“签收”要经历多个阶段，任何跳跃都会导致业务风险。状态机让流程稳定可控。

## 本章目标

*   用枚举表达有限状态集合。
*   使用模式匹配校验状态流转。
*   保证业务流程可追踪、可解释。

## 1. 状态定义

```cangjie
enum ShipmentState {
    | Created
    | Assigned(String)    // 指派车辆 ID
    | InTransit
    | Delivered(String)   // 签收人
    | Failed(String)
}
```

## 2. 状态流转

```cangjie
class ShipmentFlow {
    public func next(state: ShipmentState, action: String): ShipmentState {
        match ((state, action)) {
            case (Created, "assign") => Assigned("V-07")
            case (Assigned(_), "depart") => InTransit
            case (InTransit, "deliver") => Delivered("Receiver-A")
            case (_, "fail") => Failed("异常中断")
            case _ => state
        }
    }
}

main() {
    let flow = ShipmentFlow()
    var state = Created
    state = flow.next(state, "assign")
    state = flow.next(state, "depart")
    state = flow.next(state, "deliver")
}
```

## 语言特性与应用解读

带参数的枚举分支（如 `Assigned(String)`）让状态天然携带业务数据，避免额外的字段管理。
`match ((state, action))` 通过元组匹配把规则集中表达，使状态机更像一张规则表。
`case _ => state` 为兜底策略，保证未知动作不会破坏状态一致性。

## 工程化提示

*   状态流转建议集中管理，避免散落在各模块。
*   动作参数建议使用枚举，避免字符串拼写错误。
*   每一次状态变更应记录日志与时间戳。

## 实践挑战

1. 为状态机增加 `Returned` 状态与对应流转。
2. 把 `action` 改为枚举类型，提升可维护性。
