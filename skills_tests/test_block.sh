#!/bin/bash
#
# 仓颉代码块快速测试脚本
#
# 用法：
#   ./test_block.sh <cangjie_file> [--stdx] [--run]
#
# 参数：
#   <cangjie_file>  仓颉源代码文件路径
#   --stdx          使用 stdx 扩展标准库
#   --run           编译后运行（默认仅编译）
#
# 环境变量：
#   CANGJIE_STDX_PATH  stdx 静态库路径
#
# 示例：
#   ./test_block.sh /tmp/test.cj --run
#   ./test_block.sh /tmp/test.cj --stdx --run
#

set -e

# 参数解析
CJ_FILE=""
USE_STDX=false
DO_RUN=false

for arg in "$@"; do
    case "$arg" in
        --stdx) USE_STDX=true ;;
        --run)  DO_RUN=true ;;
        *)      CJ_FILE="$arg" ;;
    esac
done

if [ -z "$CJ_FILE" ]; then
    echo "用法: $0 <cangjie_file> [--stdx] [--run]"
    exit 1
fi

if [ ! -f "$CJ_FILE" ]; then
    echo "错误: 文件不存在: $CJ_FILE"
    exit 1
fi

# 检查 cjpm
if ! command -v cjpm &> /dev/null; then
    echo "错误: 找不到 cjpm，请先执行 source envsetup.sh"
    exit 1
fi

# 自动检测是否需要 stdx
if grep -q "import stdx\." "$CJ_FILE"; then
    USE_STDX=true
fi

# stdx 路径
STDX_PATH="${CANGJIE_STDX_PATH:-/tmp/cangjie-stdx/linux_x86_64_cjnative/static/stdx}"

# 创建临时项目
PROJECT_DIR=$(mktemp -d /tmp/cjpm_test_block_XXXXXX)
trap "rm -rf $PROJECT_DIR" EXIT

mkdir -p "$PROJECT_DIR/src"

# 生成 cjpm.toml
if [ "$USE_STDX" = true ]; then
    cat > "$PROJECT_DIR/cjpm.toml" << TOML
[package]
  cjc-version = "1.0.5"
  name = "testproject"
  version = "1.0.0"
  output-type = "executable"
  compile-option = "-ldl"
[dependencies]
[target.x86_64-unknown-linux-gnu]
  [target.x86_64-unknown-linux-gnu.bin-dependencies]
    path-option = ["${STDX_PATH}"]
TOML
else
    cat > "$PROJECT_DIR/cjpm.toml" << TOML
[package]
  cjc-version = "1.0.5"
  name = "testproject"
  version = "1.0.0"
  output-type = "executable"
[dependencies]
TOML
fi

# 生成 main.cj
CODE=$(cat "$CJ_FILE")

# 检查是否已有 package 声明
if echo "$CODE" | grep -q "^package "; then
    # 替换 package 名为 testproject
    echo "$CODE" | sed 's/^package .*/package testproject/' > "$PROJECT_DIR/src/main.cj"
else
    echo "package testproject" > "$PROJECT_DIR/src/main.cj"
    echo "" >> "$PROJECT_DIR/src/main.cj"
    cat "$CJ_FILE" >> "$PROJECT_DIR/src/main.cj"
fi

# 编译
echo "📦 编译中..."
cd "$PROJECT_DIR"
if cjpm build 2>&1; then
    echo "✅ 编译成功"
else
    echo "❌ 编译失败"
    exit 1
fi

# 运行
if [ "$DO_RUN" = true ]; then
    echo ""
    echo "🚀 运行中..."
    echo "---"
    timeout 10 cjpm run 2>&1 | grep -v "cjpm run finished" || true
    echo "---"
fi
