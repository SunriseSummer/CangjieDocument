---
name: cangjie-package
description: "仓颉语言包管理。当需要了解仓颉语言的包声明(package)、程序入口(main)、包导入(import/import as)、重新导出(public import)、顶层访问修饰符(private/internal/protected/public)等特性时，应使用此 Skill。"
---

# 仓颉语言包管理 Skill

## 1. 包概述

### 1.1 基本概念
- **包**是最小编译单元，产生 AST/静态/动态库文件
- 每个包有自己的命名空间（顶层名称不允许重复，函数重载除外）
- **模块**是包的集合，是最小分发单元
- 模块的 `main` 入口须在其根目录中

---

## 2. 包声明

### 2.1 语法
- 使用 `package pkg1.sub1` 声明，须与相对于 `src/` 的目录路径匹配
- 须为文件中第一个非空/非注释行
- 同一包中所有文件须有相同的包声明
- 目录名须与包名匹配
- `src/` 直接下的文件默认为 `default` 包
- 子包不能与顶层声明同名
- Windows 上包名仅限 ASCII

---

## 3. 程序入口

### 3.1 `main` 函数
- `main` 是入口点，每个根包最多一个
- 不能有访问修饰符
- 被导入包时不会被导入
- 参数：无参或 `Array<String>`
- 返回类型：`Unit` 或整数类型
- 定义时不使用 `func` 关键字

---

## 4. 包导入

### 4.1 语法
```cangjie
import fullPkg.item
import fullPkg.{a, b}
import fullPkg.*
import {pkg1.*, pkg2.*}
```

### 4.2 规则
- 须在 `package` 之后、其他声明之前
- 导入成员的作用域优先级低于当前包
- 不允许循环依赖
- 不能导入当前包
- 不能导入不可见的声明

### 4.3 遮蔽/重载
- 导入的名称被同名本地声明遮蔽（除非构成函数重载，此时适用重载解析）

### 4.4 隐式 core 导入
- `String`、`Range` 等可用是因为 `core` 包被自动导入

### 4.5 import as（重命名导入）
- 重命名导入以解决冲突：`import pkg.name as newName`、`import pkg as alias`
- 重命名后原名不可用
- 不重命名时，冲突名称在使用处报错（非导入处）
- 也可 `import fullPkg` 用作命名空间限定符

### 4.6 重新导出
- `public import`、`protected import`、`internal import` 重新导出导入的成员
- `private import`（默认）将导入限制为文件内可见
- 包本身不能被重新导出

---

## 5. 顶层访问修饰符

### 5.1 四个级别
| 修饰符 | 可见性 |
|--------|--------|
| `private` | 当前文件 |
| `internal`（大多数声明的默认值） | 当前包及子包 |
| `protected` | 当前模块 |
| `public` | 全局可见 |

### 5.2 规则
- `package` 声明默认为 `public`
- `import` 默认为 `private`
- 声明的访问级别不能超过其使用的类型（参数、返回类型、泛型、where 约束）的访问级别
- 但 `public` 声明可在内部（函数体、初始化表达式中）使用非 public 类型
- 内置类型如 `Int64` 为 `public`
- 同包中同名的 `private` 声明在导出时可能导致错误
