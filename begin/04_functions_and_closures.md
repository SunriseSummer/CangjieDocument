# 04. 函数与闭包

函数是组织代码的基本单元，而闭包（Lambda 表达式）则提供了强大的函数式编程能力。

## 1. 定义函数

使用 `func` 关键字定义函数。函数可以指定参数和返回值类型。如果函数没有返回值，返回类型为 `Unit`（通常可以省略）。

```cangjie
// 定义一个求和函数
func add(a: Int64, b: Int64): Int64 {
    return a + b
}

main() {
    let sum = add(3, 5)
    println("Sum: " + sum.toString())
}
```

### 命名参数

在仓颉中，你可以定义命名参数，使函数调用更加清晰。

```cangjie
func greet(name: String, message: String) {
    println("${name} says: ${message}")
}

main() {
    // 调用时按位置传递
    greet("Alice", "Hello World")
}
```

## 2. Lambda 表达式 (闭包)

Lambda 表达式是一种匿名函数，可以直接赋值给变量或作为参数传递。语法为 `{ 参数 => 函数体 }`。

```cangjie
main() {
    // 定义一个 Lambda
    let sayHi = { name: String =>
        println("Hi, " + name)
    }

    sayHi("Bob")
}
```

### 尾随 Lambda

如果函数的最后一个参数是函数类型，可以将 Lambda 表达式写在括号外面。这在编写类似 DSL（领域特定语言）的代码时非常有用。

```cangjie
// 接受一个函数作为参数
func repeatAction(times: Int64, action: (Int64) -> Unit) {
    for (i in 0..times) {
        action(i)
    }
}

main() {
    // 尾随 Lambda 写法
    repeatAction(3) { i =>
        println("Action executed: " + i.toString())
    }
}
```
