# 第六章：统一协议 (接口与扩展)

> 你的系统需要支持小米、飞利浦、华为等不同品牌的设备。你不可能为每个品牌写一套代码。你需要定义一个“统一控制协议”（Interface）。

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
