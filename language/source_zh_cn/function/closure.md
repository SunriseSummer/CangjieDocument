# 闭包 (Closure)

闭包是一个函数，它“捕获”了其定义环境中的变量。即使离开了定义它的作用域，闭包依然可以访问这些变量。

## 1. 变量捕获

当一个内部函数引用了外部函数的变量时，就形成了闭包。

<!-- verify -->
```cangjie
func makeCounter(): () -> Int64 {
    var count = 0
    // 返回一个闭包，捕获了 count
    return { =>
        count++
        count
    }
}

main() {
    let counter = makeCounter()
    println(counter()) // 1
    println(counter()) // 2

    let counter2 = makeCounter()
    println(counter2()) // 1 (新的独立计数器)
}
```

## 2. 捕获机制

- **引用捕获**: 闭包捕获的是变量的引用（对于局部变量），因此可以在闭包内修改变量的值（如上例中的 `count`），并且这种修改在闭包多次调用间是持久的。
- **值捕获**: 对于不可变数据，直接捕获其值。

> **💡 提示**: 闭包是实现数据封装和状态保持的强大工具，无需定义完整的类。
