# 字符串类型

字符串类型 **`String`** 用于表示文本数据，它是由一系列 Unicode 字符组成的序列。

## 1. 字符串字面量

仓颉提供了多种定义字符串的方式，以适应不同的场景。

### 单行字符串
使用一对双引号 `"` 或单引号 `'` 包围。
- **限制**: 必须写在同一行内。

<!-- compile -->
```cangjie
let s1 = "Hello, Cangjie"
let s2 = 'Hello, World'
```

### 多行字符串
使用三个双引号 `"""` 或三个单引号 `'''` 包围。
- **特点**: 可以跨越多行，保留换行符。
- **起止规则**: 内容从开头引号换行后的第一行开始，直到结束引号所在行的前一行。

<!-- compile -->
```cangjie
let poem = """
    白日依山尽，
    黄河入海流。
    """
```

### 原始字符串 (Raw String)
使用 `#` 号和引号组合（如 `#""#`, `##""##`）。
- **特点**: **不进行转义**。字符串内的内容（包括 `\`）会原样保留。
- **用途**: 适合编写正则表达式、Windows 路径等包含大量反斜杠的内容。
- **定界符**: 开头有几个 `#`，结尾就必须有几个 `#`。这允许字符串内部包含引号。

<!-- compile -->
```cangjie
let path = #"C:\Users\Admin\Documents"#
let regex = ##"Pattern with "quotes" inside"##
```

## 2. 插值字符串

**插值字符串**允许您直接在字符串中嵌入变量或表达式，极大简化了字符串拼接。
- **语法**: `${表达式}`。如果是简单的变量名，也可以省略花括号（视具体编译器实现而定，但建议始终加上 `{}` 以保持清晰）。
- **适用范围**: 普通单行和多行字符串（原始字符串不支持插值）。

<!-- verify -->
```cangjie
main() {
    let name = "Cangjie"
    let age = 1

    // 嵌入变量
    println("Language: ${name}, Age: ${age}")

    // 嵌入表达式
    println("Next year age: ${age + 1}")

    // 甚至可以嵌入代码块
    println("Result: ${ if (age > 0) "Active" else "Inactive" }")
}
```

## 3. 常用操作

### 拼接
使用 `+` 操作符可以将两个字符串拼接在一起。

```cangjie
let s = "Hello" + " " + "World"
```

### 比较
支持 `==`, `!=`, `<`, `>` 等比较操作符，基于字典序比较。

```cangjie
if ("apple" < "banana") {
    println("apple comes first")
}
```

### 常用方法
`String` 类型提供了丰富的方法，如 `contains`, `split`, `replace` 等。

<!-- run -->
```cangjie
main() {
    let text = "Hello, Cangjie"

    println(text.contains("Cangjie")) // true
    println(text.split(", ")[0])      // Hello
}
```

## 4. 特殊赋值规则: Byte 和 Rune

为了方便处理底层数据，仓颉允许将特定的**字符串字面量**赋值给 `Byte` (UInt8) 或 `Rune` 类型的变量。
- **Byte**: 字符串必须是单个 ASCII 字符（如 `"A"`）。
- **Rune**: 字符串必须是单个 Unicode 字符（如 `"仓"`）。

<!-- verify -->
```cangjie
main() {
    let b: Byte = "A"   // 等价于 let b: Byte = 65
    let r: Rune = "仓"  // 等价于 let r: Rune = r'仓'
    println("${b}, ${r}")
}
```
