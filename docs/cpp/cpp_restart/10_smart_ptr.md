# 10 智能指针

!!! info "本节录播地址"
    本节的朋辈辅学录播可以在 [B 站](https://www.bilibili.com/video/BV1Uo4y1g7tH/?spm_id_from=333.788&vd_source=c5a9383e47adf0fdb6896be9dbbc50fc) 找到！

!!! success "特别感谢 @atditto 根据录播内容整理了本文文档！"

!!! info "本节部分内容来自以下演讲"
    - [Back to Basics: C++ Smart Pointers - David Olsen - CppCon 2022](https://youtu.be/YokY6HzLkXs)
    - [CppCon 2014: Herb Sutter "Back to the Basics! Essentials of Modern C++ Style"](https://youtu.be/xnqTKD8uD64)
    - [Back to Basics: Templates (part 1 of 2) - Bob Steagall - CppCon 2021](https://youtu.be/XN319NYEOcE)

## 补充：模板的显式特化与偏特化

!!! danger
    参见录播，后续会补充在 模板 (I) 中。

## 10.1 动机

在讲智能指针之前，我们先要来看看指针有什么问题。

### 问题 1：指针指向的内存何时释放

看这样一个函数，我们尝试发现其中的问题：

```c++ linenums="1"
void science(double* data, int N) {
    double* temp = new double[N*2];
    do_setup(data, temp, N);
    if (!needed(data, temp, N))
        return;
    calculate(data, temp, N);
    delete[] temp;
}
```

??? info "数组和指针的区别" 
    我们说，一个数组 `double arr[N]`，即一个 `double[N]` 类型的变量 `arr`，事实上包含了 3 部分信息：
    
    1. 数组的基地址 (`&arr[0]`)
    2. 数组的元素类型 (`double`)
    3. 数组的元素个数 (`N`)
    
    上面的函数接受一个 `double *` 和一个 `int`，这些参数其实有可能表示了一个叫 `data` 的数组。我们把这个数组的基地址传进来，相当于发生了 array `double[N]` 到 pointer `double*` 的转换。但这么做我们丢失了这个数组有多少个元素的信息，所以我们用这个额外的参数 `N` 把这个信息传进来了。

    当然，这个函数也有可能是接受了一个 `new double[N]` 开出来的数组。

这个函数在最开头 `new` 了一个类型为 `double` 的数组，做了一些前期的准备，然后判断需不需要计算。如果不需要计算的话，函数返回。如果需要计算的话就计算，计算后 `delete` 这个不再用的 `temp`。

但是，如果这个 `if` 的条件为真，它直接 `return`，`new` 出来的这个 `temp` 没有被释放。

也就是说，为了避免这个问题，我们应该对这个函数的每一个出口都要把他申请过的所有的资源全部释放一遍，就像这样：

```c++ linenums="1" hl_lines="5 9"
void science(double* data, int N) {
    double* temp = new double[N*2];
    do_setup(data, temp, N);
    if (!needed(data, temp, N)) {
        delete[] temp;
        return;
    }
    calculate(data, temp, N);
    delete[] temp;
}
```

但这种方案比较冗余，容易出错，不便于阅读和维护。

那我们能不能通过某种机制（语言上的机制，或者外面套一层 wrapper 函数），默认在函数结束的时候释放所有指针呢？

注意到这个函数中一共有两个指针 `data` 和 `temp` ，为什么我们释放 `temp` 却不释放 `data` 呢？因为 `temp` 是这个函数里开出来的，这个函数就有责任把它释放。而 `data` 这个东西不是这里开出来的，我们甚至不知道它到底是 `new` 出来的，还是只是一个栈上的或者静态的数组。如果 `delete[]` 了一个栈上的或者静态的数组，或者一个堆上的数组在这里释放了但是外面发生了 use after free 或者 double free，则都是 UB。所以「默认在函数结束的时候释放所有指针」这个机制并不是正确的。

再看一个例子：

```c++ linenums="1"
float* science(float* x, float* y, int N) {
    float* z = new float[N];
    saxpy(2.5, x, y, z, N);
    delete[] x;
    delete[] y;
    return z;
}
```

在这个函数中，有 2 个数组被传入，1 个数组作为返回值被返回。从函数的实现我们容易看出，传入的 `x` 和 `y` 会在函数中被释放，而传出的 `z` 需要有调用者来释放。这两个信息对于调用者来说非常重要，但是这两个信息并没有体现在函数的声明中。

容易理解，正确的方法是，在某个指针的生命周期结束时，我们要根据是否拥有这个指针的 **所有权** 来决定是否释放。但在上面的例子中，所有数组都是 `double*` 或者 `float*` 类型；调用者和函数实现者需要通过注释或者文档来约定这些指针的所有权，这样很容易出错。

这就是指针的第 1 个问题：

我们需要依靠程序员保证指针的正确释放（有且仅有一处完成释放），但是程序员可能会犯错，导致内存泄漏或者 UB。    
我们希望有一种机制，能够自动释放指针，而不需要程序员手动释放。    
这种机制需要能够判断指针是否拥有所有权，但指针类型本身并不包含这种信息。

### 问题 2：指针指向单个对象还是数组

形如 `T*` 的指针可以指向单个对象，也可以指向数组。当它指向单个对象，其实就被视为指向了一个元素大小为一的数组，但是指向单个对象的时候

- 不应该用 `++p` 或 `--p` ，因为它们都会超出边界（数组可以 `++p` 或 `--p` ，但也不能超出边界。超出边界后再去访问数组内容，则属于 UB）。
- 使用 `delete` 释放（数组使用 `delete[]` 释放）

上面例子说明，在 C++ 中，指针类型本身并不包含它指向单个对象还是数组的信息。这意味着编译器无法通过类型信息来判断应该使用 `delete` 还是 `delete[]`。

### 问题 3：指针是否允许为空

我们在编写代码时候经常要判断指针是否为 `nullptr`。如果可以保证某种指针可以永远不为空的话，就可以省去空指针检查，从而提高代码效率。但在 C++ 中，指针类型本身无法表达是否允许为空。 

### 小结：动机和期望

上面三个问题事实上都是一个问题，就是指针本身包含了这么多信息，但是指针们看起来都长 `T*` 这个样子。事实上我们所希望的智能指针的「智能」，就在于要能提供这些信息。

总结一下，我们希望智能指针可以实现：

**「智能」**

- 自动回收资源：在生命周期结束后，智能指针能够自动释放资源
- 知道指向的是单个对象还是数组：智能指针能够根据指针的类型，自动选择 `delete` 还是 `delete[]`
- 增加一些限制：有的时候，可以强制要求智能指针不为空

**「指针」**

- 能像指针一样使用，指向对象、执行间接访问

我们还希望智能指针的实现遵从「单一职责原则」：像前面聊的 `std::string` 一样，隐藏底层的内存管理细节，让程序员专注于业务逻辑的实现，而不必担心内存泄漏或资源管理的问题。

## 10.2 垃圾回收 | GC

我们希望「自动回收资源」，那我们来调研学习一下其他地方是怎么实现的。这个问题就是 **垃圾回收**。我们简单介绍一下垃圾回收的基本概念和常见简单实现。

!!! warning
    GC 并不是本次内容的重点。如果感兴趣，可以在 https://www.iecc.com/gclist/GC-faq.html 上找到更多关于 GC 的信息。

垃圾回收（Garbage Collection）的核心是 **回收「不可达」的对象**。

??? info "如何判断对象的「可达性」"
    当一个对象不能通过任何途径被访问到时，我们称这个对象是「不可达」的。我们可以通过以下几种方式判断对象的「可达性」：

    - **Reference Counting**    
        引用计数的核心思想是为每个对象维护一个**引用计数器**，记录有多少个指针指向该对象。当引用计数为零时，说明没有任何指针指向该对象，因此可以安全地回收该对象的内存。    
        引用计数的优点是实现简单，且可以立即回收不再使用的对象。但它的缺点是：

        - **循环引用问题**：如果两个对象互相引用，它们的引用计数永远不会为零，导致内存泄漏。
        - **性能开销**：每次指针的赋值或析构都需要更新引用计数，可能会带来额外的性能开销。

    - **Mark & Sweep**    
        这是一种更复杂的垃圾回收方式。它的核心思想是从程序的 Root Set（如全局变量、栈上的变量等）开始，递归地标记所有可以访问到的对象。标记完成后，垃圾回收器会清除所有未被标记的对象，回收它们的内存。    
        它的优点是能够处理循环引用问题，但它的缺点是：

        - **暂停时间较长**：标记和清除的过程可能会暂停程序的执行，影响程序的响应速度。
        - **内存碎片问题**：清除过程中可能会产生内存碎片，导致内存利用率下降。

??? info "知道对象「不可达」时，回收多大空间？"
    这个问题是一个 **类型安全** 的问题。尽管从 C 到 C++ 的过程中，做了一些关于类型安全的处理，但由于向前兼容等原因，C++ 仍然不是一门类型安全的语言。例如：

    - `void *`: C 和 C++ 都允许指针到 `void *` 类型的转换，这在损失元素个数的基础上进一步损失了元素类型的信息，导致更不知道该释放多少空间。
    - `union`: `union` 也是一个类型不安全的工具，它可以让一个变量在不同的时间点代表不同的类型，这也会导致不知道该释放多少空间。

??? info "内存回收要考虑的问题"
    - 需要考虑哪些指标？
        - 总体运行时间
        - 碎片
        - 停顿时间
        - Locality
    - 更多考虑
        - 并行 / 并发
        - 类型不安全

## 10.3 `std::unique_ptr`

### 10.3.1 概念
我们首先要讲的第一种智能指针，叫做 `unique_ptr` ，定义在 `<memory>` 头文件中。

 `unique_ptr` 假设自己是对象唯一的所有者，是引用计数的简化版本。

!!! abstract
    `unique_ptr` 是对象的所有者，并假设是唯一的所有者。

    - 这意味着：使用者有义务保证 `unique_ptr` 是对象唯一的所有者
    - 这也意味着：当 `unique_ptr` 被析构时，它可以安全地释放它所拥有的对象
    - 这还意味着：`unique_ptr` 不能被拷贝，只能被移动

### 10.3.2 使用方法

`unique_ptr` 是一个类模板，它的构造函数可以接受一个指针。再次提醒：智能指针只维护堆上的东西，不要把栈上的指针传给他。

```c++
void calculate_more(HelperType&);

ResultType do_work(InputType inputs){
    std::unique_ptr<HelperType> owner( new HelperType(inputs) );
    owner->calculate();
    calculate_more(*owner);
    return owner->important_result();
}
```

可以看到，`unique_ptr` 提供了与普通指针类似的使用方式：

- 成员访问运算符 `->`：用于访问指针所指向对象的成员。
- 间接访问运算符 `*`：用于解引用指针，获取指针所指向的对象。

在 `do_work` 结束时，`owner` 的生命周期结束，`unique_ptr` 会自动释放它所拥有的对象。

`unique_ptr` 也可以放到类里面。我们有一个类里面有个成员 `unique_ptr` ，名字是 owner。那么我们构造的时候，给这个 owner 传一个指针进去用来初始化。

```c++
WidgetBase* create_widget(InputType);

class MyClass {
    std::unique_ptr<WidgetBase> owner;
public:
    MyClass(InputType inputs)
        : owner(create_widget(inputs)) { }
    ~MyClass() = default;
    // ... member functions that use owner-> ...
};
```

`MyClass` 析构时，它也会析构 owner，owner 的析构函数会释放相关资源。所以说我们可以看到 `MyClass` 里面没有必要再去写我们之前说了那五种 SMF，达成了 rule of zero：

- `MyClass` 的析构会自动触发 `owner` 的析构函数
- `MyClass` 的移动构造和移动赋值会自动触发 `owner` 的移动构造和移动赋值
- 由于 `owner` 的的拷贝构造和拷贝赋值是被 `delete` 的，所以 `MyClass` 的拷贝构造和拷贝赋值是被 `delete` 的，所以 `MyClass` 不能被拷贝
    - （回顾上一节的内容：拷贝构造隐式声明被定义为删除，如果该类有无法拷贝构造或析构的非静态成员或基类，或者该类有用户定义的移动构造或移动赋值。拷贝复制类似。）

### 10.3.3 实现思路

我们讨论 `unique_ptr` 的一个简化版本。首先不考虑存储数组的情况，只考虑指向单个对象的情况。

#### 成员类型

```c++
template <typename T>
struct unique_ptr {
    // ...
    using element_type = T;
    using pointer = T*;
    // ...
}
```

指向元素的类型是 `T` ，指针本身的类型是 `T *` 。

#### 构造与析构

```c++
template <typename T>
class unique_ptr {
    T* ptr;
public:
    unique_ptr() noexcept : ptr(nullptr) { }
    explicit unique_ptr(T* p) noexcept : ptr(p) { }
    ~unique_ptr() noexcept { delete ptr; }
    // ...
}
```

有一个不接受指针的默认构造函数，可以发现 `unique_ptr` 是可为空的。有一个注明为 `explicit` 的接受一个指针的构造函数。有一个析构函数。

#### 移动构造与移动赋值

```c++
template <typename T> struct unique_prt{
    // ...
    unique_ptr(unique_ptr const&) = delete;
    unique_ptr& operator=(unique_ptr const&) = delete;

    unique_ptr(unique_ptr&& o) noexcept
        : ptr(std::exchange(o.ptr, nullptr)) { }
    unique_ptr& operator=(unique_ptr&& o) noexcept {
        delete ptr;
        ptr = o.ptr;
        o.ptr = nullptr;
        return *this;
    }
    // ...
}
```

我们可以看到它的拷贝构造和拷贝赋值是被 `delete` 到的，也就是它是不能调用的。
它的移动构造和移动赋值跟前一章讲的类似。当然我们之前说 `unique_ptr` 本身可能是 nullptr，但是我们之前也讲过 delete nullptr 是安全的。

#### 重载运算符

```c++
template <typename T>

struct unique_ptr {

    T& operator*() const noexcept {
        return *ptr;
    }

    T* operator->() const noexcept {
        return ptr;
    }
    // ...
};
```

我们之前没有见过 `->` 运算符重载。事实上 `owner->calculate()` 的语义是 `(owner.operator->())->calculate()`。而 `(owner.operator->())` 返回的是 `ptr`，得到 `ptr->calculate()`。

可以发现 `unique_ptr` 是 `ptr` 的一层 wrapper。但是我们通过重载这样的 `*` 和 `->` 运算符，使得这个 wrapper 实际上是透明的，是可以像原来一样使用的；或者说在函数内联完成之后，这个包装就不存在了。

#### 其他成员函数

```c++
template <typename T>
struct unique_ptr {

    T* release() noexcept {
        T* old = ptr;
        ptr = nullptr;
        return old;
    }

    void reset(T* p = nullptr) noexcept {
        delete ptr;
        ptr = p;
    }

    T* get() const noexcept {
        return ptr;
    }

    explicit operator bool() const noexcept {
        return ptr != nullptr;
    }
};
```

它还有一些其他的成员函数，比如说将所有权转移给其他代码的 `release()`，它释放对当前管理的对象的所有权，并返回指向该对象的指针。

还有重置 `unique_ptr` 管理的对象的 `reset(T* p = nullptr)` ，它释放当前管理的对象并接管新的对象，或者将 `unique_ptr` 设置为空。

类似 `release()` 的 `get()` 只返回指针不释放所有权。

`operator bool()` 判断指针是否为空，这使得智能指针和普通指针一样可以直接用在条件语句中，即隐式转换为 `bool` 类型。

#### 使用时避免直接使用 `new` 和 `delete`

在之前的代码中，我们仍然使用了 `new` 来创建 `unique_ptr` ，但 `delete` 却通过 `unique_ptr` 的析构来自动进行，这导致了 `new` 和 `delete` 不配对。

事实上在 C++14 引入了 `make_unique` 用于创建一个 `unique_ptr`。它 **避免了显式调用 `new`** 并且提供了更好的 **异常安全性**。它长这样：

```c++
template <typename T, typename... Args>
unique_ptr<T> make_unique(Args&&... args);
```

可以这样使用：

```c++
std::unique_ptr<Type> ptr = std::make_unique<Type>(args...);
```

其中 `Type` 是想要创建的对象类型，`args...` 是传递给 `Type` 构造函数的参数。

现代 C++ 中，我们应该尽量避免使用 `new` 和 `delete`，而是使用 `make_unique` 来创建智能指针。

### 10.3.4 数组类型的实现思路

`unique_ptr` 对数组类型的模板参数做了偏特化，使得：

- `unique_ptr<T[]>` 提供了对数组类型的支持，自动调用 `delete[]` 来释放内存。
- `unique_ptr<T[]>` 提供了下标运算符 `operator[]`，可以像使用普通数组一样访问元素。

`make_unique` 也对数组类型做了一些 partial specialization 使得
 
- 可以使用 `make_unique<T[]>(size)` 来创建一个动态数组，其中 `size` 是数组的大小。与普通的 `unique_ptr<T>` 不同，`make_unique<T[]>` 只接受一个参数，即数组的大小，而不接受构造函数参数。这是因为数组类型的 `unique_ptr` 不支持构造函数参数。例如：

```c++
auto ptr = std::make_unique<double[]>(10);
```

### 10.3.5 智能指针实例

让我们回到开头指出指针的问题中的例子。

```c++
void science(double* data, int N) {
    double* temp = new double[N*2];
    do_setup(data, temp, N);
    if (!needed(data, temp, N)) return; // 可能造成内存泄漏
    calculate(data, temp, N);
    delete[] temp;
}
``` 

这个例子错误的原因是这个 `return` 里面没有 `delete`，但是如果我们使用 `unique_ptr` 来代替它的话。

```c++
void science(double* data, int N) {
    auto temp = std::make_unique<double[]>(N * 2); // 使用 `unique_ptr` 代替指针
    do_setup(data, temp.get(), N);
    if (!needed(data, temp.get(), N)) return;
    calculate(data, temp.get(), N);
}
```

在这个改进后的代码中， `temp.get()` 返回 `unique_ptr` 所管理的原始指针，这样就可以将它传递给需要 `double*` 的函数（如 `do_setup`、`needed` 和 `calculate`）。

并且 `temp` 是一个 `unique_ptr<double[]>`，它会在 `science` 函数结束时自动释放所管理的内存，无论函数是如何退出的（通过 `return` 还是正常结束）。

### 10.3.6 所有权转移

在 `unique_ptr` 实现中我们提到了它的拷贝构造和拷贝复制是 `delete` 的，这意味着它不能被拷贝，只能移动。

```c++
auto a = std::make_unique<T>();

std::unique_ptr<T> b{ std::move(a) };  // 移动构造：所有权从 A 转移到 B

a = std::move(b);  // 移动赋值：所有权从 B 转移到 A
```

回顾之前另一个例子：

```c++ linenums="1"
float* science(float* x, float* y, int N) {
    float* z = new float[N];
    saxpy(2.5, x, y, z, N);
    delete[] x;
    delete[] y;
    return z;
}
```

这个例子中，「所有权」其实既有通过函数参数转移到了这个函数中的情况，也有通过返回值传出了函数的情况。我们可以使用 `unique_ptr` 来代替这个例子。

具体来说：

- 需要给一个函数 **传递** 所有权时，按值 (移动) 传递 `unique_ptr` 
- 需要从一个函数 **返回** 所有权时，按值 (移动) 返回 `unique_ptr` 

```c++
std::unique_ptr<float[]> science(
    std::unique_ptr<float[]> x,
    std::unique_ptr<float[]> y, int N) {

    auto z = std::make_unique<float[]>(N);
    saxpy(2.5, x.get(), y.get(), z.get(), N);
    return z;
}
```

外部可以 `auto result = science(std::move(upx), std::move(upy), N);` 来调用这个函数，这样调用者既可以清晰地看到 `upx` 和 `upy` 的所有权被转移，也可以从返回值类型清晰地看到 `result` 的所有权被返回。

但其实，在更多的情况下，`science` 函数内部并不需要 `x` 和 `y` 的所有权。此时我们不传递 `unique_ptr` ，而是传递裸指针，这样可以避免不必要的所有权转移。

```c++
void science(float* x, float* y, int N) {
    auto z = std::make_unique<float[]>(N);
    saxpy(2.5, x, y, z.get(), N);
}
```

外部调用：`auto result = science(upx.get(), upy.get(), N);` ，这样调用者就可以清晰地看到 `upx` 和 `upy` 的所有权没有被转移。`science` 的实现中也不应该释放 `x` 和 `y` 的内存，因为它们的所有权并没有转移。

也就是说，在有所有权转移的地方，传递智能指针；在不涉及所有权转移的地方，仍然继续使用指针 `.get()` 和引用 `*` 即可。例如：

```c++
void f(widget & w) { // if required
    use(w);
}

void g(widget * w) { // if optional
    if (w) use(*w);
}

auto upw = make_unique<widget>();
g(upw.get());
```

使用指针 `.get()` 还是引用 `*` 其实取决于指向的东西能不能为空。如果有可能指向一个空的东西的话，那么我们就使用指针 `.get()` 然后在里面去判断。如果你笃定你在你的代码里面，确定这个东西永远不会为空的话，那么直接使用引用 `*` 就好了。

### 10.3.7 用法小结

将 `unique_ptr` 作为引用传递给函数的情况，通常是函数需要重新设置指针的情况。这种情况下，调用者需要明确地知道函数会改变指针的指向。

我们把 `unique_ptr` 以不同方式作为函数参数和返回值的可能性提炼如下：

```c++
unique_ptr<widget> factory(...);  // source - produces widget
auto ptr = factory(...);

void use(widget&);  // use - use content but not consume widget
use(*ptr);

void use(widget*);  // use - use content but not consume widget
use(ptr.get());

void sink(unique_ptr<widget>);  // sink - consumes widget
sink(std::move(ptr));

void reseat(unique_ptr<widget>&);  // "will" or "might" reseat ptr
reseat(ptr);

void thinko(const unique_ptr<widget>&); // usually not what you want
```

### 10.3.8 陷阱

除非明确知道一个指针来自哪里，而且它确实需要一个所有者，否则不要用它初始化 `unique_ptr` 

```c++
T* p = ...;

std::unique_ptr<T> a(p);
std::unique_ptr<T> b(p);
// crash due to double free

auto c = std::make_unique<T>();
std::unique_ptr<T> d(c.get());
// crash due to double free
```

### 10.3.9 unique_ptr 在容器中使用

```c++
std::vector<std::unique_ptr<T>> v;

v.push_back(std::make_unique<T>());

std::unique_ptr<T> a;
v.push_back(std::move(a));

v[0] = std::make_unique<T>();

auto it = v.begin();
v.erase(it);
```

## 10.4 `std::shared_ptr`

### 10.4.1 概念

`shared_ptr` 其实是一个更高级的智能指针版本。它高级的地方就在于它的 **所有权是可以共享** 的。这就是我们之前说的「引用计数」的完整版本。

!!! note
    - 是对象的所有者，但可能有多个 `shared_ptr` 同时指向一个对象
    - 可以被拷贝
    - 当指向一个对象的 **最后一个** `shared_ptr` 不再指向它后（引用计数减到 0），对象被析构

例如可以实现为：

```cpp
struct ControlBlock {
    int* object; // 指向实际对象
    int count;   // 引用计数
};
```

当 `shared_ptr` 被复制时，新的 `shared_ptr` 会指向同一个 `Control Block`，并且引用计数会加 1。也就是说，`shared_ptr` 的拷贝是浅拷贝。

<center>![](2023-05-20-04-48-38.png){width=300} ![](2023-05-20-04-48-50.png){width=300}</center>

因此我们可以看到，`shared_ptr` 是 **有额外的内存和性能开销的**，并不像 `unique_ptr` 那样只是一个指针的包装。


### 10.4.2 接口

**构造与析构：**

```c++
template <typename T>
struct shared_ptr {
    // ...
    shared_ptr() noexcept;      // Creates empty shared_ptr
    explicit shared_ptr(T*);    // Starts managing an object
    ~shared_ptr() noexcept;     // Decrements count, and Cleanup if count == 0
    // ...
};
```

有一个默认构造函数，把它设为 `nullptr`。另外有一个直接把指针 `T*` 传进来，这个时候它才开始管理对象。

**拷贝和移动，以及从 unique_ptr 的移动**

```c++
template <typename T>
struct shared_ptr {
    // ...
    shared_ptr(shared_ptr const&) noexcept;     // copy ptrs, count++
    shared_ptr(shared_ptr&&) noexcept;          // transfer ownership
    shared_ptr(unique_ptr<T>&&);                // transfer ownership
    
    // origin count will decrease, possibly cleanup:
    shared_ptr& operator=(shared_ptr const&) noexcept;
    shared_ptr& operator=(shared_ptr&&) noexcept;
    shared_ptr& operator=(unique_ptr<T>&&);
    // ...
};
```

- **拷贝构造**：引用计数加 1。
- **移动构造**：不会增加引用计数，因为原 `shared_ptr` 不再指向该对象。
- `shared_ptr` 可以接受 `unique_ptr` 的右值引用，从而将独占所有权转换为共享所有权。
- 在赋值操作中，`shared_ptr` 会先减少原对象的引用计数，然后再指向新对象。如果原对象的引用计数减到 0，则会释放原对象。

**重载运算符：**

```c++
template <typename T>
struct shared_ptr {
// ...
    T& operator*() const noexcept;
    T* operator->() const noexcept;
// ...
};
```

**其他成员函数：**

```c++
template <typename T>
struct shared_ptr {
// ...
    void reset(T*);
    T* get() const noexcept;
    long use_count() const noexcept;
    explicit operator bool() const noexcept;
// ...
};
```

### 10.4.3 std::make_shared

类似 `unique_ptr` 的 `make_unique`，`shared_ptr` 也有一个 `make_shared` 函数，用于创建 `shared_ptr`。

```c++
template <typename T, typename... Args>
shared_ptr<T> make_shared(Args&&... args);
```

`make_shared` 是创建 `shared_ptr` 的首选方式，因为它只需要一次内存分配，同时为对象和引用计数分配内存。相比之下，直接使用 `new` 会进行两次内存分配。

我们知道内存申请是比较昂贵的，所以说有这样的 `make_shared` 就可以省下一些时间。同时可以让对象和引用计数离得更近，进而带来更好的 locality。

<center>![](2023-05-20-04-49-05.png){width=600}</center>

`shared_ptr` 在 C++17 时引入对数组的支持，`make_shared` 在 C++20 时引入对数组的支持。

### 10.4.4 shared_ptr 作为函数参数和返回值

类似前面的讨论，常见可能的用法是：

```c++
shared_ptr<widget> factory();               // source + shared ownership 
void share( shared_ptr<widget> );           // share: "will" retain refcount
void reseat( shared_ptr<widget>& );         // "will" or "might" reseat ptr
void may_share( const shared_ptr<widget>& );// "might" retain refcount
```

### 10.4.5 shared_ptr 的常见陷阱

#### Double Free 问题

```c++
T* p = ...;
std::shared_ptr<T> a(p);
std::shared_ptr<T> b(p);
// runtime error: double free

auto a = std::make_shared<T>();
std::shared_ptr<T> b(a.get());
// runtime error: double free

auto a = std::make_shared<T>();
std::shared_ptr<T> b(a);
std::shared_ptr<T> c;
c = b;
// Good
```

#### 多线程环境下的问题：the reentrancy pitfall

```c++
// global (static or heap), or aliased local
... shared_ptr<widget> g_p ...

void f(widget& w) { g(); use(w); }
void g() { g_p = ... ; } 

void my_code() {
    f(*g_p); // bad
    g_p->foo(); // bad
}
```

解决方案："Pin" using unaliased local copy

```c++
// global (static or heap), or aliased local
... shared_ptr<widget> g_p ...

void f(widget& w) { g(); use(w); }
void g() { g_p = ... ; }

void my_code() {
    auto pin = g_p; // 1 ++ for whole tree
    f(*pin); // ok, *local
    pin->foo(); // ok, local->
}
```

## 10.5 回顾：Rule of Zero

C++11 改进了语言和标准库，提供了对动态分配对象生命周期管理的更好工具。在这种背景下 Rule of Zero 被提出，作为对之前 Rule of Three 的更新：

- `std::string` 代为管理字符串
- STL 容器代为管理数据类型，如 `std::vector` 或者 `std::array` 代为管理数组
- 智能指针代为管理动态内存
- `std::fstream` 等代为管理文件读写

## 10.6 本文暂未讨论的话题

- **线程安全**: 在多线程环境下，尤其是 `shared_ptr`，需要保证线程安全。这个话题值得深入讨论，但由于我们没有涉及多线程的内容，暂时不展开讲解。
- **异常安全**: 虽然我们还没有设计异常处理，但智能指针除了之前提到的各种优点外，还能提供较好的异常安全性。
- **`std::weak_ptr`**: C++ 标准库中有几种智能指针，除了 `shared_ptr` 和 `unique_ptr` 之外，还有一个 `weak_ptr`。`weak_ptr` 是与 `shared_ptr` 共同使用的，它是 `shared_ptr` 的一个弱引用。所谓弱引用，就是即使 `weak_ptr` 存在，如果最后一个 `shared_ptr` 被销毁，对象仍然可以正常析构。`weak_ptr` 不影响对象的析构。`weak_ptr` 的一个常见用途是在实现 cache 时使用，大家有兴趣的话可以自行查阅相关资料。
- **自定义删除器**: `shared_ptr` 和 `unique_ptr` 都支持自定义删除器。默认情况下，对于非数组类型，删除器是 `delete`，对于数组类型，删除器是 `delete[]`。但在实际应用中，我们可能需要管理非普通指针，比如 `FILE*`，这时我们希望在析构时调用 `fclose` 而不是 `delete`。这种情况下，我们可以自定义删除器。
- **继承关系中的智能指针**: 在 C++ 中，子类的指针可以转换为基类的指针。同样，子类的智能指针也可以转换为基类的智能指针。这是对普通指针行为的一种模仿。如果大家有需要，可以进一步了解这方面的内容。
- **`shared_from_this`**
