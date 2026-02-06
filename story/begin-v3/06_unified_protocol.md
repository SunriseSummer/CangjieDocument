# 第六章：统一协议 (接口与扩展)

> 你的系统需要支持小米、飞利浦、华为等不同品牌的设备。你不可能为每个品牌写一套代码。你需要定义一个“统一控制协议”（Interface），把差异隔离在适配层。

## 本章目标

*   学会使用接口抽象跨品牌设备能力。
*   理解多态在统一控制中的作用。
*   掌握扩展标准类型的安全方式。

## 1. 定义协议标准 (Interface)

不管是什么设备，只要接在电源上，就应该能“开关”。

```cangjie
interface Switchable {
    func on(): Unit
    func off(): Unit
    func getStatus(): String
}
```

## 2. 厂商适配 (Implementation)

不同厂商的设备底层指令可能不同，但都必须实现上述接口。

```cangjie
class PhilipsHue <: Switchable {
    public func on() { println("Hue: 发送 Zigbee 开启指令") }
    public func off() { println("Hue: 发送 Zigbee 关闭指令") }
    public func getStatus(): String { return "Hue Online" }
}

class XiaomiPlug <: Switchable {
    public func on() { println("Mi: 发送 Wi-Fi 开启指令") }
    public func off() { println("Mi: 发送 Wi-Fi 关闭指令") }
    public func getStatus(): String { return "Mi Plug Active" }
}
```

## 3. 统一控制中心 (多态)

控制中心不需要知道设备品牌，只认 `Switchable` 协议。

```cangjie
func masterSwitch(device: Switchable, state: Bool) {
    if (state) device.on() else device.off()
}

main() {
    let lamp = PhilipsHue()
    let fan = XiaomiPlug()

    println("--- 一键全开 ---")
    masterSwitch(lamp, true)
    masterSwitch(fan, true)
}
```

## 4. 扩展现有功能 (Extensions)

你想让所有的字符串（比如设备日志）都能自动加上时间戳，但不能修改系统 String 类的源码。

```cangjie
extend String {
    func withTime(): String {
        return "[2024-01-01 12:00:00] " + this
    }
}

main() {
    let log = "系统异常重启"
    println(log.withTime())
}
```

代码要点：

接口 `Switchable` 定义了稳定的能力契约，实现类通过 `<:` 声明遵循协议，调用端只依赖接口即可获得多态行为。
`masterSwitch` 的参数是接口类型，编译器会在运行时分派到具体实现，实现“品牌无关”的控制。
`extend` 为现有类型添加方法，`this` 代表被扩展的实例，它不会破坏原有类型，适合作为工具增强层。

## 工程化提示

*   协议定义要稳定清晰，避免频繁变更影响所有设备实现。
*   适配层可以隔离厂商差异，保持核心业务逻辑统一。
*   时间戳示例为占位，真实系统应调用统一时间服务。

## 小试身手

1. 为 `Switchable` 增加 `restart()` 方法，并在实现中补齐。
2. 扩展 `String` 增加 `withLevel(level: String)`，输出日志级别。
