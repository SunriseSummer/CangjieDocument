# 第二章：HTTP 协议封装 (结构体与枚举)

> HTTP 协议本质上是文本的交互。我们需要定义一套数据结构来描述“请求”和“响应”，这是框架通信的通用语言，也是中间件链的核心载体。

## 本章目标

*   学会用枚举表达有限集合的协议常量。
*   理解请求/响应模型的数据结构设计。
*   认识上下文对象在框架中的作用。

## 1. 请求方法 (Enum)

HTTP 方法（GET, POST 等）是有限且固定的，非常适合使用枚举 (`enum`)。

```cangjie
enum HttpMethod {
    | GET
    | POST
    | PUT
    | DELETE
}

// 扩展枚举，增加实用方法
extend HttpMethod {
    func toString(): String {
        match (this) {
            case GET => "GET"
            case POST => "POST"
            case PUT => "PUT"
            case DELETE => "DELETE"
        }
    }
}
```

## 2. 请求与响应 (Class)

请求对象需要在中间件链中传递和修改，适合用引用类型 (`class`)。

```cangjie
class Context {
    let path: String
    let method: HttpMethod
    var responseBody: String = ""
    var statusCode: Int64 = 200

    public init(path: String, method: HttpMethod) {
        this.path = path
        this.method = method
    }

    // 辅助方法：发送响应
    public func string(content: String) {
        this.responseBody = content
    }

    public func json(json: String) {
        this.responseBody = json
        // 这里可以设置 Content-Type 头
    }
}

main() {
    // 模拟接收到一个 GET /home 请求
    let ctx = Context("/home", HttpMethod.GET)

    println("收到请求: ${ctx.method.toString()} ${ctx.path}")

    // 业务逻辑处理
    ctx.string("<h1>Hello Cangjie Web</h1>")

    println("响应内容: ${ctx.responseBody}")
}
```

代码要点：

枚举 `HttpMethod` 用 `extend` 增加方法，体现“数据 + 行为”的组合式设计，避免在外部写大量 `match`。
`class Context` 作为引用类型，方便在中间件链中被多次修改；默认字段值让对象创建更轻量。
初始化函数中使用 `this` 绑定成员，体现了仓颉面向对象的清晰语义。

## 工程化提示

*   协议字段的命名要与标准一致，避免歧义。
*   `Context` 应控制可变状态的访问路径，防止被随意修改。
*   序列化与内容类型需在真实项目中严格处理，本例仅示意。

## 小试身手

1. 为 `HttpMethod` 增加 `PATCH` 分支并补充转换逻辑。
2. 在 `Context` 中加入 `headers` 字段，并提供 `setHeader` 方法。
