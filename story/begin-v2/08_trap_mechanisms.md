# 第八章：机关陷阱 (错误处理)

> 塔的高层布满了致命机关。有些宝箱是空的（Option），有些拉杆会触发爆炸（Exception）。你需要学会如何安全地通过这些区域。

## 本章目标

*   理解 `Option` 的安全返回方式。
*   掌握异常捕获的基本流程与资源清理。
*   学会用模式匹配处理复杂分支。

## 1. 薛定谔的宝箱 (Option)

这个宝箱可能含有传说装备，也可能什么都没有。在打开之前，它是未知的。

```cangjie
func openChest(id: Int64): Option<String> {
    if (id == 888) {
        return Some("圣剑")
    } else {
        return None // 空空如也
    }
}

main() {
    let loot = openChest(888)

    // 安全检查模式
    match (loot) {
        case Some(item) => println("✨ 哇！获得了: ${item}")
        case None => println("💨 又是空的...")
    }
}
```

## 2. 拆除炸弹 (Try-Catch)

如果你剪错了线，就会触发异常。

```cangjie
func defuseBomb(wireColor: String) {
    if (wireColor == "Red") {
        throw Exception("轰！！！炸弹爆炸了！")
    }
    println("✅ 拆弹成功: ${wireColor} 线是安全的。")
}

main() {
    println("发现定时炸弹！尝试拆除...")

    try {
        defuseBomb("Red") // 尝试剪红线
    } catch (e: Exception) {
        // 捕获了异常，幸好有“复活币”
        println("🚑 受到重伤: " + e.message)
        println("使用复活币... 身体重组中...")
    } finally {
        println("无论死活，这场试炼结束了。")
    }
}
```

## 3. 机关解析 (Pattern Matching)

面对复杂的符文锁，你需要根据图案做出不同反应。

```cangjie
enum RuneLock {
    | Triangle
    | Square(Int64) // 带数字的方块
    | Circle
}

func unlock(shape: RuneLock) {
    match (shape) {
        case Triangle => println("按下三角形按钮。")
        case Square(num) => println("输入密码: ${num}")
        case Circle => println("旋转圆形转盘。")
    }
}

main() {
    let lock = Square(1234)
    unlock(lock)
}
```

## 工程化提示

*   能用 `Option`/`Result` 表达的错误优先使用返回值，异常用于不可恢复错误。
*   捕获异常时应记录上下文信息，方便复盘与定位。
*   模式匹配要覆盖所有分支，避免遗漏带来的运行期错误。

## 小试身手

1. 为 `openChest` 增加“陷阱宝箱”分支，返回失败原因。
2. 扩展 `RuneLock` 增加新图案，并在 `unlock` 中处理。
