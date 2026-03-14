---
name: cangjie-compile-and-build
description: "仓颉语言编译与构建。当需要了解仓颉语言的编译器cjc和项目管理工具cjpm的基本用法，以及条件编译(@When)特性时，应使用此 Skill。"
---

# 仓颉语言编译与构建 Skill

## 1. cjc 编译器

### 1.1 基本用法

- `cjc` 是仓颉编译器
- 用法：`cjc [option] file...`
- 编译为可执行文件，默认名称为 `main`
- 示例：`cjc hello.cj`

### 1.2 前端与后端
- `cjc-frontend` 是仅前端编译器（输出 LLVM IR）
- `cjc` 自动处理前端 + 后端 + 链接

### 1.3 主要选项
- `-o` 指定输出文件名
- `--output-type` 指定输出类型（如 `dylib`）
- `--compile-macro` 编译宏包
- `--import-path` 指定导入路径
- `-L`/`-l` 链接库路径和库名
- `--cfg` 定义条件编译变量
- `-g` 启用调试信息
- `--test` 启用测试模式
- `--debug-macro` 启用宏调试

> 如需了解 cjc 更多细节，请引用 `cangjie-cjc` Skill

---

## 2. cjpm 项目管理器

### 2.1 功能
- 管理仓颉项目：模块系统、依赖解析（多版本冲突解决）、自定义构建脚本

### 2.2 主要命令
| 命令 | 说明 |
|------|------|
| `init` | 创建项目（生成 `cjpm.toml` + `src/main.cj`） |
| `build` | 编译（支持增量/并行/交叉编译，`-V` 详细输出） |
| `run` | 运行 |
| `test` | 测试 |
| `bench` | 基准测试 |
| `clean` | 清理 |
| `install` | 安装 |
| `uninstall` | 卸载 |
| `check` | 检查 |
| `update` | 更新依赖 |
| `tree` | 显示依赖树 |

### 2.3 cjpm.toml 配置

#### [package] 区段
- `name` — 包名
- `version` — 版本
- `cjc-version` — 编译器版本
- `output-type` — 输出类型
- `compile-option` — 编译选项
- `src-dir` — 源码目录
- `target-dir` — 目标目录

#### [workspace] 区段
- `members` — 工作区成员
- `build-members` — 构建成员
- `test-members` — 测试成员

#### 其他区段
- `[dependencies]` — 依赖（git/path 来源）
- `[test-dependencies]` — 测试依赖
- `[ffi.c]` — C 库依赖
- `[profile]` — 构建/测试/基准配置
- `[target.<triple>]` — 平台特定设置

> 如需了解仓颉项目的组织构建和 cjpm 更多细节，请引用 `cangjie-project-management` Skill

---

## 3. 条件编译

### 3.1 语法
- 使用 `@When[condition]` 应用于导入/声明节点（非 `package`）
- 不允许嵌套
- 不能出现在宏生成的代码中

### 3.2 内置变量
| 变量 | 操作 | 值 |
|------|------|-----|
| `os` | `==`/`!=` | `"Windows"`、`"Linux"`、`"macOS"` |
| `backend` | `==`/`!=` | `"cjnative"` |
| `arch` | `==`/`!=` | `"x86_64"`、`"aarch64"` |
| `cjc_version` | 全部 6 种比较 | 格式 `xx.xx.xx` |
| `debug` | `!` 仅 | `-g` 启用时为 true |
| `test` | `!` 仅 | `--test` 使用时为 true |

### 3.3 自定义变量
- 通过 `--cfg "key=value"` 或 `cfg.toml` 文件定义
- 支持 `==`/`!=`
- 不能与内置变量名重复
- 多个条件可用 `&&`、`||`、`!`、`()` 组合
