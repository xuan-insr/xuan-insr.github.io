学校 Python 课程 课程记录 / 翁恺

- 智云：[https://media.zju.edu.cn/index.php?r=course/live-view&id=22665&tenant=112](https://media.zju.edu.cn/index.php?r=course/live-view&id=22665&tenant=112)
- 课件：[https://mo.zju.edu.cn/workspace/61e93c256f482ed63c0b94e8/app](https://mo.zju.edu.cn/workspace/61e93c256f482ed63c0b94e8/app)
   - 打不开的话：[https://mo.zju.edu.cn/classroom/class/Python_2021_ss?&activeKey=section](https://mo.zju.edu.cn/classroom/class/Python_2021_ss?&activeKey=section)
- 题目集：[https://pintia.cn/problem-sets/1111652100718116864/](https://pintia.cn/problem-sets/1111652100718116864/)

范围：1~6, 7.1, 8.1, 8.2

- 在浏览器中编程
   - [https://clin.icourse163.org/py/](https://clin.icourse163.org/py/) ：功能阳春，没有库，加载快，支持手机
   - [http://pythontutor.com/](http://pythontutor.com/) ：可调试，有助于理解程序的执行，没有库，加载较慢，手机不友好，iPad可用
   - [https://mo.zju.edu.cn/](https://mo.zju.edu.cn/) ：不用安装库
- 编程软件
   - IDLE：[https://www.python.org](https://www.python.org/) ，有电脑就应该安装一个，必须学会，考试只能用IDLE和Thonny
   - Thonny：[https://thonny.org/](https://thonny.org/)
   - Visual Studio Code：[https://code.visualstudio.com](https://code.visualstudio.com/) ，可以用于各种语言的编程

:::tips
在此敬告过往者<br />如果想看本文：

- 蓝色背景需要看懂！
- 其他颜色的无所谓）会有别的做法的
:::


## Python 学习时间线
PTA 和翁恺先生的课件来回穿插进行

### PTA 编程题 (1)

#### 1-1 A+B
![image.png](./assets/1642677657448-abeb1eb9-30e0-4964-8745-c3b1966ccf65.png)
:::info

- input() 读入一行，字符串
- int(foo) 将 foo 转化为整型
   - 类似地有 float() 和 str()
   - 前后有空格不影响，有非空白符不行 ![image.png](./assets/1642681855381-35dec2cb-b210-4b58-a98a-4af2f5b585cf.png)
- print(foo) 输出
:::
```python
print(int(input()) + int(input()))
```

#### 1-2 A+B，但是在一行
![image.png](./assets/1642677648209-f2b55294-dccf-471a-8e41-ccaf1d4d673a.png)
:::info

- 赋值语句
- 不用看懂，但是要记住可以这么写
- str.split()，用空格分隔形成列表，列表中的元素还是字符串
   - `'12/18'.split('/')` --> `['12', '18']`
:::
:::success

- map(fun, list)，生成器
- a, b, c = <generator>
:::
```python
a, b, c = map(int, input().split())
print(b * b - 4 * a * c)
```

#### 1-3 Hello, world!
:::info
记得用 Python 3
:::
```python
print("人生苦短，我学Python")
```

#### 2-1 输入一个正整数m(20<=m<=100)，计算 11+12+13+...+m 的值
:::success
range() 也是一个生成器<br />输出的时候，逗号隔开的各部分之间会自动添一个空格
:::
```python
print("sum =", sum(range(11, int(input()) + 1)))
```

#### 2-2 if-else
![image.png](./assets/1642678436821-666238dc-0a31-4518-b3a3-1b3d62494291.png)
:::info

- float()
- print(f"...") 表示这是格式控制输出
   - 注意：`{x:.1f}` 和 `{x: .1f}`输出也会差一个空格的！
- if 和 else 的范围用缩进控制。
   - 记得写冒号！
:::
```python
x = float(input())
if x != 0:
    print(f"f({x:.1f}) = {1/x:.1f}")
else:
    print(f"f(0.0) = 0.0")
```

#### 2-3 if-elif-else
![image.png](./assets/1642678963877-c1eddc88-00f4-4b77-bac3-ea3517d53740.png)
```python
x = int(input())
if x < 0:
    print("Invalid Value!")
elif x <= 50:
    print(f"cost = {0.53 * x:.2f}")
else:
    print(f"cost = {0.53 * x + 0.05 * (x - 50):.2f}")
```

#### 2-4 while
![image.png](./assets/1642679705435-6ad2dc23-0c22-4555-97db-e11ed7d8a2c8.png)
:::info

- while 语句
- +=, -= 语句
- 字符串可以通过 '+' 实现拼接
:::
```python
a, n = input().split()
n = int(n)
tot = 0
cur_str = a
while n > 0:
    tot += int(cur_str)
    cur_str += a
    n -= 1
print("s =", tot)
```
或者：
:::info
字符串也可以通过 '*' 实现若干次重复（`a * i`）
:::
:::success
lambda 表达式格式：`lambda i: int(a * i)`
:::
```python
a, n = input().split()
print("s =", sum(map(lambda i: int(a * i), range(1, int(n) + 1))))
```

#### 2-5 for
:::info
for 语句的格式
:::
```python
n = int(input())
sum = 0
for i in range(1, n + 1):
    sum += 1 / (2 * i - 1)
print(f"sum = {sum:.6f}")
```

#### 2-6
:::info
`a ** b`：乘方
:::
```python
print(f"{1 + sum(map(lambda i : (-1)**(i + 1) * i / (2 * i - 1), range(2, int(input()) + 1))):.3f}")
```

### 翁先生课件 (1)

#### 01 做计算 - break
:::info
`break`跳出循环
:::

#### 02 循环计算 - 除法 取模 同步赋值 逻辑运算 链式比较
:::info
![image.png](./assets/1642680921089-5ecf5f6e-2867-49d1-8519-f9fd4331cff5.png)
![image.png](./assets/1642680933292-d1a08995-4b19-4888-ad93-b419e4651eae.png)

- 同步赋值 `a, b = b, a`
- `print(a, end=', ')`里的end=用来指定这次输出之后自动输出什么
   - 默认是\n，表示要换一行

![image.png](./assets/1642681144322-7cde5ebb-3796-4efd-b0aa-e273298f1c92.png)
![image.png](./assets/1642681151711-ca5fc521-42f7-490f-9e3e-646f1ffbc4b3.png)
:::

#### 03 字符串 - 复数 字面量 字符串
:::info
![image.png](./assets/1642681331012-892023f1-04b4-4284-9b97-b17c0deb6299.png)

- 字面量和值
   - `"Hello"` 和 `'Hello'` 是两个不同的字面量，但是有相同的值
- 字符串 `s[i]`取字符，下标从 0 开始
   - 下标为负数表示从后往前数，倒数第一个是`s[-1]`
- `s[6:14]` 表示下标为 6 ~ **13** 的子串
   - `s[6:]`表示下标为 6 开始到结束
   - `s[:-1]`表示从开始到倒数第**二**个

![image.png](./assets/1642681661082-ce326700-ab64-433d-b4f7-59b43b488441.png)
![image.png](./assets/1642681688912-23efc25a-8dbb-4416-bf8a-57a651bc8211.png)
![image.png](./assets/1642681705054-4b98748c-c390-4187-be4d-2792c19d70a2.png)
![image.png](./assets/1642681884531-6dc52913-3685-43ee-baca-7550ac2b833d.png)
![image.png](./assets/1642681904630-bf160fdd-8985-4ad1-9897-0968f5c16ac0.png)
:::

### 继续 PTA 编程题 (2)

#### 2-7
```python
a, b = map(int, input().split(','))
print(str(a) * b)
```

#### 2-8 进制转换
:::info

- 其他进制转十进制，第一个参数是字符串，第二个参数是表示进制数的数字
- `int(s, n)`, `bin(n)`, `oct(n)`, `hex(n)`
:::
```python
a, b = input().split(',')
print(int(a, int(b)))
```

#### 2-9 三个数排序
```python
a, b, c = map(int, input().split())
if b < a:
    a, b = b, a
if c < b:
    b, c = c, b
if b < a:
    a, b = b, a
print(f"{a}->{b}->{c}")
```

#### 2-10 华氏-摄氏温度表
:::info

- `6.1f`表示占 6 格右对齐一位小数
- `range(l, u+1, 2)`的 2 表示步长
:::
```python
l, u = map(int, input().split())
if l > u:
    print("Invalid.")
else:
    print("fahr celsius")
    for i in range(l, u + 1, 2):
        print(f"{i}{5*(i-32)/9:6.1f}")
```

#### 2-11
```python
m, n = map(int, input().split())
print(f"sum = {sum(map(lambda i : i * i + 1 / i, range(m, n + 1))):.6f}")
```

#### 2-12
```python
a, b, c = map(int, input().split())
s = (a + b + c) / 2
if a + b > c and a + c > b and b + c > a:
    print(f"area = {(s * (s - a) * (s - b) * (s - c)) ** 0.5:.2f}; perimeter = {s * 2:.2f}")
else:
    print("These sides do not correspond to a valid triangle")
```

#### 2-13 2-14 不想做了


### 突然做 PTA 函数题

#### 6-1
```python
def fn(a, n):
    return sum(map(lambda i : int(str(a) * i), range(1, n + 1)))
```

#### 6-2
```python
def prime(p):
    if p == 2:
        return True
    elif p == 1 or p % 2 == 0:
        return False
    elif any([i for i in range(3, int(p ** 0.5) + 1, 2) if p % i == 0]):
        return False
    else:
        return True
    
def PrimeSum(m, n):
    return sum([i for i in range(m, n + 1) if prime(i)])
```

#### 6-3
```python
def CountDigit(number,digit):
    return str(number).count(str(digit))
```

#### 6-4
```python
def fib(n):
    i, a, b = 1, 1, 1
    while i < n:
        a, b, i = b, a + b, i + 1
    return b

def PrintFN(m,n):
    i, lst = 0, []
    while True:
        if fib(i) <= m:
            i += 1
        elif fib(i) <= n:
            i += 1
            lst.append(fib(i))
        else:
            break
    return lst
```

#### 6-5
```python
def funcos(eps,x):
    expbase, factbase, thisfact, posneg, res = 1, 1, 1, 1, 0
    thisval = expbase / factbase
    while thisval >= eps:
        res += posneg * thisval
        expbase *= x * x
        factbase *= thisfact * (thisfact + 1)
        thisfact += 2
        posneg *= -1
        thisval = expbase / factbase
    return res
```

#### 6-6
```python
def acronym(phrase):
    return ''.join(list(map(lambda s : s[0], phrase.upper().split())))
```
