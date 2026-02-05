# 06. 接口与扩展：万能支付网关

在现实开发中，我们经常需要对接不同的系统（如支付宝、微信支付、银联）。如何用一套代码兼容它们？答案是**接口 (Interface)**。

## 本章目标

*   理解接口在“能力抽象”上的价值。
*   学会通过多态实现“调用方与实现方解耦”。
*   掌握扩展现有类型的安全方式。

## 1. 定义支付标准 (Interface)

不管是什么支付方式，都必须具备“支付”这个能力。

```cangjie
interface PaymentGateway {
    func pay(amount: Float64): Unit
    func refund(amount: Float64): Unit
}
```

## 2. 对接不同渠道 (Implementation)

```cangjie
class AliPay <: PaymentGateway {
    public func pay(amount: Float64) {
        println("🔵 支付宝支付: ¥${amount} (正在连接蚂蚁金服...)")
    }

    public func refund(amount: Float64) {
        println("🔵 支付宝退款: ¥${amount}")
    }
}

class WeChatPay <: PaymentGateway {
    public func pay(amount: Float64) {
        println("🟢 微信支付: ¥${amount} (正在调用微信 API...)")
    }

    public func refund(amount: Float64) {
        println("🟢 微信退款: ¥${amount}")
    }
}
```

## 3. 统一收银台 (多态)

收银台不需要知道用户具体用什么 App，它只认“支付网关”。

```cangjie
func processPayment(gateway: PaymentGateway, price: Float64, orderId: String) {
    println("--- 开始交易: ${orderId} ---")
    gateway.pay(price)
    println("--- 交易结束: ${orderId} ---\n")
}

main() {
    let ali = AliPay()
    let wechat = WeChatPay()

    let price = 99.9

    // 用户选择支付宝
    processPayment(ali, price, "ORD-2024-0001")

    // 用户选择微信
    processPayment(wechat, price, "ORD-2024-0002")
}
```

## 4. 扩展现有能力 (Extensions)

为了防止支付金额出现负数，我们想给系统的 `Float64` 类型加个检查功能，但我们不能修改系统源码。扩展（Extend）来帮忙！

```cangjie
extend Float64 {
    func isValidMoney(): Bool {
        return this >= 0.0
    }
}

main() {
    let money = -10.0
    if (!money.isValidMoney()) {
        println("❌ 错误：金额不能为负！")
    }
}
```

## 工程化提示

*   接口定义应保持精简稳定，避免在上层频繁变动。
*   不同支付渠道的差异建议通过配置或适配层处理，避免业务逻辑分散。
*   扩展方法命名要清晰，避免与未来标准库接口冲突。

## 小试身手

1. 为 `PaymentGateway` 增加 `queryStatus()` 方法并在两种实现中补齐。
2. 将 `processPayment` 的输出改为结构化日志格式（例如添加交易号）。
