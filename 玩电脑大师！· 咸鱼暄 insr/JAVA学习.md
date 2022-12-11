
# 0 开始之前

- 本次学习以[Java教程 | 廖雪峰](https://www.liaoxuefeng.com/wiki/1252599548343744)的顺序与逻辑为主，根据学习情况有所更改。本次学习也是对学习小组内容的复习，同时对[Java 教程 | 菜鸟教程](https://www.runoob.com/java/java-tutorial.html)作了参考。
- 本次学习根据学校课程《Java 程序设计》做了增补。Java 程序设计的课程笔记，参见 [Java 程序设计](https://www.yuque.com/xianyuxuan/coding/crs-java/edit)。
- 本次学习基于 C 语言的基本知识（不包括 C++ 面向对象）。文中会与 C/C++ 做对比，相似的地方可能会有省略。

- 在此，暂略去开发环境的配置。本次学习使用的 IDE 主要是 IntelliJ Idea。


# 1 JAVA基础语法


## 1.1 程序基本结构
C 语言的程序代码写在一个扩展名为 .c 的文本文件中，由 C 编译器编译后形成可执行文件运行。Java 语言类似。Java 的代码的基本单位是一个个的 **类** ，其中我们可以定义各种 **成员方法** （类似 C 语言中的函数）以及 **成员变量**。每个类储存在一个与类同名的 .java 文件中。<br />同时，类似 C++ 中的名字空间，Java 要求每个代码文件声明其所属的 **包** 。包的结构类似于文件夹的结构。在IDE 中新建类文件时，IDE 一般会帮助我们写好所属的包。关于包的更多问题，可以在后面的 **2.11 包** 中学习。<br />在 IDE 中编写 Java 程序的步骤是：新建 project-> 在源码（src）文件夹中新建类（class）-> 在创建出的类文件中编写代码。

例如，下面的代码段 1-1：
```java
public class Code1_1{
    public static void main(String[] args){
        System.out.println("Hello, Java!");
    }
}
```
运行结果为：
:::success
Hello, Java!
:::

   - 该代码中， `public class Code1_1{ ... } ` 定义了一个名为 **Code1_1** 的 **类**。
      - Java 是 **大小写敏感** 的。
      - 按照习惯， **类名要用大写字母开头** 。
      - **public** 是这个类的 **修饰符** 说明这个类是公开的。
      - 花括号中的代码是这个类的定义。
   - `public static void main(String[] args){ ... }` 定义了名为 **main** 的 **方法** 。
      - 按照习惯， **方法名用小写字母开头** 。
      - 方法是可执行的代码块，花括号中的内容就是这个方法的代码。
      - 括号中的内容是这个方法的 **参数** ，本方法中有一个类型为 **String[]** （即字符串数组），名称为 **args** 的参数。
      - **public static** 是这个方法的 **修饰符** ，说明这个方法是公开、静态的。
      - **void** 是方法的 **返回类型** 。
      - Java 规定，某个类定义的`public static void main(String[] args)`是Java程序的固定入口方法。因此，Java 程序总是从`main`方法开始执行。
   - 该代码被保存在 Code1_1.java 文件中。 **Java 程序的源文件名与类名必须相同** ，否则会导致编译错误。


## 1.2 标识符
类名、变量名、方法名都被称为 **标识符** 。

   - 所有的标识符都应该以字母（A-Z 或者 a-z）,美元符（$）或者下划线（_）开始
   - 首字符之后可以是字母（A-Z 或者 a-z）,美元符（$）、下划线（_）或数字的任何字符组合
   - 关键字不能用作标识符
   - 标识符是大小写敏感的
   - 合法标识符举例：age、$salary、_value、__1_value
   - 非法标识符举例：123abc、-salary


## 1.3 变量和数据类型

### 1.3.1 基本数据类型
基本数据类型是CPU可以直接进行运算的类型。Java定义了以下几种基本数据类型：

         - 整数类型：byte，short，int，long
            - 一个整数的缺省类型为 int。如果要表示一个整数为 long 类型，需要加后缀 L 或 l，如 31L。
            - 八进制数以 0 为前缀，如 027 等，十六进制数以 0x 或 0X 为前缀，如 0xAC, 0X1b 等。
         - 浮点数类型：float，double
            - 一个浮点数的缺省类型为 double。如果要表示一个浮点数为 float 型，需要加后缀 F 或 f。
            - 浮点数可以用标准计数法（如 12.3）或科学技术法（如 2.5E4, 3.66e7 等）表示。科学计数法也称指数形式，E 或 e 前面的数称为尾数，后面的数称为阶码。
         - 字符类型：char
            - 与 C 不同的是，Java 中 char 类型是一个单一的 16 位 Unicode 字符。所以，一个英文字符和一个中文字符都用一个 char 类型表示，它们都占用两个字节。
            - 要显示一个字符的 Unicode 编码，将 char 类型直接赋值给 int 类型即可。如 `int n2 = '中';`  （汉字“中”的 Unicode 编码是 20013）。
            - 还可以直接用转义字符 **\u**+Unicode 编码（16 进制）来表示一个字符：

`char c4 = '\u4e2d';`（十六进制 4e2d = 十进制 20013）。

            - 由多个字符组成的字符序列称为字符串，字符串用双引号引起来。
         - 布尔类型：boolean
            - 与 C++ 不同的是，Java 中的 true 不能表示为 1，false 也不能表示为 0。
      - 在此省略这些变量的范围和占用的字节数。
      - 定义基本数据类型变量的语法与C相同。
      - 根据习惯， **变量名用小写字母开头** 。

Java中，用 **final** 修饰符来修饰常量。如 `final double PI = 3.14;` 。

      - 常量在程序运行时是不能修改的。
      - 根据习惯， **常量名全部使用大写字母** 。


### 1.3.2 运算

#### 整数及其运算
整数运算的规则与C基本相同。

         - 可以使用四则运算、取模、自增自减、移位运算与位运算。
            - 位运算中， `>>>` 表示一个不带符号的右移运算，即符号位也会一同进行移位。
            - 此处略去运算符的优先级。
            - 整数运算中，除数为 0 时运行会报错。
         - 整数之间的运算仍为整数，小数部分（如果有）将被舍去。
         - 整数运算会出现溢出，但不会报错。


#### 浮点数及其运算
浮点数运算的规则与C基本相同。

         - 浮点数存在误差。
         - 与整数运算不同， **浮点数运算时，除数为0不会报错。** 但是会返回几个特殊值：
```java
double d1 = 0.0 / 0; // NaN
double d2 = 1.0 / 0; // Infinity
double d3 = -1.0 / 0; // -Infinity
```


#### 布尔型及其运算
Java中的布尔型与 C++ 中的有以下区别：

         - 数据类型为 boolean。
         - 给布尔型变量赋值为 1 或 0 是不合法的。

布尔运算的规则与C基本相同。

         - 与C相同，布尔运算有 **短路运算** 的特点。


#### 强制类型转换
Java中的强制类型转换与C相同。


#### 自动类型提升
整型、实型（常量）、字符型数据可以混合运算。运算中，不同类型的数据先转化为同一类型，然后进行运算。规则如下：

         - 转换从低级到高级：byte, short, char -> int -> long -> float -> double

         - 浮点数到整数的转换是通过舍弃小数得到，而不是四舍五入。
         - 转换的溢出部分将被舍弃。
            - 如，一个浮点数（超过了整数的最大范围）转化为整数时，小数部分、超出最大范围的部分都将被舍弃，即转化成的整数为其范围的最大值。
         - 需要特别注意，在一个复杂的四则运算中，两个整数的运算不会出现自动提升的情况。例如：`double d = 1.2 + 24 / 5; ` 计算结果为 5.2，原因是编译器计算 24 / 5 这个子表达式时，按两个整数进行运算，结果仍为整数 4。


### 1.3.3 引用类型

#### 引用类型

         - 建议在阅读本节前，首先阅读**2.1 类 **以及** 2.2 对象**。
         - 在Java中，引用类型的变量非常类似于C的指针。引用类型指向一个对象（参见2.1 面向对象的基本概念），指向对象的变量是 **引用变量** 。这些变量在声明时被指定为一个特定的类型，比如 Person 等。变量一旦声明后，类型就不能被改变了。
         - 对象、数组、字符串都是引用数据类型。
         - 所有引用类型的默认值都是null。
         - 一个引用变量可以用来引用任何与之兼容的类型。

#### 字符串

         - 字符串类型String（注意首字母大写）是引用类型，但可以使用 `String str = "123"` 这样的定义方法。
            - 引用类型的变量类似C中的指针，可能指向一个对象，也可能指向一个空值（null）。代码段 `String s1 = null, s2, s3="";` 中，s1为null；s2没有赋初值，也为null；但s3指向了一个空字符串，空字符串是一个有效的字符串对象，不是null。
            - **字符串是不可变的。**

代码段`String s1 = "abc"; s1 = "def";`中，执行`String s1 = "abc";`时，JVM虚拟机创建了字符串"abc"，然后让s1指向它；执行`s1 = "def";`时，JVM虚拟机创建了新的字符串"def"，然后让s1指向它，但原来的字符串"abc"并没有消失，还是存在于内存中。<br />例如代码段：
```java
		String s = "Hello";
        String a = s;
        s = "HELLO";
        System.out.println(a + " " + s);
```
输出为 `Hello HELLO` 。这说明原来的字符串 "Hello" 仍存在于内存中，s 只是指向了一个新的字符串 "HELLO"，并没有改变原有字符串的值。

         - 字符串的表示方法与C++相同。
         - 字符串之间、字符串与其他类型之间，都可以用 **+** 连接，返回他们拼接成的字符串。其中其他数据类型的变量会先被转换为字符串再拼接。
         - 关于字符串的更多操作，参见 [3.1 字符串](#2flVb)。

#### 数组

         - 数组的声明方法是：**dataType[] arrayRefVar = new dataType[arraySize]**。例如：

`int[] myArray = new int[105]` 。<br />也可以使用下面的声明方法：<br />**dataType[] arrayRefVar = new dataType[] {value0, value1, ..., valueK}**<br />或进一步简写为：<br />**dataType[] arrayRefVar = {value0, value1, ..., valueK}**<br />例如：`String[] names = {"ABC", "XYZ", "zoo"};`

         - 多维数组可以用类似的方法定义。如：
            - `int[][] a = new int[2][3];` 
            - `int[][] b = { {1,2}, {2,3}, {3,4} };`
         - 数组所有元素初始化为默认值，整型都是0，浮点型是0.0，布尔型是false。
         - 与C一样，Java数组的下标（索引）也是从0开始。
         - 数组也是引用类型。以int数组（值类型的数组）为例，数组名类似C中“基地址”的概念，指向的是这个数组（的第一个元素的地址）。如果是String数组（引用类型的数组），那么实际上数组名指向的数组中每个元素都指向了一个字符串的地址。
         - 我们可以重新定义数组，但与String类型类似， **数组的大小是不可变的** ，对数组的重新定义只是让数组变量指向了一个新的数组，原来的数组的大小并没有发生变化，只是它不在被曾经的数组名所指。
         - _arrayRefVar_.length 是数组类的一个属性，值为数组的大小。
            - 如果有数组 `int[][] a = new int[2][3]` ，那么 a.length 为 2，a[1].length 为 3。


## 1.4 修饰符
Java语言提供了很多修饰符，主要分为下面两种：

### 1.4.1 访问控制修饰符
Java中，可以使用访问控制符来保护对类、变量、方法和构造方法的访问。Java 支持 4 种不同的访问权限 : default, public, protected, private。这部分的详细解释，参见 **2.6 访问控制修饰符** 。

### 1.4.2 非访问修饰符
为了实现一些其他功能，Java中也包含了一些非访问修饰符。例如： static, abstract, final等。这部分内容也将在后文讲解。


## 1.5 输入和输出

#### 输入
Java中的输入相对复杂。下面的代码段1-2是读入一个整数的例子：
```java
import java.util.Scanner;
public class Code1_2 {
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        int a = scanner.nextInt();
        System.out.println("answer:" + (a + 1));
    }
}
```
输入5，运行结果为：
:::success
answer:6
:::
第1行，我们通过import语句导入java.util.Scanner，这类似于C中的#include语句。<br />第4行，我们创建了一个名为scanner的Scanner对象，并传入System.in。<br />第5行，我们使用scanner.nextInt()读入用户输入的一个整数。<br />要读取其他类型的数据，使用：

         - **scanner.next()** 读入字符串
         - **scanner.nextLine() **读入一行
         - **scanner.nextLong()**
         - **scanner.nextFloat()**
         - **scanner.nextDouble()**
         - **scanner.nextBoolean()**
         - 等等。

第6行，我们输出了一个字符串，这个字符串是"answer"与(a+1)的结果6相连得到的。如果(a+1)没有括号，根据1.3.3.2的内容，输出的将是answer:51。

#### 输出

         - **System.out.println() **    输出括号中的内容并换行。
         - **System.out.print() **       输出括号中的内容。
         - **System.out.printf()       **格式化输出，与C/C++中的printf语法类似。占位符有：
            - %d	格式化输出整数
            - %x	格式化输出十六进制整数
            - %f	格式化输出浮点数
            - %e	格式化输出科学计数法表示的浮点数
            - %s	格式化字符串
            - %% 输出%



关于输入和输出的更多内容，将在后文展示。


## 1.6 顺序 分支 循环
Java具有与C/C++类似的if-else, switch, while, do-while, for, break, continue语句。但下面几个方面需要特别注意：

#### switch 语句的要求
switch 括号中的表达式只能是 int, char, short, int, String 和枚举类型，long, float 等类型是不被允许的。

_此处暂略去Java 12中新的 switch语法。_


#### 判断引用类型相等 —— ==与equals() 
Java中，判断值类型变量是否相等，可以使用 **==** 运算符，但是在引用类型的变量之间使用 **==** 表示“引用是否相等”，即“是否指向同一个对象”（就像C中两个指针相等当且仅当其指向同一个地址）。而使用引用类型变量的 **equals()** 方法即可判断两个变量的内容是否相等。语法为： **_var1_.equals(**_**var2**_**)** ，返回值是boolean类型。<br />需要注意的是，如果上面的var1为null，则运行时会出现NullPointerException错误。为避免此错误，需要提前进行判断。<br />另外， **switch** 中的判断其实是与 **equals()** 等价的。


#### 更方便地遍历数组 —— for each循环 
Java中引入了一种用于遍历数组的循环。其语法为：<br />**for( **_**d****ataType**_** **_**tempVar**_ **: **_**arrayRefVar**_**) {...}** ，例如：
```java
String[] a = {"1", "54", "12"};
String str = "";
for(String n : a){
    str += n;
}
System.out.println(str);
```
输出为15412。<br />这样的循环，定义了一个局部变量（类型与数组元素的类型相同），在每次遍历的时候，取值为当前数组元素的值。


# 2 Java面向对象基础
Java是一种面向对象的编程语言。面向对象编程，英文是Object-Oriented Programming，简称OOP。<br />面向对象程序设计中的概念主要包括：对象、类、数据抽象、继承、动态绑定、数据封装、多态性、消息传递。通过这些概念面向对象的思想得到了具体的体现。


## 2.1 类
**类（Class）** 类似于C++中的结构体，可以包含成员变量和成员函数（方法）。实际上，C++中也有类的概念，且与struct非常相似。<br />类是一个共享相同结构和行为的对象的集合。类定义了一件事物的抽象特点。通常来说，类定义了事物的属性和行为。类可以为程序提供模版和结构。一个类的方法和属性被称为“成员”。<br />用人举例，“人”这个类包含了人的基础特征：状态有名字、身高、财产等等；行为有：睡觉、逛街等等。<br />“人”是一种抽象概念，而具体的人，例如你的对象（如果有）则是人这个概念的 **实例（Instance）** 。<br />所以说，类是一种模板，它定义了如何创建实例。

#### 在Java中定义一个类
例如：
```java
public class Person{
    String name;
    int age, property;
    void sleep(){}
    void shopping(){}
}
```


## 2.2 对象
**对象（Object）**是可以对其做事情的一些东西。每个对象都有其状态和行为。<br />用你的对象（如果有）举例，同“人”这个抽象的概念一样，你的对象的状态也有：名字、财产、身高等等；行为也有：（和你）睡觉、（和你）逛街等等。

#### 在Java中创建一个对象
Java中，定义了class，只是定义了对象模版，而要根据对象模版创建出真正的对象实例，必须用new操作符。new操作符可以创建一个实例，然后，我们需要定义一个引用类型的变量来指向这个实例：<br />`Person boyfriend = new Person();` 

此时，我们定义了一个Person类型的实例，并用boyfriend指向它。<br />我们可以通过 `boyfriend.age` 来访问其成员变量，通过 `boyfriend.sleep()` 来访问其成员方法。


## 2.3 方法

#### public存在的问题
有时，我们并不希望一个类中的成员变量被外部代码直接访问，因为这可能会造成数据的损失或逻辑的混乱。例如，对于这个类：
```java
public class User{
    public String password;
    public int id, age;
}
```
外部代码可以这样写：
```java
/* user1是已经存在的对象 */
String user1PasswordCopy = user1.password;
user1.age = -100;
```
可以看到，直接将类中的变量定为 **public** 可能会造成信息丢失和逻辑混乱，破坏了代码的封装性。


#### 解决方法——private
如果将上面User类中修饰变量的 **public** 改为 **private** ，上面的外部代码在编译时就会报错，因为private修饰的变量拒绝外部访问。但是，为了让外部可以（有限制地）访问这些值，我们需要使用 **方法（Method）** 。例如：
```java
public class User{
    private String password;
    private int id, age;
    public int getAge(){
        return this.age;
    }
    public void setAge(int age){
    	if(age > 0)	this.age = age;
        else 		throw new IllegalArgumentException("Invalid Age Value");
    }
}
```
在上面代码中，虽然外部代码无法直接读取或修改age变量的值，但是可以通过getAge()和setAge()方法来间接读取或修改。同时，我们也有机会在外部代码试图修改时对数据进行检查。例如，第8行中我们对年龄的值进行了判断，如果值为负，那么我们抛出了一个错误，程序报错，修改失败。

同样地，我们也可以定义private的方法，这些方法也是外部无法调用的，但是在外部调用public方法时可能会用于运算。


#### 指向当前实例的变量——this
上例中的 **this** 是一个隐含的变量，它始终指向当前实例。例如，我们用User类创建了对象user1，那么在运行其中的方法时，this指向的就是user1。因此，通过this就可以访问当前实例（对象）的变量或方法。<br />如果没有命名冲突，可以省略this。例如上例中第5行的this.age就可以写成age；但是如果局部变量与类变量重名，局部变量优先级更高，就必须加上this，如上例中的第8行。


#### 方法的参数
与C语言中的函数类似，Java方法允许传入0至任意个参数。但是，Java方法有如下不同：

##### 可变参数
例如：
```java
int[] values = new int[105];
public void setArray(int... values){
    this.values = values;
}
```
这个函数的参数类型为int，但数目可以是0到任意个，调用 `setArray();` 或 `setArray(1, 2);` 即可。可变参数相当于数组类型。这方便了调用方的使用。因为如果将传入参数定义为 `int[] values` ，那么调用方需要先构造一个数组，而且调用方有可能传入null，但可变参数则不会为null。

##### 参数传入的规则
回忆C中我们试图用函数swap()来交换两个数，如果使用 `swap(int a, int b)` 是不能达到效果的，因为C中的函数传递的参数是 **值的拷贝** ，其交换不会影响原来的值。但是使用 `swap(int *a, int *b)` 可以达到效果，因为这样虽然传递的也是值的拷贝，但传入的是指针，即需要交换的值所储存的地址。这样对指针指向的内容进行交换，就可以达到交换的目的。<br />在Java中也存在类似的情况。其规则为：基本类型对象传入方法时传入的是 **值的拷贝** （占用空间小），而引用类型对象传入方法时传入的是 **引用的拷贝** 。<br />例如代码段2-1：
```java
	public static void main(String[] args){
        int[] a = new int[]{2};
        int b = 2;
        change_ref(a);
        change_val(b);
        System.out.print(a[0] + " ");
        System.out.print(b);
    }
    public static void change_ref(int[] x){
        x[0]++;
    }
    public static void change_val(int x){
        x++;
    }	
```
输出为：
:::success
3 2
:::

可以看到，我们在两个方法中都作了一次自增运算。对于基本类型（int），调用方法是传递的是值的拷贝，即建立了一个新的临时的int变量x，将b的值复制给它，此后对x的更改与b无关。而对于引用类型（数组），其传递的是 **引用的拷贝** ，即 **指向的对象** 。也就是说，虽然也有一个新的变量x被建立，但它的值拷贝的是a的指向，即main中的a和change_ref中的x其实指向的是同一个数组，因此a[0]的值也被更改了。

下面的例子从这个角度再次说明了字符串类型是不可变的。
```java
public static void main(String[] args) {
    List list = new List();
    String name = "a";
    for(int i = 1; i <= 3; i++){
        name += "b";
        list.insert(name);
    }
    System.out.println(list.getList());
}
/*---in List.java---*/
public class List {
    private String[] name = new String[10];
    private int count = 0;
    public void insert(String name){
        this.name[count++] = name;
    }
    public String getList(){
        String list = "";
        for(int i = 0; i < count; i++){
            list += name[i] + " ";
        }
        return list;
    }
}
```
输出为：
:::success
ab abb abbb 
:::
这是因为，每次name += "b"，即name = name + "b"，实际上都是创建了一个新的字符串并让name指向它，而原来的字符串没有发生改变。而传入时，每次传入的是当时name的引用的拷贝，因此list.name数组中的字符串仍旧指向原来的字符串。


#### 方法的重载（Overload）
在Java中，允许在一个类中存在多个 **名称相同** 的方法，但其 **传入参数列表** 必须不同（数量或变量类型不同）。编译器将通过调用时 **传入参数的数目和类型** 来确定调用哪一个方法。<br />方法重载的典型实例之一，即为下面的**2.4 构造方法**。


## 2.4 构造方法
在2.2中，我们通过Person boyfriend = new Person();创建了一个实例。而 **Person()** 方法并不是我们定义的。实际上， **Person()** 方法是 **构造方法** ，当一个对象被创建的时候，构造方法用来初始化该对象。构造方法与其所在类的名称相同，且没有返回值。调用构造方法，必须使用 **new** 操作符。<br />无论我们是否定义，所有的类都有构造方法。这是因为Java给每个类提供了一个默认的构造方法，它没有参数，也没有执行语句。一旦我们定义了自己的构造方法， 默认的构造方法就会消失。<br />下面是自己定义构造方法的一个实例：
```java
public class Person{
    String name;
    int age;
    public Person(){
    }
    public Person(String name){
        this.name = name;
    }
    public Person(String name, int age){
        this.name = name;
        this.age = age;
    }
}
```
第4行允许我们创建一个没有初始化其中变量的对象，我们可以在后续操作中更改变量的内容。即，这允许我们用 `Person person = new person();` 来定义一个对象。<br />第6行允许我们创建一个只初始化了name变量的对象。当然，我们也可以定义一个只初始化age变量的对象。即，这允许我们用`Person person = new person("xyx");` 来定义一个对象，但这里由于没有传入参数为int类型的构造方法，因此`Person person = new person(1);`会导致编译错误。<br />第9行允许我们创建一个对象，并直接完成其初始化。即，这允许我们用`Person person = new person("xyx", 19);` 来定义一个对象。但是，由于参数列表的限制，我们不能调换传入参数中字符串和整数的位置，否则也会导致编译错误。

很多IDE的菜单中可以方便地创建构造方法（可以自由选取参数）以及getter setter（例如2.3中的setAge()等，参见**3.3 JavaBean**），无需自己编写。


## 2.5 继承

### 2.5.1 继承类
2.1中，我们了解了类的意义。对于“人”这个类，它的实例满足“是一个 **人** ”这个概念。而实际上，“人”这个群体下也可以划分出一些 **子类** ，它们在具有“人”的属性和行为的同时，也有不同于 **父类** 的属性和行为。子类满足的是“属于 **人** ”的概念，例如 **教师** 是人的一个子类。<br />**继承** 就是子类继承父类的特征和行为。它允许了我们创建分等级层次的类，可以帮助我们省略重复的代码，同时提高代码的可维护性。<br />Java使用 **extends** 关键字来实现继承。Java中每个类只允许继承一个类。例如：
```java
/*--- in Person.java ---*/
public class Person{
    String name;
    int age, property;
    void sleep(){}
    void work(){}
}
/*--- in Teacher.java ---*/
public class Teacher extends Person{
    int teachingLength;
    void teach(){}
    void work(){
        teach();
    }
}
```
这时，我们定义 `Teacher teacher1 = new Teacher();` ，由于Teacher继承了Person的（非 **private** 的）成员变量和成员方法，因此Teacher类实际上也包含name, age等变量以及sleep()等方法。同时，Teacher类也可以有自己的变量和方法。<br />这里，我们把Person称为 **父类（parent class），超类（super class）或基类（base class）** ，把Teacher称为 **子类（subclass）或扩展类（extended class）** 。


### 2.5.2 Object类
实际上，每一个类（除了Object类）都有且仅有一个父类。没有extends关键字修饰的类实际上继承了Object类的成员方法。其成员方法包括 **equals()**（注：object类中的equals()是与==等价的，String类中对equals()进行了重写）**, toString()** 等等。


### 2.5.3 重写与super关键字
我们还可以看到，第12行重新定义了其父类中已有的work()方法。这称为 **重写(Override)** 。重写有如下规则：

      - 参数列表必须完全与被重写方法的相同（如果不同，实际上是方法的重载）。<br />
      - 返回类型与被重写方法的返回类型可以不相同，但是必须是父类返回值的 **派生类** （即子类、子类的子类等等）。
      - 访问权限不能比父类中被重写的方法的访问权限更低（参见 **2.6 访问控制修饰符** ）。例如：如果父类的一个方法被声明为 public，那么在子类中重写该方法就不能声明为 protected。
      - 父类的成员方法只能被它的子类重写。<br />
      - 声明为 final 的方法不能被重写。<br />
      - 声明为 static 的方法不能被重写，但是能够被再次声明。<br />
      - 子类和父类在同一个包（参见 **2.11 包** ）中，那么子类可以重写父类所有方法，除了声明为 private 和 final 的方法。
      - 子类和父类不在同一个包中，那么子类只能够重写父类的声明为 public 和 protected 的非 final 方法。<br />
      - 重写的方法能够抛出任何非强制异常，无论被重写的方法是否抛出异常。但是，重写的方法不能抛出新的强制性异常，或者比被重写方法声明的更广泛的强制性异常，反之则可以。<br />
      - 构造方法不能被继承。<br />
      - 如果不能继承一个方法，则不能重写这个方法。<br />

需要在子类中调用被重写的父类方法时，需要使用 **super** 关键字。例如前代码的Teacher类中， `work()` 与 `this.work()` 调用的是Teacher类中重写的work()方法，而 `super.work()` 则会调用Person类中未被重写的work()方法。


### 2.5.4 子类的构造方法
实际上，Java中所有子类的构造方法中，都需要 **首先调用父类的构造方法** ，如果构造方法中没有调用，编译器则会自动加上 **super();** 以调用父类的构造方法。看下面的代码段：
```java
/*--- in Person.java ---*/
public class Person{
    String name;
    int age;
    public Person(int age){
        this.age = age;
    }
}
/*--- in Teacher.java ---*/
public class Teacher extends Person{
    int teachingLength;
}
```
这个代码段会出现编译错误。这是因为，Teacher类中没有定义构造方法，因此编译器自动帮助我们定义了默认的构造方法`public Teacher(){}`。同时，由于该构造方法中没有调用父类的构造方法，因此编译器自动帮助我们调用了父类的默认构造方法，即 `public Teacher(){ super(); }` 。然而，由于我们在父类中自定义了有age参数的构造方法，因此其默认无参的构造方法并不存在，即 `super();` 是不合法的调用，因此出现了编译错误。<br />为了修正此编译错误，有两种解决方式：

      - 在Person类中增加无参构造方法： `public Person(){}` ；
      - 在Teacher类中定义构造方法，以避免自动定义无参的构造方法。如：
         - `public Person(int age){ super(age); }` 
            - 注：此处省略super(age);同样会导致编译错误，因为编译器仍然会自动添加 `super();` 。
         - `public Person(int age, String name){ super(age); this.name = name; }` 等。


### 2.5.5 向上转型与向下转型
_本小节的讨论中的代码示例基于小节2.5.1中的代码段。_<br />_<br />在C语言中，指针的类型决定了其指向的数据的类型。例如int*指向的变量为int类型，char**指向的是char*类型等等。而Java中的引用类型也类似。例如 `Person person = new Person();` 中，person是一个Person类型的引用变量，指向了一个Person类型的对象。<br />但是，这样的指向在Java中也是被允许的： `Person p = new Teacher();` 。经过测试我们发现，这样定义的对象具有Person（父类）的所有变量和方法，但是不具有Teacher（子类）中独有的变量和方法。实际上，这样的操作 **将一个子类的对象安全地 **_**抽象 **_**为一个父类的对象** ，类似于自动类型转换。但是由于子类一定包含父类的所有变量和方法，因此这样的变换 **一定是安全的** 。这样的变换称为 **向上转型** 。<br />同时，如果我们想将一个父类对象强制转换成子类对象，就是 **向下转型** 。但是，向下转型不能与向上转型使用同样的语法。即， `Teacher p = new Person();` 会导致编译错误。如果需要向下转型，需要用到强制类型转换，即 `Person p = new Person(); Teacher t = (Teacher) p;` 。但实际上，这样的操作在运行时会出现错误：**ClassCastException**。这是因为，我们的定义中Teacher类中可能含有Person类中不包含的变量和方法。这些方法不可能凭空“变”出来，因此出现了错误。即，我们 **不能让父类强制变为子类** ，因为子类的功能比父类多。<br />实际上，我们想要进行向下转型，必须保证被强制转换的引用类型的确是我们需要转到的类型。例如，这样的向下转型就是合法的：`Person p = new Teacher(); Teacher t = (Teacher) p;` 。这是因为，引用变量p确实指向了一个Teacher类型的变量。<br />为了避免向下转型的失败，Java提供了 **instanceof** 操作符， _**varOfClassA**_** instanceof **_**ClassB** _的返回值为true或false。其字面意思是： _**变量A**_**（是否）是**_**类B**_**的实例** 。我们可以用这样的方法保证我们的转型不会出现运行时错误： `if(s instanceof Teacher) { Teacher t = (Teacher) s; }` 。<br />从Java14开始，判断`instanceof`后，可以直接转型为指定变量，避免再次强制转型。例如，对于代码：`if(s instanceof Teacher) { Teacher t = (Teacher) s; t.sleep(); }`，就可以简略为：<br />`if(s instanceof Teacher t) { t.sleep(); }`。使用**instanceof **_**variable**_这种判断并转型为指定类型变量的语法时，必须打开编译器开关**--source 14**和**--enable-preview**。<br />特别地，如果一个引用变量的值为null，那么其对任何instanceof的判断结果均为false。


### 2.5.6 多态
_本小节的讨论中的代码示例基于小节2.5.1中的代码段。_<br />_<br />在2.5.5中，我们了解到，一个变量的声明类型和其实际指向的变量类型可能不同，例如2.5.5中讨论的`Person p = new Teacher();`。此时，如果我们调用 `p.work()` ，调用的其实是Teacher类中重写过的work方法。实际上， **Java的对象方法调用是基于运行时实际类型的动态调用** ，而非变量的声明类型。这种重要的特性称为 **多态（Polymorphic）** 。<br />这样的特性可以让我们的子类具有更好的功能拓展。我们可以无需讨论变量所述的类，就可以让对象根据其实际的类型调用其重写的方法。例如我们可以定义方法 `public void toWork(Person p) { p.work(); }` ，无论传入的参数是Person类型还是其子类，都可以自动按照对应的方法调用。<br />实际上，equals()是多态的重要例子之一。String类等对其进行了重写，我们在调用 _str_.equals() 时就会自动访问其重写的equals()方法。


## 2.6 访问控制修饰符
Java中可以使用访问控制修饰符来保护对类、方法、变量、构造方法等的访问。Java支持4种不同的访问权限：

| 修饰符 | 当前类 | 同一包内 | 派生类(同一包) | 派生类(不同包) | 其他包 |
| :---: | :---: | :---: | :---: | :---: | :---: |
| public | Y | Y | Y | Y | Y |
| protected | Y | Y | Y | Y/N（注2） | N |
| default | Y | Y | Y | N | N |
| private | Y | N | N | N | N |

注1：private 和 protected 不可用于修饰外部类。<br />注2：对于子类和父类在不同包中的情况，子类只能访问其 **直接继承** 的类中的protected方法。即，其父类的父类的protected方法是不可以访问的。


## 2.7 静态变量与静态方法
在一个class中定义的变量称为 **实例变量** ，每声明一个实例（对象），其都包含一个对应的独立变量。而用 **static** 修饰的变量则为 **静态变量** ，静态变量属于类而不属于实例。虽然在对象中也可以访问静态变量，但每个对象访问到的都是同一个静态变量，即所属类的静态变量。实际上，编译器将对象对静态变量的访问自动转换成了类对静态变量的访问。因此，建议 **始终使用 **_**className.staticVar**_** 访问静态变量** 。<br />类似地， **static** 修饰的方法为 **静态方法** 。由于静态方法属于类而不属于对象，因此 **静态方法只能访问静态变量** ，而不能访问实例变量和this变量。


## 2.8 final类与final方法
1.3.1中，我们了解了 **final** 修饰符修饰 **常量** 的相关内容。实际上， **final** 也可以用于修饰类和方法：<br />**final类** 不能被继承；<br />**final方法** 可以被子类继承，但不能被其重写。


## 2.9 抽象类与抽象方法
在Java中，每一个对象都是对一个类的实例化。但是，并不是每个类都被代码的设计者认为具有足够的信息来实例化一个对象。由于继承的存在，我们可以让某些类用于 **规范子类的功能** 。这样的类被称为 **抽象类** ，用关键字（修饰符） **abstract** 修饰。抽象类只能被继承，而不能用来实例化对象。<br />由于抽象类对子类功能的规范，我们可能会希望抽象类的 **所有子类都需要按照自己的功能重写某个方法** 。我们可以用 **抽象方法** 来满足这个需求。抽象方法同样用 **abstract** 修饰。抽象方法专门用于被重写，其 **没有任何方法实现语句** 。其定义必须为 **abstract **_**methodName **_**( **_**Parameter List **_**);** ，没有大括号，而是使用分号结尾。<br />由于抽象方法本身是无法执行的，其必须被重写，因此 **具有抽象方法的类必须为抽象类** 。抽象类的子类如果仍然没有重写抽象方法，那么该子类仍旧必须是抽象类，不能实例化对象。


## 2.10 接口
在抽象类中，抽象方法实际上是定义接口规范。即规定了子类必须具有的接口实现，从而发挥多态的作用。<br />如果一个抽象类中没有变量，且所有的方法都是抽象方法，就可以把该抽象类改为一个 **接口（interface）**。<br />在Java中， **interface** 可以用于声明一个接口。接口与类一样，也需要保存在 _**InterfaceName**_**.java** 文件中。<br />具体的类实现接口时，需要用到关键字 **implements** 关键字。但与类不同的是， **接口允许多继承** 。如果进行多继承，继承的接口之间用逗号隔开。<br />接口也可以继承接口。继承时使用 **extends** 关键字。<br />接口中可以定义 **default** 方法。这样的方法可以有其实现，且子类不必重写该方法。

至此，我们学习到了引用类型的全部：引用类型包含所有 **class** 类型和 **interface** 类型。


## 2.11 包
为了解决不同代码设计者编写的类的名字冲突，Java 定义了一种名字空间，称为 **包（package）** 。包是类似于文件夹的树型储存结构，实际上，包在计算机中的实现的确是通过文件夹的路径完成的。例如 package net.java.util;的类的存储目录就是 net/java/util/。<br />每个类都属于一个包。因此实际上每个类的完整类名均为 **包名.类名** 。每个类都需在文件开头（类外）声明所属的包。语法为 **package 包名** 。没有定义包名的类属于默认包，这很可能产生名字冲突，这是非常不被推荐的做法。<br />需要特别注意的是， **包没有父子关系（没有任何继承关系）**。例如，net.java.util 与 net.java 没有任何关系。<br />希望调用其他包中的类，可以使用下面两种方法：

   - 使用完整类名（即 **包名.类名** ）。
   - 使用 import 语句引入（也在文件开头）。语法为 **import 包名.类名** 。此后在本文件中就可以使用简略的类名。
      - 我们也可以通过 **import 包名.*** 来引入包中的所有类（但不包括内层包中的类）。

编译器遇到任何一个类名的时候都会寻找其完整类名。如果不是完整类名，编译器会先寻找本包中有没有对应的类，其次寻找 import 的包是否有对应的类，最后寻找 java.lang 包是否有对应的类。如果都没有，则编译错误。实际上，编译器默认帮助我们 import 了当前包中的其他类以及 java.lang.*。<br />如果希望同时使用两个或多个同名的 class，那么至多只能按上面的寻找规则简写其中一个（当然也可以不简写），其他的必须使用完整类名。


# 3 Java核心类
_此部分暂缓学习。需要使用时学习并补充。_

## 3.1 字符串
在 [1.3.3 引用类型 -- 字符串](#VLYE3) 小节中，我们已经对字符串有了一些基本的认识。下面我们介绍关于 String 类更多的知识。

#### 字符串比较
看下面一个例子。
```java
public class Main {
    public static void main(String[] args) {
		String s1 = "hello";
        String s2 = "hello";
        System.out.print((s1 == s2) + " " + (s1.equals(s2)) + " ");
        /* 请注意，== 优先级较高，例如 s1 == s2 + " " 的运行顺序为 s1 == (s2 + " ")。 */
        String s3 = "hello";
        String s4 = "HELLO".toLowerCase();
        System.out.print((s3 == s4) + " " + (s3.equals(s4)) + " ");
    }
}
```
代码段的运行结果为 `true true false true` 。<br />第三个输出为 false 的原因已经在 [1.6](#B6DkH) 中讲解过了。而第一个输出为 true 的原因其实是编译器在编译过程中将相同的字符串当做同一个常量放入常量池，因此它们的地址是相同的。

`equalsIgnoreCase()` 方法可以忽略大小写比较两个字符串。

`compareTo()` 方法按字典序与另一个字符串作比较。逐个比较字符，找到第一个不相同的字符时，返回两个字符的差值（如下例第 4 行）；如果没有找到不相同的字符，返回两字符串长度的差值（如下例第 5, 6 行）；如果两个字符串完全相同，返回 0。

```java
		String str1 = "Stringv";
        String str2 = "Strings123";
        String str3 = "Strings12345";
		str1.compareTo( str2 );	//3
		str2.compareTo( str3 ); //-2
        str3.compareTo( str1 ); //-3
```
`compareToIgnoreCase()` 方法按字典序忽略大小写与另一个字符串作比较。其中计算两字符差值时，以小写字母计算。


#### 更多方法
```java
/* 基本操作 */
String s1 = "abcde";
s1.charAt(1);		//'b'
s1.length();		//5

/* 搜索、提取子串 */
String s1 = "Hello";
s1.contains("ll");	//true
s1.indexOf("l");	//2
s1.lastIndexOf("l");//3
s1.startsWith("He");//true
s1.endsWith("lo");	//true
s1.substring(2);	//"llo"
s1.substring(2, 4); //"ll" （注：第二个参数是结束索引，不包括在提取的子串中）

/* 空白字符处理 */
/* trim 和 strip 方法可以去除首尾空白字符，空白字符包括空格, \r, \n, \t，strip 还额外包括中文空格 */
"  \tHello\r\n ".trim();	 // "Hello"
"\u3000Hello\u3000".strip(); // "Hello"
" Hello ".stripLeading();	 // "Hello "
" Hello ".stripTrailing();	 // " Hello"

/* 空白字符串判断 */
"".isEmpty(); 			// true，因为字符串长度为0
"  ".isEmpty();			// false，因为字符串长度不为0
"  \n".isBlank();		// true，因为只包含空白字符
" Hello ".isBlank(); 	// false，因为包含非空白字符

/* 替换子串 */
String s = "hello";
s.replace('l', 'w'); 	// "hewwo"，所有字符'l'被替换为'w'
s.replace("ll", "~~"); 	// "he~~o"，所有子串"ll"被替换为"~~"
//也可以用正则表达式替换：
String s = "A,,B;C ,D";
s.replaceAll("[\\,\\;\\s]+", ","); // "A,B,C,D"

/* 分割、拼接字符串 */
String s = "A,B,C,D";
String[] ss = s.split("\\,"); // {"A", "B", "C", "D"}
String[] arr = {"A", "B", "C"};
String s = String.join("***", arr); // "A***B***C"

/* 类型转换 */
//valueOf 方法是一个重载方法。
String.valueOf(123); // "123"
String.valueOf(45.67); // "45.67"
String.valueOf(true); // "true"
//char[] 和 String 也可以互相转换。
char[] cs = "Hello".toCharArray(); // String -> char[]
String s = new String(cs); // char[] -> String
```

#### String 向其他类型转换
```java
int n1 = Integer.parseInt("123"); // 123
int n2 = Integer.parseInt("ff", 16); // 按十六进制转换，255
boolean b1 = Boolean.parseBoolean("true"); // true
boolean b2 = Boolean.parseBoolean("FALSE"); // false
/* 其他类型用类似的方法，如 Float.parseFloat("123.45") 等等 */
```

## 3.2 包装类型

## 3.3 JavaBean
在 Java 中，有很多 class 都由若干 private 实例变量组成，并通过 public 方法来读写实例字段。这些读写方法命名为 **public void set**_**VarName**_**(**_**Type varName**_**)** 与 **public **_**Type**_** get**_**VarName**_**()**。那么这种 class 被称为JavaBean。这些读写方法被称为 setter 和 getter。JavaBean 主要用来传递数据，即把一组数据组合成一个JavaBean 便于传输。而且 JavaBean 可以方便地被 IDE 工具分析，生成读写属性的代码。


## 3.4 枚举类


## 3.5 BigInteger


## 3.6 BigDecimal


## 3.7 Math类
Java 的核心库中给我们提供了大量的工具类供我们使用。java.lang.Math 类提供大量静态成员方法来执行基本数学函数的运算：
```java
//abs方法有多种数据类型的重载。
Math.abs(-15.2);	// 15.2

//max 和 min 只能有两个操作数。该方法有多种数据类型的重载。
Math.max(1, 6);		// 6
Math.min(2.5, 3.1);	// 2.5

//返回 double。
Math.pow(2, 10);	// 1024.0
Math.sqrt(4);		// 2.0
Math.exp(2);		// e^2
Math.log(4);		// ln4
Math.log10(4);		// lg4

//round 方法返回最接近的操作数的整数。算法是加 0.5，然后向下取整。
//该方法有传入 float 和 double 的重载，分别返回 int 或 long。
Math.round(11.5);	// 12
Math.round(-11.5);	// -11

//返回 double。
Math.sin(3.14);		//还有 cos, tan, asin, acos, atan 等。

//（伪）随机数，范围是 0 <= x < 1。
Math.random();

//几个常量
Math.PI;			//3.14159...
Math.E;				//2.71828...
```


## 3.8 随机数
除了 3.7 中的 Math.random()，java.util.Random 类中还为我们提供了几种随机数的生成方法：
```java
Random r = new Random();
//当我们创建 Random 实例时，可以在括号中给定种子。如果不给定种子，则以系统当前时间戳为种子。
r.nextInt(); 		
r.nextInt(10); 		// 生成一个[0,10)之间的int
r.nextLong(); 		
r.nextFloat(); 		// 生成一个[0,1)之间的float
r.nextDouble(); 	// 生成一个[0,1)之间的double
```

但是，这些生成的都是伪随机数。java.security.SecureRandom 类为我们提供了安全的随机数。
```java
SecureRandom sr = new SecureRandom();
sr.nextInt(); 		
sr.nextInt(10); 		// 生成一个[0,10)之间的int
sr.nextLong(); 		
sr.nextFloat(); 		// 生成一个[0,1)之间的float
sr.nextDouble(); 		// 生成一个[0,1)之间的double
```


# 4 Java进阶
_此部分暂缓学习。需要使用时学习并补充。_

## 4.1 Java异常处理

