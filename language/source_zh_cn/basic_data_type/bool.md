# 布尔类型

布尔类型 (`Bool`) 是逻辑运算的基础，用于表示“真”或“假”。

## 1. 字面量

布尔类型只有两个预定义的值：

- **`true`**: 表示真。
- **`false`**: 表示假。

<!-- compile -->
```cangjie
let isCangjieFun: Bool = true
let isCompleted = false
```

## 2. 逻辑运算

布尔类型支持标准的逻辑操作符，常用于条件判断（如 `if` 表达式）中。

| 操作符 | 描述 | 示例 | 结果 |
| :--- | :--- | :--- | :--- |
| **`!`** | **逻辑非** (Not) | `!true` | `false` |
| **`&&`** | **逻辑与** (And) | `true && false` | `false` |
| **`||`** | **逻辑或** (Or) | `true || false` | `true` |

此外，还支持比较操作符 `==` (等于) 和 `!=` (不等于)。

<!-- verify -->
```cangjie
main() {
    let a = true
    let b = false

    if (a && !b) {
        println("Logic check passed!")
    }
}
```
