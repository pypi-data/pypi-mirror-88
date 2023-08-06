# 简介

***

本库是专门用于爬取或操作列表式网页的页面类，基于 DrissionPage。  
页面类抽象了列表式页面基本特征，封装了常用方法。
只需少量设置即可进行爬取或页面操作，实现可复用、可扩展。  
广泛适用于各种网站的列表页面。  

示例：https://gitee.com/g1879/DrissionPage-demos

DrissionPage库：https://gitee.com/g1879/DrissionPage

联系邮箱：g1879@qq.com

# 背景及特性
***

## 背景

大量的数据用列表页方式存放在网站中，这些列表页有相同的特征，用相同的方法爬取。  
爬取网站时经常重复编写相同的代码，做重复的劳动。  
因此本库把列表页共有的特征提取出来，封装成类，实现可复用。减轻开发的工作量。

## 特性

- 配置简单，上手容易
- 封装常用列表页属性及方法，实现可复用
- 不同类型页面使用相同的操作方式，使用方便
- 可根据特殊情况扩展，实用性强

# 原理

***

所有列表页都有共同的特征：**数据行**、**行中的数据列**。有些列表还能获取到**翻页按钮**和**总页数**。

只要获取到前三者的定位方式，就能封装一个方法实现 **读取 -> 翻页 -> 读取** 的循环操作，直到没有下一页或到达指定页数。

本库采用 xpath 定位方式，针对不同页面，只要获取到这三个元素的 xpath 路径，传递给页面对象，即可实现一行爬取全部页的功能。

# 演示

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
p.num_param = 'page'

# 爬取全部页
p.get_list(targets)
```

输出：

```
第1页
https://gitee.com/explore/all
['guanguans/soar-php', 'https://gitee.com/guanguans/soar-php', '6']
...省略第1页...
['drinkjava2/jBeanBox', 'https://gitee.com/drinkjava2/jBeanBox', '61']

第2页
https://gitee.com/explore/all?page=2
['pai01234/tokencore', 'https://gitee.com/pai01234/tokencore', '22']
...省略第2页...
['docsifyjs/docsify', 'https://gitee.com/docsifyjs/docsify', '47']

...省略下面98页...
```


# 安装

***

```
pip install ListPage
```


# 翻页式列表页

***

## 基类ListPage

ListPage 类是翻页式列表页基类，继承自 DrissionPage 的 MixPage 类。  
专门用于处理翻页式列表页面。如商城产品页、文章列表页。  

**注意：不要直接使用 ListPage，而应该使用它的子类。**

它封装了以下方法：
- 读取读取一定范围页数据列表
- 获取当前页数据列表
- 获取当前页行元素对象列表
- 跳转到下一页
- 跳转到特定页
- 获取总页数

## ListPageS

ListPageS 用于处理无须 js 加载的静态页面。基于 MixPage 的 s 模式，即使用 requests 访问页面。



## ListPageD

ListPageD 用于处理由js加载的列表页。基于 MixPage 的 d 模式，即使用 selenium 访问页面。  

使用 ListPageD 须预先配置浏览器和驱动文件路径，详见 DrissionPage 用法中[初始化](https://gitee.com/g1879/DrissionPage#%E5%88%9D%E5%A7%8B%E5%8C%96)一节。



## 格式要求

创建 ListPage 对象时须传入页面结构，格式如下：

```python
待补充
```

取内容时传入待爬内容结构，格式如下：

```python
待补充
```

返回内容格式如下：

```python
   [  
        ['参数1结果', '参数2结果', ...],  
        ['参数1结果', '参数2结果', ...],  
        ...  
    ]
```

# 滚动式列表页

***

## ScrollingPage

ScrollingPage 类是滚动加载式列表页基类，继承自 DrissionPage 的 MixPage 类。  
专门用于处理滚动加载式列表页面。如新闻列表页。  
封装了对页面的基本读取和操作方法，只能在 MixPage 的 d 模式下工作。  

它封装了以下方法：

- 获取当前数据列表
- 获取当前行元素对象
- 获取新加载的数据列表
- 获取新加载的元素对象
- 滚动一页

## 格式要求

ScrollingPage 要求的 xpaths 稍有不同，格式如下：

```python
待补充
```

待爬内容结构及返回内容结构与翻页式列表相同。

# 使用方法

***



# APIs

***

