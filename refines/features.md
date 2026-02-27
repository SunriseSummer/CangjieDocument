# 仓颉语言特性精炼总结

> 本文档面向 AI 工具，精炼覆盖仓颉（Cangjie）语言全部语法规则与特性，可作为快速掌握仓颉开发的参考。

---

## 1. 语言概览

- **多范式**：融合函数式（高阶函数、代数数据类型、模式匹配、泛型）、面向对象（封装、接口、继承、多态）和命令式编程。
- **静态强类型**：编译期类型检查，支持强大的类型推断以减少显式注解。
- **内存安全**：自动内存管理（GC），运行时数组越界检查和溢出检测。
- **轻量级并发**：用户态轻量线程（原生协程），M:N 调度模型，抢占式调度。
- **双后端**：CJNative（编译为原生二进制）和 CJVM（编译为字节码）。
- **跨语言互操作**：支持与 C 语言互操作（FFI）。
- **宏与元编程**：词法宏，编译期代码变换。
- **丰富标准库**：数据结构、算法、数学、正则、文件、网络、数据库、日志、压缩、编解码、加密、序列化等。

---

## 2. 程序结构

- **源文件**：`.cj` 扩展名。
- **注释**：`//` 单行注释，`/* */` 多行注释。
- **程序入口**：`main()` 函数，签名可选：
  - `main(): Unit` 或 `main(): Int64`
  - `main(args: Array<String>): Unit` 或 `main(args: Array<String>): Int64`
- **包声明**：`package pkg_name`，必须是文件首个非注释非空行；同包文件声明必须一致。
- **顶层作用域**：可定义全局变量、全局函数、自定义类型（`struct`/`class`/`enum`/`interface`）。
- **作用域**：花括号 `{}` 创建新作用域；内层可遮蔽外层同名绑定；自定义类型只能在顶层定义。

---

## 3. 标识符

- **普通标识符**：以 `XID_Start` 字符（含中文、英文等）或下划线 `_` 开头（`_` 后必须跟至少一个 `XID_Continue` 字符），不能是关键字。
- **原始标识符**：用反引号包裹，可将关键字当标识符使用，如 `` `if` ``、`` `while` ``。
- **Unicode 规范化**：使用 NFC 归一化，NFC 等价的标识符视为相同。

---

## 4. 变量

| 修饰符 | 说明 |
|--------|------|
| `let` | 不可变变量，仅初始化时赋值一次 |
| `var` | 可变变量，可多次重新赋值 |
| `const` | 编译期常量，不可重新赋值，声明时必须初始化 |

- **类型推断**：变量类型可省略，编译器从初始值推导。
- **全局变量 / static 成员变量**必须有初始值（或在 `static init` 中初始化）。
- **值类型**（`Int`、`Float`、`struct`）：赋值时拷贝数据。
- **引用类型**（`class`、`Array`）：赋值时共享引用。`let` 阻止引用重新赋值但允许修改引用对象内部数据。
- **`const` 变量**产生深度不可变性；可用于全局、局部或 static 成员变量，不可定义在扩展中。

---

## 5. 基础数据类型

### 5.1 整数类型

- **有符号**：`Int8`、`Int16`、`Int32`、`Int64`、`IntNative`（平台相关）。
- **无符号**：`UInt8`、`UInt16`、`UInt32`、`UInt64`、`UIntNative`。
- **字面量**：二进制 `0b`/`0B`、八进制 `0o`/`0O`、十进制、十六进制 `0x`/`0X`；可用 `_` 分隔。
- **后缀**：`i8`、`i16`、`i32`、`i64`、`u8`、`u16`、`u32`、`u64`。
- **字节字面量**：`b'x'` 表示 `UInt8`（ASCII 值）。
- **支持运算**：算术、位运算、关系、自增/自减、复合赋值。溢出默认抛出异常。

### 5.2 浮点类型

- **类型**：`Float16`、`Float32`、`Float64`，遵循 IEEE 754。
- **字面量**：十进制（必须有整数部分或小数部分）、十六进制（`0x`/`0X` 前缀，指数用 `p`/`P`）。
- **后缀**：`f16`、`f32`、`f64`。
- **不支持**：自增/自减运算符。

### 5.3 布尔类型

- **类型**：`Bool`，字面量 `true`、`false`。
- **支持**：逻辑运算 `!`、`&&`、`||`，关系运算 `==`、`!=`，复合赋值 `&&=`、`||=`。

### 5.4 字符类型 (Rune)

- **类型**：`Rune`，表示 Unicode 字符。
- **字面量**：`r'a'` / `r"a"`，支持转义序列和 Unicode 形式 `r'\u{4f60}'`。
- **转换**：`Rune` ↔ `UInt32`；整数类型 → `Rune`（需在合法 Unicode 范围）。

### 5.5 字符串类型

- **类型**：`String`，不可变 Unicode 文本。
- **字面量**：
  - 单行：`"..."` 或 `'...'`。
  - 多行：`"""..."""` 或 `'''...'''`。
  - 原始多行：`#"..."#`（转义规则不适用，可用多个 `#`）。
- **插值**：`"${expression}"`，大括号内可含多条语句，取最后一项的值。
- **运算**：关系比较、`+` 拼接。

### 5.6 元组类型

- **声明**：`(T1, T2, ..., TN)`，至少 2 个元素。
- **字面量**：`(e1, e2, ...)`。
- **访问**：`tuple[index]`，index 为字面量整数，0 开始。
- **多重赋值**：`(a, b) = (1, 2)`。
- **可选命名**：`(name: String, price: Int64)`，全部命名或全部不命名。
- **不可变**：元素不可更新；整个元组可替换。
- **关系运算**：`==`、`!=`（要求所有元素支持）。

### 5.7 数组类型

#### `Array<T>`
- **可变元素，固定长度**（不可增删）。
- 初始化：字面量 `[0, 1, 2]`；构造函数 `Array<T>(size, repeat: v)` 或 `Array<T>(size, { i => ... })`。
- 访问：下标 `arr[i]`（`Int64`），范围切片 `arr[0..5]`，`.size` 属性。
- **引用语义**：赋值共享引用。

#### `VArray<T, $N>`（值类型数组）
- 固定长度 `$N` 在编译期确定，泛型参数不可省略。
- **元素限制**：不可包含引用类型、枚举、Lambda（`CFunc` 除外）。
- **值语义**：赋值拷贝。减少堆分配和 GC 压力。

### 5.8 区间类型

- **类型**：`Range<T>`。
- **字面量**：
  - 左闭右开：`start..end`（默认步长 1）。
  - 左闭右闭：`start..=end`。
  - 指定步长：`start..end : step`，步长不可为 0。

### 5.9 Unit 类型

- **字面量**：`()`。
- 用于仅关心副作用的表达式，如 `print()`、赋值、循环等。

### 5.10 Nothing 类型

- 无值的特殊类型，是所有类型的子类型。
- `break`、`continue`、`return`、`throw` 表达式的类型为 `Nothing`。

---

## 6. 运算符（按优先级从高到低）

| 优先级 | 运算符 | 说明 |
|--------|--------|------|
| 0 | `@` | 宏调用 |
| 1 | `.` `[]` `()` | 成员访问、索引、函数调用 |
| 2 | `++` `--` `?` | 自增/自减（后缀）、可选链 |
| 3 | `!` `-`（一元） | 逻辑非/位非、取负 |
| 4 | `**` | 幂运算（右结合） |
| 5 | `*` `/` `%` | 乘、除、取模 |
| 6 | `+` `-` | 加、减 |
| 7 | `<<` `>>` | 位左移、位右移 |
| 8 | `..` `..=` | 区间 |
| 9 | `<` `<=` `>` `>=` `is` `as` | 关系比较、类型检查/转换 |
| 10 | `==` `!=` | 等于、不等于 |
| 11 | `&` | 位与 |
| 12 | `^` | 位异或 |
| 13 | `\|` | 位或 |
| 14 | `&&` | 逻辑与（短路） |
| 15 | `\|\|` | 逻辑或（短路） |
| 16 | `??` | 空值合并（右结合） |
| 17 | `\|>` `~>` | 管道、组合 |
| 18 | `=` `+=` `-=` 等 | 赋值与复合赋值 |

**关键规则**：
- 赋值表达式类型为 `Unit`，可防止 `if(a = 3)` 误用。
- `??`：对 `Option<T>` 使用，`Some(v) ?? e2` 返回 `v`，`None ?? e2` 返回 `e2`。
- `|>`（管道）：`e1 |> f` 等价于 `f(e1)`。
- `~>`（组合）：`f ~> g` 等价于 `{ x => g(f(x)) }`。
- `++`/`--` 仅后缀，类型为 `Unit`。

---

## 7. 表达式与控制流

### 7.1 代码块

- `{}` 包裹一系列表达式，类型和值为最后一个表达式的类型和值；空块类型为 `Unit`。
- 分号 `;` 分隔同一行多条语句。

### 7.2 if 表达式

```cangjie
if (condition) { branch1 } else { branch2 }
```

- 条件必须是 `Bool` 类型（不支持隐式 0/非0 转换）。
- 支持 `let` 模式条件：`if (let pattern <- expr) { ... }`。
- 有 `else` 时两个分支类型必须兼容；无 `else` 时类型为 `Unit`。
- 可作为表达式使用（类似三元运算符）。

### 7.3 循环

- **while**：`while (condition) { body }`，类型 `Unit`。
- **do-while**：`do { body } while (condition)`，至少执行一次。
- **for-in**：`for (iter_var in sequence) { body }`。
  - 序列类型需实现 `Iterable<T>`。
  - 迭代变量不可变（`let` 语义）。
  - 支持 `where` 子句过滤：`for (i in 0..8 where i % 2 == 1)`。
  - 支持元组解构：`for ((x, y) in array)`。

### 7.4 break 和 continue

- `break`：终止当前循环；`continue`：跳到下一次迭代。
- 类型均为 `Nothing`，仅在循环体中使用。

### 7.5 match 表达式

```cangjie
match (value) {
    case pattern1 => expr1
    case pattern2 where guard => expr2
    case _ => default_expr
}
```

- 必须**穷尽**所有可能值（否则编译错误），常用 `_` 兜底。
- 支持 `|` 连接多个模式：`case A | B => ...`。
- 支持模式守卫 `where condition`。
- 匹配到即执行，不存在 fall-through。

**无值 match**：
```cangjie
match {
    case bool_expr1 => ...
    case _ => ...
}
```

---

## 8. 模式匹配

| 模式 | 说明 | 可反驳性 |
|------|------|----------|
| 常量模式 | 匹配字面值 | 可反驳 |
| 通配符 `_` | 匹配任意值，不绑定变量 | 不可反驳 |
| 绑定模式 `id` | 匹配任意值，绑定到变量 `id` | 不可反驳 |
| 元组模式 `(p1, p2, ...)` | 逐位置匹配子模式 | 取决于子模式 |
| 类型模式 `id: Type` | 检查运行时类型 | 可反驳 |
| 枚举模式 `Ctor(p1, ...)` | 匹配枚举构造器 | 取决于枚举变体数量 |

- **不可反驳模式**可用于变量定义（`let (a, b) = (1, 2)`）和 `for-in`。
- **可反驳模式**需用于 `match` 或含模式守卫的上下文。

---

## 9. 函数

### 9.1 定义

```cangjie
func functionName(p1: T1, p2: T2): ReturnType {
    body
}
```

- 参数不可变；参数类型必须显式标注。
- 返回类型可省略（编译器推断）。
- 裸 `return` 等价于 `return ()`，要求返回 `Unit`。

### 9.2 命名参数与默认值

- 命名参数：`p!: T`，调用时须写参数名 `f(p: value)`。
- 默认值仅命名参数支持：`p!: T = default_value`。
- 非命名参数必须在命名参数之前。

### 9.3 函数类型

- 语法：`(T1, T2) -> ReturnType`，`->` 右结合。
- 函数是一等公民：可赋值给变量、作为参数传递和返回值。

### 9.4 Lambda 表达式

```cangjie
{ p1: T1, p2: T2 => body }
```

- 参数类型可省略（从上下文推断）。
- 必须包含 `=>`（尾随 Lambda 语法除外）。
- 返回类型从上下文或最后一个表达式推断。

### 9.5 闭包

- 闭包可捕获外层作用域变量。
- **`var` 变量捕获限制**：捕获了 `var` 变量的闭包**不能作为一等公民**（不能赋值、不能作为返回值、不能作为参数传递），只能直接调用。此限制具有传递性。
- 对引用类型的捕获可修改其内部可变成员。

### 9.6 嵌套函数

- 函数体内定义的函数，仅在外层函数内可见。

### 9.7 函数重载

- 同名函数参数数量或类型不同即可重载。
- **重载解析**：优先选择更高作用域级别的函数；同级别选"最匹配"的候选；有歧义则编译错误。
- 不可重载：同一类中的 static 和实例同名函数；枚举中的构造器与 static/实例函数同名。

### 9.8 操作符重载

```cangjie
operator func +(right: Point): Point { ... }
operator func [](i: Int64): T { ... }                // get
operator func [](i: Int64, value!: T): Unit { ... }   // set
operator func ()(args...): R { ... }                   // 调用
```

- 只能在 `class`/`interface`/`struct`/`enum`/`extend` 中定义。
- 实例成员函数语义，不可 `static`，不可泛型。
- 重载的运算符保留原有优先级和结合性。

### 9.9 语法糖

- **尾随 Lambda**：最后一个参数为函数类型时，Lambda 可放在圆括号外。单参数时可省略 `()`。
- **管道 `|>`**：`e1 |> f` 等价于 `f(e1)`。
- **组合 `~>`**：`f ~> g` 等价于 `{ x => g(f(x)) }`。
- **变长参数**：最后一个非命名的 `Array` 类型参数可接受多个独立参数而非数组字面量。

### 9.10 const 函数

- `const func name(...) { ... }`：在 `const` 上下文中编译期求值，否则运行时求值。
- 函数体只能包含 `const` 表达式，只能声明 `let`/`const` 局部变量（不可 `var`）。
- `const init`：允许类型实例用于 `const` 表达式的构造器。

---

## 10. struct（结构体）

- **值类型**：赋值/传参时拷贝。
- 可包含：成员变量、属性、`static init`、构造器（`init` / 主构造器）、成员函数。
- **主构造器**：与结构体同名，参数可用 `let`/`var` 前缀直接声明成员变量。
- **访问修饰符**：`private`、`internal`（默认）、`protected`、`public`。
- **禁止递归**：`struct` 不可直接或间接地自引用。
- **`mut` 函数**：可修改 `struct` 实例自身；只有 `var` 声明的实例可调用 `mut` 函数；`mut` 函数中 `this` 不能被捕获；非 `mut` 函数不可调用 `mut` 函数。

---

## 11. class（类）

- **引用类型**：赋值共享引用。
- 可包含：成员变量、属性、`static init`、构造器、终结器 `~init()`、成员函数。
- **抽象类**：`abstract class`，可含 `abstract` 成员函数（无函数体）；不可实例化。
- **`open`/`sealed`**：非 abstract 类需 `open` 才能被继承；`sealed` 限制仅同包可继承。
- **主构造器**：与类同名，支持 `let`/`var` 成员变量参数。
- **构造器链**：可调用 `super(...)` 或 `this(...)`（不可同时，须为第一条语句）。
- **终结器** `~init()`：无参无返回值，执行时机不可预测。非 `open` 类才可定义。
- **`This` 类型**：仅作为实例函数返回类型的占位符，表示当前类类型。
- **继承**：单继承，`<:` 语法。子类继承所有非 `private` 非构造器成员。
- **方法覆盖**：父类用 `open`，子类用 `override`（可选）；动态派发按运行时类型。
- **静态函数重定义**：子类用 `redef`（可选），按类名静态派发。
- **访问修饰符**：同 `struct`。

---

## 12. interface（接口）

- 定义抽象行为，成员可含函数、操作符重载、属性（默认抽象）。
- 实现：`class Foo <: I1 & I2 { ... }`，实现类需提供所有接口成员。
- 接口成员默认 `public`，实现时也必须用 `public`。
- 接口可继承多个接口：`interface I2 <: I1 & I3`。
- 支持默认实现；多接口冲突时实现类须显式覆盖。
- 支持 static 成员（可有默认实现）。
- `sealed` 接口：仅同包可实现/继承。
- **`Any`**：内置接口，所有接口继承自 `Any`，所有非接口类型实现 `Any`。

---

## 13. 属性 (prop)

```cangjie
prop name: Type {
    get() { ... }
    set(v) { ... }
}
```

- 仅 `get` 为只读；有 `get` + `set` 需 `mut` 修饰，为可变属性。
- 可在 `interface`、`class`、`struct`、`enum`、`extend` 中定义。
- 支持 `open`/`override`/`redef`，子类覆盖时 `mut` 和类型须匹配。
- 支持抽象属性（接口和抽象类中无实现）。

---

## 14. 子类型关系

- 子类是父类的子类型；接口实现者是接口的子类型。
- 元组子类型：逐元素协变。
- 函数子类型：参数逆变、返回值协变。
- 固有关系：`T <: T`（自反）、`Nothing <: T`（Nothing 是所有类型子类型）、`T <: Any`、`C <: Object`（所有类）。
- 可传递。

---

## 15. 类型转换

- **数值转换**：`TargetType(expr)`，溢出编译期报错或运行时异常。
- **`Rune` ↔ `UInt32`**：`UInt32(rune)` / `Rune(int)`。
- **`is` 运算符**：`e is T` → `Bool`，运行时类型检查。
- **`as` 运算符**：`e as T` → `Option<T>`，安全类型转换。

---

## 16. 泛型

### 16.1 基本语法

```cangjie
func id<T>(a: T): T { a }
class List<T> { ... }
interface Iterator<E> { ... }
struct Pair<T, U> { ... }
enum Option<T> { Some(T) | None }
```

### 16.2 泛型约束

- `where T <: Interface1 & Interface2`：要求类型参数实现指定接口。
- 也可约束为类的子类型。
- 多个类约束须在同一继承链上。

### 16.3 型变

- **用户定义泛型**：不变（invariant）。
- **内置类型型变**：
  - 元组：每个元素位置协变。
  - 函数：参数逆变，返回值协变。

### 16.4 类型别名

```cangjie
type AliasName = OriginalType
type RD<T> = RecordData<T>  // 泛型别名
```

- 不创建新类型，仅为替代名称。仅顶层定义，不可循环引用。

---

## 17. 枚举类型

```cangjie
enum Color {
    | Red | Green | Blue(UInt8)
}
```

- 列举所有可能值（构造器），支持无参和有参构造器。
- **非穷尽枚举**：末尾加 `...`，模式匹配须用 `_` 或绑定模式兜底。
- 支持递归枚举。
- 可包含成员函数、操作符函数和属性。
- **`Option<T>`**：内置枚举，`Some(T)` | `None`；缩写 `?T`。值可自动包装为 `Some`。

---

## 18. 扩展 (extend)

```cangjie
extend TypeName { ... }                     // 直接扩展
extend TypeName <: Interface1 & Interface2 { ... } // 接口扩展
extend<T> MyList<T> where T <: Eq<T> { ... }       // 泛型扩展
```

- **可扩展任意可见类型**（函数、元组、接口除外）。
- **能添加**：成员函数、操作符重载、属性、接口实现。
- **不能添加**：成员变量。
- **不能使用** `open`/`override`/`redef`，不可访问被扩展类型的 `private` 成员。
- **孤儿规则**：不可在第三方包中为第三方类型实现第三方接口。
- 扩展随类型或接口导入自动导入，无需显式 `import`。

---

## 19. Collection 类型

| 类型 | 元素可变 | 增删 | 有序 | 唯一 |
|------|---------|------|------|------|
| `Array<T>` | ✓ | ✗ | ✓ | ✗ |
| `ArrayList<T>` | ✓ | ✓ | ✓ | ✗ |
| `HashSet<T>` | ✗ | ✓ | ✗ | ✓ |
| `HashMap<K, V>` | V 可变 | ✓ | ✗ | K 唯一 |

- 使用 `import std.collection.*`。
- `HashSet` / `HashMap` 的键类型须实现 `Hashable` 和 `Equatable<T>`。
- 所有集合均为引用语义。

### Iterable / Iterator

- 实现 `Iterable<T>` 接口即可被 `for-in` 遍历。
- `Iterator<T>` 接口：`mut func next(): Option<T>`。

---

## 20. 包与模块

### 20.1 包 (Package)

- 最小编译单元，每个包有自己的命名空间。
- 包名映射源码路径（相对于 `src/`），用 `.` 分隔。
- `core` 包隐式导入。

### 20.2 导入

```cangjie
import pkg.module.item            // 单个导入
import pkg.module.{a, b, c}      // 多个导入
import pkg.module.*               // 通配符导入
import pkg.name as alias          // 别名
```

- 导入项的作用域级别低于当前包成员。
- **不可循环依赖**。
- **重导出修饰符**：`private`（默认）、`internal`、`protected`、`public` 控制导入项的再导出可见性。

### 20.3 可见性修饰符

| 修饰符 | 可见范围 |
|--------|---------|
| `private` | 当前文件 |
| `internal` | 当前包及子包（默认） |
| `protected` | 当前模块 |
| `public` | 所有模块 |

- 声明的访问级别不可超过其使用的类型的访问级别。

---

## 21. 异常处理

### 21.1 异常层次

- `Error`：系统内部错误，不可手动 `throw`。
- `Exception`：逻辑/IO 错误，可被捕获处理；自定义异常需继承 `Exception`。

### 21.2 try-catch-finally

```cangjie
try {
    // 可能抛出异常的代码
} catch (e: SomeException) {
    // 处理
} catch (_: Exception) {
    // 兜底
} finally {
    // 清理，始终执行
}
```

- `catch` 支持类型模式和通配符 `_`，支持 `|` 匹配多个异常类型。
- `finally` 始终执行，用于资源释放。

### 21.3 try-with-resources

```cangjie
try (resource = SomeResource()) {
    // 使用资源
}
```

- 资源须实现 `Resource` 接口（`isClosed()` 和 `close()`），退出时自动关闭。

### 21.4 Option 作为错误处理

- `??`（空值合并）、`?`（可选链 `e?.member`）、`getOrThrow()`。

---

## 22. 并发编程

### 22.1 线程模型

- M:N 模型：M 个仓颉轻量线程在 N 个 OS 线程上调度。
- 抢占式调度。

### 22.2 创建线程

```cangjie
let fut = spawn { =>
    // 并发执行的代码
}
```

- 返回 `Future<T>`。
- 主线程结束时所有子线程终止。

### 22.3 Future<T>

- `get(): T`：阻塞等待结果。
- `get(timeout: Duration): T`：带超时。
- `tryGet(): Option<T>`：非阻塞。
- `cancel()`：发送取消请求（需线程自行检查 `Thread.currentThread.hasPendingCancellation`）。

### 22.4 同步机制

- **原子操作**：`AtomicInt64` 等，支持 `load`/`store`/`swap`/`compareAndSwap`/`fetchAdd` 等。
- **互斥锁** `Mutex`：`lock()`/`unlock()`/`tryLock()`；可重入。
- **条件变量** `Condition`：`wait()`/`notify()`/`notifyAll()`；须在持有锁时调用。
- **`synchronized`**：自动获取/释放锁，异常安全。
  ```cangjie
  synchronized(mutex) { /* 受保护代码 */ }
  ```
- **`ThreadLocal<T>`**：线程本地存储，`get()` / `set()`。
- **`sleep(Duration)`**：阻塞当前线程指定时长。

---

## 23. I/O 操作

- **流抽象**：`InputStream`（`read`）、`OutputStream`（`write`/`flush`）。
- **标准流**：`getStdIn()`/`getStdOut()`/`getStdErr()`（`import std.env.*`），线程安全。
- **文件操作**（`import std.fs.*`）：
  - 静态方法：`File.exists()`/`File.copy()`/`File.readFrom()`/`File.writeTo()`。
  - 打开模式：`OpenMode.Read`/`Write`/`Append`/`ReadWrite`。
  - 资源管理：`try (file = File(...)) { ... }`。
- **处理流**：`BufferedInputStream`/`BufferedOutputStream`、`StringReader`/`StringWriter`。

---

## 24. 网络编程

### TCP

```cangjie
// 服务端
try (server = TcpServerSocket(bindAt: port)) {
    server.bind()
    let client = server.accept()
    // read/write
}
// 客户端
try (socket = TcpSocket(host, port)) {
    socket.connect()
    // read/write
}
```

### UDP

```cangjie
try (socket = UdpSocket(bindAt: port)) {
    socket.bind()
    socket.sendTo(address, data)
    let (remote, count) = socket.receiveFrom(buffer)
}
```

### HTTP

- 服务端：`ServerBuilder().addr(...).port(...).build()` → `server.distributor.register(path, handler)` → `server.serve()`。
- 客户端：`ClientBuilder().build()` → `client.get(url)` → `response.body.read(buffer)`。
- 库：`stdx.net.http.*`。

### WebSocket

- 基于 HTTP 升级，持久双向连接。
- `WebSocket.upgradeFromClient(...)` / `WebSocket.upgradeFromServer(...)`。
- 帧操作：`write(frameType, payload)` / `read()` → 匹配 `TextWebFrame`/`BinaryWebFrame`/`CloseWebFrame` 等。

---

## 25. 宏

### 25.1 基本概念

- 宏是输入/输出为程序代码的特殊函数，用 `@` 前缀调用。
- 宏定义和使用必须在不同包中，宏包需先编译。

### 25.2 定义

```cangjie
macro package define
import std.ast.*

public macro MacroName(input: Tokens): Tokens {
    // 处理 input，返回变换后的代码
    return quote(/* 模板代码 */)
}
```

### 25.3 属性宏

```cangjie
public macro Foo(attrs: Tokens, input: Tokens): Tokens { ... }
// 调用：@Foo[attrs] declaration
```

### 25.4 核心 API

- `Token`/`Tokens`：词法单元和序列。
- `quote(...)`：构造 `Tokens`。
- `$(...)`：在 `quote` 中插值表达式。
- `parseExpr`/`parseDecl`/`parseType`/`parsePattern`：解析 Tokens 为语法节点。
- `diagReport(level, tokens, message, hint)`：报告宏展开错误。

### 25.5 编译

```bash
cjc macros/*.cj --compile-macro --output-dir ./target
cjc src/*.cj --import-path ./target -o main
```

---

## 26. 反射与注解

### 26.1 反射

- `TypeInfo.of(instance)` / `TypeInfo.of<T>()` / `TypeInfo.get("module.package.type")`。
- 仅 `public` 成员可见。
- 可获取并调用：构造器、成员变量、属性、函数。

### 26.2 内置注解

| 注解 | 说明 |
|------|------|
| `@OverflowThrowing` | 整数溢出时抛异常（默认行为） |
| `@OverflowWrapping` | 整数溢出时截断高位 |
| `@OverflowSaturating` | 整数溢出时取边界值 |
| `@FastNative` | 优化短时 C 函数调用 |
| `@Frozen` | 标记函数/属性签名和实现跨版本稳定 |
| `@Attribute[value]` | 设置声明的属性值 |
| `@Deprecated[message]` | 标记 API 已弃用 |

### 26.3 自定义注解

```cangjie
@Annotation
class MyAnnotation {
    const init(param: String) { ... }
}
// 使用：@MyAnnotation["value"] class Foo { ... }
// 获取：TypeInfo.of(obj).findAnnotation<MyAnnotation>()
```

- 可用 `target` 限制注解位置：`Type`/`Parameter`/`Init`/`MemberProperty`/`MemberFunction`/`MemberVariable`。

---

## 27. FFI（仓颉-C 互操作）

### 27.1 调用 C 函数

```cangjie
foreign func c_function(a: Int32, b: Int32): Int32
main() {
    unsafe { c_function(1, 2) }
}
```

- `foreign` 声明 C 函数（无函数体），参数/返回类型须符合 C-仓颉类型映射。
- 调用须在 `unsafe {}` 块中。

### 27.2 CFunc 类型

- 三种形式：`foreign` 函数、`@C` 仓颉函数、`CFunc` Lambda（不可捕获变量）。
- 泛型类型：`CFunc<(ParamTypes) -> ReturnType>`。

### 27.3 类型映射

| 仓颉 | C |
|------|---|
| `Unit` | `void` |
| `Bool` | `bool` |
| `Int8`/`UInt8` | `int8_t`/`uint8_t` |
| `Int16`/`UInt16` | `int16_t`/`uint16_t` |
| `Int32`/`UInt32` | `int32_t`/`uint32_t` |
| `Int64`/`UInt64` | `int64_t`/`uint64_t` |
| `Float32`/`Float64` | `float`/`double` |
| `CPointer<T>` | `T*` |
| `CString` | `char*` |
| `@C struct` | C 结构体（内存布局兼容） |
| `VArray<T, $N>` | `T[N]` |

### 27.4 指针操作

- `CPointer<T>`：`read()`/`write(value)`/`isNull()`；偏移 `ptr + 1`。
- `CString`：`LibC.mallocCString(str)` 分配，`LibC.free(cstr)` 释放。
- `inout` 参数：将变量按引用传递给 CFunc。

### 27.5 编译链接

```bash
cjc -L . -l myfunc test.cj -o test.out
LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./test.out
```

---

## 28. 条件编译

```cangjie
@When[os == "Linux"]
func linuxOnly() { ... }

@When[arch == "x86_64" && !debug]
func optimizedCode() { ... }
```

- 内置条件：`os`、`backend`、`arch`、`cjc_version`、`debug`、`test`。
- 自定义条件：`--cfg "key = value"` 或 `cfg.toml` 文件。
- 逻辑运算：`&&`、`||`、`!`，支持括号。
- 适用于 `import` 和声明节点。

---

## 29. 编译标记

- `@sourcePackage()`：返回当前包名（`String`）。
- `@sourceFile()`：返回当前文件名（`String`）。
- `@sourceLine()`：返回当前行号（`Int64`）。
