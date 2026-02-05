# 10. 综合实战：迷你搜索引擎

我们将综合运用之前学到的所有知识（结构体、集合、并发、错误处理），构建一个迷你的“倒排索引”搜索引擎。

## 本章目标

*   综合运用结构体、集合与并发编程的能力。
*   理解倒排索引的核心概念与基础流程。
*   建立“拆分模块 + 组合流程”的工程实践思维。

## 1. 场景描述

我们有若干个文本文档（模拟文件）。我们需要：
1.  **索引阶段**：并发扫描所有文档，统计每个单词出现在哪些文档中。
2.  **搜索阶段**：用户输入单词，系统快速返回包含该单词的文档列表。

## 2. 完整实现

```cangjie
import std.collection.*
import std.sync.*
import std.time.*

// === 数据模型 ===

struct Document {
    let id: Int64
    let content: String
}

// 倒排索引：单词 -> 文档ID列表
// 使用 ConcurrentHashMap 或者是加锁的 HashMap。
// 为了简化演示，我们这里使用互斥锁保护普通 HashMap。
class SearchIndex {
    // 存储结构: "apple" -> [1, 3]
    var indexMap: HashMap<String, ArrayList<Int64>>
    let lock: Mutex

    public init() {
        indexMap = HashMap<String, ArrayList<Int64>>()
        lock = Mutex()
    }

    // 添加索引条目 (线程安全)
    public func addEntry(word: String, docId: Int64) {
        // 加锁保护写操作
        synchronized(lock) {
            if (!indexMap.contains(word)) {
                indexMap.put(word, ArrayList<Int64>())
            }
            let list = indexMap[word]
            // 避免重复添加
            var exists = false
            for (id in list) { if (id == docId) { exists = true; break } }

            if (!exists) {
                list.append(docId)
            }
        }
    }

    // 搜索 (线程安全)
    public func search(query: String): ArrayList<Int64> {
        synchronized(lock) {
            if (indexMap.contains(query)) {
                // 返回副本以避免并发修改问题
                let result = ArrayList<Int64>()
                for (id in indexMap[query]) { result.append(id) }
                return result
            } else {
                return ArrayList<Int64>()
            }
        }
    }
}

// === 核心逻辑 ===

// 分词函数 (简单按空格切分)
func tokenize(text: String): Array<String> {
    // 实际项目中会用更复杂的正则或 NLP 库
    // 这里简单模拟：转小写，去标点（略），按空格分
    // 仓颉目前 String split 示例
    // 由于 std 库变动，这里用伪代码逻辑展示：
    // 假设 content 只有空格分隔
    // 真实环境需使用 text.split(" ")
    // 这里为简化演示，我们手动模拟几个关键词
    let words = ArrayList<String>()
    if (text.contains("cangjie")) { words.append("cangjie") }
    if (text.contains("programming")) { words.append("programming") }
    if (text.contains("fast")) { words.append("fast") }
    if (text.contains("safe")) { words.append("safe") }
    return words.toArray()
}

func indexDocument(doc: Document, engine: SearchIndex) {
    let words = tokenize(doc.content)
    for (w in words) {
        engine.addEntry(w, doc.id)
    }
    // 模拟处理耗时
    sleep(Duration.millisecond * 10)
}

// === 主程序 ===

main() {
    println("🚀 搜索引擎启动中...")

    // 1. 准备数据
    let docs = [
        Document(1, "Cangjie is a fast programming language"),
        Document(2, "Safe and efficient programming"),
        Document(3, "Cangjie is safe"),
        Document(4, "I love fast cars")
    ]

    let engine = SearchIndex()
    let futures = ArrayList<Future<Unit>>()

    // 2. 并发构建索引
    let start = DateTime.now()

    for (doc in docs) {
        let f = spawn {
            indexDocument(doc, engine)
        }
        futures.append(f)
    }

    // 等待所有索引任务完成
    for (f in futures) { f.get() }

    let end = DateTime.now()
    println("索引构建完成！耗时: ${(end - start).toMilliseconds()} ms")

    // 3. 执行搜索
    let queries = ["cangjie", "safe", "fast", "java"]

    println("\n=== 搜索结果 ===")
    for (q in queries) {
        let results = engine.search(q)
        if (results.size > 0) {
            print("🔍 搜索 '${q}': Found in docs [")
            for (id in results) { print(" ${id} ") }
            println("]")
        } else {
            println("🔍 搜索 '${q}': 未找到相关文档")
        }
    }
}
```

## 3. 课程结语

恭喜你！通过这 10 个实战案例，你已经从打印 "Hello World" 成长为能够构建并发搜索引擎的仓颉开发者。

**回顾我们的旅程：**
1.  **基础**: 变量、流程控制 (RPG角色, 猜数字)
2.  **核心**: 函数、结构体、接口 (密码机, 订单系统, 支付网关)
3.  **进阶**: 集合、错误处理 (播放器, 计算器)
4.  **高阶**: 并发、综合实战 (股市, 搜索引擎)

未来的编程之路还在脚下，愿仓颉语言成为你手中的利剑，创造出更多精彩的程序！

## 工程化提示

*   真实搜索引擎需要完善的分词、索引持久化与查询优化，本例仅关注核心流程。
*   并发写入共享结构时要格外注意锁粒度与性能瓶颈。
*   建议在索引与查询阶段都记录指标，便于性能定位。

## 小试身手

1. 为索引增加“词频统计”，并在搜索结果中输出出现次数。
2. 将索引构建与搜索过程拆分成两个函数模块，并为其补充日志。
