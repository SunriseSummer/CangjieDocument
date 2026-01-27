# 02. 变量与基础类型

本节我们将学习如何在仓颉中定义变量以及常用的数据类型。

## 1. 变量定义

仓颉使用 `let` 定义不可变变量，使用 `var` 定义可变变量。

```cangjie
main() {
    let name = "Cangjie" // let 定义后不可修改
    var age = 1          // var 定义后可以修改

    // name = "New Name" // 编译错误！let 定义的变量不能重新赋值
    age = 2              // 正确

    println("Name: " + name)
    println("Age: " + age.toString())
}
```

## 2. 基础数据类型

仓颉是强类型语言，支持以下基础类型：

*   **整数**: `Int64`, `Int32`, `UInt64`, `UInt8` 等 (默认整数通过字面量推断为 `Int64`)。
*   **浮点数**: `Float64`, `Float32` (默认浮点数推断为 `Float64`)。
*   **布尔值**: `Bool` (取值为 `true` 或 `false`)。
*   **字符**: `Rune` (表示 Unicode 字符，使用单引号，如 `'a'`, `'中'`)。
*   **字符串**: `String` (表示文本，使用双引号，如 `"Hello"`)。

```cangjie
main() {
    let pi: Float64 = 3.14159
    let isActive: Bool = true
    let char: Rune = '仓'

    println(pi)
    println(char)
}
```

## 3. 类型推断

仓颉编译器具有强大的类型推断能力，在大多数情况下，你可以省略显式的类型标注，编译器会根据上下文自动推导出变量的类型。

```cangjie
let x = 100     // 自动推断为 Int64
let y = 3.14    // 自动推断为 Float64
let z = "Text"  // 自动推断为 String
```
