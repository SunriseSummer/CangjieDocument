---
name: cangjie-pattern-match
description: "仓颉语言模式匹配。当需要了解仓颉语言的match表达式（有匹配值/无匹配值）、case分支代码块写法、穷举性、模式守卫(where)、常量模式、通配符模式、绑定模式、元组模式、类型模式、枚举模式、模式嵌套、模式可反驳性(refutability)、模式在变量定义和for-in中的使用等特性时，应使用此 Skill。关于枚举类型定义，请参阅 cangjie-enum Skill。关于 Option 类型及其解构方式，请参阅 cangjie-option Skill。"
---

# 仓颉语言模式匹配 Skill

## 1. match 表达式

### 1.1 有匹配值的 match 表达式

```cangjie
match (expr) {
    case pattern1 => exprs
    case pattern2 => exprs
    case _ => exprs
}
```

**case 分支代码块规则：**
- `=>` 后是 **exprs**（1~N 个表达式、变量定义或函数定义），多个时各占一行，**不需要用 `{}` 包裹**
- 每个 `case` 分支的**值 = 最后一个表达式的值**，分支的**类型 = 最后一个表达式的类型**
- `=>` 后新定义的变量/函数的作用域从其定义处到下一个 `case` 之前结束
- 每个 `case` 可用 `|` 连接多个模式（须为同类模式）

**完整示例：case 分支的多行代码块**
```cangjie
main() {
    let opt: ?Int64 = 42
    let result = match (opt) {
        case Some(x) =>
            let doubled = x * 2
            println("doubled = ${doubled}")
            doubled   // 最后一个表达式决定当前 case 分支的值
        case None => 0
    }
    println("result = ${result}")  // result = 84
}
```

```cangjie
// ❌ 错误：case 分支不使用 {} 包裹代码块
// match (x) {
//     case 1 => { println("one"); 1 }  // 错误写法
// }

// ✅ 正确：直接写多行表达式
match (x) {
    case 1 =>
        println("one")
        1
    case _ => 0
}
```

### 1.2 无匹配值的 match 表达式

```cangjie
match {
    case boolExpr1 => exprs
    case boolExpr2 => exprs
    case _ => exprs   // _ 表示 true
}
```
- 每个 `case` 接受 `Bool` 表达式（非模式）
- `=>` 后同样是 **exprs**（1~N 个表达式/定义），各占一行，**不需要 `{}`**
- 此形式不支持模式守卫

```cangjie
main() {
    let x = -1
    match {
        case x > 0 => print("x > 0")
        case x < 0 => print("x < 0")    // 匹配：x = -1 < 0
        case _ => print("x = 0")
    }
}
```

### 1.3 穷举性
- **所有 `match` 表达式须穷举** — 须覆盖所有可能值。非穷举 → **编译错误**
- 常见做法：使用通配符 `_` 作为最后一个 case
- **非穷举枚举**（`...` 构造器）须使用 `_` 或绑定模式覆盖（关于非穷举枚举，详见 `cangjie-enum` Skill）

```cangjie
// ❌ 错误：未穷举所有可能值
// func bad(x: Int64) {
//     match (x) {
//         case 0 => "zero"
//         case 1 => "one"
//     }  // 编译错误：未覆盖所有可能取值
// }

// ✅ 正确：使用 _ 覆盖剩余情况
func good(x: Int64) {
    match (x) {
        case 0 => "zero"
        case 1 => "one"
        case _ => "other"
    }
}
```

### 1.4 模式守卫（`where`）
- 模式后可添加 `where condition`（条件须为 `Bool` 类型）
- case 仅在模式匹配**且**守卫为 true 时才匹配
- **注意**：仓颉使用 `where` 关键字作为模式守卫，而非其他语言常用的 `if`

```cangjie
match (value) {
    case n where n > 0 => "positive"   // 正确：使用 where
    // case n if n > 0 => ...           // ❌ 错误：不支持 if 作为模式守卫
    case _ => "non-positive"
}
```

**模式守卫完整示例：**
```cangjie
enum RGBColor {
    | Red(Int16) | Green(Int16) | Blue(Int16)
}

main() {
    let c = RGBColor.Green(-100)
    let cs = match (c) {
        case Red(r) where r < 0 => "Red = 0"
        case Red(r) => "Red = ${r}"
        case Green(g) where g < 0 => "Green = 0"    // 匹配
        case Green(g) => "Green = ${g}"
        case Blue(b) where b < 0 => "Blue = 0"
        case Blue(b) => "Blue = ${b}"
    }
    println(cs)  // 输出：Green = 0
}
```

### 1.5 执行语义
- case 按**从上到下**顺序求值，首个匹配执行后退出 match
- **无穿透**（fall-through）

### 1.6 match 表达式类型
- **有显式上下文类型**：每个分支体须为期望类型的子类型
- **无上下文类型**：match 表达式类型为所有分支体的**最小公共父类型**
- **值未使用时**：类型为 `Unit`，无公共父类型要求

```cangjie
// match 表达式作为值使用
let x = 2
let s: String = match (x) {
    case 0 => "zero"
    case 1 => "one"
    case _ => "other"     // 所有分支须为 String 子类型
}
```

---

## 2. 模式类型

### 2.1 常量模式
- 整数、浮点、字符、布尔、字符串字面量（无插值）和 `Unit` 字面量
- 须与匹配目标**同类型**
- 值相等时匹配
- 多个常量可用 `|` 组合
- 匹配 `Rune` 值时，`Rune` 字面量和单字符字符串字面量均可作为常量模式
- 匹配 `Byte` 值时，ASCII 字符字符串字面量可作为常量模式

```cangjie
main() {
    let score = 90
    let level = match (score) {
        case 0 | 10 | 20 | 30 | 40 | 50 => "D"
        case 60 => "C"
        case 70 | 80 => "B"
        case 90 | 100 => "A"               // 匹配
        case _ => "Not a valid score"
    }
    println(level)  // 输出：A
}
```

### 2.2 通配符模式（`_`）
- 匹配**任意值**
- 通常用作最后一个 case 捕获剩余情况

### 2.3 绑定模式（`id`）
- 匹配任意值并将其**绑定**到标识符 `id`
- `id` 是**不可变**变量，作用域从引入处到该 `case` 分支结束
- `=>` 后不能修改 `id`
- **不能与 `|`** 连接多个模式一起使用
- **注意**：若 `id` 是枚举构造器名，则被视为**枚举模式**而非绑定模式

```cangjie
main() {
    let x = -10
    let y = match (x) {
        case 0 => "zero"
        case n => "x is not zero and x = ${n}"  // n 绑定 x 的值
    }
    println(y)  // 输出：x is not zero and x = -10
}
```

```cangjie
// ❌ 错误：绑定模式不能与 | 一起使用
// case x | x => {}                    // 编译错误
// case Some(x) | Some(x) => {}        // 编译错误

// ❌ 错误：绑定变量不可修改
// case n => n = n + 1                  // 编译错误：n 不可变
```

### 2.4 元组模式
- 语法：`(p_1, p_2, ..., p_n)`，每个 `p_i` 是一个模式，`n ≥ 2`
- 每个位置都匹配时整体匹配
- 同一元组模式内不允许重复绑定名

```cangjie
main() {
    let tv = ("Alice", 24)
    let s = match (tv) {
        case ("Bob", age) => "Bob is ${age} years old"
        case ("Alice", age) => "Alice is ${age} years old"  // 匹配
        case (name, 100) => "${name} is 100 years old"
        case (_, _) => "someone"
    }
    println(s)  // 输出：Alice is 24 years old
}
```

### 2.5 类型模式
- 两种形式：`_: Type`（无绑定）和 `id: Type`（有绑定）
- 检查值的**运行时类型**是否为 `Type` 的**子类型**
- 若匹配，值被转换为 `Type` 并可选绑定到 `id`

```cangjie
open class Base {
    var a: Int64
    public init() { a = 10 }
}

class Derived <: Base {
    public init() { a = 20 }
}

main() {
    var d = Derived()
    var r = match (d) {
        case b: Base => b.a      // 匹配：Derived 是 Base 的子类型
        case _ => 0
    }
    println("r = ${r}")  // 输出：r = 20
}
```

### 2.6 枚举模式
- 镜像枚举构造器语法：`C`（无参）或 `C(p_1, ..., p_n)`（有参）
- 类型前缀可省略
- 构造器名匹配**且**所有嵌套模式匹配时整体匹配
- 须**覆盖枚举的所有构造器**（或使用 `_`）
- **不能在含绑定变量的枚举模式中使用 `|`**

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

main() {
    let x = Year(2)
    let s = match (x) {
        case Year(n) => "x has ${n * 12} months"  // 匹配
        case TimeUnit.Month(n) => "x has ${n} months"
    }
    println(s)  // 输出：x has 24 months
}
```

### 2.7 模式嵌套
- 元组和枚举模式可**任意深度嵌套**其他模式

```cangjie
enum TimeUnit {
    | Year(UInt64)
    | Month(UInt64)
}

enum Command {
    | SetTimeUnit(TimeUnit)
    | GetTimeUnit
    | Quit
}

main() {
    let command = (SetTimeUnit(Year(2022)), SetTimeUnit(Year(2024)))
    match (command) {
        case (SetTimeUnit(Year(year)), _) => println("Set year ${year}")
        case (_, SetTimeUnit(Month(month))) => println("Set month ${month}")
        case _ => ()
    }
    // 输出：Set year 2022
}
```

---

## 3. 模式可反驳性

| 模式 | 可反驳性 | 规则 |
|------|----------|------|
| **常量** | 始终**可反驳** | 可能不匹配值 |
| **通配符**（`_`） | 始终**不可反驳** | 总是匹配 |
| **绑定**（`id`） | 始终**不可反驳** | 总是匹配 |
| **类型**（`id: Type`） | 始终**可反驳** | 运行时类型可能不是子类型 |
| **元组** `(p1,...,pn)` | 当且仅当**所有** `pi` 不可反驳时**不可反驳** | 一个可反驳子模式使整体可反驳 |
| **枚举** `C(p1,...,pn)` | 当且仅当枚举**仅有一个**有参构造器**且**所有 `pi` 不可反驳时**不可反驳** | 多个构造器 → 始终可反驳 |

---

## 4. 模式的其他用途

### 4.1 变量定义（let）
- 仅允许**不可反驳**模式
```cangjie
let _ = 100                      // 通配符
let x = 100                      // 绑定
let (x, y) = (100, 200)          // 不可反驳元组（解构）
```

### 4.2 `for in` 表达式
- 仅允许**不可反驳**模式
```cangjie
for (_ in 1..5) { ... }                     // 通配符
for (i in 1..5) { ... }                     // 绑定
for ((i, j) in [(1,2),(3,4),(5,6)]) { ... } // 元组解构
```

### 4.3 `if` 和 `while` 条件
- 可使用 `let pattern <- expression` 条件
```cangjie
// if let 解构 Option 值（详见 cangjie-enum Skill 的 Option 部分）
let opt: ?Int64 = 42
if (let Some(v) <- opt) {
    println("value = ${v}")
}
```

### 4.4 这些上下文中允许的不可反驳模式
1. 通配符模式 `_`
2. 绑定模式 `id`
3. 不可反驳的元组模式
4. 不可反驳的枚举模式（单构造器枚举且所有嵌套模式不可反驳）

---

## 5. 完整可运行示例

```cangjie
enum Shape {
    | Circle(Float64)
    | Rect(Float64, Float64)
    | Triangle(Float64, Float64)
}

main() {
    let shapes = [Circle(5.0), Rect(3.0, 4.0), Triangle(3.0, 6.0)]

    for (shape in shapes) {
        let area = match (shape) {
            case Circle(r) =>
                let a = 3.14159 * r * r
                a
            case Rect(w, h) => w * h
            case Triangle(b, h) =>
                b * h / 2.0
        }
        // 使用无匹配值 match 分类输出
        match {
            case area > 50.0 => println("Large: ${area}")
            case area > 10.0 => println("Medium: ${area}")
            case _ => println("Small: ${area}")
        }
    }
}
```
