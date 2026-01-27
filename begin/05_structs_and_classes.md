# 05. 结构体与类：电商订单系统

在构建复杂系统（如淘宝、京东）时，我们需要精准地模拟现实世界的实体。结构体 (`struct`) 和类 (`class`) 是我们的基石。

## 1. 商品模型 (Struct - 值类型)

商品信息通常是静态的数据集合，适合用 `struct`。

```cangjie
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
    var items: Array<Product>
    var status: String

    public init(id: String) {
        this.orderId = id
        this.items = [] // 初始化空购物车
        this.status = "Pending"
    }

    // 添加商品
    public func addItem(p: Product) {
        items = Array<Product>(items.size + 1) { i =>
             if (i < items.size) items[i] else p
        } // 简化演示，实际应使用 ArrayList
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
