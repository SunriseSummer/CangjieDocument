# 04. 策略函数与闭包：路径评分

> 调度不仅看优先级，还要衡量路网拥堵、距离与耗时。我们用函数与闭包构建“可替换的评分策略”。

## 本章目标

*   学会定义函数并封装业务计算。
*   理解高阶函数与闭包的策略化价值。
*   让调度逻辑具备可替换的评分模型。

## 1. 路径模型与评分

```cangjie
struct Route {
    let distanceKm: Float64
    let congestion: Int64 // 0-10
    let toll: Float64
}

type ScoreFn = (Route) -> Float64

func scoreRoute(route: Route, scorer: ScoreFn): Float64 {
    return scorer(route)
}
```

## 2. 策略示例

```cangjie
main() {
    let route = Route(18.5, 6, 12.0)

    // 快速优先策略：距离 + 拥堵权重
    let fastScore = scoreRoute(route) { r =>
        return r.distanceKm * 1.2 + Float64(r.congestion) * 3.0
    }

    // 成本优先策略：收费 + 拥堵权重
    let costScore = scoreRoute(route) { r =>
        return r.toll * 5.0 + Float64(r.congestion) * 2.0
    }

    println("快速策略评分: ${fastScore}")
    println("成本策略评分: ${costScore}")
}
```

代码要点：

`type ScoreFn = (Route) -> Float64` 把函数签名抽象成类型，使策略接口更稳定、更易复用。
传入的闭包 `{ r => ... }` 会捕获外部上下文，让评分逻辑可以在不改动核心函数的情况下灵活替换。
`Float64(r.congestion)` 展示了显式类型转换，确保算术计算的精度一致。

## 工程化提示

*   策略函数命名要表达业务意图，如 `scoreByFast`。
*   高阶函数对外接口要保持稳定，避免策略频繁调整导致调用方破坏。
*   在真实系统中，评分策略应支持配置化与版本化。

## 实践挑战

1. 新增一个“安全优先”策略，将拥堵权重提高。
2. 将 `ScoreFn` 改为返回结构体（含评分与说明）。
