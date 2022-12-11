`std::string_view`是 C++17 引入的一个 lightweight, non-owning, read-only view into a subsequence of a string。
```cpp
template<
    class CharT,
    class Traits = std::char_traits<CharT>
> class basic_string_view;
```
`std::string_view`就是`std::basic_string_view<char>`。<br />string_view 的 view 是 视图 的意思，实际上 string_view 只存了一个指针和长度（注意，string_view 并不一定以`\0`为结尾）；这样做`substr`之类的操作的时候也不需要新建一个 string 对象了。<br />string 的只读接口在 string_view 都有。

可以使用 `string str = "123"; string_view svb(str);`的方式初始化一个`string_view`，但是实际上这并不是因为调用了对应的构造函数，而是`std::basic_string`有一个`std::basic_string_view`操作符用于类型转换。这个操作符调用了`string_view`的构造函数：`string_view(str.data(), str.size())`。

string_view 还定义了 literal 格式，即`""sv`。形如`"123"sv`的字面量的类型是`string_view`。<br />（user-defined literal 参见 ）

---

类似地，还有 C++20 引入的`std::span`。
