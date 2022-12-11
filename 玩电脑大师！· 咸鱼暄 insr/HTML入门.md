
# 0 开始之前

- 本次学习主要参考 [HTML教程 | 菜鸟教程](https://www.runoob.com/html/html-tutorial.html)。

- HyperText Makeup Language, 超文本标记语言，不是编程语言。
- HTML文档也称web页面。
- HTML包含HTML标签及文本内容，通过HTML标签来描述网页。
- HTML文档的后缀名为 .html 或 .htm，两者没有区别。



# 1 HTML基础


## 1.1 HTML简介
首先简单地看一看HTML到底长啥样qwq

### 

### 1.1.1 举个栗子！
从例子学起是不是更有目标性一些）

```html
<!DOCTYPE HTML>
<html>
  <head>
    <meta charset = "utf-8">
    <title>咸鱼暄的HTML入门<\title>
  <\head>
  <body>
    <h2>早！<\h2>
    <p>不知道写什么了）<\p>
  <\body>
<\html>
```

看看效果！

:::info

## 早！
不知道写什么了）
:::


### 1.1.2 来学习一下叭！

1. HTML标记标签(HTML tag)

通常称为HTML标签。是由尖括号包围的关键词，通常成对出现。标签对中的第一个标签是开始标签，第二个标签是结束标签，也称开放标签和闭合标签。

2. HTML元素

即从开始标签到结束标签的全部代码。

3. HTML网页结构

![HTML网页结构.png](./assets/1580369681880-d058adc4-b940-4178-8e8d-9298f55d81d6.png)
只有其中白色的<body>部分才会在浏览器中显示。

4. <!DOCTYPE> 声明

<!DOCTYPE>声明有助于浏览器正确识别网页。HTML5网页使用 ` <!DOCTYPE HTML>` 即可。<br /><!DOCTYPE>声明不区分大小写。

5. 中文编码

直接输出中文可能会出现乱码，因此我们需要在头部（<head>）将字符声明为 UTF-8 或 GBK。<br />即 `<meta charset = "utf-8">` 

6. 上面那坨代码的解析）
   1. `<!DOCTYPE HTML>` 声明为HTML5文档
   2. `** **<html>`  元素是 HTML 页面的根元素
   3. `<head>` 元素包含了文档的元（meta）数据，如 <meta charset="utf-8"> 定义网页编码格式为 utf-8
   4. `<title>`  元素描述了文档的标题
   5. `<body>`  元素包含了可见的页面内容
   6. `<h2>`  元素定义一个h2标题
   7. `<p>`  元素定义一个段落


## 1.2 HTML基础
下面来稍微具体地看看一些基础内容叭！


### 1.2.1 元素
HTML文档由 **HTML元素** 定义。<br />HTML元素以 **开始标签** （起始标签）起始，以 **结束标签** （闭合标签）终止。<br />元素的 **内容** 是开始标签和结束标签之间的内容。<br />某些HTML元素具有 **空内容（empty content）** ，这样的元素 **在开始标签中关闭** 。例如<br>标签（定义换行）。而保险起见， **所有标签都需要被关闭** ，因此虽然<br>可以表示换行，但使用<br/>是正确的。<br />同样的，对于有内容的元素，虽然大多数情况下不使用结束标签也能正常显示，但仍应该使用结束标签以保证长久的正确。<br />HTML标签 **对大小写不敏感** ，但 **请使用小写** 。


### 1.2.2 一些元素

1. 一些基本的元素
   1. 标题，通过标签<h1>~<h6>定义。浏览器会自动在标题前后添加空行。
   2. 段落，通过标签<p>定义。浏览器会自动在段落前后添加空行。
   3. 链接，通过标签<a>定义。例如：`<a href="url">文本</a>`。
      - href，Hypertext Reference，超文本链接，这里是元素的 **属性** （参见 **1.2.3 属性** ）。
   4. 图片，通过标签<img>定义。例如：`<img src="url" width="100" height="35" />` 
      - 关于图片的更多信息，还可以参见 **2.1 图像** 。
   5. 换行，通过标签<br>定义。例如： ` <br />` 
   6. 水平线（分割线），通过标签<hr>定义。例如： `<hr />` 
   7. 注释，通过标签<!--...-->定义。例如： `<!-- 这是注释-->` 
   8. 节（块级），通过标签<div>定义。
   9. 节（行内），通过标签<span>定义。
2. 文本格式化
   1. 加粗，<b><strong>
   2. 斜体，<i><em>
   3. 放大，<big>
   4. 放小，<small>
   5. 上标，<sub>
   6. 下标，<sup>
   7. 下划线，<ins>
   8. 删除线，<del>

For more: [HTML Tag Ref](https://www.runoob.com/tags/ref-byfunc.html)


### 1.2.3 属性
HTML元素可以设置 **属性(Attribute)** ，在元素中（一般描述与 **开始标签** ）添加附加信息。<br />属性总是以 **名称/值** 对的形式出现，如 **name="value"** 。<br />属性的值应该始终包括在引号内。双引号较为常用，但单引号也可用。

   - 但在属性值本身就包含双引号时，则必须使用单引号。

属性和属性值 **对大小写不敏感** ，但 **请使用小写** 。


### 1.2.4 一些属性

   1. class，为html元素定义 **一个或多个** 类名（类名从 **样式文件** （参见[咸鱼暄的CSS入门 1.3](https://www.yuque.com/xianyuxuan/coding/css#98pcQ)）引入）。
   2. id，定义元素的 **唯一** ID。多个是无效的。
      - 例如，存在id="tips"，那么可以创建链接 `<a href="#tips">提示</a>` 到该id所在的位置。
   3. style，规定元素的 **行内样式** 。

For more: [HTML Standard Attributes Ref](https://www.runoob.com/tags/ref-standardattributes.html)


### 1.2.5 头部
<head>元素内部（<head>和</head>之间的所有代码）包含了所有的头部标签元素。<br /><head>元素中，可以插入脚本（scripts），样式文件（CSS）以及各种元数据（Metadata）。

   1. <title>    `<title>标题</title>` 
      -  <title> 标签定义了不同文档的标题。
      - <title> 在 HTML/XHTML 文档中是必须的。
      - <title> 元素定义了：
         - 浏览器工具栏的标题
         - 当网页添加到收藏夹时，显示在收藏夹中的标题
         - 显示在搜索引擎结果页面的标题
   2. <base>    `<base href="url" target="_blank">` 
      - <base> 标签描述了基本的链接地址/链接目标，该标签作为HTML文档中所有的链接标签的默认链接
      - 其中的 **target** 属性定义了 **被链接的文档在何处显示** 。属性值为 **_blank** 时，将在新窗口中打开被链接的文档。属性值默认为 **_self** ，即在相同的框架中打开被链接的文档。其他属性值，参见[<a> target](https://www.runoob.com/tags/att-a-target.html)。
   3. <link>    `<link href="url" rel="stylesheet" type="text/css">` 
      - <link> 标签描述了文档与外部资源的关系，最常见的用途是链接样式表。
      - 其中的 **rel** 属性是必需的，规定了 **当前文档与被链接的文档/资源之间的关系** 。属性值为 **stylesheet** 表示导入的是样式表的URL。其他属性值，参见[<link> rel](https://www.runoob.com/tags/att-link-rel.html)。
      - 其中的 **type** 属性规定了被链接文档/资源的MIME类型，常用的为 **text/css** ，表示样式表。
         - MIME类型的相关知识在此并不重要，从略。
   4. <meta>
      - <meta> 标签提供了HTML文档的元数据。元数据不会显示，但会被浏览器、搜索引擎等调用。
      - <meta> 标签常见以下三种：
         - **<meta charset="UTF-8" />** 。
         - **<meta name="keywords" content="XianYu, HTML" />** 。其中 **content** 属性提供了元数据， **name** 属性将其关联到了一个名称。常见 **name** 属性的值有： **application-name（页面所代表的的Web应用程序的名称）** , **author（文档的作者名）** , **description（文档的描述**，搜索引擎会将这个描述显示在搜索结果中**）** , **keywords（关键词列表）。**
            - 请规定关键词，以便搜索引擎对其进行分类。
         -  **<meta http-equiv="refresh" content="30" />** 。其中 **content** 属性提供了元数据， **http-equiv** 属性起到了http头的作用。此处 **refesh** 规定了文档自动刷新的间隔时间（秒）。
      - 建议在<meta> 标签中包含结束标签（符合XHTML的语法规范）。
   5. <script>
      - <script>用于定义客户端脚本，比如JavaScript。
      - <script>既可以包含脚本语句，也可以通过 **src** 属性指向外部脚本文件。
      - 如果使用src属性，<script>必须是空的。
      - 关于JavaScript，参见[咸鱼暄的JavaScript入门](https://www.yuque.com/xianyuxuan/coding/js)。
   6. <style>   例如：
```html
<style type="text/css">
  p	{ color:rgb(0,255,0); }
</style>
```

      - <style> 标签定义HTML文档的样式信息。具体规则参见[咸鱼暄的CSS入门 - 1.2 CSS属性](https://www.yuque.com/xianyuxuan/coding/css#FYOk3)。
      - 如需链接外部样式表，使用前述<link>标签。
      - 每个HTML文档可能含有多个<style>元素。
      - 实际上，不写 **type="text/css"** 也不影响此处代码。但为了代码规范性，请使用。


### 1.2.6 其他

   - 需要说明的是，HTML代码中的所有连续空格和空行，在显示页面时 **都只会被算作一个空格** 。但是，我们可以通过<pre>标签对空行和空格进行控制。例如：
```html
<pre>
T   e   x  t 
1
</pre>
<br />
T   e   x  t 
2
```
运行结果：
:::info
T   e   x  t <br />1

T e x t 2:::


# 2 HTML实用


## 2.1 图像（未完成）

- **<img>** 标签定义图像。
   - <img>中的属性可以有：
      - **src** ，必需，规定图像的URL。
      - **alt** ，建议使用，规定图像的替代文本，在图片显示失败时显示。
      - **height** , **width** ，规定图像的高度和宽度。
   - 可以通过在<a>标签中嵌套<img>标签，给图像添加超链接。

- **<map>** 定义图像地图，即图像中带有一个或多个可点击区域，每个区域都可以设置超链接。

要用的时候再学8


## 2.2 表格

- **<table>** 定义表格。
   - 其属性 **border** 值为**""（无边框）**或**1（有边框）**。
- 表格下， **<tr>** 定义表格行(table row)。
- 行下 **<td>** 定义单元格(table data)。
   - 其属性 **colspan, rowspan** 分别定义了单元格横跨的列数和行数，这样可以实现单元格的合并。
   - 在第一行中，可以使用 **<th>** 定义表头(table heading)（也是单元格）。
- 表格下，可用 **<caption>** 定义表格标题。这会显示在表格外。
- 表格下，可以将表格行用 **<thead> <tbody> <tfoot>** 分为表格头、主体、表格尾三个部分。这可以帮助分页打印时，在每一页都显示表格头和尾。


## 2.3 列表

- **<ul>** 定义无序列表。 **<ol>** 定义有序列表。
   - 在上述标签内，用 **<li>** 定义列表项。
- **<dl>** 定义自定义列表。这种列表是项目及其注释的的组合。
   - 在上标签内，用 **<dt>** 定义自定义列表项， **与其并列地** ，<dd>定义自定义列表的注释。


## 2.4 表单

- 表单是一个包含表单元素的区域，通过表单标签 **<form>** 设置。
- <form>的部分属性如下：
   - **action** ，规定当提交表单时向何处发送数据。值为URL。
   - **method** ，规定如何发送表单数据。值可以为：
      - **get** ，将表单数据以名称/值对的形式附到URL中。注意：
         - URL的长度是有限的（约3000个字符）。
         - 通过这种方法提交的表单在URL中是可见的。因此 **不能用来发送敏感数据** ，但是 **适合需要加入书签的表单提交** （如搜索引擎的搜索页面）。
      - **post** ，将表单数据附加到HTTP请求的body内，不显示在URL中。注意：
         - 这种方法没有长度限制。
         - 这种方法提交的表单无法被加入书签。
   - **name** ，规定表单的名称。

- 多数情况下用到的表单元素是输入标签 **<input>** （没有结束标签，需要在开始标签中被封闭）。该标签 **支持所有事件属性** 。输入类型由属性 **type** 定义。常见的输入类型（即type属性的值）如下（示例将在本小节末一并给出）：
   - **text** ，文本域。用于键入字符。一般浏览器中的默认宽度为20个字符，但不限制输入内容数量。
   - **password** ，密码。用于键入密码字段。浏览器不会明文显示，而是用星号或圆点替代。
   - **radio** ，单选按钮。
   - **checkbox** ，复选框。
   - **submit** ，提交按钮。用户单击后，表单内容会被传送到另一个文件。目的文件由 **表单的action属性** 定义。
   - **reset** ，重置按钮。用户单击后，重置当前表单的内容。
   - **button** ，按钮。
   - 更多输入类型，参见[input-type](https://www.runoob.com/tags/att-input-type.html)。

input标签除了type属性，还有 **value, name **等常用属性。

- 其他表单元素也包括：
   - **textarea** ，文本域。用于键入字符。其部分属性如下：
      - **cols** ，文本区域内可见部分的宽度。
      - **rows** ，文本区域内可见部分的行数。
      - **autofocus** （值为"autofocus"），规定当文档加载时，文本区域自动获得焦点。
      - **maxlength** ，文本区域允许的最大字符数。
      - **placeholder** ，给予简单提示，描述文本区域期望的输入值。
      - **disabled** （值为"disabled"），禁用文本区域。可以设置此属性，并当满足某种条件时使用JavaScript移除此属性的值。
      - **name** ，规定文本域的名称。
      - **required** ，规定文本域是必填的。
      - **readonly** ，规定文本域是只读的。
   - **label** ，标记。这为鼠标用户提供方便。其属性 **for** （值为 _id_ ）将标签内的内容绑定到具有对应id的表单控件。在label标签内点击文本，浏览器则会视为点击了绑定的表单控件。
   - **fieldset** ，将表单元素分组，并在周围绘制边框。
      - **legend** 标签用来定义fieldset元素的标题，并在边框上显示。
      - fieldset标签可以具有 **disabled,** **name** 属性。
   - **select** ，用来定义下拉选项列表。在select元素内部，使用 **option** 元素定义下拉列表的选项。
      - **option** 元素可以具有的属性有：**value, disabled, selected**。其中selected的值为"selected"，规定了首次加载时对应选项被选中。
      - select标签可以具有 **disabled, required,** **name** 属性。
   - **button** ，用来定义一个按钮。元素内部可以放置内容，如文本和图像。其部分属性有：
      - **name, value, disable** 等；
      - **type** 属性，必需，用于规定按钮的类型。其值可为：
         - **button** 。
         - **reset** ，重置按钮。用户单击后，重置当前表单的内容。
         - **submit** ，提交按钮。用户单击后，表单内容会被传送到另一个文件。此时，（可能）需要如下属性配合使用：
            - **formaction** ，规定当提交表单时向何处发送数据。值为URL。覆盖form的action。
            - **formmethod** ，规定如发送表单数据。参见<form>的method属性。


## 2.5 框架（未完成）

## 2.6 媒体（未完成）

