# 简介

***

优雅的列表爬虫。

本库是专门用于爬取或操作列表式网页的页面类，基于 DrissionPage。  
页面类抽象了列表式页面基本特征，封装了常用方法。
只需少量设置即可进行爬取或页面操作，实现可复用、可扩展。  
广泛适用于各种网站的列表页面。  

示例：https://gitee.com/g1879/DrissionPage-demos

DrissionPage库：https://gitee.com/g1879/DrissionPage

联系邮箱：g1879@qq.com

# 背景及特性
**背景**

大量的数据用列表页方式存放在网站中，这些列表页有相同的特征，用相同的方法爬取。  
爬取网站时经常重复编写相同的代码，做重复的劳动。  
因此本库把列表页共有的特征提取出来，封装成类，实现可复用。减轻开发的工作量。

**特性**

- 配置简单，上手容易
- 封装常用列表页属性及方法，实现可复用
- 不同类型页面使用相同的操作方式，使用方便
- 可根据特殊情况扩展，实用性强
- 支持 requests 和 selenium 方式，并支持无缝切换

**原理**

所有列表页都有共同的特征：**数据行**、**行中的数据列**。能通过 **翻页按钮 ** 或 **滚动页面** 方式翻页。

只要获取到这几个元素的定位方式，就能封装一个方法实现 **读取 -> 翻页（滚动） -> 读取** 的循环操作，直到没有下一页或到达指定页数。

本库支持 xpath 或 css selector 路径，针对不同页面把必要元素路径传递给页面对象，即可实现一行爬取全部页的功能。

# 简单演示

***

一段简单的代码，演示爬取码云推荐项目列表（全部页）。

```python
from ListPage import ListPageS, Targets, Xpaths

# 定义页面结构
xpaths = Xpaths()
xpaths.pages_count = '//a[@class="icon item"]/preceding-sibling::a[1]'  # 总页数
xpaths.rows = '//div[@class="project-title"]'  # 行
xpaths.set_col('项目', './/h3/a')  # 列1
xpaths.set_col('星数', './/div[@class="stars-count"]')  # 列2

# 定义目标
targets = Targets(xpaths)
targets.add_target('项目')
targets.add_target('项目', 'href')
targets.add_target('星数')

# 列表第一页
url = 'https://gitee.com/explore/weixin-app?page=1'

p = ListPageS(xpaths, url)
p.num_param = 'page'  # url中页面的参数

# 爬取全部页
p.get_list(targets)
```

输出：

```
第1页
https://gitee.com/explore/all
['guanguans/soar-php', 'https://gitee.com/guanguans/soar-php', '6']
...第1页省略部分...
['drinkjava2/jBeanBox', 'https://gitee.com/drinkjava2/jBeanBox', '61']

第2页
https://gitee.com/explore/all?page=2
['pai01234/tokencore', 'https://gitee.com/pai01234/tokencore', '22']
...第2页省略部分...
['docsifyjs/docsify', 'https://gitee.com/docsifyjs/docsify', '47']

...省略下面98页...
```


# 使用方法

***

## 安装及导入

**安装**

```
pip install ListPage
```

**导入**

```python
# 翻页式列表页
from ListPage import ListPage, Paths, Targets

# 滚动式列表页
from ScrollingPage import ScrollingPage, Paths, Targets
```



## 初始化

如只使用 requests 方式爬取，或已在系统变量加入 chrome.exe 和 chromedriver.exe 的路径，可跳过本节。

ListPage 是基于 DrissionPage 实现的，初始化的方法与 DrissionPage 一致，请查看 [DrissionPage 初始化方法]()。



## 定位符

> 了解用法前先了解定位符概念，这个概念是进阶用法，如须快速上手可暂时跳过本节。

有些数据不是储存在元素的文本，而是在元素某个属性中，还可能不是整个字段，而是字段的一部分。因此本库设定了一个定位符格式，用于提取这样的数据。

定位符在定义页面总页数、设置目标时会用到。

示例

```html
<img alt="金刚川" class="board-img" src="https://p1.meituan.net/moviemachine/5cbf9a626b7ed27c96ca3c748655b3ec2550103.jpg@160w_220h_1e_1c">
```

例如猫眼电影榜单中的图片，我们想下载这张图片，就要获取 src 属性，而且要去掉后面 @160w_220h_1e_1c 部分。这个数据的定位符可以这样写：

```python
('封面', 'data-src', r'(.*)@')
```

定位符由3部分组成

1. 第一部分是元素定位语句，这里的 '封面' 是因为在 paths 已定义 '封面' 的定位语句
2. 第二部分是元素的属性名，可省略，省略时默认为 text
3. 第三部分是从元素属性提取内容的正则表达式，可省略，省略时默匹配整个字段

注意，如有第三部分，则第二部分的 'text' 不可省略。

综上所述，定位符有以下形式：

```python
'作者'  # 单个字符串，即('作者', 'text', '(.*)')
('作者')  # 和上一行相同，省略二三部分
('链接', 'href')  # 省略第三部分，即('链接', 'href', '(.*)')
('封面', 'data-src', r'(.*)@')  # 三部分都写全
```



## Paths 类

Paths 类用于管理关键元素的路径信息。ListPage 创建时须接收记录了页面元素路径的 Paths 对象或字典，用于解析页面。

路径用 xpath 和 css selector 都可以，但一个 Paths 对象保存的路径必须是同一种类的。

**创建 Paths 对象：**

``` python
paths = Paths('css')  # 创建类型为css selector的Paths对象
paths = Paths(paths_dict=paths_dict)  # 通过字典创建，字典格式见下文
```

**Paths 类属性：**

```python
# 路径的类型
paths.type

# 共有的关键元素
paths.rows  # 列表行元素的定位路径，必须
paths.cols  # 行元素中列元素的定位路径，字典格式，必须
paths.next_btn  # 下一页或加载更多按钮元素路径，按页面情况使用，非必须

# 翻页式列表页独有属性
paths.page_count  # 总页数所在元素路径，可指定元素属性及提取正则表达式，按页面情况使用，非必须

# 滚动式列表页独有属性
paths.container  # 列表容器，必须
```

**Paths 类方法：**

```python
# 获取某列的路径
paths.get_col(col_name)

# 设置一列路径
paths.set_col(cols_data)

# 设置多列路径
paths.set_col({'col1': 'path1', 'col2': 'path2', ...})  # 用字典设置列
paths.set_col(('col', 'path'))  # 通过一维列表或元组设置列
paths.set_col((('col1', 'path11'), ('col2', 'path2'), ...))  # 通过二维列表或元组设置列

# 从字典读取全部路径设置
paths.from_dict(paths_dict)

# 以字典形式输出保存的路径
paths.as_dict()
```

**通过字典创建**

```python
paths_dict = {
    # 路径的类型，只能是'css'或'xpath'，非必须
    'type': 'css',
    
    # 行元素路径，必须 
    'rows': 'xpath 或 css selector',
    
    # 列元素相对于行元素的路径，必须
    'cols': {
        'col1': 'xpath 或 css selector',
        'col2': 'xpath 或 css selector',
        ...
    }
    
    # 翻页式页面总页数获取定位符，格式见上一节，非必须
    'page_count': 定位符,  
    
    # 下一页（翻页式）或加载更多（滚动式）按钮元素路径，非必须
    'next_btn': 'xpath 或 css selector',
    
    # 行元素所在容器路径，滚动式页面专用，使用滚动式页面时必须
    'container': 'xpath 或 css selector',
}

paths = Paths(paths_dict=paths_dict)
```

**Tips：** 

- ListPage 不是必须接收 Paths 对象，接收格式正确的字典也是可以的。
- 如果不指定 type，程序会尝试从字符串中判断类型
- 滚动式页面的列路径是相对于 container 的路径的



### Xpath 类和 CssPaths 类

Xpaths 类和 CssPaths 类是 Paths 类的子类，用法与 Paths 类一致，但不能通过 paths.type 改变类型。



## Targets 类

Targets 类用于定义爬取目标。  

Targets 对象接收一个 Paths 对象或定义路径的字典，针对列来定义爬取目标。  
每个目标要有一个唯一的名字，内容由一个定位符表示：(列名, [属性名, 正则表达式])  。定位符用法见上文。

示例：
```python
targets.add_targets('项目名', '项目')  # 前一个是目标名称，后一个是列名
targets.add_targets('链接', '项目', 'href')  # 在'项目'列获取href属性定义为链接目标
targets.add_targets('序号', '序号', 'text', '(//d+)')  # 在'序号'列获取数字定义为序号目标
```

**创建 Targets 对象：**

```python
targets = Targets(paths)  # 创建时要接收一个Paths对象或路径字典，创建这个值后不能修改
targets = Targets(paths, targets_dict)  # 创建时同时接收目标字典，直接创建目标
```

**Targets 类属性：**

```python
targets.paths  # 页面路径管理 Paths 对象
targets.start_stop_row  # 设置爬取列表起止行号
targets.targets  # 返回所有目标组成的字典
```

**Tips：** 有些列表表头表尾不容易通过定位语句和内容区分，因此可设置爬取范围，忽略表头表尾

**Targets 类方法：**

```python
targets.set_targets(targets_dict)  # 通过传入字典批量设置目标
targets.add_target(name, col, attr, re_str)  # 增加单个目标
```

Targets 对象中的目标是针对其保存的 Paths 对象的列设置的。

**通过字典创建**

```python
targets_dict = {
    'start_stop': (1, -1),  # 爬取第2到倒数第2行，与切片规则一样，非必须
    '目标1': '列1',
    '目标2': ('列2', 'href'),
    '目标3': ('列3', 'data-src', '(.*)@')
    ...
}

targets = Targets(targets_dict)
```

**start_stop规则**

与切片规则一致，0 为第一个，-1 为最后一个，包含前面的数字，不包含后面的数字。第二个数字可省略，如省略，则爬到最后一行。

示例：

```python
(0, 5)  # 爬取第1行到第4行
(2, -2)  # 爬取第3行到倒数第3行
(1,)  # 爬取第2行到最后一行
(1, None)  # 爬取第2行到最后一行
```

**Tips：** ListPage 不是必须接收 Targets 对象，接收格式正确的字典也是可以的。



## ListPage 类

ListPage 类是翻页式列表页基本类，继承自 DrissionPage 的 MixPage 类。  
专门用于处理翻页式列表页面。如商城产品页、文章列表页。   
它有两种模式，s 模式使用 requests 处理页面，d 模式使用 selenium。  
s 模式效率高，适用于非 js 加载页面数据爬取。  
d 模式可处理 js 加载的页面，可用于自动化操作。  
这两种模式可以互相切换，但要一般没有必要。

**创建 ListPage 对象：**

```python
page = ListPage(paths, index_url, mode, timeout, drission)
'''参数说明
paths: Paths对象或路径字典
index_url: 列表第一页url
mode: 's'使用requests，'d'使用selenium
timeout: s模式时为连接等待时间，d模式时为查找元素等待时间
drission: 驱动器对象，可忽略，详见DrissionPage库
'''
```

**ListPage 属性：**

```python
page.paths  # 页面元素管理对象
page.pages_count  # 总页数
page.current_page_num  # 当前页码
page.num_param  # url中的页码参数
page.step  # 页码步长，配合num_param属性使用
page.first_num  # 第一个页码是0还是1，配合num_param属性使用
```

**ListPage 方法：**

```python
page.to_first_page()  # 跳转到第一页
page.to_next_page(wait)  # 跳转到下一页，然后等待若干秒
page.to_page(num, wait)  # 跳转到任意页，然后等待若干秒
page.get_current_rows()  # 获取当前行元素
page.get_current_list(targets)  # 根据targets中定义的目标获取结果列表
page.get_list(targets, begin, count, stop_when_empty, wait, show_msg, recorder, return_data)
'''参数说明
targets: Targets对象或目标字典
begin: 起始页码
count: 爬取页数
stop_when_empty: 遇到空页是否停止，一般应对无法获取总页数时使用
wait: 翻页后等待秒数
show_msg: 是否实时打印爬取到的信息
recorder: 记录器对象，详见下文
return_data: 是否返回结果，如设置了记录器，不返回结果可以节省内存
'''
```

**Tips:**

- get_list() 是爬取列表页的核心方法
- 用 get_current_rows() 获取到行元素对象可用于自动化操作

**返回的格式**

爬取结果以列表形式呈现，每行数据为一个字典。

```python
[
    {'目标1': '结果1', '目标2': '结果2', ...},
    {'目标1': '结果1', '目标2': '结果2', ...},
    ...
]
```



### 不同列表页的应对方法

总的来说，爬取列表页的思路是：  
**获取总页数** > **爬取一页数据** > **点击下一页按钮或访问下一页链接** > **循环直到最后一页或指定页**

但列表页有多种形态，不一定都提供需要的元素，本库提供灵活的配置，可适应绝大多数列表页的处理。

- **url 带页码信息的列表页**

这种列表页 url 中带页码参数或把路径写在页码中，将其提取出来可大大提高定位页面的效率。

示例：

```
https://gitee.com/explore/all?page=1
https://sz.lianjia.com/ershoufang/pg1/
https://www.procell.com.cn/filters-type-3-p-1.html
https://maoyan.com/board/6?offset=10
```

针对这种页面，可设置 ListPage对象的 num_param 属性。这种方法只适用于页码是有规律数字的情况。  
注意，使用 num_param 时，页面对象的 index_url 属性里也必须包含页码参数。

以上页面的 num_param 设置方法：

```python
# https://gitee.com/explore/all?page=1
page.num_param = 'page'

# https://sz.lianjia.com/ershoufang/pg1/
page.num_param = '/pg'

# https://www.procell.com.cn/filters-type-3-p-1.html
page.num_param = '/filters-type-3-p-'

# https://maoyan.com/board/6?offset=0
page.num_param = 'offset'
page.step = 10
page.first_num = 0
```

可以看出，当页码为 url 后续参数时，直接设置参数名；当是路径一部分时，加上 '/'，程序会匹配后续的数字。

注意以上最后一种情况，页码步长为 10，并且以 0 为第一页，因此需要设置 step 和 first_num 两个属性。

设置 num_param 属性后，无须定义下一页按钮的路径即可进行爬取、翻页等操作，程序会用替换数字的方式产生任意页的 url。

- **无法获取总页数的页面**

针对这种页面可指定 pages_count 属性，或在爬取时设置爬取页数。  
如两者都不设置，在爬全部页时，程序直到空页或没有下一页按钮时就会停下。

```python
page.pages_count = 100  # 手动设置总页数
page.get_list(targets, count=100)  # 在爬取时指定爬取页数
```

- **JS 加载的列表页**

这种列表页使用 ajax 获取列表内容，url 不会变化，适合用 d 模式进行爬取。  
d 模式使用 selenium 模拟操作网页，反复点击下一页按钮即可实现翻页。

```python
page = ListPage(xpaths, index_url, 'd')  # 用d模式创建列表页对象
```

- **模式切换**

ListPage 继承自 MixPage，因此也支持 s 模式和 d 模式之间的切换，以及 MixPage 一切功能。

```python
page.change_mod()  # 切换模式
```

MixPage 详情请查看 [DrissionPage 库](https://gitee.com/g1879/DrissionPage)



## ScrollingPage 类

ScrollingPage 类是滚动加载式列表页基本类，继承自 DrissionPage 的 MixPage 类。  
专门用于处理滚动加载式列表页面。如新闻列表页。  
封装了对页面的基本读取和操作方法，只能在 MixPage 的 d 模式下工作。  

**创建 ScrollingPage 类对象**

```python
page = ScrollingPage(paths, index_url, timeout, drission)
```

参数含义与 ListPage 相同，不再赘述。

**ScrollingPage 属性**

```python
page.paths  # 页面元素管理对象
```

**ScrollingPage 方法**

```python
page.to_first_page()  # 重新访问页面，回到首页
page.get_current_rows()  # 获取当前行对象
page.get_current_list(targets, show_msg)  # 根据Targets定义，获取当前页面数据
page.to_next_page(wait)  # 下拉，加载新内容
page.get_new_rows()  # 获取新加载的行对象
page.get_new_list(targets, show_msg)  # 根据Targets定义，获取新加载的数据
page.click_more_btn(wait)  # 点击加载更多按钮（如有定义）
page.get_list(targets, scroll_times, wait, show_msg, recorder, return_data)
'''参数说明
targets: Targets对象或目标字典
scroll_times: 滚动次数
wait: 滚动后等待秒数
show_msg: 是否实时打印爬取到的信息
recorder: 记录器对象，详见下文
return_data: 是否返回结果，如设置了记录器，不返回结果可以节省内存
'''
```

因为无法得知滚动页面的长度，所以滚动页面爬取内容时必须指定滚动次数。

其余用法与 ListPage 类似。



## Recorder 类

Recorder对象用于暂缓写入数据，它可接收列表数据，达到一定数量时才一次进行写入，以降低文件读写次数，减少开销。可支持 .csv、.txt、.xlsx、.json 四种格式文件。

**创建 Recorder 对象**

```python
recorder = Recorder(file_path, cache_size)
```

**Recorder 属性**

```python
recorder.cache_size  # 缓存大小
recorder.file_path  # 文件路径
```

**Recorder 方法**

```python
recorder.add_data(data)  # 添加一批数据，列表或元组格式
recorder.record()  # 将缓存记录到文件然后清空
recorder.set_head(head)  # 设置表头，csv和xlsx格式适用
recorder.set_before(before_col)  # 设置数据前的列，列表、元组或字典格式
recorder.set_after(after_col)  # 设置数据后的列，列表、元组或字典格式
recorder.clear()  # 清空缓存
```

**Tips:** 

- set_before() 和 set_after() 用于添加不是在页面中获取到的数据，通常用于区分多批写入数据，如多次爬取的标识等。示例：爬二手房时各区数据都记录在一个表，就要在爬取到的数据前加一个区列。详见下文示例。
- csv 和 xlsx 写入时会按照结果字典创建表头，如set_before() 和 set_after() 参数也是字典，也可自动写入表头，一般无须 set_head()。

# 实用案例

- [爬取政府采购网搜索结果](https://gitee.com/g1879/ListPage/blob/master/demos/%E6%94%BF%E5%BA%9C%E9%87%87%E8%B4%AD%E7%BD%91.py)
- [爬取爬东方财富网业绩报表](https://gitee.com/g1879/ListPage/blob/master/demos/%E7%88%AC%E4%B8%9C%E6%96%B9%E8%B4%A2%E5%AF%8C%E7%BD%91%E4%B8%9A%E7%BB%A9%E6%8A%A5%E8%A1%A8.py)
- [爬取链家二手房信息](https://gitee.com/g1879/ListPage/blob/master/demos/%E7%88%AC%E9%93%BE%E5%AE%B62.py)
- [爬取百度学术搜索结果](https://gitee.com/g1879/ListPage/blob/master/demos/%E7%99%BE%E5%BA%A6%E5%AD%A6%E6%9C%AF%E6%90%9C%E7%B4%A2%E7%BB%93%E6%9E%9C.py)
- [爬取码云推荐项目列表](https://gitee.com/g1879/ListPage/blob/master/demos/%E7%A0%81%E4%BA%91%E9%A1%B9%E7%9B%AE%E5%88%97%E8%A1%A8.py)

# APIs

***

请在 wiki 中查看：[APIs](https://gitee.com/g1879/ListPage/wikis/ListPage?sort_id=3260220)