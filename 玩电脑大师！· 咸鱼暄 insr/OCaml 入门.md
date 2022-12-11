本文大量内容来自 [Real World OCaml](https://dev.realworldocaml.org/) ，若无注明，本文中的代码也来自本书。本文也包含一些个人的理解，也可能根据需求省略或者折叠一些内容。为了尽可能避免误解和误导，大部分专有词汇仍然保留原文。<br />本文预设读者学习过至少一门编程语言，如 C++。

文档中下面这样的东西是折叠框，通常用来放一些没有那么重要的内容：
点击左边展开 / 折叠这是折叠框！


### Prologue
> Ref: [Prologue - Real World OCaml](https://dev.realworldocaml.org/prologue.html)


#### Why OCaml?  
编程语言是非常重要的。编程语言的特性会影响我们写出代码的可靠性、安全性和性能，同时也会影响代码是否易于阅读、重构或扩展。翁恺老师去年上课的时候说，我们的思考建立在语言的基础上；而在计算机世界中，我们所熟悉的编程语言也会影响我们编程时的思维习惯，甚至在我们使用一门新的编程语言时也会受之前熟悉的语言影响。<br />而 OCaml 是一个通用的、多范式的编程语言，兼顾效率、表达力和实用性，在教学和生产中都有丰富的实践。它良好地集合了许多语言特性，例如 Garbage collection, First-class functions, Static type-checking, Parametric polymorphism (类似 C++ 中的 template), Good support for immutable programming, Type inference (类似 C++11 中的`auto`), Algebraic data types and pattern matching 等。（这里的很多内容对我们来说可能还比较陌生，但是在后面的学习中，我们也将逐渐理解一切！）<br />我们要学习编程语言，应该对各种编程范式和语言特性有所了解。OCaml 作为一个优雅地集合了上述内容以及其他优势的编程语言，是一个不错的选择。


### 安装 OCaml
请按照 [Installation Instructions - Real World OCaml](http://dev.realworldocaml.org/install.html) 的指导安装 OCaml 的运行环境！<br />（如果网站挂了也可以看这个 ）<br />（下载和安装 OCaml 编译器的时间可能需要若干分钟，请耐心等待QWQ）<br />（似乎有 [OCaml for Windows](https://fdopen.github.io/opam-repository-mingw/)，但是我没试过）））

Unknown directive 'require':::tips
在设置下面这一步之后，在 terminal 启动 `ocaml` 可能会提示 `Unknown directive 'require'.`。参考解决方案在 。
![image.png](./assets/1662435438989-12b55b4d-8e14-4277-9af4-33a574c6cdac.png)
:::

安装完成后，在 terminal 运行指令`ocaml`，提示字符串变成`# `之后就可以开始写代码啦！<br />实际上，我们打开了一个允许我们交互式地键入和计算 OCaml 表达式的 toplevel。<br />通过 `opam install utop`可以下载`utop`，它也是一个 toplevel，相较于`ocaml`有更多的功能，例如 history navigation, auto-completion 等。下载完成后，在 terminal 运行指令`utop`即可进入 utop。


## Part 1: Language Concepts

### 1 A Guided Tour
本节通过一系列例子来帮助我们了解 OCaml 的主要特性，帮助我们之后深入了解这些内容。
:::tips
**阅读提示**<br />为了保证学习效果，请多多动手尝试！较为复杂的代码一定要完全理解！<br />本节需要的阅读和实践时间约 1 小时。<br />本节基本是 [A Guided Tour - Real World OCaml](https://dev.realworldocaml.org/guided-tour.html) 的翻译，如果不介意英文环境学习，可以直接阅读原文。
:::

#### 1.1 OCaml as a Calculator
首先，我们需要 `open Base;;`。`Base`是包含了一些基础功能的库，`open`将其中的定义引入。`;;`告知 `utop`运行。

下面我们尝试一些基础的计算：
![image.png](./assets/1662461321777-a3284e2f-c192-4a4e-bc78-06b5a0b228c3.png)
这里`#`开头的行就是我们键入的内容，其他行则为 `utop`给出的结果。可以看到：

   - 每次计算后 `utop`会打印出结果的类型 (type) 和值 (value)。
   - OCaml 明确地区分 int 和 float，`+`, `-`, `*`, `/`, `%` 的两个操作数都必须是 int；而 float 则使用 `+.`, `-.`, `*.`, `/.`，且 float 类型的字面量必须含小数点，即`6`是 int，而`6.`是 float。否则就会得到错误：
      - ![image.png](./assets/1663815848354-0e2c4449-353a-4606-8ddb-f834690ca06c.png)

我们可以用关键字`let`来创建一个变量，从而给一个表达式的值命名：
![image.png](./assets/1662461411743-d890fe8d-6894-42a6-a67b-e6b15801a942.png)
我们称之为一个 **let binding**：我们将`3 + 4`的值 bind 到变量名`x`上。<br />变量的名字可以包含大小写字母、`_`、`'`和数字，但是第一个字符必须是一个小写字母或者`_`。

值得说明的是，`;;`并不是每句话之后必需的：它只是告知`utop`去运行和打印结果，并不是用来分隔两个语句的。例如：
![image.png](./assets/1663815875785-f77c8edd-3a97-44ef-9a1c-eb9964e8e71c.png)


#### 1.2 Function and Type Inference
`let`也可以用来定义一个函数 (function)：
![image.png](./assets/1662461434437-3f376c31-332d-475e-b22e-9bc62759e8e2.png)
事实上，OCaml 中的函数也是一个值。例如上面例子中的`square`的值，它就是类型 `int -> int = <fun>`的一个值 ![](https://cdn.nlark.com/yuque/__latex/7a4b255cad94778c2d46185a201b9070.svg#card=math&code=%5Clambda%20x.x%20%2A%20x&id=N5u6Z)，这和`1`是类型 int 的一个值没有什么区别。这个类型表示接受一个 int 作为参数并返回一个 int 的函数。因此，我们也可以用`let`把这个值绑定到名字`square`上。<br />我们可以通过`square 2`的方式调用这个函数，即 ![](https://cdn.nlark.com/yuque/__latex/136b7e35deaf42db3e9a7c4719e3f75c.svg#card=math&code=%28%5Clambda%20x.x%20%2A%20x%29%5C%202&id=Pw950)。

我们也可以定义一个多参数的函数：
![image.png](./assets/1662461442713-8e8ce97c-f60a-4c55-b080-4b71f887c59e.png)
`int -> int -> float = <fun>`表示接受 2 个 int 作为参数并返回一个 float 的函数。实际上，回顾对柯里化 (currying) 的学习，不难看到这样表示的意义。<br />这里的 `Float.of_int`是 module `Float`中的函数`of_int`，它将一个 int 转为 float。

:::tips
**Open Modules Locally**<br />Modules can also be opened to make their contents available without explicitly qualifying by the module name. We did that once already, when we opened `Base` earlier. We can use that to make this code a little easier to read, both avoiding the repetition of `Float` above, and avoiding use of the slightly awkward `/.` operator. In the following example, we open the `Float.O` module, which has a bunch of useful operators and functions that are designed to be used in this kind of context. Note that this causes the standard int-only arithmetic operators to be shadowed locally.  
![image.png](./assets/1662462678080-1fb608ed-e4df-483d-a9d7-0220d25e4485.png)
We used a slightly different syntax for opening the module, since we were only opening it in the local scope inside the definition of `ratio`. There's also a more concise syntax for local opens, as you can see here.
![image.png](./assets/1662462686688-28a5033c-69ac-46e7-bbfe-cc7a154e9578.png)
:::

函数还可以接受其他的函数作为参数。例如：
![image.png](./assets/1662461472128-92b3a0bb-6a64-43d8-87bf-4464e41b1597.png)
可以看到，这个函数接受 3 个参数：第一个参数是一个`int -> bool`的函数，后两个参数是 int。这个函数返回 1 个 int。<br />下面是使用它的一个例子，就不解释了！
![image.png](./assets/1662461479614-a5caa275-202b-4323-b461-170b5afe29a1.png)
注意在`is_even`的定义中，`x % 2 = 0`的表达式显示了`=`在 let binding 以外的另一种用法，即用于判断是否相等。


##### Type Inference
不过，在上面定义函数的过程中，我们并没有指明函数的参数和返回值类型，但是 OCaml 却给出了它们的类型。这就是类型推断 (type inference) 技术。<br />我们来看看如何推断出`sum_if_true`的类型：

1. OCaml 要求`if`的两个分支具有同一类型，而`if test first then first else 0`中`0`是 int 类型，因此另一个分支的`first`一定也是 int；类似地，`second`也一定是 int；
2. `test first`接受 int 类型的`first`作为参数，而其结果又作为`if`语句的判断条件，因此`test`的类型一定是`int -> bool`；
3. `+`的返回值始终是 int，因此`sum_if_true`的返回值类型是 int。


##### Inferring Generic Types
有时，已知的信息并不足以完全推断出一个值的类型。例如：
![image.png](./assets/1662461496260-bd00d3bb-e179-4e11-8cd3-90d71e038897.png)
从这里，我们只能推断出`x`和`y`具有统一类型，`first_if_true`的返回值也属于这一类型；同时`test`是接受该类型的 1 个参数、返回 bool 类型的函数。但是我们并不能获得关于这一类型的信息。<br />我们可以看到，`utop`给出了这个函数的类型：`('a -> bool) -> 'a -> 'a -> 'a = <fun>`。这里的 `'a`是 **类型变量 (type variable)**，来表示这个类型是 generic 的；也就是说，它可以代表任意类型。不过，无论`'a`是什么类型，在`'a`的所有出现位置都会是这个类型。

有多个类型变量的情况![image.png](./assets/1662462143032-c48e29a0-ec5d-40df-8e10-991524930efc.png)

这种特性称为 **参数多态 (parametric polymorphism)**，因为它将类型参数化。这类似于 C++ 中的模板 (template) 以及 Java 和 C# 中的泛型 (generics)。

另外，我们也可以显式地注明一个或多个参数的类型或者返回值的类型；这种标注可以作为有用的注释，也可以在需要的时候避免参数多态。例如：
![image.png](./assets/1663815940611-ad30758d-f2de-4599-99fb-5d8cf4997b79.png)
可以看到，当需要注明参数的类型时需要使用`(名字 : 类型)`的方式，括号不可以省略；而需要注明返回值时在`=`前面增加`: 类型 `即可。

TYPE ERRORS VERSUS EXCEPTIONSThere's a big difference in OCaml between errors that are caught at compile time and those that are caught at runtime. It's better to catch errors as early as possible in the development process, and compilation time is best of all.    <br />Working in the toplevel somewhat obscures the difference between runtime and compile-time errors, but that difference is still there. Generally, type errors like this one:
![image.png](./assets/1662462741015-280e0881-5623-43ec-93fc-2d7c48d71cc6.png)
are compile-time errors (because + requires that both its arguments be of type int), whereas errors that can't be caught by the type system, like division by zero, lead to runtime exceptions:
![image.png](./assets/1662462764198-b51b49d4-b0cc-4367-9edd-ccede99358a6.png)
The distinction here is that type errors will stop you whether or not the offending code is ever actually executed. Merely defining `add_potato` is an error, whereas `is_a_multiple` only fails when it's called, and then, only when it's called with an input that triggers the exception.


#### 1.3 Tuples, Lists, Options, and Pattern Matching
我们在此前已经尝试了 int, float, bool, string 等基本的类型以及函数类型，下面我们来看看一些数据结构。


##### Tuple
**Tuple** 是一个 N 元有序组，其中的每个值的类型可以是不一样的：
![image.png](./assets/1662513827117-a5a803ff-4cda-45fb-9011-37d43b956881.png)
如上面所示，我们可以通过将值用逗号连接起来来创建一个 tuple。在不引起歧义的前提下，括号是不必要的：
![image.png](./assets/1663815977551-2538a853-5fde-4ecf-aee8-b4919597dd50.png)
这里`tuple1`的 3 个值依次是 int, string, float 类型的，因此`tuple1`的类型是这三个类型的 **笛卡尔积 (Cartesian product)**，即`int * string * float`。


##### Pattern Matching
Pattern-matching 语法可以用于提取 tuple 的值：
![image.png](./assets/1662515046431-c5f724bf-727d-4d5f-979c-c5dd3cb6c777.png)
也可以用在函数参数中：
![image.png](./assets/1662515102930-5c2f203d-029e-45f2-800c-80a1213f9428.png)
`**.`是计算浮点数的幂。
OPERATORS IN Base AND THE STDLIBOCaml's standard library and `Base` mostly use the same operators for the same things, but there are some differences. For example, in `Base`, `**.` is float exponentiation, and `**` is integer exponentiation, whereas in the standard library, `**` is float exponentiation, and integer exponentiation isn't exposed as an operator.

`Base` does what it does to be consistent with other numerical operators like `*.` and `*`, where the period at the end is used to mark the floating-point versions.

In general, `Base` is not shy about presenting different APIs than OCaml's standard library when it's done in the service of consistency and clarity.


##### Lists
List 是容纳 **同一种 **类型的任意元素的数据结构。例如：
![image.png](./assets/1662515649235-b62a5b0a-9242-43b8-9d7e-4b4da2762504.png)
这里的`languages`的类型是`string list`。<br />需要注意的是，OCaml 中的 list 用分号`;`分隔元素。如果用逗号，则会被认为是 tuple：
![image.png](./assets/1662515820519-0136ae33-5bb9-4b95-b05c-ae301f032dc5.png)

`Base`中的`List`module 提供了大量好用的函数，例如：
![image.png](./assets/1662516282371-5883c2db-f4c3-4566-8a63-e9e90e7c1643.png)

再例如，`List.map`接受两个参数：一个 list 和一个 function。它返回一个新的 list，这个 list 中的每个元素都是传入 list 中对应元素经过 function 变换得到的。例如：
![image.png](./assets/1662518240806-e242b70e-9f50-4b26-a203-0ba9d219720a.png)
这里我们计算了 languages 中的每个元素的长度。<br />注意到这里的函数是通过`~f:String.length`的方式传入的，这里的`~f`叫做 **labeled argument**，这样的参数通过名字指定，而不是之前我们熟悉的按位置绑定。改变这样的参数的位置并不影响函数的行为：
![image.png](./assets/1662518666370-5295dc49-8a25-4f96-a9ed-5f108bca7946.png)
我们会在后面（如果有）详细学习 labeled argument 和它的好处。

List constructor`[]`表示一个空列表：
![image.png](./assets/1663815991104-bd6fb28a-8d3a-4a71-947a-32dae15ae04a.png)

List constructor`::`可以用来在一个 list 的最前面添加元素：
![image.png](./assets/1662516355929-b6614213-e843-4cf3-bb8e-b8f4fa58cc34.png)
这个操作构造出一个新的 list，`languages`本身不会变化：
![image.png](./assets/1662516388653-f17426df-4483-4ebe-9de7-60e38be33616.png)

List concatenation operator`@`用来连接两个 list：
![image.png](./assets/1662516601293-16514b5e-1fd9-4a06-a310-44c9d978d0d3.png)
`@`的复杂度是![](https://cdn.nlark.com/yuque/__latex/e65a67ac353abeeff44c359310d05c02.svg#card=math&code=O%28n%29&id=jELGb)，其中![](https://cdn.nlark.com/yuque/__latex/df378375e7693bdcf9535661c023c02e.svg#card=math&code=n&id=j1hCJ)是第一个 list 的长度


##### List Patterns Using Match
List patterns 基于`[]`和`::`这两个 list constructor。看这样一个例子：
![image.png](./assets/1662516970868-3be7921f-d6d0-486f-9a67-4e52a87f492f.png)
从输出的最后一行可以看到，这个函数接受一个 list；而我们将这个 list 用`my_favorite :: the_rest`的方式接受，其实就是将 list 的首个元素绑定到`my_favorite`，而将剩下的列表绑定到`the_rest`。<br />不过，输出的 1~4 行给出了 warning：pattern-matching 并不全面，`[]`是不能被匹配的一个例子。如果我们尝试运行，可以看到参数为`[]`时会出现匹配失败的 exception：
![image.png](./assets/1662517140733-25688daa-88d4-4830-816a-e64cf59bc550.png)

因此，我们需要让我们的程序能够处理所有的情况。我们使用`match`语句，这种语句类似于 C/C++ 和 Java 中的`switch`。用这种语句，我们可以列举一系列 pattern，中间用 pipe character `|`分隔。第一个 case 之前的`|`是非必要的：
![image.png](./assets/1662517304496-44a18e18-5cd2-4225-b896-c657d50db19c.png)
可以看到，这时不再有 warning 了，运行也能成功。<br />也可以看到，我们使用`(* something *)`的方式作为注释。


##### Recursive List Functions
递归函数在任何函数式语言中都非常重要。下面的例子是对 list 求和：
![image.png](./assets/1662517670479-5832d64e-5e2d-4301-802f-1a277bcd1c62.png)
上面的`hd`是 head 的缩写，`tl`是 tail 的缩写。<br />注意，对于递归函数，必须显式地用关键字`rec`标明，否则会报错：
![image.png](./assets/1663816030541-405bc74a-5298-4a87-8368-c11f3cfea280.png)
这里是另一个例子：
![image.png](./assets/1662517819294-ded439b1-e063-4cbf-9e0c-ac230d63cd14.png)


##### Options
`option`是用来表示一个值有可能存在也有可能不存在的数据结构，类似 C# 和 Java 的 nullable，以及 C++17 的 `std::optional`。例如：
![image.png](./assets/1662519085350-d0cb004f-1ec7-4f2f-b76d-73372c12fb40.png)
`None`和`Some`是 option 的 constructor，就像`[]`和`::`是 list 的 constructor 一样。

我们同样利用 pattern matching 来使用 option 中的内容。作为例子，我们写一个函数，它接受一个文件名，返回将其扩展名转成小写后的结果。这里我们会用到`String.rsplit2`函数，它找到字符串中最右边的给定字符，从这里把字符串分割，返回值类型为`(string * string) option`。如果没有找到给定字符，返回`None`。
![image.png](./assets/1662519416000-fa291afe-3644-41a7-ae67-a3df72fb12a7.png)
这里的`^`操作符用来连接字符串。


#### 1.4 Records and Variants

##### Records
类似 C 语言的 struct，我们可以定义 record 作为新的数据类型：<br />`type point2d = { x : float; y : float }`<br />我们可以这样构造：
![image.png](./assets/1662520729067-6e20424b-695e-440b-a88f-7f255d45058b.png)

Record 同样适用 pattern matching：
![image.png](./assets/1662521047219-08bc31ad-416f-4601-bff4-34f12348e5c8.png)
这里实际上就是把`x_pos`的值绑定到`x`字段上、`y_pos`的值绑定到`y`字段上。<br />当这两个名字恰好相同时，我们可以使用 **field punning** 来使代码更加简洁：
![image.png](./assets/1662532714198-00785dea-794c-412e-b6ae-5b6b787457a0.png)

我们还可以使用`.`来访问 record 的字段：
![image.png](./assets/1662532763878-7ddb89ac-caff-464e-a4d2-b892ffddd2ba.png)

我们自定义的类型也可以作为其他数据类型的组分：
![image.png](./assets/1662532813279-914f4ff1-2b9a-4fda-8d3f-0a92bdfc7d54.png)

##### Variants
Variant 允许我们定义类似 C 中 union 的结构：
![image.png](./assets/1662533329432-f623f802-96e4-4a81-882d-49ec340e8ab2.png)
和`match`语句类似，我们用`|`分隔不同的 case，第一个 case 前的`|`也不是必需的。<br />每个 case 都要有一个首字母大写的 tag。

我们展示一个使用 variant 的例子：
![image.png](./assets/1662533928960-585491ca-6b2b-44be-823e-9d17f7940c37.png)

- 可以看到，`is_inside_scene_element`函数接受一个`point2d`和一个`scene_element`，根据后者的类型判断前者代表的点是否在后者代表的图形内。
   - 这里的`| Segment _ -> false`中的`_`是一个通配符 (wildcard) pattern，表示可以匹配任意单个值，但是我们不会（不需要）将其中的值绑定到任何变量上。
- 而`is_inside_scene`函数接受一个`point2d`和一个`scene_element list`，返回前者代表的点是否在后者列表中的某个图形内。
   - 这里的`List.exists`接受一个列表和一个函数，返回这个列表中是否存在一个元素使得函数的返回值为真。
   - 这里的`(fun el -> is_inside_scene_element point el)`是一个 **匿名函数 (anonymous function)**，它接受一个参数`el`，返回`is_inside_scene_element point el`。这样的函数使用关键字`fun`定义，在`List.map`, `List.exist`这样的迭代函数中非常常用。
      - 匿名函数的使用方法和普通的函数一致
         - ![image.png](./assets/1662544642366-222ff0ef-db44-4a62-a2ad-9820e20f675c.png)

下面是运行的例子，同样展示了 Varient 的构造方法：
![image.png](./assets/1662534832901-38196e94-9f55-44e4-a5a7-222c43a5b265.png)


#### 1.5 Imperative Programming
上面我们所写的函数都是 pure function，这样的函数和数学中的函数一样，没有任何副作用，也不受任何副作用的影响；给定一个确定的输入一定能得到一个确定的输出。另外我们遇到的变量和数据结构都是不可变的 (immutable)，当我们给一个变量名重新做 let binding 时，原本的值并没有被改变，只是我们将新值绑定到了这个名字上。这些都是函数式 (functional) 编程语言的重要特性，也是 OCaml 的默认做法。<br />不过，OCaml 也支持指令式的编程，包括 array, hash-table 这样的可变数据结构，以及`for`, `while`这样的控制流结构。<br />请在 [Imperative Programming - A Guided Tour | Real World OCaml](https://dev.realworldocaml.org/guided-tour.html#scrollNav-5) 阅读相关内容。 


#### 1.6 A Complete Program
我们目前的尝试都是在`utop`上完成的，下面我们来实现一个单独的程序。<br />以下面的程序`sum.ml`为例：
```ocaml
open Base
open Stdio

let rec read_and_accumulate accum =
  let line = In_channel.input_line In_channel.stdin in
  match line with
  | None -> accum
  | Some x -> read_and_accumulate (accum +. Float.of_string x)

let () =
  printf "Total: %F\n" (read_and_accumulate 0.)
```
请注意，在`utop`以外我们不再需要`;;`来标识表达式的结束。

我们使用`Dune`来构建一个 OCaml 工程。在工程根目录下，需要有一个`dune-project`文件，保存这个工程的 metadata。这里我们可以写：
```scheme
(lang dune 2.9)
(name rwo-example)
```
同时，每个工程目录下需要一个`dune`文件，描述如何处理当前目录内的文件。这里我们只有一个根目录，所以在根目录写：
```scheme
(executable
 (name      sum)
 (libraries base stdio))
```
我们的目录结构如下：
![image.png](./assets/1662531624175-e38ae71e-3788-4616-8556-5b76a9335c3a.png)

下面，我们使用`dune build sum.exe`来构建。完成后的目录结构如下：
![image.png](./assets/1662532194631-96b7cdba-3951-4a0c-bff2-db6f7d6b2b0c.png)

下面就可以尝试运行了！
![image.png](./assets/1662532238575-57a8dae6-a6f8-43e4-bb11-24172a2bd8ed.png)
（用 Ctrl + D 结束输入）

这只是一个小例子，如果希望探索更多相关内容，可以查看以下资料：

   - [Command-Line Parsing - Real World OCaml](https://dev.realworldocaml.org/command-line-parsing.html#command-line-parsing)
   - [Quickstart - dune documentation](https://dune.readthedocs.io/en/stable/quick-start.html)


##### `#use`
在`utop`中，我们可以使用`#use "file.ml";;`来读取并执行名为`file.ml`的文件中的语句，其效果与在`utop`中直接键入这些语句一致。如果对应文件中有错误，读取将在遇到第一个错误时停止。<br />请注意，`#use`只能用在`utop`中，它并不是 OCaml 本身的一部分。


### 2 Variables & Functions


### 3 Lists & Patterns


### 4 Files, Modules, and Programs


### 5 Records


### 6 Variants


### 7 Error Handling
