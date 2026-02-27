# 仓颉工具链精炼总结

> 本文档面向 AI 工具，精炼覆盖仓颉（Cangjie）工具链的全部常用命令与配置，侧重 `cjpm` 项目管理工具。

---

## 1. 工具链总览

| 工具 | 用途 |
|------|------|
| `cjc` | 编译器 |
| `cjpm` | 项目管理工具（构建、依赖管理、测试、运行） |
| `cjdb` | 调试器（基于 lldb） |
| `cjfmt` | 代码格式化 |
| `cjlint` | 静态代码检查 |
| `cjcov` | 覆盖率统计 |
| `cjprof` | 性能分析（CPU 采样、堆内存分析） |
| `cjtrace-recover` | 异常堆栈信息还原 |
| `chir-dis` | CHIR 反序列化（编译中间产物可视化） |
| `LSPServer` | 语言服务器（IDE 支持） |

**安装**：解压 SDK 包后执行 `source cangjie/envsetup.sh`（Linux/macOS）或运行 `envsetup.bat`（Windows），验证 `cjc -v`。

---

## 2. cjc 编译器

### 2.1 基本用法

```bash
cjc hello.cj                    # 编译为默认可执行文件 main
cjc hello.cj -o hello           # 指定输出文件名
cjc -p src/                     # 整包编译
```

### 2.2 常用编译选项

| 选项 | 说明 |
|------|------|
| `-o, --output <file>` | 指定输出文件路径 |
| `-p, --package` | 整包编译（目录） |
| `--output-type=[exe\|staticlib\|dylib]` | 输出类型 |
| `--module-name <name>` | 指定模块名 |
| `-g` | 生成调试信息（仅 -O0） |
| `-O0 / -O1 / -O2 / -Os / -Oz` | 优化级别 |
| `-l, --library <name>` | 链接库文件 |
| `-L, --library-path <dir>` | 库搜索路径 |
| `--import-path <dir>` | AST 文件搜索路径 |
| `--static` | 静态链接仓颉库（仅 Linux） |
| `--coverage` | 生成覆盖率支持（仅 -O0） |
| `--test` | 编译用于单元测试 |
| `--test-only` | 仅编译 `_test.cj` 文件 |
| `--mock [on\|off\|runtime-error]` | Mock 编译支持 |
| `--cfg "key = value"` | 自定义条件编译 |
| `--compile-macro` | 编译宏定义 |
| `--debug-macro` | 生成宏展开源码 |
| `-j, --jobs <N>` | 并行编译线程数 |
| `--lto=[full\|thin]` | 链接时优化 |
| `--int-overflow=[throwing\|wrapping\|saturating]` | 整数溢出策略 |
| `-v, --version` | 显示版本 |
| `-h, --help` | 显示帮助 |

### 2.3 代码混淆选项

| 选项 | 说明 |
|------|------|
| `--fobf-all` | 启用全部混淆 |
| `--fobf-string` | 字符串常量混淆 |
| `--fobf-const` | 数值常量混淆 |
| `--fobf-layout` | 符号/路径/行号/函数布局混淆 |
| `--fobf-cf-flatten` | 控制流平坦化混淆 |
| `--fobf-cf-bogus` | 虚假控制流混淆 |
| `--obf-sym-output-mapping <file>` | 输出符号映射文件 |

### 2.4 PGO（Profile-Guided Optimization）

```bash
cjc --pgo-instr-gen -o app app.cj    # 生成插桩可执行文件
./app                                  # 运行收集 profile
cjc --pgo-instr-use=default.profdata -O2 -o app app.cj  # 使用 profile 优化
```

---

## 3. cjpm 项目管理工具（重点）

### 3.1 项目初始化

```bash
cjpm init                              # 初始化可执行模块
cjpm init --name myapp                 # 指定模块名
cjpm init --type static               # 静态库模块
cjpm init --type dynamic              # 动态库模块
cjpm init --workspace                  # 初始化工作区
cjpm init --path ./submodule           # 指定路径
```

生成结构：
```
project/
├── cjpm.toml      # 项目配置文件
└── src/
    └── main.cj    # 入口文件（executable 类型）
```

### 3.2 构建

```bash
cjpm build                             # 编译项目
cjpm build -i                          # 增量编译
cjpm build -g                          # 调试版本
cjpm build -j 8                        # 8 线程并行编译
cjpm build -V                          # 显示详细编译命令
cjpm build --coverage                  # 生成覆盖率信息
cjpm build --cfg "feature=debug"       # 条件编译
cjpm build --target <triple>           # 交叉编译
cjpm build --target-dir ./out          # 指定输出目录
cjpm build -o myapp                    # 指定可执行文件名
cjpm build -l                          # 同时运行 cjlint 静态检查
cjpm build --mock on                   # 启用 Mock
cjpm build --skip-script               # 跳过构建脚本
cjpm build -m member_name              # 编译工作区指定成员
```

产物目录：`target/release/bin/`（release）或 `target/debug/bin/`（debug）。

### 3.3 运行

```bash
cjpm run                               # 编译并运行
cjpm run -g                            # 调试模式运行
cjpm run --name myapp                  # 指定二进制名
cjpm run --skip-build                  # 跳过编译直接运行
cjpm run --build-args "-V"             # 传递构建参数
cjpm run --run-args "arg1 arg2"        # 传递运行参数
```

### 3.4 测试

```bash
cjpm test                              # 运行所有测试
cjpm test -g                           # 调试模式测试
cjpm test -i                           # 增量编译测试
cjpm test --coverage                   # 生成测试覆盖率
cjpm test --filter "test_name"         # 过滤测试用例
cjpm test --include-tags "tag1"        # 按 @Tag 包含
cjpm test --exclude-tags "tag2"        # 按 @Tag 排除
cjpm test --parallel true              # 并行执行测试
cjpm test --timeout-each 30s           # 单个测试超时
cjpm test --report-path ./reports      # 报告输出路径
cjpm test --report-format xml          # XML 格式报告
cjpm test --dry-run                    # 仅打印不执行
cjpm test --no-run                     # 仅编译不运行
cjpm test --skip-build                 # 仅运行不编译
cjpm test -j 4                         # 并行编译线程数
```

### 3.5 基准测试

```bash
cjpm bench                             # 运行基准测试
cjpm bench --report-format csv         # CSV 报告格式
cjpm bench --baseline-path base.csv    # 对比基准数据
```

### 3.6 依赖管理

```bash
cjpm check                             # 检查依赖，显示编译顺序
cjpm update                            # 更新 cjpm.lock
cjpm tree                              # 显示包依赖树
cjpm tree -V                           # 显示版本和路径详情
cjpm tree --depth 3                    # 限制树深度
cjpm tree --invert pkg_name            # 反向依赖查询
cjpm tree --no-tests                   # 排除测试依赖
```

### 3.7 安装与卸载

```bash
cjpm install                           # 安装当前项目二进制
cjpm install --path ./project          # 安装本地项目
cjpm install --git <url> --branch main # 从 Git 安装
cjpm install --git <url> --tag v1.0    # 按 Tag 安装
cjpm install --root /usr/local         # 指定安装目录
cjpm install --list                    # 列出已安装二进制
cjpm uninstall <name>                  # 卸载
```

### 3.8 清理

```bash
cjpm clean                             # 清理构建产物
cjpm clean -g                          # 仅清理 debug 产物
cjpm clean --target-dir ./out          # 清理指定目录
```

### 3.9 cjpm.toml 配置文件详解

#### [package] 段（与 [workspace] 互斥）

```toml
[package]
cjc-version = "0.53.4"                 # 最低 cjc 版本（必填）
name = "myapp"                         # 模块名/根包名（必填）
version = "1.0.0"                      # 模块版本（必填）
description = "My application"         # 描述（可选）
output-type = "executable"             # 输出类型：executable / static / dynamic（必填）
src-dir = "src"                        # 源码目录（可选）
target-dir = "target"                  # 产物目录（可选）
compile-option = "-O2"                 # 额外编译选项（可选）
override-compile-option = ""           # 全局覆盖编译选项（可选）
link-option = ""                       # 链接器选项（可选）
```

**package-configuration**（单包配置）：
```toml
[package.package-configuration.pkgA]
compile-option = "--warn-off all"
output-type = "static"
```

#### [workspace] 段

```toml
[workspace]
members = ["module_a", "module_b"]     # 工作区成员（必填）
build-members = ["module_a"]           # 要编译的成员（可选）
test-members = ["module_a"]            # 要测试的成员（可选）
compile-option = ""                    # 应用于所有成员（可选）
target-dir = "target"                  # 产物目录（可选）
```

#### [dependencies] 段

```toml
[dependencies]
# 本地路径依赖
mylib = { path = "./libs/mylib" }
# Git 依赖（支持 branch / tag / commit）
utils = { git = "https://example.com/utils.git", branch = "main" }
utils = { git = "https://example.com/utils.git", tag = "v1.0.0" }
utils = { git = "https://example.com/utils.git", commit = "abc123" }
```

#### [test-dependencies] 段

```toml
[test-dependencies]
# 同 dependencies 格式，仅用于测试阶段
testlib = { path = "./libs/testlib" }
```

#### [script-dependencies] 段

```toml
[script-dependencies]
# 同 dependencies 格式，用于构建脚本
buildtool = { path = "./tools/buildtool" }
```

#### [replace] 段

```toml
[replace]
# 替换间接依赖
oldlib = { path = "./libs/newlib" }
```

#### [ffi.c] 段

```toml
[ffi.c]
# C 语言库依赖
mylib.path = "/usr/local/lib"
```

#### [profile] 段

```toml
[profile.build]
lto = "full"                           # 链接时优化

[profile.test]
filter = "test_add"                    # 测试过滤
timeout-each = "30s"                   # 超时
parallel = true                        # 并行

[profile.bench]
report-format = "csv"                  # 基准报告格式

[profile.run]
run-args = "arg1 arg2"                 # 运行参数

[profile.customized-option]
feature = "advanced"                   # 自定义 cfg 选项
```

#### [target.PLATFORM] 段（平台特定配置）

```toml
[target.x86_64-unknown-linux-gnu]
compile-option = "-O2"
link-option = ""

[target.x86_64-unknown-linux-gnu.dependencies]
linux-lib = { path = "./libs/linux" }

[target.x86_64-unknown-linux-gnu.bin-dependencies]
path-option = ["./test/pro0"]

[target.x86_64-unknown-linux-gnu.bin-dependencies.package-option]
"pro0.xoo" = "./test/pro0/pro0.xoo.cjo"
```

---

## 4. cjdb 调试器

### 4.1 启动

```bash
cjc -g hello.cj -o hello              # 编译时须加 -g
cjdb hello                             # 启动调试
cjdb                                   # 启动后用 file hello 加载
```

### 4.2 常用命令

| 命令 | 说明 |
|------|------|
| `run` / `r` | 运行程序 |
| `continue` / `c` | 继续执行 |
| `step` / `s` | 步入函数 |
| `next` / `n` | 步过 |
| `finish` | 跳出当前函数 |
| `breakpoint set --file f.cj --line N` | 源码行断点 |
| `breakpoint set --name func` | 函数断点 |
| `breakpoint set --condition expr` | 条件断点 |
| `watchpoint set variable -w write var` | 写入监视点 |
| `locals` | 查看所有局部变量 |
| `globals` | 查看全局变量 |
| `print var` | 打印变量 |
| `set var=value` | 修改变量值 |
| `expr expression` | 求值表达式 |
| `cjthread list` | 列出仓颉线程 |
| `cjthread backtrace N` | 仓颉线程调用栈 |
| `attach PID` | 附加到进程 |
| `kill` | 终止程序 |

---

## 5. cjfmt 格式化工具

```bash
cjfmt -f hello.cj                     # 格式化单个文件
cjfmt -d src/                         # 格式化整个目录
cjfmt -f hello.cj -o formatted.cj     # 输出到指定文件
cjfmt -c cangjie-format.toml -f hello.cj  # 使用自定义配置
cjfmt -l 10:20 -f hello.cj            # 仅格式化第 10-20 行
```

**配置文件** `cangjie-format.toml`：

```toml
indentWidth = 4                        # 缩进宽度（0-8，默认 4）
linelimitLength = 120                  # 行宽限制（1-120，默认 120）
lineBreakType = "LF"                   # 换行类型：LF 或 CRLF
```

---

## 6. cjlint 静态检查工具

```bash
cjlint -f src/                        # 检查目录
cjlint -f src/ -o report.json         # 输出报告
cjlint -f src/ -r csv                 # CSV 格式报告
cjlint -f src/ -e "test:vendor"       # 排除目录（正则，冒号分隔）
cjlint -f src/ -c ./config            # 指定配置目录
cjlint -f src/ --import-path ./libs   # 添加 .cjo 搜索路径
```

**代码内抑制警告**：
```cangjie
/* cjlint-ignore !RULE_ID */           // 单行抑制
/* cjlint-ignore -start !RULE_ID */    // 多行抑制开始
/* cjlint-ignore -end */               // 多行抑制结束
```

---

## 7. cjcov 覆盖率工具

```bash
# 工作流
cjc --coverage -o app app.cj          # 编译时启用覆盖率
./app                                  # 运行程序收集数据
cjcov -r . -o ./coverage              # 生成 HTML 报告

# 常用选项
cjcov -r . -o ./out --html-details    # 每个源文件单独 HTML
cjcov -r . -x                         # XML 报告
cjcov -r . -j                         # JSON 报告
cjcov -r . -b                         # 分支覆盖率（实验性）
cjcov -r . -s src/ -e "test/*"        # 指定源码目录，排除测试
```

---

## 8. cjprof 性能分析工具

### CPU 采样分析

```bash
cjprof record ./app                    # 采集 CPU 数据
cjprof record -f 10000 ./app           # 指定采样频率（Hz）
cjprof record -o my.data ./app         # 指定输出文件
cjprof record -p <PID>                 # 附加到已运行进程

cjprof report                          # 生成报告
cjprof report -F                       # 生成火焰图（SVG）
cjprof report -i my.data               # 指定输入文件
cjprof report -o report.svg            # 指定输出文件
```

### 堆内存分析

```bash
cjprof heap -d <PID>                   # dump 进程堆
cjprof heap -i heap.data               # 分析堆数据
cjprof heap -i heap.data --show-reference  # 显示对象引用
cjprof heap -i heap.data -t            # 显示线程堆栈
```

**注意**：仅 Linux 平台支持，需要 root 权限或 `perf_event_paranoid=-1`。

---

## 9. cjtrace-recover 堆栈还原工具

```bash
cjtrace-recover -f stacktrace.txt -m mapping1.txt,mapping2.txt
```

- 使用混淆映射文件（`--obf-sym-output-mapping` 生成）还原混淆后的异常堆栈。

---

## 10. chir-dis CHIR 反序列化工具

```bash
chir-dis package.chir                  # 生成 package.chirtxt（可读文本）
```

---

## 11. LSPServer 语言服务器

```bash
LSPServer                             # 启动语言服务器
LSPServer --enable-log=true           # 启用日志
LSPServer --log-path=/var/log/cj      # 指定日志目录
LSPServer -V                          # 启用崩溃日志
LSPServer --disableAutoImport         # 禁用自动导入补全
```

- 支持 LSP 协议，可与 VSCode 等 IDE 集成。

---

## 12. 运行时环境变量

### 堆与内存

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `cjHeapSize` | 256MB | 最大堆大小 |
| `cjRegionSize` | 64KB | 线程本地缓冲区大小 |
| `cjLargeThresholdSize` | 32KB | 大对象阈值 |
| `cjStackSize` | 128KB | 线程栈大小 |

### GC 配置

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `cjHeapUtilization` | 0.8 | 堆利用率 |
| `cjGCThreshold` | 堆大小 | GC 水线 |
| `cjGCInterval` | 150ms | GC 最小间隔 |
| `cjBackupGCInterval` | 240s | 备份 GC 间隔 |

### 线程

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `cjProcessorNum` | CPU 核心数 | 最大并发仓颉线程数 |

### 日志

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `MRT_LOG_LEVEL` | `e` | 日志级别（v/d/i/w/e/f/s） |
| `MRT_LOG_PATH` | stdout | 日志输出路径 |
| `MRT_REPORT` | 无 | GC 日志输出路径 |

---

## 13. 典型开发流程

```bash
# 1. 初始化项目
cjpm init --name myapp

# 2. 编辑源代码
#    src/main.cj

# 3. 添加依赖（编辑 cjpm.toml）
#    [dependencies]
#    mylib = { git = "https://...", branch = "main" }

# 4. 构建
cjpm build

# 5. 运行
cjpm run

# 6. 测试
cjpm test

# 7. 格式化代码
cjfmt -d src/

# 8. 静态检查
cjlint -f src/

# 9. 覆盖率分析
cjpm build --coverage
cjpm run
cjcov -r . -o ./coverage --html-details

# 10. 性能分析
cjprof record -- cjpm run
cjprof report -F

# 11. 调试
cjpm build -g
cjdb target/debug/bin/myapp

# 12. 安装发布
cjpm install
```
