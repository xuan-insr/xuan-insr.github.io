感谢肥肥和高宝的笔记QWQ 部分内容直接取自其中）<br />若无特殊说明，本文内容和图片均来源于课件。

# 1 Intro

## Info
course website: [https://list.zju.edu.cn/kaibu/netsec2022/](https://list.zju.edu.cn/kaibu/netsec2022/)

10% Performance (Assignments + _possible_ Quizzes)
40% Lab * 3 (10% / 2 Weeks + 10% / 2 Weeks + 20% / 3 Weeks) _OR_ Project<br />50% Final (A4 cheat sheet)


## Reference

- Courses
   - [Computer and Network Security](https://courses.csail.mit.edu/6.857/2018/)
   - [Network Security](http://users.ece.cmu.edu/~vsekar/Teaching/Spring18/18731/)
   - [Computer Systems Security](https://www.youtube.com/watch?v=GqmQg-cszw4&list=PLUl4u3cNGP62K2DjQLRxDNRi0z2IRWnNh/)
   - [Computer Security](http://www-inst.cs.berkeley.edu/~cs161/sp18/)
- Book
   - [Security Engineering](https://www.cl.cam.ac.uk/~rja14/book.html)


### The CIA Triad
Three Common properties to protect is: confidentiality, integrity, and availability

- Confidentiality | 保密性 (not leaked to unauthorized parties)
- Integrity | 完整性 (not modified)
- Availability | 可用性 (keep online, available when needed)

Reading

- The Security Mindset by Bruce Schneier [[video](https://www.youtube.com/watch?v=eZNzMKS7zjo)] [[text1](https://www.schneier.com/blog/archives/2008/03/the_security_mi_1.html)] [[text2](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7404197)]
- [The Internet: Cybersecurity & Crime](https://www.youtube.com/watch?v=AuYNXgO_f3Y) by Parisa Tabriz and Jenny Martin


# 2 DDos Attack & Defence

## 2.1 DoS - Denial of Service

   - 控制一个机器，向 victim 发送海量 request 以 overload 它，从而使其没有能力满足一些合理的请求
   - flood / overload
   - defence: block the attacking device
   - 每层都能 DoS

## 2.2 DDoS - Distruibuted DoS

   - 弄好多个机器，就很难 block 了

### 2.2.1 Symmetric DDoS Attack

#### 2.2.1.1 Ping Flood

- ICMP Echo
- Echo request & response consume bandwidth
- 消耗其响应能力 或者 网络带宽
- 解决：禁用 ICMP (ping / tracert / etc.)

#### 2.2.1.2 TCP SYN Flood

- 发 SYN 后 server 会分配资源并加入 SYN queue / SYN backlog 中，而这个队列的容量是比较小的（一般只有 128）
- 如果扔掉 server 发来的 SYN + ACK，那么 server 就会将资源一直维持直到超过时限（一般 3 分钟）；在这一段时间内 server 就无法服务新的 client
- 优化：IP Spoofing，即发送的 SYN 携带的是随机的 IP 地址而不是 attacker 的 IP 地址，这样可以减小攻击者的带宽压力；亲测这样不会发回 RST（看下面的图）

![URNRW3OQ)JUM3C~V]POA3YB.jpg](./assets/1648607419542-89792870-d8d5-4c21-be9d-c1b079bf0f73.jpeg)
![P8`48`G[[IGP6G_MLMFDUNW.png](./assets/1648607425146-0e9bfc27-5233-449d-b5cd-1828ed5c28bf.png)

- 解决：SYN Cookies
   - server 接受到 SYN 之后并不是直接发回内容，而是根据该数据包以及一些其他信息构造一个 SYN Cookies 作为 SYN + ACK 中的 seq；收到 ACK 时再检查内容，合法才分配资源
- TCP SYN Flood Backscatter：指 server 接收到 Spoofed IP 的 SYN 后发回的 SYN + ACK
   - 可以用来检测 DDoS 攻击


### 2.2.2 Asymmetric DDoS Attack (Traffic Flood)

- 用较少的资源造成较大规模的攻击

#### 2.2.2.1 Smurf Attack
将一个 Echo Request 广播到一个子网去，这个 request 的 IP 被 spoof 成 victim；这个子网的每个 host 都会给 victim 发回一个 reply。<br />解决：禁用子网的 broadcast，或者拒绝外来的 broadcast packet。
![image.png](./assets/1648622693186-c287a5c0-de23-43a4-9987-038a1141ba73.png)


#### 2.2.2.2 DNS Amplification Attack
利用 open DNS resolvers，即互联网公开、大家都可以访问的 DNS resolver；利用 DNS 请求的 `ANY` 类型，可以获取给定名字的所有类型的信息；同样使用 spoofed IP。<br />解决：减少 open resolver 的数量，或者认证 src IP，防止 spoofed packet 离开子网（这需要 ISP 来做）。
![image.png](./assets/1648654805137-1959a70f-fc2f-49c2-bdf7-0df6165f4d72.png)


#### 2.2.2.3 NTP Amplification Attack
NTP (Network Time Protocol) 的 `monlist` 指令可以获取当前活跃 IP 信息。借此可以实现 DDoS。<br />解决：减少支持 `monlist` 的 NTP Server，或者认证 src IP，防止 spoofed packet 离开子网。
![image.png](./assets/1648657633184-91daed54-683b-4d6d-84db-1bdc01eb9952.png)


#### 2.2.2.4 Memcached Attack
 Memcached servers 提供通用的缓存服务以提高网站访问速率。Memcached 服务使用 UDP，因此发送前并不需要握手（前面几个也一样）。攻击者预先加载一些信息，然后伪装成 victim 向 server 请求。<br />解决：禁用 UDP 或者屏蔽 Memcached server 或者认证 IP 或者对 Memcached server 发送 `flush_all` 命令。
![image.png](./assets/1648657792742-339732c6-55e3-47a4-9167-cfd4d3c21cec.png)


#### 2.2.2.5 SSDP Attack
Simple Service Discovery Protocol 简单服务发现协议 是 Universal Plug and Play (UPnP) 即插即用设备技术的基础，大意是即插即用设备会维护一个列表。<br />攻击者伪造成 victim 的地址，发送 `ssdp:rootdevice`和 `ssdp:all` 等请求以获得全部设备列表。<br />解决：关闭 UDP 端口 1900。
![image.png](./assets/1648658660664-cabcde08-5258-4869-ba44-0f35d335250b.png)


### 2.2.3 Asymmetric DDoS Attack (Computation)

- 用较低的开销消耗 victim 的大量算力

#### 2.2.3.1 HTTP Flood


#### 2.2.3.2 Fragmented HTTP Flood


#### 2.2.3.3 Payment DDoS


### 2.2.4 Asymmetric DDoS Attack (Others)

#### 2.2.4.1 Tail Attack


#### 2.2.4.2 SDN CrossPath Attack


## 2.3 DDoS Defences
第一个思路是让攻击者的攻击更困难（1~3）<br />第二个思路是消耗攻击者的更多资源（4~5）


### 2.3.1 Ingress Filtering
要求 ISP 只传输合法 src IP 的包。问题是：这种方式需要所有 ISP 都使用，但是他们没有理由要用。<br />只有 src AS 能检查，中间的都很难检查……


### 2.3.2 Traceback
……除非给包里新增一些内容

- 最简单的方式是在 packet 里维护路径信息
   - 但是太大了
- 可以通过 Edge Sampling
   - 基于路由器可信、包足够多且路径一致的假设
   - ![image.png](./assets/1648727331665-1c2af20f-ce73-4417-9e7e-34c6a727c151.png)
   - ![image.png](./assets/1648727358949-4a106deb-837e-4594-bc2f-3d131aa49bff.png)
   - ![image.png](./assets/1648727377440-7f49ea94-eed7-4f83-8d8e-a7715338f702.png)
   - ![image.png](./assets/1648727401540-91e98420-216c-4515-8ccd-37749f70ee8b.png)
   - 由于包足够多，因此根据不同包的采样就可以还原出路径。
   - 但是如果有恶意的中间路由器……
      - 增加一些密码学手段做校验 (Path Validation)


### 2.3.3 Alibi Routing
证明一个 packet **没有** 经过某个 AS

- 引入 proof waypoint 使得 packet 在给定时间内不可能同时经过 proof waypoint 和需要避开的 AS


### 2.3.4 Client Puzzles
让 client 算个题。
![image.png](./assets/1648727881865-1669091e-ccfc-4e0f-9462-c15259083cd1.png)
（n 可以根据流量情况修改）<br />坏处：需要修改协议；对垃圾设备不友好，尤其是 n 较大时


### 2.3.5 CAPTCHA
Completely Automated Public Turing test to tell Computers and Humans Apart<br />就是验证码


# 3 Secure Routing

## 3.1 Routing Attacks

- Distance-Vector
   - ![](./assets/1637714738195-5eed0d30-6a45-4902-bcca-8c55d2683d7e.png)
   - announce 0 distance to all other nodes
- Link-State
   - ![](./assets/1637722042082-b2bf5f2d-46e8-452f-9f01-2345333980ed.png)
   - drop links（不想要的）OR claim direct link to other routers
- BGP
   - 类似 Vector Routing；AS 的 border routers 扮演 routers，AS 的 prefix 扮演 IP
   - ![image.png](./assets/1648839195631-774264f4-9219-4ac9-984e-e047d1191ac9.png)
   - announce arbitrary prefix; alter paths


### 3.1.1 Prefix Hijacking

1. 说自己是某个 prefix
   - ![image.png](./assets/1648877178950-f5bef201-f8d5-472c-ba6d-5ed8e4d24090.png)
2. 或者说自己离得近
   - ![image.png](./assets/1648877186557-8193c57e-8f33-467f-8eb8-6516cf2d4f8a.png)


### 3.1.2 Path Tampering
![image.png](./assets/1648877256712-3b163394-7404-4d58-b1f3-f3475f9a9204.png)


## 3.2 Secure Routing

### 3.2.1 RPKI | Resource Public Key Infrastructure
![image.png](./assets/1648886948197-09842659-a042-4292-83df-7376551fb4fb.png)
问题：3.1.1.2 防不住
![image.png](./assets/1648887016051-fe10c6f9-ec6a-48d2-a1e9-1dfea110d801.png)

### 3.2.2 Secure BGP

- Each AS on the path cryptographically signs its announcement
   - Guarantees that each AS on the path made the announcement in the path.
   - Address attestations
      - Claim the right to originate a prefix
      - Signed and distributed out-of-band
      - Checked through delegation chain from ICANN
   - Route attestations
      - Distributed as an attribute in BGP update message
      - Signed by each AS as route traverses the network
      - Signature signs previously attached signatures
   - S-BGP can validate
      - AS path indicates the order ASes were traversed
      - No intermediate ASes were added or removed 
- Deployment challenges
   - Complete, accurate registries
      - E.g., of prefix ownership
   - Public Key Infrastructure
      - To know the public key for any given AS
   - Cryptographic operations
      - E.g., digital signatures on BGP messages
   - Need to perform operations quickly
      - To avoid delaying response to routing changes
   - Difficulty of incremental deployment
      - Hard to have a "flag day" to deploy S-BGP

# 4 Anonymous Communication

## 4.1 Overlay Communication
Packet 里至少包含 IP 信息。<br />Why wanted？匿名访问医疗、选举等信息；以及攻击者匿名访问非法信息。

通过加密（比如 HTTPS）可以保护访问的内容；但是访问行为本身也可以泄露很多信息。<br />因此，应当隐藏目的 IP 信息；但是总需要以某种方式送过去。可以 relay：
![image.png](./assets/1648888241815-61c8ff89-dae0-41aa-908a-7ed8cb4aa47c.png)
![image.png](./assets/1648888346471-32d46649-eba8-4287-b76e-c7b4b26b9a5f.png)


### 4.1.1 Threat Model
下面我们要考虑这种 relay 的风险。<br />考虑风险时，我们需要定义攻击者的行为模式：Insider Byzantine Attacker.<br />**Insider** 表示攻击者本身是网络的组成部分（ASes），而且攻击者可能控制着不止一个 ASes，但是攻击者并没有能力看到网络的全貌；<br />**Byzantine** 是一种攻击模式，表示攻击者的攻击方式是不稳定的。长期、一致的攻击会容易被发现，因此攻击者采取间断式的、不同方式的攻击，就比较难被检测到了。

攻击者的目标是在目的 IP 信息隐藏在数据包中的情况下，得知数据包的最终目的地。


### 4.1.2 Traceforward Attack
![image.png](./assets/1648888681595-d12fe86b-08cf-4e1c-b8df-cdc60e5f2111.png)
攻击者跟踪数据信息


### 4.1.3 Marking Attack
![image.png](./assets/1648888704089-c6c87d35-bdc8-48a3-b81b-79589c8d59c1.png)
攻击者比较厉害，可以改数据包（比如数据包经过他了），那可以加个标记，然后在其他地方发现就知道是发过来了


## 4.2 Anonymizing Proxy
![image.png](./assets/1649905980378-ec5de13d-e113-460f-b4b1-d82c29909a27.png)
如果攻击者在 sender 和 proxy 之间，攻击者丧失匿名性；如果在 proxy 和 receiver 之间，receiver 丧失匿名性；如果两个攻击者串通对比 ingress 和 egress 代理流量，则匿名性失效；如果 proxy 本身是 attacker，匿名性同样失效。


### 4.2.1 Receiver as Attacker
![image.png](./assets/1649906173439-798f8f3d-f352-4a52-9aed-632a773f31e1.png)
保护发送者的匿名性


### 4.2.2 Advantages & Disadvantages

- **Advantages**
   - easy to configure
   - receiver need not to be aware of anonymity service
   - have been widely deployed on Internet
- **Disadvantages**
   - trusted third party needed
   - proxy may release / sell logs or blackmail (敲诈) senders
   - anonymity largely depends on the locations of the attacker, which is likely unknown


### 4.2.3 How to evade (逃避) attackers?
Dynamize proxy location<br />**Crowds Algorithm**<br />人海战术，每个结点叫做一个 Jondo<br />算法是：首先将信息发给一个 random jondo，每个 jondo 以![](https://cdn.nlark.com/yuque/__latex/d4cd21d60552e207f237e82def9029b6.svg#card=math&code=p&id=LD9UM)的概率发给另一个随机 jondo，以![](https://cdn.nlark.com/yuque/__latex/661fd2266df4a104d2665deebdbaeea5.svg#card=math&code=1-p&id=L8i4X)的概率发给终点。
![image.png](./assets/1649906736895-3f8280d9-292e-4706-82f8-8f55f542645e.png)
问题是：必须信任 proxy；任何一个 proxy 是恶意的都会暴露 receiver


### 4.2.4 How to evade untrusted proxies?

- 弄多一些 proxies，这样攻击者控制的概率就小了


#### 4.2.4.1 Source Routing
Source Routing / Path Addressing 允许发送者指定一个包的部分或者全部路由


#### 4.2.4.2 POF-Based Source Routing
POF - Protocol Oblivious Forwarding
![image.png](./assets/1649907788395-1ba938e4-6c44-4536-81f1-903a28481013.png)
匿名性问题：泄露了 port sequence<br />如何解决：隐藏非 neighbors 的 port sequence


## 4.3 Onion Routing
source-routing based anonymous overlay communication

1. 向 directory node 获取结点列表，并随机选择一些结点形成 chain (or circuit)
2. 从 directory node 获取一个公钥，借此与 A 协商密钥；经过 A 与 B 协商密钥；经过 B 与 C 协商密钥，直到建立起整条链
3. 发送 {{{{msg}D,D}C,C}B,B}A ，这样逐层解密最终给 D 发送 D 才能解密的 msg
4. 发回来的时候用同一条反向链接即可

![image.png](./assets/1649909150251-8743917d-d59f-4099-8e40-555d9e20428f.png)
可以只用三个，更多没啥用了，而且慢；两个的话万一他们属于一个人就寄了；三个的话可能性低一点，差不多够了


### 4.3.1 How to de-anonymization?
如果 tor nodes collude with each other 就寄了<br />或者算力足够破解密码

或者，被动监测 / 主动部署 Tor 结点，进行流量分析和关联

如何分析？后面再说

#### 4.3.1.1 Path Selection Attack
Tor 选择结点时是有权重的，权重和 bandwidth 有关。<br />恶意结点报告一个高 bandwidth，从而可以拥有更大的权重；<br />如果它作为 entry node，则可以知道 sender；作为 exit node，则可以知道 receiver


#### 4.3.1.2 Counting Attack
 通过计算数据包的数量来关联流入和流出的流 <br />![](./assets/1649938841468-3605b5fd-9c19-4263-ba28-3cf77e0a3064.png)


#### 4.3.1.3 Low Latency Attack
Tor 路由器为每个匿名电路分配自己的队列，以循环方式从每个队列中取出一个包。<br />新队列会影响所有其他队列的延迟，基于此对队列中的包进行推测。<br />假设只有 Init 和 A 在占用 T2，A 循环给 T2 发包并测试延迟，当延迟变大，意味着有 Init Traffic。
![image.png](./assets/1649951614036-c35d6afb-d229-419d-be38-ecfd5819234c.png)


#### 4.3.1.4 Cross Site Attack
Crawling:<br />攻击者部署 Tor routers，访问 darknet，抓取 transaction 信息，并从中提取有价值的 Bitcoin 账户等<br />Correlation:<br />在公开网络上搜索这些账户


# 5 Web Security

## 5.1 Goals

- Integrity | 完整性
   - 恶意网站不应能够修改计算机，或者其他网站上的信息
- Confidentiality | 保密性
   - 恶意网站不应能够得知计算机或者其它网站上的机密信息
- Privacy | 隐私性
   - 恶意网站不应能够窥探我的在线活动
- Availability | 可用性
   - 攻击者不应能够使得网站不可用


## 5.2 Web Security: Server Side

- 可能遇到的问题
   - 窃取敏感信息
   - 修改用户信息
   - 攻击者可以服务器网关攻击用户
   - 冒充用户
   - 注入攻击
      - 攻击者使用恶意的输入
      - 服务器没有检查输入的格式
      - 于是攻击者可以执行任意代码


### 5.2.1 SQL Injection
`ok = execute( SELECT * FROM Users  WHERE user= ' ' ; DROP TABLE Users -- … )`


#### 5.2.1.1 Solution: Input Sanitization
检查或者通过操作使得用户输入的字符串不存在指令

   - 拒绝一些特殊的字符；或者
   - 对输入进行转义
      - 在一些如引号之类的特殊字符之前加 `\`；取决于不同的 SQL 解析器


#### 5.2.1.2 Solution: Prepared Statement
SQL 注入攻击的主要原因是数据和代码混在了一起。因此我们可以考虑将代码和数据分开。<br />Prepared Statement 的本意是优化一些常用的计算：它允许用户给数据库发送一种语句模板，其中的参数可能尚未绑定。数据库进行解析、编译、优化，但尚不执行，直到用	户将参数绑定上去再计算。<br />但是，这种方式也可以用来防止 SQL 注入攻击，因为此时数据库非常明确地了解代码和数据之间的界限，通过后面的绑定传入的参数并不会被解析。
![image.png](./assets/1649395728841-979f70a7-7c5d-4dde-bed7-8988709e025b.png)



## 5.3 Web Security: Client Side

### 5.3.1 Same-Origin Policy
防止恶意网站监视/篡改用户信息或与其他网站的交互<br />浏览器强制进行。浏览器中不同站点相互隔离，同一站点的不同页面不隔离
![image.png](./assets/1649431353162-32d78079-700b-4896-a2c9-a920db6bfb84.png)
一个 origin 不能访问另一个 origin 的资源
![image.png](./assets/1649431379497-46211651-c6e3-4ae2-88d1-ec53fb3bd87f.png)
http 80, https 443


### 5.3.2 Cookie
如果现在有能对应的 cookie 就带上；如果没有的话服务器会返回一个 `Set-Cookie: `
![image.png](./assets/1649496527051-6cf5a885-8c6d-4e3f-9ab4-a68632818109.png)
![image.png](./assets/1649496536473-d4858d4b-4d9d-4a1a-b1f1-8da753580630.png)


### 5.3.3 Session Token
![image.png](./assets/1649496794228-eb948c0d-150b-48ee-95bc-1f223a06171c.png)
一个 HTTP Session 是一系列请求-响应 transactions。<br />服务器在用户登入后会给其分配一个 session token，作为当前 session 的唯一 identifier，以 cookie 的形式呈现。服务器维护用户和 session token 的表，因此看到 session token 即知道是哪个用户。


### 5.3.4 Cross-Site Request Forgery | CSRF
![image.png](./assets/1649497018509-cb7316cb-42e6-43c7-8a60-42738d26c880.png)
See also [CSRF | NetSec Lab3](https://www.yuque.com/xianyuxuan/coding/netsec_lab3#f7nTS).


#### 5.3.4.1 Defenses: Referer Validation
HTTP header 中的 `Referer` 字段显示发起这个 request 的 URL
![image.png](./assets/1649497143428-a9671319-e152-4566-aeac-d38fbb289336.png)


#### 5.3.4.2 Defenses: CSRF Token
CSRF 攻击的攻击者并不能获取到 cookie，而只是冒用之。因此服务器可以生成一个唯一的、秘密的、不可预测的 token，以 cookie 以外的方式发给 client，client 在提交请求的时候会附带这些信息；如果没有这些信息则认为是非法的。<br />对于 GET 请求，可以放在 URL 里，这可以通过 server 在返回 html 之前将其中所有 <a> 或 <href> 的链接后面加上 `ctrftoken=value` 这种东西；对于 POST 请求，server 可以在表单里加一个 hidden 的 <input>，将 token value 写进去。


### 5.3.5 Cross-Site Scripting | XSS
用户输入包含脚本，网站如果试图显示这些输入而缺乏适当处理，则会被当做脚本执行。<br />可以用来盗取 Cookie 等。<br />核心仍然是之前所说的 Same-Origin Policy

#### 5.3.5.1 Stored XSS | 存储型跨站脚本攻击
脚本会持久地放在数据库里，例如留言板等


#### 5.3.5.2 Reflected XSS | 反射型跨站脚本攻击
攻击者把脚本通过 URL 的方式发给服务器（可以发给 victim 让他访问这个 URL），而服务器如果试图不加处理地显示输入（例如搜索结果等），就会使得访问者运行相应的脚本


#### 5.3.5.3 Defenses: Input Validation 
规定输入的合法格式等


#### 5.3.5.4 Defenses: Output Escaping
![image.png](./assets/1649500181099-7faa20bf-6d56-4474-a8d2-aafbc3a375d9.png)


#### 5.3.5.5 Defenses: Content Security Policy | CSP
Content-Security-Policy 这个 HTTP header 允许 response 指定白名单，指示浏览器仅执行或呈现来自这些来源的资源。<br />例如 `Content-Security-Policy: script-src 'self'; object-src 'none'; style-src cdn.example.org third-party.org; child-src https:`指示了：

   - 脚本：只信任当前域名
   - <object> 标签：不信任任何URL，即不加载任何资源
   - 样式表：只信任 cdn.example.org 和 third-party.org
   - 框架（frame）：必须使用HTTPS协议加载
   - 其他资源：没有限制

(ref: [http://www.ruanyifeng.com/blog/2016/09/csp.html](http://www.ruanyifeng.com/blog/2016/09/csp.html))


# 6 Email Security

## 6.1 Email Architecture
![image.png](./assets/1649743888122-e1aa1389-6a60-4711-95f3-6f9c75e96553.png)

## 6.2 Email Security Threats

- **Authentication-related Threats**
   - 未认证的访问	unauthorised access to email systems 
- **Integrity-related Threats**
   - 非法修改		unauthorized modification of email contents 
- **Confidential-related Threats**
   - 信息泄露		unauthorized disclosure of sensitive information 
- **Availability-related Threats**
   - 无法正常使用	block users from sending and receiving emails  


## 6.3 S/MIME
Secure / Multipurpose Internet Mail Extension 

- Authentication | 认证
- Confidentiality | 保密
- Compression | 压缩 
- Email compatibility | 兼容


### 6.3.1 Authentication

1. 发送方创建消息
2. 使用 SHA-256 生成 256 位的消息摘要
3. 使用发送方的私钥用 RSA 加密消息摘要，将结果和签名者的身份追加到消息中
4. 接收方使用 RSA 和发送方的公钥对消息摘要进行解密、恢复和验证


### 6.3.2 Confidentiality

1. 发送方创建一条消息和一个 128 位的随机数字，作为此消息的内容加密密钥（Content-Encryption Key）
2. 使用内容加密密钥加密消息
3. 使用接收方的公钥对内容加密密钥进行 RSA 加密，并将其附加到消息中
4. 接收方使用 RSA 及其私钥对内容加密密钥进行解密和恢复
5. 使用内容加密密钥解密消息


### 6.3.3 Content Type
Data - 内部 MIME 编码的消息内容，可以封装在以下类型：

- SignedData - 信息的数字签名
- EnvelopedData - 任何类型的加密数据，以及一个或多个收件人的加密内容加密密钥
- CompressedData - 信息的压缩


## 6.4 PGP
**Pretty Good Privacy** - 和 S/MIME 一样的功能，对个人使用免费且流行<br />**与 S/MIME 的区别：**

- Key Certification 
   - S/MIME 使用由 CA 或授权机构颁发的 X.509 证书
   - OpenPGP 允许用户生成他们自己的 OpenPGP 公钥和私钥，然后从已知的个人或组织征求对他们的公钥的签名
- Key Distribution 
   - OpenPGP 不在每条消息中包含发送者的公钥
   - 接收方需要从受 TLS 保护的网站或 OpenPGP 公钥服务器来获取
   - OpenPGP 密钥没有审查，用户自己决定是否信任

NIST 800-177 建议使用 S/MIME 而不是 PGP，因为在验证公钥的 CA 系统中更有信心。


## 6.5 DANE
CA 也很危险诶，万一 CA 被破坏了就寄了

DANE 的目的是用 DNSSEC 提供的安全性取代对 CA 系统安全性的依赖。<br />鉴于域名的 DNS 管理员有权提供有关该区域的身份信息，所以也可以让管理员在 域名 和 该域名上的主机可能使用的证书 之间进行认证和绑定。<br />即，DANE 是 DNS-based Authentication of Named Entities，基于 DNS 的对有域名实体的认证。使用 DNSSEC 将 X.509 证书绑定到 DNS 域名。


### 6.5.1 TLSA Record
TLS Authentication Record

- 一个由 DANE 定义的新的 DNS 记录类型，用于 SSL/TLS 证书的安全认证方式
- 指定 CA 可以为证书提供担保的约束条件，或指定特定的 PKIX [Public Key Infrastructure (X.509)] end-entity 证书有效的约束条件。Specify constraints on which CA can vouch for a certificate, or which specific PKIX [Public Key Infrastructure (X.509)] end-entity certificate is valid. 
- 指定可以直接在 DNS 中认证的 service certificate 或者 CA。Specify that a service certificate or a CA can be directly authenticated in the DNS itself.


### 6.5.2 DANE for SMTP


### 6.5.3 DANE for S/MIME


### 6.5.4 SPF	
隔壁班没讲<br />ADMDs (Administrative Management Domains) publish SPF records in DNS specifying which hosts/IP-addresses are permitted to use their names<br />receivers use the published SPF records to test the authorization of sending Mail Transfer Agents (MTAs) using a given "HELO" or "MAIL FROM" identity during a mail transaction;


### 6.5.5 DKIM

- sign email message by a private key of the administrative domain from which the email originates;
- at the receiving end, the MDA can access the corresponding public key via a DNS and verify the signature, thus authenticating that the message comes from the claimed administrative domain 


## **6.6 What if Email is exploited?**

### Spam

### Phishing

### Malware


# 7 Traffic Analysis
filter malicious traffic

## 7.1 Firewall
一个 barrier，双向流量都需要通过，分别用 firewall security policy 指定两方向有什么流量可以通过。<br />**目标**：

- 所有从内部到外部的流量都必须通过防火墙，反之亦然。
- 只有 local security policy 定义的授权流量才被允许通过。
- 防火墙本身是不受渗透的。


### 7.1.1 Design Techniques

- Service Control - 确定可访问的服务类型（入站或出站） 
   - 根据 IP 地址、协议或端口号对流量进行过滤
   - 提供代理软件，在传递服务请求之前接收并解释每个服务请求
   - 托管服务器软件本身，例如 Web 或电子邮件服务
- Direction Control - 确定特定服务请求被允许发起和通过防火墙的方向
- User Control - 根据试图访问服务的用户来控制对服务的访问 
   - 一般适用于本地用户
   - 也适用于外部用户通过安全认证技术（如 IPsec 认证头）
- Behavior Control - 控制特定服务的使用方式 
   - 例如，过滤电子邮件以消除垃圾邮件，或允许外部访问本地 Web 服务器上的部分信息


### 7.1.2 Types of Firewalls

#### 7.1.2.1 Packet Filtering Firewall
对每个传入和传出的 IP 数据包应用一组规则，转发或丢弃报文

- 在单个数据包的基础上做出过滤决策
- 不考虑更高层次的上下文
- 如果没有匹配，则默认丢弃，或者默认转发

（实际上按照图片，应该是对传输层 segment 进行过滤；会考虑双方的 IP, port 以及包中的 Flags，如 ACK）


#### 7.1.2.2 Stateful Inspection Firewall
数据包和它们的上下文都由防火墙检查，也是传输层的


#### 7.1.2.3 Application Proxy Firewall
作为一个应用层的 relay，使得客户端和服务端从不直接交互，而是以防火墙作为代理，同时可以检查数据包的全部内容


#### 7.1.2.4 Circuit-Level Proxy Firewall
作为一个 transport layer 的 relay，代理主机和对方完成 TCP 连接建立；一旦建立连接后就正常转发，不检查内部内容。


### 7.1.3 Where Firewall Stand

#### 7.1.3.1 DMZ networks
DMZ - DeMilitarized Zone 停火区<br />**External Firewall**

- 为 DMZ 系统提供与外部连接需求一致的访问控制和保护

**Internal Firewall**

- 增加更严格的过滤能力，保护内部网络免受来自 DMZ 的攻击，反之亦然；保护内部网络之间的安全。

![](./assets/1649982001368-fbbfe468-9b55-46a0-960f-0ad2b93457c9.png)


#### 7.1.3.2 Virtual Private Networks
在较低的协议层使用加密和身份验证，通过不安全的 Internet 提供安全连接

- 比使用专用线路的专用网络便宜
- 常用协议： IPsec

![image.png](./assets/1649982092654-65c35eb3-de8a-46b8-ab1d-d57092c7642c.png)


#### 7.1.3.3 Distributed Firewalls
独立防火墙设备和基于主机的防火墙在中央管理控制下协同工作
![image.png](./assets/1649982133764-50ee8876-6f77-49dd-bb04-0dddd2c2da31.png)


## 7.2 IDS | Intrusion Detection System
individually secure packets yet collaboratively malicious (e.g. TCP SYN Flood)

检测异常的活动模式或与已知入侵相关的活动模式，提供入侵的早期预警，以便采取防御行动。（只报告不过滤）


### 7.2.1 Intrusion Behavior Pattern
入侵者的行为与合法用户的不同之处是可以量化的：
![image.png](./assets/1649982410042-b8053b52-1409-431a-8718-95b10268c65e.png)


### 7.2.2 How to Detect Intrusion

#### 7.2.2.1 Audit Record

- 记录用户正在进行的活动
- 向 IDS 输入记录
- Native Audit Record 
   - 使用操作系统内可用的审计软件收集用户活动信息
   - 不需要额外的收集软件
   - 可能不包含所需的信息或可能不以方便的形式包含信息
- Detection-Specific Audit Record 
   - 使用专用工具生成只包含 IDS 所需信息的审计记录
   - 独立、便携
   - 额外的开销
- Example fields - Subject, Action, Object, Exception Condition, Resource-Usage, Time-Stamp


#### 7.2.2.2 **Statistical Anomaly Detection**

- Threshold Detection - 在一段时间内，统计特定事件类型的发生次数，如果超过合理数量，则报告入侵
- Profile-Based Detection - 描述一些用户的过去行为，如果发生重大偏差，报告入侵


#### 7.2.2.3 **Rule-Based Detection**

- 通过观察系统中的事件并应用一组规则来检测入侵，这些规则可以决定给定的活动模式是否可疑
- 分析历史审计记录，以识别使用模式并生成描述这些模式的规则


### 7.2.3 Distributed IDS 

- 在需要监控的系统上作为后台进程运行；这些系统分别收集安全相关事件的数据，并传输给中央管理员
- 有一个叫 LAN monitor 的东西，operate the same as host agent module except that it analyzes LAN traffic and reports to central manager
- 中央管理员处理来自 LAN monitor 和 host agents 的报告，处理并关联它们从而报告入侵

![image.png](./assets/1649982871880-b9d29885-a5ac-4526-9ddc-6cbe7322ebb5.png)



### 7.2.4 Honeypot

- 诱饵系统，旨在引诱潜在的攻击者远离关键系统
- 收集关于攻击者活动的信息
- 鼓励攻击者在系统上停留足够长的时间，以便管理员作出响应

![image.png](./assets/1649982949877-04144a6a-35db-44ca-8e3f-bd936493e155.png)


### 7.2.5 Honeywords

- 将假密码（Honeywords）与每个用户的帐户关联
- 窃取（哈希）密码文件的攻击者无法区分密码和 Honeywords
- 尝试使用 Honeywords 登录会引发警报

![image.png](./assets/1649986474475-ad35b623-7304-4c1e-89ed-a756a8a17b50.png)


**密码**

- 注册一个新密码：Salt + password -> Hash
- Salt由服务器随机生成，和用户 ID 一起记录在数据库中
- 验证密码 - 通过用户 ID 获取 Salt 然后 hash

**Salt 用途**

- 防止重复密码在密码文件中可见
- 大大增加了离线字典攻击的难度
- 这大大增加了查明一个人是否在两个或多个系统上使用了相同密码的难度。


### 7.2.6 IDS Detection Accuracy
**Detection Rate / True Positive Rate **`**TP**`

- 假设存在入侵，IDS 正确输出警报的可能性有多大
- False Negative Rate `FN = 1 - TP`

**False Alarm / False Positive Rate **`**FP**`

- 假设没有入侵，IDS 错误输出警报的可能性有多大
- True Negative Rate `TN = 1 - FP`


## 7.3 IPS | Intrusion Prevention System

- Host-based, network-based, or distributed

- **Anomaly Detection** | 异常检测 - 识别不同于合法用户的行为
- **Signature/Heuristic Detection** | 特征/启发式检测 - 识别恶意行为


## 7.4 Advanced Traffic Analysis

- 模式识别（时间分布，或者流量分布 | event-based / shape-based），甚至机器学习

但是，恶意用户可能会使用手段隐藏流量模式：

- Traffic Obfuscation | 混淆
   - 加密流量以隐藏有效负载
   - 使用代理隐藏整个数据包
   - 引入噪声流量以隐藏模式
      - 例如，ditto 通过 padding 来混淆数据包大小，通过冗余数据包混淆传输间隔

![image.png](./assets/1649983446349-8778c41d-007d-4d60-8fd0-02c6b354dfdc.png)

咋整捏？

- Active Probing，大意就是主动发一个探测器过去，看看对面反应正不正常


# 8 Attack Traceback
我们识别出了攻击！但是攻击是哪里来的捏

源 IP 地址不可靠，因为有 IP Spoofing 的可能。Ingress filtering 可以解决，但是部署上有困难。


## 8.1 IP Traceback
在 [2.3.2 Traceback](#aQcSf) 讨论过了！


## 8.2 ICMP Traceback
**iTrace**

- 每个路由器对它所转发的包中的一个进行取样（实际上是以一定概率），然后将包的内容和相邻路由器的信息复制到 ICMP Traceback 消息中
- 路由器使用 HMAC 和 X.509 数字证书对回溯消息进行认证
- 路由器向目的地发送 ICMP 回溯消息

一些问题

- 要求所有发送攻击流量的路由器都启用了 iTrace，构建完整的攻击路径
- 然而 ICMP 报文通常被过滤，因为 ICMP Ping Flood 攻击
- 并不是所有数据包都在每一跳上采样


## 8.3 Path Validation


## 8.4 Link Testing
每个包都要进行标记吗？应该总是采样某些包吗？

Only when needed

- 追踪离受害者最近的路由器
- 确定发起攻击流量的上行链路
- 递归地应用前面的技术，直到到达攻击源
- 基于攻击持续进行的假设

具体而言：

### 8.4.1 Input Debugging

- 查找攻击签名，即所有攻击报文所包含的共同特征
- 将攻击签名发送给上游路由器，由上游路由器对攻击包进行过滤，并确定进入端口
- 在上游路由器上递归地应用上述技术，直到到达攻击源

困难：

- 在 ISP 级别上进行通信和协调追溯需要相当大的管理开销

<br />

### 8.4.2 Controlled Flooding

- 需要协作的主机
- 强制主机将 link 泛洪到上游路由器
- 由于受害链路上的缓冲区被所有入站链路共享，导致攻击链路泛洪，使得攻击报文被丢弃
- 在上游路由器上递归地应用上述技术，直到到达攻击源

困难：

- 需要一张精确的拓扑图
- 如果有多个攻击源（如 DDoS），会有高开销


## 8.5 Logging-Based Traceback
post-attack traceback

如果在路由器上记录报文，支持查询，就可以在之后进行回溯

- 路由器存储包日志
- 攻击对象会向最近的路由器查询攻击报文的报文外观
- 含有攻击报文的路由器会递归地查询上游路由器，直至到达攻击源

![image.png](./assets/1649985403051-94c53920-5144-42ba-92db-6bbf08e36b09.png)

记录什么信息呢？

- Raw Packet？路由器上的高存储开销
- Hash of invariant content per packet？在高流量的情况下，存储开销仍然很高

咋整捏？

### 8.5.1 Bloom Filter
每个采样包使用多个哈希值，对采样包中的不变内容进行多次哈希，使用一个 bitmap 保存哈希结果<br />需要检验时，检查是否采样包的所有哈希值都在 bitmap 里<br />不会有 false negative，但是会有 false positive<br />在 m-size bitmap, n members, k hash functions 的情况下，false positive 的概率大约是：
![image.png](./assets/1649985870626-e3b8e36a-d8c0-4487-92f1-2bdce43e092e.png)


### 8.5.2 SPIE System
Source Path Isolation Engine


# 9 Network Protection

## 9.1 Firewall / IDS / IPS
监测 / 过滤恶意流量<br />See [7 Traffic Analysis](#n9aem)

## 9.2 Load Balancing
将网络流量分配给多个 server，以缓解单个 server 的负载以及故障
![image.png](./assets/1650003672221-7ff1dbe2-3d12-4aa9-b6ff-2fc456714b28.png)

- Least Connection Method 
   - 将流量直接发送到当前活动连接最少的 server
- Least Response Time Method 
   - 将流量直接发送到具有最少活动连接和最低平均响应时间的服务器
- Round Robin Method 
   - 按照顺序将流量分给某个 server（这次分给 1 号，下次就分给 2 号）
- IP Hash 
   - 对 IP 做 hash，将 packet 分给 IP hash 出的 server


## 9.3 Traffic Scrubbing
使用数据清理服务，对流量进行分析，过滤恶意流量

此类服务提供者应该配备足够的资源，以承受高容量的 traffic flood

一旦攻击被检测到，那就让这个流量进入 scrubbing service

- 分析并过滤恶意流量
- 将其中包含的合法流量发给 user


## 9.4 User Authentication
The basis for most types of access control and for user accountability<br />识别用户并对用户声称的身份进行验证

**Identification Step**<br />向安全系统提供一个 ID<br />**Verification Step**<br />提供或生成用于验证用户和 ID 之间绑定的身份验证信息

**方式**

- 用户知道的信息
   - password，personal identification number(PIN), 提前准备好的问题的答案
- 用户拥有的信息
   - 电子卡，智能卡，物理密钥
- 用户“是谁”（唯一辨认）
   - 静态生物特征
      - 指纹，视网膜，脸
- 用户的行为
   - 动态生物特征
      - 声音模式、笔迹、打字的节奏


## 9.5 Token
复习 PPT 甚至没有

- 用于用户认证的用户拥有的东西
- e.g. 电子卡，智能卡，生物ID卡


## 9.6 Access Control
Authorize a subject with some access right(s) for some object(s)

- Subject			某个用户 / 进程
   - Owner			creator of a resource, system administrator, project leader, etc.
   - Group			组；一个用户可能属于多个组
   - World			其他
- Object			某种 resource
- Access Right		是否有权限做某种事情


### 9.6.1 DAC
Discretionary Access Control，自由访问控制

- Access Matrix

![](./assets/1650009174305-e739854e-6f60-42ce-800f-c96efddd8a9c.png)

- ACL - Access Control List

![](./assets/1650009188936-1395a6c7-e514-49a3-b01b-9a182d6c37a3.png)

- Capability List

![](./assets/1650009204289-9bd168ad-aa61-41f2-a4cf-2ab28bbf38fc.png)


### 9.6.2 RBAC
Role-Based Access Control，基于权限分类，授予不同的身份<br />根据 user 的职责，给 user 设置某种 role，赋予 role 对应的权限；检测 role，而不是 ID
![image.png](./assets/1650009333021-64eb8471-66d0-4b81-bb58-d62cdeb97acd.png)


### 9.6.3 ABAC
Attribute-Based Access Control，基于实时的属性和使用场景划分用户对某资源的访问权限<br />灵活，前几种都是分配了访问权限之后就固定了。


## 9.7 Incident Response
周期性活动，不断学习和进步，以发现如何最好地保护组织。<br />四个主要阶段:准备、检测/分析、控制/根除和恢复<br />在四个阶段中不断切换反复
![image.png](./assets/1650009406653-bfb9bf8b-8fba-4d39-b3ab-9898b686c542.png)
