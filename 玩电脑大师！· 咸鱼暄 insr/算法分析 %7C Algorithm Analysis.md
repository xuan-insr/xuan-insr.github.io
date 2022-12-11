
### Time complexities

![](https://cdn.nlark.com/yuque/__latex/39dfdf394234e6ca20160e52efa012e2.svg#card=math&code=T_%7Bavg%7D%28N%29%2C%20%5C%20T_%7Bworst%7D%28N%29&height=21&id=u0EI5)

![](https://cdn.nlark.com/yuque/__latex/8d9c307cb7f3c4a32822a51922d1ceaa.svg#card=math&code=N%0A&height=16&id=WF2QV) stands for the input. There may be more than one input.<br />Predict the **growth** in run time as the N change.

![](https://cdn.nlark.com/yuque/__latex/3593a694527e68cef7f7673b52fd68ea.svg#card=math&code=T%28N%29%20%3D%20O%28f%28N%29%29%20%5Ctext%7B%2C%20if%7D%5C%20%5C%20T%28N%29%20%5Cleq%20cf%28N%29%2C%20N%20%5Cgeq%20n_0%20&height=20&id=kFcVX)(upper bound)
![](https://cdn.nlark.com/yuque/__latex/6452fe5c13dc1432f41fbaf2a7c3e6d1.svg#card=math&code=T%28N%29%20%3D%20%5COmega%28f%28N%29%29%2C%20%5Ctext%7B%20if%20%7D%5C%20T%28N%29%5Cgeq%20cf%28N%29%2C%20N%5Cgeq%20n_0&height=20&id=aLuUq)(lower bound)
![](https://cdn.nlark.com/yuque/__latex/b5ef597e223ab663a6ec7da3efcebcfa.svg#card=math&code=T%28N%29%20%3D%20%5CTheta%28f%28N%29%29%5C%20%5C%20%5Cequiv%5C%20%5C%20%20T%28N%29%20%3D%20O%28f%28N%29%29%20%5Cland%20T%28N%29%20%3D%20%5COmega%28f%28N%29%29&height=20&id=QdGlh)
![](https://cdn.nlark.com/yuque/__latex/1dea4e698e45435252275a1cd67ea4e0.svg#card=math&code=T%28N%29%20%3D%20o%28f%28N%29%29%5Ctext%7B%2C%20if%20%7D%20T%28N%29%20%3D%20O%28f%28N%29%29%20%5Cland%20T%28N%29%5Cneq%20%5CTheta%28f%28N%29%29&height=20&id=dBnws)

![](https://cdn.nlark.com/yuque/__latex/f97c58a97a83811734453e158124485d.svg#card=math&code=T_1%28N%29%20%3D%20O%28f%28N%29%29%2C%20T_2%20%3D%20O%28g%28N%29%29%2C%20%5Ctext%7Bthen%3A%7D&height=20&id=gYM4r)
![](https://cdn.nlark.com/yuque/__latex/38c91ed3ba3ad217e28d22b067943bb4.svg#card=math&code=T_1%28N%29%20%2B%20T_2%28N%29%20%3D%20O%28%5Cmax%28f%28N%29%2Cg%28N%29%29%29&height=20&id=x0Sw1)
![](https://cdn.nlark.com/yuque/__latex/328320517084d49e755b36578018fc10.svg#card=math&code=T_1%28N%29%5Ctimes%20T_2%28N%29%20%3D%20O%28f%28N%29%5Ccdot%20g%28N%29%29&height=20&id=LupVj)


### 递归函数的复杂度分析示例
```c
long int Fib(int N)
{
    if(N <= 1) return 1;
    else return Fib(N - 1) + Fib(N - 2);
}
```
如上所示是求解斐波那契数列第 N 项值 ![](https://cdn.nlark.com/yuque/__latex/cb0072665108e047bc0c03b5bd3a35ef.svg#card=math&code=F_N&height=18&id=Krytx) 的递归函数。我们用 ![](https://cdn.nlark.com/yuque/__latex/2ce6ca675078d284ed5853fe03197df2.svg#card=math&code=Fib%28N%29&height=20&id=taDW7) 表示函数 Fib(N) 调用 Fib() 的次数。可见：![](https://cdn.nlark.com/yuque/__latex/5e66cc5ba76147f07c17aa58e2819290.svg#card=math&code=Fib%28N%29%20%3D%20%0A%5Cbegin%7Bcases%7D0%2C%5Cquad%20N%20%3D%200%2C%201%5C%5C%0AFib%28N-1%29%2BFib%28N-2%29%2B2%2C%5Cquad%20N%5Cgeq%202%0A%5Cend%7Bcases%7D&height=45&id=E29oK)
其中 ![](https://cdn.nlark.com/yuque/__latex/38beb697680e0b7945aac76b12ad4ab2.svg#card=math&code=%2B2&height=16&id=adsWP) 是调用 Fib(N-1) 和 Fib(N-2) 的两次计数。<br />显然有![](https://cdn.nlark.com/yuque/__latex/9e25e6ffda0363209bbb957291e3f65c.svg#card=math&code=Fib%28N%29%20%5Cgeq%20F_N&height=20&id=nDgTT)。另外，我们可以用数学归纳法证明 ![](https://cdn.nlark.com/yuque/__latex/6886e8bff39f214d662654705afb89ba.svg#card=math&code=Fib%28N%29%5Cgeq%20%28%5Cfrac%2032%29%5EN%2C%5C%20N%5Cgeq%204&height=37&id=wLXIp)。<br />可见，Fib() 函数的时间复杂度 ![](https://cdn.nlark.com/yuque/__latex/d278441290e5580e891c430ef743a6b7.svg#card=math&code=T%28N%29%20%3D%20%5COmega%28%28%5Cfrac%2032%29%5EN%29&height=37&id=DSFVn)，以指数级增长，这是非常差的。另外，它的空间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/d1584c0702ec9e82e73e7e049c972aea.svg#card=math&code=%5CTheta%28N%29&height=20&id=bOXFs)，因为最深的递归层数为 N 层，即栈空间内至多同时储存 N 层递归的相关信息。

