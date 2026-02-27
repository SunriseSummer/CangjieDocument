---
name: cangjie-enum
description: "仓颉语言枚举类型。当需要了解仓颉语言的enum定义规则、构造器（有参/无参/同名/非穷举）、枚举的使用与名称冲突、枚举成员函数和属性、递归枚举、枚举与Equatable接口、Option类型(?T)及其自动包装等特性时，应使用此 Skill。关于模式匹配和match表达式，请参阅 cangjie-pattern-match Skill。"
---

# 仓颉语言枚举类型 Skill

## 1. 枚举类型定义

### 1.1 定义规则
- 使用 `enum` 关键字 + 名称 + `{}` 体定义
- 体内包含**构造器**，以 `|` 分隔（第一个 `|` 可选）
- 每个枚举须有**至少一个具名构造器**
- 构造器可以是**无参**（`Red`）或**有参**（`Red(UInt8)`）
- **同名构造器**在参数数量不同时允许（包括 0 个参数）
- **构造器名不能与仓颉关键字同名**（如 `Bool`、`String`、`Int64` 等都是关键字）。若需要使用关键字作为构造器名，须用反引号转义（如 `` `Bool` ``），或改用其他名称（如 `JBool`）：
  ```cangjie
  // 错误：Bool 是关键字
  // | Bool(Bool)  // 编译错误
  // 正确：使用反引号转义或改名
  | `Bool`(Bool)   // 反引号转义
  | JBool(Bool)    // 改名避免冲突
  ```
- **非穷举枚举**：可有一个特殊的未命名 `...` 构造器作为最后一个。不能直接匹配，须用 `_` 或绑定模式（详见 `cangjie-pattern-match` Skill）
- **递归定义**支持（构造器参数可引用枚举自身）
- 枚举体还可包含**成员函数**、**运算符函数**和**成员属性**，但不能与构造器同名
- **枚举仅能在顶层作用域定义**

### 1.2 定义示例
```cangjie
// 基本枚举：无参构造器
enum Direction {
    | Up | Down | Left | Right
}

// 有参构造器
enum RGBColor {
    | Red(UInt8) | Green(UInt8) | Blue(UInt8)
}

// 同名构造器（参数个数不同）
enum Color {
    | Red | Green | Blue
    | Red(UInt8) | Green(UInt8) | Blue(UInt8)
}

// 非穷举枚举
enum Token {
    | Number | Plus | Minus | ...
}

// 递归枚举
enum Expr {
    | Num(Int64)
    | Add(Expr, Expr)
    | Sub(Expr, Expr)
}

// 包含成员函数的枚举
enum RGBColor2 {
    | Red | Green | Blue

    public static func printType() {
        print("RGBColor")
    }
}
```

---

## 2. 枚举的使用

### 2.1 创建枚举值
- 通过 `TypeName.Constructor` 或直接使用构造器名创建实例
```cangjie
enum RGBColor {
    | Red | Green | Blue(UInt8)
}

main() {
    let r = RGBColor.Red   // 类型名限定
    let g = Green           // 直接使用构造器名
    let b = Blue(100)       // 有参构造器
}
```

### 2.2 名称冲突
- 若构造器名与作用域中的变量、函数或类名冲突，**须**用枚举类型名限定
```cangjie
let Red = 1                           // 变量名与构造器同名

enum RGBColor {
    | Red | Green(UInt8) | Blue(UInt8)
}

let r1 = Red                          // 选择变量 Red，而非构造器
let r2 = RGBColor.Red                 // 正确：通过类型名访问构造器
```

---

## 3. 枚举与 Equatable

- **枚举默认不实现 `Equatable` 接口**，不能直接使用 `==` 比较枚举值
- 若需要 `==` 比较，须使用 `@Derive[Equatable]` 宏自动派生（需导入 `import std.deriving.*`）
- 不使用 `@Derive` 时，应通过 `match` 模式匹配来判断枚举值（详见 `cangjie-pattern-match` Skill）

> **跨 Skill 引用**：关于 `@Derive` 宏的详细用法（支持的接口、适用类型、辅助宏等），请参阅 `cangjie-std-libs` Skill 第 17 节"自动派生（std.deriving）"。

### 完整示例：枚举与 Equatable

```cangjie
import std.deriving.*

@Derive[Equatable]
enum Color {
    | Red | Green | Blue
}

main() {
    let c = Color.Red

    // 使用 @Derive 后可以直接用 == 比较
    if (c == Color.Red) {
        println("It's red!")
    }

    // 不使用 @Derive 时，须通过 match 判断
    // （详见 cangjie-pattern-match Skill）
    let name = match (c) {
        case Red => "Red"
        case Green => "Green"
        case Blue => "Blue"
    }
    println(name)
}
```

### 常见错误

```cangjie
// ❌ 错误：枚举默认不支持 == 比较
enum Status {
    | Active | Inactive
}
// if (Status.Active == Status.Inactive) { }  // 编译错误

// ✅ 正确：添加 @Derive[Equatable]
import std.deriving.*

@Derive[Equatable]
enum Status2 {
    | Active | Inactive
}
// if (Status2.Active == Status2.Inactive) { }  // 正确
```

---

## 4. Option 类型

### 4.1 定义
```cangjie
enum Option<T> {
    | Some(T)
    | None
}
```
- `Some(v)` = 有值；`None` = 无值

### 4.2 简写语法
- `?Ty` 等价于 `Option<Ty>`

### 4.3 自动包装
- 当上下文期望 `Option<T>` 时，可直接传 `T` 值 — 编译器自动包装为 `Some`
```cangjie
let a: ?Int64 = 100      // 自动包装为 Some(100)
let b: ?String = "hello"  // 自动包装为 Some("hello")
```

### 4.4 显式 `None` 带类型
- 无上下文类型时使用 `None<T>` 语法
```cangjie
let a = None<Int64>   // a: Option<Int64>
let b = None<Bool>    // b: Option<Bool>
```

### 4.5 Option 的使用
- 使用 `??` 提供默认值：`let name = getName() ?? "unknown"`
- 使用 `match` 进行模式匹配解构（详见 `cangjie-pattern-match` Skill）
- 使用 `if let` 条件解构：`if (let Some(v) <- opt) { ... }`

> **跨 Skill 引用**：`??` 运算符的优先级低于比较运算符，使用时需注意加括号，详见 `cangjie-basic-data-type` Skill 的运算符优先级部分。

---

## 5. 完整可运行示例

```cangjie
import std.deriving.*

// 使用枚举定义一个简单的表达式求值器
enum Expr {
    | Num(Int64)
    | Add(Expr, Expr)
    | Neg(Expr)
}

// 枚举可以定义成员函数
@Derive[ToString]
enum Color {
    | Red | Green | Blue
}

main() {
    // 创建枚举值
    let expr = Add(Num(1), Neg(Num(2)))

    // 使用 match 递归求值（详见 cangjie-pattern-match Skill）
    // eval(expr) => 1 + (-2) = -1

    // Option 类型使用
    let opt: ?Int64 = 42           // 自动包装为 Some(42)
    let val = opt ?? 0             // 解包：42
    let none: ?Int64 = None        // 无值
    let fallback = none ?? -1      // 解包：-1
    println("val = ${val}, fallback = ${fallback}")
}
```
