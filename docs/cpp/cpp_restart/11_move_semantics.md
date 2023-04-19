# 9 右值引用与移动语义

## Back to Basics: Understanding Value Categories - Ben Saks - CppCon 2019

下面的讨论暂时不考虑类。

假如有定义 `int n;`，为什么 `n = 1;` 是合法的，而 `1 = n;` 是非法的呢？这不是类型的原因，`n` 和 `1` 这两个表达式的类型都是 `int`。其原因是，`n` 是一个表达式，它指向一个对象；回顾上一节我们给出的对对象的定义，它表征着一块内存，其内容表示一个值。而 `1` 则不指向一个实在的对象，它是一个不与对象关联的值，因此它不必占据内存。

也就是说，虽然 `n` 和 `1` 都是表达式，但是它们具有不同的性质。这一设计的原因是，让一些表达式的值不必占据内存有助于我们实现一些优化。如果我们规定所有表达式的值都是一个对象的话，那么字面量 `1` 也需要占据一块实际的内存，这会使得代码中的内存操作变得非常多。

我们将指向一个对象的表达式称为 **左值 (lvalue)**，因为它们可以出现在赋值表达式的左边；而将一个值不与对象关联的表达式称为 **右值 (rvalue)**，因为它们只能出现在赋值表达式的右边。

左值表征一个对象，而右值则是一个值。当我们将一个左值放在赋值表达式的右边时，如 `n = m;`，则会发生 lvalue-to-rvalue conversion，因为此时我们关注的是 `m` 这个对象中的值，而不是 `m` 这个对象本身。

右值不一定不占用内存，例如虽然 `n += 1;` 可以用一句汇编语句（如 `addi x1, x1, 1;`）实现，但是当字面量变得足够大时，一条语句可能装不下，这时右值会占据一定内存。

同时，左值表征的对象虽然从概念上说一定占据内存，但编译器有可能对其做一些优化从而使其实际上不占内存，而只是放在寄存器中或者直接在编译时完成相关的计算从而删除它。但是，这只会发生在我们不会注意到的情况下。例如，定义 `const int n = 2;` 有可能会使得所有对 `n` 的使用被替换成 `2`，从而左值 `n` 表征的对象在生成的程序中不再存在（因而不再占据内存），但是如果我们使用了 `std::cout << &n;`，那么 `n` 就一定会存在并占据内存以满足这一输出的要求。

除了字符串字面量是 lvalue（因为字符串字面量的类型是 `const char[N]`^[lex.string#5](https://timsong-cpp.github.io/cppwp/n4868/lex.string#5)^）以外，其他字面量都是 rvalue。（用户自定义字面量不一定）

在 C++ 中，这一切有所不同。

类类型的右值会占据内存，例如 `int i = foo().y;`，需要用 base + offset 的方式得到 `y` 的值。

不是所有左值都能出现在赋值表达式的左边，比如 `const char name [] = "Xuan";`，`name[0] = 'D';` 是非法的，虽然 `name[0]` 是个左值。这样的左值被称为 non-modifiable lvalues。

我们说过引用的实现类似于常指针，而指针必须指向一个 lvalue，因此引用也只能引用一个 lvalue。如 `int * pi = &3;` 和 `int & ri = 3;` 是非法的。

不过例外是，当将一个 rvalue 绑定到一个 const & 时，会创建出一个 temporary object。这个 temporary object 仍然不能被赋值，因为它是个 reference to const。这个创建的过程称为 **temporary materialization conversion**，具体来说，从一个 prvalue 转到一个 xvalue。

也就是说，内置的类型 rvalue 不占内存，但如果创建了 temp object 则占内存。因此，我们将 rvalue 分成两种：不占内存的 pure rvalue 和占内存的 expiring rvalue。

当把一个 prvalue 绑定给一个 rvalue reference 时，materialization 也发生。

有名字的东西就是个 lvalue。

## C++ Rvalue References Explained

```c++ linenums="1"
template<typename T>
class Container {
    T* data;
    unsigned size = 0, capa;
public:
    Container(unsigned capa = 512) : data(new T[capa]), capa(capa) {}
    ~Container() { delete[] data; }
    Container(const Container &) = delete;
    Container & operator=(const Container &rhs) {
        if (this == &rhs)   return *this;
        if (capa != rhs.capa) {
            delete[] data;
            data = new T[rhs.capa];
        }
        for (unsigned i = 0; i < rhs.size; i++)
            data[i] = rhs[i];
        capa = rhs.capa;
        size = rhs.size;
        return *this;
    }

    T& operator[](unsigned index) { return data[index]; }
    const T& operator[](unsigned index) const { return data[index]; }

    unsigned getSize() const { return size; }
    unsigned getCapa() const { return capa; }

    Container & add(const T& val) { 
        /* if full, expand storage */
        data[size++] = val;
        return *this; 
    }
    // ...
};
```

```c++
Container<int> x;
// perhaps use x in various ways
x = foo();
```

在赋值运算符右侧是右值的特殊情况下，我们希望赋值运算符能够简单地将 `this` 和 `rhs` 的 `data` 交换，然后让编译器销毁 `rhs` 时将 `this` 本来的 `data` 释放，这样可以避免不必要的新建内存和拷贝。

这被称为 **移动语义 (moving semantics)** 这可以通过函数重载来完成：

```c++
template<typename T>
Container<T> & Container<T>::operator=(/* some type */ rhs) {
    swap(data, rhs.data);
    swap(size, rhs.size);
    swap(capa, rhs.capa);
    return *this;
}
```

这里的参数类型是什么呢？首先它肯定是个引用，否则交换没有意义，那样 `this` 原先持有的数据无人释放，而现在持有的数据已经被释放了，这会导致严重的问题。

但是，它不能是个 `Container<T> &`，因为右值不能绑定给 non-const 引用；而它也不能是个 `const Container<T> &`，因为这样就无法修改。因此，事实上在 C++11 之前这个事情无法简单地完成。不过，在 C++11，**右值引用 (rvalue reference)** 被引入，解决了这个问题。上面的函数被实现为：

```c++
template<typename T>
Container<T> & Container<T>::operator=(Container<T>&& rhs) {
    swap(data, rhs.data);
    swap(size, rhs.size);
    swap(capa, rhs.capa);
    return *this;
}
```

由于这样的赋值运算符实现移动语义，因此它也被称为 **移动赋值运算符**。

对于任何类型 `X`，`X&&` 被称为「对 `X` 的右值引用」。为了与此区分，`X&` 现在也被称为「对 `X` 的左值引用」。

右值引用只能绑定右值：

```c++
int z = 1;
int && y = z; // Error: rvalue reference to type 'int' cannot bind to lvalue of type 'int'

int && x = 1; // OK
```

在 `int && x = 1;` 时，实际上完成了 temporary materialization conversion，即虽然 `1` 本身是个 prvalue，但是它被用来


```c++
int && x = 1; // OK
int && r = x; // Error: rvalue reference to type 'int' cannot bind to lvalue of type 'int'
```



本文参考：
- [Back to Basics: Understanding Value Categories - Ben Saks - CppCon 2019](https://youtu.be/XS2JddPq7GQ)
- [A Taxonomy of Expression Value Categories](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2010/n3055.pdf)
- [C++ Rvalue References Explained](http://thbecker.net/articles/rvalue_references/section_01.html)

值类型 https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2015/p0135r0.html