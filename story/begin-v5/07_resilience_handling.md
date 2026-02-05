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

## 工程化提示

*   能用返回值表达的错误不要抛异常，提升可控性。
*   异常处理要记录上下文信息，便于排查。
*   关键路径建议加上兜底策略与报警机制。

## 实践挑战

1. 为 `findOrder` 增加“超时重试”的日志提示。
2. 在 `loadRouteFile` 中加入路径合法性校验逻辑。
