# 咸鱼暄学区块链

学一下区块链！

[北京大学肖臻老师《区块链技术与应用》公开课](https://www.bilibili.com/video/BV1Vt411X7JF) 看起来不错，从这里开始学试试。

笔记先都记在这个文档里！形成体系之后再重新梳理和拆分。

## 1 BitCoin

### 1.1 密码学原理

比特币是一种加密货币 (Cryptocurrency)。它的核心技术是区块链 (Blockchain)。

- 加密货币其实没有加密，区块链上的所有信息都是公开的。

!!! warning
    密码学相关知识在以前的安全相关课程学过了，这里不过多展开。

#### Cryptographic Hash Function

密码学中的哈希函数 (Cryptographic Hash Function) 是比特币的基础。它们通常有以下重要特性：

1. Collision Resistance：没有高效的方法找到两个不同的输入，使得它们的哈希值相同。
    - 这一点很难证明，通常是验证性的。但是也有一些哈希函数被破解了，比如 MD5。
2. Hiding：给定一个哈希值，没有高效的方法找到对应的输入。
    - 这个性质可以被用来实现 Digital Commitment，也叫做 Digital Equivalent of Sealed Envelope。
    - 例如，如果某个时刻我需要证明我已经知道了某个信息，但是我不想让别人知道这个信息，我可以先把这个信息哈希一下，然后把哈希值公开。等到需要证明的时候，我再公开原始信息，让别人验证哈希值是否匹配。
3. Puzzle Friendly：给定一个哈希值，没有高效的方法找到对应的输入，使得哈希值的前缀满足某个条件。
    - 这个性质可以被用来实现 Proof of Work。Proof of Work 的目的是为了让计算机在找到一个特定的输入的时候需要花费一定的时间，从而防止恶意用户快速地生成大量的输入。
    - Puzzle 的一个例子是，我们定义对于一个输入 `payload`，我们需要找到一个 `nonce`，使得哈希函数值 `H(payload + nonce)` 的前缀有 `k` 个 0 (即 `H(payload + nonce) < target`)。
    - Puzzle Friendly 事实上是指，difficult to solve but easy to verify。

比特币使用的哈希函数是 SHA-256。

#### Digital Signature

如何在比特币中开一个「账户」？只需要生成一对 Public Key 和 Private Key。

- 这个概念来自于非对称加密 (Asymmetric Cryptography)。对称加密 (Symmetric Cryptography) 是指加密和解密使用同一个密钥，它的核心问题是密钥的分发。非对称加密使用一对密钥，一个用来加密，一个用来解密。这样只需要分发公钥，私钥可以保密。

当我发布一个交易时，我使用我的私钥对交易进行签名。其他人需要验证这个交易是否是我发布的，只需要使用我的公钥对签名进行验证。

值得注意的是，在生成公私钥以及签名时，我们都需要使用随机数。使用一个好的随机数生成器是非常重要的，否则会导致私钥泄露。

### 1.2 数据结构

#### Hash Pointers

