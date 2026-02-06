# 07. 容错与模式匹配：异常处理

> 夜间网络抖动频繁，设备可能离线。系统不能因为单个设备异常而崩溃，你需要区分“可预期错误”与“异常故障”。

## 本章目标

*   使用 `Option` 表达可能为空的结果。
*   用 `try-catch` 捕获不可恢复的异常。
*   通过模式匹配实现清晰的错误处理流程。

## 1. 可预期错误：Option

```cangjie
func findOrder(id: String): Option<Order> {
    if (id == "O-404") {
        return None
    }
    return Some(Order(id, 20.0, 5))
}

main() {
    let order = findOrder("O-404")

    match (order) {
        case Some(o) => println("找到订单: ${o.id}")
        case None => println("订单不存在，进入人工复核")
    }
}
```

## 2. 不可预期错误：Try-Catch

```cangjie
func loadRouteFile(path: String) {
    if (path == "") {
        throw Exception("路径为空")
    }
    println("读取路线文件: ${path}")
}

main() {
    try {
        loadRouteFile("")
    } catch (e: Exception) {
        println("❌ 路线文件加载失败: ${e.message}")
        println("切换至默认路线配置")
    }
}
```

## 语言特性与应用解读

`Option` 的 `Some/None` 明确区分“数据不存在”与“系统失败”，让可预期错误走轻量路径。
`match` 结构保证每个分支都被处理，逻辑更适合做审计与可追踪输出。
`try-catch` 处理不可恢复异常时应尽量把错误上下文写入日志，便于后续问题复盘。

## 工程化提示

*   能用返回值表达的错误不要抛异常，提升可控性。
*   异常处理要记录上下文信息，便于排查。
*   关键路径建议加上兜底策略与报警机制。

## 实践挑战

1. 为 `findOrder` 增加“超时重试”的日志提示。
2. 在 `loadRouteFile` 中加入路径合法性校验逻辑。
