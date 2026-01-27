# 字符类型

仓颉语言使用 **`Rune`** 类型来表示字符。与许多传统语言不同，`Rune` 可以表示所有的 Unicode 字符，而不仅仅是 ASCII 字符。

## 1. 字符字面量

字符字面量使用字符 `r` 开头，后跟一对单引号 `'` 或双引号 `"` 包围的单个字符。

<!-- compile -->
```cangjie
let a: Rune = r'a'
let b: Rune = r"b"
let cn: Rune = r'仓' // 支持 Unicode 字符
```

### 转义字符
对于特殊字符，可以使用反斜杠 `\` 进行转义。

| 转义序列 | 说明 |
| :--- | :--- |
| `\\` | 反斜杠本身 |
| `\'`, `\"` | 单引号，双引号 |
| `\n` | 换行符 |
| `\r` | 回车符 |
| `\t` | 制表符 |
| `\0` | 空字符 |
| `\u{...}` | Unicode 转义 (十六进制) |

<!-- verify -->
```cangjie
main() {
    let newline = r'\n'
    let smile = r'\u{1F600}' // 😀
    println(smile)
}
```

## 2. 字符操作

`Rune` 类型支持比较操作符，比较的是其对应的 Unicode 标量值。

<!-- verify -->
```cangjie
main() {
    println(r'a' < r'b') // true
    println(r'仓' == r'仓') // true
}
```

> **注意**: `Rune` 类型和整数类型之间不能直接隐式转换，需要使用显式转换。详情请参考[类型转换](../class_and_interface/typecast.md)。
