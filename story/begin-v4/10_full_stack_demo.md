# 第十章：全栈博客实战 (CangjieWeb 综合演示)

> 终于，我们的 `CangjieWeb` 框架初具雏形。现在，让我们用它来构建一个真实的博客后端 API。我们将串联起所有知识点，并演示“分层 + 依赖注入”的开发方式。

## 本章目标

*   综合运用模型、服务与控制器的分层思路。
*   理解 IoC 注入与路由分发的完整流程。
*   建立“全链路设计”的系统观念。

## 1. 架构设计

*   **Models**: 定义 `Post` (文章)。
*   **Service**: 处理业务逻辑（IoC 注入）。
*   **Controller**: 处理路由与请求。
*   **Main**: 启动服务。

## 2. 完整代码实现

```cangjie
import std.collection.*
import std.time.*

// === 1. Core Framework (迷你版) ===
class Context {
    let path: String
    public init(path: String) { this.path = path }
    public func json(data: String) { println("HTTP 200 OK\nContent-Type: application/json\n\n${data}") }
}

// === 2. Models ===
struct Post {
    let id: Int64
    let title: String
    let content: String
}

// === 3. Services (Interface & Impl) ===
interface BlogService {
    func getAllPosts(): String
    func createPost(title: String): Unit
}

class BlogServiceImpl <: BlogService {
    var posts = ArrayList<Post>()

    public init() {
        posts.append(Post(1, "Hello Cangjie", "First Post"))
        posts.append(Post(2, "Web Dev", "Framework Design"))
    }

    public func getAllPosts(): String {
        // 模拟 JSON 序列化
        var json = "["
        for (p in posts) {
            json = json + "{\"id\": ${p.id}, \"title\": \"${p.title}\"},"
        }
        json = json + "]"
        return json
    }

    public func createPost(title: String) {
        let newId = posts.size + 1
        posts.append(Post(newId, title, "Content..."))
        println("Service: 文章 '${title}' 已创建")
    }
}

// === 4. Controller ===
class BlogController {
    let service: BlogService

    // 依赖注入
    public init(svc: BlogService) {
        this.service = svc
    }

    // GET /posts
    public func list(ctx: Context) {
        println("Processing GET /posts ...")
        let data = service.getAllPosts()
        ctx.json(data)
    }

    // POST /posts/new
    public func create(ctx: Context) {
        println("Processing POST /posts/new ...")
        service.createPost("New Article")
        ctx.json("{\"status\": \"created\"}")
    }
}

// === 5. App Entry ===
main() {
    println(">>> 启动博客后端 API...")

    // 1. IoC 组装
    let service = BlogServiceImpl()
    let controller = BlogController(service)

    // 2. 模拟路由分发 (Router Loop)
    let requests = [
        Context("/posts"),
        Context("/posts/new"),
        Context("/posts") // 再次查询验证数据更新
    ]

    for (req in requests) {
        println("\n>>> Incoming Request: ${req.path}")

        if (req.path == "/posts") {
            controller.list(req)
        } else if (req.path == "/posts/new") {
            controller.create(req)
        } else {
            println("404 Not Found")
        }

        sleep(Duration.millisecond * 200)
    }
}
```

## 终章：架构师之路

恭喜！你不仅学会了仓颉语言的语法，更重要的是，你通过构建 `CangjieWeb` 框架，深入理解了：
*   **IoC 与解耦**
*   **中间件洋葱模型**
*   **并发处理模型**
*   **领域建模**

这正是从“码农”进阶为“架构师”的必经之路。继续探索吧，用仓颉构建更宏大的数字大厦！

## 语言特性与应用解读

`struct Post` 用值类型承载只读数据，而 `class BlogController` 管理依赖与行为，体现“数据/行为分离”的建模习惯。
接口 `BlogService` 让控制器只依赖抽象能力，便于替换实现并进行测试。
列表字面量 `[]` 与 `for (req in requests)` 展示了集合初始化与迭代语法，适合模拟请求流转。

## 工程化提示

*   JSON 序列化应使用可靠库，避免手工拼接引入格式问题。
*   路由分发应统一处理 404 与异常响应，保持接口一致。
*   业务服务层应与控制器解耦，便于测试与扩展。

## 小试身手

1. 为 `Post` 增加 `author` 字段，并在输出中体现。
2. 添加 `delete` 接口示例，并模拟删除文章流程。
