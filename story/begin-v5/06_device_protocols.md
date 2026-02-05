# 06. 接口与扩展：设备协议

> 星港物流中心有 GPS、温度计、闸机等设备。不同厂商协议不同，但我们希望调度层只面对统一接口。

## 本章目标

*   使用接口抽象设备能力。
*   通过多态屏蔽厂商差异。
*   了解 `extend` 为基础类型添加工具方法。

## 1. 统一设备接口

```cangjie
interface Telemetry {
    func read(): SensorPacket
}

struct SensorPacket {
    let deviceId: String
    let value: Float64
    let capturedTimestamp: Int64
}

class GpsSensor <: Telemetry {
    public func read(): SensorPacket {
        return SensorPacket("GPS-01", 31.2, 1718888888)
    }
}
```

## 2. 扩展基础类型

```cangjie
extend Float64 {
    func asKm(): String {
        return "${this} km"
    }
}

main() {
    let distance = 12.5
    println("路程: " + distance.asKm())
}
```

## 工程化提示

*   接口定义要稳定，避免频繁改动影响所有设备。
*   适配器层应隔离协议细节，核心业务只面向接口。
*   扩展方法命名要清晰，避免与标准库冲突。

## 实践挑战

1. 增加 `GateSensor` 设备并实现 `Telemetry`。
2. 为 `SensorPacket` 增加 `toLog()` 方法输出结构化日志。
