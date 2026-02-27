---
name: cangjie-first-understanding
description: "仓颉语言入门。当需要了解仓颉语言的整体概述、语言特性、Hello World程序、编译运行方法、工具链安装(SDK/cjc/cjpm)等基础信息时，应使用此 Skill。"
---

# 仓颉语言初识 Skill

## 1. 语言概述

### 1.1 定位
- 仓颉是面向全场景开发的通用多范式编程语言

### 1.2 多后端
- **CJNative**：编译为原生二进制
- **CJVM**：编译为字节码

### 1.3 语言特性
- **简洁语法**：字符串插值、主构造函数、流式表达式、match、重新导出
- **多范式**：
  - 函数式：高阶函数、代数数据类型、模式匹配、泛型
  - 面向对象：封装、接口、继承、子类型多态
  - 命令式：值类型、全局函数
- **静态强类型** + 类型推断
- **内存安全**：自动 GC、边界检查
- **轻量级线程**：用户空间协程
- **C 互操作**
- **词法宏**
- **丰富的标准库**：数据结构、算法、数学、正则、网络、数据库、日志、加密、序列化等

---

## 2. Hello World

### 2.1 第一个程序
```cangjie
main() {
    println("你好，仓颉")
}
```

### 2.2 编译与运行
- Linux/macOS：`cjc hello.cj -o hello`
- Windows：`cjc hello.cj -o hello.exe`

### 2.3 注释
- 单行注释：`//`
- 多行注释：`/* */`

---

## 3. 工具链安装

### 3.1 SDK 组成
- 编译器、调试器、项目管理器、静态检查器、格式化器、覆盖率工具

### 3.2 系统要求
- Linux：glibc 2.27+、Kernel 4.15+、libstdc++ 6.0.24+、OpenSSL 3
- macOS：macOS 12.0+，需 `brew install libffi`
- Windows：可用 `.exe` 安装程序或 `.zip`

### 3.3 安装步骤（Linux/macOS）
1. 下载 tar.gz
2. 解压
3. 执行 `source cangjie/envsetup.sh`
4. 验证：`cjc -v`
5. 添加到 `.bashrc`/`.zshrc` 持久化

### 3.4 安装步骤（Windows）
1. 使用 `.exe` 安装程序或解压 `.zip`
2. Zip 方式须运行 `envsetup.bat`/`.ps1`/`.sh`
3. 持久化：设置 `CANGJIE_HOME` 环境变量，将 `bin`、`tools/bin`、`tools/lib`、`runtime/lib/...` 添加到 `Path`

### 3.5 卸载
- 删除安装目录即可
