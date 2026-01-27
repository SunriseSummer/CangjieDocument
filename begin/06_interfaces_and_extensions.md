# 06. 接口与扩展

## 1. 接口 (Interface)

接口定义了一组行为规范（方法签名），任何实现了该接口的类型都必须提供这些方法的具体实现。接口实现了多态。

```cangjie
// 定义接口
interface Printable {
    func printInfo(): Unit
}

// 类实现接口
class Book <: Printable {
    let title: String

    init(title: String) {
        this.title = title
    }

    // 实现接口方法
    public func printInfo() {
        println("Book: " + title)
    }
}

class Car <: Printable {
    let model: String

    init(model: String) {
        this.model = model
    }

    public func printInfo() {
        println("Car: " + model)
    }
}

main() {
    let items: Array<Printable> = [Book("Cangjie Guide"), Car("Tesla")]

    for (item in items) {
        item.printInfo() // 多态调用
    }
}
```

## 2. 扩展 (Extend)

扩展（Extensions）允许你向已有的类型（甚至是系统内置类型）添加新的功能，而无需修改原始源码。

```cangjie
// 为系统内置的 Int64 类型添加一个 square 方法
extend Int64 {
    func square(): Int64 {
        return this * this
    }
}

main() {
    let num = 5
    // 就像调用原生方法一样调用扩展方法
    println(num.square()) // 输出 25
}
```

扩展不仅可以添加方法，还可以让已有类型实现新的接口，极大增强了代码的灵活性。
