# 04. 函数与闭包：凯撒密码

编程的核心在于将复杂问题分解。本节我们将通过实现一个古老的加密技术——“凯撒密码”，来学习函数和闭包。

## 1. 打造加密机器 (定义函数)

凯撒密码的原理是将字母表中的每个字母向后移动固定位数。例如，移动 1 位，'A' 变成 'B'。

```cangjie
// 字符处理函数：将单个字符加密
func encryptChar(char: Rune, shift: Int64): Rune {
    // 简单的位移算法 (仅演示原理，非生产级加密)
    let base = UInt32(char)
    let newChar = Rune(base + UInt32(shift))
    return newChar
}

// 主加密函数
func encryptMessage(msg: String, key: Int64): String {
    var result = ""
    for (char in msg) {
        let encrypted = encryptChar(char, key)
        result = result + encrypted.toString()
    }
    return result
}

main() {
    let secret = "Cangjie"
    let key = 1

    let encoded = encryptMessage(secret, key)
    println("原文: " + secret)
    println("密文: " + encoded)
}
```

## 2. 定制化加密 (高阶函数与 Lambda)

如果我们想让加密算法更灵活，比如允许用户自定义“如何处理每个字符”，该怎么办？

我们可以让函数接收另一个函数作为参数。

```cangjie
// 通用处理器：它不知道具体做什么，全看 `processor` 怎么说
func processString(text: String, processor: (Rune) -> Rune): String {
    var result = ""
    for (char in text) {
        result = result + processor(char).toString()
    }
    return result
}

main() {
    let text = "Hello"

    // 场景 1: 加密 (Lambda 表达式)
    let encrypted = processString(text) { c =>
        return Rune(UInt32(c) + 1)
    }
    println("加密后: " + encrypted)

    // 场景 2: 掩码 (把所有字符变成 '*')
    let masked = processString(text) { c => '*' }
    println("掩码后: " + masked)
}
```

通过这种方式，我们的代码变得极具扩展性。这就是函数式编程的魅力。
