---
name: cangjie-appendix
description: "仓颉语言附录参考。当需要查阅仓颉语言的关键字列表、运算符优先级与结合性、运算符重载函数签名、运行时环境变量配置、包兼容性规则、TokenKind枚举类型时，应使用此 Skill。"
---

# 仓颉语言附录参考 Skill

## 1. 仓颉语言关键字

`as`、`abstract`、`break`、`Bool`、`case`、`catch`、`class`、`const`、`continue`、`Rune`、`do`、`else`、`enum`、`extend`、`for`、`func`、`false`、`finally`、`foreign`、`Float16`、`Float32`、`Float64`、`if`、`in`、`is`、`init`、`import`、`interface`、`Int8`、`Int16`、`Int32`、`Int64`、`IntNative`、`let`、`mut`、`main`、`macro`、`match`、`Nothing`、`open`、`operator`、`override`、`prop`、`public`、`package`、`private`、`protected`、`quote`、`redef`、`return`、`spawn`、`super`、`static`、`struct`、`synchronized`、`try`、`this`、`true`、`type`、`throw`、`This`、`unsafe`、`Unit`、`UInt8`、`UInt16`、`UInt32`、`UInt64`、`UIntNative`、`var`、`VArray`、`where`、`while`

---

## 2. 运算符优先级与结合性

共 **19 个优先级级别**（0 = 最高）

| 优先级 | 运算符 | 说明 | 结合性 |
|--------|--------|------|--------|
| 0 | `@` | 宏调用 | 右 |
| 1 | `.`、`[]`、`()` | 成员访问、索引、函数调用 | 左 |
| 2 | `++`、`--`、`?` | 自增、自减、可选链 | 无 |
| 3 | `!`、`-`（一元） | 取反、取负 | 右 |
| 4 | `**` | 幂运算 | 右 |
| 5 | `*`、`/`、`%` | 乘、除、取模 | 左 |
| 6 | `+`、`-` | 加、减 | 左 |
| 7 | `<<`、`>>` | 位移 | 左 |
| 8 | `..`、`..=` | 半开区间、闭区间 | 无 |
| 9 | `<`、`<=`、`>`、`>=`、`is`、`as` | 比较、类型检查、类型转换 | 无 |
| 10 | `==`、`!=` | 相等、不等 | 无 |
| 11 | `&` | 按位与 | 左 |
| 12 | `^` | 按位异或 | 左 |
| 13 | `\|` | 按位或 | 左 |
| 14 | `&&` | 逻辑与 | 左 |
| 15 | `\|\|` | 逻辑或 | 左 |
| 16 | `??` | 空合并 | 右 |
| 17 | `\|>`、`~>` | 管道、组合 | 左 |
| 18 | `=` 及所有复合赋值 | 赋值 | 无 |

---

## 3. 运算符重载函数签名

| 运算符 | 签名 | 用法 |
|--------|------|------|
| `[]`（取值） | `operator func [](index: T): R` | `this[index]` |
| `[]`（赋值） | `operator func [](index: T, value!: V): Unit` | `this[index] = value` |
| `()` | `operator func ()(params): R` | `this(params)` |
| `!` | `operator func !(): R` | `!this` |
| `-`（一元） | `operator func -(): R` | `-this` |
| `**` | `operator func **(other: T): R` | `this ** other` |
| `*`、`/`、`%` | `operator func *(other: T): R` 等 | 二元算术 |
| `+`、`-` | `operator func +(other: T): R` 等 | 加减 |
| `<<`、`>>` | `operator func <<(other: T): R` 等 | 位移 |
| `<`、`<=`、`>`、`>=` | `operator func <(other: T): R` 等 | 比较 |
| `==`、`!=` | `operator func ==(other: T): R` 等 | 相等 |
| `&`、`^`、`\|` | `operator func &(other: T): R` 等 | 位运算 |

---

## 4. 运行时环境变量

### 堆与内存配置
| 变量 | 说明 | 默认值 |
|------|------|--------|
| `cjHeapSize` | 最大堆大小 | 256MB |
| `cjRegionSize` | 区域分配器线程本地缓冲区 | 64KB |
| `cjHeapUtilization` | 堆利用率 | 0.8 |
| `cjGCInterval` | GC 最小间隔 | 150ms |
| `cjBackupGCInterval` | 备份 GC 触发间隔 | 240s |

### 线程配置
| 变量 | 说明 | 默认值 |
|------|------|--------|
| `cjProcessorNum` | 最大仓颉线程并发数 | CPU 核数 |
| `cjStackSize` | 线程栈大小 | 128KB |

### 日志配置
| 变量 | 说明 | 默认值 |
|------|------|--------|
| `MRT_LOG_LEVEL` | 最低日志级别 | e（ERROR） |
| `MRT_LOG_PATH` | 日志输出路径 | stdout/stderr |
| `cjHeapDumpOnOOM` | OOM 时堆转储 | off |

---

## 5. 包兼容性规则

- 运行时版本 `a.b.c` 与包版本 `x.y.z`：
  - 当 `a` 和 `x` 均为 0 时：三个分量须完全匹配
  - 当均为非 0 时：仅主版本号须匹配
- **核心包不兼容**：运行时立即终止
- **非核心包不兼容**：抛出 `IncompatiblePackageException`

---

## 6. TokenKind 枚举类型

`TokenKind` 枚举定义了仓颉语言的所有词法 token 类型，包括：
- **标点/分隔符**：`DOT`、`COMMA`、`LPAREN`、`RPAREN`、`LSQUARE`、`RSQUARE`、`LCURL`、`RCURL`、`COLON`、`SEMI` 等
- **算术运算符**：`ADD`、`SUB`、`MUL`、`DIV`、`MOD`、`EXP`、`INCR`、`DECR`
- **逻辑运算符**：`AND`、`OR`、`NOT`
- **位运算符**：`BITAND`、`BITOR`、`BITXOR`、`LSHIFT`、`RSHIFT`
- **比较运算符**：`LT`、`GT`、`LE`、`GE`、`EQUAL`、`NOTEQ`、`IS`、`AS`
- **赋值运算符**：`ASSIGN` 及所有复合赋值
- **特殊运算符**：`COALESCING`、`PIPELINE`、`COMPOSITION`、`QUEST`、`RANGEOP`、`CLOSEDRANGEOP`、`ARROW`、`DOUBLE_ARROW` 等
- **类型关键字**：`INT8`~`INT64`、`UINT8`~`UINT64`、`FLOAT16`~`FLOAT64`、`BOOLEAN`、`RUNE`、`NOTHING`、`UNIT` 等
- **声明/控制流/修饰符关键字**：对应语言的所有关键字
- **字面量**：`IDENTIFIER`、`INTEGER_LITERAL`、`FLOAT_LITERAL`、`STRING_LITERAL`、`BOOL_LITERAL` 等

---

