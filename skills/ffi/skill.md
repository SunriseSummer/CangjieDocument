# 仓颉语言外部函数接口（FFI）Skill

## 1. 从仓颉调用 C

### 1.1 外部函数声明
- 使用 `foreign func` 声明 C 函数：`foreign func rand(): Int32`
- `@C` 修饰符可选
- 所有对 `foreign` 函数的调用须包装在 `unsafe {}` 块中
- `foreign` 函数不能有函数体，不支持命名参数或默认值，但允许末尾的变长参数（`...`）

### 1.2 CFunc
- 三种形式：
  1. `@C foreign func`
  2. `@C` 仓颉函数
  3. `CFunc<...>` Lambda 表达式（不能捕获变量）
- CFunc 对应 C 函数指针
- `CPointer<T>` 可转换为 `CFunc`

### 1.3 inout 参数
- `inout` 关键字以 `CPointer<T>` 的形式按引用传递参数
- 约束：仅用于 CFunc 调用，被修改的对象须满足 `CType`（非 `CString`），不能是 `let` 绑定/字面量/临时值，不能来源于 `class` 实例成员
- 指针仅在调用期间有效

### 1.4 unsafe
- 标记不安全的 C 互操作代码
- 可修饰函数、表达式或作用域块
- 调用 `foreign`、`@C` 或 `CFunc` 函数时须使用
- 普通 Lambda 不传播 `unsafe` — 须在 Lambda 内使用 `unsafe {}` 块

### 1.5 调用约定
- `@CallingConv[CDECL]`（默认）和 `@CallingConv[STDCALL]`（Win32 API）
- 适用于 `foreign` 块、单个 `foreign` 函数和顶层 `CFunc` 函数

---

## 2. 类型映射

### 2.1 基本类型
| 仓颉类型 | C 类型 |
|----------|--------|
| `Unit` | `void` |
| `Bool` | `bool` |
| `Int8/16/32/64` | `int8_t/16_t/32_t/64_t` |
| `UInt8/16/32/64` | `uint8_t/16_t/32_t/64_t` |
| `IntNative` | `ssize_t` |
| `UIntNative` | `size_t` |
| `Float32` | `float` |
| `Float64` | `double` |

### 2.2 结构体
- `@C struct` 映射到 C 结构体
- 须满足：成员为 CType，无接口/扩展，无枚举关联值，无闭包捕获，无泛型

### 2.3 指针
- `CPointer<T>` 映射到 C 指针
- 支持 读/写/偏移/空检查/转换
- 读/写/偏移为 unsafe 操作

### 2.4 数组
- `VArray<T, $N>` 映射到 C 数组
- 可作为 `@C struct` 成员或函数参数（以 `CPointer<T>` 传递）
- 不能作为返回类型
- 不支持柔性数组

### 2.5 字符串
- `CString` 类型，提供 `size()`、`isEmpty()`、`equals()`、`toString()` 等方法
- `String` → `CString`：通过 `LibC.mallocCString()`（使用后须释放）

### 2.6 sizeOf/alignOf
- `sizeOf<T>()` 和 `alignOf<T>()` 返回 CType 类型的内存大小/对齐

---

## 3. CType 接口
- 空接口，作为所有 C 互操作类型的父类型
- 不能被继承或扩展

---

## 4. C 调用仓颉
- 使用 `@C` 函数或 `CFunc` Lambda
- 避免使用 `CJ_` 前缀的名称
- 链接：`cjc -L. -lmyfunc`
- 编译 C 代码时启用 `-fstack-protector-all`

---

## 5. 使用约束
- 线程局部变量有风险（仓颉线程任意调度到 OS 线程）
- 不推荐线程绑定/亲和性
- 阻塞 C 调用会阻塞仓颉线程
- `fork()` 子进程不能执行仓颉逻辑
- C 中的进程退出可能导致非法访问
