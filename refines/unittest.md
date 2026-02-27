# 仓颉单元测试框架精炼总结

> 本文档面向 AI 工具，精炼覆盖仓颉（Cangjie）单元测试框架的核心内容，包括测试编写、断言、参数化测试、Mock 框架和基准测试。

---

## 1. 快速入门

### 1.1 编写测试

```cangjie
// add.cj
func add(left: Int64, right: Int64): Int64 {
    return left + right
}

// add_test.cj
@Test
func addTest() {
    @Expect(add(2, 3), 5)
}
```

### 1.2 运行测试

```bash
# cjc 方式
cjc add.cj add_test.cj --test -o add_test
./add_test

# cjpm 方式（推荐）
cjpm test
```

- 测试文件以 `_test.cj` 结尾，`cjpm` 自动识别。
- 普通构建自动排除 `_test.cj` 文件。
- 测试框架 API 无需显式 `import`（自动导入 `std.unittest` 和 `std.unittest.testmacro`）。

---

## 2. 测试组织

### 2.1 测试函数

```cangjie
@Test
func simpleTest() {
    @Expect(1 + 1, 2)
}
```

### 2.2 测试类

```cangjie
@Test
class MathTests {
    @TestCase
    func addTest() {
        @Expect(add(2, 3), 5)
    }

    @TestCase
    func addZero() {
        @Expect(add(2, 0), 2)
    }
}
```

### 2.3 生命周期

仅适用于 `@Test` 类（不适用于 `@Test` 顶层函数）：

| 宏 | 执行时机 |
|----|---------|
| `@BeforeAll` | 所有测试用例之前执行一次 |
| `@BeforeEach` | 每个测试用例之前执行一次 |
| `@AfterEach` | 每个测试用例之后执行一次 |
| `@AfterAll` | 所有测试用例之后执行一次 |

```cangjie
@Test
class FooTest {
    @BeforeAll
    func setup() { /* 初始化共享资源 */ }

    @BeforeEach
    func prepareData(testCaseName: String) { /* 每个用例前准备 */ }

    @AfterEach
    func cleanup() { /* 每个用例后清理 */ }

    @AfterAll
    func teardown() { /* 释放共享资源 */ }

    @TestCase
    func testSomething() { /* ... */ }
}
```

**执行顺序**：`@BeforeAll` → (`@BeforeEach` → `@TestCase` → `@AfterEach`) × N → `@AfterAll`

- `@BeforeEach` / `@AfterEach` 可声明一个 `String` 参数接收测试用例名。
- 同一生命周期步骤有多个函数时，按声明顺序执行。

---

## 3. 断言

### 3.1 基本断言

| 宏 | 行为 | 说明 |
|----|------|------|
| `@Assert(a, b)` | **停止**（fail-fast） | 相等断言，失败则立即抛异常停止 |
| `@Expect(a, b)` | **继续** | 相等断言，失败记录后继续执行 |
| `@Assert(condition)` | 停止 | 布尔断言，等价于 `@Assert(condition, true)` |
| `@Expect(condition)` | 继续 | 布尔断言 |

- 类型要求：`a: A`、`b: B`，则 `A` 需实现 `Equatable<B>`。
- 支持比较运算符：`==`、`!=`、`<`、`>`、`<=`、`>=`。

### 3.2 近似相等断言

```cangjie
@Expect(1.0, 1.001, delta: 0.01)
@Assert(1.0 == 1.001, delta: 0.01)
@Expect(1.0 != 1.9, delta: RelativeDelta(absoluteDelta: 0.001, relativeDelta: 0.02))
```

- 类型需实现 `NearEquatable<CT, D>` 接口。
- 浮点类型内置支持。

### 3.3 异常断言

```cangjie
// fail-fast 版本
@AssertThrows[ExceptionType](expression)
@AssertThrows[TypeA | TypeB](expression)    // 多异常类型

// 继续执行版本
@ExpectThrows[ExceptionType](expression)
@ExpectThrows[ExceptionType]({              // 代码块形式
    foo()
    bar()
})
```

- `@AssertThrows` 返回捕获的异常对象（可进一步检查）。
- `@ExpectThrows` 返回 `Option<ExceptionType>`。
- 无属性参数时默认期望 `Exception`。

### 3.4 失败断言

```cangjie
@Fail("reason")         // 立即失败，抛异常
@FailExpect("reason")   // 记录失败，继续执行
```

### 3.5 PowerAssert

```cangjie
@PowerAssert(a + b == c * d)
```

显示表达式中每个中间值的详细求值结果，便于调试。

### 3.6 自定义断言

```cangjie
@CustomAssertion
func assertPositive(ctx: AssertionCtx, value: Int64) {
    @Assert(value > 0)
}

@Test
func test() {
    @Assert[assertPositive](42)
}
```

---

## 4. 参数化测试

### 4.1 值参数化

```cangjie
@Test[size in [0, 1, 50, 100, 1000]]
func testWithSize() {
    let arr = Array<Int64>(size, { i => i })
    @Expect(arr.size, size)
}
```

### 4.2 多参数组合

```cangjie
@Test[x in [1, 2, 3], y in [10, 20]]
func testCombinations() {
    @Expect(x + y > 0)
}
```

### 4.3 随机参数化

```cangjie
@Test[arr in random()]
func testSort() {
    let sorted = sort(arr)
    // 默认生成 200 个随机测试用例
}
```

- 值偏向边界条件（零值、最大/最小值、空集合）。
- 失败时自动缩减输入并显示 `randomSeed`。
- `@Configure[randomSeed: 42]` 可复现测试。

### 4.4 类型参数化

```cangjie
@Test
@Types[T in <Int32, Int64, Float64>]
func testComparable() where T <: Comparable<T> {
    // 每个类型独立测试
}
```

### 4.5 数据策略 (@Strategy)

```cangjie
@Strategy[len in [0, 1, 5, 10, 100]]
func uniqueArrays(): ArrayList<Int64> {
    let list = ArrayList<Int64>()
    // ... 生成唯一元素的数组
    return list
}

@Test[arr in uniqueArrays()]
func testUnique() {
    // 使用生成的数据
}
```

### 4.6 数据源

| 数据源 | 语法 | 说明 |
|--------|------|------|
| 数组 | `x in [1, 2, 3]` | 固定值列表 |
| 区间 | `x in 0..14` | Range |
| 随机 | `x in random()` | 随机生成 |
| JSON 文件 | `x in json("file.json")` | 从 JSON 加载 |
| CSV 文件 | `x in csv("file.csv")` | 从 CSV 加载 |
| 策略函数 | `x in strategyFunc()` | @Strategy 函数 |

---

## 5. 测试配置

### 5.1 @Configure 宏

```cangjie
@Test
@Configure[randomSeed: 42, generationSteps: 500]
class MyTests {
    @TestCase
    func test() { /* ... */ }
}
```

**通用参数**：

| 参数 | 类型 | 说明 |
|------|------|------|
| `randomSeed` | `Int64` | 随机种子 |
| `generationSteps` | `Int64` | 参数化生成最大步数（默认 200） |
| `reductionSteps` | `Int64` | 参数化缩减最大步数（默认 200） |

### 5.2 命令行参数

| 参数 | 说明 |
|------|------|
| `--filter=pattern` | 过滤测试：`*.*Test`、`MyTest*.*`、`-*.*skip` |
| `--dry-run` | 仅列出测试用例不执行 |
| `--include-tags=tag1,tag2` | 按标签包含（逗号=或，加号=与） |
| `--exclude-tags=tag1` | 按标签排除（优先级高于 include） |
| `--timeout-each=30s` | 单个测试超时 |
| `--parallel[=N]` | 并行执行测试 |
| `--bench` | 仅运行基准测试 |
| `--report-path=dir` | 报告输出目录 |
| `--report-format=xml` | 报告格式（单元测试默认 xml） |
| `--capture-output` | 捕获测试输出（cjpm 默认开启） |
| `--no-capture-output` | 禁用输出捕获 |
| `--show-all-output` | 报告中显示所有输出（含通过用例） |
| `--show-tags` | 报告中显示标签信息 |
| `--coverage-guided` | 启用覆盖率引导随机测试 |
| `--no-progress` | 禁用进度报告 |

### 5.3 标签过滤

```cangjie
@Test
@Tag[Smoke, API]
class SmokeTests {
    @TestCase
    @Tag[Critical]
    func criticalTest() { /* ... */ }
}
```

```bash
cjpm test --include-tags=Smoke+Critical   # 同时有 Smoke 和 Critical
cjpm test --exclude-tags=Slow             # 排除 Slow
```

### 5.4 跳过与超时

```cangjie
@Test
@Skip                                 // 跳过此测试
class SkippedTest { /* ... */ }

@Test
@Timeout[Duration.second * 30]        // 30 秒超时
func longRunningTest() { /* ... */ }
```

### 5.5 并行执行

```cangjie
@Test
@Parallel                             // 标记可并行
class IndependentTests { /* ... */ }
```

```bash
cjpm test --parallel                   # 并行执行，进程数=CPU核心数
cjpm test --parallel=4                 # 指定4个并行进程
```

- 不同测试类在独立进程中运行。
- 测试类须相互独立，无共享可变状态。
- 不可与 `--bench` 同时使用。

---

## 6. 测试模板

```cangjie
@TestTemplate
abstract class CollectionTestTemplate {
    prop collection: Collection<Int64>

    @TestCase
    func testIsEmpty() {
        @Expect(collection.isEmpty())
    }

    @TestCase
    func testSize() {
        @Expect(collection.size, 0)
    }
}

@Test
class ArrayListTest <: CollectionTestTemplate {
    public prop collection: Collection<Int64> = ArrayList<Int64>()
}

@Test
class HashSetTest <: CollectionTestTemplate {
    public prop collection: Collection<Int64> = HashSet<Int64>()
}
```

- 子类自动继承所有 `@TestCase`。
- 生命周期方法也被继承（`@BeforeAll` 基类 → 子类，`@AfterAll` 子类 → 基类）。
- 不可与 `@Parallel`、`@Types` 同时使用。

---

## 7. 动态测试

```cangjie
@TestBuilder
func buildDynamicTests(): TestSuite {
    let builder = TestSuite.builder("DynamicTests")
    builder.add(UnitTestCase.create("test1") {
        @Expect(1 + 1, 2)
    })
    builder.add(UnitTestCase.createParameterized("paramTest", [1, 2, 3]) { value =>
        @Expect(value > 0)
    })
    builder.build()
}
```

---

## 8. Mock 框架

### 8.1 导入

Mock 框架 API 在 `std.unittest.mock` 和 `std.unittest.mock.mockmacro` 中。使用 `cjpm test` 自动启用。

### 8.2 创建 Mock/Spy

```cangjie
let mockRepo = mock<Repository>()        // 骨架 Mock（默认无操作）
let spyRepo = spy<Repository>(realRepo)   // 包装真实对象的 Spy
```

**可 Mock 类型**：类（含 final/sealed）、接口。
**不可 Mock**：扩展、foreign 函数、局部声明、构造器、常量、private 声明。

### 8.3 配置行为 (@On)

```cangjie
// 返回指定值
@On(mockRepo.findById(any())).returns(testData)

// 连续返回
@On(mockRepo.getAll()).returnsConsecutively([data1, data2, data3])

// 抛出异常
@On(mockRepo.save(_)).throws(TimeoutException())

// 调用原始方法（Spy）
@On(spyRepo.findById(_)).callsOriginal()

// 属性 setter
@On(mockObj.prop = _).doesNothing()

// 次数控制
@On(mockRepo.findById(any())).returns(data).once()
@On(mockRepo.findById(any())).returns(data).times(3)
@On(mockRepo.findById(any())).returns(data).anyTimes()

// 链式配置
@On(mockRepo.getStatus()).returns("active").times(2).then().returns("inactive").once()
```

### 8.4 参数匹配器

| 匹配器 | 说明 |
|--------|------|
| `any()` 或 `_` | 匹配任意值 |
| `eq(value)` | 结构相等（常量可省略 eq） |
| `same(reference)` | 引用相等 |
| `ofType<T>()` | 类型匹配 |
| `argThat(predicate)` | 自定义谓词 |
| `none()` | 匹配 Option None |
| `captor(listener)` | 捕获参数值 |

### 8.5 Stub 模式

```cangjie
// ReturnsDefaults：未配置的方法返回默认值
let m = mock<Foo>(modes: [ReturnsDefaults()])
// Bool → false, 数值 → 0, String → "", Option → None, 集合 → 空

// SyntheticFields：为可变属性创建合成字段
let m = mock<Foo>(modes: [SyntheticFields()])
```

### 8.6 顶层/静态声明 Mock

```cangjie
// 直接使用 @On，无需创建 mock 对象
@On(TopLevelModule.globalFunction(_)).returns(value)
@On(MyClass.staticMethod(_)).returns(value)
```

### 8.7 验证 (@Called)

```cangjie
// 验证调用发生
Verify.that(@Called(mockRepo.findById(any())))

// 验证调用次数
Verify.that(@Called(mockRepo.save(_)).times(2))
Verify.that(@Called(mockRepo.delete(_)).never())

// 无序验证
Verify.unordered([
    @Called(mockRepo.findById(1)),
    @Called(mockRepo.save(_)).times(2)
])

// 有序验证
Verify.ordered([
    @Called(mockRepo.findById(1)),
    @Called(mockRepo.save(_)),
    @Called(mockRepo.delete(1))
])

// 验证无交互
Verify.noInteractions([mockRepo])

// 清除调用日志
Verify.clearInvocationLog()
```

**验证次数控制**：`once()`、`atLeastOnce()`（默认）、`times(n)`、`times(min!, max!)`、`atLeastTimes(n)`、`never()`

### 8.8 参数捕获

```cangjie
let listener = ValueListener<String>()
@On(mockRepo.save(captor(listener))).returns(true)

mockRepo.save("test_data")

@Expect(listener.lastValue(), "test_data")
@Expect(listener.allValues().size, 1)
```

### 8.9 编译要求

- `cjc` 编译需加 `--mock` 标志。
- `cjpm test` 自动检测并启用。
- 仅接口可从预编译库 Mock。

---

## 9. 基准测试

### 9.1 基本用法

```cangjie
@Test
class PerfTests {
    @Bench
    func benchSort() {
        let arr = Array<Int64>(1000, { i => 1000 - i })
        sort(arr)
    }
}
```

```bash
cjpm bench                             # 运行基准测试
cjpm bench --report-format=html        # HTML 报告（需 Gnuplot）
cjpm bench --report-format=csv         # CSV 报告
```

### 9.2 参数化基准

```cangjie
@Test
class SortBench {
    @Bench[size in [100, 1000, 10000]]
    func benchSort() {
        let arr = Array<Int64>(size, { i => size - i })
        sort(arr)
    }
}
```

### 9.3 基准配置

```cangjie
@Test
@Configure[
    warmup: Duration.second * 2,       // 预热时间
    minDuration: Duration.second * 10, // 最小执行时间
    minBatches: 20,                    // 最小批次数
    explicitGC: ExplicitGcType.Disable // 禁用 GC
]
class BenchTests { /* ... */ }
```

### 9.4 自定义度量

```cangjie
@Bench
@Measure[TimeNow(Nanos), CpuCycles()]
func benchCompute() { /* ... */ }
```

| 度量 | 说明 |
|------|------|
| `TimeNow()` | 实时时间（默认） |
| `TimeNow(Nanos)` / `TimeNow(Micros)` | 指定单位 |
| `CpuCycles()` | CPU 周期（仅 x86） |
| `Perf()` | Linux perf 硬件计数器 |

### 9.5 输入提供器

```cangjie
@Bench[data in GenerateEachInputProvider { => generateData() }]
func benchProcess() {
    process(data)
}
```

| 提供器 | 说明 |
|--------|------|
| `ImmutableInputProvider` | 复用同一数据（默认） |
| `GenerateEachInputProvider` | 每次调用前生成新数据 |
| `BatchSizeOneInputProvider` | 每次生成，批大小=1 |
| `BatchInputProvider` | 缓冲区批量生成 |

### 9.6 结果指标

- **Median**：中位数执行时间
- **Err%**：可靠性指标（< 3% 可靠，> 10% 需排查）
- **Mean**：平均执行时间
- HTML 报告含：核密度估计图、线性回归图、统计表（均值/中位数/标准差/R²/置信区间）

---

## 10. 完整宏参考

### 测试组织宏

| 宏 | 说明 |
|----|------|
| `@Test` | 标记测试函数或测试类 |
| `@TestCase` | 标记测试类中的测试用例 |
| `@TestBuilder` | 动态测试套件构建 |
| `@TestTemplate` | 测试模板（抽象类） |

### 生命周期宏

| 宏 | 说明 |
|----|------|
| `@BeforeAll` | 所有用例前 |
| `@BeforeEach` | 每个用例前 |
| `@AfterEach` | 每个用例后 |
| `@AfterAll` | 所有用例后 |

### 断言宏

| 宏 | 说明 |
|----|------|
| `@Assert(a, b)` / `@Assert(cond)` | 相等/布尔断言（fail-fast） |
| `@Expect(a, b)` / `@Expect(cond)` | 相等/布尔断言（继续执行） |
| `@AssertThrows[Type](expr)` | 异常断言（fail-fast） |
| `@ExpectThrows[Type](expr)` | 异常断言（继续执行） |
| `@Fail(msg)` | 强制失败（fail-fast） |
| `@FailExpect(msg)` | 强制失败（继续执行） |
| `@PowerAssert(expr)` | 详细表达式断言 |
| `@CustomAssertion` | 自定义断言函数 |

### 配置与控制宏

| 宏 | 说明 |
|----|------|
| `@Configure[key: value]` | 测试配置 |
| `@Skip` / `@Skip[condition]` | 跳过测试 |
| `@Timeout[duration]` | 超时设置 |
| `@Parallel` | 并行执行标记 |
| `@Tag[tag1, tag2]` | 标签过滤 |
| `@Types[T in <Type1, Type2>]` | 类型参数化 |

### 参数化与数据宏

| 宏 | 说明 |
|----|------|
| `@Test[x in source]` / `@TestCase[x in source]` | 值参数化 |
| `@Strategy[x in values]` | 数据策略定义 |

### 基准测试宏

| 宏 | 说明 |
|----|------|
| `@Bench` / `@Bench[x in source]` | 基准测试标记 |
| `@Measure[measurements]` | 度量方式指定 |

### Mock 宏

| 宏 | 说明 |
|----|------|
| `@On(stub_signature).operation()` | Mock/Spy 行为配置 |
| `@Called(stub_signature)` | 调用验证 |
