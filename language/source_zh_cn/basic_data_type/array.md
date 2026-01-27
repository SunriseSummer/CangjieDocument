# 数组类型

仓颉提供了两种数组类型：
1.  **`Array<T>`**: **引用类型**数组。这是最常用的数组，支持动态操作（如获取切片），存储在堆上。
2.  **`VArray<T, $N>`**: **值类型**数组。长度固定，存储在栈或包含它的结构体中，通常用于高性能场景或与 C 语言交互。

---

## 1. Array (引用类型)

`Array<T>` 是一个泛型类型，`T` 代表元素类型。

### 创建数组

#### 使用字面量
最简单的方式是使用方括号 `[]`。

<!-- compile -->
```cangjie
let arr1 = [1, 2, 3]          // 推断为 Array<Int64>
let arr2: Array<String> = []  // 空数组
```

#### 使用构造函数
- `Array<T>(size, repeat: value)`: 创建指定长度的数组，填充相同的值。
- `Array<T>(size, init_func)`: 创建指定长度的数组，通过函数初始化每个元素。

<!-- compile -->
```cangjie
let zeros = Array<Int64>(5, repeat: 0) // [0, 0, 0, 0, 0]
let seq = Array<Int64>(5, { i => i * i }) // [0, 1, 4, 9, 16]
```

> **⚠️ 注意**: 使用 `repeat` 初始化时，如果元素是引用类型，所有位置将指向同一个对象。

### 访问与修改

#### 索引访问
使用下标 `[index]` 访问元素。索引从 0 开始。

<!-- verify -->
```cangjie
main() {
    let arr = [10, 20, 30]
    println(arr[1]) // 20

    arr[1] = 99
    println(arr[1]) // 99
}
```

#### 获取长度
使用 `.size` 属性。

```cangjie
let len = arr.size
```

#### 切片 (Slicing)
使用区间操作符获取数组的一部分（返回一个新的 Array 视图或拷贝，具体视实现而定，但在仓颉中通常是切片操作）。

<!-- compile -->
```cangjie
let arr = [0, 1, 2, 3, 4]
let sub = arr[1..3] // [1, 2] (包含 start，不包含 end)
let sub2 = arr[2..=4] // [2, 3, 4]
```

### 引用语义
由于 `Array` 是引用类型，将一个数组变量赋值给另一个变量，它们将指向**同一个**数组对象。修改其中一个会影响另一个。

<!-- verify -->
```cangjie
main() {
    let a = [1, 2]
    let b = a
    b[0] = 100
    println(a[0]) // 100
}
```

---

## 2. VArray (值类型)

`VArray<T, $N>` 是固定长度的值类型数组。`$N` 是一个特殊的语法，用于在类型中指定长度（如 `$3`）。

### 适用场景
- 极高性能敏感的代码，减少 GC 压力。
- 与 C 语言接口 (FFI) 交互，对应 C 的定长数组。

### 限制
- 长度 `N` 必须是编译时确定的整数。
- 赋值是**拷贝**语义（整个数组被复制）。
- 不支持动态扩容。

### 创建与使用

#### 字面量初始化
必须显式指定类型，因为字面量默认推断为 `Array`。

<!-- compile -->
```cangjie
var va: VArray<Int64, $3> = [1, 2, 3]
```

#### 构造函数
<!-- compile -->
```cangjie
let v1 = VArray<Int64, $5>(repeat: 0)
let v2 = VArray<Int64, $5>({ i => i })
```

#### 值语义演示

<!-- verify -->
```cangjie
main() {
    var a: VArray<Int64, $2> = [1, 2]
    var b = a  // 发生整个数组的拷贝
    b[0] = 100
    println(a[0]) // 1 (a 不受影响)
}
```
