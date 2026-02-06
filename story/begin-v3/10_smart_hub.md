# 第十章：智能中枢 (综合实战)

> 我们将整合所有模块，构建一个“智能家居控制中枢 CLI”，它能够注册设备、批量控制并输出状态报告。
> 功能：
> 1.  **设备注册**：支持不同类型设备。
> 2.  **并发控制**：一键开启“离家模式”（并行关闭所有设备）。
> 3.  **状态查询**：实时显示系统概览。

## 本章目标

*   综合运用接口、集合与并发机制实现完整流程。
*   理解设备注册、批量控制与状态汇总的关键步骤。
*   建立“模块拆分 + 统一调度”的工程思路。

## 1. 完整系统实现

```cangjie
import std.collection.*
import std.sync.*
import std.time.*

// === 1. 核心协议 ===
interface SmartDevice {
    func getName(): String
    func turnOff(): Unit
    func getStatus(): String
}

// === 2. 设备实现 ===
class SmartLight <: SmartDevice {
    let name: String
    var isOn: Bool = true

    public init(name: String) { this.name = name }

    public func getName() = name

    public func turnOff() {
        // 模拟网络延迟
        sleep(Duration.millisecond * 100)
        isOn = false
        println("💡 [${name}] 已熄灭")
    }

    public func getStatus() = if (isOn) "ON" else "OFF"
}

class SmartSpeaker <: SmartDevice {
    let name: String
    var isPlaying: Bool = true

    public init(name: String) { this.name = name }

    public func getName() = name

    public func turnOff() {
        sleep(Duration.millisecond * 200)
        isPlaying = false
        println("🔇 [${name}] 已停止播放")
    }

    public func getStatus() = if (isPlaying) "PLAYING" else "IDLE"
}

// === 3. 控制中枢 ===
class SmartHomeHub {
    var devices = ArrayList<SmartDevice>()

    public func addDevice(dev: SmartDevice) {
        devices.append(dev)
        println("系统: 接入新设备 -> ${dev.getName()}")
    }

    // 离家模式：并发关闭所有设备
    public func activateAwayMode() {
        println("\n>>> 正在激活 [离家模式] <<<")
        let futures = ArrayList<Future<Unit>>()
        let start = DateTime.now()

        for (dev in devices) {
            // 为每个设备启动一个关闭任务
            let f = spawn {
                dev.turnOff()
            }
            futures.append(f)
        }

        // 等待所有设备响应
        for (f in futures) { f.get() }

        let end = DateTime.now()
        println(">>> 离家模式激活完成！耗时: ${(end - start).toMilliseconds()} ms\n")
    }

    public func reportStatus() {
        println("=== 系统状态报告 ===")
        for (dev in devices) {
            println("Device: ${dev.getName()} | Status: ${dev.getStatus()}")
        }
        println("==================")
    }
}

// === 4. 主程序入口 ===
main() {
    let hub = SmartHomeHub()

    // 1. 系统初始化，接入设备
    hub.addDevice(SmartLight("客厅主灯"))
    hub.addDevice(SmartLight("卧室台灯"))
    hub.addDevice(SmartSpeaker("小米音箱"))
    hub.addDevice(SmartLight("走廊灯带"))

    // 2. 查看当前状态
    hub.reportStatus()

    // 3. 用户出门，触发离家模式
    hub.activateAwayMode()

    // 4. 再次确认状态
    hub.reportStatus()
}
```

## 终章：万物互联

恭喜！你已经亲手构建了一个微型智能家居系统。

**知识回顾：**
*   **变量与类型**：定义传感器数据结构。
*   **流程控制**：实现自动化判断逻辑。
*   **函数与类**：封装设备驱动与模型。
*   **接口与多态**：统一不同品牌的控制协议。
*   **并发编程**：实现高效的批量控制。

智能家居只是物联网（IoT）的一个缩影。同样的逻辑可以应用在工业自动化、智慧城市等更广阔的领域。仓颉语言的高效与安全，将是你构建万物互联世界的坚实基石。

## 语言特性与应用解读

接口 `SmartDevice` 让控制中枢只依赖抽象能力，`public func getName() = name` 体现了表达式函数的简洁写法。
`if (isOn) "ON" else "OFF"` 也是表达式，适合用于状态映射，减少冗余分支。
`DateTime.now()` 与时间差计算展示了标准库时间 API，配合并发 `spawn` 与 `Future` 构成批量控制与耗时统计的完整链路。

## 工程化提示

*   批量控制设备时建议设置超时与失败重试机制。
*   设备状态上报应独立于控制流程，避免阻塞。
*   真实系统要考虑权限与安全验证，防止非法控制。

## 小试身手

1. 为 `SmartHomeHub` 增加 `removeDevice` 方法并测试。
2. 增加一个 `SmartThermostat` 设备，并在状态报告中输出当前温度。
