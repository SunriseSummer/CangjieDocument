# 仓颉语言与 Swift 语法/特性差异清单

> **用途说明**：本文档面向熟悉 Swift 的开发者（或 AI 模型），以 Swift 为锚点，列出仓颉语言的每一处语法与语义差异。阅读者可据此将 Swift 程序机械地转写为仓颉版本。
>
> **约定**：Swift 侧标注 `[Swift]`，仓颉侧标注 `[CJ]`；"相同"表示行为一致但写法可能不同。

---

## 1. 程序入口

- [Swift] 使用 `@main` 属性或直接在顶层写执行语句（Swift Script 模式）；也可定义 `static func main()` 方法。
- [CJ] 必须在包的顶层定义 `main()` 函数（不带 `func` 关键字），签名为 `main()` 或 `main(args: Array<String>)`。

## 2. 变量与常量声明

- [Swift] `let` 声明不可变绑定，`var` 声明可变绑定。
- [CJ] 同样使用 `let`（不可变）和 `var`（可变），语义一致。
- [CJ] 额外提供 `const` 关键字，表示**编译期常量**（深度不可变），Swift 无直接等价物。
- [Swift] 类型标注语法 `let x: Int = 10`。
- [CJ] 类型标注语法相同：`let x: Int64 = 10`，同样支持类型推断。

## 3. 基础数据类型

### 3.1 整数

- [Swift] 提供 `Int`、`UInt` 以及 `Int8/16/32/64`、`UInt8/16/32/64`。`Int`/`UInt` 与平台字长一致。
- [CJ] 提供 `Int8/16/32/64`、`UInt8/16/32/64` 以及 `IntNative`/`UIntNative`（平台字长）。无不带位宽的 `Int`/`UInt` 别名。
- [CJ] 整数字面量可附后缀指定类型：`42i8`、`0xFFu32` 等；Swift 不支持后缀。
- [CJ] 支持字节字面量 `b'A'`，类型为 `UInt8`；Swift 无此语法。

### 3.2 浮点数

- [Swift] 提供 `Float`（32 位）和 `Double`（64 位）。
- [CJ] 提供 `Float16`、`Float32`、`Float64`，名称直接体现位宽。
- [CJ] 浮点字面量可附后缀：`3.14f32`、`1.0f64`；Swift 不支持后缀。
- [CJ] 支持十六进制浮点字面量 `0x1.1p0`；Swift 同样支持。

### 3.3 布尔

- 两者均为 `Bool`，字面量 `true`/`false`，行为一致。

### 3.4 字符

- [Swift] 字符类型为 `Character`，代表一个扩展字素簇（Extended Grapheme Cluster），字面量用双引号 `"A"`。
- [CJ] 字符类型为 `Rune`，代表一个 Unicode 码位（Scalar Value），字面量用 `r'A'` 或 `r'\u{4f60}'`。

### 3.5 字符串

- [Swift] 使用双引号 `"hello"`，多行用 `""" """`，字符串插值 `\(expr)`。
- [CJ] 单行支持双引号 `"hello"` 和单引号 `'hello'`；多行支持 `"""..."""` 和 `'''...'''`。
- [CJ] 字符串插值语法为 `${expr}`（非 `\(expr)`）。
- [CJ] 支持原始字符串 `#"..."#`、`##'...'##`，可嵌套 `#` 调整转义层级；Swift 同样支持 `#"..."#`。

### 3.6 元组

- [Swift] 元组 `(1, "hello")`，可命名 `(x: 1, y: 2)`，访问用 `.0`/`.x`。
- [CJ] 元组语法相同 `(1, "hello")`，可命名 `(name: "a", price: 10)`，但访问用**方括号** `tuple[0]` 而非 `.0`。
- [CJ] 支持元组解构赋值 `(a, b) = (1, 2)`，可用 `_` 忽略；Swift 也支持。

### 3.7 数组

- [Swift] `Array<T>` 为值类型（COW），字面量 `[1, 2, 3]`。
- [CJ] `Array<T>` 为**引用类型**，字面量 `[1, 2, 3]`。
- [CJ] 额外提供 `VArray<T, $N>`（值类型、编译期固定长度数组），类似 C 数组；Swift 无直接等价物。
- [CJ] 数组构造支持 `Array<Int64>(3, repeat: 0)` 和 `Array<Int64>(3, {i => i + 1})`（lambda 初始化）。

### 3.8 区间 / Range

- [Swift] 闭区间 `1...5`，半开区间 `1..<5`。
- [CJ] 半开区间 `1..5`（左闭右开），闭区间 `1..=5`。
- [CJ] 支持指定步长 `0..10 : 2`；Swift 需用 `stride(from:to:by:)`。

### 3.9 特殊类型

- [CJ] `Unit` 类型，字面量 `()`，表示无有意义返回值，等价于 Swift 的 `Void`（`()`）。
- [CJ] `Nothing` 类型，是所有类型的子类型，表示表达式永不正常返回（如 `throw`/`return`/`break`）。Swift 的 `Never` 与之类似。

## 4. 操作符

### 4.1 算术

- 两者均支持 `+`、`-`、`*`、`/`、`%`。
- [CJ] 额外提供**幂运算符** `**`（如 `2 ** 10`）；Swift 无内建幂运算符，需调用 `pow()`。

### 4.2 位运算

- [Swift] 按位取反 `~`，左移 `<<`，右移 `>>`，与 `&`，或 `|`，异或 `^`。
- [CJ] 按位取反使用 `!`（不是 `~`），其余 `<<`、`>>`、`&`、`|`、`^` 相同。

### 4.3 比较 / 逻辑

- 两者均支持 `==`、`!=`、`<`、`<=`、`>`、`>=`，以及 `!`（逻辑非）、`&&`、`||`。
- [CJ] 额外支持 `&&=`、`||=` 复合赋值；Swift 无此语法。

### 4.4 自增 / 自减

- [CJ] 支持后缀 `++`、`--`（返回 `Unit`，无前缀形式）。
- [Swift] 已在 Swift 3 移除 `++`/`--`。

### 4.5 空合并

- [Swift] `a ?? b`，解包 `Optional<T>`。
- [CJ] `a ?? b`，解包 `Option<T>`，语义相同，类型名不同。

### 4.6 管道 / 组合

- [CJ] 管道操作符 `|>`：`x |> f` 等价于 `f(x)`。
- [CJ] 函数组合操作符 `~>`：`f ~> g` 等价于 `{ x => g(f(x)) }`。
- [Swift] 无内建管道和组合操作符。

### 4.7 赋值

- 两者 `=` 均为赋值，不可链式赋值（赋值表达式无值）。
- [CJ] 复合赋值支持 `**=`（幂赋值）；Swift 无此项。

### 4.8 类型操作符

- [Swift] `is` 做类型检查，`as`/`as?`/`as!` 做类型转换。
- [CJ] `is` 做类型检查；`as` 返回 `Option<T>`（等价于 Swift 的 `as?`），无强制转换等价物。

### 4.9 数值类型转换

- [Swift] 显式构造 `Int(someDouble)`。
- [CJ] 同样用构造语法 `Int64(someFloat)`，行为一致。

## 5. 控制流

### 5.1 if 表达式

- [Swift] `if` 是语句，不能作为表达式赋值（Swift 5.9 起 `if`/`switch` 可作为表达式）。
- [CJ] `if` 是**表达式**，可直接 `let x = if (cond) { a } else { b }`。
- [CJ] 条件必须写在圆括号内 `if (cond)`；Swift 不需要圆括号。
- [CJ] 支持 `if-let` 模式绑定：`if (let Some(v) <- optVal) { ... }`；Swift 写法为 `if let v = optVal { ... }`。

### 5.2 while / do-while

- [Swift] `while cond { }` 和 `repeat { } while cond`。
- [CJ] `while (cond) { }` 和 `do { } while (cond)`（关键字为 `do` 而非 `repeat`，条件须加圆括号）。

### 5.3 for-in

- [Swift] `for item in collection { }`，可加 `where` 过滤。
- [CJ] `for (item in collection) { }`（圆括号必需），同样支持 `where` 过滤。
- [CJ] 支持元组解构 `for ((k, v) in map) { ... }`。

### 5.4 match vs switch

- [Swift] `switch value { case pattern: ... }`，需 `default` 或穷举，支持 `fallthrough`。
- [CJ] `match (value) { case pattern => ... }`，使用 `=>` 而非 `:`，无 `fallthrough`，需穷举或 `case _ =>`。
- [CJ] `match` 是**表达式**，可赋值给变量。
- [CJ] 支持无参数 `match { case cond1 => ... case cond2 => ... }`（条件分支）。
- [CJ] 模式之间用 `|` 分隔多个选项；Swift 中用 `,` 分隔。

### 5.5 模式匹配

- 两者均支持：常量模式、通配符模式 `_`、绑定模式、元组模式、枚举模式、类型模式。
- [CJ] 类型模式写法 `id: Type` 或 `_: Type`；Swift 写法 `let id as Type` 或 `is Type`。
- [CJ] 模式守卫使用 `where`；Swift 同样使用 `where`。

### 5.6 labeled break / continue

- [Swift] 支持标签语句 `label: for ...`，可 `break label`、`continue label`。
- [CJ] 文档未体现标签循环语法，仅支持无标签 `break`/`continue`。

## 6. 函数

### 6.1 定义

- [Swift] `func name(label param: Type) -> ReturnType { }`。
- [CJ] `func name(param: Type): ReturnType { }`，返回类型用 `:` 而非 `->`，无参数标签机制。

### 6.2 参数

- [Swift] 每个参数有外部标签（argument label）和内部名（parameter name），默认外部标签=内部名，可用 `_` 省略。
- [CJ] 默认参数为位置参数（无外部标签）；若需命名传参，声明时在名称后加 `!`：`func f(name!: String)`，调用 `f(name: "x")`。
- [CJ] 命名参数可有默认值：`func f(size!: Int64 = 10)`。
- [Swift] 支持 `inout` 参数（值传递 + 拷贝回写）。
- [CJ] 无 `inout` 关键字。

### 6.3 可变参数

- [Swift] `func f(_ items: Int...) { }`，参数在函数内为数组。
- [CJ] 无 `...` 可变参数语法，但**参数类型为 `Array<T>` 时可直接传多个值**作为语法糖：`f(1, 2, 3)` 等价于 `f([1, 2, 3])`。

### 6.4 返回值

- [Swift] 单表达式函数可省 `return`；显式 `return expr`。
- [CJ] 函数体最后一个表达式即为返回值（隐式返回），也可显式 `return`。
- [CJ] 返回类型可省略（由推断得出）；Swift 中不返回值时省略 `-> Void`。

### 6.5 嵌套函数

- 两者均支持函数内部定义嵌套函数。

### 6.6 Lambda / 闭包

- [Swift] `{ (params) -> ReturnType in body }`，类型可推断时简写为 `{ params in body }` 或 `{ $0 + $1 }`。
- [CJ] `{ params: Type => body }`，使用 `=>` 而非 `in`，无 `$0` 简写。
- [CJ] 无参 Lambda：`{ => body }`。
- [Swift] 尾随闭包可省略参数标签和括号。
- [CJ] 尾随 Lambda 类似：最后一个参数为函数类型时，Lambda 可写在 `()` 之外，且 `=>` 可省略。

### 6.7 函数类型

- [Swift] `(Int, Int) -> Int`。
- [CJ] `(Int64, Int64) -> Int64`，语法相同。

### 6.8 函数重载

- 两者均支持同名函数按参数类型/数量重载。

### 6.9 操作符重载

- [Swift] 用 `static func +(lhs: T, rhs: T) -> T` 或全局 `func +(...)`。
- [CJ] 用 `operator func +(right: T): ReturnType` 作为实例方法，左操作数为 `this`。
- [CJ] 下标操作：`operator func [](index: Int64): T`（读取），`operator func [](index: Int64, value!: T): Unit`（赋值）。
- [Swift] 下标用 `subscript(index: Int) -> T { get { } set { } }`。

### 6.10 const 函数

- [CJ] `const func` 在编译期上下文中求值，可用于编译期计算；Swift 无直接等价物（Swift 的 `@inlinable` 和泛型特化不同）。

## 7. 结构体 (Struct)

- [Swift] `struct` 是值类型，支持继承协议、存储/计算属性、方法、下标、初始化器。`mutating` 标记可变方法。
- [CJ] `struct` 是值类型，可实现接口，支持成员变量、属性（`prop`）、方法、操作符重载。**不支持继承**。
- [CJ] 可变方法用 `mut func` 标记（对应 Swift 的 `mutating func`）。
- [CJ] 构造器用 `init(...)` 定义，与 Swift 相同。
- [Swift] struct 有自动生成的逐成员初始化器（memberwise initializer）。
- [CJ] 文档未提及自动生成的逐成员初始化器，需显式定义 `init`。

## 8. 枚举 (Enum)

- [Swift] `enum` 可定义关联值（associated values）、原始值（raw values），支持方法和计算属性。
- [CJ] `enum` 构造器用 `|` 前缀语法定义，支持关联值：`| Red | Green | Blue(UInt8)`。
- [CJ] 无原始值（raw value）概念。
- [CJ] 枚举成员可直接当函数用（如 `Blue(100)`），无需 `.Blue(100)`（上下文可推断时可省略枚举名）。
- [CJ] 支持 `...` 表示非穷举枚举（模式匹配时不要求覆盖所有分支）；Swift 使用 `@unknown default`。
- [CJ] 枚举是值类型（与 Swift 相同）。

## 9. 类 (Class)

### 9.1 定义与继承

- [Swift] `class SubClass: SuperClass, Protocol1, Protocol2 { }`。
- [CJ] `class SubClass <: SuperClass & Interface1 & Interface2 { }`，用 `<:` 表示继承/实现。
- [CJ] 类默认**不可继承**，需显式标记 `open class`；Swift 中类默认可继承，需 `final` 禁止。
- [CJ] 支持 `abstract class`（含抽象方法）；Swift 无 `abstract` 关键字，用 protocol 代替。
- [CJ] 支持 `sealed class`/`sealed interface`（限包内继承）；Swift 无直接等价物。

### 9.2 方法覆写

- [Swift] 子类用 `override func`；父类方法默认可被覆写（除非 `final`）。
- [CJ] 子类用 `override func`；但父类方法必须标记 `open` 才可被覆写。

### 9.3 构造器

- [Swift] `init(...)`，可标记 `convenience`/`required`，有两段式初始化（designated + convenience）。
- [CJ] `init(...)`，用 `super(...)` 调用父类构造器。无 `convenience`/`required` 区分。

### 9.4 析构器

- [Swift] `deinit { }`。
- [CJ] 文档未提及析构器语法。

### 9.5 引用类型

- 两者的 class 均为引用类型。

### 9.6 this vs self

- [Swift] 实例引用用 `self`。
- [CJ] 实例引用用 `this`；当前类型引用用 `This`（类似 Swift 的 `Self`）。

## 10. 接口 vs 协议

- [Swift] `protocol` 定义接口，支持属性要求、方法要求、关联类型、协议继承、协议扩展提供默认实现。
- [CJ] `interface` 定义接口，支持方法声明与默认实现、属性要求（`prop`），支持接口继承。
- [CJ] 接口**不能**包含实例变量（stored properties），只能有方法和属性。
- [Swift] 协议可包含 `associatedtype`（关联类型）。
- [CJ] 无关联类型语法，用泛型接口 `interface Container<T>` 替代。
- [CJ] 接口方法可直接提供默认实现体；Swift 需在 protocol extension 中提供默认实现。
- [CJ] `redef` 关键字用于在子接口中重新定义父接口的默认实现；Swift 无此机制。

## 11. 属性 (Properties)

- [Swift] 存储属性 `var x: Int`；计算属性 `var x: Int { get { } set { } }`；`lazy var` 延迟初始化；属性观察者 `willSet`/`didSet`。
- [CJ] 成员变量用 `let`/`var`；属性用 `prop name: Type { get() { } }` 和 `mut prop name: Type { get() { } set(v) { } }`。
- [CJ] 只读属性只需 `get()`；可变属性必须同时实现 `get()` 和 `set()`，且声明为 `mut prop`。
- [CJ] 无 `lazy` 属性、无 `willSet`/`didSet` 属性观察者。
- [CJ] 属性 getter/setter 语法为 `get()` / `set(value)`（带圆括号，像函数）；Swift 为 `get { }` / `set { newValue }`。

## 12. 泛型

### 12.1 语法

- [Swift] `func f<T>(param: T) -> T`；`class C<T>`；`struct S<T>`；`enum E<T>`。
- [CJ] 语法相同：`func f<T>(param: T): T`；`class C<T>`；`struct S<T>`；`enum E<T>`。

### 12.2 约束

- [Swift] `func f<T: Protocol>(...)` 或 `where T: Protocol`，支持 `T: Class`、`T: Protocol1 & Protocol2`、`T == U`。
- [CJ] `func f<T>(param: T) where T <: Interface` 或 `where T <: Class`，支持 `T <: I1 & I2`。
- [CJ] 约束只能用 `where` 子句（不能写在 `<>` 中）；Swift 两种写法均可。
- [CJ] 无 `T == U` 同类型约束。

### 12.3 类型别名

- [Swift] `typealias Name = ExistingType`。
- [CJ] `type Name = ExistingType`（关键字为 `type` 而非 `typealias`）。

### 12.4 泛型子类型

- [CJ] 泛型类型默认不协变/逆变，行为与 Swift 类似（Swift 中仅 `Array`、`Optional` 等标准库类型有编译器特殊协变处理）。

## 13. 扩展

- [Swift] `extension Type { }` 可添加方法、计算属性、下标、嵌套类型、协议遵从。
- [CJ] `extend Type { }` 可添加方法、属性（`prop`）、操作符重载。
- [CJ] 扩展实现接口：`extend Type <: Interface { }`，对应 Swift 的 `extension Type: Protocol { }`。
- [CJ] 泛型扩展：`extend<T> Array<T> <: Iterable<T> { }`。
- [CJ] 扩展**不能**添加实例变量（与 Swift 相同）。
- [CJ] 扩展中不能使用 `open`、`override`、`redef`。
- [CJ] 扩展中的成员不能访问被扩展类型的 `private` 成员（Swift 中 `private` 在同文件可访问，`fileprivate` 等价）。

## 14. 集合类型

- [Swift] 标准库提供 `Array`、`Set`、`Dictionary`，均为值类型（COW）。
- [CJ] 标准库提供 `ArrayList<T>`、`HashSet<T>`、`HashMap<K, V>`，均为引用类型。
- [CJ] `Array<T>` 是语言内建类型（引用类型），`ArrayList<T>` 是标准库集合。
- [Swift] 字典字面量 `["key": value]`；集合字面量 `Set([1, 2, 3])`。
- [CJ] 集合无字面量语法，需通过构造器和 `add`/`put` 方法构建。

## 15. Option vs Optional

- [Swift] `Optional<T>`（`T?`），解包方式：`if let`、`guard let`、`!`（强制解包）、`??`、可选链 `a?.b`。
- [CJ] `Option<T>`，为枚举类型 `enum Option<T> { Some(T) | None }`。
- [CJ] 无 `T?` 语法糖，需写全 `Option<T>`。
- [CJ] 解包方式：`match` 模式匹配、`??` 空合并、`if (let Some(v) <- opt)`。
- [CJ] 无强制解包操作符 `!`。
- [CJ] 无可选链 `?.` 语法。
- [Swift] `guard let` 可提前退出；[CJ] 无 `guard` 关键字。

## 16. 异常处理

- [Swift] 用 `throw`、`do { try expr } catch { }`，函数需标记 `throws`，调用时需 `try`/`try?`/`try!`。
- [CJ] 用 `throw`、`try { } catch (e: ExceptionType) { } finally { }`。
- [CJ] 函数**不需**标记 `throws`，调用时**不需** `try` 关键字修饰。
- [CJ] 异常体系：`Error`（系统错误，不应捕获）+ `Exception`（程序异常，应捕获），自定义异常继承 `Exception`。
- [Swift] 错误类型遵从 `Error` 协议，通常用 `enum` 定义。
- [CJ] 异常用 `class` 定义并继承 `Exception`。
- [CJ] `try` 为块语句（不是表达式前缀）；Swift 的 `try` 是表达式前缀。
- [Swift] 支持 `Result<Success, Failure>` 类型。
- [CJ] 无内建 `Result` 类型，但可通过枚举自行定义。

## 17. 访问控制

- [Swift] 五级：`open`、`public`、`internal`（默认）、`fileprivate`、`private`。
- [CJ] 四级：`public`、`protected`、`internal`（默认，包级可见，无显式关键字）、`private`。
- [CJ] 无 `fileprivate`。
- [CJ] `open` 仅用于标记类/方法可被继承/覆写，**不是**访问级别。
- [CJ] `sealed` 限制继承/实现范围为同包。

## 18. 包 / 模块系统

- [Swift] 用模块（module）组织代码，`import ModuleName`；内部用文件划分，无显式包声明。
- [CJ] 用包（package）组织代码，文件顶部 `package com.example.myapp`；导入用 `import std.collections.ArrayList` 或 `import other.module.*`。
- [CJ] 同包内不同文件的顶层声明互相可见（类似 Swift 同模块 `internal`）。

## 19. 并发

- [Swift] 使用 `async`/`await`、`Task { }`、`actor`、`@Sendable`、结构化并发。
- [CJ] 使用 `spawn { => ... }` 创建线程（类似轻量线程/协程），无 `async`/`await` 语法。
- [CJ] 同步原语：`synchronized(lock) { }`、`Mutex`、`AtomicInt64` 等原子类型、条件变量 `Condition`。
- [CJ] 线程睡眠：`sleep(Duration)`。
- [CJ] 无 `actor` 模型，无 `@Sendable`，无结构化并发。
- [CJ] 提供 `ThreadLocal<T>` 线程局部存储。

## 20. 宏

- [Swift] 使用 `@` 开头的宏（Swift 5.9+），分为 freestanding macro `#macroName(...)` 和 attached macro `@MacroName`，通过 SwiftSyntax 实现。
- [CJ] 使用 `@macroName(...)` 调用宏，通过 `macro` 关键字定义，接收 `Tokens` 并返回 `Tokens`。
- [CJ] 提供 `quote { ... }` 表达式用于构造代码片段。
- [CJ] 宏在**编译期**展开，支持语法节点级别操作。
- [CJ] 内置编译标记（条件编译），类似 Swift 的 `#if`、`#else`、`#endif`。

## 21. 反射与注解

### 21.1 反射

- [Swift] 提供有限的 `Mirror` API 做运行时反射；无完整的运行时类型操作。
- [CJ] 提供 `TypeInfo` API，可在运行时获取类型信息、访问 public 成员变量/属性/方法、动态调用方法。
- [CJ] `TypeInfo.of(obj)` 获取运行时类型，`TypeInfo.of<T>()` 获取静态类型，`TypeInfo.get("qualifiedName")` 按名称查找。

### 21.2 注解 / 属性

- [Swift] 内建属性 `@available`、`@discardableResult`、`@objc` 等；自定义属性通过 property wrapper `@propertyWrapper` 或宏实现。
- [CJ] 用 `@Annotation` 标记的 class 定义自定义注解，注解类必须有 `const init`。
- [CJ] 内建溢出注解：`@OverflowThrowing`（默认）、`@OverflowWrapping`、`@OverflowSaturating`。
- [CJ] 注解可通过 `target` 限定适用目标（Type、Parameter、Init、MemberFunction、MemberProperty、MemberVariable）。
- [CJ] 注解不被子类继承。

## 22. 跨语言互操作 (FFI)

- [Swift] 原生与 Objective-C 互操作（`@objc`、bridging header）；与 C 互操作通过 C 模块映射；Swift/C++ 互操作（Swift 5.9+）。
- [CJ] 与 C 互操作：`foreign func cFunction(x: Int64): Int64` 声明外部 C 函数；`foreign class` 声明 C 结构体。
- [CJ] 提供 `unsafe { }` 块执行不安全操作。
- [CJ] 使用 `VArray<T, $N>` 与 C 定长数组互操作。
- [CJ] 无与 Objective-C / C++ 的互操作。

## 23. I/O

- [Swift] 标准库 `print()`、`readLine()`；Foundation 框架提供文件/网络 I/O。
- [CJ] 内建 `print()`、`println()`（带换行）；标准库提供 I/O 流（节点流 + 处理流）、文件操作。

## 24. 网络编程

- [Swift] 通过 Foundation 的 `URLSession`、第三方库或 SwiftNIO。
- [CJ] 标准库内建 Socket、HTTP、WebSocket 编程支持。

## 25. 编译与构建

- [Swift] 编译器 `swiftc`；包管理器 Swift Package Manager (`swift build`)；构建系统 Xcode Build System。
- [CJ] 编译器 `cjc`；包管理器 `cjpm`（类似 cargo / npm）。
- [CJ] 支持条件编译（编译标记），类似 Swift 的 `#if os(Linux)` 等。

## 26. 值类型 vs 引用类型对比

| 特性 | Swift | 仓颉 |
|------|-------|------|
| struct | 值类型 | 值类型 |
| class | 引用类型 | 引用类型 |
| enum | 值类型 | 值类型 |
| Array | 值类型 (COW) | **引用类型** |
| String | 值类型 | **值类型** |
| 元组 | 值类型 | 值类型 |

## 27. 仓颉独有特性（Swift 无直接等价物）

- `const` 编译期常量与 `const func` 编译期函数求值。
- `VArray<T, $N>` 固定长度值类型数组。
- `Rune` 字符类型（单 Unicode 码位，区别于 Swift 的扩展字素簇 `Character`）。
- 幂运算符 `**` 和幂赋值 `**=`。
- 管道操作符 `|>` 和函数组合操作符 `~>`。
- 整数/浮点字面量类型后缀（`42i8`、`3.14f32`）。
- 字节字面量 `b'A'`。
- `mut func` / `mut prop` 显式可变标记（概念类似 `mutating` 但语法不同）。
- `sealed class` / `sealed interface`（限包内继承）。
- `abstract class`（抽象类）。
- `redef` 关键字（在子接口中重新定义默认实现）。
- `synchronized(lock) { }` 同步块。
- `spawn` 轻量线程创建。
- 非穷举枚举标记 `...`。
- 注解系统（`@Annotation` 类，`const init`，`target` 限定）。
- 完整运行时反射（`TypeInfo` API）。
- 数组参数调用语法糖（`f(1,2,3)` → `f([1,2,3])`）。
- 半开区间 `..` 和闭区间 `..=` 语法（不同于 Swift `..<` 和 `...`）。
- 区间步长语法 `0..10 : 2`。

## 28. Swift 独有特性（仓颉无直接等价物）

- `guard` 语句（提前退出）。
- `defer` 语句（作用域退出时执行）。
- `Optional` 语法糖 `T?`、强制解包 `!`、可选链 `?.`。
- 属性观察者 `willSet` / `didSet`。
- `lazy var` 延迟初始化属性。
- Property Wrapper（`@propertyWrapper`）。
- `associatedtype`（协议关联类型）。
- `async` / `await` / `actor` 结构化并发模型。
- `@Sendable` 并发安全标注。
- `some` / `any` 不透明类型与存在类型（Opaque / Existential types）。
- Result Builder（`@resultBuilder`）。
- 带标签的循环 `label: for` + `break label`。
- `fallthrough`（switch 穿透）。
- `convenience init` / `required init` 构造器分类。
- `deinit` 析构器。
- `@objc` / Objective-C 互操作。
- `indirect enum`（间接枚举，递归枚举）。
- 枚举原始值（raw value）。
- 参数外部标签（argument label）/ `_` 省略标签。
- `inout` 参数。
- `$0`、`$1` 闭包参数简写。
- Key Path（`\Type.property`）。
- `#selector`、`#keyPath` 等编译器指令。
- `@autoclosure` 自动闭包。
- `@escaping` 逃逸闭包标注。
- `fileprivate` 访问级别。
- `typealias`（仓颉用 `type`）。
- `willSet`/`didSet` 存储属性观察者。
- `Any` / `AnyObject`（仓颉有 `Any` 但行为可能不同）。

---

## 快速对照表

| 概念 | Swift | 仓颉 |
|------|-------|------|
| 入口 | `@main` / 顶层代码 | `main() { }` |
| 不可变变量 | `let` | `let` |
| 可变变量 | `var` | `var` |
| 编译期常量 | — | `const` |
| 默认整数 | `Int` | `Int64` |
| 字符类型 | `Character` | `Rune` |
| 字符字面量 | `"A"` | `r'A'` |
| 字符串插值 | `\(expr)` | `${expr}` |
| 可选类型 | `T?` / `Optional<T>` | `Option<T>` |
| 空合并 | `??` | `??` |
| 可选链 | `?.` | — |
| 强制解包 | `!` | — |
| 半开区间 | `..<` | `..` |
| 闭区间 | `...` | `..=` |
| 幂运算 | `pow(a, b)` | `a ** b` |
| 按位取反 | `~` | `!`（位运算上下文） |
| 自增 | — (已移除) | `x++` |
| 管道 | — | `\|>` |
| 函数组合 | — | `~>` |
| 函数定义 | `func f() -> T` | `func f(): T` |
| Lambda | `{ x in body }` | `{ x => body }` |
| 尾随闭包 | 支持 | 支持 |
| `$0` 简写 | 支持 | — |
| 命名参数 | 默认有标签 | `name!: Type` |
| switch / match | `switch` | `match` |
| 分支分隔 | `case ...:` | `case ... =>` |
| 多模式 | `,` | `\|` |
| 穿透 | `fallthrough` | — |
| 协议 / 接口 | `protocol` | `interface` |
| 继承语法 | `:` | `<:` |
| 类默认 | 可继承 | 不可继承（需 `open`） |
| 抽象类 | — | `abstract class` |
| 密封类 | — | `sealed class` |
| self / this | `self` / `Self` | `this` / `This` |
| 属性声明 | `var x: T { get set }` | `mut prop x: T { get() set(v) }` |
| mutating | `mutating func` | `mut func` |
| 错误处理 | `do-try-catch` + `throws` | `try-catch-finally`（无 `throws`） |
| 并发 | `async/await` + `actor` | `spawn` + `synchronized` |
| 类型转换 | `as?` → `T?` | `as` → `Option<T>` |
| 类型检查 | `is` | `is` |
| 类型别名 | `typealias` | `type` |
| 泛型约束 | `T: Protocol` / `where` | `where T <: Interface` |
| 扩展 | `extension` | `extend` |
| FFI | C / ObjC / C++ | C（`foreign func`） |
| 元组访问 | `.0` / `.name` | `[0]` / `[name]` |
| 数组类型 | 值类型 | 引用类型 |
| if 条件括号 | 不需要 | 需要 |
| for-in 括号 | 不需要 | 需要 |
| 包 / 模块 | `import Module` | `package x.y; import x.y.Z` |
