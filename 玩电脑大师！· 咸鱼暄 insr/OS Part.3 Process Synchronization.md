
# 6 Synchronization Tools

## 6.1 Background

我们说 **Cooperating Process** 是可以影响系统中其他运行进程或被其他进程影响的进程。
> A **cooperating process** is one that can affect or be affected by other processes executing in the system.

Cooperating processes 会共同使用一些数据，可能是直接使用同一段地址空间（代码+数据），或者是通过共享的内存或信息传递来共用一些数据。对数据的同时访问 (concurrent access) 可能会导致 data inconsistency，因为数据的一致性需要 cooperating processes 有序的运行。看下面一个例子：
```c
/* Bounded-buffer Problem */

/* Producer Process */
while (true) {
    /* produce an item in next_produced */
    while (count == BUFFER_SIZE)
    	; /* do nothing */
    buffer[in] = next_produced;
    in = (in + 1) % BUFFER_SIZE;
    count++;
}

/* Consumer Process */
while (true) {
    while (count == 0)
    	; /* do nothing */
    next_consumed = buffer[out];
    out = (out + 1) % BUFFER_SIZE;
    count--;
    /* consume the item in next_consumed */
}
```
![image.png](./assets/1606538531271-2da84ec2-f0cc-49b9-8bce-50385fa63201.png)
一种可能的运行顺序是：
![image.png](./assets/1606538607576-dcbbb24e-ff78-4e57-a35d-3a95f5b8f4e3.png)
![image.png](./assets/1606538870850-98c7e695-5e25-4f28-bbdf-8b7de2e662d0.png)
出现这个问题，是因为我们允许两个进程同时操控变量 `count` 。类似这样的多个进程同时操控同一个数据，因而结果取决于每一种操控的出现顺序的情形，称为 **race condition**。为了防止 race condition，我们需要保证同一时间只有一个进程可以操控某个变量。
> A situation where several processes access and manipulate the same data concurrently and the outcome of the execution depends on the particular order in which the access takes place, is called a **race condition**. 

Race condition 在操作系统中是常见的。Kernel code 中也包含 race condition 的可能性。如下例：

![image.png](./assets/1606542148202-b7f2337c-060a-41af-ae79-4adb551e5149.png)
两个进程 P0 和 P1 同时 fork() 时，如果不加限制，可能会出现类似前例的情况，即在某一个进程把当前的 `next_avaliable_pid` 分配给他的 child 后，在没来得及更新 `next_avaliable_pid` 前，另一个进程使用了 `next_avaliable_pid` 来给 child 分配 PID，这就会导致两个不同的线程使用同一个 PID 的情况。


##  6.2 The Critical-Section Problem
考虑一个有 n 个进程的系统，每个进程中都有这样一段代码，它可能会修改一些与其他至少一个进程公用的数据，这段代码称为 **critical section**。这个系统的重要性质是，当一个进程正在运行它的 critical section 时，其他进程都不能进入它的 critical section。**Critical-section problem** 就是要设计一种达成这一性质的方法。
> In **critical section**, the process may be accessing — and updating — data that is shared with at least one other process. 
> The **critical-section problem** is to design a protocol that the processes can use to synchronize their activity so as to cooperatively share data.

![image.png](./assets/1606544592560-1e6f5283-c7bb-4de2-9b05-2aeb5a5b8a8e.png)
  每个进程必须在 entry section 中申请进入 critical section 的许可；在 critical section 运行结束后进入 exit section，在这里许可被释放。其他代码称为 remainder section。<br />Critical-section problem 的解决方法必须满足如下三个要求：

- **Mutual exclusion** - 没有两个进程可以同时在运行 critical section。
- **Progress** - 系统整体上是在运行的，即要么有进程在运行它的 critical section，要么没有任何进程想要（将要，即在运行 critical section 之前的 section）进入 critical section，要么在有限时间内将有一个进程被选中进入它的 critical section。
- **Bounded waiting** - 任何一个进程等待进入 critical section 的时间是有限的。即，当一个进程提出一个进入 critical section 的请求后，只有有限个（次）进程会在它之前进入 critical section。

对于单核系统，我们可以通过在 critical section 中禁止中断（即，在 entry section 中 disable，在 exit section 中 enable）的方式来实现上述功能（虽然可能是危险的）。但是对于多核系统，中断禁止的消息要传到所有处理器，消息传递会延迟进入临界区，会降低效率；同时也会影响时钟中断。
![image.png](./assets/1606551048955-1191f1f7-e129-4ff8-a854-9fdcf09391a3.png)


## 6.3 Peterson's Solution
Peterson's solution 解决了两个 task 的 synchornization，并基于 LOAD 和 STORE 过程不会被打断的假设。虽然这一假设在实际的硬件结构中不能保证，但是 Peterson's solution 给出了一个经典的方案来解决 critical-section problem：
```c
int turn;			// Who is allowed to enter
boolean flag[2];	// Ready to enter its CS

void foo() {
    while (true) {
        flag[i] = true; 	// Mark self ready
        turn = 1 - i;		// Assert that if the other process wishes to 
        					// enter its CS, it can do so.
        while (flag[1 - i] && turn == 1 - i);	// Wait
        /* critical section */
        flag[i] = false;	// Set ready to false
        /* remainder section */
    }
}
```
其中， `i` 是 0 或 1，表示第 i 个进程； `turn` 是当前有权进入 critical section 的进程（0 或 1）； `flag[i]` 是第 i 个进程是否准备好进入 critical section，初始值均为 FALSE。<br />To enter the critical section, process Pi first sets `flag[i]` to be true and then sets `turn` to the value `1-i` (the other process), thereby asserting that if the other process wishes to enter the critical section, it can do so. If both processes try to enter at the same time, `turn` will be set to both `0` and `1` at roughly the same time. Only one of these assignments will last; the other will occur but will be overwritten immediately. The eventual value of `turn` determines which of the two processes is allowed to enter its critical section first.<br />我们可以通过简易的分类讨论证明 Peterson's Solution 满足 6.2 中提到的三个性质：Mutual exclusion, process and bounded waiting。<br />但实际上，Peterson's solution 在现代计算机体系结构上不一定适用，因为现代的处理器和编译器有可能会为了优化性能而对一些读写操作进行重排。在优化中，处理器或编译器会考虑其重排的合理性，即保证了在单线程程序中结果值是稳定且正确的。但是这不能保证其在多线程共用数据时的正确性，重排可能会导致不稳定或者不期望的输出。
![image.png](./assets/1606573574517-4bfd5351-5ded-480b-992f-f048d520f027.png)
![image.png](./assets/1606573588613-5d1f5ac4-e5ca-41a8-846c-ee30a57a97f0.png)
Note that reordering of memory accesses can happen even on processors that don't reorder instructions ([Src](https://en.wikipedia.org/wiki/Peterson%27s_algorithm#Note))
[N process Peterson algorithm - GeeksforGeeks](https://www.geeksforgeeks.org/n-process-peterson-algorithm/)

## 6.4 Hardware Support for Synchronization
如上文，software-based 解决方案（它没有使用操作系统或某些硬件操作来保证 mutual exclusion）不能保证在现代计算机体系结构上适用。因此，我们试图寻找一些基于硬件的操作来帮助解决 critial-section problem。

### 6.4.0 Memory Models
没看懂
> How a computer architecture determines what memory guarantees it will provide to an application program is known as its **memory model**. In general, a memory model falls into one of two categories:
> 1. **Strongly ordered**, where a memory modification on one processor is immediately visible to all other processors.
> 2. **Weakly ordered**, where modifications to memory on one processor may not be immediately visible to other processors.

**Memory model **are the memory guarantees a computer architecture makes to application programs.


### 6.4.1 Memory Barriers
部分内容参考 [https://blog.csdn.net/caoshangpa/article/details/78853919](https://blog.csdn.net/caoshangpa/article/details/78853919)。<br />如我们之前所说，编译器和处理器会对代码的结构进行 reorder，以达到最佳效果。例如：
```c
int x = 1;
int y = 2;
int a1 = x * 1;
int b1 = y * 1;
int a2 = x * 2;
int b2 = y * 2;
// 可能会优化为：
int x = 1;
int y = 2;
int a1 = x * 1;
int a2 = x * 2;
int b1 = y * 1;		// a2, b1 的顺序进行了重排
int b2 = y * 2; 
```
对 a2 和 b1 进行重排，使得不需反复读取交替 x 和 y 值。<br />在运行时，CPU 虽然会乱序执行指令，但是在单个 CPU 的上，硬件能够保证程序执行时所有的内存访问操作看起来像是按程序代码编写的顺序执行的，这时候 Memory Barrier 没有必要使用（不考虑编译器优化的情况下）。这里我们了解一下 CPU 乱序执行的行为。在乱序执行时，一个处理器真正执行指令的顺序由可用的输入数据决定，而非程序员编写的顺序。<br />早期的处理器为有序处理器（In-order processors），有序处理器处理指令通常有以下几步：

   - 指令获取
   - 如果指令的输入操作对象（input operands）可用（例如已经在寄存器中了），则将此指令分发到适当的功能单元中。如果一个或者多个操作对象不可用（通常是由于需要从内存中获取），则处理器会等待直到它们可用
   - 指令被适当的功能单元执行
   - 功能单元将结果写回寄存器堆（Register file，一个 CPU 中的一组寄存器）

相比之下，乱序处理器（Out-of-order processors）处理指令通常有以下几步：

   - 指令获取
   - 指令被分发到指令队列
   - 指令在指令队列中等待，直到输入操作对象可用（一旦输入操作对象可用，指令就可以离开队列，即便更早的指令未被执行）
   - 指令被分配到适当的功能单元并执行
   - 执行结果被放入队列（而不立即写入寄存器堆）

只有所有更早请求执行的指令的执行结果被写入寄存器堆后，指令执行的结果才被写入寄存器堆（执行结果重排序，让执行看起来是有序的）<br />从上面的执行过程可以看出，乱序执行相比有序执行能够避免等待不可用的操作对象（有序执行的第二步）从而提高了效率。现代的机器上，处理器运行的速度比内存快很多，有序处理器花在等待可用数据的时间里已经可以处理大量指令了。<br />现在思考一下乱序处理器处理指令的过程，我们能得到几个结论：

   - 对于单个 CPU 指令获取是有序的（通过队列实现）
   - 对于单个 CPU 指令执行结果也是有序返回寄存器堆的（通过队列实现）

由此可知，在单 CPU 上，不考虑编译器优化导致乱序的前提下，多线程执行不存在内存乱序访问的问题。

诸如此类的优化使得程序在运行时的实际内存访问与程序代码编写的访问顺序不一定一致。但是如 6.3 中所提到的，这种重排可能使得在多核运行时出现与期望不同的结果。为了解决这个问题，我们引入 **Memory Barrier**：它用来保证其之前的内存访问先于其后的完成。即，我们保证在此前对内存的改变对其他处理器上的进程是可见的。如 6.3 提出的简单例子：
![image.png](./assets/1606579394097-e92e7a8a-2787-4780-a9fa-b1ad04587e7a.png)
Note that memory barriers are considered very low-level operations and are typically only used by kernel developers when writing specialized code that ensures mutual exclusion.


### 6.4.2 Hardware Instructions
许多现代系统提供硬件指令，用于检测和修改 word 的内容，或者用于 atomically（uniterruptably，不可被打断地） 交换两个 word。这里，我们不讨论特定机器的特定指令，而是通过指令 `test_and_set()` 和 `compare_and_swap()` 抽象了解这些指令背后的主要概念。


#### 6.4.2.1 test_and_set()
指令 `test_and_set()` 可以按如下方式来定义：
```c
bool test_and_set(bool *target) {
    bool rv = *target;
    *target = true;
    return rv;
}
```
这一指令的重要特征是，**它的执行是 atomic 的**。我们可以在支持这个指令的机器上实现 mutual exclusive：定义一个 bool 变量 `lock` ，初始化为 false。进程的结构为：
```c
while (true) {
    /* Entry Section */
    while (test_and_set(&lock)) 	
        ; /* do nothing */
   	
    /* Critical Section */
    
    /* Exit Section */
    lock = false;
    
    /* Remainder Section */
}
```
可见，如果 `lock` 在 Entry Section 时为 true，那么 `test_and_set(&lock)` 将返回 true，因此会始终在 while 循环中询问。直到某个时刻 `lock` 为 false，那么 `test_and_set(&lock)` 将返回 false 同时将 `lock` 置为 true，进程进入 Critical Section，同时保证其他进程无法进入 Critical Section。当持锁的进程完成 Critical Section 的运行，它在 Exit Section 中释放 `lock` ，从而允许其他进程进入 Critical Section。<br />如果某个时刻 `lock` 为 false，而有两个或多个进程几乎同时调用了 `test_and_set(&lock)` 。但由于它是 atomic 的，因此只有一个进程可以返回 false。

但是，如上所示的控制不能满足 bounded waiting 条件：
![image.png](./assets/1606583543590-e3e70d63-2cf9-4a6f-8d4f-61b6e4dabbd5.png)
我们可以作如下更改以满足 bounded waiting：
```c
while (true) {
    /* Entry Section */
    waiting[i] = true;
    while (waiting[i] && test_and_set(&lock)) 	
        ; /* do nothing */
   	waiting[i] = false;
    
    /* Critical Section */
    
    /* Exit Section */
    j = (i + 1) % n;
    while ((j != i) && !waiting[j]))
        j = (j + 1) % n;
    if (j == i)
        lock = false;
    else
        waiting[j] = false;
    
    /* Remainder Section */
}
```
我们引入了 bool 数组 `waiting[]` 。在 Entry Section 中，我们首先置 `waiting[i]` 为 true；当 `waiting[i]` 或者 `lock` 中任意一个被释放时，进程可以进入 Critical Section。初始时， `lock` 为 false，第一个请求进入 CS 的进程可以获许运行。在 Exit Section 中，进程从下一个进程开始，遍历一遍所有进程，发现正在等待的进程时释放它的 `waiting[j]` ，使其获许进入 CS，当前进程继续 Remainder Section 的运行；如果没有任何进程在等待，那么它释放 `lock` ，使得之后第一个请求进入 CS 的进程可以直接获许。<br />这样的方式可以保证每一个进程至多等待 n-1 个进程在其前面进入 CS，满足了 bounded waiting 条件。


#### 6.4.2.2 Compare_and_Swap()
指令 `compare_and_swap()` 可以如下定义：
```c
int compare_and_swap(int *value, int expected, int new_value) {
    int temp = *value;
    if (*value == expected)
        *value = new_value;
    return temp;
}
```
同样，`compare_and_swap()` 的执行是 atomic 的。类似地，我们声明一个全局变量 `lock` ，初始值设为 0。进程的结构为：
```c
while (true) {
    /* Entry Section */
    while (compare_and_swap(&lock, 0, 1) != 0) 	
        ; /* do nothing */
   	
    /* Critical Section */
    
    /* Exit Section */
    lock = 0;
    
    /* Remainder Section */
}
```
可见，`compare_and_swap()` 和 `test_and_set()` 没有本质区别。上例 `compare_and_swap()`  的使用方法同样无法保证 bounded waiting，我们可以使用与 `test_and_set()` 同样的方式来解决。

:::info
在 Intel x86 架构中，汇编指令 `cmpxchg`  用于实现 `compare_and_swap()` 指令；但是不保证是 atomic 的（因为最初用于单核）。我们可以增加前缀 `lock`  来强制实现 atomic。<br />`lock cmpxchg <destination operand>, <source operand>` 
:::


### 6.4.3 Atomic Variables
如我们先前所说，之前介绍的指令常被用来作为同步工具的组成部分而不是直接使用，我们可以使用 `compare_and_swap()` 指令来实现一些工具。其中一个工具就是 **Atomic Variable**。<br />如同我们在 6.1 开始提到的问题那样，一个变量在更新的过程中可能会导致一个 race condition。Atomic Variable 可以为数据提供 atomic updates。例如，我们使用不可打断的 `increment(&count);` 指令来代替可被打断的 `count++` 指令就可以解决 6.1 中的 Bounded-buffer Problem。<br />我们可以如下设计 `increment()` 函数：
```c
void increment(atomic_int *v) {
    int temp;
    do {
        temp = *v;
    } while (temp != compare_and_swap(v, temp, temp+1));
}
```
注意到，程序循环尝试将 `v` 赋值为 `temp+1` ，当赋值成功时返回。由于 CAS 指令是 atomic 的，因此它不会在运行过程中被打断；在程序其他运行过程中 `v` 的值都没有发生改变。<br />但是需要注意的是，如果 buffer 有两个 consumer 在同时等待读取，那么当 `count` 由 0 变成 1 的时候两个 consumer 可能会同时进入来读取，但是实际上只有 1 个值在 buffer 中。即，Atomic Variable 并不能解决所有 race condition，因为它解决的问题仅是变量更新过程中的 race condition。


## 6.5 Mutex Locks
（MUTEX - MUTual EXclusion）<br />我们尝试设计软件工具来解决 CS problem。我们考虑让进程在 Entry Section 申请 `acquire()` 一个锁，然后在 Exit Section `release()` 一个锁。对于这个锁，我们用一个布尔变量来表示它是否 `avaliable` ：
```c
while (true) {
    acquire();
    /* critical section */
    release();
    /* remainder section */
}

/* ------- */
void acquire() {
    while (!available)
        ; /* busy waiting */
    avaliable = false;
}

void release() {
    avaliable = true;
}
```
我们需要保证 `acquire()` 和 `release()` 是 atomic 的。我们可以使用 `test_and_set()` 和 `compare_and_swap()` 来实现：
```c
void acquire() {
    while (compare_and_swap(&available, 1, 0) != 1)
        ; /* busy waiting */
}

void release() {
    available = true;
}
```
但是这种实现的缺点是，它需要 **busy waiting**，即当有一个进程在临界区中时，其他进程在请求进入临界区时在 acquire() 中持续等待，<br />例如当两个进程同时使用一个 CPU 时：
> T0 acquires lock -> INTERRUPT-> T1 runs, spin, spin spin … (till time's out) -> INTERRUPT-> T0 runs -> INTERRUPT->T1 runs, spin, spin spin … -> INTERRUPT-> T0 runs, release locks -> INTERRUPT -> T1 runs, enters CS

可以发现，T1 在它的 CPU 时间内不断循环等待，直到 T0 释放锁。因此这种锁也成为 **spinlock**。可以想象，如果有 N 个进程同时使用一个 CPU，那么将有大约 ![](https://cdn.nlark.com/yuque/__latex/5cc07649359b61b52158b63470984d21.svg#card=math&code=%5Cfrac%7BN-1%7D%7BN%7D&height=37&id=L2Y6K) 的时间被浪费。我们称一个锁 **contended**（被争夺），如果有进程在企图 acquire 它时被阻止；反之我们称它 **uncontended**。如我们所述，highly contended locks 会降低当前运行程序的整体性能。<br />但是，spinlocks 也有其优势：当进程在等待锁时，不需要 context switch，而 context switch 通常需要不短的时间。<br />我们还可以考虑下面的解法：
```c
void acquire() {
    while (compare_and_swap(&avaliable, 1, 0) != 1)
        yield(); 
}

void release() {
    avaliable = true;
}
```
其中 `yield()` 会使程序从 running 转为 ready，从而让出 CPU。<br />Mutex locks 通常被认为是最简单的 synchronization tool。


## 6.6 Semaphores
我们给出一种更厉害的 synchronization tool，称为 semaphore。一个 semaphore `S` 是一个整型变量，它除了初始化外只能通过两个 atomic 操作 `wait()` 和 `signal()` （原称为 `P()` 和 `V()` ）来访问：
```c
void wait(S) {
    while (S <= 0)
        ;	/* busy waiting */
    S--;
}

void signal(S) {
    S++;
}
```
这里通常有 2 种 semaphore：

- **Counting semaphore** - S 的值不受限制；
- **Binary semaphore** - S 的值只能是 0 或 1。类似于互斥锁。

我们可以使用 semaphore 来解决各种同步问题，例如：
![image.png](./assets/1606635803693-a8545283-e07c-4e0f-bae6-8505fe1e68e3.png)

但是，如同前面我们所说，semaphore 也具有 busy waiting 的问题。为了解决这个问题，我们可以为 semaphore 引入 **waiting queue**：
```c
typedef struct {
    int value;
    struct list_head * waiting_queue;
} semaphore; 

wait(semaphore *S) {
    S->value--;
    if (S->value < 0) {
        add this process to S->list;
        block();
    }
}
signal(semaphore *S) {
    S->value++;
    if (S->value <= 0) {
        remove a process P from S->list;
        wakeup(P);
    }
}
```
操作 `block()` 挂起调用它的进程，操作 `wakeup(P)` 重新启动 P 的执行，这两个操作都是由操作系统作为基本系统调用提供的。
> The list of waiting  processes can be easily implemented by a link field in each process control block (PCB). Each semaphore contains an integer value and a pointer to a list of PCBs. One way to add and remove processes from the list so as to ensure bounded waiting is to use a FIFO queue, where the semaphore contains both head and tail pointers to the queue. In general, however, the list can use any queuing strategy. Correct usage of semaphores does not depend on a particular queuing strategy for the semaphore lists.

需要重申的是， `wait()` 和 `signal()` 应该是 atomic 的。
> In a multicore environment, interrupts must be disabled on every processing core. Otherwise, instructions from different processes (running on different cores) may be interleaved in some arbitrary way. Disabling interrupts on every core can be a difficult task and can seriously diminish performance. Therefore, SMP systems must provide alternative techniques—such as `compare_and_swap()` or spinlocks— to ensure that `wait()` and `signal()` are performed atomically.

下面这段没看懂
> It is important to admit that we have not completely eliminated busy waiting with this definition of the `wait()` and `signal()` operations. Rather, we have moved busy waiting from the entry section to the critical sections of application programs. Furthermore, we have limited busy waiting to the critical sections of the `wait()` and `signal()` operations, and these sections are short (if properly coded, they should be no more than about 10 instructions). Thus, the critical section is almost never occupied, and busy waiting occurs rarely, and then for only a short time. An entirely different situation exists with application programs whose critical sections may be long (minutes or even hours) or may almost always be occupied. In such cases, busy waiting is extremely inefficient.


但是，semaphore 可能会导致 deadlock：
![image.png](./assets/1606637016834-083d56ca-fd9f-449d-8f3b-8fd1db4b908f.png)


## 6.7 Priority Inversion
![image.png](./assets/1606637206616-b1f5d0fd-158f-4266-a80b-8e5fed3b5a09.png)
这个问题称为 **priority inversion**，即具有中等优先级的 M 的运行时间反而影响了具有较高优先级的 H 的等待时间。我们可以通过优先级继承 **priority inheritance** 来解决这一问题：所有正在访问资源（如上例中，低优先级的 L 所持的锁）的进程获得需要访问它的更高优先级进程的优先级，直到它们用完有关资源为止。（如上例中，priority inheritance 将允许 L 临时继承 H 的优先级从而防止被 M 抢占；当 L 释放锁后则回到原来的优先级，此时 H 将在 M 之前执行。）
:::info
PRIORITY INVERSION AND THE MARS PATHFINDER
![image.png](./assets/1606637564619-ce1c1fdb-ae3c-4107-85e6-2c61892f712f.png)
:::


# 7 Synchronization Examples

## 7.1 Classic Problems of Synchronization

### 7.1.1 The Bounded-Buffer Problem
我们讨论用 Semaphores 解决 Bounded-Buffer Problem / Producer-Consumer Problem：
:::success
Two processes, the producer and the consumer share n buffers, the producer generates data, puts it into the buffer; the consumer consumes data by removing it from the buffer.<br />The problem is to make sure: the producer won't try to add data into the buffer if it is full; the consumer won't try to remove data from an empty buffer.
:::

首先我们尝试使用一个 `lock`  和一个 `eslot` (empty slot，空闲 buffer 的个数) 来解决：
```c
Semaphore lock = 1;
Semaphore eslot = N;

// Producer:
do {
    wait(eslot);	// will make eslot--
    wait(lock);
    produce();
    signal(lock);
} while (true);
    
// Consumer:
do {
    signal(eslot);	// will make eslot++
    wait(lock);
    consume();
    signal(lock);
} while (true);
```
我们会发现，这种方式不能够满足要求，因为当 buffer 为空，即 eslot 为 N 时，consumer 并不会不运行，因为 signal 并不作判断。因此，我们需要一个额外的 semaphore `fslot`  (full slot) 来解决这个问题：
```c
Semaphore lock = 1;
Semaphore eslot = N;
Semaphore fslot = 0;

// Producer:
do {
    wait(eslot);	// will make eslot--
    wait(lock);
    produce();
    signal(lock);
    signal(fslot);	// will make fslot++
} while (true);
    
// Consumer:
do {
    wait(fslot);	// will make fslot--
    wait(lock);
    consume();
    signal(lock);
    signal(eslot);	// will make eslot++
} while (true);
```


### 7.1.2 The Readers-Writers Problem
:::success
对一些数据，readers 只能读取，而 writers 可以读和写。设计方案保证：多个 readers 可以同时读取，但是 writer 进行写时不能有其他 writers 和 readers。
:::
解决方法：
```c
Semaphore rcnt_mutex = 1;
Semaphore rw_mutex = 1;
int reader_count = 0;

// Writer
do {
    wait(rw_mutex);
    
    read_and_write();
    
    signal(rw_mutex);
} while (true);

// Reader
do {
    wait(rcnt_mutex);			// 保证 reader_count 的同步
    reader_count++;
    if (reader_count == 1)
        wait(rw_mutex);			// 第一个 reader 出现时拿走 rw_mutex
    signal(rcnt_mutex);
    
    read();
    
    wait(rcnt_mutex);			// 保证 reader_count 的同步
    reader_count--;
    if (reader_count == 0)
        signal(rw_mutex);		// 全部 reader 退出时释放 rw_mutex
    signal(rcnt_mutex);
}
```
这种解决策略可能会导致 writer 的 starvation。


### 7.1.3 Dining-Philosophers Problem
:::success
每两个哲学家之间有一根筷子，每个人一次可以拿起来一根筷子，拿到两根筷子的就可以吃一段时间。吃完思考一段时间。
![image.png](./assets/1610672853220-24ba826e-8a4b-4bdc-9879-cd88cc9c5504.png)
:::
![image.png](./assets/1610673972039-98f38896-c8bc-4e8d-bfe7-679d60428bcd.png)
![image.png](./assets/1610674117857-602b10b2-6205-4649-b147-7e937cdb60e7.png)
![image.png](./assets/1610674110296-0fdb6b00-8c5d-4bb7-96be-ada474710173.png)
![image.png](./assets/1610674130285-51ceb2f1-39f5-423e-92be-e6d8ad925f5e.png)
![image.png](./assets/1610674139875-9ea82099-e2f3-4c63-af34-a206ca2cab68.png)

# 8 Deadlock

## 8.3 Deadlock Characterization

### 8.3.1 Necessary Conditions
当下面四个条件同时成立时，系统会出现死锁：

1. **Mutual exclusion** : 至少一个资源处于非共享模式；
2. **Hold and wait** : 一个进程应 **占有** 至少一个资源，并 **等待** 另一个为其他进程占有的资源；
3. **No preemption** : 资源不能被抢占，只能在进程结束后主动释放；
4. **Circular wait** : 有一组等待进程 {T0, T1, ..., Tn}，T0 is waiting for a resource held by T1, T1 is waiting for a resource held by T2, ..., Tn−1 is waiting for a resource held by Tn, and Tn is waiting for a resource held by T0.

这四个条件并不完全独立。
