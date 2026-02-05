# 08. 错误处理与模式匹配：简易计算器

在数学计算中，总有一些“非法操作”，比如除以零。如何优雅地处理这些异常？如何解析用户的指令？

## 本章目标

*   学会使用 `Option` 表达“可能为空”的结果。
*   理解 `match` 模式匹配在分支逻辑中的优势。
*   掌握异常捕获的基本结构与资源清理意识。

## 1. 安全除法 (Option 类型)

与其让程序崩溃，不如返回一个“可能为空”的结果。

```cangjie
func safeDivide(a: Float64, b: Float64): Option<Float64> {
    if (b == 0.0) {
        return None // 就像返回 null，但更安全
    }
    return Some(a / b)
}

main() {
    let result1 = safeDivide(10.0, 2.0)
    let result2 = safeDivide(10.0, 0.0)

    // 处理 result1
    match (result1) {
        case Some(val) => println("结果: ${val}")
        case None => println("错误：不能除以零")
    }

    // 简写：如果只是为了取值
    if (let Some(val) <- result2) {
        println("Result 2: ${val}")
    } else {
        println("计算 2 失败！")
    }
}
```

## 2. 指令解析 (Match 模式匹配)

假设我们要解析用户的文本指令进行计算。

```cangjie
// 定义操作类型
enum Operation {
    | Add(Float64, Float64)
    | Subtract(Float64, Float64)
    | Power(Float64) // 求平方
    | Quit
}

func execute(op: Operation) {
    match (op) {
        case Add(x, y) => println("${x} + ${y} = ${x + y}")
        case Subtract(x, y) => println("${x} - ${y} = ${x - y}")
        case Power(x) => println("${x}² = ${x * x}")
        case Quit => println("程序退出。")
    }
}

main() {
    let commands = [
        Add(5.0, 3.0),
        Power(4.0),
        Quit
    ]

    for (cmd in commands) {
        execute(cmd)
    }
}
```

## 3. 异常拦截 (Try-Catch)

对于不可控的系统错误（如文件不存在），我们使用 `try-catch`。

```cangjie
func readFile(path: String) {
    if (path == "") {
        throw Exception("路径不能为空！")
    }
    println("读取文件: ${path}")
}

main() {
    try {
        readFile("")
    } catch (e: Exception) {
        println("❌ 捕获异常: " + e.message)
    } finally {
        println("清理资源...")
    }
}
```

## 工程化提示

*   能用 `Option`/`Result` 表达的错误尽量不要抛异常，让逻辑更可控。
*   模式匹配时覆盖所有分支，必要时提供兜底分支。
*   `try-catch` 中避免吞掉异常，至少记录上下文与输入。

## 小试身手

1. 为 `Operation` 增加 `Divide` 分支，并在执行时复用 `safeDivide`。
2. 模拟读取不同路径时返回 `Option<String>`，避免直接抛异常。
