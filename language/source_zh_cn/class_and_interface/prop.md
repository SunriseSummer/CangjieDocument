# 属性 (Property)

属性 (`prop`) 是一种特殊的成员，它结合了字段（存储）和方法（访问逻辑）的特性。在外部看来，访问属性就像访问普通变量一样，但内部实际上是调用了 getter 和 setter 方法。

## 1. 定义属性

属性通常定义在接口或抽象类中作为规范，或者在类中作为计算属性。

### 语法
```cangjie
prop 属性名: 类型 {
    get() { ... }
    set(value) { ... }
}
```

## 2. 示例：计算属性

<!-- verify -->
```cangjie
class Circle {
    var radius: Float64

    public init(r: Float64) {
        this.radius = r
    }

    // 定义 area 属性，它是只读的（只有 get）
    public prop area: Float64 {
        get() {
            return 3.14 * radius * radius
        }
    }
}

main() {
    let c = Circle(10.0)
    println(c.area) // 像访问变量一样访问，但实际执行了计算
    // c.area = 100.0 // ❌ 错误：没有 setter，无法赋值
}
```

## 3. 接口中的属性

在接口中，我们通常只声明属性要求，而不提供实现。

```cangjie
interface Named {
    prop name: String // 要求实现类必须有一个 name 属性
}
```
