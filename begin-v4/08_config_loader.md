# 第八章：配置加载器 (IO 与异常)

> 硬编码配置是架构的大忌。我们需要从文件系统读取 `config.json` 或 `.env` 文件，并优雅地处理文件不存在或格式错误的情况。

## 1. 模拟文件读取 (File IO)

假设我们有一个读取文件的底层函数。

```cangjie
// 模拟 std.fs 的读取
func readFileContent(path: String): String {
    if (path == "config.json") {
        return "{\"port\": 8080, \"db\": \"mysql\"}"
    } else {
        // 抛出异常：文件未找到
        throw Exception("FileNotFound: ${path}")
    }
}
```

## 2. 安全配置加载 (Try-Catch)

```cangjie
struct AppConfig {
    var port: Int64 = 80
    var dbType: String = "sqlite"

    public func printInfo() {
        println("配置加载: Port=${port}, DB=${dbType}")
    }
}

func loadConfig(path: String): AppConfig {
    println("正在加载配置: ${path} ...")

    try {
        let content = readFileContent(path)
        println("读取成功: ${content}")
        // 这里应该有 JSON 解析逻辑，简化为模拟赋值
        let config = AppConfig()
        config.port = 8080
        config.dbType = "mysql"
        return config

    } catch (e: Exception) {
        println("⚠️ 配置加载失败: ${e.message}")
        println("🔄 回退到默认配置")
        return AppConfig() // 返回默认值
    }
}

main() {
    // 场景 1: 文件存在
    let conf1 = loadConfig("config.json")
    conf1.printInfo()

    println("\n----------------\n")

    // 场景 2: 文件不存在
    let conf2 = loadConfig("missing.yaml")
    conf2.printInfo()
}
```
