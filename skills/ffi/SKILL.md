---
name: cangjie-ffi
description: "仓颉语言外部函数接口(FFI)。当需要了解仓颉语言与C语言互操作的foreign声明、CFunc、inout参数、unsafe块、调用约定、类型映射(CPointer/VArray/CString)、C调用仓颉、编译构建（cjc链接静态库/动态库、cjpm ffi.c配置）等特性时，应使用此 Skill。"
---

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
- 避免使用 `CJ_` 前缀的名称（可能与标准库及运行时等编译器内部符号冲突）
- 编译 C 代码时应启用 `-fstack-protector-all` 或 `-fstack-protector-strong` 栈保护选项

---

## 5. C 互操作编译构建

### 5.1 cjc 编译器链接选项
- `--library-path <value>` / `-L <value>` / `-L<value>`：指定库文件搜索目录
  - 环境变量 `LIBRARY_PATH` 中的路径也会加入搜索路径，`-L` 指定的路径优先级更高
- `--library <value>` / `-l <value>` / `-l<value>`：指定要链接的库文件
  - 库文件名格式为 `lib[arg].[extension]`（如 `-l draw` 链接 `libdraw.so` 或 `libdraw.a`）

### 5.2 使用 cjc 直接编译链接（不使用 cjpm）

**步骤 1：编译 C 代码为动态库或静态库**

Linux 平台：

```shell
# 编译为动态库（.so）
clang -shared -fPIC -fstack-protector-all hello.c -o libhello.so

# 编译为静态库（.a）
clang -c -fstack-protector-all hello.c -o hello.o
ar rcs libhello.a hello.o
```

Windows 平台：

```shell
# 编译为动态库（.dll），不需要 -fPIC 选项
clang -shared -fstack-protector-all hello.c -o hello.dll
```

> **注意：**
>
> 在 Windows 平台上，C 动态库的导出函数需要使用 `__declspec(dllexport)` 修饰，例如：
> ```c
> __declspec(dllexport) void hello() { ... }
> ```

**步骤 2：使用 cjc 编译仓颉代码并链接 C 库**

```shell
# 链接动态库
cjc -L . -l hello main.cj -o main

# 链接静态库（同样使用 -L 和 -l）
cjc -L . -l hello main.cj -o main
```

**步骤 3：运行可执行文件**

```shell
# 链接动态库时，运行需要指定动态库搜索路径
LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./main

# 链接静态库时，可直接运行
./main
```

### 5.3 使用 cjpm 项目管理器编译构建

**步骤 1：初始化项目**

```shell
cjpm init                       # 默认创建可执行项目
cjpm init --type=static         # 创建静态库项目
cjpm init --type=dynamic        # 创建动态库项目
```

**步骤 2：在 cjpm.toml 中配置 C 库依赖**

使用 `[ffi.c]` 区段配置外部 C 库依赖，将编译好的动态库或静态库放到指定 `path` 下：

```toml
[package]
  name = "demo"
  cjc-version = "0.1.0"
  version = "1.0.0"
  output-type = "executable"

[ffi.c]
hello = { path = "./libs/" }  # hello 为库名，path 为 libhello.so 或 libhello.a 所在目录
```

**步骤 3：构建和运行**

```shell
cjpm build            # 构建项目，自动链接 [ffi.c] 中配置的 C 库
cjpm build -V         # 构建并打印详细的编译命令
cjpm run              # 构建并运行
```

### 5.4 cjpm.toml 中与编译链接相关的配置项

- `output-type`：输出产物类型，可选 `"executable"`（可执行程序）、`"static"`（静态库）、`"dynamic"`（动态库）
- `compile-option`：传给 `cjc` 的额外编译选项，如 `compile-option = "-O1"`
- `link-option`：传给链接器的选项，如 `link-option = "-z noexecstack -z relro -z now"`
- `[ffi.c]`：配置 C 库依赖，格式为 `库名 = { path = "库文件目录" }`

### 5.5 完整示例：仓颉调用 C 库

C 代码（`draw.c`）：

Linux 平台：

```c
#include<stdio.h>
#include<stdint.h>

typedef struct {
    int64_t x;
    int64_t y;
} Point;

void drawPoint(Point* point) {
    point->x = 1;
    point->y = 2;
    printf("Draw Point: (%lld, %lld)\n", point->x, point->y);
}
```

Windows 平台（导出函数需加 `__declspec(dllexport)` 修饰）：

```c
#include<stdio.h>
#include<stdint.h>

typedef struct {
    int64_t x;
    int64_t y;
} Point;

__declspec(dllexport) void drawPoint(Point* point) {
    point->x = 1;
    point->y = 2;
    printf("Draw Point: (%lld, %lld)\n", point->x, point->y);
}
```

仓颉代码（`main.cj`）：

```cangjie
@C
struct Point {
    var x: Int64 = 0
    var y: Int64 = 0
}

foreign func drawPoint(point: CPointer<Point>): Unit

main() {
    let pPoint = unsafe { LibC.malloc<Point>() }
    unsafe {
        drawPoint(pPoint)
        println(pPoint.read().x)  // 1
        println(pPoint.read().y)  // 2
        LibC.free(pPoint)
    }
}
```

**方式一：使用 cjc 直接编译**

Linux 平台：

```shell
clang -shared -fPIC -fstack-protector-all draw.c -o libdraw.so
cjc -L . -l draw main.cj -o main
LD_LIBRARY_PATH=.:$LD_LIBRARY_PATH ./main
```

Windows 平台：

```shell
clang -shared -fstack-protector-all draw.c -o draw.dll
cjc -L . -l draw main.cj -o main.exe
main.exe
```

**方式二：使用 cjpm 项目编译**

项目结构：

```text
myproject/
├── cjpm.toml
├── libs/
│   └── libdraw.so
└── src/
    └── main.cj
```

`cjpm.toml` 配置：

```toml
[package]
  name = "myproject"
  cjc-version = "0.1.0"
  version = "1.0.0"
  output-type = "executable"

[ffi.c]
draw = { path = "./libs/" }
```

```shell
cjpm build
cjpm run
```

---

## 6. 使用约束
- 线程局部变量有风险（仓颉线程任意调度到 OS 线程）
- 不推荐线程绑定/亲和性
- 阻塞 C 调用会阻塞仓颉线程
- `fork()` 子进程不能执行仓颉逻辑
- C 中的进程退出可能导致非法访问
