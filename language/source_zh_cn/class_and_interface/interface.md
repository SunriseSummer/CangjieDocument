# 接口 (Interface)

接口定义了一组行为规范（契约），任何实现了该接口的类型都必须提供这些行为的具体实现。

## 1. 定义接口

使用 `interface` 关键字。接口中可以包含函数声明和属性声明，但不能包含状态（成员变量）。

```cangjie
interface Flyable {
    func fly(): Unit
    prop speed: Int64
}
```

## 2. 实现接口

类或结构体使用 `<:` 符号来实现接口。

<!-- verify -->
```cangjie
interface Runnable {
    func run(): Unit
}

class Runner <: Runnable {
    public func run() {
        println("Running...")
    }
}

main() {
    let r: Runnable = Runner() // 多态：使用接口类型变量
    r.run()
}
```

## 3. 接口继承

接口也可以继承其他接口，同样使用 `<:`。

```cangjie
interface Animal {}
interface Bird <: Animal {}
```

## 4. 默认实现

接口中的方法可以提供默认实现。如果实现类不重写该方法，则使用默认版本。

```cangjie
interface Logger {
    func log(msg: String) {
        println("[Log] ${msg}")
    }
}
```
