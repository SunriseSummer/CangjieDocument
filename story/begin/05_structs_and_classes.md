# 05. 结构体与类：电商订单系统

在构建复杂系统（如淘宝、京东）时，我们需要精准地模拟现实世界的实体。结构体 (`struct`) 和类 (`class`) 是我们的基石。

## 本章目标

*   理解值类型与引用类型的语义差异。
*   学会用 `struct`/`class` 建模业务实体。
*   认识封装与初始化在工程中的必要性。

## 1. 商品模型 (Struct - 值类型)

商品信息通常是静态的数据集合，适合用 `struct`。

```cangjie
import std.collection.*

struct Product {
    let id: Int64
    let name: String
    var price: Float64 // 价格可能会变

    public init(id: Int64, name: String, price: Float64) {
        this.id = id
        this.name = name
        this.price = price
    }

    public func display() {
        println("[商品 #${id}] ${name} - ¥${price}")
    }
}
```

## 2. 订单系统 (Class - 引用类型)

订单需要被追踪、状态需要被修改，且可能涉及复杂的业务逻辑，适合用 `class`。

```cangjie
class Order {
    let orderId: String
    var items: ArrayList<Product>
    var status: String

    public init(id: String) {
        this.orderId = id
        this.items = ArrayList<Product>() // 初始化空购物车
        this.status = "Pending"
    }

    // 添加商品
    public func addItem(p: Product) {
        items.append(p)
        println("已添加: ${p.name}")
    }

    // 结账
    public func checkout() {
        var total = 0.0
        for (item in items) {
            total = total + item.price
        }
        this.status = "Paid"
        println("订单 ${orderId} 支付成功！总计: ¥${total}")
    }
}

main() {
    // 1. 上架商品
    let p1 = Product(101, "机械键盘", 399.0)
    let p2 = Product(102, "人体工学椅", 1299.0)

    // 2. 用户下单
    let myOrder = Order("ORD-2024-001")
    myOrder.addItem(p1)
    myOrder.addItem(p2)

    // 3. 支付
    myOrder.checkout()
}
```

通过区分值类型（数据）和引用类型（行为实体），我们构建了一个清晰的业务模型。

## 工程化提示

*   数据对象尽量保持不可变，减少并发与状态共享带来的复杂度。
*   类的职责保持单一，避免“万能类”导致维护困难。
*   订单类示例采用 `ArrayList` 管理商品，实际工程可按容量与并发需求选择更合适的数据结构。

## 小试身手

1. 为 `Order` 增加 `cancel()` 方法，并更新订单状态。
2. 为 `Product` 增加库存字段，并在 `addItem` 时做库存校验。
