# 函数概述

函数是代码复用和逻辑封装的基本单元。在仓颉中，函数不仅是组织代码的方式，更是一等公民（First-class citizen），可以作为参数传递、作为返回值返回，支持闭包、Lambda 表达式等高级特性。

## 定义函数

使用 `func` 关键字定义函数。

```text
func 函数名(参数列表): 返回值类型 {
    函数体
}
```

### 示例

<!-- compile -->
```cangjie
// 定义一个简单的加法函数
func add(a: Int64, b: Int64): Int64 {
    return a + b
}

// 如果函数没有返回值，返回类型可以写为 Unit 或省略
func sayHello(name: String) {
    println("Hello, ${name}")
}
```

## 深入学习

仓颉的函数特性非常丰富，包含以下核心内容：

- **[定义函数](../function/define_functions.md)**: 详细的参数、返回值语法。
- **[调用函数](../function/call_functions.md)**: 命名参数、参数默认值等调用方式。
- **[一等公民](../function/first_class_citizen.md)**: 函数作为变量和值。
- **[Lambda 表达式](../function/lambda.md)**: 简洁的匿名函数写法。
- **[闭包](../function/closure.md)**: 捕获上下文变量的函数。
- **[函数重载](../function/function_overloading.md)**: 同名不同参的函数定义。

请点击上述链接深入了解函数的强大功能。
