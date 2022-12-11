今天 dzdd 提了一个相关的问题，引出了这个问题。我们曾经在 oop 课的作业中实现过一个 vector，其中函数 `at` 为：
```cpp
template <class T>
T& at(int index) {
    if (index < 0 || index >= m_nSize)
        throw std::out_of_range("index out of range");
    return *(m_pElements + index);
}
```
	在这个函数里，我们没有对 `this` 做改变。那么我们为什么不使用 `T& at(int index) const;` 呢？

实际上，在 C++ 标准里，`vector::at` 有两个重载：
```cpp
      reference at (size_type n);
const_reference at (size_type n) const;
```
	这里重载的两个函数具有同样的参数列表，但是后者有 `const` 关键字。实际上，这也是不同的参数列表；因为前者隐含了一个 `vector * const this` 参数，而后者隐含了一个 `const vector * const this` 参数，这两个参数具有不同的数据类型。<br />在我们用一个非 const 的实例调用一个 const 的成员函数的时候，编译器实际上将 `T*` 自动转化为了 `const T*`，这是合法的；而反过来是不合法的，理由显然。

这样的重载是合理的，因为对于 `vector` 和 `const vector`，获取其索引理应分别返回引用和常引用，因为这样可以保证前者的元素可以更改，而后者不可以更改。<br />但是，如果我们让前者也加上 `const`，那么这两个函数除了返回值类型就会完全一致，这不能形成一个正确的重载。因此，即使前者的函数本身也可以使用 `const`，但是出于重载的考虑，我们并不这样设计。
