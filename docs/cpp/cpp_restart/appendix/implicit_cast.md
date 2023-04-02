#### 标准转换 | Standard Conversion

在 C 语言中，我们已经熟悉了 **隐式类型转换 (implicit conversion)** 的含义。隐式转换中的「隐式」代表这种转换是自动发生的，例如我们可以写 `i = 'c';`（其中 `i` 是一个 `int`）而不必写 `i = (int)'c';` 或者 `i = int('c');`。后面两者分别是 C-style cast 和 function-style cast，它们都属于 **显式类型转换 (explicit conversion)**。

作为几个例子（并不完整，我们会在后面的章节完整讨论这个话题）：

- **转换和调整**
    - 数组类型可以转换为指针类型，这称为 **array-to-pointer conversion**，例如函数要求一个 `int *` 参数而我们传递了一个类型为 `int[25]` 的数组时，这个转换发生。
    - 函数类型可以转换为指针类型，这称为 **function-to-pointer conversion**，例如函数要求一个 `void(*)(int)` 
    - 非 `const` 指针可以转换为 `const` 指针，这称为 **qualification conversion**，例如函数要求一个 `const int *` 而我们传递了一个 `int *` 时，这个转换发生。
- **Promotion**
    - 小整数类型能够转换为更大的整数类型，这称为 **integral promotion**，例如 `char` 可以隐式转换到 `int`。
    - `float` 能转换为 `double`，这称为 **floating-point promotion**。
- **Numeric conversions**
    - 任何两个整数类型之间都可以相互转换（可能发生截断），如果不属于 promotion，则属于 **integral conversion**。例如 `long long` 可以隐式转换到 `int`（虽然编译器可能会报 warning）
    - `double` 也能转换为 `float`，这称为 **floating-point conversion**
    - 浮点类型和整数类型之间也可以互相转换（可能发生截断），这属于 **floating-integral conversion**。例如 `int` 可以隐式转换到 `double`，也可以相反
    - 空指针常量可以隐式转换给任何指针类型，任何 `T *` 也可以隐式转换为 `void *`。这称为 **pointer conversion**
    - 整数、浮点数、指针等可以隐式转换给 `bool` 类型，这称为 **boolean conversion**。若原来的值为 `0`，则结果为 `false`；其他任意值结果为 `true`。

上面的隐式类型转换统称为 **standard conversion**。这种隐式转换能够给编写程序带来很多方便，例如我们求一个 `int` 变量的平方根时就不必写 `sqrt(double(i))`，而是直接写 `sqrt(i)` 就可以了。这个过程发生了 `int` 到 `double` 的 floating-integral conversion。

#### 用户定义的转换 | User-Defined Conversion

那我们来考虑这样一个问题！关于我们实现的复数类：

```c++ linenums="1"
class Complex {
private:
	double real, imaginary;
public:
    Complex(double r) : real(r), imaginary(0) {}
    Complex(double r, double i) : real(r), imaginary(i) {}
    friend Complex operator+(Complex, Complex);
    friend Complex operator-(Complex, Complex);
    friend Complex operator*(Complex, Complex);
    // ...
};
```

我们重载了运算符，来实现两个复数之间的加法、减法和乘法。那么问题来了！将复数和实数混合运算是非常正常的事情，比如我们有：

```c++
void foo() {
    Complex c;
    double d;
    // ...
    Complex c2 = c + d; // Complex + double
    Complex c3 = d + c; // double + Complex
}
```

如何解决这个问题呢？

方法之一是，要求调用者显式写出转换（请复习 function-like cast），即 `c + Complex(d)` 和 `Complex(d) + c`，这会调用构造函数来构造出一个临时的 `Complex` 参与运算。不过这会让调用者很困扰！

另一种方法是，为每个运算符写 `Complex, Complex`, `double, Complex`, `Complex, double` 三个版本。这会让代码的可读性和可维护性变差！

为了解决这个问题，C++ 允许从类型 `A` 到类型 `B` 的隐式转换，只要有这样的 **user-defined conversion**。也就是说，除了前面我们提到的 **standard conversion** 之外，用户还可以自定义转换规则。

User-defined conversion 有两种：**转换构造函数 (converting constructor)** 和 **用户定义的转换函数 (user-defined conversion function)**。我们分别讨论这两种东西！

#### 转换构造函数 | Converting Constructor

转换构造函数 **不是** 一种特殊的构造函数，而是构造函数的一种性质。简单来说，凡是没有 `explicit` 说明符的构造函数 **都是** 转换构造函数。我们稍后讨论 `explicit` 的含义。

也就是说，比如我们有构造函数 `Complex::Complex(double r);`，这其实就提供了一种 **隐式转换** 的规则：`double` 类型的变量可以隐式转换成一个 `Complex`。也就是说：

```c++
void g(Complex z, double d) {
    Complex z1 = z + d;     // OK, calls operator+(z, Complex(d));
    Complex z2 = d + z;     // OK, calls operator+(Complex(d), z);
}
```

即，编译器看到现在有一个 `Complex` 和一个 `double` 调用 `operator+`，但是没有找到精确匹配的函数；这时候编译器发现：有一个接收两个 `Complex` 的函数，而又有一个转换构造函数 `Complex::Complex(double r);` 允许我们把 `double` 隐式地转换为 `Complex`，所以编译器决定：先完成这个隐式转换，然后调用。因此实际上调用的就是 `operator+(z, Complex(d))` 了！

???+ note "将运算符重载设为成员还是全局"
    有了这种隐式转换，我们就需要意识到一个问题：如果 `operator+` 是 `Complex` 的一个成员函数，那么上面代码中 `z + d` 仍然可以被当做 `z.operator+(Complex(d))` 来调用，但是 `d + z` 就不能调用 `d.operator+(z)`，因为 `double` 类型中没有这样的函数。如我们之前所说，C++ 不希望给内部类型增加新的运算。

    从这里我们可以知道：如果我们将一个运算符重载设为全局函数能够有更强的逻辑对称性；而将其定义为成员函数则能够保证第一个操作数不发生转换。根据我们之前的讨论，转换得到的是一个临时对象[^conv_tmp]；因此对于那些赋值运算符之类的要求第一个操作数是一个实际存在的对象[^lvalue]的运算符，设为成员是比较好的。

    [^conv_tmp]: 其实转换得到的是一个 prvalue；从 C++17 开始它不一定会产生一个临时对象，但是如果它作为了函数参数那它一定会 materialize 出一个临时对象。

    [^lvalue]: 左值。

    作为一个好的例子：

    ```c++
    class String {
        // ...
    public:
        // ...
        String& operator+=(const String &);
    };

    String operator+(const String &s1, const String &s2) {
        String sum = s1;
        sum += s2;
        return sum;
    }
    ```

作为一个回顾和提示，`Complex operator+(Complex, Complex);` 也可以定义为 `Complex operator+(const Complex &, const Complex &);`，但是不适合定义为 `Complex operator+(Complex &, Complex &);`，因为后者不能支持我们说的隐式转换。请读者自行回顾其原因。

不过，我们考虑这样一个问题。以前面的 `Container` 为例：

```c++
class Container {
    elem* val;
    unsigned size = 0, capa;
    // ...
public:
    Container(unsigned capa) : val(new elem[capa]), capa(capa){}
    // ...
};
```

根据我们之前所说，假如我们有一个函数接收一个 `const Container &`，而我们不慎传进去了一个整数 `1`，则编译器会帮我们生成一个隐式转换 `Container(1)` 构造出了一个临时的 `Container`；又或者我们写出了 `Container c = 1;` 这样的语句，编译器把它解释为 `Container c = Container(1);` 即 `Container c(1);`。如果这些隐式转换并非我们的本意，则它们会给我们带来一些意料之外的情况，而且会让我们 debug 变得困难。

为了解决这个问题，C++ 引入了说明符 `explicit`。如果一个构造函数有 `explicit`，那么它就不是 converting constructor，不能用作隐式类型转换，而只能用作显式类型转换：

```c++ linenums="1" hl_lines="3 16-17"
class Foo {
public:
    explicit Foo(int i) {}
};

class Bar {
public:
    Bar(int i) {}
};

void foo(Foo f);
void bar(Bar b);

int main() {
    Foo f = Foo(1); // OK, explicit conversion
    Foo g = 1;      // Error: no valid conversion
    foo(1);         // Error: no valid conversion
    Bar b = Bar(1); // OK, explicit conversion
    Bar c = 1;      // OK, implicit conversion
    bar(1);         // OK, implicit conversion
}
```

因此，如果不希望前述隐式转换的发生，请将构造函数（尤其是单个参数的构造函数）标记为 `explicit`。

??? note "隐式转换的限制"
    隐式转换限于：首先按一定要求完成 0 次或若干次 standard conversion，然后完成 0 次或 1 次 user-defined conversion；如果完成了 user-defined conversion，还可以完成 0 次或若干次 standard conversion。也就是说，隐式转换不会触发两次 user-defined conversion。作为一个例子：

    ```c++
    class Bar {
    public:
        Bar(int i) {}
    };

    class Foo {
    public:
        Foo(Bar b) {}
    };

    void foo(Foo f);

    int main() {
        foo(Bar(1));    // OK, foo(Foo(Bar(1))), only Foo(Bar) used
        foo(1);         // Error: no conversion from int to Foo
    }
    ```

??? warning
    在 C++11 之前，只有单个参数且没有 `explicit` 的构造函数才是 converting constructor；但是自 C++11 开始引入了 braced-init-list 即 `{}`，有 0 个或多个参数且没有 `explicit` 的构造函数也是 converting constructor 了。参看下面的例子^[Cppref: converting_constructor](https://en.cppreference.com/w/cpp/language/converting_constructor)^：

    ```c++
    struct A
    {
        A() { }         // converting constructor (since C++11)  
        A(int) { }      // converting constructor
        A(int, int) { } // converting constructor (since C++11)
    };
    
    struct B
    {
        explicit B() { }
        explicit B(int) { }
        explicit B(int, int) { }
    };
    
    int main()
    {
        A a1 = 1;      // OK: copy-initialization selects A::A(int)
        A a2(2);       // OK: direct-initialization selects A::A(int)
        A a3{4, 5};    // OK: direct-list-initialization selects A::A(int, int)
        A a4 = {4, 5}; // OK: copy-list-initialization selects A::A(int, int)
        A a5 = (A)1;   // OK: explicit cast performs static_cast, direct-initialization
    
    //  B b1 = 1;      // error: copy-initialization does not consider B::B(int)
        B b2(2);       // OK: direct-initialization selects B::B(int)
        B b3{4, 5};    // OK: direct-list-initialization selects B::B(int, int)
    //  B b4 = {4, 5}; // error: copy-list-initialization selected an explicit constructor
                       //        B::B(int, int)
        B b5 = (B)1;   // OK: explicit cast performs static_cast, direct-initialization
        B b6;          // OK, default-initialization
        B b7{};        // OK, direct-list-initialization
    //  B b8 = {};     // error: copy-list-initialization selected an explicit constructor
                       //        B::B()
    }
    ```

    另外需要提示的是，braced-init-list 并不是一个表达式，因此它出现的位置是有一定限制的。参见 [这个问题](https://stackoverflow.com/questions/51071557/converting-constructor-with-multiple-arguments)。

#### 用户定义的转换函数 | User-defined Conversion Function

前面的 conversion constructor 给定了从一个其他类型到当前类进行隐式或显式转换的方式。不过，有时我们可能也会希望能够将当前类转换为其他类型从而参与计算或者函数调用等。例如：

```c++
class Complex {
// ...
public:
    std::string to_string() const;
    double to_double() const;
    bool to_bool() const;
};
```

我们也许会想通过 `str += c.to_string()` 的方式获取 `c` 转换为 `std::string` 的结果；或者有时我们想要将 `c` 作为判断条件，写出 `if (c.to_bool())` 之类的代码。但是实际上，C++ 提供了机制能够实现从一个类到其他类型的转换，这称为 user-defined conversion function。例如：

```c++
class Complex {
// ...
public:
    operator std::string() const;
    operator double() const;
    operator bool() const;
};
```

事实上，当我们写 function-style cast `bool(c)` 时，这是一个 cast operator，因此 `operator bool()` 其实就是重载了 cast operator。这种重载并不需要写出返回值类型，因为它的返回值类型就是它的 operator 名字。作为一个例子[^cout_string]：

[^cout_string]: 需要注意的是，如果这里 `cout << c` 会发生编译错误。首先由于 `operator double` 是 `explicit` 的，因此它不会被选中；而另一方面，`cout << c` 也不会输出 `std::string`，这是因为 `cout` 对 `basic_string` 的重载需要模板参数，而隐式类型转换在模板参数推导时不会被考虑。参见 [这个问题](https://stackoverflow.com/questions/64310779/why-cant-the-compiler-use-the-stdstring-conversion-function-of-the-class-when)。

```c++
#include <iostream>
#include <string>

using namespace std;

class Complex {
    double r, i;
public:
    Complex(double r) : r(r), i(0) {};
    Complex(double r, double i) : r(r), i(i) {};
    operator string() const {
        cout << "operator string" << endl;
        return to_string(r) + " + " + to_string(i) + 'i';
    }
    explicit operator double() const {
        cout << "operator double" << endl;
        return r;
    }
    explicit operator bool() const {
        cout << "operator bool" << endl;
        return r != 0 || i != 0;
    }
};

void foo(double x) {}

int main() {
    Complex c = 3;      // implicit conversion, calls Complex(3)
    string str = c;     // implicit conversion, calls Complex::string()

    foo(double(c));     // OK, explicit conversion
    foo((double)c);     // OK, explicit conversion
    // foo(c);          // Error: no matching call to 'foo', because no 
                        // implicit conversion from Complex to double

    // bool b = c;      // Error: no implicit conversion from Complex to bool
    if (c) {            // OK, this context considers explicit operator bool
        cout << str;
    }
    return 0;
}
```

上面的例子中也显示了 `explicit` 的意义，即当 `opeator type()` 为 `explicit` 时，这种转换只能用于显式转换而不能用于隐式转换，这和前面的转换构造函数是一致的。

作为一个需要特殊注意的问题，在一些上下文中，类型 `bool` 是被希望的，而且此时即使 `operator bool` 是 `explicit` 的也会被使用。这些上下文包括 `if`, `while`, `for` 的条件、内置逻辑运算符 `!`, `&&`, `||` 的操作数、三元运算符 `?:` 的第一个操作数等[^bool_ctx]。

[^bool_ctx]: 这被称为 [Contextual conversions](https://en.cppreference.com/w/cpp/language/implicit_conversion#Contextual_conversions)。