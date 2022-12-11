
## 4 实验过程

### 4.1 环境搭建
编译前后的文件结构如图：
![image.png](./assets/1609687487410-5c5a5dcf-9a85-4126-9383-2604111bd525.png)

### 4.2 添加系统调用处理函数
我们在 strap.c 中增加了系统调用处理函数：
```c
size_t handler_s(size_t scause, size_t sepc, uintptr_t *regs)
{
	size_t return_value;
	if ((scause & 0x8000000000000000) != 0)	//interrupt
	{
		scause = scause & 0x7fffffffffffffff;
		switch (scause)
		{
			case 5:
			__asm__(
				"ecall\n\t");
				do_timer();
				break;
			default:
				break;
		}
	}
	else	//exception
	{
		switch (scause)
		{
			case 0x8:
				return_value = do_ecall_from_U(regs);
				break;
			case 0xc:
				do_instruction_page_fault();
				break;
			case 0xd:
				do_load_page_fault();
				break;
			case 0xf:
				do_store_page_fault();
				break;
			default:
				break;
		}
		__asm__(
			"csrr t0, sepc\n\t"
			"addi t0, t0, 4\n\t"
			"csrw sepc, t0\n\t");
	}
	return return_value;
}

size_t do_ecall_from_U(uintptr_t * regs)
{
	size_t return_value;
	//系统调用的参数
	size_t reg_a0 = *(uintptr_t *)((char *)regs + 22 * 8);
	size_t reg_a1 = *(uintptr_t *)((char *)regs + 21 * 8);
	size_t reg_a2 = *(uintptr_t *)((char *)regs + 20 * 8);
	size_t reg_a3 = *(uintptr_t *)((char *)regs + 19 * 8);
	size_t reg_a4 = *(uintptr_t *)((char *)regs + 18 * 8);
	size_t reg_a5 = *(uintptr_t *)((char *)regs + 17 * 8);

	//系统调用号
	size_t reg_a7 = *(uintptr_t *)((char *)regs + 15 * 8);

	switch (reg_a7)
	{
		case 64:
			return_value = sys_write(reg_a0, reg_a1, reg_a2);
			break;
		case 172:
			return_value = sys_getpid();
			break;
		default:
			break;
	}
	*(uintptr_t *)((char *)regs + 22 * 8) = return_value;
	return return_value;
}


size_t sys_write(unsigned int fd, const char *buf, size_t count)
{
	size_t puts_count = 0;
	char temp[2] = {'\0', '\0'};
	while(count!=1)
	{
		temp[0] = *buf;
		puts(temp);
		buf++;
		puts_count++;
		count--;
	}
	return puts_count;
}

size_t sys_getpid()
{
	long pid = current->pid;
	return (size_t)pid;
}
```
这里，我们为了满足 `sys_write` 的计数，每次只输出一个字符（通过将每个字符放在一个 `'\0'` 前面）从而实现这一点。

我们增加了对应头文件 syscall.h：
```c
#include"sched.h"
typedef long long unsigned int size_t;
typedef unsigned long long uintptr_t;     //定义上下文的结构

//系统调用处理函数
size_t handler_s(size_t scause, size_t sepc, uintptr_t *regs);

/*
    64号系统调用sys_write():
    该调用将用户态传递的字符串打印到屏幕上，此处fd为标准输出（1），buf为用户需要打印的起始地址，count为字符串长度，返回打印的字符数。 
*/
size_t sys_write(unsigned int fd, const char *buf, size_t count);

/*
    172号系统调用sys_getpid():
    该调用从current中获取当前的pid放入a0中返回，无参数。
*/
size_t sys_getpid();

//处理ecall from User mode
size_t do_ecall_from_U(uintptr_t *regs);
```
在 head.S 中，我们设置了相应委托：
```c
	#设置environment call from U mode委托
	li t1, 1
	slli t1, t1, 8		#t1=0000 0001 0000 0000
	csrs medelg, t1
```


### 4.3 修改进程初始化以及进程调度相关逻辑
本次实验中，由于实验要求，我们只进行了 SJF 模式的相关修改。

我们在结构体 `thread_struct` 中增加了如下内容以满足进程切换的要求：
```c
    unsigned long long sepc;
    unsigned long long sscratch;
    struct mm_struct mm;
```
其中 `mm_struct` 中只保存了根页表的地址：
```c
struct mm_struct {
	unsigned long long *pgtbl;
};
```
我们增加了对每个用户程序的内存映射函数：
```c
void task_paging_init(struct task_struct *tsk) {
	tsk->thread.mm.pgtbl = (uint64_t *)(cur += 0x1000);
	// kernel
	create_mapping(tsk->thread.mm.pgtbl, (uint64_t)&text_start, (uint64_t)&text_start-offset, (uint64_t)&rodata_start - (uint64_t)&text_start, 5);
    	create_mapping(tsk->thread.mm.pgtbl, (uint64_t)&rodata_start, (uint64_t)&rodata_start-offset, (uint64_t)&data_start - (uint64_t)&rodata_start, 1);
   	create_mapping(tsk->thread.mm.pgtbl, (uint64_t)&data_start, (uint64_t)&data_start-offset, 0x1000000 - ((uint64_t)&data_start - (uint64_t)&text_start), 3);
	// UART
	create_mapping(tsk->thread.mm.pgtbl, 0xffffffdf90000000, 0x10000000, 0x1000, 11);
	// User Program
	create_mapping(tsk->thread.mm.pgtbl, 0x0, 0x84000000, 0x1000, 15);
	// User Stack
	create_mapping(tsk->thread.mm.pgtbl, 0xffffffdf80000000 - 0x1000, cur+=0x1000, 0x1000, 15);
}
```
对应地，我们对各个 task 的初始化也作了一些调整：<br />`task[i] = (struct task_struct *)((cur+=0x1000)+offset);` <br />`task[0]->thread.sp = 0xffffffdf80000000;` 

在发生中断或异常时，我们需要对用户栈和内核栈进行切换。这里我们的方案核心思路是，用 `sp` 作为当前栈的同时，用 `sscratch`  保存另一个栈的栈指针。即，在用户态运行时， `sp` 是用户栈而 `sscratch` 保存内核栈；在处理中断或异常时，这两个寄存器作交换， `sp` 指向内核栈， `sscratch` 保存用户栈。我们对 entry.S 做了相应修改：
![image.png](./assets/1609686943118-5f23d28b-7276-4702-b895-5f67906ff116.png)


### 4.4 用户态测试程序
为了加载用户态程序，我们对 Makefile 作了对应修改：
![image.png](./assets/1609619888528-b1e612a5-b32a-4f40-ba6e-1719d524cf67.png)
并对每个 task，我们将虚拟地址空间中 `0x0` 开始的一个 page 映射到物理地址空间中的 `0x84000000` 处：<br />`create_mapping(tsk->thread.mm.pgtbl, 0x0, 0x84000000, 0x1000, 15);`


### 4.5 编译及测试
我们在 SJF 模式下测试，得到了预期结果：
![image.png](./assets/1609683443283-a3ab82d7-fdaf-487c-a54d-3e9668315147.png)
改为 63 个进程后也可以得到正确的结果：
![image.png](./assets/1609684146799-695aebd8-c3ba-41ba-b1fc-8f9d0cbf6bd6.png)

## 5 心得体会
本次实验指导比较简略，因此我们花费了一些时间梳理需要完成的任务以及一些具体的实现思路。总体上来说，本次实验内容的方面比较多，当发现出错时很难定位问题。由于对 UART 作了映射，因此通过输出进行调试的方法也不可靠（当没有输出时无法判定是程序运行过程出现了错误还是对 UART 的映射不正确），这使得调试难度进一步增加。

本次实验过程中遇到了很多问题，我们用了很长的时间进行调试。下面是调试的部分细节：<br />我们发现切换到用户模式后程序不能正常运行。我们怀疑是映射出现了问题，因此我们将 `paging_init` 和 `task_paging_init`  的页表分配情况进行了输出进行检查：
![image.png](./assets/1609684903218-e71b804b-9622-42d6-9d10-25645c08922f.png)
进一步检查时发现，由于我们分配页表的方式有问题，在 `task_paging_init` 时，我们分配给 UART 的页表和分配给用户程序的是同一张，这导致 UART 的映射出现错误，因此没有输出：
![image.png](./assets/1609685041421-954652ec-b34c-4456-ac36-8b549b8a1d38.png)
![image.png](./assets/1609685081090-4ed53b79-779a-4a1c-b388-178ff417e242.png)
![image.png](./assets/1609685105347-0834684f-0b6f-4182-af76-1031eef83345.png)
发现这个问题之后，我们对页表的分配方式进行了修改。

另外，我们在调试过程中发现用户栈不平衡，进而导致之后的进栈出栈出现问题（未保留截图）。分析后我们发现，我们进行出栈后没有改变 `sp` 的值。在之前的实验中，我们不改变 `sp`  的值的原因是我们已经预先保存了 `sp`  并在出栈时恢复了；但这次由于用户栈和内核栈的互换，这里并不能通过出栈恢复 `sp` 的值。因此我们增加了手动改变 `sp` ：
![image.png](./assets/1609685271212-46cd76f0-e26a-4512-bb89-73cb6078faf1.png)

总体而言，这次实验对我们理解虚拟内存以及用户态的相关知识有很大帮助，但是我们认为本次实验的难度也非常大，我们花费了很长的时间进行编写和调试。本次实验中，我们也发现了一些之前存在的问题，同时由于时间或者条件限制，有些问题的解决是比较特殊的，只能大致满足本次实验的要求。这些问题也需要我们在之后使用更加通用的方法进行解决。本次实验的后期过程较为仓促，因此代码中可能仍然存在一些问题，这也有待后续更细致的调试以及更多功能的实现过程中再来发现并解决。

（另外希望实验指导可以更详细一些😥）
