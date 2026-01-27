# 05. 结构体与类

仓颉提供了 `struct` (值类型) 和 `class` (引用类型) 来构建自定义数据类型。

## 1. 结构体 (Struct)

结构体是值类型，通常用于表示轻量级的数据聚合。当结构体实例被赋值给新变量或作为参数传递时，会发生值拷贝。

```cangjie
struct Point {
    var x: Int64
    var y: Int64

    // 构造函数
    public init(x: Int64, y: Int64) {
        this.x = x
        this.y = y
    }

    // 成员函数
    public func printPos() {
        println("Position: (${x}, ${y})")
    }
}

main() {
    var p1 = Point(10, 20)
    var p2 = p1 // 值拷贝

    p2.x = 100

    p1.printPos() // 输出 (10, 20)，p1 不受影响
    p2.printPos() // 输出 (100, 20)
}
```

## 2. 类 (Class)

类是引用类型，支持继承和多态。当类实例被赋值时，传递的是引用（指针）。

```cangjie
// 定义父类，使用 open 允许被继承
open class Animal {
    var name: String

    public init(name: String) {
        this.name = name
    }

    // open 允许子类重写
    public open func speak() {
        println("Animal sound")
    }
}

// 定义子类
class Dog <: Animal {
    public init(name: String) {
        super(name)
    }

    // 重写父类方法
    public override func speak() {
        println(name + ": Woof!")
    }
}

main() {
    let dog = Dog("Buddy")
    dog.speak()
}
```

## 3. struct vs class 核心区别

| 特性 | struct | class |
| :--- | :--- | :--- |
| **类型** | 值类型 (Value Type) | 引用类型 (Reference Type) |
| **内存分配** | 通常在栈上 | 堆上 |
| **赋值行为** | 拷贝值 | 拷贝引用 |
| **继承** | 不支持 | 支持 |
| **用途** | 简单数据模型 | 复杂业务逻辑、对象体系 |
