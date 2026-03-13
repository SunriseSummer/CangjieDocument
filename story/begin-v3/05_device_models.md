# 第五章：设备建模 (结构体与类)

> 现实世界中，灯泡、恒温器、摄像头都有各自的属性和行为。我们需要在代码中对这些实体进行建模，确保数据快照与设备状态被正确区分。

## 本章目标

*   理解结构体与类在智能设备建模中的区别。
*   学会为实体添加初始化与行为方法。
*   认识状态对象在系统中的生命周期管理。

## 1. 数据采集点 (Struct)

传感器上报的数据包通常是只读的快照，适合使用 `struct`（值类型）。

<!-- check:run project=device_models -->
```cangjie
struct SensorPacket {
    let timestamp: Int64
    let value: Float64
    let unit: String

    public init(val: Float64, unit: String) {
        this.timestamp = 1718888888 // 模拟时间戳
        this.value = val
        this.unit = unit
    }

    public func log() {
        println("[Log] Value: ${value}${unit}")
    }
}
```

## 2. 物理设备 (Class)

一个真实的灯泡是有状态的（开/关，亮度），且在这个系统中是唯一的对象，适合使用 `class`（引用类型）。

<!-- check:run project=device_models -->
```cangjie
class SmartLight {
    let id: String
    var brightness: Int64
    var isOn: Bool

    public init(id: String) {
        this.id = id
        this.brightness = 0
        this.isOn = false
    }

    public func turnOn() {
        isOn = true
        brightness = 100
        println("💡 灯光 [${id}] 已开启")
    }

    public func dim(level: Int64) {
        if (isOn) {
            brightness = level
            println("💡 灯光 [${id}] 亮度调节为 ${level}%")
        }
    }
}

main() {
    // 收到一个传感器数据包
    let data = SensorPacket(25.5, "C")
    data.log()

    // 控制客厅主灯
    let livingRoomLight = SmartLight("L-001")
    livingRoomLight.turnOn()
    livingRoomLight.dim(50)
}
```

<!-- expected_output:
[Log] Value: 25.500000C
💡 灯光 [L-001] 已开启
💡 灯光 [L-001] 亮度调节为 50%
-->

## 工程化提示

*   传感器数据应带上时间戳与来源，便于回溯。
*   对设备状态的修改建议集中在方法内，避免外部随意写入。
*   设备 ID 与业务命名需保持一致，避免资产管理混乱。

## 小试身手

1. 为 `SmartLight` 增加 `turnOff()` 方法并更新状态。
2. 在 `SensorPacket` 中加入 `sensorId` 字段并输出。
