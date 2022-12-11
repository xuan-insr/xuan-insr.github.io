

### 分类

- fundamental types
   - `void`
   - `std::nullptr_t`
   - 算术：浮点数、整型（含布尔型）
- compound types
   - 引用
   - 指针
   - 数组
   - 函数
   - 枚举
   - 类
   - union

### 分组

- scalar types
   - 算术、枚举、指针
- object types
   - scalar types、数组、union、类
   - 不含函数、引用和 void
- trivial types
- POD types
- literal types

### cv-qualifiers
除了引用和函数以外，其他类型都有对应的 cv 版本：

- <br />

### decltype


### typeid
![image.png](./assets/1658215338019-d2894a35-1d79-49d7-8a62-3b5aa50fc441.png)
![image.png](./assets/1658215346040-be08ad56-f611-447c-8125-d7457a631585.png)

### 类型别名 Type alias
一个例子是：`using ull = unsigned long long;`，除了看得清楚一点以外和`typedef unsinged long long ull`没有区别。<br />但是，type alias 可以支持 template，例如：<br />`template <unsigned N> using signed_int_t = typename signed_int<N>::type`

