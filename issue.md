# issue.md — 已知问题与潜在隐患

## 1. tree-sitter-cangjie 插件需手动安装

**问题**：`check:ast` 指令依赖 `tree-sitter-cangjie` Python 包，该包未发布到 PyPI，需从 GitHub Releases 手动下载安装 `.whl` 文件。

**影响**：在 CI/CD 环境中需额外配置安装步骤。

**缓解**：当 tree-sitter 不可用时，`check:ast` 自动退化为 PASS（不报错），不影响其他测试。可通过 `--skip-ast` 选项显式跳过。

## 2. tree-sitter 末尾换行符敏感

**状态**：已解决。

tree-sitter-cangjie 插件 v1.0.5.3 已修复末尾换行符敏感问题，代码不以换行符结尾也不再产生误报。`check_ast()` 中的换行符补充逻辑已移除。

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

## 6. 示例代码 if-else 表达式语法错误

**状态**：已解决。

`story/begin/03_control_flow.md` 中无大括号的 if-else 表达式（`if (cond) "Win" else "Try Again"`）为语法错误，已修正为 `if (cond) { "Win" } else { "Try Again" }`，标注从 `check:skip` 改回 `check:ast`。
