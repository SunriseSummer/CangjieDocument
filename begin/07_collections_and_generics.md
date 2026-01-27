# 07. 集合与泛型：音乐播放器列表

我们都用过音乐 App。如何管理成千上万首歌？如何让我们的播放列表既能存“流行歌”，又能存“古典乐”，甚至将来存“播客”？集合与泛型是关键。

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

我们需要快速查找某个歌手的所有专辑。`HashMap` 是最佳选择。

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

用户的“我喜欢的音乐”列表是随时变化的，使用 `ArrayList` 可以高效增删。

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
