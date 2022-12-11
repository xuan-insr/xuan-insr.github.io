
## 5 实验过程

### 5.1 环境搭建
编译前后的文件结构如图：<br />前： ![image.png](./assets/1611515372082-a12bcc09-b81f-4968-9fee-1a645a85f689.png)


### 5.2 管理空闲内存空间 ，在 buddy.c 中实现 buddy system
我们实现了如下的 buddy system 内存分配：
```c
extern unsigned long long _end;
#define GET_POWER_2(x) (x==1 ? 1 : 1<<log_2(x-1)+1)
short bitmap[8192], size = 4096;
short log_2(int x) {
	short i = 0;
	for (;; i++) {
		x >>= 1;
		if (!x)	return i;
	}
}
short ind2fn(int index) {
	short level = log_2(index);
	short level_head = 1 << level;
	short l_offset = index - level_head;
	short level_base = 1 << (log_2(size) - level);
	short frame_num = l_offset * level_base;
	return frame_num;
}
void *alloc_pages(int num) {
	if (num <= 0)	return 0;
	num = GET_POWER_2(num);
	int index = 1;
	while (index < size) {
		if (bitmap[index << 1] < num && bitmap[(index << 1) + 1] < num) {
			bitmap[index] = 0;
			for (int i = index >> 1; i; i >>= 1)
				bitmap[i] = (bitmap[i << 1] > bitmap[(i << 1) + 1]) ? bitmap[i << 1] : bitmap[(i << 1) + 1];
			return 0x80000000 + ind2fn(index) * 0x1000;
		}
		int smallerChild = index << 1, largerChild = index << 1, select;
		if (bitmap[(index << 1) + 1] < bitmap[index << 1]) smallerChild++;
		else	largerChild++;
		if (num <= bitmap[smallerChild]) select = smallerChild;
		else	select = largerChild;
		index = select;
	}
	bitmap[index] = 0;
	for (int i = index >> 1; i; i >>= 1)
		bitmap[i] = (bitmap[i << 1] > bitmap[(i << 1) + 1]) ? bitmap[i << 1] : bitmap[(i << 1) + 1];
	return 0x80000000 + ind2fn(index) * 0x1000;
}

void init_buddy_system(void) {
	for (int i = 1; i < size * 2; i++) {
		bitmap[i] = 1 << (log_2(size) - log_2(i));
	}
	alloc_pages(((unsigned long long)&_end - 0x80000000) / 0x1000 + 4);
}

void free_pages(void* ptr) {
	int frame_num = (int)((unsigned long long)ptr - 0x80000000) / 0x1000;
    int ind = size + frame_num;
    while (bitmap[ind] != 0) {
    	ind >>= 1;
	}
	bitmap[ind] = 1 << (log_2(size) - log_2(ind));
	while (ind > 0) {
		ind >>= 1;
		if (bitmap[ind << 1] == bitmap[(ind << 1) + 1] && bitmap[ind << 1] == 1 << (log_2(size) - log_2(ind << 1)))
			bitmap[ind] = 1 << (log_2(size) - log_2(ind));
		else
			bitmap[ind] = (bitmap[ind << 1] > bitmap[(ind << 1) + 1]) ? bitmap[ind << 1] : bitmap[(ind << 1) + 1];
	}
}
```
`log_2(x)` 是对 2 取对数的函数；<br />`ind2fn(x)` 是根据给出的 `bitmap` 中的序号（index，即满二叉树的节点序号）获取对应的页号。<br />`alloc_pages(num)` 是 buddy system 分配 `num` 个 page 的函数。其思路是查找 `bitmap` 代表的满二叉树，每次前往值较小且值不小于 `num` 的儿子节点，当到达叶结点或者当前节点的两个儿子节点都比 `num` 小时，当前节点即为所给的分配。分配后，向上返回并更新每一个父亲节点为较大的儿子节点的值（只有当两个儿子均为未分配的状态下，父亲节点的值才不是较大儿子节点的值，而是它们之和。但是在进行分配过后，两个儿子不可能均未分配，因此这种算法是合理的）。<br />`free_pages(ptr)` 是 buddy system 收回 page 的函数。收回 page 的首要步骤是找到该地址是从哪里分配的，即其大小是多少。由于一个地址有可能对应 `bitmap` 上多个结点，因此我们需要进行查找。核心思路是：分配这一部分 pages 的 `bitmap` 项取值应为 0，因此我们从粒度为 1 page，即叶子结点向上查找，查看其 `bitmap`项值是否为 0。如果为 0，那么这就是当时分配的 index。我们可以根据这个 index 算出其大小，然后继续向上回溯，依次判断该结点的父亲和祖先的两个儿子是否都为未分配，如果是，则合并两个儿子节点，即将父节点的值改为未分配的值；否则，将父节点的值更新为两个儿子中较大的值。


### 5.3 其他任务
我们尝试了在 slub.c 中实现 slub 内存动态分配算法以及实现统一内存分配接口，但是出现了 bug。由于时间原因，我们没有完成该部分内容的调试。此后的任务，我们也由于时间原因暂时没有尝试。


### 5.4 更新物理页分配逻辑
我们将之前实验中直接指定的 Kernel 物理地址替换成了用 buddy.c 中实现的 `alloc_pages`  进行分配的地址。相关修改代码包括：<br />（注：其中注释掉的修改是我们尝试使用 `kmalloc()` 但失败的过程，我们现在将这些物理页分配都使用 `alloc_pages()` 实现，并没有使用 slub 动态分配内存）
![image.png](./assets/1611568099567-919812d7-59d4-46c7-b94f-95bed3e81988.png)
![image.png](./assets/1611568192809-cdd27794-599c-4533-a315-640e2cbd6723.png)
![image.png](./assets/1611568205864-a10b1487-ea60-4450-8be6-0d7a227e54e8.png)
![image.png](./assets/1611568212813-9e0a41a4-ab8c-4b63-9532-58d38ef6ecd8.png)
![image.png](./assets/1611568221665-e0aa2bf2-e2c3-44d2-b09f-da527123c1a9.png)


### 5.5 编译及测试
我们对之前 vm.c 和 sched.c 中的内存分配做了相应修改后，进行编译测试，得到了正确的结果（由于后续任务没有进行，我们除了内存分配外仍然沿用 Lab5 的其他内容）：
![image.png](./assets/1611516336723-12707b0c-d5d1-4b70-a660-1930383fd047.png)
由于实验中并未调用 `free_pages()` 函数，我们设计了 C 语言代码对其进行了单独测试：<br />（注：为了方便检查结果，这里将 `size` 暂时设为了 8。）
```c
int main() {
	init_buddy_system();
	
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
		
	void *ap1 = alloc_pages(3);
	printf("\n Alloc 3 pages - %p\n", ap1);
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
		
	void *ap2 = alloc_pages(1);
	printf("\n Alloc 1 page  - %p\n", ap2);
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
		
	void *ap3 = alloc_pages(2);
	printf("\n Alloc 2 pages - %p\n", ap3);
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
	
	free_pages(ap2);
	printf("\n Free 1 page\n");	
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
		
	free_pages(ap3);
	printf("\n Free 2 pages\n");	
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
		
	free_pages(ap1);
	printf("\n Free 3 pages\n");	
	for (int i = 1; i <= 15; i++)
		printf(" %d %d |", i, bitmap[i]);
	return 0;
}
```
![image.png](./assets/1611518327324-c653426c-5607-4ff4-a666-eefbcf82279a.png)

:::info
由于时间原因，后面的任务并未完成。
:::


## 6 思考题
**`fork`系统调用为什么可以有两个返回值？**<br />对于父进程来说，fork()仅仅是调用了一个syscall，调用完成后会返回一个值给父进程以显示调用函数的运行情况；对于子进程来说，fork()了之后，子进程的PC会被赋值为父进程的PC，所以将会返回到父进程调用fork()的后一条指令。至于返回值，是因为函数调用的返回值存在X0寄存器里面，而在执行fork()的时候，子进程会将X0寄存器的值赋为0，故而子进程收到的返回值就为0。


## 7 心得与体会
本次实验由于处在考试周，并没有充足的时间完成，因此只完成了 buddy system 的实现。该部分更加偏向数据结构的相关操作，也体现了我们在之前几次实验的基础上，已经开始进行了更加丰富的设计。为了检验 buddy system 的实现正确性，我们首先设计了独立的 C 语言代码对其进行测试，得到了正确的结果后再与之前实验的内存分配进行结合。这样的方法保证了正确性，并且一定程度上节省了调试的时间。<br />下图为用 C 语言测试和调试的截图：
![image.png](./assets/1611516297204-54da5da6-e380-4013-a976-75fec51ed59b.png)
