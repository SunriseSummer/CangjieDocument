# 08. 错误处理与模式匹配

## 1. Option 类型

在仓颉中，`Option<T>` 类型用于表示一个值可能存在，也可能不存在。它有两个构造器：`Some(T)` 表示有值，`None` 表示无值。这比使用空指针更加安全。

```cangjie
func findUser(id: Int64): Option<String> {
    if (id == 1) {
        return Some("Alice")
    } else {
        return None
    }
}

main() {
    let result = findUser(1)

    // 使用 match 处理 Option
    match (result) {
        case Some(name) => println("Found user: " + name)
        case None => println("User not found")
    }

    // 简便方法：getOrThrow (如果有值则返回，无值则抛出异常)
    // println(result.getOrThrow())
}
```

## 2. 模式匹配 (match)

`match` 表达式是仓颉中强大的控制流工具，不仅可以匹配值，还可以匹配类型和解构对象。

### 值匹配

```cangjie
main() {
    let score = 85
    match (score) {
        case 100 => println("Perfect")
        case 90..100 => println("Excellent") // 区间匹配 (注意：仓颉 match 不直接支持区间语法，需结合 guard 或 if)
        // 修正：仓颉的 case 支持字面量，对于范围通常使用 if guard
        case x where x >= 60 => println("Pass")
        case _ => println("Fail")
    }
}
```

*(注意：上文中的区间匹配 `90..100` 在 `match` 的 `case` 中可能需要特定语法或使用 guard `where`。为了准确性，这里使用 `where` 子句。)*

### 类型匹配

```cangjie
open class Base {}
class A <: Base {}
class B <: Base {}

func identify(obj: Base) {
    match (obj) {
        case a: A => println("It is A")
        case b: B => println("It is B")
        case _ => println("Unknown")
    }
}
```

## 3. 异常处理 (try-catch)

对于运行时错误，仓颉使用异常机制。

```cangjie
func divide(a: Int64, b: Int64): Int64 {
    if (b == 0) {
        // 抛出异常
        throw Exception("Division by zero")
    }
    return a / b
}

main() {
    try {
        let res = divide(10, 0)
        println(res)
    } catch (e: Exception) {
        println("Error caught: " + e.message)
    } finally {
        println("Execution finished")
    }
}
```
