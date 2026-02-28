---
name: cangjie-macro
description: "仓颉语言宏。当需要了解仓颉语言的Token/Tokens类型、quote表达式与插值、非属性宏、属性宏、嵌套宏与通信、std.ast包与语法节点(AST)解析、宏包编译构建(cjc/cjpm)、内置编译标记(@sourceFile/@When/@FastNative/@Frozen/@Deprecated等)时，应使用此 Skill。"
---

# 仓颉语言宏 Skill

## 1. 宏概述

### 1.1 核心概念
- 宏是特殊函数，输入和输出均为**程序片段**（非值）
- 使用 `@` 前缀调用：`@macroName(...)`
- 宏接收 `Tokens` 输入，转换后返回新的 `Tokens`，在编译时替换调用处
- 须声明在专用的**宏包**中：`macro package <name>`
- 所有宏实现须 `import std.ast.*`

---

## 2. Token 与 Tokens 类型

### 2.1 Token 类型
- `Token` 是最小词法单元：标识符、字面量、关键字或运算符
- 每个 `Token` 有：类型（`TokenKind`）、内容、位置信息
- 构造函数：`Token(k: TokenKind)` 或 `Token(k: TokenKind, v: String)`
- 示例：`Token(TokenKind.ADD)` → `+`，`Token(TokenKind.IDENTIFIER, "x")` → `x`

### 2.2 Tokens 类型
- `Tokens` 是 `Token` 对象的序列
- 构造函数：`Tokens()`、`Tokens(tks: Array<Token>)`、`Tokens(tks: ArrayList<Token>)`
- 操作：`size`、`get(index)`、`[]` 索引、`+` 拼接、`dump()` 调试输出、`toString()` 代码字符串

### 2.3 Quote 表达式与插值
- `quote(...)` 将代码模板转换为 `Tokens`
- 在 `quote` 内使用 `$(expr)` 插值来插入实现 `ToTokens` 的表达式
- 支持 `ToTokens` 的类型：所有 AST 节点类型、`Token`/`Tokens`、所有基本类型、`Array<T>`、`ArrayList<T>`

### 2.4 Quote 转义规则
- `quote` 中未匹配的括号须用 `\` 转义：`\(` 或 `\)`
- `$` 作为字面 token（非插值）须转义：`\$`
- 输入中的 `@` 须转义：`\@`

---

## 3. 宏实现

### 3.1 非属性宏
- 定义：`public macro MacroName(args: Tokens): Tokens { ... }`
- 调用：`@MacroName(...)` 带括号，或 `@MacroName` 在声明前（括号可选）
- 可应用于：`func`、`struct`、`class`、`var`、`enum`、`interface`、`extend`、`prop` 等声明

#### 输入规则
- 输入须为合法的 `Token` 序列
- 未匹配的 `(` `)` 须用 `\` 转义

#### 展开后规则
- 展开代码须为合法仓颉代码
- 展开代码不能包含包声明或导入语句

### 3.2 属性宏
- 定义：`public macro Foo(attrTokens: Tokens, inputTokens: Tokens): Tokens { ... }`
- 有**两个** `Tokens` 参数：属性 token + 输入 token
- 调用语法：`@Foo[attrContent](inputContent)` 或 `@Foo[attrContent]` 在声明前
- 属性内容在 `[]` 中，常规内容在 `()` 中

#### 一致性规则
- 若宏定义有 2 个参数（属性宏），调用处须使用 `[]`（可为空）
- 若定义有 1 个参数（非属性宏），调用处不能使用 `[]`

### 3.3 嵌套宏
- 宏定义**不能嵌套**，但宏调用**可以**出现在宏定义和宏调用处内部
- **展开顺序**：内层宏先展开，然后外层。始终由内向外

### 3.4 嵌套宏通信

#### 上下文断言
- `assertParentContext("OuterMacroName")` — 若内层宏不在指定外层宏内则报错
- `insideParentContext("OuterMacroName")` — 返回 `Bool`

#### 消息传递（内 → 外）
- 内层宏发送数据：`setItem("key", "value")`
- 外层宏接收：`getChildMessages("InnerMacroName")` 返回消息对象集合
- 每个消息对象支持 `getString("key")` 获取值

---

## 4. std.ast 包与语法节点

### 4.1 std.ast 包概述

`std.ast` 是仓颉宏编程的核心依赖包，提供源码的词法分析和语法解析能力。主要包含：

- **词法单元**：`Token`（单个词法单元）和 `Tokens`（词法单元序列），以及 `TokenKind` 枚举（表示所有词法结构：符号、关键字、标识符等）
- **语法解析器**：将 `Tokens` 解析为抽象语法树（AST）节点对象的函数族（`parseExpr`、`parseDecl`、`parseType` 等）
- **AST 节点体系**：以 `Node` 为基类的完整语法树节点类型，涵盖声明（`Decl`）、表达式（`Expr`）、类型（`TypeNode`）、模式（`Pattern`）四大分支
- **Visitor 遍历框架**：`Visitor` 抽象类提供节点访问函数，配合 `traverse()` 实现 AST 遍历
- **嵌套宏上下文通信**：`assertParentContext`、`insideParentContext`、`setItem`、`getChildMessages` 等函数，用于宏展开时的上下文信息传递
- **诊断报告**：`diagReport` 函数在宏展开阶段输出 `ERROR`/`WARNING` 级别的编译信息
- **辅助工具**：`cangjieLex`（字符串转 Tokens）、`compareTokens`（Tokens 比较）、`ToTokens`/`ToBytes` 接口

> 所有宏实现文件须 `import std.ast.*`

### 4.2 AST 节点层次
- `Node` — 所有语法节点的基类
- `TypeNode` — 所有类型节点
- `Expr` — 所有表达式节点
- `Decl` — 所有声明节点
- `Pattern` — 所有模式节点

### 4.3 解析函数

| 函数 | 说明 |
|------|------|
| `parseExpr(Tokens)` | 解析为表达式节点 `Expr` |
| `parseDecl(Tokens)` | 解析为声明节点 `Decl` |
| `parseType(Tokens)` | 解析为类型节点 `TypeNode` |
| `parsePattern(Tokens)` | 解析为模式节点 `Pattern` |
| `parseProgram(Tokens)` | 解析整个源文件为 `Program` 节点 |
| `parseExprFragment(Tokens, Int64)` | 部分解析表达式，返回 `(Expr, Int64)` |
| `parseDeclFragment(Tokens, Int64)` | 部分解析声明，返回 `(Decl, Int64)` |

也可通过直接构造函数创建节点：`BinaryExpr(quote(a + b))`、`FuncDecl(quote(func f1(...) {...}))` 等

### 4.4 常用节点类型与属性

| 节点类 | 常用属性 |
|--------|----------|
| `FuncDecl` | `identifier`、`funcParams`、`declType`、`block`、`modifiers` |
| `ClassDecl` | `identifier`、`body`、`modifiers`、`superTypes` |
| `StructDecl` | `identifier`、`body`、`modifiers` |
| `VarDecl` | `identifier`、`declType`、`expr`、`keyword`（`var`/`let`） |
| `BinaryExpr` | `leftExpr`、`op`、`rightExpr` |
| `CallExpr` | `callExpr`、`arguments` |
| `Block` | `nodes: ArrayList<Node>` |
| `Body` | `decls: ArrayList<Decl>` |
| `FuncParam` | `identifier`、`paramType` |

### 4.5 在 Quote 中插值节点
- 任何节点：`$(node)` 在 `quote` 内
- `ArrayList<Node>` 可插值（项依次列出并换行）
- 插值**不会**自动为优先级添加括号，须手动包装

### 4.6 Visitor 遍历模式
```cangjie
import std.ast.*

class MyVisitor <: Visitor {
    public override func visit(varDecl: VarDecl) {
        println("Found var: ${varDecl.identifier.value}")
        breakTraverse()  // 不继续遍历子节点
        return
    }
}

// 使用方式：node.traverse(MyVisitor())
```

### 4.7 辅助工具函数

| 函数 | 说明 |
|------|------|
| `cangjieLex(String)` | 字符串转 `Tokens` |
| `compareTokens(Tokens, Tokens)` | 比较两个 `Tokens` |
| `diagReport(level, tokens, msg, hint)` | 宏展开阶段报错（`ERROR`/`WARNING`） |

---

## 5. 宏包编译与构建

### 5.1 包规则
- 宏须在 `macro package` 声明的包中
- 宏包中仅宏定义可为 `public`；其他声明为包内部可见
- 宏包**可以**重新导出宏包和非宏包的符号。非宏包**不能**重新导出宏包符号
- 宏定义和调用**须**在不同包中

### 5.2 使用 cjc 编译

宏包须**先编译**，使用 `--compile-macro` 标志，然后编译调用包并链接宏包：

```shell
cjc macros/m.cj --compile-macro --output-dir ./target   # 编译宏包
cjc src/demo.cj -o demo --import-path ./target           # 编译调用包

# 多模块场景
cjc A.cj --compile-macro                    # 编译宏包
cjc B.cj --output-type=dylib -o libB.so     # 编译依赖
cjc C.cj --compile-macro -L. -lB            # 编译带依赖的宏包
cjc main.cj -o main -L. -lB                 # 编译主程序
```

### 5.3 使用 cjpm 构建（推荐）

#### 项目结构
```text
my_project/
├── cjpm.toml              # 主项目配置
├── src/
│   └── main.cj            # 调用宏的代码
└── macros/                 # 宏模块
    ├── cjpm.toml           # 宏模块配置
    └── src/
        └── my_macros.cj    # 宏定义
```

#### 宏模块 cjpm.toml
```toml
[package]
cjc-version = "0.55.3"
name = "macros"
version = "1.0.0"
output-type = "static"
compile-option = "--compile-macro"
```

#### 主项目 cjpm.toml
```toml
[package]
cjc-version = "0.55.3"
name = "my_project"
version = "1.0.0"
output-type = "executable"

[dependencies]
macros = { path = "./macros" }
```

#### 构建与运行
```bash
cjpm build      # 自动按依赖顺序编译宏包和主包
cjpm run        # 构建并运行
cjpm test       # 运行测试
```

### 5.4 并行宏展开
- 使用 `--parallel-macro-expansion` 标志启用
- **警告**：使用全局变量的宏在并行展开时不安全

### 5.5 调试模式
- `--debug-macro` 生成 `.macrocall` 临时文件显示完全展开的宏代码

---

## 6. 内置编译标记

### 6.1 源码位置标记
- `@sourcePackage()` → 当前包名 `String`
- `@sourceFile()` → 当前文件名 `String`
- `@sourceLine()` → 当前行号 `Int64`

### 6.2 条件编译
- `@When` 标记用于平台适配、特性选择、调试支持和性能优化

### 6.3 `@FastNative`
- 优化 `foreign` 声明函数的 C 互操作调用
- 要求：C 函数不能有长循环、阻塞调用或回调仓颉

### 6.4 `@Frozen`
- 标记函数/属性为跨版本不可变（签名 + 体不可变）
- 可应用于：全局函数、类/结构体/接口/扩展/枚举成员函数、类/接口/扩展属性

### 6.5 `@Attribute`
- 为声明添加元数据属性
- `@Attribute[State] var cnt = 0`（标识符）或 `@Attribute["Binding"] var bcnt = 0`（字符串）

### 6.6 `@Deprecated`
- 标记 API 为已弃用，参数：
  - `message: String` — 迁移指南
  - `since!: ?String` — 弃用版本
  - `strict!: Bool` — `false` = 警告，`true` = 编译错误

---

## 7. 典型示例代码

### 7.1 快速幂（编译时代码生成）
- 属性宏 `@power[10](n)` 在编译时展开幂运算循环

### 7.2 记忆化（自动缓存）
- `@Memoize[true]` 将递归函数转换为使用 `HashMap` 缓存结果

### 7.3 扩展 dprint（多表达式打印）
- `@dprint2(x, y, x + y)` 打印多个逗号分隔的表达式

### 7.4 简单 DSL（类 LINQ 查询）
- `@linq(from x in 1..=10 where x % 2 == 1 select x * x)` 实现迷你查询语言

### 7.5 非属性宏：自动生成 toString

宏定义（`macros/src/my_macros.cj`）：
```cangjie
macro package macros

import std.ast.*

public macro AutoToString(input: Tokens): Tokens {
    let decl = parseDecl(input)
    let classDecl = match (decl as ClassDecl) {
        case Some(v) => v
        case None =>
            diagReport(DiagReportLevel.ERROR, input,
                "AutoToString 只能用于 class 声明", "此处不是 class")
            return input
    }
    let className = classDecl.identifier

    // 收集所有 var/let 成员变量名
    var fields = ArrayList<Token>()
    for (d in classDecl.body.decls) {
        if (let Some(varDecl) <- (d as VarDecl)) {
            fields.add(varDecl.identifier)
        }
    }

    // 构建 toString 方法体中的字段拼接
    var parts = quote(var result = "${$(className)}{")
    for (f in fields) {
        parts = quote($(parts)
            result += " $(f)=" + this.$(f).toString()
        )
    }
    parts = quote($(parts)
        result += " }"
        return result
    )

    // 添加 toString 方法到 class
    let toStringFunc = FuncDecl(quote(
        public func toString(): String {
            $(parts)
        }
    ))
    classDecl.body.decls.add(toStringFunc)
    return classDecl.toTokens()
}
```

调用处（`src/main.cj`）：
```cangjie
import macros.*

@AutoToString
class User {
    var name: String = ""
    var age: Int64 = 0
    init(name: String, age: Int64) {
        this.name = name
        this.age = age
    }
}

main() {
    let u = User("Alice", 30)
    println(u.toString())
    // 输出: User{ name=Alice age=30 }
}
```

### 7.6 属性宏：条件日志

```cangjie
macro package macros

import std.ast.*

public macro Log(attrTokens: Tokens, inputTokens: Tokens): Tokens {
    let level = attrTokens.toString().trimAscii()
    let funcDecl = FuncDecl(inputTokens)
    let funcName = funcDecl.identifier

    let logStmt = quote(
        println("[$(level)] entering $(funcName)")
    )

    // 在函数体开头插入日志语句
    let oldNodes = funcDecl.block.nodes
    funcDecl.block.nodes = ArrayList<Node>()
    funcDecl.block.nodes.add(parseExpr(logStmt))
    for (n in oldNodes) {
        funcDecl.block.nodes.add(n)
    }
    return funcDecl.toTokens()
}
```

调用处：
```cangjie
import macros.*

@Log[DEBUG]
func compute(x: Int64): Int64 {
    return x * 2
}
```

### 7.7 AST 操作：遍历并修改节点

```cangjie
import std.ast.*

// 查找所有函数声明并打印函数名
class FuncCollector <: Visitor {
    public var funcNames = ArrayList<String>()
    public override func visit(funcDecl: FuncDecl) {
        funcNames.add(funcDecl.identifier.value)
    }
}

main() {
    let code = quote(
        class Calc {
            func add(a: Int64, b: Int64): Int64 { a + b }
            func sub(a: Int64, b: Int64): Int64 { a - b }
        }
    )
    let decl = parseDecl(code)
    let collector = FuncCollector()
    decl.traverse(collector)
    for (name in collector.funcNames) {
        println("Found function: ${name}")
    }
    // 输出: Found function: add
    //       Found function: sub
}
```

---

## 8. 最优实践指导

### 8.1 项目组织
- 宏定义必须在 `macro package` 中，与调用代码分离为独立模块
- 使用 cjpm 管理宏模块依赖，避免手动 `cjc --compile-macro` 编译
- 宏包中仅宏定义可为 `public`，辅助函数保持包内可见

### 8.2 输入验证
- 始终验证输入节点类型，使用 `as` 模式匹配 + `diagReport` 报告错误
- 提供清晰的错误信息和位置提示，而非让编译器产生难以理解的错误

### 8.3 代码生成
- 优先使用 `quote(...)` + `$(...)` 插值生成代码，保持模板可读性
- 避免手动拼接 `Token`，除非需要动态构造标识符
- 插值不会自动添加括号，必要时手动包裹 `ParenExpr`

### 8.4 AST 操作
- 使用 `parseDecl`/`parseExpr` 将 `Tokens` 转为强类型节点后再操作
- 修改节点后用 `node.toTokens()` 转回 `Tokens` 返回
- 利用 `Visitor` 模式遍历复杂 AST，避免手动递归
- 使用 `dump()` 调试 AST 结构

### 8.5 调试与安全
- 开发阶段使用 `--debug-macro` 查看展开结果
- 避免在宏中使用全局可变状态（并行展开不安全）
- 嵌套宏通信使用 `setItem`/`getChildMessages`，而非全局变量
