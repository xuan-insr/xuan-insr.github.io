
# 11 Mass-Storage Structure

## 11.1 Overview
现代计算机的大部分二级存储由 **hard disk drives (HDDs)** 和 **nonvolatile memory (NVM)** 设备提供。<br />磁盘驱动器（Disk Drive）可以看做 **logical block** 的一维数组，logical block 是最小的传输单位。


### 11.1.1 Hard Disk Drives
HDD 的结构相对简单。
![image.png](./assets/1610818263655-7b382fd9-b22a-4bec-ae9a-12e68f238748.png)
如上图，每个 disk platter（盘片）长得像 CD，直径一般 1.8~3.5 inches。Disk platter 的两面附着有磁性材料，我们通过磁性记录在其上保存信息，并通过检测其上的磁性模式来读取信息。<br />每个 platter 附近有一个 read-write head，read-write head 附着在 disk arm 上，arm 会使所有 head 形成整体共同移动。<br />Platter 表面被分成了很多环形 track（磁道），再细分为 sector（扇区）。在一个 arm position 下的 track 组成一个 cylinder（柱面）。
![image.png](./assets/1610819081925-65262149-6877-41ee-ad2e-f327aee33ca6.png)
Sector 被编号，是 logical block address 在 disk drive 上的映射。编号的原则如下：以最外 cylinder 的第一个 track 的第一个 sector 为 0，然后该 track 上的 sector 依次编号，然后是 cylinder 中的其他 track，然后是内部的 cylinder。<br />使用磁盘时，电机高速旋转磁盘。参数 **Rotation Per Minute (RPM)** 是每分钟旋转的次数，普通的 HDD 通常为 5400, 7200, 10000, 15000RPM。

**Transfer Rate**：在 HDD 和计算机之间数据流的速率（理论 6Gb/sec，实际 1Gb/sec）
:::danger
[!] Gb - Gigabit; GB - Gigabyte. 1GB = 8Gb.
:::
**Positioning Time** (a.k.a **random-access time**)：将 disk arm 移动到所需要的 sector 所用的时间。包含两部分：

   - **Seek time** - 将 arm 移动到所需 cylinder 所用时间（3ms - 12ms）
   - **Rotational latency** - 旋转到 head 在所需 sector 上所用时间（与转速有关）

![](https://cdn.nlark.com/yuque/__latex/c66b105277fa36b3c8a3f852d1b661cc.svg#card=math&code=Average%5C%20access%5C%20time%20%3D%20average%5C%20seek%5C%20time%20%2B%20average%5C%20latency&height=18&width=441)
![](https://cdn.nlark.com/yuque/__latex/610e9e6e6b8cf4c4e1b74b6e11a01741.svg#card=math&code=Average%5C%20I%2FO%5C%20time%20%3D%20average%5C%20access%5C%20time%20%2B%20%5Ccfrac%7Bdata%5C%20to%5C%20transfer%7D%7Btransfer%5C%20rate%7D%20%2B%20controller%5C%20overhead&height=52&width=615)

![image.png](./assets/1610822511208-b96d44fd-3465-4222-a06a-eb4f8499cb8e.png)

Head 有和 platter 接触的风险。此时 platter 表面可能被损坏（**head crash**），这是无法修复的。


### 11.1.2 Nonvolatile Memory Devices
NVM devices 是电子的而非机械的。
> Solid-state disks (SSD), USB drives (thumb drive, flash drive), DRAM disk replacements, surface-mounted on motherboards, and main

比 HDD 更可靠，也更贵，可能寿命更短，容量更小，但是快很多。标准总线可能会太慢，所以有的 SSD 设计成直接连接到系统总线，如 PCI。<br />没有移动的部分，所以没有 seek time 和 rotational latency。

NAND Flash 是一种 NVM device。<br />Read & write 是以 page (e.g. 4k) 为单位的，但是在重新写入之前必须 erase，且 erase 发生在更大的 block (64k, i.e. 16 pages)。Erase 的次数有限 (~100000)。生命周期用 **drive writes per day (DWPD)** 表征，即预期寿命内每天可以完整写入驱动器总大小的次数。e.g. 1TB, 5DWPD 保证预期寿命内每天可以写 5TB 不失败。<br />由于没有 overwrite，因此 page 是 valid 和 invalid 的混合。为了了解哪些 logical block（r/w 的基本单位，即 page），controller 维护一个 **flash translation layer (FTL) table**。Controller 还实现 **garbage collection (GC)** 来 free invalid page space，分配额外空间（over-provisioning）来给 GC 等提供工作空间（将 valid data 暂时放在 over-provisioning 并 erase the block）。<br />每个 cell 都有自己的生命周期，因此应尽量平衡使用它们。
![image.png](./assets/1610822116122-f046bc9b-aa04-4b85-8eb7-2bc772707cf6.png)


### 11.1.3 Magnetic Tape
早期的二级内存。现在主要用来备份不常用的信息。<br />空间很大（200GB ~ 1.5TB），访问很慢，随机访问特别慢。


## 11.2 Disk Scheduling
OS 需要负责硬件使用的高效性。对于 disk drives 来说，OS 需要提供一个 fast access time 和 high disk bandwidth。我们讨论 HDD。

   - **access time** : seek time (roughly linear to seek distance) + rotational latency
   - **disk bandwidth** : the speed of data transfer (data bytes / time from request to completion)

每当进程需要进行磁盘 I/O 时，它向 OS 发出一个系统调用，包括信息：输入/输出，磁盘地址，内存地址，扇区数。如果目标磁盘的驱动器和控制器正忙，则加入请求队列（每个 disk 或 device 有一个队列）。Disk scheduling 需要选择队列中的一个请求来使其下一个使用目标磁盘。

通常主要目标是 minimize **seek time。**对计算机来说，rotational latency 很难算。<br />下面的调度算法，均使用 request queue of cylinders "98, 183, 37, 122, 14, 124, 65, 67" ([0, 199]), and initial head position 53 as the example。

> In the past, operating system responsible for queue management, disk drive head scheduling
> Now, built into the storage devices, controllers - firmware
> Just provide LBAs, handle sorting of requests
> Some of the algorithms they use described next


### 11.2.1 First-Come First-Served (FCFS)
Advantages: 

   - Every request gets a fair chance 
   - No indefinite postponement

Disadvantages: 

   - Does not try to optimize seek time 
   - May not provide the best possible service

![image.png](./assets/1610823094099-0279425e-0a8b-4f69-833b-b1dbc142fd61.png)


### 11.2.2 Shortest Seek Time First (SSTF)
类似 SJF，选择离现在 head position 最近的 request。但是 SSTF 不一定最好。
![image.png](./assets/1610823400263-fa316129-4c39-45b9-beb9-b52f8addde7e.png)
Advantages: 

   - Average Response Time decreases
   - Throughput（吞吐量） increases

Disadvantages: 

   - Overhead to calculate seek time in advanse
   - Starvation may exist
   - High variance : favors only some requests


### 11.2.3 SCAN / Elevator algorithm
从一边往另一边走，选择路上的 request 不回头，直到到达另一端反向。
![image.png](./assets/1610824004349-94e8fe81-ce9b-4673-8a58-428753d0f35d.png)
Advantages: 

   - Average Response Time
   - High Throughput
   - Low variance of response time

Disadvantages: 

   - Long waiting time for requests for locations just visited by disk arm


### 11.2.4 C-SCAN
Circular-Scan：到达一端时立刻回到开头。
![image.png](./assets/1610824200602-97701733-8ea4-4490-9123-38f7aa42c4e0.png)
Advantage:

   - Provides more uniform（均匀） wait time compared to SCAN


### 11.2.5 LOOK / C-LOOK
在 SCAN / C-SCAN 的基础上，只走到一端最后一个任务（look 是否有请求）而不走到头。
![image.png](./assets/1610824434537-3ba07ffe-c147-462f-a2ba-0e9c401eee3b.png)
Advantage:

   - Prevents the extra delay which occurred due to unnecessary traversal to the end of the disk.


### 11.2.6 Selecting Disk-Scheduling Algorithm
取决于请求的数目和类型。SSTF 最常见，但是当 I/O 负荷较大时，使用 LOOK / C-LOOK 以避免 starvation。
> disk performance can be influenced by file-allocation and metadata layout
> file systems spend great deal of efforts to increase spatial locality



## 11.3 Disk Management
**Physical formatting** （物理格式化, a.k.a **low-level formatting**, 低级格式化）：将 disk 分成 sectors 以便 read/write。
> Each sector can hold header information, plus data (Usually 512 bytes of data, 但可选), plus error correction code (ECC)
> ECC: 写入一个扇区的数据时，计算数据区域的字节数并存储；读取时重新计算并比较，如果不一样则表明扇区数据区已损坏。

在可以使用磁盘存储文件之前，OS 需要将自己的数据结构存到磁盘上。

- Step 1：将 disk 分为由柱面组成的多个分区（**partition**），每个分区都可以当做一个单独的磁盘
- Step 2 - **Logical formatting**：创建一个文件系统（**file system**）。有些 FS 预留一些 sectors 来处理 bad blocks。FS 可能将 block 组合成更大的 clusters，以其为 File I/O 的单位，提高效率。
- 如果 partition 包含 OS image，则初始化 boot sector。

> Root partition contains the OS, other partitions can hold other OSes, other file systems, or be raw 
> Mounted at boot time 
> Other partitions can mount automatically or manually 
> At mount time, file system consistency checked 
> Is all metadata correct? 
> If not, fix it, try again 
> If yes, add to mount table, allow access
> Boot block can point to boot volume or boot loader set of blocks that contain enough code to know how to load the kernel from the file system 
> Or a boot management program for multi-os booting
> Raw disk access for apps that want to do their own block management, keep OS out of the way (databases for example) 
> Boot block initializes system 
> The bootstrap is stored in ROM, firmware 
> Bootstrap loader program stored in boot blocks of boot partition 
> Methods such as sector sparing used to handle bad blocks
> ![image.png](./assets/1610826791296-1390cff0-e706-4b42-bb9c-47eb3e2334b2.png)



## 11.4 Swap Space Management


# 12 I/O Systems











