# 第七章：数据中心 (集合与泛型)

> 智能家居系统连接了上百个设备，分布在不同房间。我们需要高效的数据结构来管理这些设备列表和配置信息，并为后续的状态汇总提供支撑。

## 本章目标

*   掌握哈希表与列表的典型应用场景。
*   学会用泛型配置结构承载不同类型的参数。
*   理解缓存数据在可视化与分析中的作用。

## 1. 房间设备管理 (HashMap)

我们需要根据房间名快速查找该房间内的所有设备 ID。

```cangjie
import std.collection.*

main() {
    // Key: 房间名, Value: 设备ID列表
    let roomDevices = HashMap<String, ArrayList<String>>()

    // 初始化客厅
    let livingList = ArrayList<String>()
    livingList.append("L-001 (Main Light)")
    livingList.append("AC-001 (Air Conditioner)")
    roomDevices["Living Room"] = livingList

    // 初始化卧室
    let bedList = ArrayList<String>()
    bedList.append("L-002 (Bed Light)")
    roomDevices["Bedroom"] = bedList

    // 查询客厅有哪些设备
    if (roomDevices.contains("Living Room")) {
        println("客厅设备清单:")
        for (dev in roomDevices["Living Room"]) {
            println("- " + dev)
        }
    }
}
```

## 2. 通用配置加载器 (Generics)

系统配置项有多种类型：有的配置是数字（超时时间），有的是字符串（WiFi密码）。我们定义一个泛型配置类。

```cangjie
struct ConfigItem<T> {
    let key: String
    let value: T

    public func printConfig() {
        println("配置项 [${key}] = ${value}")
    }
}

main() {
    // 整数类型的配置
    let timeout = ConfigItem<Int64>("TimeoutMS", 5000)
    timeout.printConfig()

    // 字符串类型的配置
    let wifi = ConfigItem<String>("SSID", "MySmartHome_5G")
    wifi.printConfig()
}
```

## 3. 历史数据缓存 (ArrayList)

我们需要缓存最近 10 条温度记录用于绘图。

```cangjie
import std.collection.*

main() {
    let history = ArrayList<Float64>()

    // 模拟存入数据
    history.append(23.5)
    history.append(23.6)
    history.append(23.8)

    println("缓存记录数: ${history.size}")

    // 计算平均温
    var sum = 0.0
    for (val in history) { sum = sum + val }
    println("平均温度: ${sum / Float64(history.size)}")
}
```

## 工程化提示

*   房间设备映射应考虑同步更新机制，避免配置漂移。
*   泛型配置建议配合校验规则，确保值合法。
*   历史数据缓存要控制容量，避免内存持续增长。

## 小试身手

1. 为 `roomDevices` 增加“删除设备”逻辑，并在输出中验证。
2. 将温度缓存改为固定容量（超过 10 条时移除最旧记录）。
