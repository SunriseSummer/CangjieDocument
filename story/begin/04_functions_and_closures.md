# 04. 函数与闭包：凯撒密码

编程的核心在于将复杂问题分解。本节我们将通过实现一个古老的加密技术——“凯撒密码”，来学习函数和闭包。

## 本章目标

*   学会定义函数与拆分逻辑，提高复用性。
*   理解高阶函数与闭包在“自定义行为”中的价值。
*   认识函数式思维在工程扩展上的优势。

## 1. 打造加密机器 (定义函数)

凯撒密码的原理是将字母表中的每个字母向后移动固定位数。例如，移动 1 位，'A' 变成 'B'。

```cangjie
// 字符处理函数：将单个字符加密
func encryptChar(char: Rune, shift: Int64): Rune {
    // 简单的位移算法 (仅演示原理，非生产级加密)
    let code = UInt32(char)
    let lowerA = UInt32('a')
    let lowerZ = UInt32('z')
    let upperA = UInt32('A')
    let upperZ = UInt32('Z')

    if (code >= lowerA && code <= lowerZ) {
        return Rune(lowerA + (code - lowerA + UInt32(shift)) % 26)
    }
    if (code >= upperA && code <= upperZ) {
        return Rune(upperA + (code - upperA + UInt32(shift)) % 26)
    }
    return char
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

通过这种方式，我们的代码变得极具扩展性。这就是函数式编程在工程中可组合、可替换的魅力。

## 工程化提示

*   生产环境中的加密逻辑必须使用标准安全算法，本例仅演示函数拆分思路。
*   处理字符时注意范围边界，避免超出合法字符集导致不可预期结果。
*   高阶函数要控制参数数量与命名，避免接口难以理解。

## 小试身手

1. 为 `encryptMessage` 增加解密函数 `decryptMessage`。
2. 让 `processString` 支持传入“是否跳过空格”的策略参数。
