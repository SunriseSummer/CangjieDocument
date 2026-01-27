# Unit 类型

`Unit` 类型表示“无意义的值”或“无返回值”。它类似于其他语言中的 `void`，但在仓颉中，它是一个真正的类型。

## 1. 唯一值

`Unit` 类型只有一个值，写作 `()`。

<!-- compile -->
```cangjie
let u: Unit = ()
```

## 2. 使用场景

### 函数无返回值
当一个函数不需要返回任何数据时，其返回类型就是 `Unit`。通常可以省略返回类型标注。

```cangjie
func log(msg: String): Unit { // : Unit 可以省略
    println(msg)
    // 隐式 return ()
}
```

### 表达式求值
某些表达式（如赋值表达式、循环表达式）的值固定为 `()`。

<!-- verify -->
```cangjie
main() {
    let a = 1
    let result = (a = 2) // result 的类型是 Unit，值为 ()
    println(result)      // 输出 ()
}
```
