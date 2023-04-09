---
title: Week 5 - 模板 (I) - 基础知识与 STL 使用
verticalSeparator: ===
revealOptions:
  width: 1600
  height: 900
  margin: 0.04
  transition: 'fade'
  slideNumber: true
---

<link rel="stylesheet" href="custom_light.css">
<link rel="stylesheet" href="../custom_light.css">
<link rel="stylesheet" href="custom.css">
<link rel="stylesheet" href="../custom.css">

# 探索 C++

<br>

## Week 5 - 模板 (I) 基础知识与 STL 使用

---

## 后续一部分的内容安排

- 模板 (I): 核心目标是让大家能用 STL，针对此目标，引入并介绍必要的模板知识
- 模板 (II): 详细讨论 STL 的设计理念，理解泛型<!-- .element: class="fragment" -->
  - 到这里，预期大家能够具备只看 cppreference 就会用 STL 的能力<!-- .element: class="fragment" -->
- 右值引用与移动语义: 现代 C++ 的最后一座大山 (?)<!-- .element: class="fragment" -->
  - 到这里，预期大家能够具备只看 cppreference 就能看懂大多数内容的能力<!-- .element: class="fragment" -->
- 模板 (III): 关于模板的更多常见话题<!-- .element: class="fragment" -->
- 类 (IV): 继承、(运行时) 多态<!-- .element: class="fragment" -->
- 模板 (IV): 关于模板的高级话题<!-- .element: class="fragment" -->

---

## 7.1 泛型编程

===

```c++
struct node {
    elem* val;
    struct node* next;
};
typedef struct node* linkedlist;

linkedlist create();
int size(linkedlist llist);
elem* get(linkedlist llist, int index);
void add(linkedlist llist, elem val);
// ...
```

===

```c++
struct node {
    elem* val;
    struct node* next;
};

struct linkedlist {
    struct node* llist;

    static linkedlist create();
    int size() const;
    elem* get(int index) const;
    void add(elem val);
    // ...
};
```

===

我们的需求实际上是：让我们的代码独立于具体的类型 (type-independently) 工作

我们写出一个适用于所有类型的数据结构（类）或者算法（函数）

在真正需要使用时，生成一个适用于所需要类型的实例

===

这种编程范式称为 **泛型编程 (generic programming)**

也就是说，在泛型的代码中，我们编写的并不是一个具体的类 / 函数，而是函数 / 类的一个族 (family)

或者说，我们定义了一种生成类 / 函数的模式。

===

```c++
#define elem Circle
#include "linkedlist.h"
#undef elem

#define elem Rectangle
#include "linkedlist.h"
#undef elem
```

![](2023-04-02-13-19-08.png)

===

我们当时的解决方案是，用一个 `Shape` 类作为它们的基类，然后 `using elem = Shape;` 即可

假如我们确实要维护两个不同类型的链表怎么办呢？比如需要分别维护一个 `int` 类型和 `double` 类型的链表

===

给这两个类型也找一个共同的基类——或者说，给所有类型找一个共同的基类；所有容器类（例如这里的 `linkedlist` 或者我们之前设计的 `Container`）都可以使用这个基类作为其 `elem`

这种组织方式叫做 **单根结构 (singly rooted hierarchy)**

很多面向对象的编程语言（如 Java）都使用单根结构

`Object` https://docs.oracle.com/javase/7/docs/api/java/lang/Object.html

C++ 并没有采用单根结构

===

`abs.h`

```c++
TYPE abs(TYPE x) { return x > 0 ? x : -x; }
```

`main.cpp`
```c++ title="main.cpp"
#define TYPE int
#include "abs.h"
#undef TYPE

#define TYPE double
#include "abs.h"
#undef TYPE

int main() {
    int x = abs(-1);
    double y = abs(-1.0);
}
```

`g++ main.cpp -E > main.i`

===

`main.i`

```c++ title="main.i"
# 0 "main.cpp"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "main.cpp"

# 1 "abs.h" 1
int abs(int x) { return x > 0 ? x : -x; }
# 3 "main.cpp" 2



# 1 "abs.h" 1
double abs(double x) { return x > 0 ? x : -x; }
# 7 "main.cpp" 2


int main() {
    int x = abs(-1);
    double y = abs(-1.0);
}
```

===

```c++ title="main.cpp"
#define TYPE int
#include "container.h"
#undef TYPE

#define TYPE double
#include "container.h"
#undef TYPE

int main() {
    Container_int ci;
    Container_double cd;
}
```

===

```c++ title="main.i"
class Container_int {
    int * val;
};
class Container_double {
    double * val;
};

int main() {
    Container_int ci;
    Container_double cd;
}
```

===

`Container_TYPE` ?

`#define a 1`

`int total = 1;` => `int tot1l = 1;` ?

===

```c++ title="container.h"
#if defined(TYPE)
#define JOIN_(a, b) a ## b
#define JOIN(a, b) JOIN_(a, b)
#define NAME JOIN(Container_, TYPE)

class NAME {
    TYPE * val;
};

#undef JOIN_
#undef JOIN
#undef NAME
#endif
```

===

希望 C++ 能够「允许用语言本身表达所有重要的东西，而不是在注释里或者通过宏这类黑客手段」

===

Release 3.0 中，C++ 受 Ada 的启发加入了 **模板 (template)** 机制来解决这一问题

模板将 **泛型编程 (generic programming)** 和 **模板元编程 (template metaprogramming)** 这两个编程范式引入了 C++，它们在现在发挥着非常重要的作用

---

## 7.2 模板和隐式实例化

===

### 7.2.1 隐式实例化

类模板独立于具体的类型，它定义的是一种根据给定的参数生成类的规则

类模板本身不是一个类，仅包含模板定义的源文件不会生成任何代码<!-- .element: class="fragment" -->

当我们要使用这样的模板时，我们应当给出其参数，编译器会根据参数和模板生成出一个实际的类<!-- .element: class="fragment" -->

<div class="fragment">

这个类为对应模板的一个 **特化 (specialization)** ；这个过程叫做模板的 **实例化 (instantiation)**

</div>

===

![](2023-04-09-10-40-55.png)

===

按需实例化：当我们需要使用一个完整类型时，隐式的实例化会发生

```c++
Container<char>* p;     // nothing is instantiated here

void foo() {
    (*p)[2] = 'c';  // implicit instantiation of Container<char> 
                    // and Container<char>::operator[](unsigned) occurs here.
                    // Container<char>::~Container() is never needed
                    // so is never instantiated: it doesn't have to be defined
}
```

===

```c++ linenums="1"
// template definition: abs is a function template
template<typename T> T abs(T x) { return x > 0 ? x : -x; }

int main() {
    // instantiates and calls abs<int>(int)
    int x = abs<int>(-1);
}
```

===

![](2023-04-09-10-42-20.png)

===

```c++ linenums="1"
// template definition: abs is a function template
template<typename T> T abs(T x) { return x > 0 ? x : -x; }

int main() {
    // instantiates and calls abs<int>(int)
    int x = abs<int>(-1);
    // instantiates and calls abs<double>(double), template argument deduced
    double y = abs<>(-1.0);
    // instantiates and calls abs<float>(float), template argument deduced
    float z = abs(-2.0f);
}
```

===

模板的实例化必须 **知道** 每个模板参数，但是这并不意味着每个参数都需要由调用者 **指定**

如果可能，编译器会从函数参数中推断出没有明确给出的模板参数

这一机制叫做 **模板参数推导 (template argument deduction)**

===

### 7.2.2 函数模板参数推导

```c++ linenums="1"
template<typename To, typename From>
To convert(From f);
 
void g(double d) 
{
    int i = convert<int>(d);    // calls convert<int, double>(double)
    char c = convert<char>(d);  // calls convert<char, double>(double)
    int(*ptr)(float) = convert; // instantiates convert<int, float>(float) 
                                // and stores its address in ptr
}
```

===

```c++
template<typename To, typename From>
To convert(From f);

void g(double d) {
    int i = convert(d);
}
```

`no matching function for call to 'convert'`，因为 `couldn't infer template argument 'To'`。

===

`double y = abs<double>(1.0f);`

`double y = abs<double>(double(1.0f));`

===

类型推导不考虑隐式转换

因为隐式类型转换发生在重载解析过程中，而模板参数推导发生在重载解析之前

```c++ linenums="1"
template<typename T> 
T greater(const T& lhs, const T& rhs) {
    return rhs > lhs ? rhs : lhs;
}

void foo(int a, double b) {
    // double x = greater(a, b); // error
    double x = greater<double>(a, b); // OK
}
```

===

### 7.2.3 运算符模板

===

```c++ linenums="1"
template<typename T>
class Container {
    T* data;
    unsigned size = 0, capa;
public:
    Container(unsigned capa = 512) : data(new T[capa]), capa(capa) {}
    ~Container() { delete[] data; }

    T& operator[](unsigned index) { return data[index]; }
    const T& operator[](unsigned index) const { return data[index]; }

    unsigned getSize() const { return size; }
    unsigned getCapa() const { return capa; }

    Container & add(T val) { 
        /* if full, expand storage */
        data[size++] = val;
        return *this; 
    }
    // ...
};

#include <iostream>
using std::cout;
using std::ostream;

template<typename T>
ostream & operator<<(ostream& os, const Container<T>& c) {
    for (unsigned i = 0; i < c.getSize(); i++)
        os << c[i] << ' ';
    return os;
}

int main() {
    Container<int> c(10);
    c.add(1).add(2).add(3).add(5);
    cout << c;
}
```

===

> https://godbolt.org/z/87fezqvb5

> https://godbolt.org/z/3845W6Wdf

===

```c++ linenums="1"
template<typename T>
class Container {
    T* data;
    unsigned size = 0, capa;
public:
    Container(unsigned capa = 512) : data(new T[capa]), capa(capa) {}
    ~Container() { delete[] data; }
    Container(const Container &) = delete;
    Container & operator=(const Container &rhs) {
        if (this == &rhs)   return *this;
        if (capa != rhs.capa) {
            delete[] data;
            data = new T[rhs.capa];
        }
        for (unsigned i = 0; i < rhs.size; i++)
            data[i] = rhs[i];
        capa = rhs.capa;
        size = rhs.size;
        return *this;
    }

    T& operator[](unsigned index) { return data[index]; }
    const T& operator[](unsigned index) const { return data[index]; }

    unsigned getSize() const { return size; }
    unsigned getCapa() const { return capa; }

    Container & add(const T& val) { 
        /* if full, expand storage */
        data[size++] = val;
        return *this; 
    }
    // ...
};

#include <iostream>
using std::cout;
using std::ostream;

template<typename T>
ostream & operator<<(ostream& os, const Container<T>& c) {
    os << '[';
    for (unsigned i = 0; i + 1 < c.getSize(); i++)
        os << c[i] << ' ';
    if (c.getSize())
        os << c[c.getSize() - 1];
    return os << ']';
}

int main() {
    Container<Container<int>> c(10);
    c.add(Container<int>(10)).add(Container<int>(10)).add(Container<int>(10));
    c[0].add(1).add(2).add(3).add(5);
    c[1].add(4).add(5);
    cout << c;
}
```

===

`Container<Container<int>>`

`Container< Container<int> >`

===

### 7.2.4 默认模板参数

我们之前讨论过，函数参数可以有默认参数；事实上，模板参数也可以有默认参数。例如：

```c++
template<typename T, typename U = int> class Foo { /* ... */ };

Foo<int> x;         // Foo<int, int>
Foo<int, char> y;   // Foo<int, char>
// Foo<> z;  Foo w; // Error
```

===

与函数参数一样，类模板默认参数也只能存在于最后的若干参数中，即 `template<typename T = int, typename U> class Bar { /* ... */ };` 是非法的。

===

不过，由于函数模板通常有模板参数推导，因此函数模板的默认参数 **不必** 只能存在于最后的若干参数中，例如；

```c++
template<typename RT = void, typename T>    // OK
RT* address_of(T& value) { return (RT*)(&value); }

void foo(int x) {
    void * pv = address_of(x);		// address_of<void, int>
    int * pi = address_of<int>(x);	// address_of<int, int>
}
```

===

另外，如果模板参数既有默认参数也可以推导出来，则使用推导出来的结果（除非推导失败），例如：

```c++
template<typename T = int>  void foo(T x) {}

void bar(double x) {
    foo(x); // foo<double>
}
```

===

### 7.2.5 模板成员

我们之前看到了类模板，例如：

```c++
template<typename T> class Container {
    // ...
    Container & operator=(const Container &rhs);
};
```

===

如果我们想在类外写这个成员函数的定义，我们需要这样写：

```c++
template<typename T>
Container<T> & Container<T>::operator=(const Container<T> &rhs) { /* ... */ }
```

原因很简单，`Container<T>` 是一个类，而 `Container` 不是。

===

类也可以有模板成员。例如：

```c++
#include <iostream>

struct Printer {
    std::ostream& os;
    Printer(std::ostream& os) : os(os) {}
    template<typename T>
    void print(const T& obj) { os << obj << ' '; } // member template
};

int main() {
    Printer p(std::cout);
    p.print(1);   // instantiates and calls p.print<int>(1), prints 1
    p.print('a'); // instantiates and calls p.print<char>('a'), prints a
}
```

===

如果我们希望把 `Printer::print` 放到类外来定义，那么它会写成：

```c++
template<typename T>
void Printer::print(const T& obj) { /* ... */ }
```

===

```c++
template<typename T> class Container {
    // ...

    template<typename U>
    Container & operator+=(const Container<U> & rhs);
};

template<typename T>    // for the enclosing class template
template<typename U>    // for the member template
Container<T> & Container<T>::operator+=(const Container<U> & rhs) {
    for (unsigned i = 0; i < size && i < rhs.getSize(); i++) {
        data[i] += rhs[i];
    }
    while (size < rhs.getSize()) {
        data[size] = rhs[size];
        size++;
    }
    return *this;
}
```

---

## 7.3 STL 基本使用

<br>

#### Standard Template Library, 标准模板库

===

### 7.3.1 为什么要用 STL

<br>

<center>因为好用！</center>

===

```c++
#include <iostream>
#include <vector>

int main()
{
    // Create a vector containing integers
    std::vector<int> v;

    // Add two integers to vector
    v.push_back(25);
    v.push_back(13);

    // Print out the vector
    std::cout << "v = { ";
    for (auto n : v)
        std::cout << n << ", ";
    std::cout << "}; \n";
}
```

`auto`, range-based for loop

===

```c++
#include <algorithm>
#include <iostream>
#include <vector>

int main()
{
    using std::vector;
    using std::cout;
    using std::endl;

    int s[] = {5, 7, 4, 2, 8, 6, 1, 9, 0, 3};
    vector<int> v = {5, 7, 4, 2, 8, 6, 1, 9, 0, 3};

    std::sort(s, s + 10);
    for (int i : s) 
        cout << i << " ";
    cout << endl;

    std::sort(v.begin(), v.end(), std::greater<int>());
    for (int i : v) 
        cout << i << " ";
    cout << endl;
}
```

===

```c++
bool cmp(const int& a, const int& b) { return a > b; }
vector<int> v = {3, 1, 4, -2, 5, 3};
sort(v.begin(), v.end(), cmp);
```

===

```c++
bool cmp(const vector<int>& a, const vector<int>& b) {
    return a[0] == b[0] ? a[1] < b[1] : a[0] < b[0];
}

void foo(vector<vector<int>> & foo) {
    sort(foo.begin(), foo.end(), cmp);
}
```

===

### 7.3.2 STL 都有什么

<br/>

- [Containers library](https://en.cppreference.com/w/cpp/container)
- [Algorithms library](https://en.cppreference.com/w/cpp/algorithm)

<br/><br/>

> 本节中部分图片取自 Bob Steagall 在 CppCon 2021 的演讲 Back to Basics: Classic STL

===

#### Containers library

===

<img src="2023-04-07-01-24-04.png" width="50%">

===

<img src="2023-04-07-01-26-56.png" width="80%">

===

<img src="2023-04-07-01-30-35.png" width="80%">

===

<img src="2023-04-07-01-32-52.png" width="50%">

===

#### Algorithms Library

===

**Non-modifying sequence operations**

- `auto it = std::find(v.begin(), v.end(), 3);`
- `int n = std::count(v.begin(), v.end(), 3);`
- `int n = std::count_if(v.begin, v.end(), [](int i) { return i % 4 == 0; });`
- `std::for_each(v.begin(), v.end(), [](int &n){ n *= 2; });`

`auto`: 该变量的类型由其初始化器的类型推导

`[](/* para list */){/* func body */};`: lambda 表达式，「匿名函数」

===

**Modifying sequence operations**

- `std::reverse(v.begin(), v.end());`
- `std::fill(v.begin(), v.end(), -1);`

===

**Partitioning operations**

```c++
#include <algorithm>
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    std::cout << "Original vector: ";
    for (int elem : v)
        std::cout << elem << ' ';
 
    auto it = std::partition(v.begin(), v.end(), [](int i){
        return i % 2 == 0;
    });
 
    std::cout << "\nPartitioned vector: ";
    auto print = [](int x){ std::cout << x << ' '; };
    std::for_each(v.begin(), it, print);
    std::cout << "* ";
    std::for_each(it, v.end(), print);
}

/* Output:
Original vector: 0 1 2 3 4 5 6 7 8 9 
Partitioned vector: 0 8 2 6 4 * 5 3 7 1 9
*/
```

===

**Sorting operations**

- `std::sort(v.begin(), v.end(), std::greater<int>());`
- `std::stable_sort(v.begin(), v.end());`
- `std::partial_sort(v.begin(), v.begin() + 5, v.end());`

===

**Binary search operations** (on sorted ranges)

- `bool res = std::binary_search(v.begin(), v.end(), 4);`
- `auto upper = std::upper_bound(data.begin(), data.end(), 5);`
- `auto lower = std::lower_bound(data.begin(), data.end(), 5);`

![](2023-04-07-17-08-09.png)

===

**Other operations on sorted ranges**

```c++
#include <algorithm>
#include <iostream>
#include <vector>
 
template<class Iter>
void merge_sort(Iter first, Iter last)
{
    if (last - first > 1)
    {
        Iter middle = first + (last - first) / 2;
        merge_sort(first, middle);
        merge_sort(middle, last);
        std::inplace_merge(first, middle, last);
    }
}
 
int main()
{
    std::vector<int> v {8, 2, -2, 0, 11, 11, 1, 7, 3};
    merge_sort(v.begin(), v.end());
    for (auto n : v)
        std::cout << n << ' ';
    std::cout << '\n';
}

// Output: -2 0 1 2 3 7 8 11 11
```

===

**Set operations** (on sorted ranges)

- `std::includes`
- `std::set_difference`
- `std::set_intersection`
- `std::set_symmetric_difference`
- `std::set_union`

===

**Minimum/maximum operations**

- `int maxn = std::max(a, b);`
- `int maxn = std::max({a, b, c, d});`
- `auto it = std::max_element(v.begin(), v.end());`

===

**Heap operations**

- `std::make_heap(v.begin(), v.end());`
- `std::pop_heap(v.begin(), v.end()); int top = v.back();`
- `v.push_back(6); std::push_heap(v.begin(), v.end());`

===

**Comparison operations**

- `bool res = std::equal(a.begin(), a.end(), b.begin());`
- `bool res = std::lexicographical_compare(v1.begin(), v1.end(), v2.begin(), v2.end());`

```c++
bool is_palindrome(const std::string& s)
{
    return std::equal(s.begin(), s.begin() + s.size() / 2, s.rbegin());
}
```

===

**Permutation operations**

```c++
#include <algorithm>
#include <iostream>
#include <string>
 
int main()
{
    std::string s = "aba";
    std::sort(s.begin(), s.end());
 
    do std::cout << s << '\n';
    while (std::next_permutation(s.begin(), s.end()));
}

/* Output:
aab
aba
baa
*/
```

===

常用的部分我们在 [快速入门 C++ 写题](../../cpp_for_contests) 有所介绍

大家也可以在 Week6 结束后，自行阅读网页中的内容，查阅这些算法

其中关于 C++20 引入的 `ranges` namespace 下的算法版本，我们会在后面的章节中具体介绍其背景和动机；大家可以暂时先行跳过

---

## Takeaway

- 泛型编程
  - 定义一种生成类 / 函数等的模式
  - 单根结构
  - 用 C 的实现
- 模板
  - 动机：写出泛型的类来实现容器
  - 特化与实例化
  - 按需产生的隐式实例化
  - 模板参数推导
  - 运算符模板
  - 默认模板参数
  - 模板成员

===

## Takeaway

- STL
  - `std::vector` 和 `std::sort` 的简单使用
  - `auto`
  - range-based for loop
  - STL 里都有什么
  - [快速入门 C++ 写题](../../cpp_for_contests)