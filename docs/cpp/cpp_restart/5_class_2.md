# 5 类 (II) - 拷贝构造与拷贝赋值

--8<-- "cpp/cpp_restart/toggle_visibility.md"

!!! warning "本节使用的副本"

## 5.1 拷贝赋值运算符

在上一节中，我们创建了一个「容器」类：

```c++ linenums="1"
class Container {
    elem* val;
    // ...
};
```

我们考虑一个问题：假如有两个 `Container` 的实例 `c1` 和 `c2`，那么 `c1 = c2;` 会发生什么？

很容易理解，在这个赋值表达式完成后，`c1.val` 的值变得和 `c2.val` 一样了；也就是说，这两个容器现在指向同一块内存。

这样的结果会带来两个问题：

1. `c1` 原来的 `val` 也许指向了一块申请来的内存，但是它并没有被释放；
2. 这样的「赋值」实际上完成的是某种「共享」，而并非真正地建立一个副本。如果这并非本意，那么此后对 `c1.val` 的修改对于 `c2` 也可见，且两个对象的析构函数可能会重复析构这块内存，引发错误。

为了解决这个问题，C with Classes 开始就允许用户 **重载赋值运算符**。实现的方法是，在类内声明一个称为 `operator=` 的成员函数。例如：

```c++ linenums="1"
class Container {
    elem* val;
    unsigned size = 0, capa;
    // ...
public:
    Container(unsigned capa) : val(new elem[capa]), capa(capa){}
    ~Container() { delete[] val; }

    void operator=(Container from) {
        delete[] val;
        val = new elem[from->capa];
        for (unsigned i = 0; i < from->size; i++) {
            val[i] = from->val[i];
        }
        size = from->size;
        capa = from->capa;
    }
};
```

上面的实现演示了一个重载 `operator=` 的例子，它将 `from` 中指向的内容拷贝了一份，而非简单地拷贝指针。虽然还有一些问题。在讨论这些问题以及解决方案之前，我们先来看一看这样的运算符重载函数是如何被调用的。

在一个有运算符的表达式中，如果至少一个操作符是某个类的对象[^overload_op_enum]，则由重载解析查找对应的函数。例如 `x = y;` 就会被视为 `x.operator=(y);` 进行查找。

[^overload_op_enum]: class type OR enum type

上面的例子还有一些问题和改进空间：

如果我们写出了 `x = x;` 会发生什么事情呢？容易理解，这时 `this` 和 `from` 的 `val` 是同一个，因此 `delete[]` 在 `new[]` 之后事实上里面的数据已经丢失了。因此我们需要防范这种情况。

另一个问题是，如果 `capa` 和 `from->capa` 的值相同，那就没必要重新开一份空间了。

考虑上述问题，我们可以写出这样的代码：

```c++ linenums="1"
class Container {
    elem* val;
    unsigned size = 0, capa;
    // ...
public:
    Container(unsigned capa) : val(new elem[capa]), capa(capa){}
    ~Container() { delete[] val; }

    void operator=(Container from) {
        if (from->val != val) { // avoid self-assignment
            if (from->capa != capa) {
                delete[] val;
                val = new elem[from->capa];
            }
            for (unsigned i = 0; i < from->size; i++) {
                val[i] = from->val[i];
            }
            size = from->size;
            capa = from->capa;
        }
    }
};
```

结合函数重载，我们也容易理解，`operator=` 同样可以有重载。例如：

```c++ linenums="1"
class Container {
    elem* val;
    unsigned size = 0, capa;
    // ...
public:
    Container(unsigned capa) : val(new elem[capa]), capa(capa){}
    ~Container() { delete[] val; }

    void operator=(Container from);
    void operator=(elem * val) {
        this->val = val;
    }
};
```

虽然这个例子有点不太恰当（因为没有正确处理 `size` 和 `capa`），但是我们仍然能够从中理解：如果有 `Container` 的实例 `c` 和一个 `elem *` 类型的 `ptr`，那么 `c = ptr;` 是合法的，因为它实际上会被解释为 `c.operator=(ptr);`。

[这里](https://godbolt.org/z/jKvvsK8xP) 有一个具体的例子：

<center>![](2023-03-15-16-23-50.png)</center>

与之前的讨论类似，如果用户没有显示地给出 `operator=`，那么编译器会生成一个 public 的默认拷贝赋值运算符的定义；它完成的内容即为将各个成员变量拷贝一遍。

用户也可以将 `operator=` 设置为 `= default;` 或者 `= delete;`。如果 `operator=` 在当前上下文不可见，那么 `a = b;` 这样的表达式非法：

```c++
class Foo { 
    void operator=(Foo){} // private operator=
    void foo() {
        Foo a, b;
        a = b;      // OK, private function available here
    }
};
struct Bar { 
    void operator=(Bar) = delete; // deleted operator=
    void foo() {
        Bar c, d;
        c = d;      // error: use of deleted function 
                    // 'void Bar::operator=(Bar)'
    }
};

void foo() {
    Foo a, b;
    a = b;      // error: 'void Foo::operator=(Foo)' 
                // is private within this context
    Bar c, d;
    c = d;      // error: use of deleted function 
                // 'void Bar::operator=(Bar)'
}
```

## ▲ 运算符重载

既然 `operator=` 可以重载，那么其他运算符可不可以重载呢？答案是肯定的。C++ 希望表达方式是灵活且自由的；对于自定义类型，C++ 希望人们能写出 `F = M * A`，而非 `assign(F, mul(M, A))`。

事实上，C 语言的运算符就在一定程度上做了「重载」。回顾上一节的定义，重载的含义是同一个函数（根据参数列表不同）具有不同的行为。例如，`*` 运算符作为单目运算符时是取值运算符，而作为双目运算符时表示相乘；`+` 运算符在两个算术类型之间表示求和，而对于 `ptr + i` 时其实表示 `ptr + i * sizeof(A)`，其中 `ptr` 的类型是 `A*`。

而 C++ 允许用户重载大多数的运算符从而提高代码的简洁性和可维护性。

考虑一个存放 `M * M` 大小矩阵的类 `Matrix`：

```c++ linenums="1"
const int M = 100;
class Matrix {
    int data[M][M];
    // ...
};
```

那么，我们可能希望它能支持 `Matrix + Matrix`, `int * Matrix`, `Matrix * Matrix` 等操作。根据我们之前处理 `operator=` 的经历，我们容易写出如下的代码：

```c++ linenums="1"
const int M = 100;
class Matrix {
    int data[M][M];
public:
    Matrix operator+(Matrix mat) { /* */ }
    Matrix operator*(int x) { /* */ }
    Matrix operator*(Matrix mat) { /* */ }
};
```

此时，如果我们写 `m1 * m2`，其实就等价于 `m1.operator*(m2)`，就调用我们写的重载了！

这样的实现方式确实能够实现上述操作，但是它限制了我们只能写出 `Matrix * int` 而不能写出 `int * Matrix`，因为后者被解释为 `int::operator*(Matrix)`，但是 `int` 中并没有这样的重载（C++ 也不希望支持给内部类型增加新的运算[^builtin_newop]）

[^builtin_newop]: DnE 3.6.2 中，BS 表示不希望支持给内部类型增加新的运算，因为「C 内部类型之间的转换已经够肮脏了，决不能再往里面添乱」。

如何解决这个问题呢？事实上，运算符重载也可以放在全局，例如：

```c++ linenums="1"
const int M = 100;
class Matrix {
    int data[M][M];
public:
    Matrix operator+(Matrix mat) { /* */ }
    Matrix operator*(int x) { /* */ }
    Matrix operator*(Matrix mat) { /* */ }
};
Matrix operator*(int x, Matrix mat) { /* */ }
```

当 `x * y` 的操作数中有类实例时，则重载解析会尝试将它解释为 `x.operator*(y)` 和 `operator*(x, y)`^[over.binary.general#1](https://timsong-cpp.github.io/cppwp/n4868/over.binary.general#1)^，即 `x` 对应类中的成员 `operator*` 和全局的 `operator*` 都会被纳入候选函数集，然后再根据实际的参数列表完成重载解析：

<center>![](2023-03-15-18-05-58.png)</center>

这里出现了一个问题！上面的函数 `Matrix operator*(int x, Matrix mat)`，我们可能会给出这样的实现：

```c++ linenums="1"
Matrix operator*(int x, Matrix mat) {
    Matrix tmp = mat;   // copy mat
    for (int i = 0; i < M; i++)
        for (int j = 0; j < M; j++)
            tmp.data[i][j] *= x;
    return tmp;
}
```

### 友元

但是，这个函数并非成员函数，因此访问 private 成员 `data` 时会出现错误：

<center>![](2023-03-15-18-10-24.png)</center>

如何解决这个问题呢？事实上，C++ 允许一个类的定义中给一个外部的函数[^friend]「授予」访问其 private 成员的权限，方式是将对应的函数在该类的定义中将对应的函数声明为一个 **友元 (friend)**：

[^friend]: 或者类。

```c++ linenums="1"
const int M = 100;
class Matrix {
    int data[M][M];
public:
    Matrix operator+(Matrix mat) { /* */ }
    Matrix operator*(int x) { /* */ }
    Matrix operator*(Matrix mat) { /* */ }
    friend Matrix operator*(int x, Matrix mat); // Designates a function as friend of this class
};
Matrix operator*(int x, Matrix mat) {
    Matrix tmp = mat;   // copy mat
    for (int i = 0; i < M; i++)
        for (int j = 0; j < M; j++)
            tmp.data[i][j] *= x;        // can access private member Matrix::data
    return tmp;
}
```

这样，这个问题就解决了！

!!! note
    友元只是一种权限授予的声明，而并非类的成员。因此它并不受 access-specifier 的影响。

当然，另一种解决方案是这样的：

```c++ linenums="1"
const int M = 100;
class Matrix {
    int data[M][M];
public:
    Matrix operator+(Matrix mat) { /* */ }
    Matrix operator*(int x) { /* */ }
    Matrix operator*(Matrix mat) { /* */ }
};
Matrix operator*(int x, Matrix mat) {
    return mat * x;
}
```

这种方案复用了 `Matrix::operator*(int)`，这样一方面能提高代码的重用性和可维护性，另一方面又不需要把 `operator*(int, Matrix)` 设置成友元（因为没有访问 private 成员），因此事实上比前面那种解决方案更好。

其他大多数运算符也能重载。对于一元运算符（如作为正负号的 `+`, `-`，以及 `!`, `~`, `++`, `--` 等），`@x` 会调用 `x.operator@()` 或者 `operator@(x)`。如 `-x` 会调用 `x.operator-()` 或者 `operator-(x)`。

??? tips inline end
    不过，BS 说他更愿意用 `operator prefix++()` 和 `operator postfix++()` 的方式处理，虽然有些人不喜欢增加关键字。

一个例外是，`++` 和 `--` 既可以作为前缀，也可以作为后缀；这如何区分呢？由于其他的单目运算符都是前缀，因此 C++ 规定 `Foo::operator++()` 和 `operator++(Foo)` 用来处理前缀的 `++`，而后缀的 `x++` 会调用 `x.operator++(0)` 或者 `operator++(x, 0)`，即作为后缀时，编译器通过让一个额外的参数 `0` 参与重载解析。即：

```c++
Foo operator++(Foo right);      /* prefix  */
Foo operator++(Foo left, int);  /* postfix */

class Bar {
    Bar operator++();       /* prefix  */
    Bar operator++(int);    /* postfix */
};
```

??? info "一些限制"
    这些运算符不能被重载：`::` (scope resolution), `.` (member access), `.*` (member access through pointer to member), and `?:` (ternary conditional) 

    对 `=` (assignment), `()` (function call), `[]` (subscript), `->` (member access) 的重载 **必须是成员**

    ???+ info "上面这条的原因"
        Release 2.0 开始要求 `operator=` 必须是成员，因为：

        ```
        class X {
            // no operator=
        };

        void f(X a, X b) { 
            a = b;  // predefined meaning of =
        }     

        void operator=(X&, X);  // disallowed by 2.0

        void g(X a, X b) {
            a = b;  // user-defined meaning of =
        }
        ```

        即，上面这样的代码会造成混乱。其他赋值运算符因为没有默认的定义，因此不会引起这个问题。

        文中还讨论了 `[]`, `()`, `->` 必须是成员的原因。BS 解释说「这些运算符通常要修改第一个 operand 的内部状态」，不过他也说「这也可能是不必要的谨小慎微」。[这里](https://stackoverflow.com/questions/3938036/rationale-of-enforcing-some-operators-to-be-members) 提到，BS 本人现在可能也觉得不太合理，但是没空改。

    不能添加用户自定义的运算符。重载运算符也不能修改运算符的优先级、结合性和操作数数目。

    除了函数调用运算符 `operator()` 以外的运算符重载不能包含 default arguments。

    对 `&&` 和 `||` 的重载将不再会有 short-circuit evaluation。

    ^[over.oper.general](https://timsong-cpp.github.io/cppwp/n4868/over.oper.general)^

### ▲ 引用

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

一个引用是一个已经存在的对象或者函数的别名。

[^algol_ref]: 作为一个改进，C++ 不允许改变一个引用所引用的东西（也就是不允许重新约束），绑定只能发生在初始化时。

讨论 [keyword arguments](../notes/dne_notes/#651-keyword-arguments)

讨论类中引用成员的初始化

### ▲ 隐式类型转换

## ▲ I/O stream

## 5.1 拷贝赋值运算符 (Cont.)

现在的拷贝赋值运算符长啥样

## ▲ const 类型

为什么要有 const

## 5.2 拷贝构造函数

## 5.3 Special Member Functions

总结除了 move ctor 和 move assignment

[special](https://timsong-cpp.github.io/cppwp/n4868/special)

## 5.4 new 和 delete

malloc 和 free

---

--8<-- "cpp/cpp_restart/toggle_visibility.md"