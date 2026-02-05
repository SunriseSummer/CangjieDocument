# 07. 集合与泛型：音乐播放器列表

我们都用过音乐 App。播放列表既要保存歌曲，也要支持播客、专辑等不同内容。要做到“同一结构、不同类型”，集合与泛型是关键。

## 本章目标

*   理解泛型在“复用数据结构”中的意义。
*   熟悉数组、哈希表与列表等常用集合的使用场景。
*   形成“选择合适容器”的工程意识。

## 1. 泛型播放列表 (Generics)

我们不想为每种音频类型都写一个列表类。我们可以定义一个“万能盒子”。

```cangjie
// T 代表某种类型，由使用者决定
class Playlist<T> {
    var items: Array<T>
    var name: String

    public init(name: String) {
        this.name = name
        this.items = [] // 初始化空
    }

    public func add(item: T) {
        // 简易扩容逻辑演示
        let newItems = Array<T>(items.size + 1) { i =>
            if (i < items.size) items[i] else item
        }
        items = newItems
        println("添加到 [${name}]: 1 首新曲目")
    }
}

struct Song {
    let title: String
    let artist: String
}

main() {
    // 创建一个“歌曲”播放列表
    let popList = Playlist<Song>("流行金曲")
    popList.add(Song("稻香", "周杰伦"))

    // 创建一个“字符串”列表 (模拟文件名)
    let fileList = Playlist<String>("本地文件")
    fileList.add("audio_001.mp3")
}
```

## 2. 歌手与专辑库 (HashMap)

我们需要快速查找某个歌手的所有专辑或销量。`HashMap` 是最佳选择。

```cangjie
import std.collection.*

main() {
    // 键(Key)是歌手名，值(Value)是专辑销量
    let salesData = HashMap<String, Int64>()

    salesData["Adele"] = 30000000
    salesData["Taylor Swift"] = 50000000

    // 粉丝查询
    let query = "Adele"
    if (salesData.contains(query)) {
        println("${query} 的销量: ${salesData[query]}")
    } else {
        println("未找到该歌手数据。")
    }

    // 遍历排行榜
    println("\n=== 销量榜单 ===")
    for ((artist, sales) in salesData) {
        println("${artist}: ${sales}")
    }
}
```

## 3. 动态歌单 (ArrayList)

用户的“我喜欢的音乐”列表是随时变化的，使用 `ArrayList` 可以高效增删，同时保持顺序。

```cangjie
import std.collection.*

main() {
    let myFavorites = ArrayList<String>()

    myFavorites.append("Hotel California")
    myFavorites.append("Yesterday")

    println("当前收藏数: ${myFavorites.size}")

    // 移除非最爱
    myFavorites.remove(1) // 移除第二个

    for (song in myFavorites) {
        println("正在播放: " + song)
    }
}
```

## 工程化提示

*   集合类型的性能差异明显：查找频繁用 `HashMap`，顺序遍历用数组。
*   示例中的集合 API 为演示用途，实际项目以标准库实现为准。
*   为集合设置清晰的容量预估，能减少扩容成本。

## 小试身手

1. 为 `Playlist` 增加 `remove` 与 `listAll` 方法。
2. 用 `HashMap` 记录歌曲播放次数，并输出 Top 3。
