# Match 表达式

`match` 是仓颉中强大的模式匹配工具，类似于其他语言的 `switch`，但功能更强。

## 1. 基本用法

`match` 将一个值与多个模式进行比较，并执行第一个匹配成功的分支。

<!-- verify -->
```cangjie
main() {
    let x = 1
    match (x) {
        case 1 => println("One")
        case 2 => println("Two")
        case _ => println("Other") // 通配符，匹配所有其他情况
    }
}
```

> **注意**: `match` 是表达式，可以返回值。

## 2. 模式匹配枚举

`match` 最常用于解构枚举类型，特别是携带数据的枚举。

<!-- verify -->
```cangjie
enum Result {
    Success(Int64) | Failure(String)
}

main() {
    let res = Result.Success(100)

    match (res) {
        case Success(val) => println("Got value: ${val}")
        case Failure(err) => println("Error: ${err}")
    }
}
```

## 3. 模式守卫 (Pattern Guard)

可以在模式后面加上 `where` 子句，进行更细粒度的条件判断。

```cangjie
match (x) {
    case i where i > 0 => println("Positive")
    case i where i < 0 => println("Negative")
    case _ => println("Zero")
}
```

## 4. 类型匹配

`match` 还可以用于检查值的运行时类型。

```cangjie
match (obj) {
    case s: String => println("It's a string: ${s}")
    case i: Int64 => println("It's an integer: ${i}")
    case _ => println("Unknown type")
}
```
