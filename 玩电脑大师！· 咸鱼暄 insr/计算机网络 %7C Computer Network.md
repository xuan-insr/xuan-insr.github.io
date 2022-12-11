

### 开始之前
本文是《计算机网络》课程（自学）笔记，文中提到的“课本”指清华大学出版的《计算机网络（第 5 版）》，另外较大程度上参考了王道 2022 年计网考研复习指导；除此之外也部分参考了《计算机网络 自顶向下方法（第 7 版）》帮助部分内容的理解。对于参考的博客等网络资料，如果有直接引用的部分一般标注了来源；其他资料并未全部标明出处。

- 部分实验报告放在了 [GitHub](https://github.com/smd1121/zju-course)。
- Cisco Packet Tracer 的使用记录：[Cisco Packet Tracer 使用记录](https://www.yuque.com/xianyuxuan/coding/qkw2i9?view=doc_embed)
- 参与了朋辈辅学讲解计网，**录播** 在：
   - 物理层				[https://www.bilibili.com/video/BV1Xr4y1r7gM](https://www.bilibili.com/video/BV1Xr4y1r7gM)
   - 数据链路层			[https://www.bilibili.com/video/BV1rb4y1t7JB](https://www.bilibili.com/video/BV1rb4y1t7JB/)
   - 介质访问控制子层 I		[https://www.bilibili.com/video/BV1WZ4y197xQ](https://www.bilibili.com/video/BV1WZ4y197xQ)
   - 介质访问控制子层 II	[https://www.bilibili.com/video/BV1SZ4y197RN](https://www.bilibili.com/video/BV1SZ4y197RN)
   - 网络层 I				[https://www.bilibili.com/video/BV1RZ4y1977Y](https://www.bilibili.com/video/BV1RZ4y1977Y)
   - 网络层 II				[https://www.bilibili.com/video/BV1Tq4y1B7cH](https://www.bilibili.com/video/BV1Tq4y1B7cH)
   - 传输层				[https://www.bilibili.com/video/BV1sD4y1c7QR](https://www.bilibili.com/video/BV1sD4y1c7QR)
   - 应用层				[https://www.bilibili.com/video/BV1V44y177eS](https://www.bilibili.com/video/BV1V44y177eS)
   - 典型题目选讲			[https://www.bilibili.com/video/BV13R4y1s72m](https://www.bilibili.com/video/BV13R4y1s72m)


### 尝试用思维导图做笔记！
（点击思维导图后左边六个点那里可以全屏）

- 如果思维导图不方便看，可以看文字版：

[计网思维导图文字版](https://www.yuque.com/xianyuxuan/coding/gez9yl?view=doc_embed)
![](./assets/1639906191521-e1e4b7d2-fc54-4ec8-9d45-543d194f624d.jpeg)

### 一些补充

#### 1 带宽

:::success
我们可以将要发送的信号分解为傅里叶级数。在实际工程中，我们只会取傅里叶级数的前若干项来对信号进行传输；下图展示了二进制信号 01100010 通过 1, 2, 4, 8 个谐波传输的实际波形：

可以看到，使用 8 个谐波就可以较好地传输所需的信号；所用谐波数越少，信号的质量越差，出错的可能也就越大。<br />不同傅里叶分量的区别在于其频率和振幅，第 ![](https://g.yuque.com/gr/latex?i#card=math&code=i&id=Toxi7) 个傅里叶分量的频率是第 1 个（**基频** ![](https://g.yuque.com/gr/latex?f#card=math&code=f&id=hTOb8)）的 ![](https://g.yuque.com/gr/latex?i#card=math&code=i&id=eOZQ7) 倍。而实际问题是，现实中的传输媒体对不同频率谐波的振幅有不同程度的衰减，这就会导致信号产生变形。

对于导线而言，从 0 Hz 到某个频率 ![](https://g.yuque.com/gr/latex?f_c#card=math&code=f_c&id=cjj53)（我们称之为 **截止频率**）的谐波在传输过程中不会有明显减弱，我们称 0 ~ ![](https://g.yuque.com/gr/latex?f_c#card=math&code=f_c&id=teMPn) 的这段频率宽度为 **带宽 (bandwidth)**。事实上，截止频率并没有那么尖锐，因此我们有时也把从 0 到使得接受能量保留一半的那个频率之间的宽度称为带宽。<br />带宽会对 data rate 产生一定的限制。举例来说，如果 data rate 为 ![](https://g.yuque.com/gr/latex?r#card=math&code=r&id=qcbEK) bps，传输 ![](https://g.yuque.com/gr/latex?b#card=math&code=b&id=SnoA6) bit 的信号（就像这里的例子那样）就需要 ![](https://g.yuque.com/gr/latex?%5Ccfrac%20br#card=math&code=%5Ccfrac%20br&id=cOab5) 秒，因此信号的基频就是 ![](https://g.yuque.com/gr/latex?%5Ccfrac%20rb#card=math&code=%5Ccfrac%20rb&id=s9nMe) Hz **_（为什么？）_**；因此我们可以接受的谐波个数 ![](https://g.yuque.com/gr/latex?N#card=math&code=N&id=mb2d9) 就需要满足 ![](https://g.yuque.com/gr/latex?N%5Ccdot%20%5Ccfrac%20rb%5Cleq%20f_c#card=math&code=N%5Ccdot%20%5Ccfrac%20rb%5Cleq%20f_c&id=rEonx)，即 ![](https://g.yuque.com/gr/latex?N%20%5Cleq%20%5Ccfrac%7Bb%5Ccdot%20f_c%7Dr#card=math&code=N%20%5Cleq%20%5Ccfrac%7Bb%5Ccdot%20f_c%7Dr&id=WDcVA)。我们很容易理解，![](https://g.yuque.com/gr/latex?N#card=math&code=N&id=N3BOD) 与信号的质量成正相关，因此 ![](https://g.yuque.com/gr/latex?r#card=math&code=r&id=OeUoB) 过大时，信号的质量就会受到影响。下图展示了 ![](https://g.yuque.com/gr/latex?b%20%3D#card=math&code=b%20%3D&id=im89r) 8 bits, ![](https://g.yuque.com/gr/latex?f_c%20%3D#card=math&code=f_c%20%3D&id=o8LR2) 3 kHz 时的一个例子。
![image.png](./assets/1633608028637-3bc1e78e-a3d9-456f-bb03-e5c162417fa0.png)
正是因为这里所说的带宽（对电气工程师来说）与 ![](https://g.yuque.com/gr/latex?%5Cmax%7B(r)%7D#card=math&code=%5Cmax%7B%28r%29%7D&id=SFiB1) 有如此大的关系，因此我们也会将 data rate 的最大值称为带宽（对计算机科学家来说）。

带宽是传输介质的一种物理特性；滤波器可以通过过滤掉某些频率的信号来进一步限制信号的带宽。

带宽指的是一段频率范围，它并不要求这段频率一定从 0 开始；事实上对于无线信道来说，发送低频率的信号也是不可能的。我们称之前所说的频率为 0 ~ B Hz 的信号为 **基带信号 (baseband signal)**，而将其搬移到 S ~ S+B Hz 的信号为 **通带信号 (passband signal)**。

为了检验学习成果，思考：为什么从每秒发送 _b_ 个 bit 到每秒发送 _mb_ 个 bit，所需带宽是原来的 _m_ 倍？
:::


#### 2 码分多址

:::info
考虑这样的问题：我们有若干由 1 或 -1 组成的序列。对于每个序列 ![](https://g.yuque.com/gr/latex?S#card=math&code=S&id=wVQnM)，我们用 ![](https://g.yuque.com/gr/latex?%5Coverline%20S#card=math&code=%5Coverline%20S&id=zdrof) 表示其反码（序列中的每个数取其相反数）。对于任意两个序列 ![](https://g.yuque.com/gr/latex?S#card=math&code=S&id=MfxmB) 和 ![](https://g.yuque.com/gr/latex?T#card=math&code=T&id=gCY99)，我们定义其 **归一化内积 (normalized inner product)** ![](https://g.yuque.com/gr/latex?S%5Ccdot%20T%20%5Cequiv%20%5Cfrac%201m%5Csum_%7Bi%3D1%7D%5Em%20S_iT_i#card=math&code=S%5Ccdot%20T%20%5Cequiv%20%5Cfrac%201m%5Csum_%7Bi%3D1%7D%5Em%20S_iT_i&id=VgbLL)，其中 ![](https://g.yuque.com/gr/latex?m#card=math&code=m&id=a8o4V) 是序列的长度，此处为 8。容易理解，有 ![](https://g.yuque.com/gr/latex?S%5Ccdot%20S%20%3D%201#card=math&code=S%5Ccdot%20S%20%3D%201&id=Z64IW)，![](https://g.yuque.com/gr/latex?S%5Ccdot%20%5Coverline%20S%20%3D%20-1#card=math&code=S%5Ccdot%20%5Coverline%20S%20%3D%20-1&id=Kfyv6)。若 ![](https://g.yuque.com/gr/latex?S%5Ccdot%20T%20%3D%200#card=math&code=S%5Ccdot%20T%20%3D%200&id=cmHSX)，我们称这两个序列是 **正交 (orthogonal)** 的；显然此时 ![](https://g.yuque.com/gr/latex?%5Coverline%20S%20%5Ccdot%20T%20%3D%20S%5Ccdot%5Coverline%20T%20%3D%20%5Coverline%20S%5Ccdot%5Coverline%20T%3D0#card=math&code=%5Coverline%20S%20%5Ccdot%20T%20%3D%20S%5Ccdot%5Coverline%20T%20%3D%20%5Coverline%20S%5Ccdot%5Coverline%20T%3D0&id=qulEC)。根据这一定义，图中 (a) 的 4 个序列是两两正交的。

现在我们尝试利用这些序列发送信号。每个发送端被分配了一个序列；每一个周期中，发送端可以选择发送 1（通过发送这个序列），或者发送 0（通过发送这个序列的反码），或者什么都不发送。当多个站同时发送时，它们发送的信号会叠加起来；但是由于序列的正交性，我们可以将每个站发送的信息单独解码出来。假设在某一个周期中，A 和 D 发送了 0，B 发送了 1，C 什么都没有发送，那么叠加出的信号就形如 ![](https://g.yuque.com/gr/latex?S%20%3D%20%5Coverline%20A%20%2B%20B%20%2B%20%5Coverline%20D%20%3D%20(1%2C-1%2C3%2C-1%2C1%2C3%2C-1%2C-1)#card=math&code=S%20%3D%20%5Coverline%20A%20%2B%20B%20%2B%20%5Coverline%20D%20%3D%20%281%2C-1%2C3%2C-1%2C1%2C3%2C-1%2C-1%29&id=rkiaC)。我们将这个信号与 ![](https://g.yuque.com/gr/latex?B#card=math&code=B&id=jngT8) 作归一化内积：![](https://g.yuque.com/gr/latex?S%5Ccdot%20B%20%3D%20%5Cfrac%20%7B-1%2B1%2B3%2B1%2B1%2B3-1%2B1%7D8%3D1#card=math&code=S%5Ccdot%20B%20%3D%20%5Cfrac%20%7B-1%2B1%2B3%2B1%2B1%2B3-1%2B1%7D8%3D1&id=Cxhwd)，即 B 发送的是 1。如果与 ![](https://g.yuque.com/gr/latex?C#card=math&code=C&id=Z38bo) 作归一化内积，则结果为 0，表示 C 什么都没有发送。如果与 ![](https://g.yuque.com/gr/latex?A#card=math&code=A&id=zwBlL) 或 ![](https://g.yuque.com/gr/latex?D#card=math&code=D&id=Rg54Y) 做归一化内积，则结果为 -1，表示发送的是反码（即 0）。这是因为，归一化内积满足分配律，![](https://g.yuque.com/gr/latex?S%5Ccdot%20D%20%3D%20%5Coverline%20A%5Ccdot%20D%20%2B%20B%5Ccdot%20D%20%2B%20%5Coverline%20D%5Ccdot%20D#card=math&code=S%5Ccdot%20D%20%3D%20%5Coverline%20A%5Ccdot%20D%20%2B%20B%5Ccdot%20D%20%2B%20%5Coverline%20D%5Ccdot%20D&id=Sacr1)，而前两项由于正交性为 0，第三项为 -1，因此最终结果为 -1；其他的情况也是类似的。图中有更多的实例。

下面回顾我们做了什么。我们在原本需要发送 1 个 bit 的时间发送了 ![](https://g.yuque.com/gr/latex?m#card=math&code=m&id=QjBo3) 个 bit 组成的序列，这样的序列可以有 ![](https://g.yuque.com/gr/latex?m#card=math&code=m&id=s2B2D) 个且两两正交（考虑正交矩阵），从而满足 ![](https://g.yuque.com/gr/latex?m#card=math&code=m&id=H3MDu) 个发送方同时互不干扰地传输的需要。同时由于我们在单位时间内传输的 bit 数是原来的 ![](https://g.yuque.com/gr/latex?m#card=math&code=m&id=Vnrts) 倍，因此所需要的带宽也是原来的 ![](https://g.yuque.com/gr/latex?m#card=math&code=m&id=JssWJ) 倍（回顾 **_1 带宽_** 的思考题）；如此我们将一个窄带信号扩展到一个很宽的频带上，这样更能容忍干扰，同时允许多个用户共享同一个频带。因此我们称这样的码分复用技术为 **码分多址 CDMA, Code Division Multiple Access**。
![image.png](./assets/1633673317422-35efb2f6-e494-4f73-a4f5-64312cd2e1fc.png)
:::


#### 3 物理层计算中的“采样频率”
:::success
Sampling frequency 实际上就是 Baud rate 的理论上限之一，和带宽共同约束 Baud rate 的上限。 

看一些题目：

- **一条无噪声的 8kHz 信道，每个信号包含 8 级，每秒采样 24k 次，那么可以获得的最大传输速率是**
   - 无噪声 - Nyquist，data rate = 2 * 8kHz * log_2(8) bit/symbol = 48kbps 
   - “题目中给出的每秒采样 24k 次是无意义的，因为超过了波特率的上限 2W = 16 kBuad，所以 72kbps 是错误答案”
- **一个信道每 1/8s 采样一次，传输信号共有 16 中变化状态，最大数据传输速率是**
   - 8Baud * log_2(16) bit/symbol = 32bps
- ![image.png](./assets/1634992025084-468c56f5-631e-4081-9793-67aab69b0177.png)
:::


#### 4 数据链路层的一些题目
![image.png](./assets/1636884401345-bbc6b202-c5ea-4756-9216-53680d54297d.png)
![image.png](./assets/1636884419967-b3522a81-e3a5-44aa-8acd-f17aea9c2786.png)
![image.png](./assets/1636884432129-dd15231a-78cb-44c5-8f38-cd518f743142.png)
 # Protocol 5 is go-back-n protocol; Protocol 6 is selective repeat protocol.
![image.png](./assets/1636884475191-fac37e58-0fe6-4e0d-92e3-252b8c56625d.png)
![image.png](./assets/1636884490533-46755443-71cb-4352-8b60-80c8c78edd32.png)


#### E 实验相关

- PC 和 Router 算一种设备，Switch, Hub, Bridge 算另一种设备：同种设备之间用直通线 Straight Cable，不同设备之间用交叉线 Cross Cable


### 进度

- 10.6 开始~基带传输
- 10.7 通带传输
- 10.8 物理层（基本）结束
- 10.9 链路层开始~纠错检错
- 10.10 流量控制
- 10.11 ~ALOHA
- 10.12 广播信道分配结束
- 10.13~10.22 体验新版本原神和炉石
- 10.23 物理层做做题
- 10.24~11.1 原神激情跑图
- 11.2 更新了以太网和网桥，还差 WLAN 和 VLAN 看了但是后面再整理
- 11.19 终于搞完了链路层
- 11.29 网路层差不多了
- 12.2 传输层弄完了
- 12.3 应用层弄完了
- 12.4 网络层补完了！完结撒花！




