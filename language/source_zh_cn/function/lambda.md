# Lambda 表达式

Lambda 表达式是一种简洁的定义匿名函数的方式。它常用于作为参数传递给高阶函数（如 `map`, `filter`）。

## 1. 基本语法

```text
{ 参数 1, 参数 2, ... => 表达式 }
```

- 参数类型通常可以省略（由编译器推断）。
- 如果只有一个参数，参数列表可以省略。
- 返回值类型由表达式自动推断。

<!-- verify -->
```cangjie
main() {
    let add = { a: Int64, b: Int64 => a + b }
    println(add(1, 2)) // 3
}
```

## 2. 尾随 Lambda

如果函数的最后一个参数是函数类型，调用时可以将 Lambda 表达式写在圆括号外面。

<!-- verify -->
```cangjie
func repeat(times: Int64, action: () -> Unit) {
    for (i in 0..times) {
        action()
    }
}

main() {
    // 括号内调用
    repeat(3, { => println("Hi") })

    // 尾随 Lambda 写法 (推荐)
    repeat(3) {
        println("Hello")
    }
}
```

## 3. 省略参数

当 Lambda 只有一个参数且不需要显式使用参数名时，可以使用 `it`（视具体库支持）或上下文推断。但在仓颉的基础语法中，我们通常显式命名或使用 `_` 忽略。

<!-- compile -->
```cangjie
let arr = [1, 2, 3]
// 遍历数组
// arr.forEach { i => println(i) }
```
