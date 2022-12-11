

### 交换机 CLI

- `?` 查看可用指令
- Translating "XXXX"...domain server (255.255.255.255) 可以用 `Shift+Ctrl+6` 终止
- `enable` 进入特权模式
- `show version` 查看型号信息；不行的话就 `do show version`
- `dir flash` 或者 `show flash` 查看当前文件系统的内容
- `show vlan` 查看 VLAN
   - `show vlan br` 查看精简信息
- `configure terminal` 进入全局配置模式
   - 在该模式下使用 `interface FastEthernet 0/1` 进行该端口的配置
      - 在配置情况下用 `shutdown` 可以关闭端口，用 `no shutdown` 打开
      - ![intConfig.png](./assets/1637257803615-4e5d166d-d2fd-42fb-a4d8-f643251d31bc.png)
      - `do show interface fa0/1` 查看端口状态
   - 用 `interface vlan 1` 进入 VLAN 1 的配置
      - `ip address 192.168.0.11 255.255.255.0` 实现对 VLAN 1 配置 IP 地址；同时即是给交换机配置管理 IP 地址
   - 用 `line vty 0 4` 打开虚拟终端；`0 4` 表示支持 0 ~ 4 这 5 个端口
      - `login` 允许远程登录
      - `password ***` 设置登录密码
      - 这样相连的计算机连接在支持的端口上时就可以用 `telnet` 连接交换机进行管理了
   - 用 `vlan 2` 进入 VLAN 2 的配置，然后用 `interface Fa0/3` 进入 Fa0/3 端口的配置，然后用 `switchport access vlan 2` 可以将该端口加入 VLAN 2。
- 查看交换机的运行配置 `show running-config`。



### PC Command Prompt

- 配置 IP 地址：`ipconfig 192.168.0.10 255.255.255.0 192.168.0.1`
   - 然后写 `no shutdown`
- 查看 IP 地址：`ipconfig` 



### Others

#### Sniffer
[https://www.youtube.com/watch?v=gsCSKQAVT2M](https://www.youtube.com/watch?v=gsCSKQAVT2M)

- 在 PC1 和交换机之间连接 Sniffer，在另外2台（PC2、PC3）上互相持续的 Ping，观察在 PC1 上是否能抓取到 PC2 和 PC3 发出的 ARP 广播包以及 ICMP 响应包。如果不能抓取到 PC2、PC3 发送的 ARP 广播包，在 PC2、PC3 上先运行“arp –d *”删除所有主机的 ARP 缓存。正常情况下，ICMP 响应包是不能被抓取到的。
- 选择一个交换机端口配置为镜像端口（命令：monitor session 1 destination interface 端口），将 PC1的网线切换到该端口，将 PC2 和 PC3 所连端口配置为被镜像端口（命令：monitor session 1 source interface 端口）。此时 Sniffer 能抓取到 PC2 和 PC3 的 ICMP 响应包。
- 关闭 PC1 端口的镜像功能（命令：no monitor session 1 destination interface 端口)，否则该端口不能正常收发数据。


#### 查看 MAC 地址
![ptMAC.png](./assets/1637258299813-585716be-24ee-4637-a467-6404bf655198.png)


#### Trunk
See Lab4 T15


#### Spanning Tree
See Lab4 T17


#### Router

- 查看路由表 `show ip route`


neighbor
