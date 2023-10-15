# 1 基本数据类型和操作

Original Post: [http://git-zju-edu-cn-s.webvpn.zju.edu.cn:8001/ppl-course/mua/-/tree/main/](http://git-zju-edu-cn-s.webvpn.zju.edu.cn:8001/ppl-course/mua/-/tree/main/)

By PPL2021

## 要求

你的任务是实现一个 MUA 语言的解释器。从标准输入中读入输入程序，然后在标准输出（屏幕）中写入 MUA 程序的输出（也就是 `print` 操作产生的效果）。

你暂时不需要考虑任何输入不合法的情况。输出实数时，你可以在合理的范围内自由定义输出的小数位数。

### 提示

1. 先完整看完这个提示，再看下面的语法说明。
2. 为了挑战自己，尝试在看懂语法说明之前 **不要** 看测试样例。确信自己看懂之后，再看测试样例来验证自己有没有真的看懂。如果没有超出你预期的测试样例，奖励你一块饼干 🍪
3. 看输入样例时，可以根据自己的理解脑补一下输出，再与输出样例比对。如果一致，再来一块 🍪
4. 完全看懂测试样例之后，再开始构思怎么组织这个程序。
5. 在构思怎么组织这个程序之前，建议你简单浏览完整的 [MUA 语法说明](../grammar)。你不需要完全看懂它，但是你需要获得一些有用的信息，例如之后你可能要支持更多的基本操作、数据类型，或者对现有的数据类型做更多的操作。

## 语法说明

### 基本数据类型 | value

数字 number，字 word，布尔 bool

- 任何值之间都以空格分隔
- 数字的字面量以 `[0~9]` 或 `'-'` 开头，不区分整数，浮点数
- 字的字面量以双引号`"`开头，不含空格。在 `"` 后的任何内容，直到空格（包括空格、tab和回车）为止的字符（不含空格），都是这个字的一部分，包括其中可能有的 `"` 和 `[]` 等符号
    - `"abc`
- 布尔量只有两个值：`true` 和 `false`
- 数字和布尔量在计算时可以被看作是字的特殊形式。即，在字面量和变量中的字，当其中的内容是数字或布尔量时，总是可以根据需要自动被转换成数字或布尔量

### 名字 | name

一个只含有字母和数字及下划线的字可以用做名字，名字区分大小写。

### 基本操作 | operation

基本形式：操作名 参数

操作名是一个名字，与参数间以空格分隔。参数可以有多个，多个参数间以空格分隔。每个操作所需的参数数量是确定的，所以不需要括号或语句结束符号。所有的操作都有返回值。

一个程序就是操作的序列。

基本操作有：

- `make <name> <value>`： 将 value 绑定到 name 上，绑定后的名字位于当前命名空间，返回 value。此文档中的基本操作的名字不能重新命名
    - `make "a 1`
- `thing <name>`：返回 word 所绑定的值
    - `thing "a`
- `:<name>`：与 thing 相同，但如果 name 是一个字的字面量，省去前导 `"`
    - `:a`
- `print <value>`：输出 value 并换行，返回这个 value
- `read`：返回一个从标准输入读取的数字或字
- 运算符 operator 
    - `add`, `sub`, `mul`, `div`, `mod`：`<operator> <number> <number>`

---


## 测试样例

### Input Case 1

```lua
print 1
print 1.1
print -1
print "hello
print "hello"
print true
```

### Input Case 2

```lua
make "a 1
print :a
print make "a 2
print print thing "a
make "b "a
print thing thing "b
make "c mul add :a 13 :a
print sub :c "6
print div 12 5
print mod 12 5
make "d read
1234dd
make "e print :d
print :e
```

提示：上面这个例子的倒数第二行是 `read` 读取的输入。

### Output Case 1

注：数字的小数位数不重要

```
1.0
1.1
-1.0
hello
hello"
true
```

### Output Case 2

```
1.0
2.0
2.0
2.0
2.0
24.0
2.4
2.0
1234dd
1234dd
```
