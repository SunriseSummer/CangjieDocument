# 第五章：IoC 容器 (泛型与接口)

> 为了解耦业务代码，现代框架通常提供依赖注入（Dependency Injection）功能。我们需要构建一个简单的 IoC (Inversion of Control) 容器，让服务注册与使用分离。

## 本章目标

*   理解依赖注入与控制反转的核心概念。
*   学会用接口与泛型容器管理服务实例。
*   认识构造注入在模块解耦中的作用。

## 1. 容器定义 (Generics)

我们需要一个万能的字典，可以存储任意类型的服务实例。

```cangjie
import std.collection.*

// 抽象服务接口
interface Service {
    func getName(): String
}

class Container {
    // 简化版：Key 是服务名，Value 是服务实例
    // 真实框架会使用反射或 TypeId
    var services = HashMap<String, Service>()

    public func register(name: String, svc: Service) {
        services[name] = svc
        println("IoC: 注册服务 [${name}]")
    }

    // 泛型获取方法 (模拟)
    // 仓颉中通常需要转换类型，这里简化演示
    public func resolve(name: String): Option<Service> {
        if (services.contains(name)) {
            return Some(services[name])
        }
        return None
    }
}
```

## 2. 服务注册与获取

```cangjie
class DatabaseService <: Service {
    public func getName() = "Database"
    public func query() = "SELECT * FROM users"
}

class CacheService <: Service {
    public func getName() = "Redis"
    public func get(key: String) = "Value for ${key}"
}

class UserController {
    let db: DatabaseService

    // 构造注入
    public init(db: DatabaseService) {
        this.db = db
    }

    public func getUser() {
        println("Controller 调用 DB: " + db.query())
    }
}

main() {
    let container = Container()

    // 1. 注册依赖
    container.register("db", DatabaseService())
    container.register("cache", CacheService())

    // 2. 解析依赖
    if (let Some(svc) <- container.resolve("db")) {
        // 假设我们知道它是 DatabaseService 并进行了转换
        // 在强类型语言中，这里通常涉及 cast
        if (svc is DatabaseService) {
             let db = svc as DatabaseService

             // 3. 注入 Controller
             let ctrl = UserController(db)
             ctrl.getUser()
         }
     }
}
```

## 语言特性与应用解读

接口 `Service` 提供统一能力约束，容器可以只暴露接口类型，降低模块之间的耦合。
`Option` 配合 `if (let Some(svc) <- ...)` 展示了模式匹配式的解包语法，避免空指针风险。
`is`/`as` 体现了类型检查与显式转换，提示我们在强类型体系下要谨慎对待类型边界。

## 工程化提示

*   真实 IoC 容器需要生命周期管理与依赖图校验，本例仅演示核心流程。
*   强类型语言中应避免随意类型转换，建议引入明确的注册与解析接口。
*   服务命名建议统一规范，避免重复注册或歧义。

## 小试身手

1. 为 `Container` 增加 `unregister` 方法，并验证服务移除。
2. 给 `UserController` 增加 `CacheService` 依赖并完成注入。
