---
name: cangjie-deploy-and-run
description: "仓颉语言部署与运行。当需要了解仓颉编译产物的运行方式（直接执行或cjpm run）、运行时(runtime)部署方法（Linux/macOS/Windows）、静态链接免部署方案、环境变量配置(LD_LIBRARY_PATH/DYLD_LIBRARY_PATH/PATH)等信息时，应使用此 Skill。"
---

# 仓颉语言部署与运行 Skill

## 1. 运行仓颉可执行文件

### 1.1 两种运行方式

#### 直接执行
- **Linux/macOS**：先部署运行时（见下文），然后运行 `./main`。使用 `cjpm` 时，可执行文件位于 `target/release/bin/main`
- **Windows**：先部署运行时，然后运行 `.\main.exe`。使用 `cjpm` 时，位于 `target\release\bin\main.exe`

#### 使用 cjpm
- 在目标环境安装完整仓颉工具链，复制整个项目，然后执行 `cjpm run`

---

## 2. 运行时部署

### 2.1 概述
- 运行时提供内存管理和系统资源访问（动态库）支持
- 安装完整工具链时已包含运行时
- 若仅需运行（不需编译），可单独部署运行时

### 2.2 静态链接免部署
- 若编译时使用 `--static`（全静态链接），**无需部署运行时** — 所有内容嵌入可执行文件中

### 2.3 Linux 部署
1. 下载对应架构的 SDK：`cangjie-sdk-linux-x64-x.y.z.tar.gz` 或 `cangjie-sdk-linux-aarch64-x.y.z.tar.gz`
2. 解压获得 `cangjie/` 目录；运行时库位于 `cangjie/runtime/`
3. 设置环境变量：
```bash
export LD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/linux_${hw_arch}_cjnative:${LD_LIBRARY_PATH}
```

### 2.4 macOS 部署
1. 下载：`cangjie-sdk-mac-x64-x.y.z.tar.gz` 或 `cangjie-sdk-mac-aarch64-x.y.z.tar.gz`
2. 解压；运行时位于 `cangjie/runtime/`
3. 设置环境变量：
```bash
export DYLD_LIBRARY_PATH=${CANGJIE_HOME}/runtime/lib/darwin_${hw_arch}_cjnative:${DYLD_LIBRARY_PATH}
```

### 2.5 Windows 部署
1. 下载：`cangjie-sdk-windows-x64-x.y.z.zip`
2. 解压；运行时位于 `cangjie\runtime\`
3. 设置 PATH（任选一种）：
   - **CMD**：`set "PATH=${CANGJIE_HOME}\runtime\lib\windows_x86_64_cjnative;%PATH%;"`
   - **PowerShell**：`$env:PATH = "${CANGJIE_HOME}\runtime\lib\windows_x86_64_cjnative;" + $env:Path`
   - **MSYS/bash**：`export PATH=${CANGJIE_HOME}/runtime/lib/windows_x86_64_cjnative:$PATH`
