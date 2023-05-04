考虑前面我们设计的 `Matrix` 类：

```c++ linenums="1"
const int M = 100;
class Matrix {
    int data[M][M];
public:
    Matrix operator-(Matrix mat) {
        Matrix res;
        for (int i = 0; i < M; i++)
            for (int j = 0; j < M; j++)
                res.data[i][j] = data[i][j] - mat.data[i][j];
        return res;
    }
};
```

容易发现，这个类的对象占据的内存是非常大的，因此我们将对象作为参数传递时会有很大的开销。

我们在 C 语言中学习过，可以通过传递指针的方式来减少不必要的拷贝。例如有函数 `int getSum(Matrix mat);` 就可以改为 `int getSum(Matrix * mat);`，调用时通过 `getSum(&m)`，就可以只传递指针而不必拷贝整个对象了。

但是，对于上面的 `Matrix::operator-(Matrix);`，我们如何解决这个问题呢？C++ 并不希望要求程序员在这种情况下将 `m1 - m2` 改为 `&m1 - &m2` 去写。一方面是不自然，另一方面是指针相减在语言中已有定义。

为了解决这个问题，BS 将 Algol 68 中的 **引用 (reference)** 机制引入了 C++[^algol_ref]。

[^algol_ref]: 作为一个改进，C++ 不允许改变一个引用所引用的东西（也就是不允许重新约束），绑定只能发生在初始化时。

一个引用是一个已经存在的对象或者函数的别名。例如：

```c++
int x = 2;
int & y = x;    // y is an alias for x
```

这样，对 `y` 的所有操作都和对 `x` 的操作一样了；`y` 不是 `x` 的指针，也不是 `x` 的副本，而是 `x` 本身。包括获取它的地址—— `&y` 和 `&x` 的值相同。

也是因此，我们无法重新约束一个引用所绑定的变量。因为：

```c++
int z = 3;
y = z;
```

上面的 `y = z` 实际上是给 `x` 赋值为 `z`，而非将 `y` 重新绑定到 `z`。

---

#### 引用作为参数

显然，在同一个作用域内，给一个变量起一个别名并不会有太多的现实意义。引用最广泛的用法是作为参数传递：

```c++ linenums="1"
void swap(int& i, int& j) {
    int tmp = i;
    i = j;
    j = tmp;
}

int main() {
    int x, y;
    // ...
    swap(x,y);
    // ...
}
```

我们知道，C 和 C++ 的函数参数传递都默认是按值传递 (pass-by-value) 的，而引用机制使得 C++ 中可以实现类似上面的按引用传递 (pass-by-reference)。在调用 `swap` 之后，`i` 成为了 `x` 的别名，对 `i` 做的一切操作事实上就是作用于 `x` 了。

这样，我们就能简易地解决前面的问题了：我们只需要让 `Matrix` 传递时传递引用即可：

```c++ linenums="1" hl_lines="5"
const int M = 100;
class Matrix {
    int data[M][M];
public:
    Matrix operator-(const Matrix & mat) {
        Matrix res;
        for (int i = 0; i < M; i++)
            for (int j = 0; j < M; j++)
                res.data[i][j] = data[i][j] - mat.data[i][j];
        return res;
    }
};
```

我们这里使用了 `const Matrix &` 而不只是 `Matrix &`，从而说明 `mat` 是只读而不可修改的。虽然后者也能实现我们需要的效果，但是这样能够保证函数中只会读取 `mat` 的值，而不会意外修改它。

就像我们可以用一个 `const int *` 保存一个 `int` 的地址一样，这种「给出更强保证」的隐式类型转换对于引用也显然是合法的。即，如果有一个 `int`，我们可以给它一个类型为 `int &` 或者 `const int &` 的别名：

```c++
void foo() {
    int x = 1;
    const int y = 2;

    int & rx1 = x;  // OK
    rx1 = 3;        // OK, now x is 3

    const int & rx2 = x;    // OK
    rx2 = 4;        // Error: assignment of read-only reference 'rx2'

    int & ry1 = y;  // Error: binding reference of type 'int' to value of type
                    // 'const int' drops 'const' qualifier
    const int & ry2 = y;    // OK
}
```

---

#### 引用作为返回值

引用也可以作为函数的返回值。看下面的例子：

```c++ linenums="1"
class Container {
    elem* val;
    unsigned size = 0, capa;
    // ...
public:
    elem & operator[](unsigned index) {
        return val[index];
    }
    // ...
};
```

这样，如果有一个 `Container` 对象 `c`，我们就可以通过 `c[i]` 的方式访问容器中的值，如读取 `x = c[i]` 或者写入 `c[i] = x`。由于其返回的是一个引用，我们可以通过这个引用来修改其值。这使得我们不再需要写 `c.getVal()[i] = x` 之类的丑陋代码。

当然，如果希望 `operator[]` 返回的值是只读的，我们只需要让函数返回 `const elem &` 即可：

```c++
const elem & operator[](unsigned index);
```

这在 `elem` 比较大的时候有助于避免不必要的拷贝。不过，在 `elem` 是比较小的基本类型且没有修改需求的情况下，则直接返回值会更好一些。

???+ tips
    请在返回引用时注意避免 dangling reference。例如：

    ```c++
    int & foo () {
        int tmp = 10;
        // ...
        return tmp;
    }
    ```

    这里 `tmp` 作为局部变量，在函数结束时就会被销毁；但是函数却返回了一个引用这个已经不存在的变量的引用。这是个 dangling reference，将会导致 undefined behavior^[std_citation_needed](./std_citation_needed.md)^。

???+ note "关于自定义矩阵的 `operator[]`"
    假如我们有这样的定义：

    ```c++
    const int M = 100;
    class Matrix {
        int data[M][M];
    };
    ```

    如果我们希望能够以 `mat[x][y]` 的方式访问 `mat.data[x][y]`，应该怎么办呢？很遗憾，由于它实际上调用的是 `mat.operator[](x).operator[](y)`，因此 `mat.operator[](x)` 返回的东西必须是一个定义了 `operator[]` 的类型。
    
    虽然以下定义是可行的，因为 `int *` 类型可以使用下标访问：

    ```c++
    const int M = 100;
    class Matrix {
        int data[M][M];
    public:
        int * operator[](unsigned index) { return data[index]; }
    };
    ```

    但是，假如我们需要检查是否下标越界，这样的实现就不好了。
    
    因此，我们可能不得不这样定义：

    ```c++
    const int M = 100;

    class Row {
        int data[M];
    public:
        int & operator[](unsigned index) { return data[index]; }
    }

    class Matrix {
        Row data[M];
    public:
        Row & operator[](unsigned index) { return data[index]; }
    }
    ```

    另一种方案是，借用能接受任意个参数的函数调用运算符 `()`，即：

    ```c++
    const int M = 100;
    class Matrix {
        int data[M][M];
    public:
        int & operator()(unsigned x, unsigned y) { return data[x][y]; }
    };
    ```

    这样，我们就可以使用 `mat(x, y)` 的形式访问对应的元素了。

    好消息是，自 C++23 开始，`operator[]` 也可以接收任意个参数了（此前确切只能接收 1 个），因此我们可以写：

    ```c++
    const int M = 100;
    class Matrix {
        int data[M][M];
    public:
        int & operator[](unsigned x, unsigned y) { return data[x][y]; }
    };
    ```

    不过在调用时，我们仍然需要使用 `mat[x, y]` 而非 `mat[x][y]` 的方式访问对应元素。


---

#### 引用类似于包装了的指针

从实现的角度而言，我们可以认为引用更类似于 const 指针，即 `int & y = x;` 类似于对 `int * const py = &x;` 的包装，对 `y` 的使用实际上是使用 `*py`。

不过需要注意的是，在实际实现中，引用并不一定会占用存储^[dcl.ref#4](https://timsong-cpp.github.io/cppwp/n4868/dcl.ref#4)^。这是很容易理解的。

???+ note "const"
    如果你并不记得 `const int *`, `int const *`, `int * const`, `const int * const` 之类的东西代表什么含义，可以看这里复习一下。

    首先，`const` 是一种 **cv-qualifier**，它可以和任何类型说明符组合，以指定被声明的对象是常量。
    
    ??? info "cv-qualifier"
        c 指 `const`，v 指 `volatile`；后者我们暂不讨论。

    尝试直接修改 `const` 限定的变量会被编译器拒绝：

    ```c++
    const int i = 3;
    i = 0;          // assignment of read-only variable 'i'
    ```

    因此，具有 `const` 限定类型的变量必须被初始化：

    ```c++
    const int i;    // error: uninitialized 'const j'
    ```

    `const int *` 和 `int const *` 用来表示「指向一个不可变的 `int` 的指针」，指针本身可以被修改，但是指向的变量是只读的：

    ```c++ linenums="1"
    const int i = 1;
    int j = 3;

    int * s = &i;   // error: invalid conversion from 'const int *' to 'int *'

    const int * p = &i; // OK
    const int * q = &j; // OK, assign 'int *' to 'const int *' is valid

    i = 4;  // error: assignment of read-only variable 'i'
    *p = 4; // error: assignment of read-only location '*p'
    j = 4;  // OK
    *q = 4; // error: assignment of read-only location '*q'

    p = q;  // OK, the pointer itself is not constant
    const int * r;  // OK, non-const variable can be defined without initializer

    int * s = q;    // error: invalid conversion from 'const int *' to 'int *'
    ``` 

    而 `int * const` 用来表示「指向一个 `int` 的不可变的指针」，指针本身不能被修改，但是指向的变量是可以修改的：

    ```c++  linenums="1"
    int i = 3;
    int j = 4;
    int * const p = &i;

    *p = 4; // OK, *p has type 'int', which is not const
    p = &j; // error: assignment of read-only variable 'p'

    int * const q;  // error: uninitialized 'const q'
    ```

    而 `const int * const` 和 `int const * const` 则表示「指向一个不可变的 `int` 的不可变的指针」，指针本身和指向的变量都不能被修改。

这样，我们也很容易理解为什么不存在 `const & const` 这样的东西了——因为引用本身就不能被重新约束。

结合上面的讨论，我们容易理解：引用变量必须被初始化[^ref_init]^[dcl.ref#5](https://timsong-cpp.github.io/cppwp/n4868/dcl.ref#5)^：

```c++
int & bad; // error: declaration of reference variable 'r' requires an initializer
```

??? info
    而且，引用应当被初始化为一个有效的对象或函数的引用^[dcl.ref#5](https://timsong-cpp.github.io/cppwp/n4868/dcl.ref#5)^：

    ```c++
    int * p = nullptr;
    int & r = *p;   // Undefined Behavior
    ```

    没有对引用的引用、没有引用的数组，也没有指向引用的指针[^ref_not_obj]^[dcl.ref#5](https://timsong-cpp.github.io/cppwp/n4868/dcl.ref#5)^。

    [^ref_not_obj]: 因为引用不是对象。

[^ref_init]: `extern` 除外。


---

#### 引用与临时对象

***临时对象***

我们来考虑这么一个问题：

我们之前定义了 `Matrix` 类（本节 `m`, `m1`, `m2` 等均是其对象，后文不再赘述）。回顾我们前面的函数定义，我们有 `Matrix Matrix::operator-(const Matrix & mat);`。那么，我们如果写了这样一个表达式：

```c++
m1 - m2;
```

它会调用 `Matrix::operator-` 并返回一个 `Matrix` 类型的值，这个值是一个临时对象[^tmp]。问题是：这个对象会在什么时候被析构？

答案很简单——在这个表达式结束之后立刻被析构。这么做的原因是直观的：我们此后再也无法访问到这个对象，因为它是一个没有名字的 **临时对象 (temporary object)**。

[^tmp]: 在 C++17 之前，returning a prvalue from a function 会引发 temporary object 的创建 ^[cppref: Temporary object lifetime](https://en.cppreference.com/w/cpp/language/lifetime#Temporary_object_lifetime)^（返回值不为引用类型时，函数调用表达式是 prvalue^[expr.call#14](https://timsong-cpp.github.io/cppwp/n4868/expr.call#14)^）；但在 C++17 之后，仅在需要时才会发生 temporary materialization 从而将 prvalue 转换成 xvalue，同时创建出临时对象^[class.temporary#2](https://timsong-cpp.github.io/cppwp/n4868/class.temporary#2)^。除了一些特殊情况外，临时对象确实在所在完整语句结束时被销毁^[class.temporary#5](https://timsong-cpp.github.io/cppwp/n4868/class.temporary#5)^。请注意，这里的 `m1 - m2` 在 C++17 之后确实不属于比较常见的那种由于将其绑定给一个引用或者访问其内部成员被 materialization 的例子，而是 [[class.temporary#2.6](https://timsong-cpp.github.io/cppwp/n4868/class.temporary#2.6)] 中提到的那样，`m1 - m2` 出现在了一个 **discarded-value expression**^[stmt.expr#1](https://timsong-cpp.github.io/cppwp/n4868/stmt.expr#1),[expr.context#2](https://timsong-cpp.github.io/cppwp/n4868/expr.context#2)^；因此它仍然 materialized 并创建了一个临时的对象。因此它的声明周期仍然到所在完整语句结束时为止。

---

***临时对象的生命周期***

事实上，临时对象会在它所在的 **完整表达式 (full-expression)** 结束时被销毁。所谓完整表达式结束时，大多数情况下就是下一个 `;` 所在的位置[^full_expr]。

[^full_expr]: 常见的反例是 `unevaluated operand` 也是 full-expression，例如 `sizeof` 或者 `decltype` 等的操作数。详见 [[intro.execution#5](https://timsong-cpp.github.io/cppwp/n4868/intro.execution#5)]。

假如我们又定义了一个「打印矩阵」的函数 `void print(const Matrix &);`，显然，如果我们有若干个 `Matrix` 对象 `m1`, `m2`, ...，那么 `print(m1)` 和 `print(m2)` 之类的函数调用都是合法的。

那么，请问：`print(m1 - m2);` 是合法的吗？

答案是肯定的。如我们之前所说，`m1 - m2` 所形成的临时对象会在所在完整表达式结束时，即 `print(m1 - m2)` 运行完成时被销毁。因此在该函数执行过程中，这个临时对象是仍然存在的。

不过，我们考虑这样的情况：

```c++
Matrix m = m1 - m2;
```

根据我们之前所说，`m1 - m2` 得到一个临时对象，这个临时对象会在所在表达式结束时被销毁。而在这个语句中，我们又用这个临时对象构造了一个新的 `Matrix` 对象 `m`。这有些浪费——我们析构了一个对象，同时构造了一个跟它一模一样的对象；如果我们能够延长这个临时对象的生命周期，就可以节约一次构造和一次析构的开销[^rvo]。

[^rvo]: Return Value Optimazation 机制可以解决这个问题。但是在这个问题被讨论之时，还暂时没有 RVO。

因此，C++ 规定：可以将一个临时对象绑定给一个 `const` 引用，这个临时对象的生命周期被延长以匹配这个 `const` 引用的生命周期^[class.temporary#6](https://timsong-cpp.github.io/cppwp/n4868/class.temporary#6)^。例如：

```c++
void foo() {
    const Matrix & m = m1 - m2;     // temporary `Matrix` has same lifetime as `m`
    
    // ...

    // at the end of this function block, the lifetime of `m` ends,
    // so the lifetime of temporary `Matrix` ends, d'tor called.
}
```

---

***临时对象与 non-`const` 引用***

上面将临时对象传递给 `const Matrix &` 参数和用临时对象初始化 `const Matrix &` 的两个例子共同反映了一个事实：我们可以把一个临时对象绑定给一个 `const` 引用。

下一个问题是：我们能否将一个临时对象绑定给一个 non-`const` 引用呢？

答案是不能。我们考虑这样一个情形：

```c++
void incr(int & rr) { rr++; }

void g() {
    double ss = 1;
    incr(ss);       // error since Release 2.0
}
```

如果我们允许临时对象绑定给一个 non-`const` 引用，那么上面的代码会发生这样的事情：`ss` 被隐式转换成一个 `int` 类型的临时对象，这个临时对象被传递给 `incr` 并在其中 `++` 变成 2；`incr(ss);` 结束后临时对象被销毁——这时 `ss` 的值仍然是 `1.0` 而不是 `2.0`，这与直觉不符。

因此，允许将一个临时对象绑定给一个 non-`const` 引用并没有太多的好处，但是会带来一些不慎修改了临时对象引发的错误，这些错误通常十分隐晦。因此，BS 在 Release 2.0 的时候将它修复了——临时对象不允许被绑定给 non-`const` 引用。

[^ref_tmp]: https://stackoverflow.com/a/39719234/14430730

---

#### 引用与重载解析

我们之前提到，重载解析时会在可行函数集中找到一个函数，它优于其它所有函数。那么，这里的「优于」在引用相关的话题中是如何定义的呢？

我们以 `int` 类型为例，其他类型与此类似。

首先，将一个 `int` 类型的变量传递给 `int` 类型的参数和 `int &` 类型的参数的优先级是一样的[^ref_conv]：

[^ref_conv]: 一个变量是一个左值，它传递给 `int` 类型时会经历 `lvalue-to-rvalue conversion` (实际上是 glvalue to prvalue^[conv.lval#1](https://timsong-cpp.github.io/cppwp/n4868/conv.lval#1)^)；而它被绑定给 `int &` 或者 `const int &` 类型时发生的是 reference binding，这不需要任何转换^[over.ics.ref#1](https://timsong-cpp.github.io/cppwp/n4868/over.ics.ref#1)^ (identity conversion == no conversion^[over.ics.scs#2](https://timsong-cpp.github.io/cppwp/n4868/over.ics.scs#2)^)。而 identity 和 lvalue-to-rvalue conversion 都属于转换中的 Exact Match 等级^[over.ics.scs#3](https://timsong-cpp.github.io/cppwp/n4868/over.ics.scs#3)^，因此没有一个比另一个更优。不过，如果某一个参数的唯一区别是 `int &` 和 `const int &`，`int &` 更优。参见正文。

```c++
void f(int x) { puts("int"); }      // Overload #1
void f(int & r) { puts("int &"); }  // Overload #2

int main() {
    int x = 1;
    f(1);       // OK, only #1 valid
    f(x);       // Error: ambiguous overload
}
```

同时，将 `int` 类型的变量传递给 `int` 类型的参数和 `const int &` 类型的参数的优先级也是一样的；而且我们之前讨论过，字面量可以被绑定给 `const` 引用，事实上 `int` 类型的临时变量传递给 `int` 类型的参数和 `const int &` 类型的参数的优先级也是一样的[^ref_conv]：

```c++
void g(int x) { puts("int"); }
void g(const int & r) { puts("const int &"); }

int main() {
    int x = 1;
    const int y = 2;
    g(1);       // Error: ambiguous overload
    g(x);       // Error: ambiguous overload
    g(y);       // Error: ambiguous overload
}
```

不过，如果有两个重载，它们在某一个参数上的唯一区别是 `int &` 和 `const int &`，而 `int` 类型的变量绑定给这两种参数都是可行的，此时 `int &` 的更优^[over.ics.rank#3.2.6](https://timsong-cpp.github.io/cppwp/n4868/over.ics.rank#3.2.6)^：

```c++
void h(int & r) { puts("int &"); }
void h(const int & r) { puts("const int &"); }

int main() {
    int x = 1;          // Overload #1
    const int y = 2;    // Overload #2

    h(1);   // OK, only #2 valid
    h(x);   // OK, #1 called as x -> 'int&' is better than x -> 'const int&'
    h(y);   // OK, only #2 valid
}
```

---

#### 类的引用成员和 const 成员

如我们上面所说，引用和 const 变量都需要在定义时给出初始化。那么如果一个类中有引用或者 const 成员怎么办呢？答案是，就像没有默认（无参）构造函数的子对象一样，必须由 member initializer list 或者 default member initializer 提供初始化。如：

```c++
int global = 10;

class Foo {
    const int x = 4;    // OK
    const int y;        // must be initialized by member initializer list
    int & rz = global;  // OK
    int & rw;           // must be initialized by member initializer list
public:
    Foo(int m, int & n) : y(m), rw(n) {}  // OK
    Foo() : y(0), rw(global) {}           // OK
    Foo() : y(0) {}         // Error: uninitialized reference member in 'int&'
    Foo() : rw(global) {}   // Error: uninitialized const member in 'const int'
};
```

!!! info "为什么 `this` 不是引用？"
    因为有 `this` 的时候 C++ 还没有引用。[^ref_this]

    [^ref_this]: 不过，C++23 的 deducing `this` 机制使得成员函数中可以使用调用者的引用。

??? info "keyword arguments 的替代"
    Keyword arguments 或者 Named Parameter Idiom 是指根据参数的名字而非参数的位置来传参。这种机制在 C 和 C++ 中并不支持，它们只支持按位置传参。Python 之类的语言是允许这种传参方式的，即通过 `f(b = 1)` 之类的写法可以指定 `b` 的值是 `1`。
    
    没有采用这种方案的主要原因之一是，这种特性要求在函数声明和定义中每个参数的名字都必须对应相同；这会引发兼容性问题。这是因为 C 和 C++ 中忽略非定义的函数声明中参数的名字，尤其是有些风格在头文件中使用「长而富含信息」的名字，而在定义中使用「短而方便」的名字。例如：

    ```
    // in foo.h
    int vowelStrings(Container& words, int left, int right);
    // in foo.cpp
    int vowelStrings(Container& w, int l, int r) { /* ... */ }
    ```

    实现类似效果的方案之一是结合 default arguments 和继承；另一种方案是使用类似这样的代码：

    ```c++
    class w_args { 
        wintype wt; 
        int ulcx, ulcy, xz, yz; 
        color wc, bc; 
        border b; 
        WSTATE ws; 
    public: 
        w_args() // set defaults 
        : wt(standard), ulcx(0), ulcy(0), xz(100), yz(100), 
        wc(black), b(single), bc(blue), ws(open) { } 

        // override defaults: 
        w_args& ysize(int s) { yz=s; return *this; } 
        w_args& Color(color c) { wc=c; return *this; } 
        w_args& Border(border bb) { b = bb; return *this; } 
        w_args& Border_color(color c) { bc=c; return *this; } 
        // ... 
    }; 

    class window { 
        // ... 
        window(w_args wa); // set options from wa 
        // ... 
    };

    window w; // default window 
    window w( w_args().color(green).ysize(150) );
    ```

    这种方案利用了将引用作为返回值的机制。这种方法常被称为 method chaining。