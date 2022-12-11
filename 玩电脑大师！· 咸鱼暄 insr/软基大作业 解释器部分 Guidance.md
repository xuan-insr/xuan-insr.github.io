
### 在一切开始之前
请保证遵守代码规范；尤其是变量命名。<br />如果遇到编译问题，可能是我给出的部分有问题，可以先问问我QWQ<br />如果运行时遇到期望之外的结果，可以尝试调出控制台进行输出调试。具体如何调出可以百度。


### 解释器部分是干什么的？
实际上，就是从文件读取输入，根据输入在 MFC 窗口上画图。


### 怎么做？

#### 1 建立 MFC 工程文件，绘制要求的窗口
![image.png](./assets/1639393946473-c590ef45-4a5f-490c-8781-b70003b902f1.png)
状态栏就是一个显示字符串的地方；怎么实现都可以。<br />按钮的颜色都弄成一样的就可以，这里区分颜色只是为了区分功能。


#### 2 记录画布移动和放大缩小 / 状态栏

- 上面有若干按钮，紫色的是用来控制画布的移动和放大缩小的。如何实现呢？我们首先需要记录当前的移动和缩放状态。我们在画 MFC 的那个文件中建立一个结构体：
```cpp
struct MgnMoveScale {			// 记录画布移动和缩放状态
	double centerX, centerY;
	double scale;
};
```
在画 MFC 的那个类里加一个成员变量 `MgnMoveScale mms;`，用这个变量来存储当前的移动和缩放信息。初值应当是 `{0, 0, 1}`。<br />这样，我们就可以编写上下左右和放大缩小按钮的响应函数了：在这些函数里，对 mms 的值做调整即可。

我们在 MFC 的那个类里还需要维护状态栏的一些信息：
```cpp
	bool hasError;							// 是否有错误
	string statusMsg;						// 状态提示，例如成功和错误信息
	void drawStatusMsg();					// 绘制状态提示
```
有一个函数 `drawStatusMsg()`。这个函数的功能很简单：调用 MFC 的相关功能，在软件最底下打印 `statusMsg` 这个字符串。


#### 3 Load - 加载文件
下面我们来考虑如何编写 Load 按钮的响应函数。

- 首先，唤起一个选择文件窗口，引导用户选择一个文件。如何实现呢？可以百度类似“MFC 选择文件”的内容，抄一段代码。
- 用户选择完文件之后，文件路径应该会保存在一个字符串中，我们假设它叫 `filePath`。我们应当建立一个 `ifstream`（in-file stream，文件输入流，和 cin 原理一样，只是来源是文件而不是控制台）打开这个文件。例如
```cpp
ifstream fin;
fin.open(filePath, ios::in);
```

- 文件打开后，我们就可以调用我们的解释器进行解释和画图了。我们的解释器的声明长这样：
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
	也就是说，我们现在调用 `interpret(fin, mms);` 就可以了。


#### 4 关于 vector
vector 是 C++ 提供的一种容器，其实就是一个会自动变长的数组。需要头文件 `#include<vector>`。<br />例如， `vector<int> a;` 其实就和 `int a[100];` 差不多，建立一个名为 `a` 的 int 数组。只是它的大小会变化。<br />所以上面 `vector<MgnPage> pages;` 其实就是建立了一个数组，名为 `pages`，其中的每个元素都是一个 `MgnPage` 类的对象。这个类我们一会儿再说。<br />如何使用 vector 呢？会用到的用法有这几个（以 vector<int> a 为例）：

- `a.push_back(1);`，用于在这个数组最后增加一个元素，值为 1；
- `a[0]` 表示数组的第一个元素，这个和正常的数组一样；
- `a.size()` 返回这个数组的元素个数；
- 因此，遍历一个 vector 可以这么写：`for (int i = 0; i < a.size(); i++) { cout << a[i]; }`；
- 另一个简便的写法是：`for (auto item : a) { cout << item; }`，这个写法和上面那个写法等价；
- 应该用不到更多用法了；如果有需要的话可以问我qwq


#### 5 MgnInterpreter 类
这个类其实是整个解释和画图过程的启动器。再放一遍代码：
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
（注：5~7 行使用了之前说的状态栏相关的内容。因此这里的代码可能需要自行调整，因为这里不一定能访问到那些变量和函数。这个问题后面不再重复。）

draw 函数就很简单了。只需要这样：<br />（注：从这里开始，所有使用 `/* */` 注释的地方就是需要你来完成的部分！）
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


#### 6 MgnItem 类及其派生类
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
首先看到的是一个枚举，这里放的是一些颜色的定义；大概至少支持黑色、红色、蓝色吧，也可以多弄点。<br />MgnItem 类包括了颜色、字体大小、是否填充三个成员，因为它们是格式指令所指明的。`draw()` 函数前面有个 `virtual`，后面有个 `= 0`，这表示这个函数是一个虚函数，需要由继承它的各个派生类去实现，这里先不实现。因此这个类就这样放着就行了，不需要些什么实现。

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
因为这个类继承了 MgnItem，因此它也有颜色、字体大小、是否填充三个成员。<br />这里的 `draw` 函数就是真正要实现画图功能的了。这个需要自己去写！实际上画图需要根据本身的参数（如这里的 x, y, r）和 `mms` 指明的画布移动和缩放来进行绘制。例如坐标通过类似 `(x - mms.centerX) * mms.scale` 的方式计算。

另外三个派生类也大同小异。请补上对应的构造函数！
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
提示：字体大小也需要按照 scale 缩放~


#### 7 MgnPage 类
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
刚才我们看到了，MgnInterpreter 实际上是启动器，MgnItem 实现的是每个图元的绘制，那么 MgnPage 实现的就是主要是对输入的解析了。<br />解析输入时需要额外考虑的是 **输入是否正确**。用户可能给出错误的输入，程序应当发现并报错，且不应崩溃。<br />首先看一下 draw 函数，这里直接写好：
```cpp
void MgnPage::draw(MgnMoveScale &mms) {
    for (auto item : items) {
        item->draw(mms);
    }
}
```
这样就可以实现对每个图元的绘制了。

下面考虑构造函数。构造函数做的事情就是分析传入的字符串，然后据此填入一个个 item。大概可以这么写：
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
	在这个函数里像 10~24 行的示例那样完成对所有输入的处理即可。<br />请注意，15~16 行的插入方式是新增图元的标准格式；记得为每个不同的类型更换不同的子类！

两个辅助函数可以这么写：
```cpp
bool MgnPage::isNum(string &str) {
	stringstream sin(str);  
    double d;  
    char c;  
	if( !(sin >> d) )  
        return false;
    if (sin >> c) 
        return false; 
    return true;      
}

double MgnPage::toNum(string &str) {
    stringstream sin(str);  
    double d;
    sin >> d;
    return d;
}
```
	<br />有问题的话随时问我QWQ
