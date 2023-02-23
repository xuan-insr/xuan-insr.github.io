我们在 OOP 一节中，讨论封装时介绍了 getters 和 setters：

```c++ linenums="1"
struct User {
private:
    int id, age;
    char* password;
public:
    bool checkPassword(char* pw); // check if pw == password
    void setAge(int v) {
        if (v >= 0)
            age = v;
    }
    int getAge() { return age; }
    // ...
};
```

但是，众所周知，函数调用是有开销的，函数开销主要用来传递参数和获取返回值，需要时还要保存寄存器的值。看下面的例子：

<center>![](2023-02-23-00-42-13.png){width=300}</center>

可以看到，虽然 `int foo(int x) { return add5(x); }` 和 `int foo(int x) { return x + 5; }` 是等效的；但是由于函数调用的存在，其效率是慢的。那么，`getAge()` 作为一个函数，是否也有这种代价呢？

C++ 的设计哲学决定了：不应当因为封装性而带来额外的性能开销。如果 getters 和 setters 的调用也需要额外开销的话，追求效率的程序员就会选择不使用封装。因此这个问题如何解决呢？早在 C with Classes 设计之初，这个问题就通过 **内联替换 (inline substitution)**^[dcl.inline#2](https://timsong-cpp.github.io/cppwp/n4868/dcl.inline#2)^ 被解决了。

内联替换有点类似于 function-like macros^[cpp.replace.general#2](https://timsong-cpp.github.io/cppwp/n4868/cpp.replace.general#2)^，即在函数调用的地方将函数体展开，而不经过函数调用的步骤。作为一个例子，在选择 `-O1` 优化的情况下，上面的代码会变成这样：

<center>![](2023-02-23-01-03-43.png){width=300}</center>

可以明显看到，`foo()` 的计算过程中不再有函数调用出现了。

再举一个例子，如果有这样的代码：

```c++
void swap(int *a, int *b) {
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

void foo() {
    // ...
    swap(a, b);
    // ...
    swap(x, y);
    // ...
}
```

如果 `swap` 函数被内联，那么程序可能会等价于：

```c++
void foo() {
    // ...
    int tmp = a;
    a = b;
    b = tmp;
    // ...
    tmp = x;
    x = y;
    y = tmp;
    // ...
}
```

有了内联替换，getter 和 setter 就不再有额外的开销了：

<center>![](2023-02-23-02-06-15.png){width=300}</center>

!!! note inline end
    内联函数是 C++ 和 C 共同发展的一个例子。在 C89 中并没有内联函数，而 C99 和 C++ 中都有内联函数。

    C++17 开始，`inline` 还被用于变量。我们会在（也许）不远的将来讨论这个话题。

那么，什么样的函数会被内联呢？在 C with Classes 中，只有那些函数体写在类的定义中的成员函数才会被内联。当然，并非所有这样的函数都会被内联，比如如果某个函数是递归的，那么这个函数很可能就没办法被内联。（当然，如果编译器想的话，可以通过递归展开实现内联。）

而在后来的 C++ 中，`inline` 关键字被引入；它用在函数声明中，例如 `inline int foo(int x) { return add5(x); }`。它向编译器表明一个建议：这里应该优先考虑使用内联替换而非通常的函数调用。函数体写在类的定义中的成员函数也会默认有此建议。（但是编译器通常忽略这种建议，而自己选择是否需要内联。例如前面图中 `add5` 那个函数，虽然我们没有写 `inline`，但是编译器仍然决定将它内联。）

显然，内联也是有代价的。如上面的例子所示，内联会在 **每处** 调用被展开，因此如果被内联的函数非常大，则会导致生成的目标代码很大，这会带来内存紧张或者局部性问题；这也可能会对性能产生一定影响。

内联函数是 C 语言中 function-like macros 的一个好的替换。BS 说，C++ 希望「允许用语言本身表达所有重要的东西，而不是在注释里或者通过宏这类黑客手段」。宏是预处理器负责的事情，而非编译器。因此 function-like macros 的重大问题之一是缺乏类型检查，另外会因为括号之类的问题引发困扰。用内联的函数替代 function-like macros 也能够有定义域和访问控制，而这些如果使用宏则需要手动控制甚至没办法实现。

??? info
    内联函数还有相关的很多问题。例如，假如在整个程序中的不同编译单元里，同一个内联函数有不同定义会发生什么事。由于 C++ 允许分别编译，这样的检查是极端困难的。因此，标准规定这种情况是 undefined behavior^[std_citation_needed](../std_citation_needed)^。我们会在未来聊 undefined behavior 相关的问题。

    [这个回答](https://stackoverflow.com/a/1759575/14430730) 指出：Don't add `inline` just because you think your code will run faster if the compiler inlines it. ... Generally, the compiler will be able to do this better than you.

    因此，实际上在现在的 C++ 中，`inline` 比「让一个函数被内联」更重要的作用在于，帮助实现 header-only 的库。