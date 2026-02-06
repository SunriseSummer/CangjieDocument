# 第四章：中间件链 (闭包与函数式编程)

> 现代 Web 框架的灵魂是“洋葱模型”的中间件系统。日志记录、鉴权、耗时统计等功能都可以作为中间件层层包裹业务逻辑，让核心业务保持干净。

## 本章目标

*   理解中间件链的执行顺序与职责边界。
*   学会使用闭包构建“前后包裹”的逻辑。
*   认识中间件在横切关注点中的价值。

## 1. 定义中间件 (Handler Chaining)

中间件本质上是一个“包装函数”，它接收下一个处理函数，返回一个新的处理函数。

```cangjie
// Next 代表后续的处理逻辑
type Next = () -> Unit

// 中间件签名
type Middleware = (Context, Next) -> Unit

class Engine {
    var middlewares = ArrayList<Middleware>()

    public func use(mw: Middleware) {
        middlewares.append(mw)
    }

    // 模拟执行链
    public func run(ctx: Context, finalHandler: Handler) {
        // 构建洋葱模型
        // 这里用简化的递归模拟：index 指向当前中间件
        func dispatch(index: Int64) {
            if (index >= middlewares.size) {
                finalHandler(ctx) // 链条末端，执行业务
                return
            }

            let mw = middlewares[index]
            // next 函数：指向下一个中间件
            let next = { => dispatch(index + 1) }

            // 执行当前中间件
            mw(ctx, next)
        }

        dispatch(0)
    }
}
```

## 2. 实战：日志与鉴权

```cangjie
main() {
    let app = Engine()

    // 1. 日志中间件
    app.use { ctx, next =>
        println("[Log] Start Request: ${ctx.path}")
        next() // 执行后续逻辑
        println("[Log] End Request (Status: ${ctx.statusCode})")
    }

    // 2. 鉴权中间件
    app.use { ctx, next =>
        if (ctx.path == "/admin") {
            println("[Auth] ⚠️ 权限不足！拦截请求。")
            ctx.statusCode = 403
            ctx.string("Forbidden")
            // 不调用 next()，请求到此终止
        } else {
            next()
        }
    }

    // 业务处理
    let handler = { ctx: Context =>
        println("--> 执行业务逻辑...")
        ctx.string("Success")
    }

    // 测试 1: 普通请求
    println("=== 测试 /home ===")
    app.run(Context("/home", HttpMethod.GET), handler)

    // 测试 2: 受限请求
    println("\n=== 测试 /admin ===")
    app.run(Context("/admin", HttpMethod.GET), handler)
}
```

代码要点：

内部函数 `dispatch` 展示了函数嵌套与递归调用的能力，让中间件链构建保持私有封装。
`let next = { => dispatch(index + 1) }` 创建闭包并捕获 `index`，体现洋葱模型的“前后包裹”语义。
函数类型别名 `Middleware` 与 `Next` 让复杂签名变得可读，是构建框架 API 的常见方式。

## 工程化提示

*   中间件顺序要固定并可配置，避免逻辑混乱。
*   鉴权中间件应返回统一错误格式，便于前端处理。
*   洋葱模型执行时注意异常传播，确保日志完整输出。

## 小试身手

1. 添加一个“耗时统计”中间件，输出请求执行耗时。
2. 将 `Engine` 改为支持在运行时插入全局错误处理中间件。
