# 类 (Class)

类 (`class`) 是仓颉面向对象编程的核心。它是**引用类型**，支持继承、多态等特性。

## 1. 定义类

使用 `class` 关键字定义。

```cangjie
class Person {
    var name: String = ""
    var age: Int64 = 0

    public init(name: String, age: Int64) {
        this.name = name
        this.age = age
    }

    func sayHello() {
        println("Hello, I'm ${name}")
    }
}
```

## 2. 继承

使用 `<:` 符号表示继承。默认情况下类是不可继承的（final），需要使用 `open` 或 `abstract` 修饰符允许继承。

<!-- verify -->
```cangjie
open class Animal {
    open func speak() {
        println("...")
    }
}

class Dog <: Animal {
    // 重写父类方法
    public override func speak() {
        println("Woof!")
    }
}

main() {
    let d = Dog()
    d.speak() // Woof!
}
```

## 3. 访问修饰符

| 修饰符 | 说明 |
| :--- | :--- |
| **`private`** | 仅当前类内部可见 |
| **`protected`** | 当前包及子类可见 |
| **`internal`** | 当前包内可见（默认） |
| **`public`** | 全局可见 |

## 4. This 与 Super

- `this`: 引用当前实例。
- `super`: 引用父类实例（用于调用父类方法）。
