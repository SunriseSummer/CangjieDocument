# 第八章：系统容错 (错误处理)

> 物理世界是不稳定的：网络会断，传感器会坏。一个健壮的系统必须能处理这些“意外”，并提供可观测的降级路径，而不是直接崩溃。

## 本章目标

*   学会用 `Option` 处理可预期的空结果。
*   掌握异常捕获在关键路径中的作用。
*   理解模式匹配在指令解析中的优势。

## 1. 设备状态检查 (Option)

获取一个设备的状态时，设备可能已经离线（不存在状态）。

```cangjie
func getDeviceStatus(id: String): Option<String> {
    if (id == "OFFLINE_DEV") {
        return None // 获取失败，但这是一种预期内的“空”状态
    }
    return Some("Active")
}

main() {
    let status = getDeviceStatus("OFFLINE_DEV")

    // 优雅处理离线
    match (status) {
        case Some(s) => println("设备状态: ${s}")
        case None => println("⚠️ 警告: 设备无响应")
    }
}
```

## 2. 关键操作异常 (Try-Catch)

对于不可恢复的错误（如配置文件损坏、I/O 错误），我们抛出异常并在上层捕获。

```cangjie
func connectToCloud() {
    let networkAvailable = false
    if (!networkAvailable) {
        throw Exception("云端连接超时")
    }
    println("云端同步成功")
}

main() {
    println("正在初始化云服务...")

    try {
        connectToCloud()
    } catch (e: Exception) {
        println("❌ 严重错误: " + e.message)
        println("🔄 正在切换至离线本地模式...")
    } finally {
        println("初始化流程结束")
    }
}
```

## 3. 指令解析 (Pattern Matching)

用户通过语音控制发送指令，系统需要解析意图。

```cangjie
enum VoiceCommand {
    | TurnOn(String)       // "打开 X"
    | SetTemp(Int64)       // "设置温度为 X"
    | QueryStatus          // "查询状态"
}

func execute(cmd: VoiceCommand) {
    match (cmd) {
        case TurnOn(dev) => println("执行: 开启设备 -> ${dev}")
        case SetTemp(t) => println("执行: 设定温控 -> ${t}°C")
        case QueryStatus => println("执行: 播报全屋状态")
    }
}

main() {
    let cmd = SetTemp(26)
    execute(cmd)
}
```

代码要点：

`Option` 的 `Some/None` 明确区分“可预期为空”的场景，配合 `match` 实现穷尽式处理，减少遗漏分支。
`try-catch-finally` 让不可恢复的错误在关键路径被捕获并记录，同时通过 `finally` 保证收尾逻辑必然执行。
带参数的枚举分支让指令携带上下文数据，比起多字段结构体更贴近业务语义。

## 工程化提示

*   设备离线属于可预期错误，优先使用返回值而非抛异常。
*   `try-catch` 中至少记录关键上下文，避免问题难以排查。
*   语音指令要设置兜底分支，处理无法识别的输入。

## 小试身手

1. 为 `VoiceCommand` 增加 `TurnOff` 分支，并在 `execute` 中处理。
2. 当设备离线时返回默认状态信息，避免上层崩溃。
