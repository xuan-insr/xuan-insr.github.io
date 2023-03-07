### 默认参数

这样的构造函数允许用户传递一个初始大小，然后直接开一个对应大小的空间：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
public:
    Container(unsigned size) {
        val = (elem*)malloc(sizeof(elem) * size);
        // ...
    }
    // ...
};
```

那么，假如我们希望用户既可以给定大小，也能够在不知道要开多大的情况下使用一个默认大小，怎么办呢？C++ 在函数声明中支持 **默认参数 (default arguments)**，用来允许函数可以以省略末尾的若干参数的方式调用：

```c++
void point(int x = 3, int y = 4);
 
point(1, 2); // calls point(1, 2)
point(1);    // calls point(1, 4)
point();     // calls point(3, 4)
```

默认参数必须出现在末尾的若干个参数中。这个要求的合理性容易理解：假如没有这个要求，那么如果有 `void point(int x = 3, int y);`，则 `point(4);` 的含义是容易让人迷惑的。

因此，`Container` 类的构造函数可以写成：

```c++ linenums="1" hl_lines="5"
class Container {
    elem* val;
    // ...
public:
    Container(unsigned size = 512) {
        val = (elem*)malloc(sizeof(elem) * size);
        // ...
    }
    // ...
};
```

这样，就可以使用 `Container c1;` 构造一个默认大小 (512) 的容器，或者用 `Container c2(64);` 构造一个自定义大小的容器了。前者实际上是 `Container(512)`，而后者是 `Container(64)`。

??? info "补充"
    对于非模板函数，如果已声明的函数在 **同一作用域** 中重新声明（在内部作用域内的重新声明会出发作用域屏蔽），则可以向该函数添加默认参数。在函数调用时，默认值是该函数所有可见声明中提供的默认值的并集。对于默认值已经可见的参数，重新声明不能引入默认值（即使值相同）。

    ```c++
    void f(int, int);     // #1 
    void f(int, int = 7); // #2 OK: adds a default
    
    void h()
    {
        f(3); // #1 and #2 are in scope; makes a call to f(3,7)
        void f(int = 1, int); // Error: inner scope declarations don't acquire defaults
    }
    ```

    带默认参数的友元函数声明必须是一个定义，且 translation unit 中不能有其他声明。

    默认参数不允许使用局部变量，除非它们 not evaluated（比如 `sizeof n`，参见 std notes 6.3）。

    除了函数调用运算符 `operator()` 之外的运算符重载不能有默认参数。

### 函数重载

那么，假如我希望根据是否传入某个参数来选择不同的构造函数，怎么办呢？例如我们希望 `Container` 的构造函数长这样：

```c++
Container::Container(unsigned size, elem initVal) {
    val = (elem*)malloc(sizeof(elem) * size);   // allocate memory
    for (unsigned i = 0; i < size; i++) {       // set init values
        val[i] = initVal;
    }
}
```

但是！我们希望如果没有传入 `initVal`，就不要做那个 set init values 的循环怎么办呢？固然我们可以通过默认参数结合判断来实现，但是假如我们可以根据不同的传入参数来使用不同的构造函数就更好了！

事实上，C++ 支持这样的操作，这被称为 **函数重载 (function overloading)**：

```C++
class Container {
    elem* val;
    // ...
public:
    Container() { val = nullptr; }
    Container(unsigned size) {
        val = (elem*)malloc(sizeof(elem) * size);
    }
    Container(unsigned size, elem initVal) {
        val = (elem*)malloc(sizeof(elem) * size);
        for (unsigned i = 0; i < size; i++) {    
            val[i] = initVal;
        }
    }
};
```

这样，当我们使用 `Container c1, c2(4), c3(6, 2);` 定义三个对象时，它们会分别使用无参、一个参数和两个参数的构造函数：

<center>![](2023-03-03-14-45-31.png)</center>

事实上，不仅是构造函数支持重载，其他的成员函数或者独立的函数[^namespace-scope]也支持重载。例如^[over.pre#2](https://timsong-cpp.github.io/cppwp/n4868/over.pre#2)^：

```c++
double abs(double);
int abs(int);

abs(1);             // calls abs(int);
abs(1.0);           // calls abs(double);
```

[^namespace-scope]: 准确地说，函数可以在 namespace scope 或者 class scope 被定义。这里没有引入 namespace 的概念所以暂时不用这个术语。

如果一个名字引用多个函数，则称它是 overloaded 的。当使用这样的名字的时候，编译器用来决定使用哪个；这个过程称为 **重载解析 (overload resolution)**。简单来说，重载解析首先收集这个名字能找到的函数形成候选函数集 (candidate functions)，然后检查参数列表来形成可行函数集 (viable functions)，然后在可行函数集中按照一定的规则比较这些函数，如果 **恰好** 有一个函数 (best viable function) 优于其他所有函数，则重载解析成功并调用此函数；否则编译失败。

上面的「规则」比较复杂[^overload_resolution]，但是一个简单的例子是，不需要类型转换的比需要的要好[^rank_of_conversion]：

<center>![](2023-03-03-16-03-41.png)</center>

因此，上面第 5 行的 `f(0L);` 中 `0L` 是 `long` 类型的字面量，它调用 `void f(long)` 不需要转换，而调用 `void f(float)` 需要转换，因此选取前者。

但是，上面第 6 行的 `f(0);` 中 `0` 是 `int` 类型的字面量，它调用两个函数都需要转换，且两个转换没有一个优于另一个[^rank_of_conversion]，因此找不到 best viable function，因此编译错误。

[^overload_resolution]: [Overload Resolution](https://en.cppreference.com/w/cpp/language/overload_resolution), [over](https://timsong-cpp.github.io/cppwp/n4868/over)

[^rank_of_conversion]: 事实上，转换有三个等级，分别是 exact match, promotion 和 conversion。这里 int->long 和 int->float 都属于 conversion。参见[Ranking of implicit conversion sequences](https://en.cppreference.com/w/cpp/language/overload_resolution#Ranking_of_implicit_conversion_sequences)

也是因此，两个只有返回值类型不同的函数不是合法的重载，因为调用时没有办法完成重载解析：

```c++
int f(int a);
void f(int a);  // error: functions that differ only in 
                // their return type cannot be overloaded
```

我们会在后面的章节具体讨论重载解析的细节。

!!! note "nullptr"
    我们在前面的章节看到了 `nullptr`，这是 C++11 引入的一个关键字，用来表示空指针。

    为什么要引入这个东西呢？我们首先要提到一个事实：为了类型安全，C++ 不允许 `void*` 隐式转换到其他指针类型。因此，如果我们将 `NULL` 定义为 `(void*) 0`，那么 `int * p = NULL;` 会引发编译错误：

    <center>![](2023-03-03-16-20-49.png)</center>

    （这是 C++ 与 C 不兼容的例子之一。）

    既然 C++ 不允许将 `(void*) 0` 当空指针，那么我们用什么表示空指针呢？在 C++11 之前，空指针常量 (null pointer constant) 是值为 0 的整型字面量^[conv.ptr#1](https://timsong-cpp.github.io/cppwp/n4868/conv.ptr#1)^。

    因此，如果我们将 `NULL` 定义为 `0`，则 `int * p = NULL;` 即 `int * p = 0;` 是合法的（赋值成其他整数是不合法的）。

    但是！问题来了——

    ```c++
    void f(int *);
    void f(int);

    #define NULL 0
    f(NULL);   // ==> f(0) , so f(int) is called
    ```

    可以看到，重载使得上面的情况可能引起误解，造成意料之外的结果。

    因此，C++11 引入了 `nullptr` 来表示空指针常量。这样就解决了上面的问题：

    ```c++
    void f(int *);
    void f(int);

    f(nullptr);   // f(int *) is called
    ```

    因为 null pointer constant 可以转换到任意指针类型^[conv.ptr#1](https://timsong-cpp.github.io/cppwp/n4868/conv.ptr#1)^。

    当然，为了兼容，值为 0 的整型字面量仍然是空指针常量。

考虑函数重载和默认参数共同使用的情况，事实上仍然能通过上面「重载解析」的方式处理：

```c++
void f(int i = 1);
void f();

void foo() {
    f(1);   // OK, call the first one
    f();    // Error: ambiguous
}
```

不过我们可能会发现，函数重载的作用已经足以覆盖默认参数的作用。事实上确实如此：默认参数机制在 C with Classes 时就存在了，其意义就是前面给出的构造函数中默认参数的例子；而一般的函数重载直到 Release 1.0 才被引入。默认参数机制是重载机制的前驱之一；重载机制的另一个前驱是 `operator =` 的重载，我们会在后面的章节看到它。