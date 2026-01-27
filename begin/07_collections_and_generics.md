# 07. 集合与泛型

## 1. 常用集合

仓颉提供了丰富的集合类型，最常用的有 `Array`, `ArrayList` 和 `HashMap`。

### Array (数组)

`Array` 是固定大小的序列。

```cangjie
main() {
    // 定义并初始化数组
    let arr: Array<Int64> = [1, 2, 3, 4, 5]

    // 访问元素
    println("First element: " + arr[0].toString())

    // 遍历数组
    for (num in arr) {
        println("Number: " + num.toString())
    }
}
```

### ArrayList (动态数组)

`ArrayList` 是可变大小的序列，需要导入 `std.collection` 包。

```cangjie
import std.collection.*

main() {
    // 创建空的 ArrayList
    let list = ArrayList<String>()

    // 添加元素
    list.append("Apple")
    list.append("Banana")

    println("Size: " + list.size.toString())

    // 遍历
    for (item in list) {
        println(item)
    }
}
```

### HashMap (哈希表)

`HashMap` 用于存储键值对 (Key-Value)。

```cangjie
import std.collection.*

main() {
    // 创建 HashMap
    let map = HashMap<String, Int64>()

    // 添加或更新键值对
    map["Apple"] = 10
    map["Banana"] = 5

    // 安全访问
    let searchKey = "Apple"
    if (map.contains(searchKey)) {
        let price = map[searchKey]
        println("${searchKey} price: ${price}")
    } else {
        println("${searchKey} not found")
    }

    // 遍历 (顺序不保证)
    for ((k, v) in map) {
        println("Key: ${k}, Value: ${v}")
    }
}
```

## 2. 泛型 (Generics)

泛型允许我们编写适用于多种类型的代码，提高代码复用率和安全性。

### 泛型函数

我们可以定义一个泛型函数，用 `T` 代表任意类型。

```cangjie
// 交换数组中两个元素的位置
func swap<T>(arr: Array<T>, i: Int64, j: Int64) {
    let temp = arr[i]
    arr[i] = arr[j]
    arr[j] = temp
}

main() {
    let nums = [1, 2, 3]
    swap<Int64>(nums, 0, 2) // 显式指定类型，通常可省略
    println(nums[0]) // 输出 3
}
```

### 泛型类

```cangjie
class Box<T> {
    var value: T

    init(v: T) {
        value = v
    }

    func get(): T {
        return value
    }
}

main() {
    let intBox = Box<Int64>(100)
    let strBox = Box<String>("Cangjie")

    println(intBox.get())
    println(strBox.get())
}
```
