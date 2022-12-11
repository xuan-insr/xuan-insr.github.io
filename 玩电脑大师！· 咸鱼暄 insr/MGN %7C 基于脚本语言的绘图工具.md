
:::info
**本工程是 2021~2022 学年浙江大学光电学院《软件技术基础》课程设计**

**作者及分工**<br />--

**本文链接**：[https://www.yuque.com/xianyuxuan/coding/mgn](https://www.yuque.com/xianyuxuan/coding/mgn)
:::


### 1 概述

#### 1.1 设计背景与内容
在学习或教学算法和数据结构的过程中，用可视化的方式展示其具体结构或流程可以很大程度上帮助同学们加深理解和印象。我们在第 3 次上机作业中用到 MFC 来绘制树，同时第 4 次上机作业中也有用 MFC 展示排序序列的建议。我们意识到，用 MFC 绘图本身是有其繁杂性的。因此我们设计了这个工程，来帮助学习者或者教学者更方便地通过 MFC 绘制出需要的图像。

这个设计可以分为 3 部分：

1. 一种 **脚本语言 MGN, MFC Graphic Notation**，用于告诉程序：在哪里绘制一个图元（直线、圆、矩形或字符串）。
2. MGN 的 **解释器**，实现对 MGN 的解释，即根据 MGN 的描述进行绘制。
3. 根据输入的常用数据结构（如树、排序序列）等生成 MGN 的 **生成器**。

本设计可以帮助使用者无需编写复杂的绘图语句就可以实现一些基本的绘图操作；同时由于其生成代码、解释代码、绘图的模块独立性较高，因此有着非常好的 **可扩展性**。


#### 1.2 工程结构
本设计在 Windows 10 下进行，使用的开发工具是 Visual Studio 2022。低于此版本的 Visual Studio 可能不能正确打开该工程。

由于 MGN 的解释器和生成器在逻辑上并没有必然的关系，我们将其分为两个工程分别实现。<br />在总文件夹下，`/MGN/MGN`目录下可以找到解释器工程 `MGN.sln`。这个工程实现的是读入一个 mgn 代码，绘制出对应的图像序列。<br />在 `/Generator/MGNGenerator`目录下可以找到生成器示例工程 `MGNGenerator.sln`。这个工程提供使用生成器的若干实例。使用生成器，可以简单地生成若干 mgn 代码，这些代码默认存放在 `/Generator/MGNGenerator/output`文件夹下。<br />在 `/demoMgns`目录下可以找到一些 mgn 代码示例。


#### 1.3 本文内容安排
本文的第 2 节首先展示本设计的使用方法，第 3 节介绍本设计的代码结构和设计思路，第 4 节进行一些分析和讨论。


### 2 用法展示

#### 2.1 MGN 语法规则
MGN 的语法相当简单。它由三部分组成：绘制指令、格式指令和分隔符。

**绘制指令** 用于告诉解释器在哪里绘制一个图元。当前支持的语法包括：

   - `line <x0> <y0> <x1> <y1>` 其中 `<...>` 是一个浮点数（后同），表示从 (x0, y0) 到 (x1, y1) 绘制一条直线；
   - `circle <x> <y> <r>` 表示绘制一个以 (x, y) 为圆心的、半径为 r 的圆；
   - `rect <x> <y> <len> <wid>` 表示绘制一个以 (x, y) 为左上角的、长为 len、宽为 wid 的长方形；
   - `string <x> <y> <str>` 表示在 (x, y) 处打印一个字符串 str，以空白符为界。

**格式指令** 用于告诉解释器，当前页面中接下来的图元以什么格式绘制。当前支持的语法包括：

   - `color <color>` 表示接下来的所有图元以这个颜色绘制。当前支持的颜色包括：
      - black, white, red, blue, yellow, green, purple, pink
   - `filled` 表示接下来的图元（这里特指圆和长方形）都是填充的；
   - `unfilled` 表示接下来的图元（这里特指圆和长方形）都是不填充的；
   - `fontsize <sz>` 表示接下来打印的字符串的字体大小都为 sz。

在演示数据结构和算法的一些工作流程时，我们时常需要展示一段连续的变化而不是单一的图像。MGN 支持在一个文件中包含多个图像，解释器负责将它们逐个展示。**分隔符** 是在 MGN 文件中的一个单独的 `#`，用于分隔一个 MGN 文件中的多个图像。MGN 解释器每次绘制图形到一个单独 `#` 或者文件结束；用户可以通过按钮让解释器绘制前一个或者后一个图像。


#### 2.2 MGN 解释器界面
![image.png](./assets/1641888626354-85100371-6586-46df-a644-7f0fa3b691a9.png)

- Load：加载一个现有的 MGN 文件并开始绘制
- Prev / Next：跳转到前一 / 后一页
- Jump：跳转到指定页面
- 方向键：移动画布
- + / -：缩放画布


#### 2.3 绘制功能
**例 1**<br />对于下面这段简单的 MGN 代码，MGN 解释器可以给出其绘制：
```
fontsize 20
filled
color black
rect 30 310 40 14
string 30 310 1
string 30 360 2
unfilled
color red
circle 100 100 15
```
![image.png](./assets/1641889452133-d8779267-047c-422a-ad33-0dbd3e259a8b.png)

**例 2**<br />对于下面这段由多个部分组成的 MGN 代码，MGN 解释器可以逐个绘制：<br />（共 5 个页面，篇幅限制只展示前两个的代码；完整代码见 sortDemo.mgn）
```
fontsize 20
color black
rect 30 216 40 14
string 30 310 1
color black
rect 100 190 40 40
string 100 310 3
color black
rect 170 203 40 27
string 170 310 2
color black
rect 240 150 40 80
string 240 310 6
color black
rect 310 96 40 134
string 310 310 10
color black
rect 380 136 40 94
string 380 310 7
color black
rect 450 110 40 120
string 450 310 9
color black
rect 520 176 40 54
string 520 310 4
color black
rect 590 83 40 147
string 590 310 11
#
fontsize 20
color black
rect 30 216 40 14
string 30 310 1
color red
rect 100 203 40 27
string 100 310 2
color red
rect 170 190 40 40
string 170 310 3
color red
rect 240 176 40 54
string 240 310 4
color red
rect 310 150 40 80
string 310 310 6
color red
rect 380 96 40 134
string 380 310 10
color red
rect 450 136 40 94
string 450 310 7
color red
rect 520 110 40 120
string 520 310 9
color black
rect 590 83 40 147
string 590 310 11
```
（已经过放大和移动）
![image.png](./assets/1641903895230-e984c21d-b07a-4aed-ad69-d23664346e9e.png)
![image.png](./assets/1641903904327-f0e5a935-7a74-441e-9e96-67552da8a800.png)
MGN 解释器可以实现画布的大小调整和移动：
![image.png](./assets/1641889625638-4f8dbbf9-1108-4174-bc9f-87dce7c95da3.png)
![image.png](./assets/1641889634501-789ed39b-20f2-4fab-8e98-dc98edcb972b.png)

**例 3**<br />作为另一个例子，我们用堆排序展示绘制树及其应用：
![image.png](./assets/1641902095311-893175ac-d81c-483a-9b83-d382d4ee90ba.png)
![image.png](./assets/1641902105524-17df1b5e-a082-41d9-97ce-b897825d0b90.png)
![image.png](./assets/1641902115134-0d965d81-4791-41d1-82e3-25437fb84f23.png)
![image.png](./assets/1641902129799-d800a855-ec1b-4df9-8b84-12e5beea0e45.png)


#### 2.4 MGN 代码生成
MGN 代码生成有 2 种方法：

1. **调用生成器生成**。用户可以使用 MGN 生成器，在数据结构或算法流程中需要绘制的地方调用生成器的相关函数进行生成。
2. **用户手动编写**。当然，用户也可以根据 MGN 语法规则手动编写一些简单的 MGN 代码。

第二种方法较为简单，我们介绍第一种方法，即生成器的使用方式。

作为示例，我们编写了两种生成器，分别是数组生成器和树生成器；用户或者其他贡献者还可以根据需要编写其他更多的生成器。

数组生成器的类结构 `MgnArrayGenerator`如下：
```cpp
class MgnArrayGenerator {
private:
	const int MAX_HEIGHT = 200;
	const int LEFT_PAD = 30;
	const int TOP_PAD = 30;
	const int WIDTH = 40;
	const int FONT_SIZE = 20;
	const int SPACE = 30;
	
    std::stringstream result;
    std::string fileName;
    
    bool isIn(int x, std::vector<int> &vec);
public:
    MgnArrayGenerator();
    void init();
    void generate();
    void setFileName(std::string fileName);
    void addArrayFig(std::vector<int> &src, int maxValue, std::vector<int> &stressedItems);
};
```
用户创建一个该类对象后，可以调用 `setFileName()`函数设置输出文件名；如果不设置则默认为 `untitled.mgn`。

用户每调用一次 `addArrayFig()`函数，就会增加输出的一个页面；这个函数的三个参数的含义分别是：

- `src`，需要绘制的数组；
- `maxValue`，对于任意一个值 `a`，其实际画出的高度为 `MAX_HEIGHT * a / maxValue`；
- `stressedItems`，数组中需要用红色着重标出的项目的下标。

用户通过调用 `generate()`函数实现对应文件的生成；这个操作 **不会** 清空当前已经保存的绘画内容。

用户需要清空绘画内容时，可以调用 `init()`恢复初始状态。注意，这个函数会使得文件名重新置为默认值。

作为一个例子，我们展示冒泡排序如何使用这个生成器生成 MGN 代码：
```cpp
void bubbleSortExample(vector<int> &v) {
	vector<int> st = {};

	MgnArrayGenerator maGen;
	maGen.setFileName("bubbleSortExample.mgn");
										// 设置文件名
	maGen.addArrayFig(v, 15, st);		// 排序前生成一张图片
	for (int i = 0; i < v.size() - 1; i++) {
		for (int j = v.size() - 1; j >= i + 1; j--) {
			if (v[j] > v[j + 1]) {
				swap(v[j], v[j + 1]);
				st.push_back(j);		// 标记 j
				st.push_back(j + 1);	// 标记 j+1
			}
		}
		maGen.addArrayFig(v, 15, st);	// 每一趟，生成一张图片
		if (!st.size()) break;
		st.clear();						// 清空标记
	}
	maGen.generate();					// 生成文件
}
```
可以看到，标有注释的行即为调用生成器的相关行。我们着重标出的是本轮中交换过的元素。<br />生成的代码经过 MGN 解释器绘制，即为 2.3 节中的第 2 个示例（已经过放大和移动处理）。

树生成器的类结构`MgnTreeGenerator`如下：
```cpp
class MgnTreeGenerator {
private:
    static const int PLACE_R = 20;
    static const int ACTURAL_R = 30;
    static const int LEFT_PAD = 10;
    static const int TOP_PAD = 10;
    static const int FONT_SIZE = 40;
	
    std::stringstream result;
    std::string fileName;
    
    bool isIn(int x, std::vector<int> &vec);
    int getLeftCenter(int i, int levels);
    int getTopCenter(int i, int levels);
public:
	static const int INF = 0x7fffffff;
    MgnTreeGenerator();
    void init();
    void generate();
    void setFileName(std::string fileName);
    void addTreeFig(std::vector<int> &src, std::vector<int> &stressedItems);
};
```
其逻辑与数组生成器基本一致。需要说明的是：

- `addTreeFig()`函数只需要数据源和着重元素两个数组；
- 树生成器是基于完全二叉树绘制的。如果有需要留空的节点，请将其值设为 `MgnTreeGenerator::INF`，这样生成器会忽略这个节点（如下图所示）

![image.png](./assets/1641901798303-72c58831-70e0-416f-9eb4-b317bbf722be.png)

作为一个例子，我们展示堆排序如何使用这个生成器生成 MGN 代码：
```cpp
// 堆排序下滤，略
void sift(vector<int>& p, int i, int n);

// 堆排序算法
//堆排序算法
void heapSortExample(vector<int>& p) {
	vector<int> st = {};

	MgnTreeGenerator mtGen;
	mtGen.setFileName("heapSortExample.mgn");
										// 设置文件名

	int i, mm, t, n = p.size();
	mm = n / 2;

	st.push_back(mm - 1);				// 设置强调元素
	mtGen.addTreeFig(p, st);			// 展示排序前情况
	
	for (i = mm - 1; i >= 0; i--) {
		sift(p, i, n - 1);
		if (i) st[0] = i - 1;			// 设置强调元素
		else st.clear();
		mtGen.addTreeFig(p, st);		// 展示建堆时每一次下滤后的结果
	}
	
	for (i = n - 1; i >= 1; i--)
	{
		t = p[0];
		p[0] = p[i];
		p[i] = t;
		sift(p, 0, i - 1); 
		mtGen.addTreeFig(p, st);		// 展示每次删除根节点后下滤的结果
	}

	mtGen.generate();
}
```
生成的代码经过 MGN 解释器绘制，即为 2.3 节中的第 3 个示例（已经过放大和移动处理）。


### 3 解释器代码设计概述
在 2.4 小节我们讲解了生成器的基本设计思路，本节我们讨论解释器的代码设计。<br />解释器负责对 MGN 脚本语言的解释，并根据解释的结果调用 MFC 的功能进行绘制。


#### 3.1 MFC
主要是按钮的响应。<br />对于上下左右和增大缩小，用这个类的一个对象记录：
```cpp
struct MgnMoveScale {			// 记录画布移动和缩放状态
    double centerX, centerY;
	double scale;
}
```
按下 Load 以后，选择文件，建立 ifstream，然后调用 MgnInterpreter 的 interpret 函数。


#### 3.2 MgnInterpreter 类
MgnInterpreter 类其实是整个解释和画图过程的启动器：
```cpp
class MgnInterpreter {						// 解释器类
private:
	vector<MgnPage> pages;					// 当前 MGN 包含的页面
	
public:
	void interpret(ifstream &fin, MgnMoveScale &mms); 	
  											// 解释，完成 pages 的填充，顺便查错
	void draw(int pageIndex, MgnMoveScale &mms);
  											// 根据给定的移动和缩放状态绘制页面
};
```
讨论我们在第 Load 中调用的 `interpret` 函数。它的功能是，将输入的文件以 `#` 为界拆分成若干份字符串（如果不知道为什么要这么拆，请去回顾我们设计的语法规则）。对于每一份，新建一个 MgnPage，把这份字符串交给它去做。那么 MgnPage 是什么呢？它长这样：
```cpp
class MgnPage {								// 页面类
private:
	vector<MgnItem *> items;				// 当前页面包含的图元的指针
    
public:
    MgnPage(string &str);					// 构造函数，解释这个页面的代码，
    										// 完成 MgnItem 的填充
	void draw(MgnMoveScale &mms);			// 根据给定的移动和缩放状态绘制该页面
};
```
	其实和 MgnInterpreter 差不多，构造函数实现 interpret，还有一个 draw 实现绘制。<br />所以 `MgnInterpreter::interpret` 大概可以这么实现：
```cpp
void MgnInterpreter::interpret(ifstream &fin, MgnMoveScale &mms) {
    hasError = false; // 重新 load 之后，应当清空之前的错误
    
    if (!fin) {	// 如果传进来的 ifstream 无效，说明之前没有成功打开
        statusMsg = "[Error] 打开文件失败";
        hasError = true;
        drawStatusMsg();
    } else { // 如果没问题
        string currentStr = "", temp;
        while (fin >> temp) {	// 如果文件结束自动跳出
            if (temp != "#")
                currentStr += " ";
            	currentStr += temp;
            else {	// 如果遇到一个单独的 #
                if (!currentStr.empty()) {	// 如果当前字符串不为空
                    MgnPage page(currentStr);	// 交给 page 去处理
                    pages.push_back(page);	// 页面数组增加一个
                    currentStr = "";
                } 
            }
        }
        if (!currentStr.empty()) {	// 如果当前字符串不为空
            MgnPage page(currentStr);
            pages.push_back(page);
            currentStr = "";
        }
    }
    
    draw(1, mms); // 直接画第一页！
}
```
draw 函数就很简单了。只需要这样：
```cpp
void draw(int pageIndex, MgnMoveScale &mms) {
    pageIndex--;	// 程序里页面是从 0 开始编号的，所以要 -1
    /* 先清屏 */
    if (!hasError) { // 如果有错就不画页面了
        if (pages.size() > pageIndex)
            pages[pageIndex].draw(mms);
        else
            statusMsg = "Invalid page index.";
    }
    drawStatusMsg();
}
```


#### 3.3 MgnItem 类及其派生类
我们先跳过 MgnPage 类，看一看最终的图元被存在了哪里：
```cpp
enum Colors {MGN_BLACK, ...};				// 颜色的枚举

class MgnItem {								// 图元基类
protected:
	Colors color;
	int fontSize;
	bool isFilled;
public:
	virtual void draw(MgnMoveScale &mms) = 0;				
  											// 虚函数，各图元派生类实现
};
```
首先看到的是一个枚举，这里放的是一些颜色的定义。<br />MgnItem 类包括了颜色、字体大小、是否填充三个成员，因为它们是格式指令所指明的。`draw()` 函数是一个虚函数，需要由继承它的各个派生类去实现，这里先不实现。

它有四个派生类，我们举第一个为例：
```cpp
class MgnCircle : public MgnItem {			// 圆形
private:
	double x, y, r;
public:
    MgnCircle(Colors color, int fontSize, bool isFilled, double x, double y, double r);
	void draw(MgnMoveScale &mms);			// 根据给定的移动和缩放状态，真正调用 MFC 画图元
};
```
这个是表示圆形的类。它的构造函数实现了对成员的赋值：
```cpp
MgnCircle::MgnCircle(Colors color, int fontSize, bool isFilled,
                     double x, double y, double r) {
    this.color = color;
    this.fontSize = fontSize;
    this.isFilled = isFilled;
    this.x = x;
    this.y = y;
    this.r = r;
}
```
因为这个类继承了 MgnItem，因此它也有颜色、字体大小、是否填充三个成员。<br />这里的 `draw` 函数就是真正要实现画图功能的了。具体的实现可以参见代码。

另外三个派生类也大同小异。
```cpp
class MgnRect : public MgnItem {			// 矩形
private:
	double x, y, len, width;
public:
	void draw(MgnMoveScale &mms);			// 根据给定的移动和缩放状态，真正调用 MFC 画图元
};

class MgnLine : public MgnItem {			// 直线
private:
    double x1, y1, x2, y2;
public:
    void draw(MgnMoveScale &mms);			// 根据给定的移动和缩放状态，真正调用 MFC 画图元
};

class MgnString : public MgnItem {			// 字符串
private:
	double x, y;
    string content;
public:
	void draw(MgnMoveScale &mms);			// 根据给定的移动和缩放状态，真正调用 MFC 画图元
};
```


#### 3.4 MgnPage 类
```cpp
class MgnPage {								// 页面类
private:
	vector<MgnItem *> items;				// 当前页面包含的图元
    bool isNum(string &str);				// 判断字符串是不是数字
    double toNum(string &str);				// 字符串转数字
    
public:
    MgnPage(string &str);					// 构造函数，解释这个页面的代码，
    										// 完成 MgnItem 的填充
	void draw(MgnMoveScale &mms);			// 根据给定的移动和缩放状态绘制该页面
};
```
刚才我们看到了，MgnInterpreter 实际上是启动器，MgnItem 实现的是每个图元的绘制，那么 MgnPage 实现的就是主要是对输入的解析了。<br />解析输入时需要额外考虑的是 **输入是否正确**。用户可能给出错误的输入，程序应当发现并报错，且不应崩溃。<br />首先看一下 draw 函数：
```cpp
void MgnPage::draw(MgnMoveScale &mms) {
    for (auto item : items) {
        item->draw(mms);
    }
}
```
这样就可以实现对每个图元的绘制了。

下面考虑构造函数。构造函数做的事情就是分析传入的字符串，然后据此填入一个个 item：
```cpp
void MgnPage::MgnPage(string &str) {
    Colors color = MGN_BLACK;
    int fontSize = 28;
    bool isFilled = true;		// 三个状态的默认值
    
    stringstream sin(str);		// 可以理解为把 str 变成像 cin 和之前的 fin 一样
    							// 可以用 >> 读入的流
    string current;
    while (sin >> current) {	// 当 sin 没有结束
        if (current == "circle") {
            string xstr, ystr, rstr;
            sin >> xstr >> ystr >> rstr;
            if (isNum(xstr) && isNum(ystr) && isNum(rstr)) {
                int x = toNum(xstr), y = toNum(ystr), r = toNum(rstr);
                items.push_back(new MgnCircle(color, fontSize, 
                                              isFilled, x, y, r));
            }
            else {
                /* 报错:
                 statusMsg = "[Error] " + current + " " + x
                 			+ " " + y + " " + r + " 附近有语法错误";
                 */
                return;
            }
        } else if (...) 
            /* 补上剩余的可能 */
    }
}
```


### 4 分析与讨论

#### 4.1 鲁棒性测试
我们测试一些情况，观察程序的表现：

- 跳转到错误的页面
   - 当尝试跳转到非法页面时，MGN 解释器会报错。例如：

![image.png](./assets/1641903015850-bae54fb3-f171-4cbe-bba0-0f4ed831c72e.png)

- MGN 代码有语法问题
   - 当 MGN 代码有语法问题时，MGN 解释器会报错。例如：

![image.png](./assets/1641902966369-180564d3-974e-4983-b77d-f522d0924892.png)
![image.png](./assets/1641902982704-776f8e9a-1af4-48b6-b651-9c78b92a0ecd.png)

- 多次加载、重复加载
   - 经测试，在加载后重复加载或者加载其他文件不影响程序的正确性。


#### 4.2 问题与不足
有如下问题尚未解决：

- 由于 MFC 字符串绘制的定位逻辑与绘制其他图形有一定偏差，因此在放缩时会有一定程度的位移
- 没有实际上限制绘图区域。当图像被绘制在窗口非绘图区的其他地方时，清空绘图区并不能清空这些内容。


#### 4.3 可扩展性
本工程除了实现了一个方便的绘图工具外，还具有良好的可扩展性。具体表现为：

- 基本绘图方面：由于我们在解释器部分充分使用了 **继承和多态**，因此如果未来需要 **增加一种新的图元类型 **时，只需要增加 `MgnItem` 的一个子类即可，并不需要更改上层的逻辑；
- MGN 代码生成方面：由于我们编写的 `MgnArrayGenerator`和 `MgnTreeGenerator`是通用的、无预设的数组和树的 MGN 代码生成器，因此可以容易地用于可视化展示 **任何基于数组或树 **的算法；
- 生成器方面：由于生成器与解释器的耦合相当轻，因此如果未来需要 **支持更多数据结构的展示** 时，只需要编写新的生成器即可。
