# 02. 领域建模：订单、车辆与仓库

> 调度系统的核心是“看清楚对象”。订单有什么属性？车辆能装多少货？仓库如何表示？建模越清晰，规则越稳固。

## 本章目标

*   用 `struct`/`class` 描述核心业务实体。
*   理解值类型与引用类型的适用场景。
*   将业务语义转化为清晰的数据结构。

## 1. 订单与车辆模型

```cangjie
struct Order {
    let id: String
    let weight: Float64
    let priority: Int64

    public init(id: String, weight: Float64, priority: Int64) {
        this.id = id
        this.weight = weight
        this.priority = priority
    }
}

class Vehicle {
    let id: String
    var capacity: Float64
    var load: Float64

    public init(id: String, capacity: Float64) {
        this.id = id
        this.capacity = capacity
        this.load = 0.0
    }

    public func canLoad(weight: Float64): Bool {
        return load + weight <= capacity
    }
}
```

## 2. 仓库信息

```cangjie
struct Warehouse {
    let code: String
    let region: String
    let slots: Int64
}
```

代码要点：

`struct` 适合描述“不可变快照”，复制后不会共享状态，避免订单数据被意外篡改。
`class Vehicle` 作为引用类型，可以在多个模块中共享同一辆车的状态，`var load` 体现了可变业务属性。
`public init` 与 `this` 的组合，让构造流程清晰、可读，便于统一校验逻辑。

## 工程化提示

*   订单属于“数据快照”，适合用 `struct` 保持不可变。
*   车辆是有生命周期的状态对象，适合用 `class` 管理。
*   字段命名要保持一致（如 `capacity`、`load`），避免歧义。

## 实践挑战

1. 为 `Order` 增加 `deadline` 字段（字符串占位即可）。
2. 为 `Vehicle` 增加 `assign(order: Order)` 方法，更新 `load`。
