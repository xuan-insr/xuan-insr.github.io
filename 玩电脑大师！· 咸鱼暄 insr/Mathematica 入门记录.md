本文主要记录尝试使用 Mathematica 的一些操作。

看到的东西：


#### 开始

- 新建笔记本。 **指令输入后按 Shift+Enter 运行** 。


#### 函数

- **函数：** 如下图所示，在变量名后加下划线表示自变量（绿色）；输入的字母会被识别为标识符（蓝色）。按 Shift+Enter 即存储。

![image.png](./assets/1609724995264-6ab8ad3f-9238-4ad3-bea9-13b0d9c7ab47.png)
下图是一个使用，同时定义了一个名为 B1 的函数：
![image.png](./assets/1609725197367-c43d570a-2ce6-4cea-a33c-6ebe881f02a5.png)
我们可以给变量赋值：
![image.png](./assets/1609725317179-38c7e165-0658-4f3d-8e28-9d4190792094.png)
清除变量赋值：
![image.png](./assets/1609725728062-807c673e-59f2-4a9e-b733-3e6fe02168f8.png)

- **求导：** `D[func, var]` 是求导函数：

![image.png](./assets/1609725265903-084b9ee6-4094-4cba-a20e-885eac0337bc.png)

#### 作图

- **画图：** 

![image.png](./assets/1609725361734-8ee7b702-22f9-401f-8803-3791b5691e02.png)

- **描点作图：** 首先输入数据数组：

![image.png](./assets/1609725433321-1e3ff0ce-7ae8-4535-90be-ec803861c8a1.png)
![image.png](./assets/1609725519658-33cc6617-20a1-4f68-8035-c1bccf5dad13.png)
通过 `{}` 合并数组为两行多列，用 `Transpose[]` 函数将其转置为两列多行，即数对形式：
![image.png](./assets/1609725582436-8e1d516b-f72e-4f24-b231-0efe6678d9c2.png)
通过  `ListLinePlot`  绘图，用 `InterpolationOrder` 进行插值，从而使曲线平滑：
![image.png](./assets/1609725636919-bd4f6b08-1501-40ff-936b-697790cc4298.png)
对比：不用插值，箭头处显见不平滑：
![image.png](./assets/1609725682613-c24ee929-0fa8-4531-8f75-421f8b1d9af6.png)


#### 解方程
![image.png](./assets/1610830851111-950320e4-9295-4330-8d40-91bb15aae7cc.png)
![image.png](./assets/1610830858387-6aeae14c-13bf-47e1-932c-6c79063cb7f9.png)
