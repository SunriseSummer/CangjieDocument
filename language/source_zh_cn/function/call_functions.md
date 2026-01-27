# 调用函数

定义好函数后，可以通过函数名加上圆括号 `()` 来调用它。

## 1. 位置参数

这是最常见的调用方式，实参按照定义的顺序传递给形参。

<!-- verify -->
```cangjie
func sub(a: Int64, b: Int64) => a - b

main() {
    let result = sub(10, 5) // a=10, b=5
    println(result) // 5
}
```

## 2. 命名参数

调用时可以显式指定参数名，这样可以不按顺序传递，提高代码可读性。
要使用命名参数，定义函数时需要给参数指定**外部参数名**（或者直接使用变量名作为外部参数名，如果在变量名前加 `!` 则强制位置调用，或者不加特殊修饰则默认既可位置也可命名，具体视仓颉版本规则，这里以通用规则为准：参数默认即可位置也可命名）。

> **注意**: 在仓颉中，默认情况下，参数既可以使用位置参数调用，也可以使用命名参数调用。

<!-- verify -->
```cangjie
func connect(host: String, port: Int64) {
    println("Connecting to ${host}:${port}")
}

main() {
    // 混合使用
    connect("localhost", port: 8080)

    // 纯命名参数
    connect(port: 3306, host: "127.0.0.1")
}
```

## 3. 参数默认值

可以为函数参数提供默认值。调用时如果省略该参数，则使用默认值。

<!-- verify -->
```cangjie
func log(message: String, level: String = "INFO") {
    println("[${level}] ${message}")
}

main() {
    log("System starting...") // 使用默认 level="INFO"
    log("File not found", level: "ERROR") // 覆盖默认值
}
```

> **规则**: 拥有默认值的参数通常放在参数列表的末尾，以便于省略。
