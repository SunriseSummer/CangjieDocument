# 第五章：设备建模 (结构体与类)

> 现实世界中，灯泡、恒温器、摄像头都有各自的属性和行为。我们需要在代码中对这些实体进行建模。

## 1. 数据采集点 (Struct)

传感器上报的数据包通常是只读的快照，适合使用 `struct`（值类型）。

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

```cangjie
class SmartLight {
    let id: String
    var brightness: Int64 // 0-100
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
