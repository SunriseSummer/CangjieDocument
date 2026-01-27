# 第二章：HTTP 协议封装 (结构体与枚举)

> HTTP 协议本质上是文本的交互。我们需要定义一套数据结构来描述“请求”和“响应”，这是框架通信的通用语言。

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
