# 09. 并发编程基础

仓颉原生支持轻量级线程（User-level Threads），使用 `spawn` 关键字即可轻松创建。这使得在仓颉中进行并发编程变得非常简单高效。

## 1. 创建线程 (spawn)

使用 `spawn` 关键字启动一个新的并发任务。`spawn` 表达式接受一个 Lambda 表达式，并返回一个 `Future<T>` 对象，其中 `T` 是 Lambda 表达式的返回值类型。

```cangjie
import std.time.* // 导入时间包用于 Duration 和 sleep
import std.sync.* // 导入同步包

main() {
    println("Main thread started")

    // 启动新线程
    // 这里的 lambda 返回 Int64，所以 future 类型是 Future<Int64>
    let future = spawn { =>
        println("  -> New thread is running...")
        sleep(Duration.second) // 休眠 1 秒
        println("  -> New thread finished.")
        return 100
    }

    println("Main thread doing other work...")

    // get() 会阻塞当前线程，直到新线程执行完毕并返回结果
    let result = future.get()
    println("Task result: " + result.toString())
}
```

## 2. 线程同步

当多个线程需要修改同一个变量时，如果不加控制，会导致数据竞争。仓颉提供了 `Atomic` 类型和锁机制。

### 原子操作 (Atomic)

对于简单的计数器，可以使用原子类型，如 `AtomicInt64`。

```cangjie
import std.sync.*
import std.time.*

main() {
    let count = AtomicInt64(0)

    // 启动 10 个线程，每个增加 1
    let futures = ArrayList<Future<Unit>>()

    for (i in 0..10) {
        let f = spawn {
            // 原子加 1
            count.fetchAdd(1)
        }
        futures.append(f)
    }

    // 等待所有线程完成
    for (f in futures) {
        f.get()
    }

    println("Final count: " + count.load().toString())
}
```
