# 第九章：路由 DSL (宏与元编程)

> 现代框架（如 Flask, Spring）都喜欢用注解或简洁的语法来定义路由。在仓颉中，我们可以利用宏（Macro）来实现类似的 DSL（领域特定语言），让代码更具表达力，降低样板代码负担。

> *注：由于宏的实现较为复杂且涉及编译器扩展，本节主要展示宏的使用场景和概念模型。*

## 本章目标

*   理解 DSL 在提升路由声明可读性上的价值。
*   认识宏与元编程的核心概念与边界。
*   学会区分“编译期生成”与“运行期执行”的差异。

## 1. 宏的概念

宏是在编译期间运行的代码。它可以读取你的代码结构，并生成新的代码。

假设我们定义了一个 `@Route` 宏。

```cangjie
// 概念代码：宏定义 (伪代码)
// macro Route(path: String, method: String) {
//     return quote {
//         Router.register(path, method, func)
//     }
// }
```

## 2. 使用 DSL 定义 API

如果不使用宏，我们需要手动注册：

```cangjie
// 手动方式
// router.add("/user", GET, handleUser)
```

如果有了宏，我们可以这样写（更加声明式）：

```cangjie
/*
@Controller("/api")
class UserApi {

    @Get("/info")
    func userInfo() {
        return "User Info"
    }

    @Post("/login")
    func login() {
        return "Login Success"
    }
}
*/
```

## 3. 模拟宏生成的代码

既然宏在编译期生成代码，我们可以模拟一下宏“展开”后的样子。这就是元编程的本质：**写代码的代码**。

```cangjie
// 模拟宏展开后的结果
class GeneratedUserApiRoutes {
    public static func registerRoutes(router: Router) {
        println("Macro: 正在扫描注解并生成路由表...")

        router.add("/api/info", { ctx =>
            println("调用 UserApi.userInfo()")
        })

        router.add("/api/login", { ctx =>
            println("调用 UserApi.login()")
        })
    }
}

// 复用之前的 Router 类定义 (简化版)
class Router {
    public func add(path: String, handler: (String)->Unit) {
        println("Registered: ${path}")
    }
}

main() {
    let r = Router()
    // 宏在幕后自动完成了这一步
    GeneratedUserApiRoutes.registerRoutes(r)
}
```

## 工程化提示

*   DSL 设计要保持一致性，避免引入歧义。
*   宏生成代码要可追踪，便于调试与错误定位。
*   真实框架需结合编译器能力实现宏，本例仅用于概念说明。

## 小试身手

1. 设计一个 `@Put` 路由宏的使用示例，并描述生成代码。
2. 在宏展开示例中添加“路由分组”逻辑。
