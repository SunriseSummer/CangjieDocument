# Option 类型

`Option<T>` 是仓颉标准库中内置的一个枚举类型，用于表示“一个值可能存在，也可能不存在”的情况。它是仓颉处理空值安全的主要机制，替代了其他语言中容易导致错误的 `null`。

## 1. 定义

`Option` 本质上是一个简单的枚举：

```cangjie
enum Option<T> {
    Some(T) | None
}
```

- **`Some(T)`**: 包含一个类型为 `T` 的值。
- **`None`**: 表示没有值。

## 2. 创建 Option

<!-- verify -->
```cangjie
main() {
    let a: Option<Int64> = Some(10)
    let b: Option<Int64> = None
    println(a.getOrThrow())
}
```

## 3. 使用 Option

通常不需要直接使用 `match` 来解构 `Option`，仓颉提供了一些便捷的操作符和方法。

### 使用 `??` (Coalescing)
如果 `Option` 是 `None`，则提供一个默认值。

```cangjie
let val = someOption ?? 0 // 如果 someOption 是 None，val 就是 0
```

### 使用 `?.` (Safe Call)
如果对象存在则调用成员，如果不存在（None）则不调用并返回 None。

### 使用 `if-let` 解构
这种语法糖允许我们仅在值存在时执行代码。

<!-- verify -->
```cangjie
main() {
    let opt = Some("Cangjie")

    if (let Some(name) <- opt) {
        println("Hello, ${name}")
    } else {
        println("No name provided")
    }
}
```

## 4. 获取值

- **`getOrThrow()`**: 如果是 `Some` 返回值，如果是 `None` 抛出异常。
- **`getOrDefault(default)`**: 类似 `??` 操作符。

> **💡 最佳实践**: 尽量避免直接使用 `getOrThrow()`，推荐使用 `match`、`if-let` 或 `??` 来安全地处理空值。
