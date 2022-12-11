
## 题型
- Multiple choice                             22%
- Comprehensive problems              78%
   - Data representation                               10% 
      - 数的表示
      - 进制转换
      - 运算（符号扩充 SEXT、溢出）
      - 浮点数的表示
   - Gate circuit/truth table                           8%
   - Read LC3 programs / disassembly           9%
   - Implement a new instruction                  12%
   - LC3 programming                                  12%
   - Interruption                                           13%
   - Read LC3 programs /programming         14%          

<br />

## 复习

#### 浮点数表示
**Floating Point Data Type.** Figure (IEEE Floating Point Arithmetic). There is:

      - 1 bit for the sign (positive or negative)
      - 8 bits for the range (exponent, 指数, 表示范围). The actural exponent being represented is the unsigned number in the data type minus 127.
      - 23 bits for precision (fraction, 尾数, 表示精度). As the fraction is normalized, that is, exactly 1 nonzero binary digit appears to the left of the binary point, which has to be 1. So there is no need to represent that bit explicitly. Thus the fraction in data type is the numbers appear to the right of the point.

![image.png](./assets/1593932844071-2990a188-d0be-4aea-a758-b2560697e3f6.png)
![](https://cdn.nlark.com/yuque/__latex/cc2102486b9f67c1875192a2594ff3e7.svg#card=math&code=E.g.%20%5Cquad%20-6%5Cfrac%7B5%7D%7B8%7D%20%3D%20-110.101%20%3D%20-1.10101%20%5Ctimes2%5E2&height=37&width=306)
![](https://cdn.nlark.com/yuque/__latex/4d2674ba0af7330c74ab231ecf26817f.svg#card=math&code=%5Ctext%7Bsign%20bit%3A%201%2C%20exponent%7D%20%3D%202%2B127%20%3D%20129%20%3D%2010000001%2C%20%5Ctext%7B%20fraction%3A%7D10101%5C%20000000000000000000&height=18&width=631)
![](https://cdn.nlark.com/yuque/__latex/c57e4478206fad2dedb28d8a1d16e11d.svg#card=math&code=%5Ctext%7BThe%20number%7D-6%5Cfrac5%208%20%5Ctext%7B%20expressed%20as%20a%20floating%20point%20number%3A%201%2010000001%2010101000000000000000000%7D&height=37&width=687)


#### 伪代码 | Pseudo-operations
do not refer to operations executed by program<br />used by assembler
![image.png](./assets/1600387744376-e3df8df6-972f-4e15-bc4e-16e0fd08b3ca.png)

