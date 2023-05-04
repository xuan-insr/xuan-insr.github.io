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
    友元只是一种权限授予的声明，友元函数并非类的成员。因此它并不受 access-specifier 的影响。

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

--8<-- "cpp/cpp_restart/appendix/references.md"

### ▲ I/O stream

--8<-- "cpp/cpp_restart/appendix/iostream.md"

### ▲ 隐式类型转换 | Implicit Conversion

--8<-- "cpp/cpp_restart/appendix/implicit_cast.md"