# mut 函数

在结构体（值类型）中，默认情况下，成员函数是无法修改实例本身的成员变量的。如果需要修改，必须将函数标记为 `mut`。

## 1. 为什么需要 mut？

结构体是值类型，通常被视为不可变数据。为了安全起见，普通成员函数只能读取数据，不能修改。

## 2. 使用 mut 修饰符

在 `func` 关键字前加上 `mut`，允许函数修改 `this` 实例的成员。

<!-- verify -->
```cangjie
struct Counter {
    var count = 0

    // ❌ 错误：普通函数不能修改 count
    // func inc() { count++ }

    // ✅ 正确：mut 函数可以修改
    mut func inc() {
        count++
    }
}

main() {
    // 注意：必须是 var 变量才能调用 mut 方法
    var c = Counter()
    c.inc()
    println(c.count) // 1

    // let c2 = Counter()
    // c2.inc() // ❌ 错误：c2 是不可变的，不能调用 mut 方法
}
```

> **规则**: 只有当结构体实例本身被绑定为可变变量（`var`）时，才能调用其 `mut` 函数。
