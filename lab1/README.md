# Lab 1 Automatic Speech Recognition

| 姓名 | 学号    |
| ---- | ------- |
| 梁乔 | 1853572 |

## 程序功能介绍

本程序为一个简单的语音识别小程序，可以基本准确的识别用户输入的口令，并能根据口令含义完成以下功能：

1. 播放不同种类的音乐
2. 获得上海的未来几天的实时天气
3. 打开浏览器、记事本等程序

同时，程序能实时显示当前的时间。

## 程序环境

本程序的开发环境为：

python3.9, PyQt5 5.15.6

除此之外也使用了如PocketSpinx语音识别库，pyAudio等库。

## 界面布局设计

​	从GUI来说，本界面为完全重新设计实现，总体思路为标准的三栏布局，参考原型有cmd交互式命令行窗口以及Siri界面。初始界面如下图所示：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/image-20220428232342254.png" alt="image-20220428232342254" style="zoom: 67%;" />

同时，考虑到用户可能会经常拖动窗口，如果采用元素固定位置的形式，则会因为元素排布混乱而严重影响功能和用户体验。因此我的程序也采用了pyqt5的一些布局管理类：

1. `QGridLayout`：网格布局，使元素能在窗口内均匀整齐排布
2. `QBoxLayout`： 盒子布局，包括水平盒子布局和垂直盒子布局。程序内的时间，交互文字的排布就是使用盒子模型实现的。

使用以上布局方案后，就可以实现自适应布局，如下：

**最小窗口**：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/image-20220428232736930.png" alt="image-20220428232736930" style="zoom:50%;" />

**全屏窗口**：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/image-20220428232807826.png" alt="image-20220428232807826" style="zoom:67%;" />

## 界面交互设计

本程序的基本交互方式是**用户语音输入**和**程序文字输出**。

具体的交互流程图如下：

<img src="https://joes-bucket.oss-cn-shanghai.aliyuncs.com/img/%E6%9C%AA%E5%91%BD%E5%90%8D%E6%96%87%E4%BB%B6%20(11).png" alt="未命名文件 (11)" style="zoom: 50%;" />

​	为了提高交互的效果，程序在是实现时并未采取严格的输入文字匹配，而是使用**关键词匹配**的方法，当用户在正确的流程阶段所输入的文字中含有某些关键词时，则判定为该用户想要执行该指令。同时，在任何阶段若没有匹配的指令，程序都会作相应的提示并要求u用户重新输入。

​	程序判断指令的核心代码逻辑如下：

```python
    def getResponse(self,result):
        # 根据识别的信息获取相应的回复
        self.said_text = result
        if result == 'hey bro':
            return BEGIN_REPONSE
        elif 'music' in result:
                return MUSIC_CHOICE
        elif 'weather' in result:
                result = WEATHER_SERVICE
                result += '\n'
                result += self.searchWeather()
                return result
        elif 'stay' in result:
                os.system('stay.mp3')
                return MUSIC_CHOICE+'stay.'
        elif 'beautiful' in result:
                os.system('beautiful.mp3')
                return MUSIC_CHOICE + 'Beautiful(鬼怪OST)'
        elif 'love is gone' in result:
                os.system('love.mp3')
                return MUSIC_CHOICE + 'Love is Gone'
        elif 'software' in result:
            return OPEN_SOFTWARE_SERVICE
        elif 'notepad' in result:
            subprocess.run(["notepad"])
            return OPEN_NOTEPAD
        elif 'browser' in result:
            import webbrowser
            webbrowser.open("http://www.baidu.com")
            return OPEN_WEB_BROWSER
        else:
            return ERROR_RESPONSE
```

对不同的情况分别执行对应的反馈程序。

## 语音识别准确度优化

​	实例程序中调用的API准确率较低，不能很好的完成程序的功能需求。因此本程序换用了更加准确的API。考虑到`PocketSpinx`库本身集合了大量的语音识别API，因此本程序换用了如下的API进行语音识别：

```python
            houdify_id = 'kz90eBQUZiJ8BvfN6BUH9g=='
            houdify_pwd = 'ZnHajlpCtpEs2cpthYNnI_nH_dzmnsRqO4dUrwF-gmKqFZ-MiPkUrTe2Wh_cfzqTyD7RT_dLmqxV1lziDVHb_w=='
            text =  recognizer.recognize_houndify(audio, houdify_id, houdify_pwd)
```

实践证明在环境比较安静的情况下，该API基本能准确识别出用户所说的话。为作证明，可尝试输入以下的话语，程序基本能准确识别：

| 测试语句                                      | 含义                          |
| --------------------------------------------- | ----------------------------- |
| hey bro                                       | 唤醒交互程序                  |
| tell me the weather \| what about the weather | 查看上海天气                  |
| play some music                               | 播放一些音乐                  |
| play the music named beautiful                | 播放一首名为'beautiful'的音乐 |
| help me open some softwares                   | 指定程序打开软件              |
| open the browser                              | 打开默认浏览器                |

以上语句经过测试识别率达到70%以上。



