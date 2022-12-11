
## 【连载】C++ Weekly Tips #3 - 快速入门 C++ 写题！
:::success
**本期作者：**[咸鱼暄](https://www.yuque.com/xianyuxuan?view=doc_embed)
**本文所需预备知识：**C / C++ 基础<br />**本文面向对象：**需要做算法题的萌新!<br />在做 LeetCode 或者各种笔试的算法题的时候，避免造轮子可以为我们节省很多写代码和调试的时间；而 C++ 在不断的发展中为我们实现了许多好用的特性。很多小朋友只在基础课程中学过 C 语言，学校开设的 C++ 相关课程可能也没有涵盖很多这方面内容。因此，本周我们试图发现那些在写题中常用的技巧，并加以分析和总结。<br />本文准备仓促，可能有很多遗漏和不严谨之处，欢迎批评指正 QWQ
:::

> 和本文无关，但是推荐阅读：


注意：这里的介绍只为满足最基本的使用；在搜索引擎搜索，可以找到更多的用法。当自己编程而不是在 LeetCode 之类的地方做函数题时，请自行搜索它们所需的头文件等信息。

> 如未特殊说明，本文讨论的内容都在 namespace std 里；本文的例子大多来源于 [cppreference.com](https://en.cppreference.com/)。



### 1 基础
使用 C++ 答题时，有一些非常基础和常用的内容，我们简单介绍它们！

#### 1.1 引用
参见 [2.6 引用](https://www.yuque.com/xianyuxuan/coding/apd2_6?view=doc_embed)（看 2.6.1 和应用的第 1 条就够了）。其实引用就是包装了一下的指针，让人用得更舒服。

#### 1.2 vector
> #include <vector>

vector 可以理解为一种自动扩展长度的数组。<br />**构造**。我们可以通过 `vector<int> v;`的方式构造一个空的、每个元素的类型均为`int`的 vector，其名字为`v`。可以用其他类型，包括自定义的结构体替换这里的`int`。也可以通过类似`vector<int> v = {1, 2, 3};`的方式初始化。<br />**获取长度**。可以通过`v.size()`获取 vector `v`中的元素个数。<br />**在末尾插入元素**。可以通过`v.push_back(x)`的方式将`x`插入到 vector `v`的末尾。这里的插入是使用拷贝构造的，而使用`v.emplace_back(...)`则可以在`vector`中进行“原地构造”，对于一些特定的数据类型效率更好，写起来也更简单。<br />**访问（读取 / 修改）元素**。和数组一样，可以通过`v[i]`的方式访问 vector `v`的第`i`个元素，下标从 0 开始。注意，当`i >= v.size()`的时候，程序可能发生运行时错误。<br />**遍历**。C++11除了使用 `for (int i = 0; i < v.size(); i++) sum += v[i];`的方式遍历以外，还可以这样写：`for (auto a : v) sum += a;`。这种写法叫做 range-based for loop。C++11这里的`auto`会自动推断出`a`的数据类型，也就是 vector`v`中元素的类型，官方称呼是 Placeholder type specifiers。在做 LeetCode 的绝大多数场景下，我们可以使用`for (auto &a : v)`，加上一个引用。加上这个引用后就不会在遍历的过程中每次循环都构造一个临时变量，在遍历二维`vector`的时候尤为有意义。当然加上引用后对这个变量`a`做的改动会真实地影响到`vector v`。

#### 1.3 string
> #include <string>

string 是 C++ 中的字符串类型。其实现和 C 中的字符数组一致，也是以`'\0'`标识结束。<br />**构造**。可以通过`string s;`或者`string s = "123";`的方式构造一个字符串。<br />**获取长度**。可以通过`s.length()`或者`s.size()`的方式获取其长度，该长度不含末尾的`'\0'`。<br />**拼接**。可以通过`s1 + s2`或者`s + 'a'`的方式将字符串与另一个字符串或字符（均可以是字面量）拼接。<br />**访问字符**。和数组、vector 一样，可以通过`s[i]`的方式访问字符串的第 i 个字符。<br />**遍历**。C++11类似 vector，可以通过`for (auto c : s)`的方式遍历字符串中的每一个字符。<br />**比较**。可以通过`==`, `!=`, `>`等比较运算符按字典序比较两个字符串。


#### 1.4 pair
> #include <utility>

pair 可以将两个不必相同的类型攒起来，例如`pair<int, int> p1;`或者`pair<int, string> p2;`。<br />可以用 `pair<int, double> p{1, 1.3};`的方式构造，也可以通过 `p = make_pair(0, -3.1)`的方式赋值。pair 之间也可以直接赋值。<br />可以用`p1.first`、`p1.second`的方式访问其成员。<br />pair 默认的比较方法是先按第一个字段比较，相同再按第二个字段比较。


> 后面的部分基本是想到哪写到哪，所以不完全有逻辑和难度的顺序）））
> 用 ☆ 标明个人认为比较常用的内容！


### 2 不那么基础

#### 2.1 ☆☆☆ sort
> #include <algorithm>

`sort`用于对数组或 vector 等可以随机访问且元素可比较的数据结构进行排序。复杂度是 ![](https://cdn.nlark.com/yuque/__latex/391e48baddd4a41ffd6ef700a6507116.svg#card=math&code=O%28N%5Clog%20N%29&id=h8hYe)。<br />例如：
```cpp
int a[] = {3, 1, 4, -2, 5, 3};
sort(a, a + 6);
```
此时`a`中的值为 -2 1 3 3 4 5，即升序排列。<br />这里`a`和`a + 6`是左闭右开的排序区间，也可以用类似`sort(a + 1, a + 4)` 的方式对部分进行排序。

对于 vector，也可以类似使用：
```cpp
vector<int> v = {3, 1, 4, -2, 5, 3};
sort(v.begin(), v.end());
```

如果想要降序怎么办呢？方法之一是：
```cpp
vector<int> v = {3, 1, 4, -2, 5, 3};
sort(v.begin(), v.end(), greater<int>());
```
此时`v`中的值是 5 4 3 3 1 -2。

另一种方法，我们可以自定义比较函数。比较函数接收两个元素的引用，返回一个 bool 值表示前者是否应当在后者之前：
```cpp
bool cmp(const int& a, const int& b) { return a > b; }
vector<int> v = {3, 1, 4, -2, 5, 3};
sort(v.begin(), v.end(), cmp);
```
注意，比较函数逻辑上相当于`a < b`。因此当两个元素相等时，比较函数总是应当返回 false。

C++11也可以使用 lambda 表达式（其实就是匿名函数，这里不展开了，有缘再聊 XD）简化写法：
```cpp
vector<int> v = {3, 1, 4, -2, 5, 3};
sort(v.begin(), v.end(), [](const int& a, const int& b) { return a > b; });
```

自定义比较函数可以适用更复杂的排序，例如需要比较的元素本身并没有内置的比较运算符的时候。例如：
```cpp
bool cmp(const vector<int>& a, const vector<int>& b) {
    return a[0] == b[0] ? a[1] < b[1] : a[0] < b[0];
}
```
这个比较函数可以用于`vector<vector<int>>`类型的排序。<br />常用的标准库（如 libgc++）中对于`std::sort`的实现保证复杂度是![](https://cdn.nlark.com/yuque/__latex/4b4e58b8ab948749ea351313fda66383.svg#card=math&code=O%28n%5Clog%20n%29&id=IsOXI)，而不会退化成快排的![](https://cdn.nlark.com/yuque/__latex/f2d5f588234eb61a559ff90c41511b85.svg#card=math&code=O%28n%5E2%29&id=vRDju)。因为它使用的是一种快排、堆排以及插入排序的结合体。<br />（还有更多比较器的写法，这里暂时不展开啦）


#### 2.2 ☆ upper_bound & lower_bound & binary_search & equal_range
> #include <algorithm>

用于有序的数组！ 可以像`sort`一样指定比较函数。

- `auto u = upper_bound(data.begin(), data.end(), i)`返回第一个 **严格大于** `i`的元素的迭代器（和指针差不多，可以用`*u`获取其值）；如果没有找到，返回第二个参数，即`data.end()`。
- `lower_bound`返回第一个 **大于等于** `i`的元素的迭代器；如果没有找到，返回第二个参数。这里演示的是一个自定义比较函数的例子（可以看到，传入的待查找参数并不一定需要和容器内元素的类型一致，只要和自定义比较函数吻合即可）：
```cpp
auto prc_info = lower_bound(prices.begin(), prices.end(), i,
    [](const PriceInfo& info, double value){ return info.price < value; });
```

- `binary_search(v.begin(), v.end(), i)`返回一个 bool，表示`i`是否在`v`中。

注意：这 3 个函数均使用二分查找，因此如果原数组不是有序的，结果就可能是错误的。复杂度均为![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=qP5kO)。


#### 2.3 gcd & lcm C++17
> #include <numeric>

经常记不住辗转相除法怎么写……这下不用记了！<br />`cout << gcd(18, 12) << " " << lcm(18, 12) << endl;`，输出为 `6 36`。


#### 2.4 Algorithm 库里其他看起来有用的东西
（下面的“数组”不仅可以是数组，也可以是其他一些满足相关条件的数据结构，且条件可能各不相同；在此暂不展开）

- C++17返回数组中最大的元素的迭代器，可以和 sort 一样自定义比较函数：`std::max_element`，也有 min [https://en.cppreference.com/w/cpp/algorithm/max_element](https://en.cppreference.com/w/cpp/algorithm/max_element) 
- C++17合并两个有序数组：`std::merge`[https://en.cppreference.com/w/cpp/algorithm/merge](https://en.cppreference.com/w/cpp/algorithm/merge)
- C++17逆转一个数组：`std::reverse`[https://en.cppreference.com/w/cpp/algorithm/reverse](https://en.cppreference.com/w/cpp/algorithm/reverse)


#### 2.5 其他

- 内置类型的最大 / 最小值：
   - #include <limits>
   - `std::numeric_limits<int>::max()`、`std::numeric_limits<char>::min()`之类的
- 可以用 `x & (x - 1) == 0`检验`x`是不是 2 的整数次幂
- 可以用 `x & (-x)`计算`x`最大的 2 的整数次幂因子 (the greatest power of 2 that divides X)
- 可以用 `__builtin_popcount(x)`计算 int `x`在二进制表示中 1 的个数；`__builtin_popcountll`可以用于 long long。


### 3 数据结构之类的东西
这部分其实不太清楚该怎么写QWQ，所以我尝试大概描述每种数据结构是干什么的以及它的用法；关于具体的实现相关的知识我尽量贴上链接~

它们都可以通过`a.size()`获取元素个数、`a.empty()`判断是否为空（返回 bool），就不在每个里面写一遍了！<br />未特殊说明的操作，复杂度均为![](https://cdn.nlark.com/yuque/__latex/a2006f1ac61cb1902beacb3e29fff089.svg#card=math&code=O%281%29&id=vUlUv)。<br />下面均以元素类型为`int`为例，但是这个类型也可以是其他任意类型，比如`stack<map<string, Foo>>`之类的也都可以！

#### 3.1 stack & queue & priority_queue | Container adaptors
这三种数据结构是不能遍历的。“如果你需要遍历它们，那么你就不应当选择它们。”

##### 3.1.1 ☆ stack & queue
> **栈**（stack）是一个后进先出（LIFO）表，限制了插入和删除只能在表的末端（成为栈顶，top）进行。典型的操作是 Push, Pop 和 Top（读取栈顶元素的值）。

#include <stack>

- 构造：`stack<int> s;`
- 压栈：`s.push(1)`
- 出栈：`s.pop()`
- 访问栈顶：`s.top()`
> **队列**（queue）是一个先进先出（FIFO）表。入队（Enqueue）在队尾（rear）插入一个元素，出队（Dequeue）则删除队头（front）的一个元素。

#include <queue>

- 构造：`queue<int> q;`
- 入队：`q.push(2)`
- 出队：`q.pop()`
- 访问队首 / 队尾元素：`q.front()`, `q.back()`

（另外还有`deque`，双端队列。好像很少用，省略）
> See Also：
> - [表、栈和队列 | Lists, Stacks and Queues](https://www.yuque.com/xianyuxuan/coding/evgh6g?view=doc_embed)



##### 3.1.2 ☆☆ priority_queue 
> **优先队列**（priority queue）是始终保证队头元素是队列中最小的一种数据结构，这里用堆实现。支持的主要操作有：插入（入队），查询和删除最小值（出队）。

#include <queue>

- 构造
   - `priority_queue<int> q1`：队首始终是最小值
   - `priority_queue<int, vector<int>, greater<int>> q2`：队首始终是最大值
   - 自定义比较函数：
```cpp
auto cmp = [](const int &a, const int &b) {return a > b;};
priority_queue<int, vector<int>, decltype(cmp)> q3(cmp);
```

   - 还可以用已有的数组初始化优先队列：
      - `priority_queue<int> q1(v.begin(), v.end());`
      - `priority_queue<int, vector<int>, greater<int>> q2(v.begin(), v.end());`
      - `priority_queue<int, vector<int>, decltype(cmp)> q3(v.begin(), v.end(), cmp);`
      - 这样初始化的复杂度是![](https://cdn.nlark.com/yuque/__latex/8c51f5913186f8ac629f1d5838940f33.svg#card=math&code=O%28N%29&id=KEAcL)的。

- 入队：`q.push(2)`
- 出队：`q.pop()`
- 入队和出队的复杂度是 ![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=vUsrj)的。

- 访问队首（最小）元素：`q.top()`

> See Also：
> - 优先队列的实现：[堆 | Heaps](https://www.yuque.com/xianyuxuan/coding/fpxegv?view=doc_embed)



#### 3.2 ☆ set & map & multiset & multimap | Associative containers
> `std::set`是唯一、有序元素的集合，这里用红黑树实现。
> `std::map`是键值对的集合，键唯一、有序，这里用红黑树实现。
> `std::multiset`和`std::multimap`分别是它们的可重版本，即键不唯一。

这四种数据结构是可以遍历的，且遍历时也是有序的。


##### 3.2.1 set & multiset
#include <set>

- 构造：`set<int> s;` 或 `multiset<int> s;`
   - 也可以类似 priority_queue 用数组等构造，复杂度是 ![](https://cdn.nlark.com/yuque/__latex/391e48baddd4a41ffd6ef700a6507116.svg#card=math&code=O%28N%5Clog%20N%29&id=Qcjmv)的
   - 也可以自定义比较函数：`auto cmp = [](int a, int b) { return ... };  std::set<int, decltype(cmp)> s(cmp);`
- 插入：`s.insert(3);`，复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=COYRn)的
- 删除：`s.erase(2)`，返回删除了多少个，复杂度是![](https://cdn.nlark.com/yuque/__latex/92c6f275db17cb145b7c5b3f292706b5.svg#card=math&code=O%28%5Clog%20N%20%2B%20k%29&id=GMizr)的，![](https://cdn.nlark.com/yuque/__latex/df976ff7fcf17d60490267d18a1e3996.svg#card=math&code=k&id=N7oDV)是找到的个数
- 计数：`s.count(3)`，返回有多少个对应元素，复杂度是![](https://cdn.nlark.com/yuque/__latex/92c6f275db17cb145b7c5b3f292706b5.svg#card=math&code=O%28%5Clog%20N%20%2B%20k%29&id=f6RwO)的，![](https://cdn.nlark.com/yuque/__latex/df976ff7fcf17d60490267d18a1e3996.svg#card=math&code=k&id=ISojx)是找到的个数
- 查找：`s.find(2)`，返回一个值相等的元素的迭代器，如果没找到，返回`s.end()`。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=hskg8)的
- 也有 `s.lower_bound(2)`、`s.upper_bound(3)`函数。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=t8sJM)的


##### 3.2.2 map
#include <map>

- 构造：`map<int, string> s;`
   - 附注同 set & multiset
- 访问或新建：`s[1]`，如果 key`1`存在则返回对应 value 的引用，否则插入 key 为`1`，value 为对应类型默认值的键值对，并返回 value 的引用。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=VMc0Q)的
   - 也就是说，可以直接用 `s[1] = "123"`的方式新建键值对或者覆盖已有的，无论 key `1`之前是否存在。
   - 下面两个并不常用：
   - 插入：`s.insert({1, "123"});`，如果 key `1`已经存在则不会覆盖。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=TfrAC)的
   - 访问：`s.at(1)`，如果 key`1`存在则返回对应 value 的引用，否则抛出异常。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=VH3N8)的
- 删除：`s.erase(2)`，返回删除了多少个，复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=yu1Ns)的
- 计数：`s.count(3)`，返回有多少个 key 相等的元素，复杂度是![](https://cdn.nlark.com/yuque/__latex/ffe609a7d24cc2f7004a3ff72d12dd39.svg#card=math&code=O%28%5Clog%20N%0A%29&id=CX09U)
- 查找：`s.find(2)`，返回 key 相等的元素的迭代器，如果没找到，返回`s.end()`。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=Aacfe)的
- 也有 `s.lower_bound(2)`、`s.upper_bound(3)`函数。复杂度是![](https://cdn.nlark.com/yuque/__latex/42433fa38a5bb64ddbf13bc74baefea6.svg#card=math&code=O%28%5Clog%20N%29&id=Kk8Bt)的


#### 3.2.3 multimap
#include <map><br />不太常用，暂略！

> See Also：
> - 红黑树：[平衡搜索树 | Balanced Search Tree](https://www.yuque.com/xianyuxuan/coding/bgc8rm?view=doc_embed)



#### 3.3 ☆☆ unordered_set  & unordered_map | Unordered associative containers
> `std::unordered_set`和`std::unordered_map`分别是`std::set`和`std::map`的无序版本，即键不经过排序。这里用哈希实现。

这两种数据结构也是可以遍历的。

#include <unordered_set><br />#include <unordered_map>

成员函数与 set 和 map 类似，但是因为无序所以没有`lower_bound`和`upper_bound`。<br />同时由于是使用哈希实现的，因此插入、删除、访问、查找的平均复杂度均为![](https://cdn.nlark.com/yuque/__latex/a2006f1ac61cb1902beacb3e29fff089.svg#card=math&code=O%281%29&id=LBApd)。因此，在没有排序需求时可以首选这两个容器。

> See Also：
> - 哈希（乌乌我没有笔记）

（也有 unordered_multiset 和 unordered_multimap，但是好像不怎么常用）


### 4 结语
事实上，在做力扣周赛和各种笔面试的算法题的过程中，我自己会用到的 C++ 层面上能提供的帮助大概也就上面这些；其中还有相当一部分是可以自己简单实现的。而做出题目的关键更多还是靠算法的设计。我本身也没有做过多少题，目前的水平也是在尝试在周赛中能稳定做出三题，感觉基础算法、思路和见识方面还有很多欠缺。整理上面这些内容，也希望能给自己和读者（如果有）带来一点点帮助！<br />也欢迎大家互相交流、互相 push 做题预防老年痴呆，同时也请力所能及的大小朋友们来鱼肆周报写写东西QWQ！感谢大家~<br />P.S.  如果有其他好用的东西可以在评论区分享 ~
