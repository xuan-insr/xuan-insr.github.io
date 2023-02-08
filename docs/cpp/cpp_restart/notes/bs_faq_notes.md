# Bjarne Stroustrup's FAQ 阅读记录

- [Bjarne Stroustrup's FAQ](https://www.stroustrup.com/bs_faq.html)
- [Bjarne Stroustrup's FAQ2](https://www.stroustrup.com/bs_faq2.html)

类的存在使得数据和函数之间的关系更加清晰，同时提供更加清晰的接口。  
类的存在使得接口的具体实现可以被隐藏。  
如果接口的具体实现不应被隐藏，那么可以提供一个 POD (plain old data) structure，用户可以对其做任何操作。

OOP 是一种强调 encapsulation, inheritance 和 polymorphism 的编程范式；对于 C++ 而言，上述三点对应着 classes, derived classes & virtual functions，即 OOP 意味着将类结构化，并使用虚函数来实现对数据的操控和通过继承扩展代码。C++ 从 Simula 中继承了这些观念。  
虚函数可以使得到运行时再隐式地选择接口正确的具体实现，这有时也被称为 run-time dispatch 或者 dynamic dispatch。需要使用虚函数的原因是 C++ 默认 early / static binding。  
OOP 并不是万能的。如果问题本身不具备继承的结构，使用 OOP 是没有必要的。对于这些情况，单独的类、单独的函数，或者泛型编程可能更加适合。

泛型编程是基于「参数化 (parameterization)」的一种编程范式，我们可以将一个类型或者一个算法参数化，从而将一种数据结构或者算法一般化。  
泛型编程相对 OOP 更加灵活，它并不依赖继承的结构。OOP 有时被描述为 "ad hoc polymorphism"，而泛型被称为 "parametric polymorphism"，泛型相较于 OOP 更加结构化（更加抽象）。  
对于 C++ 而言，泛型编程的解析均发生在编译时（因此也被称为 static / compile-time polymorphism），并不需要运行时的 dispatch；因此对于那些对运行时性能要求较高的程序，泛型编程往往更受欢迎。  
泛型编程也不是万能的，在一些继承结构明显的情况下使用 OOP 比泛型更加方便和自然。而且除了类似写库之类有参数化需求的情况以外，泛型编程可能也并不完全需要。

自 1987 年左右，C++ 及其编程风格开发的重点转向了模板、static polymorphism、泛型编程和多范式编程。

多范式编程在不同的场景下使用不同的编程方式，例如在需要动态解析类型时使用 OOP，而在静态类型安全和运行时性能比较重要时使用泛型。

C++ 有指针、数组、casts 之类的 low-level features，它们对 close-to-the-hardware work 来说是必要的；同时，C++ 也提供了各种容器之类的东西可以避免使用上述东西，这可以让程序更加高效和安全。

Empty class 的大小不是 0，而是 1 字节；这是为了保证两个不同对象的地址不同。但是，如果一个 class 继承一个 empty class，那么并不需要额外的 1 字节。

当类里包含一个  
`virtual`-ness propagates to derived classes: 
> 12.4.7: "If a class has a base class with a virtual destructor, its destructor (whether user- or implicitly- declared) is virtual."


Deleting an object through pointer to base invokes undefined behavior unless the destructor in the base class is virtual.

**Why doesn't overloading work for derived classes?**  
That question (in many variations) are usually prompted by an example like this:
```cpp
#include<iostream>
using namespace std;

class B {
public:
    int f(int i) { cout << "f(int): "; return i+1; }
    // ...
};

class D : public B {
public:
    double f(double d) { cout << "f(double): "; return d+1.3; }
    // ...
};

int main()
{
    D* pd = new D;

    cout << pd->f(2) << '\n';
    cout << pd->f(2.3) << '\n';
}
```
which will produce:
> f(double): 3.3 	
> f(double): 3.6

rather than the
> f(int): 3 	
> f(double): 3.6

that some people (wrongly) guessed.  
In other words, there is no overload resolution between D and B. The compiler looks into the scope of D, finds the single function "double f(double)" and calls it. It never bothers with the (enclosing) scope of B. In C++, there is no overloading across scopes - derived class scopes are not an exception to this general rule.  
But what if I want to create an overload set of all my f() functions from my base and derived class? That's easily done using a using-declaration:
```cpp
class D : public B {
public:
    using B::f;	// make every f from B available
    double f(double d) { cout << "f(double): "; return d+1.3; }
    // ...
};
```
Give that modification, the output will be
> f(int): 3 	
> f(double): 3.6

That is, overload resolution was applied to B's f() and D's f() to select the most appropriate f() to call.

[https://www.stroustrup.com/bs_faq2.html#generics](https://www.stroustrup.com/bs_faq2.html#generics)：  
**模板 （templates）本应被设计为“泛型（generics）”那样吗？**  
非也。generics 其实是为抽象类而设的语法；亦即，利用 generics（无论是 Java generics 或 C# generics），你从此不再需要定义精确的接口，但相对地，你也要为此付出诸如虚函数调用以及/或者动态类型转换的花销。  
Templates 通过其各种特性的组合（整型模板参数（integer template arguments）、特化（specialization）、同等对待内建/用户定义类型等），可支持泛型编程（generic programming）、模板元编程（template metaprogramming）等。Templates 带来的灵活性、通用性，以及性能都是“generics”不能比美的。STL 就是最好的例子。  
不过，Templates 带来灵便的同时，亦带来了一些不尽人意的后果——错误检查滞后、出错信息非常糟糕。目前，可通过 [constraints classes](http://www.research.att.com/~bs/bs_faq2.html#constraints) 间接解决这个问题。C++0x 将引入 concepts 来直接解决这个问题（参考[我的论文](http://www.research.att.com/~bs/papers.html)、[提案](http://www.research.att.com/~bs/WG21.html)，以及[标 准委员会网站的所有提案](http://www.open-std.org/jtc1/sc22/wg21/)）。

- [dynamic vs static polymorphism | SO](https://stackoverflow.com/questions/20783266/what-is-the-difference-between-dynamic-and-static-polymorphism-in-java)