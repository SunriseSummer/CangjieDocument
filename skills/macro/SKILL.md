---
name: cangjie-macro
description: "仓颉语言宏。当需要了解仓颉语言的Token/Tokens类型、quote表达式与插值、非属性宏、属性宏、嵌套宏与通信、语法节点(AST)解析、宏包编译、内置编译标记(@sourceFile/@When/@FastNative/@Frozen/@Deprecated等)时，应使用此 Skill。"
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
- `InsideParentContext("OuterMacroName")` — 返回 `Bool`

#### 消息传递（内 → 外）
- 内层宏发送数据：`setItem("key", "value")`
- 外层宏接收：`getChildMessages("InnerMacroName")` 返回消息对象集合
- 每个消息对象支持 `getString("key")` 获取值

---

## 4. 语法节点

### 4.1 AST 节点层次
- `Node` — 所有语法节点的基类
- `TypeNode` — 所有类型节点
- `Expr` — 所有表达式节点
- `Decl` — 所有声明节点
- `Pattern` — 所有模式节点

### 4.2 将 Tokens 解析为节点

#### 方法一 — 解析函数
- `parseExpr(input: Tokens): Expr`
- `parseExprFragment(input: Tokens, startFrom!: Int64 = 0): (Expr, Int64)` — 部分解析
- `parseDecl(input: Tokens, astKind!: String = "")`
- `parseDeclFragment(input: Tokens, startFrom!: Int64 = 0): (Decl, Int64)`
- `parseType(input: Tokens): TypeNode`
- `parsePattern(input: Tokens): Pattern`

#### 方法二 — 直接构造函数
- `BinaryExpr(quote(a + b))`、`FuncDecl(quote(func f1(...) {...}))` 等

### 4.3 节点属性
- `BinaryExpr`：`leftExpr: Expr`、`op: Token`、`rightExpr: Expr`
- `FuncDecl`：`identifier: Token`、`funcParams: ArrayList<FuncParam>`、`declType: TypeNode`、`block: Block`
- `FuncParam`：`identifier: Token`、`paramType: TypeNode`
- `Block`：`nodes: ArrayList<Node>`

### 4.4 在 Quote 中插值节点
- 任何节点：`$(node)` 在 `quote` 内
- `ArrayList<Node>` 可插值（项依次列出并换行）
- 插值**不会**自动为优先级添加括号。须手动包装

---

## 5. 宏包定义与导入

### 5.1 包规则
- 宏须在 `macro package` 声明的包中
- 宏包中仅宏定义可为 `public`；其他声明为包内部可见
- 宏包**可以**重新导出宏包和非宏包的符号。非宏包**不能**重新导出宏包符号

### 5.2 编译顺序
- 宏包须**先编译**，使用 `--compile-macro` 标志
- 然后编译调用包，链接宏包
- 宏必须为 `public`（跨包导出）

### 5.3 编译示例
```shell
cjc A.cj --compile-macro                    # 编译宏包
cjc B.cj --output-type=dylib -o libB.so     # 编译依赖
cjc C.cj --compile-macro -L. -lB            # 编译带依赖的宏包
cjc main.cj -o main -L. -lB                 # 编译主程序
```

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

## 7. 编译、错误报告与调试

### 7.1 编译工作流
1. 宏定义和调用**须**在不同包中
2. 先编译宏包：`cjc macros/m.cj --compile-macro --output-dir ./target`
3. 编译调用包：`cjc src/demo.cj -o demo --import-path ./target`

### 7.2 并行宏展开
- 使用 `--parallel-macro-expansion` 标志启用
- **警告**：使用全局变量的宏在并行展开时不安全

### 7.3 diagReport 错误报告
- `diagReport(level: DiagReportLevel, tokens: Tokens, message: String, hint: String)`
- `level`：`DiagReportLevel.ERROR` 或 `DiagReportLevel.WARNING`

### 7.4 调试模式
- `--debug-macro` 生成 `.macrocall` 临时文件显示完全展开的宏代码

---

## 8. 实践案例

### 8.1 快速幂（编译时代码生成）
- 属性宏 `@power[10](n)` 在编译时展开幂运算循环

### 8.2 记忆化（自动缓存）
- `@Memoize[true]` 将递归函数转换为使用 `HashMap` 缓存结果

### 8.3 扩展 dprint（多表达式打印）
- `@dprint2(x, y, x + y)` 打印多个逗号分隔的表达式

### 8.4 简单 DSL（类 LINQ 查询）
- `@linq(from x in 1..=10 where x % 2 == 1 select x * x)` 实现迷你查询语言
