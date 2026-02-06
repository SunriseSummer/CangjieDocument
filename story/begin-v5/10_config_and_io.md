# 10. 配置与序列化：服务启动

> 星港调度需要加载区域配置、线路规则、限速策略。配置加载必须可靠，序列化必须可追踪。

## 本章目标

*   了解配置加载与异常兜底流程。
*   使用结构体表达配置数据。
*   认识序列化在接口输出中的意义。

## 1. 配置加载

```cangjie
struct AppConfig {
    var region: String = "star-port"
    var maxVehicles: Int64 = 200

    public func summary() {
        println("Region=${region}, MaxVehicles=${maxVehicles}")
    }
}

func readConfigFile(path: String): String {
    if (path == "config.json") {
        return "{\"region\":\"star-port\",\"maxVehicles\":200}"
    }
    throw Exception("ConfigNotFound")
}

func loadConfig(path: String): AppConfig {
    try {
        let content = readConfigFile(path)
        println("读取配置: ${content}")
        let cfg = AppConfig()
        cfg.region = "star-port"
        cfg.maxVehicles = 200
        return cfg
    } catch (e: Exception) {
        println("配置读取失败: ${e.message}")
        return AppConfig()
    }
}
```

## 2. 序列化输出

```cangjie
struct Order {
    let id: String
    let weight: Float64
    let priority: Int64
}

func orderToJson(order: Order): String {
    return "{\"id\":\"${order.id}\",\"weight\":${order.weight},\"priority\":${order.priority}}"
}

main() {
    let cfg = loadConfig("config.json")
    cfg.summary()

    let order = Order("O-190", 12.5, 4)
    println(orderToJson(order))
}
```

## 语言特性与应用解读

结构体默认值让配置具备“合理兜底”，即便读取失败也能维持基础运行。
`throw` 与 `try/catch` 将异常路径显式化，避免隐藏的失败导致启动流程不透明。
`orderToJson` 利用字符串模板输出序列化结果，便于快速验证字段是否齐全。

## 工程化提示

*   配置分层加载（默认/文件/环境变量）更稳健。
*   序列化建议使用标准库或成熟库，避免手写 JSON 出错。
*   配置错误要输出明确原因，便于排查。

## 实践挑战

1. 为 `AppConfig` 增加 `logLevel` 字段并在输出中显示。
2. 为 `orderToJson` 增加 `region` 字段（来源于配置）。
