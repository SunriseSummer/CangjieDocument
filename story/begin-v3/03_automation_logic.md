# 第三章：自动化逻辑 (流程控制)

> 智能家居的核心在于"自动决策"。如果温度过高，自动开空调；如果没人在家，自动关灯。我们需要编写这些控制逻辑，并确保策略具备可解释性与可调节性。

## 本章目标

*   掌握条件分支与循环控制的基础语法。
*   学会将传感器阈值转化为可执行策略。
*   形成"循环监控 + 及时退出"的设计习惯。

## 1. 阈值判断 (if-else)

根据传感器数据做出响应。

<!-- check:run -->
```cangjie
main() {
    let temp = 31.0
    let userSetTemp = 26.0

    print("当前室温: ${temp}°C -> ")

    if (temp > userSetTemp + 2.0) {
        println("❄️ 降温模式：开启空调")
    } else if (temp < userSetTemp - 2.0) {
        println("☀️ 取暖模式：开启暖气")
    } else {
        println("🍃 节能模式：维持现状")
    }
}
```

## 2. 持续监控 (while 循环)

传感器需要全天候工作。我们需要一个主循环来不断轮询数据。

<!-- check:run -->
```cangjie
main() {
    var checkCount = 0
    var batteryLevel = 100

    println(">>> 开始持续监控...")

    // 模拟运行 5 个周期
    while (checkCount < 5) {
        if (batteryLevel < 10) {
            println("⚠️ 电量低！系统进入休眠。")
            break
        }

        checkCount = checkCount + 1
        batteryLevel = batteryLevel - 15
        println("第 ${checkCount} 次轮询: 状态正常 (电量 ${batteryLevel}%)")
    }
}
```

<!-- expected_output:
>>> 开始持续监控...
第 1 次轮询: 状态正常 (电量 85%)
第 2 次轮询: 状态正常 (电量 70%)
第 3 次轮询: 状态正常 (电量 55%)
第 4 次轮询: 状态正常 (电量 40%)
第 5 次轮询: 状态正常 (电量 25%)
-->

## 3. 设备自检 (for-in 循环)

系统启动时，需要遍历所有已连接的端口进行检查。

<!-- check:run -->
```cangjie
main() {
    println("正在扫描端口 1-4...")

    for (portId in 1..=4) {
        // 假设端口 3 是调试接口，跳过
        if (portId == 3) {
            continue
        }
        println("✅ 端口 ${portId}: 连接正常")
    }
}
```

<!-- expected_output:
正在扫描端口 1-4...
✅ 端口 1: 连接正常
✅ 端口 2: 连接正常
✅ 端口 4: 连接正常
-->

通过这些逻辑，原本冰冷的硬件开始表现出"智能"。

## 工程化提示

*   阈值判断要考虑"抖动区间"，避免频繁开关设备。
*   监控循环应设置休眠间隔，避免占满 CPU。
*   设备自检结果建议写入日志或上报平台。

## 小试身手

1. 为温度控制增加"迟滞区间"，减少频繁切换。
2. 在端口扫描中记录失败端口数量并输出汇总。
