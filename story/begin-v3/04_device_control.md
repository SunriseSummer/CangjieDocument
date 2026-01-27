# 第四章：设备驱动 (函数与闭包)

> 随着接入设备增多，直接写 `if-else` 会让代码变得难以维护。我们需要将特定设备的控制逻辑封装成“驱动函数”。

## 1. 封装控制指令 (定义函数)

将“打开空调”这个动作封装起来，无论在哪个房间，调用方式都一样。

```cangjie
// 定义驱动函数
func setAirConditioner(mode: String, temp: Int64) {
    println("📡 发送指令 -> 空调: 模式[${mode}], 设定温度[${temp}]")
    // 这里可以是真实的硬件 I/O 操作
}

main() {
    // 业务逻辑调用，无需关心底层硬件细节
    setAirConditioner("制冷", 24)
}
```

## 2. 场景模式 (高阶函数)

用户常定义“离家模式”或“观影模式”。这些模式本质上是一系列指令的组合。我们可以编写一个“场景执行器”。

```cangjie
// 场景执行器：接收一个函数作为具体场景逻辑
func executeScene(sceneName: String, action: () -> Unit) {
    println(">>> 正在激活场景: ${sceneName}")
    action() // 执行传入的逻辑
    println(">>> 场景激活完毕\n")
}

main() {
    // 定义离家模式 (Lambda)
    let awayMode = { =>
        println(" - 关闭所有灯光")
        println(" - 开启安防摄像头")
        println(" - 锁定大门")
    }

    // 执行
    executeScene("离家模式", awayMode)
}
```

通过函数，我们将“做什么”（业务）和“怎么做”（实现）分离开来，这是现代软件工程的基石。
