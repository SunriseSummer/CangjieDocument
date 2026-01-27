# 10. 综合实战：简易日志分析器

本节我们将运用之前学到的知识（结构体、集合、错误处理、并发）来编写一个简单的日志分析工具。

## 1. 需求分析

我们需要处理一批日志数据（字符串），每条日志包含 "INFO", "WARN", "ERROR" 等级别。
目标：
1. 解析日志字符串为结构化对象。
2. 模拟耗时操作，并发处理以提高效率。
3. 统计各级别日志的数量。

## 2. 代码实现

```cangjie
import std.collection.*
import std.time.*
import std.sync.*

// 1. 定义日志结构体
struct LogEntry {
    let level: String
    let message: String

    init(level: String, message: String) {
        this.level = level
        this.message = message
    }
}

// 2. 解析函数 (模拟日志解析)
func parseLog(line: String): LogEntry {
    // 简单的字符串包含判断
    // 注意：实际开发中可能使用更复杂的字符串分割或正则
    if (line.contains("ERROR")) {
        return LogEntry("ERROR", line)
    } else if (line.contains("WARN")) {
        return LogEntry("WARN", line)
    } else {
        return LogEntry("INFO", line)
    }
}

main() {
    // 模拟日志数据
    let logs = [
        "2023-10-01 INFO: System started",
        "2023-10-01 ERROR: Database connection failed",
        "2023-10-01 WARN: Memory usage high",
        "2023-10-01 INFO: User login success",
        "2023-10-01 ERROR: Timeout waiting for response",
        "2023-10-01 INFO: Health check passed"
    ]

    println("Starting analysis of ${logs.size} logs...")

    // 用于存储并发任务的 Future 列表
    // 每个任务返回一个 LogEntry
    let futures = ArrayList<Future<LogEntry>>()

    // 3. 并发分发任务
    for (line in logs) {
        // spawn 开启轻量级线程
        let f = spawn { =>
            // 模拟解析耗时 (500ms)
            sleep(Duration.millisecond * 500)
            return parseLog(line)
        }
        futures.append(f)
    }

    // 4. 收集结果与统计
    var errorCount = 0
    var warnCount = 0
    var infoCount = 0

    for (f in futures) {
        // 等待结果
        let entry = f.get()

        // 模式匹配统计
        match (entry.level) {
            case "ERROR" => errorCount = errorCount + 1
            case "WARN" => warnCount = warnCount + 1
            case _ => infoCount = infoCount + 1
        }

        // 打印进度
        print(".")
    }

    println("\n\nAnalysis Complete!")
    println("==================")
    println("Errors : ${errorCount}")
    println("Warnings: ${warnCount}")
    println("Infos  : ${infoCount}")
}
```

## 3. 总结

在这个项目中，我们结合了：
*   **Struct**: 定义数据模型。
*   **Collection**: 存储源数据和 Future 列表。
*   **Concurrency**: 使用 `spawn` 并发处理任务。
*   **Control Flow**: 使用 `match` 进行分类统计。

通过本系列教程的学习，你已经掌握了仓颉编程语言的核心特性。继续探索吧，仓颉还有更多高级特性（如宏、FFI等）等待你去发现！
