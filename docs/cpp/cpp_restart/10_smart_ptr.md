# 10 智能指针

!!! info "本节录播地址"
    本节的朋辈辅学录播可以在 [B 站](https://www.bilibili.com/video/BV1Uo4y1g7tH/?spm_id_from=333.788&vd_source=c5a9383e47adf0fdb6896be9dbbc50fc) 找到！


## 10.1 智能指针：动机

在讲智能指针之前，我们先要来看看指针有什么问题。

???+ info "问题 1：指针的所有权"

    下面是我们可能会写出来的一个函数，它接受一个 `double` 的指针和一个 `int` 的 `N`。

    ```c++
    void science(double* data, int N) {
        double* temp = new double[N*2];
        do_setup(data, temp, N);
        if (!needed(data, temp, N))
            return;
        calculate(data, temp, N);
        delete[] temp;
    }
    ``` 
    
    这些参数其实表示一个叫 `data` 的数组。我们把这个数组的基地址传进来，相当于发生了 `array` 到 `point` 的转换，但这么做我们丢失了这个数组有多少个元素的信息，所以我们用这个额外的参数 `N` 把这个信息传进来了。

    这个函数在最开头 `new` 了一个类型为 `double` 的数组，做了一些前期的准备，然后判断需不需要计算。如果不需要计算的话，函数返回。如果需要计算的话就计算，计算后 `delete` 这个不再用的 `temp` 。


    但是这个函数有一个重大的问题，如果这个 `if` 的条件为真，它直接 `return` ， `new` 出来的这个 `temp` 没有被释放，也就是说我们应该对这个函数的每一个出口都要把他申请过的所有的资源全部释放一遍，这个事情显得比较蠢，比较累，而且比较容易出错。
    
    那么问题来了！看这个函数中一共有两个指针 `data` 和 `temp` ，为什么我们释放 `temp` 却不释放 `data` 呢？
    
    因为 `temp` 是我开出来的，那我就有责任把它释放，而 `data` 这个东西不是我开出来的，如果我把它 `delete` 外面还要用怎么办，那就是个 use after `delete` ；或者说我把它 `delete` ，外面又把它 `delete` 了一遍，那就是 double `delete`，这两个东西都会发生错误。
    
    通过这个例子就可以看到，我们要根据是否拥有来决定是否释放，但在例子中 `data` 和 `temp` 都是 `double*` 类型，也就是说，我们在代码上看不出是否拥有是否释放这种信息，那么我们只能从文档里或者从注释里找这种信息，但我们不希望这样重要的信息（是否导致ub、crash、内存鞋头）以注释的方式产生。

???+ info "问题 2：指针指向单个对象还是数组"

    形如 `T*` 的指针可以指向单个对象，也可以指向数组。当它指向单个对象，其实就被视为指向了一个元素大小为一的数组，但是指向单个对象的时候

    - 不应该用 `++p` 或 `--p` ，因为它们都会超出边界（数组可以 `++p` 或 `--p` ，但也不能超出边界）。
    - 使用 `delete` 释放（数组使用 `delete[]` 释放）
    
    上面例子说明，在C++中，指针类型本身并不包含它指向单个对象还是数组的信息。这意味着编译器无法通过类型信息来判断应该使用 `delete` 还是 `delete[]`。

???+ info "问题 3：指针是否允许为空"

    我们在编写代码时候经常要判断指针是否为 `nullptr`。如果可以保证某种指针可以永远不为空的话，就可以省去空指针检查，从而提高代码效率。但在C++中，指针类型本身无法表达是否允许为空。 

上面三个问题事实上都是一个问题，就是指针本身包含了这么多信息，但是指针们看起来都长 `T*` 这个样子。事实上我们所希望的智能指针，智能在于能提供这些信息。

总结一下，我们希望智能指针可以实现：

**智能**

- 自动回收资源：在对象使用完成后，智能指针能够自动调用析构函数来释放资源，而不需要程序员手动调用。
- 增加一些限制：例如强制指针不为空，从而避免空指针引用的问题。
- 更多的安全限制或检查

**指针**

- 能像指针一样，指向对象，间接访问

通过这种方式，智能指针可以像 `std::string` 一样，隐藏底层的内存管理细节，让程序员专注于业务逻辑的实现，而不必担心内存泄漏或资源管理的问题。

## 10.2 垃圾回收 | GC

### 10.2.1 概念

垃圾回收（Garbage Collection）的核心就是**回收不可达的对象**。

???+ info "什么是不可达"

    **不可达**就是没有任何方式可以访问到这个对象，例如：

    - **局部对象超出作用域**：
    局部对象在其作用域结束时会被自动销毁，但如果存在指向该对象的指针或引用，且这些指针或引用在对象销毁后仍然存在，那么这些指针或引用将指向一个不可达的对象。

        ```c++
        void foo() {
            MyClass obj;
            MyClass* ptr = &obj;
        } // obj 超出作用域，ptr 现在指向一个不可达的对象
        ```

    - **悬空指针**：
    悬空指针是指向已经被释放或销毁的对象的指针。这种情况下，指针指向的对象是不可达的。

        ```c++
        MyClass* ptr = new MyClass();
        delete ptr;
        // ptr 现在是一个悬空指针，指向一个不可达的对象
        ```

    - **内存泄漏**：
    如果动态分配的内存没有被正确释放，那么这些内存中的对象将变得不可达。

        ```c++
        void leak() {
            MyClass* ptr = new MyClass();
            // 没有调用 delete ptr;
        } // ptr 超出作用域，指向的对象成为不可达对象
        ```

    - **循环引用**：
    在使用智能指针（如 `std::shared_ptr`）时，如果存在循环引用，可能会导致对象无法被正确释放，从而成为不可达对象。

        ```c++
        struct Node {
            std::shared_ptr<Node> next;
        };

        auto a = std::make_shared<Node>();
        auto b = std::make_shared<Node>();
        a->next = b;
        b->next = a; // 循环引用，a 和 b 成为不可达对象
        ```

### 10.2.2 垃圾回收的要点

如何判断对象的**可达性**呢？

- **Reference Counting**

    引用计数的核心思想是为每个对象维护一个**引用计数器**，记录有多少个指针指向该对象。当引用计数为零时，说明没有任何指针指向该对象，因此可以安全地回收该对象的内存。

    引用计数的优点是实现简单，且可以立即回收不再使用的对象。但它的缺点是：

    - **循环引用问题**：如果两个对象互相引用，它们的引用计数永远不会为零，导致内存泄漏。
    - **性能开销**：每次指针的赋值或析构都需要更新引用计数，可能会带来额外的性能开销。

- **Mark & Sweep（From Root Set）**

    标记-清除是一种更复杂的垃圾回收方式。它的核心思想是从程序的根对象（如全局变量、栈上的变量等）开始，递归地标记所有可以访问到的对象。标记完成后，垃圾回收器会清除所有未被标记的对象，回收它们的内存。

    标记-清除的优点是能够处理循环引用问题，但它的缺点是：

    - **暂停时间较长**：标记和清除的过程可能会暂停程序的执行，影响程序的响应速度。
    - **内存碎片问题**：清除过程中可能会产生内存碎片，导致内存利用率下降。

知道对象**不可达**时，回收多大空间？

这个问题是一个**类型安全**的问题，尽管从 C 到 C++ 的过程中，做了一些关于类型安全的处理，但由于向前兼容等原因， C++ 仍然不是一门类型安全的语言，例如：

- `void *`： `void*` 不携带类型信息，编译器无法在编译时检查类型是否匹配。这意味着你可以在运行时将 `void*` 转换为任何类型的指针，而编译器不会报错。在这个转换过程中，如果类型不匹配，可能会导致未定义行为。

- `union`：`union` 中的成员共享同一块内存。同一时刻，`union` 中只能保存一个成员的值，但编译器无法强制执行这一点。

- `Type Punning`: 类型双关是指通过一种类型的指针访问另一种类型的数据。

### 10.2.4 智能指针与垃圾回收的关系

智能指针可以看作是 C++ 中的一种轻量级垃圾回收机制。它们通过自动管理对象的生命周期，避免了手动调用 `delete` 或 `delete[]` 的麻烦，从而减少了内存泄漏的风险。然而，智能指针并不能完全替代垃圾回收，应该通过 RAIL 机制正确管理资源。

## 10.3 unique_ptr

### 10.3.1 概念
我们首先要讲的第一种智能指针，叫做 `unique_ptr` ，定义在 `<memory>` 头文件中。

 `unique_ptr` 假设自己是对象唯一的所有者，是引用计数的简化版本。

!!! note
    - 是对象的所有者，并假设是唯一的所有者
    - 自动回收资源
    - 只能移动，不能拷贝

### 10.3.2 使用方法

`unique_ptr` 是一个类模板。它的构造函数可以接受一个指针，需要注意的是，这个智能指针只维护堆上的东西，不要把栈上的指针传给他。

```c++
void calculate_more(HelperType&);

ResultType do_work(InputType inputs){
    std::unique_ptr<HelperType> owner( new HelperType(inputs) );
    owner->calculate();
    calculate_more(*owner);
    return owner->important_result();
}
```

另外 `unique_ptr` 提供了与普通指针类似的访问方式：

- 成员访问运算符 `->`：用于访问指针所指向对象的成员。
- 间接访问运算符 `*`：用于解引用指针，获取指针所指向的对象。

事实上 `unique_ptr` 也可以放到类里面。我们有一个类里面有个成员 `unique_ptr` ，名字是 owner 。那么我们构造的时候，给这个owner传一个指针进去用来初始化。

```c++
WidgeBase* create_widge(InputType);

class MyClass {
    std::unique_ptr<WidgeBase> owner;
public:
    MyClass(InputType inputs)
        : owner(create_widge(inputs)) { }
    ~MyClass() = default;
    // ... member functinos that use owner-> ...
}
```

为什么 `~MyClass() = default` ，因为等于default的时候，它会调用 owner 这个成员函数的构造，owner的析构函数会析构掉这个指针。所以说我们可以看到 MyClass 里面没有必要再去写我们之前说了那五种 special member functions。

### 10.3.3 实现思路

**成员类型：**

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

**构造与析构：**

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

有一个不接受指针的默认构造函数，可以发现 `unique_ptr` 是可为空的。有一个注明为 `explicit` 的接受一个指针的构造函数。有一个析构函数。为什么不是 `delete[]`，因为 `unique_ptr` 对数组做了 partial specialization。

**移动构造与移动赋值：**

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
它的移动构造和移动赋值跟前一章讲的类似。当然我们之前说 `unique_ptr` 本身可能是 nullptr ，但是我们之前也讲过 delete nullptr 是安全的。

**重载运算符：**

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
我们之前没有见过这个箭头运算符重载，事实上 `owner->calculate()` 可以写成 `(owner.operator->())->calculate()` 而 `(owner.operator->())` 返回的是 `ptr`，最终这个可以写成 `ptr->calculate()`。

可以发现 `unique_ptr` 是 `ptr` 的一层 wrapper ，但是我们通过重载这样的 `*` 和 `->` 运算符，使得这个包装实际上是可以像原来一样使用的，或者说在函数内联完成之后，这个包装就不存在了。

**其他成员函数**
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

它还有一些其他的成员函数，比如说将所有权转移给其他代码的 `release()` ，它释放对当前管理的对象的所有权，并返回指向该对象的指针。还有重置 `unique_ptr` 管理的对象的 `reset(T* p = nullptr)` ，它释放当前管理的对象并接管新的对象，或者将 `unique_ptr` 设置为空。类似 `release()` 的 `get()` 只返回指针不释放所有权。`bool()` 判断指针是否为空。

???+ info "避免直接使用 `new` 和 `delete`"

    在之前的代码中，我们仍然使用了 `new` 来创建 `unique_ptr` ，但 `delete` 却通过 `unique_ptr` 的析构来自动进行，这导致了 `new` 和 `delete` 不配对。

    事实上在 C++14 引入了 `make_unique` 用于创建一个 `unique_ptr`。它**避免了显式调用 `new`**并且提供了更好的**异常安全性**，下面给出 `make_unique` 的用法：

    ```c++
    std::unique_ptr<Type> ptr = std::make_unique<Type>(args...);
    ```

    其中 `Type` 是你想要创建的对象类型，`args...` 是传递给 `Type` 构造函数的参数。
### 10.3.4 数组类型

 `unique_ptr` 对数组做了 partial specialization 使得

- `unique_ptr<T[]>` 提供了对数组类型的支持，自动调用 `delete[]` 来释放内存。
- `unique_ptr<T[]>` 提供了下标运算符 `operator[]`，使得你可以像使用普通数组一样访问元素。

 `make_unique` 也对数组类型做了一些 partial specialization 使得
 
- 可以使用 `make_unique<T[]>(size)` 来创建一个动态数组，其中 `size` 是数组的大小。与普通的 `unique_ptr<T>` 不同，`make_unique<T[]>` 只接受一个参数，即数组的大小，而不接受构造函数参数。这是因为数组类型的 `unique_ptr` 不支持构造函数参数。例如：

    ```c++
    auto ptr = std::make_unique<double[]>(10);  // 正确：创建一个包含 10 个 double 元素的数组
    // auto ptr = std::make_unique<double>(10);  // 错误：这不是数组类型
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

在这个改进后的代码中， `temp.get()` 返回 `unique_ptr` 所管理的原始指针，这样就可以将它传递给需要 `double*` 的函数（如 `do_setup`、`needed` 和 `calculate`）。并且`temp` 是一个 `unique_ptr<double[]>`，它会在 `science` 函数结束时自动释放所管理的内存，无论函数是如何退出的（通过 `return` 还是正常结束）。

### 10.3.6 所有权转移

在 `unique_ptr` 实现中我们提到了它的拷贝构造和拷贝复制是 `delete` 的，这意味着它不能被拷贝，只能通过移动语义（`std::move`）来转移所有权。

将一个 `unique_ptr` 传递给另一个对象或函数时，必须使用 `std::move` 来显式地表示所有权的转移。这种必须可以在外面让调用者轻松看出所有权的转移。

```c++
auto a = std::make_unique<T>();

std::unique_ptr<T> b{ std::move(a) };  // 所有权从 A 转移到 B

a = std::move(b);  // 所有权从 B 转移到 A
```

### 10.3.7  unique_ptr 作为函数参数和返回值
 
 `unique_ptr` 作为参数的时候，通常有几种可能：

- **按值传递：**意味着函数将接管 `unique_ptr` 的所有权

    - 需要给一个函数**传递**所有权时，按值传递 `unique_ptr` 
    - 需要从一个函数**返回**所有权时，按值传递 `unique_ptr` 

    ```c++
    std::unique_ptr<float[]> science(
        std::unique_ptr<float[]> x,
        std::unique_ptr<float[]> y, int N) {

        auto z = std::make_unique<float[]>(N);
        saxpy(2.5, x.get(), y.get(), z.get(), N);
        return z;
    }
    ```

- **按引用传递：**通常只在需要修改 `unique_ptr` 本身（例如改变它指向的对象）时使用。例如：

        ```c++
        unique_ptr<widget> factory();  // source - produces widget
        void sink(unique_ptr<widget>);  // sink - consumes widget
        void reseat(unique_ptr<widget>&);  // "will" or "might" reseat ptr
        void thinko(const unique_ptr<widget>&); // usually not what you want
        ```

 `unique_ptr` 作为返回值很好理解，就是函数将对象的所有权返回给调用者。例如：`auto result = science(std::move(x), std::move(y), N);`

### 10.3.8 不使用 unique_ptr 的场景

```c++
std::unique_ptr<float[]> science(
    // ...
    saxpy(2.5, x.get(), y.get(), z.get(), N);
    // ...
}
```

上面代码中的 `saxpy` 函数中，我们并不关心对象的所有权，只是需要访问对象的内容，所以使用裸指针。

!!! note
    在有所有权转移的地方，使用智能指针；在不涉及所有权转移的地方，仍然继续使用指针 `.get()` 和引用 `*` 即可。例如：

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

    使用指针 `.get()` 还是引用 `*` 其实取决于指向的东西能不能为空。如果有可能指向一个空的东西的话，那么我们就使用指针 `.get()` 然后在里面去判断。如果你笃定你在你的代码里面，确定这个东西永远不会为空的话，那么你直接使用引用 `*` 就好了。

### 10.3.9  unique_ptr 的陷阱

留作思考题，除非明确知道一个指针来自哪里，而且它确实需要一个所有者，否则不要用它初始化 `unique_ptr` 

```c++
T* p = ...;

std::unique_ptr<T> a(p);
std::unique_ptr<T> b(p);
// crash due to double free

auto c = std::make_unique<T>();
std::unique_ptr<T> d(c.get());
// crash due to double free
```

### 10.3.10  unique_ptr 在容器中使用

```c++
std::vector<std::unique_ptr<T>> v;

v.push_back(std::make_unique<T>());

std::unique_ptr<T> a;
v.push_back(std::move(a));

v[0] = std::make_unique<T>();

auto it = v.begin();
v.erase(it);
```

## 10.4 shared_ptr

### 10.4.1 概念

`shared_ptr` 其实是一个更高级的智能指针版本。它高级的地方就在于它的**所有权是可以共享**的。这就是我们之前说的引用计数的完整版本。

!!! note
    - 是对象的所有者，但可能有多个`shared_ptr` 同时指向一个对象
    - 可以被拷贝
    - 当指向一个对象的最后一个`shared_ptr` 不再指向它后（引用计数减到 0 ），对象被析构

### 10.4.2 设计原理

`shared_ptr` 的设计可以简化为以下几个部分：

- **Object**：实际管理的对象。
- **Control Block**：辅助管理引用计数的结构，包含一个指向对象的指针和一个引用计数。

例如：

```cpp
struct ControlBlock {
    int* object; // 指向实际对象
    int count;   // 引用计数
};
```

当 `shared_ptr` 被复制时，新的 `shared_ptr` 会指向同一个 `Control Block`，并且引用计数会加 1。与 `std::string` 不同，`shared_ptr` 是浅拷贝的。也就是说，多个 `shared_ptr` 会指向同一块内存，而不是像 `std::string` 那样复制一份新的内存。

### 10.4.3 接口

 `shared_ptr` 的实现思路比较复杂，所以这里我们只讲它的接口。

**构造与析构：**

```c++
template <typename T>
struct shared_ptr {
    // ...
    shared_ptr() noexcept; // Creates empty shared_ptr
    explicit shared_ptr(T*); // Starts managing an object

    ~shared_ptr() noexcept; // Decrements count, and ...
                            // Cleanup if count == 0
    // ...
};
```

有一个默认构造函数，把它设为 `nullptr` 。另外有一个直接把指针 `T*` 传进来，这个时候它才开始管理对象。

**拷贝构造和移动构造：**

```c++
template <typename T>
struct shared_ptr {
    // ...
    shared_ptr(shared_ptr const&) noexcept;// copy ptrs, count++
    shared_ptr(shared_ptr&&) noexcept;// transfer ownership
    shared_ptr(unique_ptr<T>&&);// transfer ownership
    // ...
};
```

 `shared_ptr` 支持拷贝构造和移动构造：
- **拷贝构造**：引用计数加 1。
- **移动构造**：不会增加引用计数，因为原 `shared_ptr` 不再指向该对象。

`shared_ptr` 可以接受 `unique_ptr` 的右值引用，从而将独占所有权转换为共享所有权。
其实就是我本来有一个东西，由我单独管理。但是我现在决定要 `share`。所以我移动给一个`shared_ptr` 。

**拷贝赋值和移动赋值

```c++
template <typename T>
struct shared_ptr {
    // ...
    // origin count will decrease, possibly cleanup:
    shared_ptr& operator=(shared_ptr const&) noexcept;
    shared_ptr& operator=(shared_ptr&&) noexcept;
    shared_ptr& operator=(unique_ptr<T>&&);
    // ...
};
```

在赋值操作中，`shared_ptr` 会先减少原对象的引用计数，然后再指向新对象。如果原对象的引用计数减到 0，则会释放原对象。

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

我们可以用 `use_count()` 来获取引用计数。

???+ info "避免直接使用 `new` 和 `delete`"

    类似的，`shared_ptr` 也可以使用 `make_shared` 来创建，并且 `make_shared` 有比`make_unique` 更高的价值。

    `make_shared` 是创建 `shared_ptr` 的首选方式，因为它只需要一次内存分配，同时为对象和 `Control Block` 分配内存。相比之下，直接使用 `new` 会进行两次内存分配。我们知道内存申请是比较昂贵的，所以说有这样的 `make_shared` 就可以省下一些时间。同时可以让对象和 `Control Block` 离得更近，进而带来更好的 locality。

    另外 `shared_ptr` 在 C++17 时引入对 `array` 的支持，`make_shared` 在 C++20 时引入对 `array` 的支持。

### 10.4.4 shared_ptr 作为函数参数和返回值

 `shared_ptr` 作为参数的时候，通常有几种可能：

- **按值传递：**如果函数确实需要获得一个副本，按值传递。

```c++
shared_ptr<widget> factory();  // source + shared ownership

void share(shared_ptr<widget>);  // share: "will" retain refcount
```

- **按引用传递：**函数有可能对 `shared_ptr` 作更改时，按引用或 const 引用（避免昂贵的拷贝）传递。
```c++
shared_ptr<widget> factory();  // source + shared ownership

void reseat(shared_ptr<widget>&);  // "will" or "might" reseat ptr
void may_share(const shared_ptr<widget>&);  // "might" retain refcount
```

### 10.4.5 shared_ptr 的陷阱

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

```c++
// the reentrancy pitfall
// global (static or heap), or aliased local
... shared_ptr<widget> g_p ...

void f(widget& w) { g(); use(w); }
void g() { g_p = ... ; } 

void my_code() {
    f(*g_p); // bad
    g_p->foo(); // bad
}
```

```c++
// "Pin" using unaliased local copy
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

## 10.5 总结

我们这次主要讲解了 `unique_ptr` 和 `shared_ptr` 这两种智能指针。需要注意的是，`unique_ptr` 没有额外开销，而 `shared_ptr` 有额外开销。我们建议大家使用 `std::make_unique` 和 `std::make_shared`，因为它们不仅能提高代码的可读性，还能减少运行时的开销。

智能指针能够更好地帮助我们实现 RAII（资源获取即初始化）。例如，我们之前提到的 `std::string` 可以很好地管理字符串资源，为 RAII 提供了巨大帮助。同样，`std::vector` 等标准库容器也能提供类似的支持。此外，文件读写也可以使用 `std::ifstream` 等工具来处理。

此外，我们建议大家不要在代码中直接使用 `new` 和 `delete`。所有需要动态分配内存的地方，都应该使用智能指针来代替，从而更好地适配 RAII ，避免内存泄漏等问题。
如果一个指针不拥有它所指向的对象，即它不需要负责释放对象的内存，那么可以使用裸指针或引用。在这种情况下，裸指针是合适的。

!!! 智能指针的使用建议
    - **函数参数传递**：如果一个函数的操作与指针的所有权无关，按照指针或引用的方式传递。如果对象一定存在，使用引用；如果对象可能存在也可能不存在，使用指针。
    - **函数返回值**：如果一个函数创建并返回一个 `unique_ptr`，按值返回。如果 `unique_ptr` 的生命周期在函数内结束，按值传递。
    - **修改智能指针指向的对象**：如果需要修改智能指针指向的对象，通常传引用。
    - **`const unique_ptr` 引用**：这种写法通常是错误的，应避免。
    - **`shared_ptr` 的使用**：如果创建并分享一个 `shared_ptr`，按值返回。如果函数需要一个副本，按值拷贝。如果可能拷贝也可能不拷贝，按 `const` 引用传递。如果可能修改智能指针的内容，按引用传递。

接下来，我们简单介绍一下这节课没有详细讲解的一些话题，大家以后遇到这些问题时，可以知道如何去搜索相关内容。

- **线程安全：**
    在多线程环境下，尤其是 `shared_ptr`，需要保证线程安全。这个话题值得深入讨论，但由于我们没有涉及多线程的内容，暂时不展开讲解。

- **异常安全：**
    虽然我们没有讲解异常处理，但智能指针除了之前提到的各种优点外，还能提供较好的异常安全性。因此，异常安全也是一个值得讨论的话题。

- **weak_ptr：**
    C++ 标准库中有几种智能指针，除了 `shared_ptr` 和 `unique_ptr` 之外，还有一个 `weak_ptr`。`weak_ptr` 是与 `shared_ptr` 共同使用的，它是 `shared_ptr` 的一个弱引用。所谓弱引用，就是即使 `weak_ptr` 存在，如果最后一个 `shared_ptr` 被销毁，对象仍然可以正常析构。`weak_ptr` 不影响对象的析构。`weak_ptr` 的一个常见用途是在缓存中使用，大家有兴趣的话可以自行查阅相关资料。

- **自定义删除器：**
    `shared_ptr` 和 `unique_ptr` 都支持自定义删除器。默认情况下，对于非数组类型，删除器是 `delete`，对于数组类型，删除器是 `delete[]`。但在实际应用中，我们可能需要管理非普通指针，比如 `FILE*`，这时我们希望在析构时调用 `fclose` 而不是 `delete`。这种情况下，我们可以自定义删除器。

- **继承关系中的智能指针：**
    在 C++ 中，子类的指针可以转换为基类的指针。同样，子类的智能指针也可以转换为基类的智能指针。这是对普通指针行为的一种模仿。如果大家有需要，可以进一步了解这方面的内容。

## 参考资料

