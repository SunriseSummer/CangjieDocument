# Nothing 类型

`Nothing` 是一个特殊的底层类型，表示“永远不会有结果”或“死胡同”。

## 1. 含义

`Nothing` 类型**没有值**。如果一个表达式的类型是 `Nothing`，说明代码执行到这里时，程序的正常控制流会被切断（例如抛出了异常、死循环、或退出了程序）。

## 2. 常见场景

### 抛出异常
`throw` 表达式的类型是 `Nothing`。

```cangjie
func error(): Nothing {
    throw Exception("Error")
}
```

### 控制流跳转
`return`、`break`、`continue` 表达式的类型也是 `Nothing`。

### 为什么需要它？
`Nothing` 是所有类型的**子类型**。这意味着它可以出现在任何需要具体类型的地方，而不会违反类型检查。

<!-- verify -->
```cangjie
main() {
    let x: Int64 = if (true) {
        100
    } else {
        throw Exception("Oops") // throw 类型是 Nothing，它是 Int64 的子类型，所以合法
    }
}
```

在上面的例子中，`if` 的一个分支返回 `Int64`，另一个分支是 `Nothing`。因为 `Nothing` 是 `Int64` 的子类型，所以整个 `if` 表达式的类型被推断为 `Int64`，编译可以通过。
