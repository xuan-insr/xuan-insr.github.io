
# 0 开始之前

- 本次学习主要参考 [JS教程 | 菜鸟教程](https://www.runoob.com/js/js-tutorial.html)。
- 本次学习基于[咸鱼暄的CSS入门](https://www.yuque.com/xianyuxuan/coding/css)、[咸鱼暄的HTML入门](https://www.yuque.com/xianyuxuan/coding/html)的基础部分。
- 本次学习将有部分内容与C或C++比较。相同部分可能会省略。

- JavaScript和Java没啥关系。
- JavaScript是一种轻量级的编程语言，代码可插入HTML页面，由浏览器执行。
- JavaScript是一种脚本语言。与传统的编程语言不同，它不会在运行前整体编译，而是直接逐行运行。
- JavaScript是一种弱类型语言。


# 1 JavaScript基础


## 1.1 JavaScript用法

- HTML中的脚本必须位于<script>元素内。可被放在<head>或<body>部分中。
- <script>既可以包含脚本语句，也可以通过 **src** 属性指向外部脚本文件。
- 如果使用src属性，<script>必须是空的。
- 外部JavaScript的扩展名为 **.js** 。外部脚本不能包含<script>标签。


## 1.2 JavaScript输出
JavaScript可以通过不同的方式输出数据：

   - **window.alart()** 可以弹出警告框。括号中填入要输出的变量/常量。
   - **innerHTML** 可以用来修改HTML元素的内容。这需要首先访问某个HTML元素，使用 **document.getElementById( **_**id**_ **)** 方法来访问具有特定id属性的元素。
      - 例如： `document.getElementById("name").innerHTML = 'xyx';` 

或者，使用 **this.innerHTML = **_**content**_ 来更改当前元素的内容。

   - **document.write()** 可以用来将内容写入HTML文档。括号中填入要输出的变量/常量。
      - 注意：在文档已经加载后使用此方法会讲已加载的内容覆盖。
   - **console.log()** 可以将内容写到控制台。在浏览器中使用F12启动调试模式。 


## 1.3 JavaScript基本语法


### 1.3.1 JavaScript字面量
编程语言中，一般固定值称为字面量。

      - **数字字面量    **整数/小数/科学计数
      - **字符串字面量    ** 可以使用单引号或双引号
      - **表达式字面量**     
      - **数组字面量**     如 [40, 100, 5]
      - **对象字面量**     如 { name:"xyx", age:19 }
      - **函数字面量**     如 function F(a,b) { return a + b; }


### 1.3.2 JavaScript变量
使用关键字 **var** 来定义变量，使用等号来赋值。变量的值可以为上述字面量的类型。

      - 变量名称对大小写敏感，以字母 _ $开头。
      - 重新声明变量，原来的值不会丢失。
      - 未被赋值的变量，值为 **undefined** 。


### 1.3.3 JavaScript数据类型

      - **基本类型** ：字符串（String），数字（Number），布尔型（Boolean），空（Null），未定义（Undefined）
      - **引用类型** ：对象（Object），数组（Array），函数（Function）
      - JavaScript的变量均为对象。因此声明变量时，可以使用 **new** 来定义其类型。
      - 可以使用 **typeof** 操作符来检测变量的数据类型。如：
```javascript
typeof "John"                // 返回 string 
typeof 3.14                  // 返回 number
typeof NaN                   // 返回 number
typeof false                 // 返回 boolean
typeof [1,2,3,4]             // 返回 object （数组是一种特殊的对象类型）
typeof {name:'John', age:34} // 返回 object
typeof null									 // 返回 object （null值为空（null），但类型为对象）
typeof undefined						 // 返回 undefined
typeof function f(){}				 // 返回 function
typeof new Date()						 // 返回 object
typeof /e./									 // 返回 object （正则表达式是一种特殊的对象类型）
```

         - 可以看到，其中数组、date、正则表达式等均返回对象类型，我们可以通过下面的 **constructor** 属性判断。

      - **constructor** 属性返回JavaScript变量的构造函数。如：
```javascript
"John".constructor                 // 返回函数 String()  { [native code] }
(3.14).constructor                 // 返回函数 Number()  { [native code] }
false.constructor                  // 返回函数 Boolean() { [native code] }
[1,2,3,4].constructor              // 返回函数 Array()   { [native code] }
{name:'John', age:34}.constructor  // 返回函数 Object()  { [native code] }
new Date().constructor             // 返回函数 Date()    { [native code] }
function () {}.constructor         // 返回函数 Function(){ [native code] }
/e./.constructor									 // 返回函数 RegExp()  { [native code] }
```

         - 注：其中的[native code]表示函数的表达式为已被编译为特定于处理器的机器码的代码，无法显示。
         - 对于返回的函数，我们可以使用函数的toString()方法转化为字符串，并使用字符串的indexOf()方法（返回指定字符串在字符串中首次出现的位置，如果没有找到返回-1）查看函数中是否包含字符串"Array"或"Date"等来判断。如`if(name.constructor.toString().indexOf("Array") > -1)`。
         - 关于正则表达式的更多内容，参见1.3.10。


### 1.3.4 JavaScript对象

      - 对象是拥有 **属性和方法** 的数据。
      - 对象属性即 **键值对（name:value）**。
      - 有两种方法访问对象的属性。如对于**var person = { name:"xyx", age:19 };  **：
         - **person.name    person.age**
         - **person["name"]    person['age']    **（注：JavaScript里单引号和双引号没啥区别qaq）
      - 对象中可以定义方法。如：
```javascript
var person = {
  name:"xyx",
  age:19,
	ageplus : function(x) { return 19 + x; }
};
```

      - 访问对象方法时：
         - **person.ageplus(1)** 会返回函数计算的值；
         - **person.ageplus** 会返回函数的定义（即冒号后面的东西qwq）。


### 1.3.5 JavaScript与HTML事件
HTML事件可以是浏览器事件，也可以是用户事件。常见的有：

      - **onchange** ，表单等HTML元素改变，如填写表单。在改变完成后。
      - **onclick** ，用户点击HTML元素。
      - **onmouseover** ，用户的在HTML元素上移动鼠标。
      - **onmouseout** ，用户的鼠标自HTML元素上移开。
      - **onkeydown** ，用户按下键盘按键。
      - **onload** ，浏览器已经完成页面加载。

更多事件，参见[HTML事件](https://www.runoob.com/jsref/dom-obj-event.html)。

在HTML元素中，可以添加事件属性。事件触发时，JavaScript可以执行一些代码。例如：<br />` <button onclick = "this.innerHTML='clicked'"> click </button>` <br />当然，也可以调用JavaScript方法。


### 1.3.6 JavaScript字符串

      - 单引号和双引号均可。
      - 可以用索引位置读取单个字符。如name[0]。
      - 可以添加转义字符。
      - 可以用内置属性 **length** 来计算字符串的长度。如name.length。


### 1.3.7 JavaScript运算符

      - 数字的计算、赋值同C。
      - 字符串可以直接用+号连接。
      - 字符串与数字相加返回字符串。
      - 比较运算符在C的基础上，还有===（绝对等于）和!==（不绝对等于），即==只要求值相等，而===要求值和类型都相等。
      - 逻辑运算符和C相同。


### 1.3.8 JavaScript语句

      - if-else, switch, for, while, do-while与C相同。
      - for-in语句用来循环遍历对象的属性。如：
```javascript
var person={fname:"Bill",lname:"Gates",age:56}; 
for (var x in person){ document.write(x+' '+person[x]+' '); }
```
输出为：fname Bill lname Gates age 56

      - break, continue可以如C中一样使用。但借用 **JavaScript标签** 还有以下用法：
         - 标记JavaScript语句：** _labelname_ : _statement(s)_**
         - 可以使用 **break _labelname_; **或 **continue _labelname_;** 跳出指定的代码（块）。其中带标签引用的continue语句只能用在循环中。


### 1.3.9 JavaScript类型转换

      - 转换为字符串： **String(), .toString()** 
      - 转换为数字： **Number()** 
      - 具体内容，参见[类型转换](https://www.runoob.com/js/js-type-conversion.html)。


### 1.3.10 JavaScript正则表达式

      - 正则表达式的基本语法是** /_regexp_/_modifier_ **，例如 `/xian*yu/i` 。
      - 其中 **regexp** 是正则表达式。相关知识，参见[咸鱼暄的正则表达式学习](https://www.yuque.com/xianyuxuan/coding/regexp)。
      - 其中 **modifier** 是修饰符。常见的修饰符有：
         - **i** ，ignoreCase，表示匹配大小写不敏感。
         - **g** ，global，表示全局匹配，即不在第一次匹配结束后就停止。
         - **m** ，multiline，表示执行多行匹配。
      - JavaScript中，正则表达式经常用于下列字符串方法（下面的regexp其实也可以为字符串）：
         - **search( **_**regexp **_**)** ，返回与正则表达式匹配的（第一个，如果使用了修饰符g）子串的起始位置。如果没有找到，返回-1。
         - **replace( **_**regexp, str**_ **) **，返回将与正则表达式匹配的子串替换为str后的字符串（不会改变原字符串）。 
         - **match( **_**regexp**_ **)**，如果正则表达式中含有修饰符g，则返回与正则表达式匹配的全部字符串，用逗号隔开，不添加空格。如果没有找到，返回null。
         -  **split( **_**regexp, limit**_ **)** ，返回按与正则表达式匹配的子串（被舍弃）分隔后得到的一个元素数不大于limit数组（大于limit个的部分被舍弃）。
            - 该方法中，regexp和limit都可选。
            - 没有regexp时，不做匹配。regexp=""时，在每个字符之间分隔。
            - 没有limit时，不限定数组的长度。

例如：
```javascript
var str = "XianyuXuan";
var pat1 = /xuan/i;
var pat2 = /n.?/g;
document.write (str.search(/.uXuan/) + ' ; ' + str.replace(pat1, "Xing") + ' ; ' 
              + str.match(pat2) + ' ; ' + str.split(/a|u/));
```
输出为: ** 4 ; XianyuXing ; ny,n ; Xi,ny,X,,n **。

      - 除了字符串方法，JavaScript还有专门的 **RegExp** 对象，如上例中的 **reg** 。此对象的属性与方法有：
         - 属性：
            - **constructor** ，返回正则表达式的构造函数RegExp()  { [native code] } 。参见1.3.3。
            - **global** ，返回true或false，表示正则表达式是否使用了g修饰符。
            - **ignoreCase**  ，返回true或false，表示正则表达式是否使用了i修饰符。
            - **multiline** ，返回true或false，表示正则表达式是否使用了m修饰符。
            - **source** ，返回正则表达式两个斜杠之间的内容。
            - **lastIndex** ，返回下一次匹配的起始位置。仅当有修饰符g时才可用。这个位置由exec和test方法找到，具体参见下文。
         - 方法
            - **exec( **_**str**_ **)**，返回检索到的子串。如果没有，返回null。
            - **test( **_**str**_ **)** ，返回true或false，表示是否检索到满足条件的字符串。
               - 注意：如果RegExp中没有使用g修饰符，那么每次对str使用上述两个方法时，都从字符串的开头开始查找。

如果使用了g修饰符，那么每次使用上述两个方法找到子串后，lastIndex属性就会指向子串的下一个字符的位置。如果没有找到，lastIndex属性则被重置为0。因此，可以借此遍历查找字符串中与正则表达式匹配的全部子串。

            - **toString()** ，返回正则表达式的字符串。


### 1.3.11 JavaScript错误处理

      - JavaScript引擎执行JavaScript代码时，可能会发生各种错误。此时，JavaScript引擎会停止并生成一个错误信息，称为 **抛出（throw）**一个错误。
      - **try** 语句允许我们定义在执行时进行错误测试的代码块；

**catch** 语句允许我们在try代码块发生错误时捕获异常，并执行代码块；<br />**finally** 语句允许我们在try-catch语句执行后，定义无论是否出现异常（即使try或catch中使用了return）都会执行的代码块。这常常用于还原数据。<br />**throw** 语句允许我们抛出一个自定义错误。<br />例如：
```javascript
<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title>XianyuXuanErrorTest</title>
		<script>
			function myFunction() {
				var message, x, i;
				document.getElementById("message").innerHTML = "";
				x = document.getElementById("demo").value;
				try { 
					if(x == 1) throw "cannot be 1";
					if(x == 2) tr;
					i = 1 / x;
					return;
				}catch(err) {
					document.getElementById("message").innerHTML = "error: " + err;
				}finally{
					document.getElementById("xValue").innerHTML = i;
					document.getElementById("demo").value = "";
				}
			}
		</script>
	</head>
	<body>
		<input id="demo" type="text">
		<button type="button" onclick="myFunction()">输入</button>
		<p id="message"></p>
		<p id="xValue"></p>
	</body>
</html>
```
在此文本框中输入0, 1, 2, 3得到的结果分别是

| 0 | Infinity |
| ---: | --- |
| 1 | error: cannot be 1<br />undefined |
| 2 | error: ReferenceError: tr is not defined<br />undefined |
| 3 | 0.3333333333333333 |

说明：

      - 对于输入0，在JavaScript中，除以0并不被认为是错误。非零数除以0得到的结果为 **Infinity（无限）** ，0除以0得到的结果为 **NaN** 。同时我们注意到，虽然try的最后使用了return退出了myFunction函数，但finally仍然得到了执行。
      - 对于输入1，我们抛出了自定义错误 **cannot be 1** 。catch语句捕获了这一错误并存储到了err中，随后输出。我们也注意到，虽然出现了错误，但finally仍然得到了执行。
      - 对于输入2，我们在2的语句中写入了错误的语句 **tr;** ，JavaScript引擎发现了这一错误并抛出，随后被catch捕获并输出。同样地，虽然出现了错误，finally语句也得到了执行。
         - 这也印证了：JavaScript不会在运行前进行统一的编译，而是逐行进行。否则在其他情况下也会出现同输入2的报错。
      - 对于输入3，程序正常运行。并同1，虽然try的最后使用了return，finally仍然得到了执行。


### 1.3.12 JavaScript变量提升

      - JavaScript中，函数与变量的声明都将被提到所在作用域的最顶部。因此，JavaScript中的变量和函数可以先使用后定义。
      - JavaScript中，变量的声明会提升，但其初始化不会提升。
      - 虽然如此，使用未声明的变量和函数是不被推荐的。


### 1.3.13 JavaScript严格模式
在脚本或函数的头部添加 **"use strict";** 表达式来声明所在作用域使用严格模式。在严格模式下的部分限制包括：

      - 不允许使用未声明的变量（包括对象、函数等）；
      - 不允许删除变量（包括对象、函数等）；
      - 不允许变量（包括对象、函数等）重名；
      - 更多限制，参见[严格模式](https://www.runoob.com/js/js-strict.html)。


### 1.3.14 其他语法规则与注意事项

      - 在JavaScript中， **分号是可选的** 。如果一句 **完整的语句** 后面进行了换行，则JavaScript会自动关闭这条语句（相当于自动补全一个分号）。例如在下面的4段代码中：
```javascript
/*  (1)  */
	var a = 10;
	return a;
/*	(2)	 */
	var a = 10
  return a
/*	(3)  */
	var
  	a = 10
  return a;
/*	(4)	 */
	var a = 10;
	return
		a;
```
这四段代码都是正确的，其中2、3段代码与第1段代码 **完全等价** ，而第4段代码虽然a也被赋值为了10，但返回值为 **undefined** 。这是因为：

         - 对于5,6行，每行都可以是一个完整的语句，JavaScript会分别关闭这两条语句，即与（1）等价。
         - 对于第8行， `var` 不能成为一个完整的语句，因此JavaScript会尝试继续读取下一行的语句，读到第9行后， `var a = 10` 可以成为一个完整的语句，JavaScript自动关闭这条语句，与（1）等价。
         - 但是对于第13行， `return` **可以被认为是** 一条完整的语句，因此JavaScript自动关闭了这条语句： `return;` 因此返回值为 **undefined** 。

因此，为了代码的正确性和可读性，请正确使用分号和换行。

      - 在各个代码块中JavaScript不会创建一个新的作用域，一般各个代码块的作用域都是全局的。例如：
```javascript
for (var i = 0; i < 10; i++) {}
document.getElementById("demo").innerHTML = i;
```
输出的结果为10而不是undefined。


# 2 JavaScript实用与进阶（未完成）




