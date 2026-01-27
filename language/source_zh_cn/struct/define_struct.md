# 定义结构体 (Struct)

结构体 (`struct`) 是一种**值类型**的复合数据结构。它将相关的数据组合在一起，常用于表示轻量级的对象。

## 1. 基本定义

使用 `struct` 关键字定义。

```cangjie
struct Point {
    var x: Int64
    var y: Int64

    // 构造函数
    public init(x: Int64, y: Int64) {
        this.x = x
        this.y = y
    }
}
```

## 2. 成员变量与函数

结构体可以包含：
- **成员变量**: 存储数据。
- **成员函数**: 定义行为。
- **静态成员**: 属于结构体类型本身。

<!-- verify -->
```cangjie
struct Rectangle {
    let width: Int64
    let height: Int64

    // 成员函数
    func area(): Int64 {
        return width * height
    }
}

main() {
    let rect = Rectangle(10, 20)
    println(rect.area()) // 200
}
```

> **注意**: 结构体是值类型，不能继承，也不能被继承。
