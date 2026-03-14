---
name: cangjie-annotation
description: "仓颉语言内置注解。当需要了解仓颉 SDK 提供的内置注解（@sourcePackage/@sourceFile/@sourceLine/@When/@FastNative/@Frozen/@Attribute/@Deprecated）的用途、语法和最优实践时，应使用此 Skill。"
---

# 仓颉语言内置注解 Skill

仓颉 SDK 提供了一组内置注解，开发者可直接作为工具使用，无需自行实现宏。它们涵盖源码定位、条件编译、性能优化、ABI 稳定性、元数据标记和废弃管理等场景。

---

## 1. 源码位置标记

获取当前代码位置信息，常用于日志、调试和错误报告。

| 注解 | 返回类型 | 说明 |
|------|----------|------|
| `@sourcePackage()` | `String` | 当前包名 |
| `@sourceFile()` | `String` | 当前文件名 |
| `@sourceLine()` | `Int64` | 当前行号 |

### 最优实践

- 封装到统一日志函数中，避免在业务代码中散落大量位置标记调用
- 配合自定义日志宏使用，自动注入位置信息

### 示例

```cangjie
func logError(msg: String) {
    let pkg = @sourcePackage()
    let file = @sourceFile()
    let line = @sourceLine()
    println("[ERROR] ${pkg}/${file}:${line} - ${msg}")
}
```

---

## 2. 条件编译 `@When`

根据编译条件选择性编译代码，用于平台适配、特性选择和调试支持。

### 语法

```cangjie
@When[condition]
```

条件表达式支持：
- `os == "Linux"` / `os == "Windows"` / `os == "macOS"` — 操作系统判断
- `arch == "x86_64"` / `arch == "aarch64"` — 处理器架构判断
- `debug` / `!debug` — 调试/发布模式
- 逻辑组合：`&&`、`||`、`!`

### 最优实践

- 将平台相关代码集中到独立文件或模块，用 `@When` 在顶层声明上条件选择，减少代码内部的条件分支
- 优先通过抽象接口 + `@When` 切换实现，而非在函数体内散布条件编译块
- 避免过度嵌套条件，保持可读性

### 示例

```cangjie
@When[os == "Linux"]
func getPlatformName(): String {
    return "Linux"
}

@When[os == "Windows"]
func getPlatformName(): String {
    return "Windows"
}

@When[os == "macOS"]
func getPlatformName(): String {
    return "macOS"
}
```

---

## 3. 性能优化 `@FastNative`

优化 `foreign` 声明函数的 C 互操作调用开销。

### 语法

```cangjie
@FastNative
foreign func c_function_name(param: CInt): CInt
```

### 约束条件

被标记的 C 函数**必须**满足：
- 不含长时间循环
- 不含阻塞调用（如 I/O、锁等待）
- 不回调仓颉函数

### 最优实践

- 仅对执行时间短、调用频率高的 C 函数使用，如数学运算、内存操作等
- 对不确定执行时间的 C 函数，不要使用此注解，否则可能阻塞仓颉运行时调度
- 配合 `cjprof` 性能分析确认热点后再标记，避免过早优化

### 示例

```cangjie
// 适合：简单数学计算
@FastNative
foreign func fast_add(a: CInt, b: CInt): CInt

// 不适合：可能阻塞的 I/O 操作
// @FastNative  // ← 不要这样做
foreign func read_file(path: CPointer<UInt8>): CInt
```

---

## 4. ABI 冻结 `@Frozen`

标记函数或属性为跨版本不可变（签名和实现体均不可变），用于保证 ABI 稳定性。

### 可应用目标

- 全局函数
- 类、结构体、接口、扩展、枚举的成员函数
- 类、接口、扩展的属性

### 最优实践

- 仅对已稳定、不再变更的公共 API 使用
- 在库的正式发布版本中标记，开发阶段避免过早冻结
- 冻结前仔细审查函数签名和实现，冻结后无法修改

### 示例

```cangjie
@Frozen
public func stableApiVersion(): String {
    return "1.0.0"
}
```

---

## 5. 元数据标记 `@Attribute`

为声明添加元数据属性，可在运行时通过反射读取。

### 语法

```cangjie
// 标识符形式
@Attribute[State]
var cnt = 0

// 字符串形式
@Attribute["Binding"]
var bcnt = 0
```

### 最优实践

- 用于框架级标记（如状态管理、数据绑定、序列化控制等），避免在普通业务代码中滥用
- 配合 `TypeInfo.findAnnotation` 反射 API 读取属性值
- 属性名使用有意义的标识符，保持语义清晰

### 示例

```cangjie
@Attribute[Serializable]
class UserConfig {
    @Attribute["json_name:user_id"]
    var userId: String = ""

    @Attribute["json_name:display_name"]
    var displayName: String = ""
}
```

---

## 6. 废弃标记 `@Deprecated`

标记 API 为已弃用，引导开发者迁移到新 API。

### 参数

| 参数 | 类型 | 说明 |
|------|------|------|
| `message` | `String` | 迁移指南，说明替代方案 |
| `since!` | `?String` | 弃用起始版本（可选） |
| `strict!` | `Bool` | `false` = 编译警告（默认），`true` = 编译错误 |

### 最优实践

- `message` 中必须说明替代方案，而非仅提示"已弃用"
- 初期使用 `strict!: false`（警告），给下游充分迁移时间；在后续版本升级为 `strict!: true`（错误）
- `since!` 始终填写版本号，方便追溯弃用时间线

### 示例

```cangjie
@Deprecated[message: "请使用 newConnect()，旧接口将在 v3.0 移除",
            since!: "2.1.0",
            strict!: false]
public func oldConnect(host: String): Connection {
    return newConnect(host)
}
```
