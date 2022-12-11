
# 3 Processes

## 3.1 Process Concept

### 3.1.1 Process
**进程 (Process)** 是被加载到内存中、正在运行的程序。多个进程可能对应同一个程序。一个正在运行的 OS 中会有多个进程。<br />一个进程包括：

   - **code** or **text** 
      - 即程序代码，加载到内存前以 executable file 的形式存储在 disk 中
   - **program counter** 
      - PC，指向下一个要运行的指令
   - content of the processer's **registers** 
      - 在进程之间切换时，需要保存寄存器的值以便下次回到该进程时继续运行
   - **run time stack** 
      - 在 ICS 和汇编语言中学习过相关内容。其中的条目称为 activation records (stack frames)
      - 由用户代码操控（编译时完成关于栈的相关调用），在调用函数时暂时存储一些数据，如 local variables, return address, return values, state of registers, parameters 等
   - **data section** 
      - global variables
   - **heap** 
      - dynamically allocated memory

![image.png](./assets/1610098694878-38e6afbe-d1ef-4a83-a340-e180cebb112e.png)


### 3.1.2 Process State
进程在执行 (execute) 时会改变状态 (state)：

   - **New**: The process is being created
   - **Running**: Instructions are being executed
   - **Waiting**: The process is waiting for some **event** to occur (如等待 I/O 完成或者等待某个信号 _[同步]_)
   - **Ready**: The process is waiting to be assigned to a processor
   - **Terminated**: The process has finished execution

![image.png](./assets/1610099011761-f2959c38-c7aa-4484-a81b-225bb057d8bd.png)
一个处理器上，只有一个进程可以 running，更多的进程可能处于 ready 或 waiting 状态。


### 3.1.3 Process Control Block
操作系统用一个 **Process Control Block (PCB, a.k.a. task control block)** 表示进程，每个进程有且仅有一个 PCB。PCB 包含许多当前进程的相关信息，如：

   - **Process state** 
   - **Program counter** 
   - **CPU registers** ，存储所有进程相关的寄存器的值
   - **CPU scheduling information** ，properities, scheduling queue pointers, etc.
   - **Memory-management information** 
   - **Accounting information** ，CPU 使用时间、时间期限、记账数据等
   - **I/O status information** ，分配给进程的 I/O 设备列表、打开文件列表等

不同的系统可能有不同的 PCB。
![image.png](./assets/1610101423155-8ed964f5-6fea-4d23-af17-4d8880c37459.png)
Linux 中的进程用结构体 `task_struct` 存储。


## 3.2 Process Creation
大多数操作系统通过一个唯一的 **进程标识符 (process indentifier, pid)** 来识别一个进程。一个进程在运行时可以创建新的进程，则它成为父进程，新建进程称为子进程；父进程的 pid 称为子进程的 **ppid (parent's pid)** 。这样进程会成为一个 **进程树 (process tree)** ：
![image.png](./assets/1610102700942-da060db8-8fbb-4ad3-b438-b6cc018d6289.png)
传统的 UNIX 系统用进程 `init` (a.k.a **System V init** , 它的 pid 总是 1) 作为所有用户进程的根进程。系统启动后，进程 `init` 可以创建各种用户进程。在最近的 Linux 版本中， `init` 被 `systemd` 替换了。 `systemd` 功能类似 `init` ，但提供了更多服务。

当子进程被创建时，它会需要一定的资源（CPU 时间、内存、文件、I/O 设备等）来完成任务。它可以从操作系统那里直接获取资源，也可以从父进程那里继承（共享）一些资源。建立子进程时，父进程也可以向子进程传递一些初始化数据，例如父进程创建一个显示图片的子进程时，可以将该图片的路径或文件名等传递给子进程。<br />当进程创建新进程时，父进程可以

   - 继续运行（和子进程并发执行，即同时或者交替运行），或者
   - 等待子进程运行完后再运行

子进程的地址空间有可能

   - 使用父进程的一份拷贝，或者
   - 加载另一个新的程序

UNIX 系统中可以使用系统调用 `fork()` 来创建一个新进程。这个新进程是父进程的一份拷贝，它们只有 pid 和 ppid 不同，另外子进程当前内存使用记录为 0，除此以外全部相同。 `fork()` 对父进程返回该子进程的 pid，而对子进程返回 0。
:::info
`**fork()**`**  如何对父进程和子进程返回不同的值**？

一种实现方式是，在进入 `fork()` 时存下当前的 pid，在建立新进程后（此时存下子进程的 pid），父进程和子进程都将分别完成 `fork()` 剩余代码的执行。在进行返回时， `fork()` 检查当前的 pid 与前面存下的是否一致，如果一致则说明当前是父进程，返回子进程的 pid；不一致则说明是子进程，返回 0。

[https://stackoverflow.com/questions/36640260/how-does-fork-know-when-to-return-0](https://stackoverflow.com/questions/36640260/how-does-fork-know-when-to-return-0)
:::

系统调用 `getpid()` 和 `getppid()` 可以分别获取进程的 pid 和 ppid。



# 4 Threads & Concurrency

## 4.1 Overview

### 4.1.1 Thread & Concurrency
**线程 (Thread) ** 是进程中的基本运行单元。每个线程都有它自己的 thread ID, PC, register set 和 runtime stack。线程与同一进程的其他线程共享 code section, data section, heap, open files 以及 signals。
![image.png](./assets/1610016411385-a8d91f0c-9267-425c-a11c-246db25a900d.png)
**并发 (Concurrency)** : 一个多线程的进程可以同时做多个工作。例如，一个浏览器可能用一个线程来显示文字和图像，另一个线程从网络接受数据。


### 4.1.2 Benefits
采用多线程 (Multi-Threaded Programming) 的优点包括：

   - **Economy:** 建立线程相比进程是很经济的，因为 code, data & heap 已经在内存中了；另外在同一进程的线程间进行 context switch 时也会更快，因为我们不需要 cache flush。
   - **Resource Sharing:** 同一进程的线程之间天然共享内存，因此我们无需为它们编写 IPC；这也允许我们对同一块内存做并行的处理。但这也会引入风险。
   - **Responsiveness:** 多线程的进程会有更好的响应性，即当一个线程 blocked 或者在做一些长时间的操作时，其他线程仍然能完成工作，包括对用户的响应。例如，在一个 client-server 结构中，我们用一个线程来响应客户端的请求。

![image.png](./assets/1610021902308-f76611b4-4be1-4dc0-b177-2e2bc165eaf8.png)

   - **Scalability:** 在多处理器的体系结构中，多线程进程可以更好地发挥作用，因为每个线程都可以在一个处理器上运行；而单线程进程只能在一个处理器上运行。

实际上，后两点对多个单线程进程也是适用的。但多线程进程相较而言更加经济和自然。


### 4.1.3 Drawbacks

   - 如果一个进程出现错误，那么整个进程都会去世（比如浏览器的一个网页挂了，那么可能整个浏览器都会挂）。
   - PPT没看懂
   - 由于 OS 对每个进程地址空间的大小限制，多线程可能会使得进程的内存限制更加紧缩（这在 64 位体系结构中不再是问题）。
   - 由于多个线程共享部分内存，因此内存保护会比较困难。


## 4.2 Multicore Programming
在计算机设计早期，由于计算性能需要，单处理器系统发展成为多处理器 (multiprocessor) 系统。之后的设计倾向于将多个芯片上的计算核放在同一个芯片上，我们称之为多核 (multicore) 系统。放在同一个芯片上的好处在于其协同性更好、通信更加简单。在我们接下来的讨论涉及的问题中，这两种系统区别不大。<br />考虑一个进程，它有 4 个线程。对一个单核系统，这 4 个线程 **并发 (concurrent)** 执行，即它们随着时间流逝交错进行：
![image.png](./assets/1610027448066-ee5a1c8c-973f-4cb1-b7b9-529641f76dcc.png)
但在多核系统上，线程可以 **并行 (parallel)** 执行，即同时可以有多个任务被执行：
![image.png](./assets/1610027519326-948ff8cf-6e19-498b-82e8-10c0c58ef948.png)
当然，并行执行也是一种并发执行。

OS 的设计者必须编写算法以更好地利用多个处理核。一般而言，多核系统编程有 5 个方面的挑战：

   - **Identifying tasks.** 应用程序需要被分为独立、并发的任务。在理想状态下，这些任务互相独立，从而可以在不同的处理核上并行执行。
   - **Balance.** 各个任务应当执行同等价值的工作，否则有的任务相较而言对整个任务的贡献并不多，那么用一个单独的处理核来运行这一任务就不值得了。
   - **Data splitting.** 既然程序已经被分为独立的任务，那么由任务访问的数据也应该划分以运行在单独的处理核上。
   - **Data dependency.** 应当妥善分析被任务访问的数据的依赖关系。当一个任务的数据依赖另一个任务时，程序员必须保证运行的同步以保证数据的依赖关系。我们会在第 6 章讨论这一话题。
   - **Testing and debugging.** 多线程并行执行时有多种可能的运行顺序，这会使测试与调试更加困难。

总的来说，并行分为两种：**数据并行 (data parallelism)** 和 **任务并行 (task parallelism)**。数据并行注重将数据分布在多个计算核上，在每个计算核上作相同操作；而任务并行注重将任务（线程）分配到多个计算核，每个任务进行不同的操作，操作的数据可以相同或不同。当然，这两种模式并非互斥，应用程序会混合使用这两种策略。
![image.png](./assets/1610031785601-8c326151-d589-4d1a-a221-19deb1aa18da.png)


## 4.3 Multithreading Models
用户线程会使用系统调用等

# 5 CPU Scheduling

## 5.1 Basic Concepts
CPU 调度就是 OS 关于哪个 ready 进程或线程可以运行（使用 CPU）以及运行多久的决定。这在 multi-programming 环境下是必要的，关系到系统的整体效率。其目标是始终允许某个进程运行以最大化 CPU 利用率。

### 5.1.1 CPU-I/O Burst Cycle
大多数进程在 CPU 执行和 I/O 执行之间反复横跳。
![image.png](./assets/1610039729682-610832f2-8333-4de6-b3c7-dabc9182b320.png)
有两种进程，一种是 I/O-bound process，它大量的时间用于等待 I/O，还有很多小的 CPU 使用；另一种是 CPU-bound process，它大部分时间在使用 CPU，可能包含小的 I/O 使用。这些进程的不同，给 CPU scheduling 带来了困难。
![image.png](./assets/1610039972851-f4d31567-5230-4c8a-8f92-23233a04e984.png)

### 5.1.2 The CPU Scheduler
每当 CPU 空闲，OS 就应该选择一个 ready process 来运行。

   - **非抢占式调度 (Non-preemptive scheduling)** : 一个进程可以不断运行直到它主动释放 CPU。也称为 **cooperative scheduling** 。
   - **抢占式调度 (Preemptive scheduling)** : 一个进程会被抢占，即使它 "could have happily continued executing"。


### 5.1.3 Scheduling Decision Points
![image.png](./assets/1610099011761-f2959c38-c7aa-4484-a81b-225bb057d8bd.png)
Revisit<br />CPU 调度可能出现在某一个进程：

   1. Running -> Waiting，如等待 I/O
   2. Running -> Ready，当发生了 interrupt，如计时器到时间了
   3. Waiting -> Ready，如 I/O 完成了
   4. Running -> Terminated
   5. New -> Ready

非抢占式调度只会在 a, d 处进行调度，因为只有这时候当前正在运行的进程不能再运行了；抢占式调度会发生在上述任何时机。因此，抢占式调度使得 OS 有更充分的控制，但它也更复杂。


### 5.1.4 Dispatcher
CPU 调度功能的实现者是 **调度程序 (dispatcher)** 。这个模块包括：

   - Context switch
   - Switching to user mode
   - Jumping to the proper location in the user program to resume that program

Dispatcher 停止一个进程而启动另一个所需的时间称为 **调度延迟 (dispatch latency)** ：
![image.png](./assets/1610042691629-f65e9316-a983-480d-af6e-5a69ba324623.png)
由于每次进程切换时都要使用 dispatcher，因此 dispatch latency 应尽可能短。


## 5.2 Scheduling Criteria / Objectives
对于不同的应用场景，我们对 scheduling 的要求也有所不同，有些也会有冲突。为此，我们需要充分考虑各种算法的属性。我们可能需要的要求包括：

   - Maximize **CPU Utilization** : CPU 使用率，即 CPU 非空闲的时间比例
   - Maximize **Throughput** : 吞吐量，每个时间单元内完成的进程
   - Minimize **Turnaround Time** : 周转时间，从进程创立到进程完成的时间，包括等待进入内存、在 ready queue 中等待、在 CPU 上执行、I/O 执行等时间
   - Minimize **Waiting Time** : 等待时间，在 ready queue 中（或在 Ready 状态下）等待所花的时间之和
   - Minimize **Response Time** : 响应时间，交互系统从进程创立到第一次产生相应的时间

这些要求有时甚至是冲突的。例如，较多的 context switch 会减少 throughput，因为 context switch 过程中并没有有用的工作；而较少的 context switch 会增加 response time。


## 5.3 Scheduling Algorithms
基于上述不同目的，多种调度算法被设计出来。


### 5.3.1 First-Come First-Served (FCFS)
先申请 CPU 的进程首先获得 CPU。可以用一个 FIFO 队列简单实现。<br />**甘特图 (Gantt chart)** 。
![image.png](./assets/1610065703003-12e6e500-4e53-42d8-98c3-2a20d013cea4.png)
There is a **convoy effect** as all the other processes wait for the one big process to get off the CPU. This effect results in lower CPU & device utilization than might be possible if the shorter processes were allowed to go first.


### 5.3.2 Shortest-Job-First Scheduling

#### 5.3.2.1 Non-preemptive: Shortest-next-CPU-burst
每当 CPU 调度时，其选取 ready queue 中下次 CPU 执行时间最短的进程。这样会使得给定的一组进程具有 minimum average waiting time.
![image.png](./assets/1610066482609-7fed1ec0-341c-4a2a-8d8b-012c3bdc3049.png)


#### 5.3.2.2 Preemptive: Shortest-remaining-time-first
每当 CPU 调度时（注意抢占式调度的调度时机），选择最短剩余运行时间的进程。
![image.png](./assets/1610066600223-c4edadac-a528-4d92-8185-46a8a637f04d.png)


#### 5.3.2.3 Discussion
SJF 在 average wait time 这一指标上是最优的。但是一个重要的问题是如何知道下次 CPU 执行的长度。"This  problem is typical of the disconnect between theory and practice." 因此我们试图预测 CPU 的下次执行长度。<br />下次 CPU 的执行时长通常预测为之前 CPU 执行时长的 **指数平均  (exponential average)** ，即：<br />![](https://cdn.nlark.com/yuque/__latex/8d5775f5825ee10546a8639439ba770e.svg#card=math&code=%5Cbegin%7Bequation%7D%0A%5Cbegin%7Baligned%7D%0A%5Ctau_%7Bn%2B1%7D%26%3D%5Calpha%20t_n%2B%281-%5Calpha%29%5Ctau_n%5C%5C%26%3D%5Calpha%20t_n%2B%281-%5Calpha%29%5Calpha%20t_%7Bn-1%7D%2B%5Ccdots%2B%281-%5Calpha%29%5Ej%5Calpha%20t_%7Bn-j%7D%20%2B%20%5Ccdots%20%2B%20%281-%5Calpha%29%5E%7Bn%2B1%7D%5Ctau_0%0A%5Cend%7Baligned%7D%0A%5Cend%7Bequation%7D%0A&height=47&id=vK2mr)
其中 ![](https://cdn.nlark.com/yuque/__latex/2ec030dc98820f99243c0c7dc30deb2c.svg#card=math&code=t_n&height=16&id=eEfD6) 是第 ![](https://cdn.nlark.com/yuque/__latex/7b8b965ad4bca0e41ab51de7b31363a1.svg#card=math&code=n&height=12&id=GbOUu) 次执行时长，![](https://cdn.nlark.com/yuque/__latex/6367548b10f43de7d442439ca5815a49.svg#card=math&code=%5Ctau_%7Bn%2B1%7D&height=14&id=M2GIy) 是第 ![](https://cdn.nlark.com/yuque/__latex/40b85027598d87611b1c8d5d11e46812.svg#card=math&code=n%2B1&height=12&id=rNk5O) 次执行时长预测值，![](https://cdn.nlark.com/yuque/__latex/7b7f9dbfea05c83784f8b85149852f08.svg#card=math&code=%5Calpha&height=12&id=XsRK1) 是一个参数，控制最近和过去历史在预测中的权重。
![image.png](./assets/1610068014367-0f6346c4-4f2d-4042-ad78-97fbb1abaffd.png)


### 5.3.3 Round-Robin Scheduling
RR Scheduling is preemptive and designed for time-sharing.<br />定义一个 **时间片 (time slice / time quantum)** ，即一个固定的较小时间单元 (10-100ms)。除非一个 process 是 ready queue 中的唯一进程，它不会连续运行超过一个时间片的时间。Ready queue 是一个 FIFO 的循环队列。每次调度时取出 ready queue 中的第一个进程，设置一个计时器使得进程在一个时间片后发生中断，然后 dispatch the process。
![image.png](./assets/1610068659879-a8b5bad6-fb94-4ae8-95c6-ca85f4ccac73.png)
RR scheduling 的性能很大程度上取决于时间片的大小。如果时间片较小，则 response/interactivity 会很好，但会有较大的 overhead，因为有较多的 context-switch；时间片较大则响应较差，但 overhead 会较小。如果时间片 -> INF，则 RR->FIFO。<br />在实践中，时间片大约 10~100ms，每次 contest-switch 约 10μs。即 context-switch 的时间花费是比较小的。


### 5.3.4 Priority Scheduling
每个进程都有一个优先级，每次调度时选取最高优先级的进程。
![image.png](./assets/1610205036381-0fbebe99-11e9-4bfe-a23b-bb18c9bda108.png)
优先级可以是内部的或者外部的：

   - internal: 一些测量数据，例如 SJF 是 Priority 的一个特例，即优先级由预测 CPU 运行时间决定。
   - external: 由用户指定进程间的重要性。 

Priority Scheduling 也可以与 Round-Robin 结合，如：
![image.png](./assets/1610205223703-19ef7694-8cd1-4bc9-a4d8-44b8d44d5dbc.png)

要实现 Priority Scheduling，可以简单地将 ready queue 用 priority queue 实现；priority queue 也可以是抢占式或非抢占式的，如 SJF 一样。<br />Priority 的一个重要问题是 **indefinite blocking** / **starvation** ，即低优先级的进程可能永远没有机会被执行。一个解决方法是 **Priority Aging** ，即根据等待时间逐渐增加在系统中等待的进程的优先级。


### 5.3.5 Multilevel Queue Scheduling
在实际应用中，进程通常被分为不同的组，每个组有一个自己的 ready queue，且每个队列内部有自己独立的调度算法。例如，前台队列使用 RR 调度以保证 response，后台队列可以使用 FCFS。同时，队列之间也应当有调度。通常使用 preemptive priority scheduling，即当且仅当高优先级的队列（如前台队列）为空时，低优先级的队列（如后台队列）中的进程才能获准运行。也可以使用队列间的 time-slicing，例如一个队列使用 80% 的时间片而另一个使用 20%。例如：
![image.png](./assets/1610207047375-3debb6bc-58ce-476a-88bf-f517da7ea787.png)


### 5.3.6 Multilevel Feedback Queue Scheduling
Multilevel Feedback Queue Scheduling 允许进程在队列之间迁移。这种算法可以有很多种实现，因为队列的数量、每个队列中的调度策略、队列之间的调度算法以及将进程升级到更高优先级/降级到更低优先级的队列的条件都是可变的。一个系统中的最优配置在另一个系统中不一定很好。这种算法也是最为复杂的。<br />看这样一个例子：有三个队列 0, 1, 2，优先级逐次降低。当进程 ready 时被添加到 Q0 中，Q0 内部采用 RR Scheduling，的每个进程都有 8ms 的时间完成其运行，如果没有完成则被打断并进入 Q1；只有当 Q0 为空时 Q1 才可能被运行。Q1 内部也使用 RR Scheduling，每个进程有 16ms 时间完成其运行，如果没有完成则被打断并进入 Q2；只有当 Q1 也为空时 Q2 才可能被运行。Q2 内部采用 FCFS 算法。
![image.png](./assets/1610275706648-6027496f-77ca-4ad8-b663-13a07576b959.png)


## 5.4 Thread Scheduling
