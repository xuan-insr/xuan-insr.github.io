前面我们聊了运算符重载和引用之类的话题。在 C++ 中，对它们的一个经典应用是输入输出流。

在 C 中，大家熟悉的输入输出方式是 `scanf` 和 `printf`，它们对类型的识别并不是静态的，而是动态地根据格式控制字符串中 `%d` 之类的东西处理的，这在带来一些安全问题[^security]的同时还引发了一个重要问题——没有办法支持用户自定义类型。

[^security]: 如 Format String Bugs 等。这不是我们讨论的重点。

在 C++ 中，新的头文件 `<iostream>` (input / output stream) 中提供了两个全局对象 `cin` (char input) 和 `cout` (char output) 用来完成输入输出。举一个例子：

```c++ linenums="1"
#include <iostream>

int main() {
    int x;
    double y;
    std::cin >> x >> y;
    std::cout << "x = " << x << ", y = " << y << std::endl;
    return 0;
}
```

这里的 `std::cin` 中的 `std` (standard) 是对象 `cin` 所处的 **命名空间 (namespace)** 的名字；我们会在后面的章节讨论命名空间；`::` 仍然是我们熟悉的 scope resolution operator。`std::cout` 和 `std::endl` 也类似；其中 `endl` (endline) 是换行[^endl]。

[^endl]: 与直接输出 `'\n'` 的区别是，输出 `std::endl` 会 flush 缓冲区。 

`std::cin >> x >> y;` 表示从标准输入流中读取 `x`，然后读取 `y`，它等价于 `std::cin >> x; std::cin >> y;`。这里的运算符 `>>` 本身的含义是右移，而这里我们通过运算符重载给它赋予了新的语义：从流中提取 (stream extraction)。

`std::cout << "x = " << x << ", y = " << y << std::endl;` 表示向标准输出流中输出字符串 `"x = "`，然后输出 `x` 的值，然后输出字符串 `", y = "`，然后输出 `y` 的值，然后输出换行。`<<` 本来是左移，而这里对各种基本类型重载了 `<<` 运算符，来实现向流中插入 (stream insertion) 的语义。

???+ note "using"
    如果懒得在每一个地方都写 `std::`，可以通过 `using` 语句。例如：

    ```c++
    void foo() {
        using std::cin;
        using std::cout;
        cin >> x;   // std::cin
        cin >> y;   // std::cin
        cout << "x = " << x << ", ";        // std::cout
        cout << "y = " << y << std::endl;   // std::cout
    }
    ```

    这里 `using std::cin` 就表示「若无特殊说明，`cin` 即指 `std::cin`」。

    或者使用 `using namespace std;` 表示「若无特殊说明，这里面不知道是什么的东西去 `std` 里找」：

    ```c++
    void foo() {
        using namespace std;
        cin >> x;   // std::cin
        cin >> y;   // std::cin
        cout << "x = " << x << ", ";   // std::cout
        cout << "y = " << y << endl;   // std::cout, std::endl
    }
    ```

    `using` 语句也属于其作用域，作用范围持续到其所在块结束。将其放到全局，则其作用范围持续到其所在文件结束。

这是如何实现的呢？`std::cin` 的类型是 `std::istream` (input stream)，它其中对各种基本类型重载了 `operator>>`，我们上面使用到的两个分别是：

```c++
istream & istream::operator>>(int & value) {
    // ... extract (read) an int from the stream
    return *this;
}
istream & istream::operator>>(double & value) {
    // ... extract (read) a double from the stream
    return *this;
}
```

函数中如何实现从流中读出数据暂且不是我们所在意的重点。我们关注的是——为什么要返回 `istream &` 类型的对象本身。

我们考虑 `cin >> x >> y;` 的运行顺序。首先 `cin >> x` 被运行，因此这个表达式就类似于 `(cin.operator>>(x)) >> y;`，而 `cin.operator>>(x)` 运行结束后返回 `cin` 本身，剩下的表达式就是 `cin >> y;` 了。因此，返回 `*this` 的好处就是能够实现这种链式的读入。

与 `cin` 类似，`std::cout` 的类型是 `std::ostream` (output stream)，它同样对各种基本类型重载了 `<<` 运算符。一个例子是 `ostream& ostream::opreator<<(int value);`。

前面代码中 `cout` 完成链式输出的具体调用过程留做练习。

知道了这些，我们就能够为自己的类提供对 `>>` 和 `<<` 的重载，从而能够支持用 `cin` 和 `cout` 方便地输入和输出自定义类型了：

```c++ linenums="1"
#include <iostream>
#include <string>

using std::istream;
using std::ostream;
using std::string;
using std::to_string;

class Complex {
private:
	double real, imaginary;
public:
    // ...
    string toString() const;
	friend istream& operator>>(istream& is, Complex& right);
};

string Complex::toString() const {
	string str = to_string(this->real);
	str += " + ";
	str += to_string(this->imaginary);
    str += 'i';
	return str;
}

ostream& operator<<(ostream& os, const Complex& right) {
	return os << right.toString();
}

istream& operator>>(istream& is, Complex& right) {
	char op;
	is >> right.real >> op >> right.imaginary >> op;
	return is;
}

int main() {
    Complex c;
    std::cin >> c;
    std::cout << c;
}
```

这里的 `std::string` 是 C++ 提供的字符串类型，它也是一个类。19 行看到的 `std::to_string` 函数能够（通过重载）把内置类型转换为 `std::string`，而 20~23 行可以看到 `+=` 能够实现字符串的拼接。`operator<<` 同样有针对 `std::ostream` 和 `std::string` 的重载。18 行的 `toString()` 成员函数实现按照 `Complex` 类的对象生成一个字符串。

可以看到，函数头部有一个 `const`，它表示这个函数不会对调用者（`*this`）造成更改；进一步地说，`this` 的类型现在是 `const Complex *` 而不是 `Complex *` 了。我们会在后面具体讨论它的意义。

26 行我们重载了 `operator<<`；由于这个运算符的第一个操作数通常会是 `cout`，但是我们又没法自己改 `std::ostream`，因此我们只能把这个运算符重载函数定义为全局函数。可以看到，这个函数简单地将 `right.toString()` 的结果输出给了 `os`（通常是 `cout`），然后返回了调用者的引用本身。

30 行我们重载了 `operator>>`。它从 `is`（通常是 `cin`）中读取了复数的虚部和实部（以及用一个 `char` 接收了不重要的部分），然后返回了调用者的引用本身。

需要注意的是，`operator>>` 访问了 `Complex` 类的私有成员 `real` 和 `imaginary`，因而必须在 `Complex` 类中声明为友元（第 14 行）；但 `operator<<` 只访问了其公有成员 `toString()`，因此无需设置成友元。

容易看到，`cin` 和 `cout` 的设计使得代码的可读性和可维护性更好，也一定程度上提高了安全性。

!!! tips
    关于 cin 和 cout 还有很多问题没有讨论，例如格式控制、遇到错误输入的处理、流的具体实现等等。作为基本要求，大家能够掌握它们的基本用法即可。感兴趣的同学可以自行寻找资料深入了解。

### ▲ const 和 static 成员

--8<-- "cpp/cpp_restart/appendix/const_static.md"