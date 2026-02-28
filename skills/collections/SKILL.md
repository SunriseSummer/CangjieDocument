---
name: cangjie-collections
description: "仓颉语言集合类型。当需要了解仓颉语言的Array、ArrayList、HashMap、HashSet集合类型的构造、访问、修改、引用语义，以及Iterable/Iterator接口和for-in迭代机制时，应使用此 Skill。"
---

# 仓颉语言集合类型 Skill

## 1. 集合概述

仓颉提供 4 种核心集合类型：

| 类型 | 可修改元素 | 增删 | 唯一元素 | 有序 |
|------|:---:|:---:|:---:|:---:|
| `Array<T>` | ✅ | ❌ | ❌ | ✅ |
| `ArrayList<T>` | ✅ | ✅ | ❌ | ✅ |
| `HashSet<T>` | ❌ | ✅ | ✅ | ❌ |
| `HashMap<K, V>` | V: ✅ | ✅ | K: ✅ | ❌ |

### 使用场景
- **Array** — 固定大小；修改元素但不增删
- **ArrayList** — 频繁增删改
- **HashSet** — 确保元素唯一性
- **HashMap** — 存储键值映射

---

## 2. ArrayList

**导入**：`import std.collection.*`

**类型**：`ArrayList<T>` — `T` 可为任意类型。**引用类型**

### 2.1 构造
```cangjie
ArrayList<String>()                        // 空
ArrayList<String>(100)                     // 空，预分配容量 100
ArrayList<Int64>([0, 1, 2])                // 从 Array 字面量
ArrayList<Int64>(otherCollection)          // 从另一个 Collection
ArrayList<String>(2, {x: Int64 => x.toString()})  // size=2，lambda 初始化
```

### 2.2 访问元素
- **for-in 循环**：`for (i in list) { ... }`
- **size 属性**：`list.size`
- **下标**：`list[0]`、`list[1]` — 索引须为 `Int64`，从 0 开始。负数或越界 → **运行时异常**
- **范围下标**：支持（与 Array 语法相同）

### 2.3 修改
- **下标赋值**：`list[0] = 3`
- **引用语义**：`let list2 = list1` — 共享数据；通过任一引用的修改均可见
- **添加单个**：`list.add(element)`
- **添加多个**：`list.add(all: someCollection)`
- **在索引处插入**：`list.add(element, at: index)` / `list.add(all: collection, at: index)`
- **按索引删除**：`list.remove(at: index)`

### 2.4 容量管理
- ArrayList 容量不足时自动扩容（重新分配 + 复制）
- **预分配**：`ArrayList<Int64>(100)` 或 `list.reserve(100)` 以避免重复重分配

---

## 3. HashMap

**导入**：`import std.collection.*`

**类型**：`HashMap<K, V>` — `K` 须实现 `Hashable` 和 `Equatable<K>`。`V` 可为任意类型。**引用类型**

### 3.1 构造
```cangjie
HashMap<String, Int64>()                                    // 空
HashMap<String, Int64>([("a", 0), ("b", 1), ("c", 2)])     // 从元组数组
HashMap<String, Int64>(otherHashMap)                        // 从另一个 Collection
HashMap<String, Int64>(10)                                  // 空，容量 10
HashMap<Int64, Int64>(10, {x: Int64 => (x, x * x)})        // size=10，lambda 初始化
```

### 3.2 访问元素
- **for-in（解构）**：`for ((k, v) in map) { ... }` — **顺序不保证**
- **size 属性**：`map.size`
- **contains**：`map.contains("a")` → `Bool`
- **按键下标**：`map["a"]` — 键须存在否则**运行时异常**

### 3.3 修改
- **下标赋值（更新）**：`map["a"] = 3`
- **下标赋值（插入新键）**：`map["d"] = 3`
- **引用语义**：与 ArrayList 相同
- **添加单个**：`map.add("a", 0)` — 键已存在时**覆盖**旧值，返回 `Option<V>`（旧值或 `None`）
- **添加多个**：`map.add(all: otherMap)`
- **按键删除**：`map.remove("d")`

---

## 4. HashSet

**导入**：`import std.collection.*`

**类型**：`HashSet<T>` — `T` 须实现 `Hashable` 和 `Equatable<T>`。**引用类型**。元素一旦存储**不可修改**

### 4.1 构造
```cangjie
HashSet<String>()                                    // 空
HashSet<String>(100)                                 // 空，容量 100
HashSet<Int64>([0, 1, 2])                            // 从 Array 字面量
HashSet<Int64>(otherCollection)                      // 从另一个 Collection
HashSet<Int64>(10, {x: Int64 => (x * x)})            // size=10，lambda 初始化
```

### 4.2 访问元素
- **for-in 循环**：`for (i in mySet) { ... }` — **顺序不保证**
- **size 属性**：`mySet.size`
- **contains**：`mySet.contains(0)` → `Bool`
- **无下标访问**（无序，无索引概念）

### 4.3 修改
- **添加单个**：`mySet.add(0)` — 元素已存在时无效果（去重）
- **添加多个**：`mySet.add(all: someArray)`
- **引用语义**：与 ArrayList/HashMap 相同
- **删除**：`mySet.remove(1)` — 按元素值删除

---

## 5. Iterable 与集合

### 5.1 `Iterable<T>` 接口
```cangjie
interface Iterable<T> {
    func iterator(): Iterator<T>
}
```

### 5.2 `Iterator<T>` 接口
```cangjie
interface Iterator<T> <: Iterable<T> {
    mut func next(): Option<T>
}
```
- `Iterator` 自身扩展 `Iterable`
- `next()` 返回 `Option<T>` — `Some(value)` 或 `None` 表示结束

### 5.3 for-in 脱糖
```cangjie
for (i in list) { println(i) }
```
等价于：
```cangjie
var it = list.iterator()
while (true) {
    match (it.next()) {
        case Some(i) => println(i)
        case None => break
    }
}
```

### 5.4 谁实现了 Iterable？
**所有四种集合类型** — `Array`、`ArrayList`、`HashSet`、`HashMap` — 均实现 `Iterable`。自定义类型也可实现 `Iterable` 以获得 `for-in` 支持

---

## 6. 跨类型规则总结

| 规则 | 说明 |
|------|------|
| **类型安全** | 不同元素类型的集合不兼容 |
| **引用语义** | ArrayList、HashSet、HashMap 为引用类型 — 赋值创建别名。Array 虽为 struct 类型，但赋值也共享底层数据 |
| **泛型约束** | HashSet 的 `T` 和 HashMap 的 `K` 须实现 `Hashable + Equatable`。ArrayList 的 `T` 和 HashMap 的 `V` 无约束 |
| **有序性** | Array 和 ArrayList 有序（有索引）。HashSet 和 HashMap 无序 |
| **下标访问** | Array/ArrayList：`Int64` 索引。HashMap：键。HashSet：无 |
| **越界/缺失键** | 无效索引或缺失键导致运行时异常 |
| **容量预分配** | ArrayList 和 HashSet 支持构造函数中的容量提示 |
| **Lambda 初始化** | 所有类型支持 `(size, lambda)` 构造函数 |
| **迭代** | 所有类型通过 `Iterable<T>` 接口支持 `for-in` |
