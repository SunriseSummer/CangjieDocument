# 创建 Struct 实例

创建结构体实例主要通过调用其构造函数。

## 1. 使用构造函数

如果在定义结构体时定义了 `init` 方法，就可以像调用函数一样创建实例。

<!-- verify -->
```cangjie
struct Color {
    let r: Int64
    let g: Int64
    let b: Int64

    public init(r: Int64, g: Int64, b: Int64) {
        this.r = r
        this.g = g
        this.b = b
    }
}

main() {
    let red = Color(255, 0, 0)
    println(red.r)
}
```

## 2. 主构造函数 (Primary Constructor)

仓颉提供了一种更简洁的写法，直接在结构体名后面定义参数，这会自动生成对应的成员变量和构造函数。

<!-- verify -->
```cangjie
struct User(let name: String, var age: Int64) {
    // 自动拥有 name 和 age 成员

    func printInfo() {
        println("${name} is ${age} years old")
    }
}

main() {
    let u = User("Alice", 30)
    u.printInfo()
}
```

这是定义简单数据容器（DTO）的首选方式。
