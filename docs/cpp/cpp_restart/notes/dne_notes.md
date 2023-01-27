# The Design and Evaluation of C++ 阅读记录

!!! abstract
    阅读 Bjarne Stroustrup 的 The Design and Evaluation of C++ 过程中的一些摘录。

### 前言

C++ 和造就它的设计思想、编程思想自身不会演化，真正演化的是 C++ 用户们对于实际问题的理解，以及它们对于能够帮助解决这些问题的工具的理解。因此，本书也将追溯人们用 C++ 去处理各种关键性问题，以及实际处理那些问题的人们的认识，这些都对 C++ 的发展产生了重要影响。

### 0 致读者

……一个通用程序设计语言必须同时是所有这些东西，这样才能服务于它缤纷繁杂的用户集合。

一种通用程序设计语言必须是折中主义的，需要考虑到许多实践性的和社会性的因素。

---

## 第一部分

!!! abstract
    我读完这一部分得到的收获是：了解了 C++ 设计和发展的一些规则和哲学，了解到了一些特性诞生的原因和过程，理解了那些规则对于 C++ 发展的影响，以及对于「C++ 解决什么问题」这个讨论的影响。

### 1 The Prehistory of C++

1.1 指出，Simula 的类和协程机制给出了好的表达能力，在此基础之上的类型检查等使得错误更易排除。但其构建和运行表现很差。这使 BS 发誓「在没有合适工具的情况下绝不去冲击一个问题」。 

1.2 提到 C 语言是 BS 比较欣赏的系统程序设计语言。

??? quote
    尊重人群而不尊重人群中的个体，实际上就是什么也不尊重。(P25)

### 2 C with Classes

#### 2.1~2.3 诞生

2.1 指出，BS 遇到了「在没有合适工具的情况下绝不去冲击」的问题。鉴于 1 中提到的原因，他设计了一个预处理程序 Cpre（1981/12 首次发布），来将 C with Classes 处理成 C。此后也从思考一种 **工具** 发展成了思考一种 **语言**。

- C with Classes 和 C++ 的「class」来自 Simula。
- 设计的 private 和 public 是 compile-time access control
- 和 C 一样，对象分配有 3 种形式：在栈上的 automatic stroage，在固定地址的 static storage 和在堆上的 dynamic storage

#### 2.4 效率

- Simula 的 class type 的对象都是 dynamic allocated 的，这是 Simula 慢的重要原因。
- C with Classes 希望让对内部类型的支持也能用于自定义类型。事实上，C++ 现在对自定义类型的支持比内部类型还多。
- C with Classes 初始版本没有 inline，但是很快就加上了，因为如果没有 inline，getter 和 setter 之类的函数有额外代价，人们就不会愿意封装。
- C with Classes 中只有函数体放在 class 声明中的成员函数才能被 inline。
- C with Classes 直到 C++ 的一条设计规则是，如果要引入一个 feature，需要有立即的、普适的 affordability。
- 关键字 `inline` 和允许非成员 inline 函数都是后来 C++ 提供的。`inline` 只是个提示。

#### 2.5 链接模型

2.5 指出，C 和 C++ 都是按名等价的，但 layout capability rules 允许了 low-level 的强转。这也发展出了 C++ 的 one definition rule，即 func, var, type 等的定义均应唯一。

C with Classes 的对象结构和 struct 一样，函数不在其中。

`this` 来自 Simula。当时 C++ 还没有引用，因此是个指针。

#### 2.6 静态类型检查

2.6 讨论了静态类型检查。早期 C with Classes 试图禁止 narrowing implicit conversions，但是失败的很惨，因为大家都这么用。于是 BS 选择使用 warning，但是对于 `int->char` 这种过于常用的转换，不报 warning。他希望 warning 只用在「有超过 90% 的可能是捕捉到实际错误」的情况。

#### 2.7 为什么是 C

2.7 指出了构造在 C 之上的一些理由。例如其灵活（通用）、高效、各种平台都有 C 编译器、可移植。他指出了一些灵感来源： Simula 提供了 class，Algol 68 提供了运算符重载、引用以及可以在块中任何地方声明变量的能力，BCPL 提供了 `//` 的注释形式。

他指出，希望 C++ 一方面能够像 C 一样接近机器，另一方面又能接近需要解决的问题。

1985 年之后，C++ 受到了来自 Ada 的模板、异常、namespace，以及 Clu 和 ML 的异常的影响。

#### 2.8 语法问题

2.8 提及了 C 语言语法的缺陷是否有被解决。BS 指出他试图修改省略类型描述符并默认为 int 的语法（例如 `f();` 表示声明一个返回值为 `int` 的函数 `f`），但是遭到了反对，就退了回来，直到十年后标准反对了这种写法。BS 还指出他试图修改 C 语言「让名字的声明模仿其使用」的语法（例如 `int *p[10];`, `int (*p) [10]`），但是最后没改。

他同时提及了 C with Classes 希望让用户定义的类型不是二等公民，所以在向 C++ 演化时 class, union, struct 的名字前面不再需要加这些语法标识符了。带来的一个问题是，`struct S {int a}; int S;` 这样的东西在 C 中是合法的。为了保持兼容性，C++ 的解决方案是，一个名字可以同时指称一个 class，同时也可以指称一个 var / func；但是如果确实同时指称了这两种，那么除非显式加了关键字 class, union, struct，否则指称的是那个 var / func。

#### 2.9 派生类

C++ 的 derived class 和 Smalltalk 中的 sub class 的概念都来自于 Simula，不过 BS 认为 derived/base 相比于 sub/super 更容易理解。

C with Classes 最初没有虚函数，因此没有任何形式的运行时支持。也没有模板，因此想实现容器等类型泛型时，采用宏来实现。[这里](https://belaycpp.com/2021/10/01/history-of-c-templates-from-c-style-macros-to-concepts/) 有一篇相关的文字。

#### 2.10 The Protection Model

保护的单位是 class。基本规则是，只有类的拥有者放置的类声明内部的声明才能授予访问权。默认所有信息都是 private 的。访问权的授予方式是 public 或者 friend。

从 C with Classes 开始，派生关系就存在 private / public 的区分，其含义即为规定基类的可见性。private 继承的应用场景之一是，基类是一个 interface，派生类是其一个实现，但是派生类并不愿意让用户访问所有基类的所有 public 接口。

如果基类有一个 public 的 `T foo(...)` 成员函数，即使是 private 继承，也有办法使用比 `T foo(...) { return Base::foo(...); }` 更优雅的方式达到暴露出某个接口的效果。C with Classes 中是在子类中添加一条 public 的 `Base.foo;`，而现在的 C++ 则使用 `using Base::foo;`。

这种保护模式一直延续到了现在的 C++。保护是编译时的，因此事实上运行时是有可能绕过保护的（因为它是为了防止意外而非欺骗）。另外，受控的是访问权而非可见性，这是一个例子：


```c++ linenums="1"
int a;

class X {
private:
    int a;
};

class Y : public X {
    void f() { a = 1; }
};
```

受控的是访问权而非可见性的含义是，虽然 `X::a` 是 private 的，但是这不影响第 9 行的 `a = 1;` 能够看到它。因此这里会出现一个编译错误，而不是访问到第 1 行的全局的 `a`。

#### 2.11 Runtime Guarantees

2.10 的访问控制提供了防止非法访问的保证。而 2.11 介绍了 Special Member Functions 提供的另一些保证，例如对象被构造过；其他成员函数就可以依赖这些保证。

C with Classes 有构造函数和析构函数作为上述的 SMFs 之一，这两个函数最开始分别叫 `new()` 和 `delete()`。同时，为了保证动态分配的对象调用构造函数，C with Classes 引入了 `new` 运算符；`delete` 运算符与之对应。

C with Class 的 SMFs 中还有 call function 和 return function，前者是调用每个成员函数（除了构造函数）前都隐式调用的函数，后者是从每个成员函数（除了析构函数）返回前都隐式调用的函数。一个例子是，monitor 可以用这两个函数实现同步：

```c++
class monitor : object {
    /* ... */
    call()      { /* grab lock */ }
    return()    { /* release lock */}
    /* ... */
};
```

但是 BS 发现除了他自己以外没人用，于是后来就去掉了。

#### 2.12 次要特性

C 语言的赋值语义 (bitwise copy) 对于 vector 之类有 nontrivial representation 的类是不正确的，因此 C with Classes 允许程序员自己描述拷贝的意义，即允许其定义一个 `void operator = (X *);` 的函数。

C with Classes 也提供了 default arguments。

这两者是 C++ 中重载机制的前驱。在重载机制引入后，default arguments 实际上已经是多余的了。

#### 2.13 Features Considered, but not Provided

虚函数、static member、模板、多继承考虑了，在后面的 C++ 中实现了。

BS 认为 C++ 不应当有自动的 GC。还考虑了支持并发，但是他更倾向于基于库来实现。

### 3 The Birth of C++

3.1 聊了 C with Classes 不足够好的原因，以及 C++ 名字的由来。

3.2 讨论了「用户会是哪些人」「他们使用什么样的系统」「作者如何避免负责提供工具」，从而讨论「这些问题将如何影响语言的定义」。最后一个问题的结论是，C++ 不能带有特别复杂的编译的或运行时的 feature，同时必须能使用原来的链接器，并且产生的代码一开始就要和 C 的一样高效。

#### 3.3 Cfront

Cfront 是 1982~83 年 BS 设计的 C++ 前端（那时候 C++ 还叫 C84），它是一个完整的编译器前端，负责语法和语义的分析和检查，在 1984/8 首次发布。源代码会先通过预处理器 Cpp 完成预处理，然后交给 Cfront 检查并生成 C 代码。生成 C 代码是为了可移植性的保证。

C++ 的一个目标是替代 C 语言对预处理器的使用，因为 BS 认为这种操作容易产生错误。

BS 提到最开始他希望用递归下降分析来做 Cfront，但是咨询了专家后选择了 YACC。但他认为这是个错误，因为当时甚至没有 C 的 LALR(1) 文法；最终实现的结果也是在 YACC 的基础上用很多基于递归下降的技巧来补充。他认为在当时为 C++ 写一个好的递归下降分析器是完全可能的。

BS 还提及了当时链接器对标识符字符数的限制带来了一些麻烦。

本节还提及了 Release 1.0 ~ 3.0 相关的简单历史。

---

3.4 提及了 C++ 在 C with Classes 之上的特性，分别在 3.5 ~ 3.10 展开讨论。此外，2.11 提到的 call / return function 被去掉了。

#### 3.5 虚函数

虚函数是从 Simula 里学来的。BS 还提到，他有意不把 Simula 中的 `INSPECT` 语句引入 C++，因为他希望鼓励人们使用虚函数来实现模块化；虽然之后 C++ 还是添加了 RAII 机制。

!!! danger "TODO"
    3.5.2 介绍了类似下面的代码，其表述是「Cfront 2.0 和更高版本会给出警告」，但实际测试时并没有；同时根据 3.5.3 的描述，派生类中的名字会屏蔽基类中同名的任何对象或者函数；但是我不知道这些东西在现在的版本有没有变化。虽然根据结果，我能大概猜到现在编译器的行为，但是我还没有找到 standard 里的具体说明：

    ```C++
    #include <iostream>
    using namespace std;

    class Base {
    public:
        virtual void g(int) {
            cout << "int" << " ";
        }
    };

    class Derived : public Base {
    public:
        void g(char) {
            cout << "char" << " ";
        }
    };

    int main() {
        Base *b = new Derived;
        b->g('a');
        b->g(1);
        Derived *d = new Derived;
        d->g('a');
        d->g(1);
    }
    ```

    输出是 `int int char char `。

    3.5 的部分内容还没有完全理解。有空具体看一下 [overload resolution](https://en.cppreference.com/w/cpp/language/overload_resolution) 吧（我也不知道是不是应该从这里看）

    11~14章好像有关于此的更多讨论。

#### 3.6 重载

BS 陈述了引入重载之前的犹豫，即讨论了实现难度、（在手册中的）定义难度、效率问题和阅读难度，并确定了这些不是问题。「一种 feature 能够怎样被用好，要比它可能怎样被用错重要得多。」

这里提及了隐式类型转换的意义。例如：

```c++ linenums="1"
class complex {
    // ...
public:
    complex(double);
    complex(double, double);

    friend complex operator+(complex, complex);
    // ...
};

void f(complex z1, complex z2) {
    complex z3 = z1 + z2;   // operator+(z1, z2);
}

void g(complex z, double d) {
    complex z1 = z + d;     // operator+(z, complex(d));
    complex z2 = d + z;     // operator+(complex(d), z);
}
```

可以看到，由于第 4 行的构造函数的存在，我们允许了 `double` 到 `complex` 的隐式转换，因此第 16 和 17 行的操作可以完成。如果不支持隐式转换，那么我们可能要写 `operator+` 的 `complex, complex`, `double, complex`, `complex, double` 三个版本。

当然，为了防止意外的隐式转换，例如为了防止 `vector<int> v = 7;` 被理解成 `vector<int> v(7);`，1995 年，C++ 引入了关键字 `explicit`。声明为 `explicit` 的构造函数只能用于显式的对象构造，不能用于隐式转换。

3.6.2 讨论了把运算符重载设置成成员还是友元。一个区别是，如果是成员的话，上面代码第 16 行调用的是 `z.operator+(complex(d))`；而 17 行的则无法完成，因为它需要调用 `d.operator+(z)`，而 `double` 类型本身没有这个函数。BS 表示不希望支持给内部类型增加新的运算，因为「C 内部类型之间的转换已经够肮脏了，决不能再往里面添乱」。

也就是说，定义为全局函数可以使得运算符的参数更具有逻辑对称性；而定义为成员成员函数则能保证第一个 operand 不发生转换，这与第一个 operand 需要为左值的运算符是比较契合的，例如赋值运算符。因此 `+=` 之类的赋值运算符最好被定义为成员函数。文中也指出，`+=` 之类的赋值函数相对于 `+` 来说更为基本，因此可以在成员中定义 `+=`，而在全局使用 `+=` 来定义 `+`。这样 `operator+` 甚至不需要被定义为友元：

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

BS 还讨论了 Release 2.0 要求 `operator=` 必须是成员的原因：

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

3.6.3 讨论了 Operator Functions，也就是 user-defined conversion functions，使得一个类可以隐式转换为其他类型。例如：

```c++
class String {
    // ...
    operator const char * ();
    // ...
};
```

这样，`String` 类型的对象就可以隐式转换为 `const char *` 了。

3.6.4 讨论了运算符重载和把运算符当做函数调用的效率问题。他指出，主要的效率问题是 inline 和避免多余的临时变量；前者是容易解决的，而后者在此后也实现了。

3.6.5 简单讨论了不支持用户自定义运算符以及改变已有运算符的操作数数目、结合性或优先级的原因。

#### 3.7 引用

引用机制的引入主要是用来支持运算符重载的。也就是说，C 语言本身的参数传递都是按值传递；对于大对象，我们本来可以通过传递指针的方式来减少不必要的拷贝。但是，在运算符重载的场景，我们不希望要求程序员把 `b - c` 写成 `&b - &c`，一方面是不自然，另一方面是指针相减在语言中已有意义。在此场景下，BS 将 Algol 68 中的引用引入了 C++。作为一个改进，C++ 不允许改变一个引用所引用的东西（也就是不允许重新约束），绑定只能发生在初始化时。

BS 陈述他翻过一个严重错误，即允许用非左值初始化非 const 引用。例如：

```c++
void inc(int &v) { v++; }

void g() {
    double x = 1.0;
    inc(x);
}
```

由于 int& 不能直接引用 double，因此会发生一次隐式转换生成一个临时变量，这样 int& 引用的就是这个临时变量了。

允许用非左值初始化引用的本意是让被调函数负责设计按值传递还是按引用传递，调用方无需关心。Release 2.0 之后，为了修正上面的问题，非左值只能用来初始化 const 引用了。

本节还讨论了能否给 `operator[]()` 的读操作和写操作赋予不同语义；例如能否让 `s1[i] = s2[j];` 这样的表达式中的 `operator[]()` 对被写的字符串 `s1` 和被读的字符串 `s2` 执行不同的操作。不过最后的决定是语言本身没有支持，可以通过返回一个辅助类来实现。

---

**3.8 常量** 讨论了常量的诞生。**3.9 存储管理** 讨论了 `new` 的优点，提及了 `new` 调用的 `malloc()` 的效率问题，具体解法在第 10 章讨论。**3.10 类型检查** 中提到，类似 `int printf(const char *, ...)` 中的 `...` 是「函数声明中的特殊描述形式，用来抑制对最后一些参数的检查」；后文中也提到，这其实是类型不安全的。

**3.11 次要特性** 描述了一些其他特性：例如 BCPL 风格的注释 `//`；构造函数和析构函数的记法由 C with Classes 的 `new` 和 `delete` 改为了现在的 `X()`, `~X()`，其中 `~` 是 C 语言中求补的运算符，同时构造和析构函数也可以定义为 private 的了（以前是默认 public）；引进了 `::` 用来表示类的成员关系，而 `.` 用来表示对象的成员关系；

3.11.4 讨论了静态对象的初始化问题，例如 `cin` 和 `cout` 的初始化。C 语言在 `main` 之前会初始化好 `stdin` 和 `stdout`，而其 `exit()` 中也会把这些关闭。C++ 中静态对象初始化的问题核心在于，这些对象可能要调用其构造函数；而构造函数的参数有可能是其他函数的运行结果；那些函数甚至可能处于其他编译单元中。因此其初始化（以及析构）顺序可能是重要的。

#### 3.11.5 声明语句

C++ 从 Algol 68 中吸收了一个概念，即允许把声明写在需要它的任何地方。这对于引用和常量来说是必然的，因为它们都不能赋值；而这对于那些默认初始化方式代价高的类型，会有更高的效率。这种方案也能减少未初始化变量带来的问题。

未初始化变量存在的典型情况还有：

1. `int i = 0; for (i = 0; i < MAX; i++) // ...`
2. `int i; cin >> i;`
3. `int i; if (i = getint()) // ...`

2 的情况并没有得到解决。

为了解决 1 的情况，`for` 语句的 `init-statement` 除了 `expression-statement` 之外，还支持 `simple-declaration`，即 `for (int i = 0; i < MAX; i++)`。

为了解决 3 的情况，`if` 语句的 `condition` 除了 `expression` 之外，还支持 initialized declaration (值是其初始值 contextually converted to bool 的结果[^stmt.pre#6])，即 `if (int i = getint())`。（C++17 开始 `if` 语句也有 `init-statement` 了。）

[^stmt.pre#6]: https://timsong-cpp.github.io/cppwp/n4868/stmt.pre#6

### 4 C++ Language Design Rules

（只是一些我觉得重要、有共鸣且不完全熟悉的内容的摘录）

C++ 和 C 不应当存在无故的不兼容性。

C++ 要求特性是当前可用的。而随着可用的计算机资源增多，异常处理和 RAII 在今天已经被考虑了。

C++ 不试图强迫人做什么。因为程序员总能找到某种方法绕过他们觉得无法接受的规则和限制。

C++ 能够作为一种「高级汇编语言」，同时也能支持数据抽象和面向对象程序设计。

C++ 希望「允许用语言本身表达所有重要的东西，而不是在注释里或者通过宏这类黑客手段」。

C++ 要求禁止隐式地违反静态类型系统。

C++ 希望加强局部性，而这是在 C 中很欠缺的，例如全局变量对外可见、宏处理、缺乏访问控制等。

C++ 希望避免顺序依赖性，即交换两个声明尽可能不要导致不同的含义。

C++ 希望对不用的东西不需要付出代价；否则对于那些 low-level 和高性能的应用而言，C 会成为比 C++ 更好的选择。

### 5 Chronology 1985-1993

### 6 Standardization

标准是「在程序员和语言实现者之间的一个协议」，它不仅描述什么是合法的源代码，还要说明哪些东西会是和具体实现有关的。

与理解一个标准允诺了什么相比，理解它不能保证哪些东西同样甚至更加重要。

6.3.1 讨论了 lookup 过程中的一些问题，6.3.2 讨论了临时变量的生命周期的问题；挺有意思的，但是懒，就不记过来了。

6.4 讨论了 C++ 的扩充及其评价准则。这里提到使用 using 而不是 use、namespace 而不是 scope 的原因就是让新关键字尽可能不与现存的标识符冲突。

6.5.2 讨论了 restricted pointers 没有被采用的原因。这个特性来自 Fortran：Fortran 允许编译器假定函数的传入作为参数的两个数组之间没有重叠。而对于 C++ 来说，这个假定并不存在；但也因此损失了一些优化。不过，最终委员会认为这种机制是不够安全的，而且其使用主要集中在特定领域；这类优化应该用非标准的特殊扩充来实现。也就是说，C++ 希望通过具有普遍意义的机制支持抽象的思想，而不是通过专用机制去支持特定的应用领域。

#### 6.5.1 Keyword Arguments

6.5.1 讨论了 Keyword Arguments 这个特性没有被采用的原因。这个特性就是 python 那种可以按参数名字传参的语法。没有采用这种方案的主要原因之一是，这种特性要求在函数声明和定义中每个参数的名字都必须对应相同；这会引发兼容性问题。尤其是有些风格在头文件中使用「长而富含信息」的名字，而在定义中使用「短而方便」的名字。

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

### 7 Interest and Use

这里 BS 建议，如果对 C 和 C++ 都不了解，那就先学 C++，因为 C++ 的 C 子集 (better C) 对于新手是比较好学的，而且比 C 本身容易使用。

BS 认为最安全的方式是自下而上地学习 C++，即先学习 C++ 所提供的传统的过程性程序设计特征，然后在学着使用和遵循那些数据抽象特征，再然后学习使用类来组织。

BS 指出，学过 C 的程序员可能会认为 better C 是熟悉的从而跳过这些部分，但这样会错过一些内容。C++ 并不只是用新语法表述一些老概念。

BS 还指出，学习 C++，最根本的是学习编程和设计技术，而不是语言细节。

C++ 的设计是为了作为一种系统编程语言，为了开发由系统部件组成的大型应用。

### 8 Libraries

8.3.1 讨论了 I/O stream 库。这个库产生的意义，一方面是为了解决 `printf()` 之类的函数依赖于未经检查的参数的类型不安全问题；另一方面是为了解决用户定义类型没有 `printf()` 理解的输出格式描述符的问题。

### 9 Looking Ahead

9.3.2 节提到了 C++ 解决的问题。

其中指出，「C++ 是目前能用的最好的低层程序设计语言」，因为它结合了 C 在这个领域的优势，同时又能在不付出额外的运行时间和空间代价的前提下完成简单的数据抽象。在这个领域里，C++ 充当的是 better C 的角色。因此也必须小心，不能把 C++ 语言或者它的实现变成 **仅仅** 是一种高级语言。同时，C++ 提供的数据抽象和面向对象的功能也直面了高层系统程序设计的要求，从而适应程序迅速增长的规模和复杂性。另外，C++ 是一个语言而不是一个系统，因此它有能力去适应各种特殊的系统（例如嵌入式系统），为特殊的执行环境生成代码。

## 第二部分




*[BS]: Bjarne Stroustrup
*[SMFs]: Special Member Functions
*[GC]: Garbage Collection