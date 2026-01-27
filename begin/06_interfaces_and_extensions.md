# 06. 接口与扩展：万能支付网关

在现实开发中，我们经常需要对接不同的系统（如支付宝、微信支付、银联）。如何用一套代码兼容它们？答案是**接口 (Interface)**。

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
func processPayment(gateway: PaymentGateway, price: Float64) {
    println("--- 开始交易 ---")
    gateway.pay(price)
    println("--- 交易结束 ---\n")
}

main() {
    let ali = AliPay()
    let wechat = WeChatPay()

    let price = 99.9

    // 用户选择支付宝
    processPayment(ali, price)

    // 用户选择微信
    processPayment(wechat, price)
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
