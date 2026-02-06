# 11. 可观测性与指标

> 当系统进入夜间高峰，性能问题必须被快速定位。日志、指标、耗时统计是调度系统的“眼睛”。

## 本章目标

*   使用枚举与模式匹配组织日志等级。
*   统计关键流程耗时并输出。
*   为后续监控平台打好基础。

## 1. 日志等级

```cangjie
enum LogLevel {
    | Info
    | Warn
    | Error
}

func log(level: LogLevel, message: String) {
    let prefix = match (level) {
        case Info => "INFO"
        case Warn => "WARN"
        case Error => "ERROR"
    }
    println("[${prefix}] ${message}")
}
```

## 2. 耗时统计

```cangjie
import std.time.*

func timeBlock(name: String, action: () -> Unit) {
    let start = DateTime.now()
    action()
    let end = DateTime.now()
    let duration = end - start
    let durationMs = duration.toMilliseconds()
    println("${name} 耗时: ${durationMs} ms")
}

main() {
    timeBlock("路线计算") {
        log(Info, "计算路线中...")
        sleep(Duration.millisecond * 120)
    }
}
```

> 说明：`duration` 为时间差对象，转换方法以标准库为准，示例使用毫秒输出以便指标统计。

## 语言特性与应用解读

`match` 表达式直接返回日志前缀，使日志等级与输出格式保持统一。
`timeBlock` 接收 `() -> Unit` 的回调函数，体现了高阶函数在指标采集中的实用性。
`DateTime.now()` 与时间差计算组成可复用的耗时统计模板，适合包装关键路径。

## 工程化提示

*   日志字段建议结构化输出，便于接入分析平台。
*   耗时统计应覆盖关键路径与外部依赖调用。
*   指标输出建议使用结构化格式（如 key=value 或 JSON），方便采集系统解析。
*   高峰期日志量大时需考虑采样与限流。

## 实践挑战

1. 为 `log` 增加 `traceId` 参数，模拟链路追踪。
2. 为 `timeBlock` 增加失败计数统计。
