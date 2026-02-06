# begin-v4 文档复查记录

以下建议以“吸引力、启发性、示范性、深度”为目标，聚焦于示例代码的正确性、可运行性与教学价值。

## 01_server_core.md

- **潜在问题**：示例主循环是无限 `while (true)`，没有退出或信号处理说明，读者可能误以为没有优雅关闭机制。
- **改进建议**：补充“如何优雅退出/健康检查”的说明，示例可增加一个简易的退出条件（如监听 `running` 标志），并提示真实场景应处理 `SIGINT/SIGTERM`。
- **启发性增强**：可以在示例结尾加一句“下一章将引入 socket accept”，形成故事连续性。

## 02_http_protocol.md

- **潜在问题**：`Context.json` 仅设置 `responseBody`，未体现状态码/响应头，容易让读者忽略内容类型的重要性。
- **改进建议**：增加 `headers` 字段及 `setHeader` 示例，并在 `json()` 中设置 `Content-Type`；补充 `HEAD/OPTIONS/PATCH` 等方法的补齐说明（或提供扩展清单）。
- **示范性增强**：在 `main()` 中加一段“模拟 404 响应”的设置，让响应模型更完整。

## 03_router_logic.md

- **潜在问题**：示例依赖 `Context/HttpMethod` 但文内未说明来源，单章阅读时缺少上下文。
- **潜在问题**：`routes.contains(ctx.path)` 与 `routes[ctx.path]` 双重访问可能与实际 API 不一致（建议使用 `get`/`containsKey` 或一次性取出 `Option`）。
- **改进建议**：在章节开头加一行“沿用第二章的 `Context`/`HttpMethod`”，并提示真实路由需支持“方法匹配 + 动态参数”。

## 04_middleware_chain.md

- **潜在问题**：示例中未显示 `Handler` 定义，也未导入 `ArrayList` 需要的集合包，读者容易复制后报错。
- **潜在问题**：`next()` 可被重复调用，容易导致业务逻辑执行多次。
- **改进建议**：补充 `Handler` 定义与 `import std.collection.*`，并在 `dispatch` 中加入“防止 next 多次调用”的简单保护逻辑提示。
- **启发性增强**：补一段“异常中间件”示例（如 `try { next() } catch { ... }`），体现真实生产链路。

## 05_ioc_container.md

- **潜在问题**：`Container.resolve` 通过字符串 key + 强制转换获取服务，易产生运行期错误。
- **改进建议**：说明这是“简化版容器”，并补充“类型安全注册”的方向（如 `register<T>` + `resolve<T>`，或基于 `TypeId` 的实现思路）。
- **示范性增强**：增加“单例/每次创建”生命周期的对比说明，让工程化落地更明确。

## 06_state_management.md

- **潜在问题**：`next` 使用字符串 `action`，容易拼写错误；同时 `case (_, "cancel")` 允许任何状态取消，业务规则过松。
- **改进建议**：把 `action` 改成枚举，并在“取消”分支中增加状态校验；对非法流转建议给出显式错误类型或 Result。
- **启发性增强**：补充“状态日志记录”的简单示例，突出可追踪性。

## 07_async_worker.md

- **潜在问题**：第二段示例仅 `sleep` 等待，可能未等所有 `spawn` 完成，示例结果不稳定。
- **改进建议**：使用 `Future` 收集并 `get()` 或引入 `Barrier/WaitGroup`（若有），保证统计准确。
- **深度增强**：补充“限流/线程池”示例，提示真实服务不会无限 spawn。

## 08_config_loader.md

- **潜在问题**：`let config = AppConfig()` 后又修改字段，可能违反不可变语义；应使用 `var`。
- **改进建议**：区分“文件缺失”与“解析失败”，并给出不同的回退策略；示例中可加入 `logLevel` 字段以体现可扩展性。
- **示范性增强**：增加“环境变量覆盖”的简短说明，体现配置优先级。

## 09_routing_dsl.md

- **潜在问题**：`Router.add` 的 handler 类型写成 `(String) -> Unit`，但实际传入的是 `ctx`，类型不匹配。
- **改进建议**：将 handler 改为 `(Context) -> Unit`（或与第三章一致的 `Handler`），并说明宏如何把方法与路径转成内部注册调用。
- **启发性增强**：给出一个“宏展开前后对照”更完整的对比，帮助读者理解编译期生成代码。

## 10_full_stack_demo.md

- **潜在问题**：`getAllPosts` 手写 JSON 结尾带多余逗号，输出不是合法 JSON。
- **潜在问题**：`createPost` 使用固定标题，缺乏“请求体解析”的示范。
- **改进建议**：
  - 用列表拼接或 `join` 的方式生成 JSON，避免尾逗号问题。
  - 在 `Context` 中加入 `body` 字段，并示例如何从请求体读取标题。
- **深度增强**：补充一个简单的错误处理/返回结构（如 `Result` 或 `statusCode`），让“全栈”示例更贴近真实服务。
