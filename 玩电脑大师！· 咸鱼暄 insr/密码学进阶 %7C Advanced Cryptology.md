“有不懂中文的吗”<br />“就跟着 Enigma 走？那都不用数学”<br />“那那那算了，反正你们也不知道”<br />“当然这个武术教练是真的嗷”

感谢 jgqgg 的笔记！[https://reticenceji.github.io/Crypto/index.html](https://reticenceji.github.io/Crypto/index.html)


## Topics

1. 引入 / 数论
2. Provable Security
3. Secure Multiparty Computation
4. Zero Knowledge Proofs
5. Encrypted Database
6. Private Information Retrieval
7. Private Set Intersection
8. Secure Multiparty Computation
9. Oblivious RAM
10. ~~Oblivious Neural Network Prediction~~
11. Federated Learning
12. ~~Blockchain Consensus~~


## 1 数论 | Number Theory

- **Divisibility**
- **Primality**
- **Greatest Common Divisor**
- **Ideal** is a non-empty set of integers that is closed under addition, and closed under multiplication by an arbitrary integer.

Semi-honest，诚实地遵守协议，但是尝试获取所有根据协议能够看到的信息<br />Proof of erasion

![55E880368DB7F4195929E6F17C3054B5.jpg](./assets/1641659513788-40abc6a3-a722-4643-9f3c-65cce97e7c7d.jpeg)

## 2 可证明安全 | Provable Security
![46D08BC872ACD11BF74942E7C5095FC8.jpg](./assets/1641659655700-887f8f12-cc65-43aa-a9c0-0b4855f9ad11.jpeg)

### 群 | Group
![2637C5413A514C2CF23E95E39B2A51A5.jpg](./assets/1641659673390-ed49c287-7689-434a-9cc4-20494d35c897.jpeg)

### 环 | Ring
![D00C0C6718D9BD083D620F29EEF54551.jpg](./assets/1641659730199-38a1cb38-9b6f-47b9-b0f5-a37904c01009.jpeg)

### 证明安全的思路
![86046E6DA56CB21C4FA1C6C2EE32C45D.jpg](./assets/1641659745799-708d3c2b-6f88-48e6-a6f4-8eb144c4af7d.jpeg)

### 同态 | Isomorphism
![5095979B5292F83A8AD2153ED107C9E8.jpg](./assets/1641659839936-76106e1a-aeb5-449e-bdda-171c375c42d7.jpeg)


### 安全性评价
![7120216527FDAD7B7F828ED3C72627AA.jpg](./assets/1641659855478-b1132dac-7af4-4abe-951b-1e0abcf178dd.jpeg)

### 离散对数问题、Game、安全性定义
![4E21312CE8E6F561F754EBD33E0EB572.jpg](./assets/1641659921554-23edf002-fd44-46bf-b161-e34dfb44dba9.jpeg)

### Diffie-Hellman Key Exchange
![6137A182A018739ADAD831EB8A76AC4D.jpg](./assets/1641659986399-0eb4781a-c14a-49ef-9f56-f526cf3d2b1a.jpeg)

### CDH, Computational Diffie-Hellman Assumption
![365CDD55CBAC741F8372C1E1CB9E9A3B.jpg](./assets/1641660124102-4033b2b2-092e-4cf5-9308-dc14092dadba.jpeg)


### INDistinguishability Security
![037CB44C7B8C7F0BC8D518D18059210E.jpg](./assets/1641660265445-b6585959-4d8f-41dc-9739-e14fb309e205.jpeg)
![07F81431B761DB64AE27E6F25AE3622F.jpg](./assets/1641660568854-6c2f59ed-b8cb-4af1-a397-733ff2aac237.jpeg)


### DDH, Dicisional Diffie-Hellman
![673FEC7A5F9EE7D8A1446931E30E9954.jpg](./assets/1641660293602-c5f8869d-30e6-4b84-b1e7-774632492140.jpeg)


## 3 安全多方计算 | Secure Multi-Party Computation

### Elgamal & Lifted Elgamal
![9EF2E382AC6508E7812C50215590479F.jpg](./assets/1641660373655-2a3e59db-1ff4-4274-8470-cee03db2c5ab.jpeg)
![C14DB56095000CE8EAEB0DB0968EE3AD.jpg](./assets/1641660489769-3f48bfed-8995-4487-822b-9514309ba8e5.jpeg)


### IND-CPA 和 IND-CCA
![F6D959E9D3233B00AC0769AB6DF0E3B6.jpg](./assets/1641660634505-081dc4e1-68a8-4ee8-a130-3f58ab80a7f5.jpeg)


### 同态加密 | Homomorphic Encryption
![5784F43D1C04335186ACFF86194764E7.jpg](./assets/1641660678280-e55e031f-c102-4f7a-917e-b91cff59d5c6.jpeg)

### 安全两方计算；可信第三方
![A41EE8867156BC4AB5A091841D306C25.jpg](./assets/1641660777900-d4a3729c-120f-463e-94f5-f325d119dc54.jpeg)


### Linearization, Rerandomize, 2-MAH
![015E818CEABD44869EEBD0A393A67857.jpg](./assets/1641660870615-20607df7-51fc-423d-a60c-9da0316bbe7d.jpeg)
为什么要 rerandomize 呢？因为 b=0 时 Enc(ab; rb) = Enc(0; 0) 太明显了<br />![E88CCD019620520753ABA51A6C0DFDFA.jpg](./assets/1641660915127-54dcf1d9-13fb-44f2-8a4d-1ee76b28a2d9.jpeg)

### Computational PIR; Oblivious Transfer
![8835C6A0AF1ADF7EFFC23580F1EEFF8C.jpg](./assets/1641660976250-271ba2b2-710f-46c2-b951-a1d2f219c934.jpeg)

### Trapdoor DL; Paillier
![1942E974DC4FF97D6CF67791C12075B0.jpg](./assets/1641661121273-e36b601f-6512-47e2-8d6c-64f5d6d468df.jpeg)
![F6B275E52162124FCA6BC48353AE00A4.jpg](./assets/1641661111930-55c42968-43fc-484d-8d0a-b22dac8c07ad.jpeg)

## 4 Zero Knowledge Proofs
![557F80E7773C5B8A84635894A21B61FD.jpg](./assets/1641660425648-f335bb07-f0c9-48e3-8af0-a3b46a5e0d8a.jpeg)


## 5 Encrypted Database
![image.png](./assets/1641657827304-0f51a346-94e1-4691-bc67-a6276a96210d.png)

### 保序加密 | OPE, Order-Preserving Encryption
![image.png](./assets/1641657942544-6dba1036-e4e6-4940-94a6-38bfc717d712.png)


#### The first practical OPE scheme: BCLO (2009)
![image.png](./assets/1641657990892-541b2627-2366-4041-a3b4-d4890227ab00.png)
类似折半查找，但是随机（超几何分布 | HG, HyperGeometric Distribution），而且要保存 key table<br />问题：Ciphertexts leak almost the entire first half of plaintexts. 


#### Modular OPE (2011)
![image.png](./assets/1641658108056-154651c9-669f-4b83-928d-fa3d8028cd4e.png)
![image.png](./assets/1641658128976-b47d9c17-6a95-49bb-8697-5d1354981df1.png)


#### MOPE, Mutable OPE (2013)
![image.png](./assets/1641658248291-d8cd161a-3138-432c-99b7-269e6070207e.png)
![image.png](./assets/1641658264894-314383e8-5974-428a-be82-94e05dd97ed6.png)
构建 AVL Tree；服务端存的其实是 AES(plaintext)
Encoding：在第 i 层则第 i 位是 1；后面都是 0；前面各位往左则为 0，往右为 1<br />问题：O(log n) 次交互


#### Efficient MOPE
![image.png](./assets/1641658547155-db4cf791-a5bb-4f51-8673-4a63d2ee4616.png)
本地要备份一份映射关系 O(n)，但查询是 O(1)
适合保存年龄之类的 |{data}| >> |{plaintext}| 的情况


#### POPE, Partial OPE (2016)
[https://www.youtube.com/watch?v=GeLvmRkq_JM](https://www.youtube.com/watch?v=GeLvmRkq_JM)
用 B Tree；都插到 root
![image.png](./assets/1641658658034-6de36770-7022-403c-a72c-de1bb81a6bd2.png)
Server 一次给不了那么多，就随机挑 L 个让 Client 排个序
![image.png](./assets/1641658696877-e67d5f8e-5198-4a3a-b42f-40b51e3406a9.png)
Client 随后给 Server 对应的顺序信息
![image.png](./assets/1641658749345-9693f38d-1a5a-47ba-a79a-940a67b13609.png)
即工作量都在查询过程中；插入过程没啥工作量


#### 比较
![image.png](./assets/1641658825449-e3c81964-f398-48fb-9160-7cc2507523bb.png)


### 针对 OPE 的攻击

#### 基于 Order
![image.png](./assets/1641659092977-f306ac7b-24bf-4d0a-b192-32a279894a2f.png)
假设顺序是可知的；考虑 Efficient OPE 那里讨论的加密年龄的情况，那用密文排个序其实也泄露了明文


#### 基于 Order + Frequency
![image.png](./assets/1641659238755-54a94949-7621-4a57-96fb-15e884370cd5.png)
Bank B 的信息是明文提供的（auxiliary data）


#### 基于 column 之间的关系
![image.png](./assets/1641659352914-7427f394-031a-4a0b-9b7b-7e959cfa4fb8.png)


### SDB (2014)
![AA4EBC9821CC831D1257E67D130711CE.jpg](./assets/1641715109853-47a4c644-3fc3-4ecf-b9c0-3017d3c33511.jpeg)
**比较**：ck = (1, 0) 的时候明文 == 密文；因此相减以后 KeyUpdate 到 (1, 0)。为了避免泄露信息，KeyUpdate 之前乘一个随机数
![image.png](./assets/1641715298652-88f4c4a2-211f-4ecc-9c72-2aed92b2156a.png)
**求和**：由于 ![](https://cdn.nlark.com/yuque/__latex/154f109418e5f4755bcc4961a4c3dd23.svg#card=math&code=g%5E%7Br_ix_j%7D&id=M3hzL) 的存在，只有另 ![](https://cdn.nlark.com/yuque/__latex/65b35f4013745a2ffcc68c1f2749438f.svg#card=math&code=x_j%20%3D%200&id=pfkEd) 才能做加和：
![image.png](./assets/1641715305351-1151d049-a47a-4a38-a1a1-609798b4a731.png)

#### 一些问题
前置知识：互质概率
![image.png](./assets/1641720380375-b8b80b70-a3ba-4379-bcf7-b51bc785be74.png)
问题 1：无法加密 0，因为 0 加密后必然为 0
![image.png](./assets/1641715314387-35180ec6-0cd4-4cc0-9c63-8f9e76b957b6.png)
问题 2：加法和乘法 KeyUpdate 后根据密文比值可以算出明文比值
![image.png](./assets/1641720526290-75089f97-bc56-46ae-9cdf-987437caf58c.png)
问题 3：大意是 KeyUpdate 可逆
![image.png](./assets/1641720850370-9ff051dd-de65-4ada-8850-4b0192d08a85.png)
问题 4：做多次比较会泄露
![image.png](./assets/1641720924958-95888658-235b-454b-947e-6e900bfaed23.png)


### SDB+
大概就是 SDB + Paillier
![image.png](./assets/1641721263422-3bfc249e-9304-4caf-895e-b77a178e4d53.png)
具体的听不懂


## 6 Private Information Retrieval
从数据库拿信息，但是数据库不知道拿的啥

- 全拿下来：Overhead 太大

### CGKS95 | PIR

- ![image.png](./assets/1641721652354-425783d0-b812-4522-893a-95fc22c33599.png)

为什么 Communication cost 𝑂(𝑛) 呢？因为我们需要保证服务器猜中用户拿走的是哪个的概率仍约等于 1/n。服务器有 1/2 的概率猜中自己收到的这个集合包不包含 i，猜中的情况下有 1/m 的概率猜中拿走的那个，因此猜中的总概率是 1/(2m)。所以我们需要让 m = n/2。
![image.png](./assets/1641722335981-80d5aca3-d507-4258-a8e5-f27de1346b92.png)

- ![image.png](./assets/1641722315710-f2b8e394-164c-4247-b5da-3f2dd40af6c7.png)
- ![image.png](./assets/1641722352185-f76c92f2-8c8f-4819-949e-5ec07c658c74.png)

问题：基于保证 server 之间不串通<br />属于 Information-Theoretic Private，即不对算力做假设的安全；单个 server 无法实现 IPIR，只能实现 CPIR：


### KO97 | Single DB cPIR
computational private：多项式算力条件下安全；即基于一些密码学假设
![image.png](./assets/1641723897771-2b46911b-ae69-4d8e-bd03-9ee82615cad5.png)
![image.png](./assets/1641723903835-dc5d20a3-cdfc-4ff4-b589-4fcb6c4959ef.png)
![image.png](./assets/1641723913399-96a504fa-9d7d-4190-a5d6-3c71d8d20309.png)
![image.png](./assets/1641723920177-185b7d61-125d-4887-ac4a-fdcd29076813.png)
为什么 0 0 1 不会被发现呢？我们用的加密方法一般不是 deterministic 的

### Gentry09 | FHE Scheme
基于全同态加密 (FHE, Fully Homomorphic Encryption)
![image.png](./assets/1641727766519-d7492362-ec8a-41c2-a0be-82446976a8e8.png)
![L[[8W63NJAK1FDSQEL]T4PN.png](./assets/1641727742346-b67e0fa4-2fad-4efc-a828-81e487092eb1.png)
（黄底表示加密）<br />XOR 通过模 2 加法算出；即同态加密用的 N 就是 2

计算太多了；FHE 由于添加了噪声只能做有限次操作


### ACLS2017 | SealPIR
想实现这样的效果：
![image.png](./assets/1641728463459-57f6e833-f8d1-4733-8093-a49f4f9a1315.png)
引入这样一个加密系统：
![image.png](./assets/1641728498618-7e9e4367-c392-43e7-a44a-0f88d43fc2a6.png)
即 Sub(Enc(x), N) = Enc(x^N)
由于 mod x^N + 1，因此 x^N + 1 = 0 => x^N = -1 => x^(N+1) = -x。<br />![JJZYP9R0I7G}23[7@HNGB)8.png](./assets/1641734392069-6b71cd5f-7c35-4732-b20a-19ff8bb0fcac.png)

后面讲了什么 25% Fewer Operations，没看懂


### PPY18 | PSIR
Private Stateful Information Retrieval<br />本地先存：
![image.png](./assets/1641736579401-3270dcc3-8ffa-4e20-8a59-add0af720aba.png)
想要 0，可以请求 {0, 2, 4} 的和
![image.png](./assets/1641736594583-028df714-403d-4fe8-bf7d-adb3107c4fbf.png)
希望让它变成 0 2 4 在一行
![image.png](./assets/1641736637564-81cac9ef-8b2e-405d-ac94-48ad87b53578.png)
怎么变呢？<br />首先让 0 在左下角。选一个随机的 k1，做一个哈希 F(k1, index)：
![image.png](./assets/1641736676619-d6f3a899-745d-4e50-a9fc-7027e231da5f.png)
其中 F(k1, 2) 结果是 5，因为有了所以跳过

给结果 +5 可以使得最下面的结果是 0，因此填入 1 7 0：
![image.png](./assets/1641736719038-7177a31a-dbb4-46cc-be4b-fc5e31efec4d.png)
第一列用 (k1, 5) 生成；删除这三个数：
![image.png](./assets/1641736765356-88338261-f6c1-435d-ba6d-174d147fbd78.png)
搞第二列。注意哈希算出来的是下标：
![image.png](./assets/1641736781379-38a0ff40-5811-4225-b7d1-3b22e16b39a0.png)
+3 使得最下面是 0；因为 a[0] = 2：
![image.png](./assets/1641736836598-79f25e36-497e-47aa-895c-f7b76c816805.png)
发现有 4！我们希望 4 在右下角，所以重新选个 k2：
![image.png](./assets/1641736860759-c5cf9bd9-fe93-46cb-b770-e6c951aa271f.png)
搞好了：
![image.png](./assets/1641736871705-4ed8f40a-6343-47cd-a9b7-779921c30e6d.png)
最后一个：
![image.png](./assets/1641736879686-1e9b217b-ed16-4d1d-b928-5e366eda80e2.png)
可以用 cPIR 取一行了：
![image.png](./assets/1641736902689-1b9fe074-f7a6-408d-926f-0680b0addb85.png)
扔掉 2+4，不然服务器容易知道你拿的是什么：
![image.png](./assets/1641736923861-43bcb3e8-2519-4854-b287-5b942687c02b.png)


## 7 Private Set Intersection
![image.png](./assets/1641737010250-3d2ecf84-621b-4758-bf2a-d1b71fb99f1c.png)

- B 把所有 item 的 hash 发给 A，然后 A 逐个做 hash 进行比对
   - 问题：字典攻击

- 基于 DDH

![image.png](./assets/1641740860734-ea6b05f7-3304-4100-ac8a-efebec60c138.png)
![image.png](./assets/1641741833199-41aab889-e1d0-47b7-9ff7-bd6ab41ec4a6.png)
由于 RSA，r^(ed) = r mod N
![image.png](./assets/1641743534533-40de7234-2714-491b-a44b-f877f518dd72.png)
![image.png](./assets/1641743547404-3734a40a-daab-4aef-b37c-5fc1950a537a.png)
![image.png](./assets/1641746027103-157a1241-f742-4753-8263-c98781954ca5.png)

### (8) 突然讲 MPC

#### 1 混淆电路 | Garbled Circuit
混淆电路 [https://baijiahao.baidu.com/s?id=1680159161472356331&wfr=spider&for=pc](https://baijiahao.baidu.com/s?id=1680159161472356331&wfr=spider&for=pc)
![image.png](./assets/1641744479388-51207266-cc8f-405b-a51b-ea202f23f1c9.png)
![image.png](./assets/1641745840175-507781bd-0bd7-4a18-bf53-389aa2695d45.png)
![image.png](./assets/1641745894840-65d66c49-00dc-46d3-8ad1-5349617ffffe.png)

#### 2 秘密共享 | Secret Sharing
![image.png](./assets/1641747381059-b0b66cb4-58fc-4a69-b57f-e23945a4c22d.png)
![image.png](./assets/1641747387202-a7ea2126-06d3-437e-98a1-418e4ba6169a.png)


### 基于 OT 的 PSI
![image.png](./assets/1641751043125-1e58ebe7-c4db-47da-a378-334a2e417bad.png)
![image.png](./assets/1641751048792-c1db89b7-c9ae-434c-b283-23ec424d5c22.png)
![image.png](./assets/1641751059010-f5cb0ebe-1f64-4a7d-90fb-9999ddc4ff3b.png)
![image.png](./assets/1641751556266-4c7b4594-b09c-4911-a876-afc33dc7e102.png)
![image.png](./assets/1641751585829-7934e8f7-a4ae-4aae-a6fc-35ae691424e1.png)
![image.png](./assets/1641751608616-aca7d998-4a48-49f9-8296-bba2a93c26ae.png)
(whp, with high probability)
![image.png](./assets/1641751665446-eb4e4d04-5fe4-4481-bb89-ef0c2e974fd8.png)
O(λn) 的 n 优化不了了，优化 λ
![image.png](./assets/1641751993869-ce17dfcd-5594-4fcb-a9f1-cdad397b1477.png)
![image.png](./assets/1641752043306-c705b764-d691-40ae-8c0d-1c0996e1d833.png)


### Unbalanced PSI
比如你的通讯录和 server 的通讯录求交集，m << n，能不能用 O(m) 而不是 O(n) 的呢？
![image.png](./assets/1641752886651-8f5fc688-4777-4b4a-8cfb-4accec063beb.png)
全同态加密做很多乘法很慢而且有可能做不了

Cuckoo hashing：算 hash；如果冲突了就把那个人踢了让他用下一个 hash 函数算一遍<br />3-way 的版本：二维的；都算出来；不踢出去了 放他后面就好了
![image.png](./assets/1641753258688-f38fd8d2-21b1-4a9b-9c75-1f93eb8b255e.png)
左边是 client 的存储方式，右边是 server 的存储方式；client 发来要查询的内容，server 在对应行查询即可

把一部分幂的计算结果发过去，服务器就不用算乘法了
![image.png](./assets/1641753722516-b984f9e1-5b3a-48d5-9f3d-8eb49833fc9e.png)

![image.png](./assets/1641753945362-a5268939-49d5-46e8-beed-69c2f8b1e143.png)


### 基于可信硬件 Trusted Execution Environments (TEE) 的 PSI
![image.png](./assets/1641754731727-2ded5f6c-fd4d-4236-8a38-86892c0c394d.png)
会泄露 memory access patterns：如果走一半不走了服务器就知道了；都走一遍又太慢了。

怎么办呢？

## 9 Oblivious RAM
![image.png](./assets/1641756420954-5b0811f7-cb83-4b16-a0af-94d3c436867e.png)
![image.png](./assets/1641756412666-cca7e7c0-12d6-418e-afc6-0e0c13196ccf.png)
![image.png](./assets/1641756435545-6de730f1-2b71-44c1-bedd-04e4ae3a5daa.png)
![image.png](./assets/1641756458894-d4d4d33d-3f3d-48cd-b51c-50fd592635b8.png) 
![image.png](./assets/1641756589624-92c410b2-3911-4d4c-829a-b27d286ee26b.png)
![image.png](./assets/1641756704562-0ba06cc3-b5df-4f5f-a910-fcfaf548a4ee.png)
![image.png](./assets/1641756686314-05de08c7-b88d-4367-b63d-989131544c53.png)
![image.png](./assets/1641756719483-2bc33766-34ca-42e9-bbfb-d313d593c691.png)
![image.png](./assets/1641756920127-6dae4d10-2819-4e0a-ab0c-740177b8557e.png)
用冒泡之类的；核心：取两个，在本地换或不换，再放回去


### Hierarchical ORAM

![image.png](./assets/1641758386134-ca02681f-a136-4d0d-9530-1f8b0d0901fe.png)
![image.png](./assets/1641758403727-50961ed3-3425-4cfd-ad61-bbbba3a5cd2f.png)
![image.png](./assets/1641758416322-6ce3c955-1835-4d6d-9817-85d3e44dbee3.png)
![image.png](./assets/1641758435749-156a7455-b14e-4e7e-94e9-f10b3aae0a2d.png)
![image.png](./assets/1641758492369-58d10961-3026-43c1-a7c4-8b32779c0e0e.png)
![image.png](./assets/1641758496948-044031ac-283d-4953-8b75-b65f298393a1.png)
![image.png](./assets/1641758501616-89b47183-3a85-4c91-ab07-4ea1eeacdc60.png)

### Practical ORAM
![image.png](./assets/1641758777714-d6ca3d93-e206-4bd6-8117-e162b7f87cbe.png)
若干个一起用；一个在 shuffle 的时候别的还能用
![image.png](./assets/1641758813527-03272489-7834-4648-bd43-4ce2557744bb.png)

![image.png](./assets/1641758821117-1c2dcb44-e1fa-4e7b-8583-5ace77ef11d8.png)
![image.png](./assets/1641758835401-2531cb51-075b-4e1d-9c99-44ee245dd060.png)
![image.png](./assets/1641758879165-333b261f-cdfa-41ad-b389-a89da5f29ff7.png)
![image.png](./assets/1641759014915-7b396012-891f-4a21-9882-0689f4136b29.png)
从下往上写


## 11 Federated Learning
![image.png](./assets/1641755158663-5a62fb34-828a-4824-800b-24e3a6701fe5.png)
把训练出的模型而不是数据给云端；云端进一步训练后返还给各方；循环若干次<br />由于模型可能会泄露信息，因此云端可以用安全多方计算只计算模型的加和等计算结果，而不是看到模型本身；也可以不用安全多方计算

![image.png](./assets/1641755444969-1d6ecbf2-2287-49ec-bfae-ee0861d78e86.png)
PRG - pseudo random generator

