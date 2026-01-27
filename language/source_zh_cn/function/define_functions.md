# 定义函数

函数是执行特定任务的独立代码块。在仓颉中，使用 `func` 关键字定义函数。

## 1. 基本语法

```text
func 函数名(参数列表): 返回值类型 {
    函数体
}
```

- **参数列表**: 形如 `参数名: 类型`，多个参数用逗号分隔。
- **返回值类型**: 可省略。如果省略，且函数体没有 `return`，默认为 `Unit`。

<!-- compile -->
```cangjie
func add(a: Int64, b: Int64): Int64 {
    return a + b
}
```

## 2. 无返回值函数

如果函数不返回任何有意义的值，返回类型可以声明为 `Unit`，或者直接省略。

<!-- compile -->
```cangjie
func greet(name: String) {
    println("Hello, ${name}")
}

// 等价于
func greetExplicit(name: String): Unit {
    println("Hello, ${name}")
}
```

## 3. 函数体

函数体是一个代码块。如果函数有返回值，函数体内必须包含 `return` 表达式（除非是简单的单表达式函数，见下文）。

## 4. 简写语法

如果函数体只包含一个表达式，可以省略花括号 `{}` 和 `return`，直接使用 `=>`。

<!-- compile -->
```cangjie
func square(x: Int64) => x * x
```

这不仅简洁，而且非常适合定义简短的工具函数。
