
# 1 Overview

## 1.1 Computer-System Organization

### 1.1.1 Storage Structure
CPU 只能从内存中加载指令，因此执行程序必须位于内存。计算机大多数程序通常位于可读写内存，称为 **主存** (main memory) 或 **随机访问内存** (Random Access Memory, RAM)，通常为 DRAM (Dynamic RAM)。计算机也使用其他形式的内存，如 **只读内存** (Read-Only Memory, ROM) 和 **电可擦可编程只读内存** (Electrically Erasable Programmable Read-Only Memory, EEPROM)。ROM 不可修改，因此只能将静态程序存在其中；EEPROM 可以修改，但是不能经常修改，因此可以保存大多数的静态程序。<br />当计算机电源打开或重启以便开始运行时，它需要一个初始程序（引导程序，bootstrap program）。这个程序通常很简单，一般位于计算机的 **固件** (firmware)，如 ROM 或 EEPROM。<br />各种内存都有一个字节数组，每个字节都有地址。指令 `load` 和 `store` 实现内存和 CPU 寄存器之间的交互，CPU 也会自动加载内存指令以便执行。<br />但是，我们不可能将程序和数据都永久存在内存中，因为内存通常比较小，而且它是 volatile（易失）的，掉电时就会失去所有内容。因此，我们使用 secondary storage（外存；二级内存；辅存）来扩充内存。外存能够永久存储大量数据。
![image.png](./assets/1602812176263-ef0f6dc4-65cd-4e39-8915-b72e95d98e34.png)
存储设备的层次

The CPU is the piece of hardware that modifies the content of memory.\In fact, one can really think of the CPU as a device that movesone memory state (i.e, all the stored content) to another memory state (some new, desired stored content)
![image.png](./assets/1604449186636-7738f0f0-f993-412d-9497-702514983a13.png)


### 1.1.2 Interrupts & I/O Structure

#### 1.1.2.1 Basic Interrupt Mechanism
事件发生通常通过硬件或软件的 **中断 (interrupt)** 来通知。中断机制的基本工作方式如下：CPU 硬件有一条称为 interrupt-request line 的线路，CPU 在执行每一条指令后都要检测它一次。当 CPU 侦测到一个设备控制器在这条线路上发出的信号时，会读取 interrupt number 并且以此作为 interrupt vector 中的 index 来跳转到对应的 interrupt-handler routine。CPU 会存储可能在中断处理过程中被改变的状态，然后执行中断处理程序，执行完后 CPU 恢复进入中断之前的状态并执行一个 `return_form_interrupt` 指令，使 CPU 回到中断发生前的执行状态。<br />We say that the device controller _**raises**_ an interrupt by asserting a signal on the interrupt request line, the CPU _**catches**_ the interrupt and _**dispatches**_ it to the interrupt handler, and the handler _**clears**_ the interrupt by servicing the device. 
![image.png](./assets/1604476630125-b20cf220-b74b-46fd-b76b-28b1c86a4a8d.png)
![image.png](./assets/1604453059062-ee2b8d41-c75a-4db8-9c83-cd5577585e67.png)

#### 1.1.2.2 More sophisticated features
在现在的操作系统上，我们还需要一些更复杂的终端处理功能：

1. 我们需要能够在关键程序处理期间延迟中断的处理；
2. 我们需要一种高效的方法来将设备中断发给正确的中断处理程序；
3. 我们需要多级中断，从而使得操作系统可以区分不同优先级的中断并根据适当的紧急程度进行响应。

在现代的计算机硬件中，这些特性由 CPU 和 interrupt-controller hardware 实现。

大多数 CPU 有两条 interrupt-request line，一条用于 nonmaskable interrupt，为一些不可恢复的内存错误等事件保留；另一条是 maskable 的，它可以在执行不可中断的关键程序之前被 CPU 关闭，用于传送一些设备控制器的中断请求。<br />中断向量表 (interrupt vector) 用来减少确定中断服务时的查找次数。但事实是，计算机的中断处理程序比中断向量表的地址元素要多。


Recall that the purpose of a vectored interrupt mechanism is to reduce the need for a single interrupt handler to search all possible sources of interrupts to determine which one needs service. In practice, however, computers have more devices (and, hence, interrupt handlers) than they have address elements in the interrupt vector. A common way to solve this problem is to use interrupt chaining, in which each element in the interrupt vector points to the head of a list of interrupt handlers. When an interrupt is raised, the handlers on the corresponding list are called one by one, until one is found that can service the request. This structure is a compromise between the overhead of a huge interrupt table and the inefficiency of dispatching to a single interrupt handler. <br />Figure 1.5 illustrates the design of the interrupt vector for Intel processors. The events from 0 to 31, which are nonmaskable, are used to signal various error conditions. The events from 32 to 255, which are maskable, are used for purposes such as device-generated interrupts. <br />The interrupt mechanism also implements a system of interrupt priority levels. These levels enable the CPU to defer the handling of low-priority interrupts without masking all interrupts and makes it possible for a high-priority interrupt to preempt the execution of a low-priority interrupt. <br />In summary, interrupts are used throughout modern operating systems to handle asynchronous events (and for other purposes we will discuss throughout the text). Device controllers and hardware faults raise interrupts. To enable the most urgent work to be done first, modern computers use a system of interrupt priorities. Because interrupts are used so heavily for time-sensitive processing, efficient interrupt handling is required for good system performance.
![image.png](./assets/1604453129761-3acf352b-6162-48d3-b609-fbd4fcd1712a.png)
The form of interrupt-driven I/O described in Section 1.2.1 is fine for moving small amounts of data but can produce high overhead when used for bulk data movement such as NVS I/O. To solve this problem, direct memory access (DMA) is used. After setting up buffers, pointers, and counters for the I/O device, the device controller transfers an entire block of data directly to or from the device and main memory, with no intervention by the CPU. Only one interrupt is generated per block, to tell the device driver that the operation has completed, rather than the one interrupt per byte generated for low-speed devices. While the device controller is performing these operations, the CPU is available to accomplish other work. Some high-end systems use switch rather than bus architecture. On these systems, multiple components can talk to other components concurrently, rather than competing for cycles on a shared bus. In this case, DMA is even more effective. Figure 1.7 shows the interplay of all components of a computer system.
![image.png](./assets/1604453247854-205631aa-cf22-419c-86d4-9f56c9df49a4.png)


# 2 OS Structures
![image.png](./assets/1609953211471-b3b1bb5a-a40f-4715-a16e-35f751bf4f3a.png)
![image.png](./assets/1609953200053-1fae6558-1308-4260-8953-cf1a3ea88e45.png)

Signal:
```cpp
#include <iostream>
#include <csignal>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>

using namespace std;

void signalHandler( int signum )
{
    cout << "Interrupt signal (" << signum << ") received.\n";

    // cleanup and close up stuff here  
    // terminate program  

   exit(signum);  

}

int main ()
{
    // register signal SIGINT and signal handler  
    signal(SIGINT, signalHandler);  

    while(1){
       cout << "Going to sleep...." << endl;
       sleep(1);
    }
    return 0;
}
```
当 CTRL+C 时发出 SIGINT 信号，程序打印
```
Going to sleep..
Going to sleep..
Going to sleep..
Interrupt signal (2) received.
```
[https://my.oschina.net/lvyi/blog/734251](https://my.oschina.net/lvyi/blog/734251)
