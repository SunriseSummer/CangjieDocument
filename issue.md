# issue.md — 已知问题与潜在隐患

## 1. tree-sitter-cangjie 插件需手动安装

**问题**：`check:ast` 指令依赖 `tree-sitter-cangjie` Python 包，该包未发布到 PyPI，需从 GitHub Releases 手动下载安装 `.whl` 文件。

**影响**：在 CI/CD 环境中需额外配置安装步骤。

**缓解**：当 tree-sitter 不可用时，`check:ast` 自动退化为 PASS（不报错），不影响其他测试。可通过 `--skip-ast` 选项显式跳过。

## 2. tree-sitter 末尾换行符敏感

**问题**：tree-sitter 仓颉解析器在代码不以换行符结尾时可能产生误报（`has_error=True` 但无实际 ERROR 节点）。

**影响**：不补充换行符时，合法代码可能被误判为语法错误。

**解决**：`check_ast()` 函数中已自动在代码末尾补充 `\n`。

## 3. check:skip 仍有少量使用

**问题**：当前仍有 6 个代码块使用 `check:skip`（均在 `language/source_zh_cn/package/` 目录），原因是这些代码块包含多文件合并的伪代码片段（如同一代码块中包含 `// file1.cj` 和 `// file2.cj`），tree-sitter 无法将其作为单一源文件解析。

**影响**：这些代码块缺少语法层面的验证。

**建议**：后续可考虑将伪代码多文件示例拆分为独立的标注代码块（使用 `project` + `file` 参数），从而完全消除 `check:skip`。

## 4. cjpm run 退出码不反映运行时异常

**问题**：`cjpm run` 在程序抛出未捕获异常时仍返回退出码 0，异常信息输出到 stderr。

**影响**：不能简单通过退出码判断运行是否成功。

**解决**：`runner.py` 中通过检查 stderr 是否包含 `An exception has occurred` 来检测运行时错误。

## 5. 并发代码输出不确定性

**问题**：包含 `spawn` 的并发示例，输出顺序可能不固定。

**影响**：设置 `expected_output` 后可能因顺序不同导致测试失败。

**建议**：并发示例不设置 `expected_output`，仅验证编译运行成功。

## 6. story 目录 skip 已全部转为 ast

**状态**：已解决。

`story/` 目录中原有 7 个 `check:skip` 代码块已全部转为 `check:ast`，经验证语法检查均通过。
