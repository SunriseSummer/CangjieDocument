# 05. 集合与泛型：路线缓存

> 高峰期每分钟有数百条路线计算。如果每次都从头计算，系统会被拖慢。我们需要用集合与泛型做缓存。

## 本章目标

*   熟悉 `HashMap` 与 `ArrayList` 的典型使用场景。
*   使用泛型构建可复用的缓存结构。
*   建立“高频访问应缓存”的工程意识。

## 1. 路线缓存容器

```cangjie
import std.collection.*
import std.sync.*

struct Route {
    let distanceKm: Float64
    let congestion: Int64
    let toll: Float64
}

class Cache<T> {
    var items = HashMap<String, T>()
    let lock = Mutex()

    public func put(key: String, value: T) {
        synchronized(lock) {
            items[key] = value
        }
    }

    public func get(key: String): Option<T> {
        synchronized(lock) {
            if (items.contains(key)) {
                return Some(items[key])
            }
            return None
        }
    }
}
```

## 2. 应用缓存

```cangjie
main() {
    let routeCache = Cache<Route>()
    let route = Route(12.0, 3, 6.0)

    routeCache.put("W1->D3", route)

    if (let Some(r) <- routeCache.get("W1->D3")) {
        println("命中缓存: ${r.distanceKm}km")
    } else {
        println("未命中缓存，重新计算")
    }
}
```

代码要点：

`Cache<T>` 展示了泛型类的可复用能力，不同类型的缓存可共享同一套逻辑。
`Mutex` 与 `synchronized(lock)` 提供最基础的临界区保护，避免并发写入导致缓存失真。
`Option` 返回值让调用端明确区分“命中”与“未命中”，避免使用空值判断。

## 工程化提示

*   缓存要设置过期策略，避免过时数据影响调度。
*   对频繁访问的数据可做预热，减少首次请求延迟。
*   HashMap Key 建议统一格式，避免重复命中失败。

## 实践挑战

1. 为 `Cache` 增加 `remove` 与 `contains` 方法。
2. 用 `ArrayList` 记录最近 5 次命中缓存的路线 Key。
