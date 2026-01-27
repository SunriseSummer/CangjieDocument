# 03. 流程控制

本节介绍仓颉语言中的流程控制语句：条件判断和循环。

## 1. 条件表达式 (if-else)

在仓颉中，`if-else` 不仅仅是语句，更是表达式，这意味着它有返回值。

```cangjie
main() {
    let score = 85

    if (score >= 60) {
        println("及格")
    } else {
        println("不及格")
    }

    // if-else 作为表达式使用，直接将结果赋值给变量
    let result = if (score >= 60) "Pass" else "Fail"
    println(result)
}
```

> 注意：`if` 条件必须是 `Bool` 类型。

## 2. 循环结构

### while 循环

`while` 循环在条件为真时重复执行代码块。

```cangjie
main() {
    var i = 0
    while (i < 3) {
        println("While loop: " + i.toString())
        i = i + 1
    }
}
```

### for-in 循环

`for-in` 循环用于遍历区间、数组或其他可迭代对象。

```cangjie
main() {
    // 遍历 0 到 4 (左闭右开区间 0..5)
    for (i in 0..5) {
        println("Index: " + i.toString())
    }

    // 遍历 1 到 3 (左闭右闭区间 1..=3)
    for (i in 1..=3) {
        println("Count: " + i.toString())
    }
}
```

## 3. 跳转语句

*   `break`: 立即跳出当前循环。
*   `continue`: 跳过本次循环的剩余部分，直接开始下一次迭代。

```cangjie
main() {
    for (i in 0..10) {
        if (i == 2) {
            continue // 跳过 2
        }
        if (i > 4) {
            break // 大于 4 时停止
        }
        println(i)
    }
}
```
