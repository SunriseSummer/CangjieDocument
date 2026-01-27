# 表达式

在仓颉编程语言中，**表达式 (Expression)** 是构建程序逻辑的核心。仓颉秉持“一切皆表达式”的理念，不仅传统的算术运算（如 `1 + 2`）是表达式，连 `if`、`while` 等控制流结构也是表达式，它们不仅执行动作，还可以返回值。

## 1. 代码块 (Block)

由一对花括号 `{}` 包围的一组语句称为**代码块**。
- **求值规则**: 代码块的值是其中**最后一个表达式**的值。
- **空块**: 如果代码块为空或最后一条语句没有返回值（如赋值语句），则代码块的值为 `()` (Unit 类型)。

<!-- compile -->
```cangjie
let val = {
    let a = 1
    let b = 2
    a + b // 代码块的值是 3
}
```

## 2. 条件表达式: if

`if` 表达式用于基于条件的分支执行。

### 基本用法
```cangjie
if (条件) {
    // 条件为 true 时执行
} else {
    // 条件为 false 时执行
}
```

### 作为表达式求值
由于 `if` 是表达式，它可以直接用于赋值。此时，所有分支的返回值类型必须兼容（拥有共同的父类型）。

<!-- verify -->
```cangjie
main() {
    let score = 85
    // if 表达式的值赋给 level
    let level = if (score >= 90) {
        "A"
    } else if (score >= 60) {
        "B"
    } else {
        "C"
    }
    println("Level: ${level}")
}
```

> **注意**: 如果 `if` 表达式用于赋值，必须包含 `else` 分支，以确保在所有情况下都有返回值。如果不包含 `else`，其类型默认为 `Unit`。

## 3. 循环表达式

仓颉提供了三种主要的循环结构：`while`、`do-while` 和 `for-in`。它们的返回值类型通常是 `Unit`。

### while 循环
先检查条件，为真则执行循环体。

```cangjie
var i = 0
while (i < 3) {
    println(i)
    i++
}
```

### do-while 循环
先执行一次循环体，再检查条件。保证循环体至少执行一次。

```cangjie
var i = 0
do {
    println(i)
    i++
} while (i < 3)
```

### for-in 循环
用于遍历序列（如区间、数组等实现了 `Iterable` 接口的类型）。

<!-- verify -->
```cangjie
main() {
    // 遍历区间 1 到 5 (包含 1 和 5)
    for (i in 1..=5) {
        print("${i} ")
    }
    println("")

    // 遍历数组
    let names = ["Alice", "Bob"]
    for (name in names) {
        println("Hello, ${name}")
    }
}
```

#### where 条件子句
`for-in` 循环支持 `where` 子句，用于在进入循环体前过滤元素，使代码更简洁。

<!-- verify -->
```cangjie
main() {
    // 只打印偶数
    for (i in 1..=10 where i % 2 == 0) {
        println(i)
    }
}
```

## 4. 跳转表达式

- **break**: 立即终止当前循环。
- **continue**: 跳过本次循环剩余部分，进入下一次迭代。

<!-- verify -->
```cangjie
main() {
    for (i in 1..=5) {
        if (i == 3) {
            continue // 跳过 3
        }
        if (i == 5) {
            break    // 到 5 停止
        }
        println(i)
    }
}
```
输出:
```text
1
2
4
```
