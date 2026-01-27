# 枚举类型 (Enum)

枚举 (`enum`) 是仓颉中的一种代数数据类型（ADT）。它不仅可以定义一组常量，还可以携带关联数据。

## 1. 基本枚举

最简单的枚举用法是定义一组相关的命名常量。

<!-- verify -->
```cangjie
enum Direction {
    Up | Down | Left | Right
}

main() {
    let d = Direction.Up
    if (d == Direction.Up) {
        println("Going Up")
    }
}
```

## 2. 携带数据的枚举

枚举成员可以携带不同类型的数据。这使得 `enum` 非常强大，能够表达复杂的状态。

<!-- verify -->
```cangjie
enum Message {
    Quit |
    Move(x: Int64, y: Int64) |
    Write(String) |
    ChangeColor(r: Int64, g: Int64, b: Int64)
}

main() {
    let msg = Message.Move(x: 10, y: 20)
    // 通常配合 match 使用
}
```

## 3. 成员函数

枚举也可以定义成员函数，用于处理自身的数据。

```cangjie
enum TrafficLight {
    Red | Green | Yellow

    func duration(): Int64 {
        match (this) {
            case Red => 30
            case Green => 60
            case Yellow => 3
        }
    }
}
```
