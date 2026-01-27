# 第三章：路由分发 (流程控制)

> 服务器需要根据 URL 的不同，执行不同的业务逻辑。这就是“路由”。我们将实现一个简单的路由匹配器。

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
