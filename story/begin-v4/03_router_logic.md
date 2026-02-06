# 第三章：路由分发 (流程控制)

> 服务器需要根据 URL 的不同，执行不同的业务逻辑。这就是“路由”。我们将实现一个简单的路由匹配器，理解“路径到处理函数”的映射关系。

## 本章目标

*   理解路由分发在 Web 框架中的职责。
*   学会使用映射结构组织路径与处理函数。
*   认识默认路由与错误响应的处理方式。

## 1. 基础路由逻辑

在很多微框架中，路由本质上就是一个巨大的 `match` 或 `if-else` 结构。

```cangjie
import std.collection.*

// 定义一个处理函数类型
type Handler = (Context) -> Unit

class Router {
    // 简单路由表：路径 -> 处理函数
    var routes = HashMap<String, Handler>()

    public func add(path: String, handler: Handler) {
        routes[path] = handler
    }

    public func handle(ctx: Context) {
        // 查找路由
        if (routes.contains(ctx.path)) {
            let handler = routes[ctx.path]
            handler(ctx) // 执行业务逻辑
        } else {
            // 404 处理
            ctx.statusCode = 404
            ctx.string("404 Not Found")
        }
    }
}

main() {
    let router = Router()

    // 注册路由
    router.add("/index") { ctx =>
        ctx.string("Welcome to Index Page")
    }

    router.add("/user") { ctx =>
        ctx.json("{\"name\": \"User1\"}")
    }

    // 模拟请求
    let req1 = Context("/index", HttpMethod.GET)
    router.handle(req1)
    println("[${req1.statusCode}] ${req1.responseBody}")

    let req2 = Context("/unknown", HttpMethod.GET)
    router.handle(req2)
    println("[${req2.statusCode}] ${req2.responseBody}")
}
```

代码要点：

`type Handler = (Context) -> Unit` 是函数类型别名，简化了路由表的类型声明。
`HashMap<String, Handler>` 让处理函数像数据一样存储与检索，符合“路径 -> 行为”的模型。
`router.add("/index") { ctx => ... }` 体现了 lambda 的简洁写法，使路由声明更接近 DSL 风格。

## 工程化提示

*   路由匹配建议支持动态参数与方法过滤，本例只演示核心思路。
*   404 等错误响应应统一处理，避免分散在业务逻辑中。
*   处理函数最好保持幂等，避免重复调用造成副作用。

## 小试身手

1. 为 `Router` 增加 `remove` 方法，支持删除路由。
2. 让路由表支持按 `HttpMethod` 匹配（例如 GET/POST 不同处理器）。
