```markdown
## 无符号除法

我们首先讨论无符号整数除法，以 32 位为例。

### 1 基本思路

当我们计算整数除法 `x / d` 时，我们实际上在计算 $$\lfloor \frac x d\rfloor$$。

而 $$\lfloor \frac x d\rfloor = \lfloor \frac x {2^k} \cdot \frac {2^k} d\rfloor$$。因此如果我们令 $$m_\mathbb{Q} = \frac {2^k}d$$，那么我们就有可能通过计算 $$\lfloor m \cdot \frac x {2^k} \rfloor(m = [m_\mathbb{Q}],\ k \in \mathbb{N})$$，即整数运算 `(x * m) >> k` 的方式来计算 `x / d`。

当然，由 $$m_\mathbb{Q}$$ 取整得到的 $$m$$，会给计算带来误差。通过选取适当的 $$m, k$$，我们可以确保在计算机整数范围内消除这种误差。

为了方便起见，下面的讨论暂时排除 $$d$$ 是 2 的非负整数次幂的情况，即 $$\log_2 d \notin \mathbb{N}$$。

### 2 控制误差
#### 2.1 m 的选取

在考虑 $$k$$ 的取值之前，我们先考虑 $$m$$ 是 $$\frac {2^k}d$$ 向上取整还是向下取整。

考虑 $$m = \lfloor m_\mathbb{Q}\rfloor$$，对于 $$\log_2 d \notin \mathbb{N}$$ 的情况，$$m_\mathbb{Q} = \frac {2^k} d \notin \mathbb{N}$$，那么当被除数为 $$d$$ 时有：

$$1 = \frac d d = m_\mathbb{Q} \cdot \frac d {2^k} > m \cdot \frac d {2^k} > \lfloor m \cdot \frac d {2^k} \rfloor = q$$

可见，此时计算结果严格小于 1，即结果是错误的。因此向下取整不可行。

> _不过，[这里](https://ridiculousfish.com/blog/posts/labor-of-division-episode-iii.html)是使得向下取整也成立的一种方法。我们的实现采用的不是这种方法，因此略。_

考虑 $$m = \lceil m_\mathbb{Q} \rceil$$，对于 $$\log_2 d \notin \mathbb{N}$$ 的情况，$$m = \lceil \frac {2^k} d \rceil = \frac {2^k + e} d$$，其中 $$e = d - (2^k\mod d)$$，即 $$e\in[1 .. d - 1]$$。

因此，我们的计算结果为

$$q = \lfloor m \cdot \frac x {2^k} \rfloor = \lfloor \frac {2^k + e} d \cdot \frac x {2^k} \rfloor = \lfloor \frac x d + \frac e d \cdot \frac x {2^k}\rfloor$$

当 $$m$$ 向上取整造成的误差 $$\frac e d \cdot \frac x {2^k} < 1 + \lfloor \frac x d \rfloor - \frac x d$$ 时，该误差不影响最终结果向下取整的结果，从而可以忽略不计。在最差的情况下，$$x \equiv d-1 (\text{mod } d)$$，此时右式等于 $$\frac 1d$$，即只要 $$\frac e d \cdot \frac x {2^k} < \frac 1 d$$ 就可以保证所有情况下均可舍弃误差。

#### 2.2 k 的选取

为了保证 $$\frac e d \cdot \frac x {2^k} < \frac 1 d (e\in[1 .. d - 1])$$，只需要保证 $$\frac x {2^k} < \frac 1 d\iff 2^k > xd$$ 即可。

又因 $$x < 2^{32}$$，因此只要 $$k > 32 + \log_2 d$$，即可完全避免误差的影响。当 $$\log_2 d \notin \mathbb{N}$$ 时，记 $$s = \lfloor\log_2d\rfloor$$，可以取

$$k = 32 + \lceil \log_2 d\rceil = 32 + s + 1 = s + 33$$

即可满足要求。记 $$d$$ = $$2^s + y$$，显然易观察到 $$m = \lceil \frac {2^k} d \rceil = \lceil \frac {2^{s + 33}} {2^s + y}\rceil $$ 的上下界

$$2^{32} = \frac {2 ^{s + 33}} {2^s + 2^s} < \frac {2^{s + 33}} {2^s + y} \le m \le \lceil \frac {2 ^{s + 33}} {2^s }\rceil = 2^{33}$$

考虑将 $$2^{33}$$ 与 $$m = \frac {2^k + e} d$$ 相减

$$\begin{align*} 2^{33} - \frac {2^k + e} d &= \frac {2^{33}d - 2^{s+33} - e} d \\
&=\frac {2^{33}(d-2^s) - e} d \\
&=\frac {2^{33}y - e} d \end{align*}$$

显然 $$2^{33}y \ge 2^{33} > 2^{32} > d > e$$，故上式 $$>0$$，即 $$2^{32} < m < 2^{33}$$。

可见，$$m$$ 是一个 33 位的数，在我们最后计算乘积的高 32 位 $$p = (m \cdot x) >> 32$$ 时可能会发生溢出，但是溢出位数最多为1位。

### 3 解决溢出问题

由于溢出最多只有1位，在溢出时，我们可以将计算转变为计算 $$p' = {(m - 2^{32})x} >> 32$$。这样就有：

$$\begin{align*} &\ \lfloor \cfrac {m \cdot x} {2^k} \rfloor \\
= &\ ((m - 2^{32})x + 2^{32}x) >> k \\
= &\ (p' + x) >> (k - 32)
\end{align*}$$

但是，这里的 $$p' + x$$ 仍然有可能溢出。我们可以这样实现：

$$\begin{align*} &\ (p' + x) >> (k - 32) \\
= &\ (\frac {x - p' + 2p'} 2) >> (k - 33) \\
= &\ (\lfloor\frac {x - p'} 2\rfloor + p') >> (k - 33)
\end{align*}$$

这里的 $$x - p'$$ 不会溢出，因为 $$p' = \lfloor\frac{(m - 2^{32})x} {2^{32}}\rfloor \le \lfloor\frac{2^{32}x} {2^{32}}\rfloor = x$$。

### 4 小结

这样，我们就解决了计算中的所有问题。我们将步骤总结如下（不考虑 d 是 2 的幂；q 表示结果）：

- 预计算 magic

   1. $$k = \lfloor \log_2 d \rfloor + 33 \iff s = \lfloor \log_2 d \rfloor$$
   2. $$m' = \lceil \frac {2^k} d\rceil - 2^{32} = \lfloor \frac {2^k} d\rfloor + 1 - 2^{32}$$

- 计算结果

   1. $$p' = (m' \cdot x) >> 32$$
   2. $$p = ((x - p') / 2) + p'$$
   3. $$q = p >> (k - 33) \iff q = p >> s$$

### 5 除数为常数时的计算优化

上文中，我们通过放缩不等式，来获取了通用的解法。这个解法中为了避免误差的最终结果中的 $$k$$ 与 $$m$$ 仅仅使用 $$s = \lfloor \log_2 d \rfloor$$ 作为约束条件，即只与 $$\log d$$ 有关。

显然这个条件过于苛刻，将 $$k$$ 限定在了 $$32 + s + 1$$，导致最终 $$m$$ 超出了 32 位整数的表示范围。而倘若能缩小 $$k$$，哪怕只能减少 1，$$m$$ 将落在 32 位整数的表示范围内，后续也不需要通过计算 $$p'$$ 加修正的方式来计算 $$p$$ 了。

#### 5.1 寻求更小的 k

在 _2.2 k 的选取_ 中，我们满足 $$\frac e d \cdot \frac x {2^k} < \frac 1d$$ 的方式是考虑 $$e$$ 在最差情况下等于 $$d - 1$$。但是实际上，$$e = d - (2^k\mod d)$$，即给定 $$d$$ 和 $$k$$，$$e$$ 的值可求得。

将不等式左边进行放缩

$$\frac e d \cdot \frac x {2^k} < \frac e d \cdot \frac {2^{32}} {2^k} = \frac {2^{32-k}} d \cdot e$$

故若满足 $$\frac {2^{32-k}} d \cdot e \le \frac 1 d$$ 的约束条件，则原不等式成立。显然这一约束条件等价于

$$e \le 2^{k-32}$$

因此，对于 $$k\ \in [32..32+s]$$，只要 $$e$$ 分别不大于 $$1, 2, 4, ..., 2^s (=2^{\lfloor \log_2 d\rfloor})$$，误差就仍然处于不影响最终结果的范围内。

同时，易证，如果 $$k = k$$ 时成立，那么 $$k = k+1$$ 时也一定成立：

$$e_{k+1} = d - (2^{k+1}\mod d) \le 2(d - (2^k\mod\ d)) = 2e_k$$，而 $$e_k < 2^{k - 32}$$，因此一定有 $$e_{k+1} < 2e < 2^{(k + 1) - 32}$$。

即最终符合条件的 $$k$$ 存在一个区间，我们将其中最小的 $$k$$ 称为 $$k_{\min}$$，同时考虑到方便计算机计算的可能性，最大值仍选 $$k_{\max} = s + 33$$。则这个区间为

$$k \in [k_{\min}..s + 33]$$

我们从 $$k = 32$$ 开始尝试。对于每个 $$k$$，算出此时 $$r_k = 2^k\mod d$$ 的值，从而判断此时 $$e = d - r$$ 是否满足 $$e \le 2^{k-32}$$。如果满足，则该 $$k$$ 就是我们要找的 $$k_{\min}$$；如果不是，则考察 $$k + 1$$，直至 $$k=s+33$$ 是一定满足条件的 $$k$$。

> _事实上，从 $$k = 32 + p$$ 开始向下尝试，进行尝试总次数的期望更小。但是我们似乎无法从 $$r_{k+1}$$ 和 $$d$$ 得到 $$r_k$$，因而需要做多次除法。而相反易注意到 $$r_{k+1} = (2 \cdot r_k)\mod d$$。不过，对于需要同时计算商的情况，涉及的调整会有些复杂，因此我们没有使用这样的做法。_

显然，如果上述过程找到的 $$k_{\min} < s + 33$$ 时，即区间内元素个数大于 1 时，我们则可以使用省去 _3 解决溢出问题_ 中的额外步骤。需要注意此时选取的 $$k$$ 不再恒等于 $$s+33$$，且由于解决溢出的额外步骤将乘积高位 $$p$$ 已提前右移了 1 位。计算时最后一步的移位应为 $$k - 32$$。

此时 [libdivide](http://libdivide.com/) 和 gcc/clang 使用了不同的处理方式。libdivide 认为，只要 $$k \le s + 32$$，最终的计算指令数就都是一样的，唯一的区别就是 $$m$$ 的大小以及移位的次数。而 gcc/clang 会找到最小的 $$k_{\min}$$，从而 m 也是最小的。

#### 5.2 当除数包含因子 2
考察 gcc/clang 对除以 `uint32_t(28)` 情形的编译结果可以发现，它在 $$x \cdot magic$$ 之前使用了 `x >>= 2`，也就是说它将被除数首先除以 4，从而降低被除数的位数。libdivide 并没有进行这一优化。

进一步考察 gcc/clang 的编译结果，我们发现 gcc/clang 对大多数偶数并没有做这个优化，而是在找到的 $$k_{\min} = 33 + s$$ 的情况下才使用。这也是合理的，因为预先移位本来也会带来更多的指令。

我们可以证明，只要我们预先移位后，结果的 $$m$$ 一定不会引发溢出。其原理非常简单：预先的移位使得 $$x'$$ 的最大位数降低到 $$32 - s_0$$，其中 $$s_0 \ge 1$$是提前移位的位数。即需要满足条件（其中 $$d' = \lfloor \frac d {2^{s_0}} \rfloor$$，即 $$d'$$ 为右移 $$s_0$$ 位后的除数）

$$\frac {e'} {d'} \cdot \frac {x'} {2^{k'}} < \frac {e'} {d'} \cdot \frac {2^{32 - s_0}} {2^{k'}} = \frac {2^{32-s_0-k'}} {d'} \cdot e' \le \frac 1 {d'}$$

其等价于 $$e' \le 2^{s_0} \cdot 2^{k'-32}$$。易证当 $$k' = s+32$$，$$s_0=1$$ 时该条件一定满足，即：

$$e' = d' - (2^{k'}\mod d') < d' < 2^{s+1} = 2^{s_0} \cdot 2^{k'-32} $$

因此 $$k'_{\min}$$ 一定不大于 $$s + 32$$。

故当 _5.1_ 的优化失败时，且恰好 $$d$$ 是偶数时，我们可以预先移位，然后再次按照与 _5.1_ 中类似的方式去寻找 $$k'_{\min}$$。但是，对于最终选取的 $$k$$，我们不希望 $$k<32$$。这是因为，当 $$k<32$$ 时，我们在最后进行移位的时候需要左移而非右移，这会带来额外的分支。因此，我们令 $$k'_{\min} = \max (k'_{\min}, 32)$$。

#### 5.3 当除数大于对应类型最大值的一半

考察 gcc/clang 对除以 `uint_32(0x80000001)` 情形的编译结果可以发现，它直接返回 `x >= 0x80000001`。这是非常合理的，因为当除数大于对应类型最大值的一半时，除法的结果要么是 1 要么是 0。

#### 5.4 k 可以选取 32 时

在 _5.1_ 和 _5.2_ 的基础上，如果最终的 $$k$$ 或 $$k'$$ 可以选取 32 时（即$$k_{\min}=32$$ 或者 $$k'_{\min} \le 32$$）时，可以省去后面的移位（因为大多数平台，包括 x86，支持乘法获得结果高 32 位的指令）。

假设不进行 _5.2_ 的预移位，则 $$k$$ 可以取 32 的条件即为 $$e \le 2^{k-32}$$，即 $$d - (2^{32}\mod d) \le 1$$，即 $$d - (2^{32}\mod d) = 1$$，即 $$(2^{32} + 1)\mod d = 0$$。  
因此，对于 32 位无符号整数而言，这样的除数 $$d$$ 只有两个，即 $$2^{32}+1$$ 的两个因数 641 和 6700417。

如果进行预移位，则类似地， $$k'$$ 可以取 32 的条件为 $$e' \le 2^{s_0} \cdot 2^{k'-32} $$，即 $$d' - (2^{32}\mod d') \le 2^{s_0}$$，即 $$(2^{32} + i)\mod d' = 0$$，其中 $$i\in [1..2^{s_0}]$$。  
例如，当 $$s_0 = 2$$ 时，$$2^{32} + 3$$ 有因数 7、$$2^{32} + 4$$ 有因数 1525 等，因此在除以 $$28 = 7 \times 2^2$$ 或者 $$6100 = 1525 \times 2^2$$ 时，预移位 $$s_0 = 2$$ 位后 $$k'$$ 可以取到 32。

#### 5.5 总结
集合以上讨论和优化，我们得到了 gcc/clang 对于除数为编译期常数的 32 位无符号整数除法的处理方式。我们将所有情形分成 5 种情况：

I. 除数大于对应类型最大值的一半
1. 如果 $$x \ge d$$ 则 q = 1，否则 q = 0

II. 除数是 2 的整数次幂
1. $$r = x >> s$$，其中 $$s = \log_2 d$$

III. 不需要避免溢出的情况  
该分类适用于 $$k_{\min} < 32 + \lceil \log_2 d\rceil$$ 的情形，其中$$k_{\min}$$ 为 $$k \in [32, 32 + \lceil \log_2 d\rceil]$$ 中找到的满足 $$d - (2^k\mod\ d) \le 2^{k-32}$$ 的最小整数
1. 选取 $$k=k_{\min}$$
2. $$p = (m \cdot x) >> 32$$，其中 $$m = \lceil \frac{2^k} d \rceil = \lfloor \frac{2^k} d \rfloor + 1$$
3. $$q = p >> (k - 32)$$

IV. 需要预移位优化的情况  
若上述 $$k_{\min} = 32 + \lceil \log_2 d\rceil$$，且 $$d$$ 为偶数，则应用 _6.2 优化 - 当除数包含因子 2_ 找出新的 $$k'_{\min}$$
1. 选取 $$k=\min(32, k'_{\min})$$
1. $$x' = x >> s_0$$，其中 $$s_0$$ 为 d 最大的 2 的整数次幂因子的指数，即$$s_0 = \log_2\gcd(2^{32}, d)$$
2. $$p = (m \cdot x') >> 32$$，其中 $$m = \lceil \frac{2^k} {d'} \rceil = \lfloor \frac{2^k} {d'} \rfloor + 1$$，$$d' = d >> s_0$$
3. $$q = p >> (k - 32)$$

V. 需要避免溢出的情况  
该分类适用于 $$k_{\min} = 32 + \lceil \log_2 d\rceil$$，且 $$d$$ 为奇数的情形。
1. 选取 $$k=k_{\min}$$，即 $$k = 32 + \lceil \log_2 d\rceil$$
2. $$p' = (m \cdot x) >> 32$$，其中 $$m = \lceil \frac{2^k} d \rceil = \lfloor \frac{2^k} d \rfloor + 1$$
3. $$p = ((x - p') / 2) + p'$$
4. $$q = p >> (k - 33)$$

### 6 除数不为常数时的计算优化

* 不采用第 5 节中讨论的优化，避免分支判断。
  1. 总是选取 $$k = 32 + \lceil \log_2 d\rceil$$
  2. $$p' = (m \cdot x) >> 32$$，其中 $$m = \lceil \frac{2^k} d \rceil = \lfloor \frac{2^k} d \rfloor + 1$$
  3. $$p = ((x - p') / 2) + p'$$
  4. $$q = p >> (k - 33)$$

* 除数为 2 的正整数次幂，可以合并，避免额外判断。
  1. $$p' = (0 \cdot x) >> 32 = 0$$，即选取 $$m = 0$$
  2. $$p = ((x - p') / 2) + p'$$，即 $$p=x >> 1$$
  3. $$q = p >> (\log_2 d - 1)$$

* 除数为 2 的 0 次幂，即 1，似乎不能额外优化。  
  实际上若是上面的通过 $$p’$$ 计算 $$p$$ 的修正计算使用进位位，即可避免提前除以 2，并在最后一步中可以使用带进位位的移位的话。只不过至少在 x86 上，带进位位的循环移位这个操作较慢。不推荐使用。


## 有符号除法

有符号除法的思路类似，但又一些不同之处。我们仍然以 32 位有符号除法为例进行讨论，同时暂不考虑除数是 2 的整数次幂的情形。

我们的基本思路是将计算 $$\frac x d$$ 转化为计算 $$\frac x {|d|}$$，然后如果 d 是负数，结果取相反数即可。也就是说，我们计算 $$\frac {x\cdot m} {2^k} = \frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k}$$。

### 7 控制误差 - k 的选取

与 _2.2 控制误差 - k 的选取_ 中的讨论类似，我们需要保证 $$- \frac 1{|d|} < \frac e {|d|} \cdot \frac x {2^k} < \frac 1{|d|}$$ 以保证误差 $$e = {|d|} - (2^k\mod\ {|d|}) \in [1..|d|-1]$$ 不会影响取整过后的结果。即，需要保证 $$e < \frac {2^k} {|x|} $$。而对于 32 位有符号整数，$$|x| \le 2^{31}$$，即只需要 $$e < 2^{k-31}$$。所以，$$k = 31 + \lceil \log_2 |d| \rceil$$ 一定是符合要求的，我们并不需要考虑溢出，也就没有必要使用 _5.2 当除数包含因子 2_ 的预移位优化了。

gcc/clang 仍然采用了 _5.1 寻求更小的 k_ 这样的方法，找到误差允许范围内最小的 $$k_{\min}$$ 从而使得移位位数和 $$m$$ 尽可能小。同样地，在 $$[k_{\min}..31 + \lceil \log_2 |d| \rceil]$$ 范围内的任一 $$k$$ 都是符合条件的。

但是，我们仍然不希望 $$k < 32$$（事实上，这样的 $$k$$ 也是存在的，例如当 $$d = 3$$ 或者 $$d = 715827883$$ 等值的时候）。因此，我们令 $$k_{\min} = \max(k_{\min}, 32)$$。

根据所选择的 $$k$$，我们计算 $$m = \lceil \frac {2^k}{|d|}\rceil$$。

### 8 校准

#### 8.1 舍入校准

但是，需要注意的是，我们在无符号除法的讨论中，对所有的结果都是向下取整的；而有符号除法的结果是向 0 舍入而不是向下取整（即向负无穷舍入）的。为了解决这一问题，计算 $$\frac {x\cdot m} {2^k} = \frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k}$$ 时，我们可以仍然按照 $$\lfloor \frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k} \rfloor$$ 计算，但是在 x 为负数的情况下，将结果 +1 进行校准。

证明这一做法的正确性，只要证明当 $$-2^{31} \le x < 0$$ 时 $$\lfloor \frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k} \rfloor < \lceil \frac x {|d|} \rceil$$。

因为 d 不为 2 的整数次幂，所以 $$\lceil \frac {2^k}{|d|}\rceil > \frac {2^k}{|d|}$$，因此当 $$x < 0$$ 时 $$\frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k} < \frac {x\cdot \frac {2^k}{|d|}} {2^k} = \frac x {|d|}$$，因此我们只需要证明 $$\frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k}$$ 和 $$\frac x {|d|}$$ 不会同时取到整数即可。

使用反证法。假设 $$\frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k} = a \in \mathbb{Z}, \frac x {|d|} = b \in \mathbb{Z}$$，则有 $$a < b < 0$$。 

与之前的讨论一致，我们记 $$\lceil \frac {2^k}{|d|}\rceil = \frac {2^k + e}{|d|}$$，其中 $$e = {|d|} - (2^k\mod\ {|d|}) \le 2^{k-31}$$。

那么，由 $$\frac {x\cdot \lceil \frac {2^k}{|d|}\rceil} {2^k} = a$$，有 $$x(2^k + e) = a|d|\cdot 2^k$$；又 $$\frac x {|d|} = b$$，则 $$b|d|(2^k + e) = a|d|\cdot 2^k$$，即 $$(a-b)2^k = be$$。

又 $$e \le 2^{k-31}, b < 0$$，因此有 $$(a-b)2^k = be \ge b\cdot 2^{k-31}$$，即 $$(a-b)2^{31} \ge b$$。又 $$a < b$$，因此 $$a - b \le -1$$，因此 $$b \le -2^{31}$$。

但是，$$b = \frac x {|d|}$$，且由于 $$|d|$$ 不是 2 的整数次幂，因此 $$|d| \ge 3$$，因此有 $$x \le -2^{31}|d| \le -3\times 2^{31}$$，这与 $$-2^{31} \le x < 0$$ 矛盾。

因此，该算法是正确的。


#### 8.2 有符号乘法校准

由于 $$x$$ 可能是负值，我们在计算 $$x \cdot m$$ 时会选用有符号乘法。但是，$$m$$ 本身是一个无符号数；如果将其转换为有符号数作乘法，在 $$m$$ 的最高位是 1 的情况下会比实际的数值小 $$2^{32}$$。为了校准这一情况，我们需要在 $$m$$ 的最高位是 1 的情况下，在计算 $$(m\cdot x) >> 32$$ 之后再将结果再加 $$x$$，也就是 $$(m\cdot x) >> 32 + x = ((m + 2^{32})\cdot x) >> 32$$。

用类似 _2.2 k 的选取_ 的方法可以证明，当且仅当 $$k = 31 + \lceil \log_2 d \rceil$$ 的时候需要这一校准。

### 9 总结

集合以上讨论和优化，我们得到了 gcc/clang 对于除数为编译期常数的 32 位有符号整数除法的处理方式：

I. 如果除数的绝对值是 2 的整数次幂

   1. 如果 $$x$$ 是负数，$$x = x + |d| - 1$$，从而将向下取整校准为向 0 舍入
   2. $$q = x >> s$$，其中 $$s = \log_2 |d|$$
   3. 如果 $$d$$ 是负数，$$q = -q$$

II. 需要校准乘法的情况  
该分类适用于 $$k_{\min} = 31 + \lceil \log_2 |d|\rceil$$ 的情形，其中$$k_{\min}$$ 为 $$k \in [32, 31 + \lceil \log_2 |d|\rceil]$$ 中找到的满足 $$|d| - (2^k\mod\ |d|) < 2^{k-32}$$ 的最小整数

   1. 选取 $$k = k_{\min}$$，即 $$k = 31 + \lceil \log_2 |d|\rceil$$
   2. $$p' = (m\cdot x) >> 32$$，其中 $$m = \lceil \frac {2^k}{|d|}\rceil$$
   3. $$p = p' + x$$
   4. $$q = p >> (k - 32)$$
   5. 如果 $$x$$ 是负数，$$q = q + 1$$
   6. 如果 $$d$$ 是负数，$$q = -q$$

III. 不需要校准乘法的情况  
该分类适用于 $$k < 31 + \lceil \log_2 |d|\rceil$$ 的情形。

   1. 选取 $$k = k_{\min}$$
   2. $$p = (m\cdot x) >> 32$$，其中 $$m = \lceil \frac {2^k}{|d|}\rceil$$
   3. $$q = p >> (k - 32)$$
   4. 如果 $$x$$ 是负数，$$q = q + 1$$
   5. 如果 $$d$$ 是负数，$$q = -q$$

### 10 除数不为常数时的计算优化

- 对于有符号整数除法，我们可以先用无符号整数除法计算其绝对值的商，再调整结果的符号，也可以避免分支判断。
  1. 总是选取 $$k = 31 + \lceil \log_2 |d|\rceil$$
  2. $$p = (m \cdot |x|) >> 32$$，其中 $$m = \lceil \frac{2^k} {|d|} \rceil = \lfloor \frac{2^k} {|d|} \rfloor + 1$$
  3. $$q = p >> (k - 32)$$
  4. 如果 $$x$$ 和 $$d$$ 正负性不同，$$q = -q$$

- 除数为 2 的正整数次幂，可以合并，避免额外判断。
  1. $$p = (2^{32 - \log_2 |d|} \cdot |x|) >> 32$$，即 $$p=\lfloor \frac {|x|} {|d|} \rfloor$$，即选取 $$m = 2^{32 - \log_2 |d|}$$
  2. $$q = p >> 0$$，即选取 $$k = 32$$
  3. 如果 $$x$$ 和 $$d$$ 正负性不同，$$q = -q$$

- 与无符号数除法一样，当 $$d = \pm 1$$ 时，无法使用上述方式计算。


## 附记

在具体的工程实现中，我们提供了不同的选项来满足各种不同的应用场景。

我们设计了结构体 `compile_time_magic`，提供与本文完全一致的 `preshift`, `d`, `k`, `m` 字段，以及对应的生成函数 `find_compile_time_magic` 和计算函数 `do_div`。  
- 同时，这些函数提供了 `max_kmin_lower` 模板参数，表示最多允许 $$k_{\min}$$ 比 $$k_{\max}$$ 小多少，从而能够生成误差允许范围内不同的 $$k$$ 以及对应的 $$m$$。  
- 对于无符号数除法，还提供了 `max_preshift` 模板参数，表示最多允许多少位的 preshift。
- 结合这两个模板参数，用户可以生成所有可行的 $$(k, m, preshift)$$ 组合。


基于 `compile_time_magic`，我们提供了类 `constant_div`，根据传入的模板参数（类型 `T` 和除数值 `v`）在编译期生成 `compile_time_magic`。用户可以使用类似 `x / impl::constant_div<uint32_t, 100U>()` 的方式来生成和 gcc/clang 一致的对除数为编译期常数的除法进行的优化。


进一步地，我们设计了结构体 `magic`，将计算所需的字段、一些辅助计算的标志位以及一些调试信息（可选）用更加紧凑的方式保存，更加适合除数不为常数的情形。我们也提供了对应的 `find_magic` 和 `do_div` 函数，实现 magic 的生成以及根据 magic 进行计算。  
- 这些函数提供了和前述一致的 `max_kmin_lower` 和 `max_preshift` （仅无符号除法）模板参数。对于无符号除法，当这些参数均为 0 时，实际上就实现了从 _5.5_ 小节到 _6_ 小节的分支判断避免。当这些参数大于 31 时，会被改为 31。

- 对于无符号数除法，还提供了 `greater_than_half_optimization` 模板参数。当该参数为 `true` 时，在遇到除数大于对应数据类型最大值一半的情形时会采用 _5.5_ 小节的方式 I 进行计算；当该参数为 `false` 时，将不考虑这种优化，正常计算。

- 对于有符号数除法，还提供了 `convert_to_unsigned` 模板参数。当该参数为 `true` 时，会按照 _10_ 小节的方式进行计算；当该参数为 `false` 时，会按照 _9_ 小节的方式进行计算。

- 同时，这些函数还提供了 `power_of_2_optimization` 模板参数。当该参数为 `true` 时，在遇到除数为 2 的整数次幂的情形时将会采用 _5.5_ 小节的方式 II 和 _9_ 小节的方式 I 进行计算；当该参数为 `false` 时，在遇到除数为 2 的整数次幂的情形时会通过生成能适配进其他计算流程的 magic number 来合并计算以避免额外判断。（参见 _6_ 小节，_10_ 小节，及下面的追记）

- `find_magic` 函数还提供了 `debug_msg` 模板参数。当该参数为 `true` 时，会将 `max_kmin_lower`, `max_preshift`, `convert_to_unsigned` 保存到 `magic` 中。

注：对于 `convert_to_unsigned` 为 `true` 且 `max_kmin_lower` 不为 0 的计算方式，当 $$x$$ 为 32 位有符号数最小值 $$-2^{31}$$ 时，对于 $$|d|$$ 是 $$2^{31} + 1$$ 的因数的情况，算出的值是错误的。

对于有符号除法，当 `convert_to_unsigned` 和 `power_of_2_optimization` 均为 `false` 时，在除数为 2 的正整数次幂或其相反数的情况下，我们合并入 _9_ 小节的计算方式 II 从而避免额外判断：  
对于 $$x < 0$$ 时 $$x = x + |d| - 1$$ 的舍入校准，我们可以将其先改为 $$x = x - 1$$，这样计算出的结果比正确结果小 1；然后再利用 _9_ 小节计算方式 II 的第 5 步将结果加 1 从而得到正确的结果。而取 $$m = 1$$，可以使得 2、3 两步实现当 $$x < 0$$ 时 $$x = x - 1$$ 的效果。  
具体步骤为：

   1. $$p' = (1\cdot x) >> 32$$，即选取 $$m = 1$$。即，当 $$x \ge 0$$，$$p' = 0$$；否则 $$p' = -1$$
   2. $$p = p' + x$$
   3. $$q = p >> (\log_2 |d|)$$，即选取 $$k = 32 + \log_2 |d|$$。即，当 $$x \ge 0$$，$$q = \lfloor \frac x {|d|} \rfloor$$；否则 $$q = \lfloor \frac x {|d|} \rfloor - 1$$
   4. 如果 $$x$$ 是负数，$$q = q + 1$$。即 $$q = \lfloor \frac x {|d|} \rfloor$$
   5. 如果 $$d$$ 是负数，$$q = -q$$
   - 注：这种方式对于 $$x$$ 为 32 位有符号数最小值 $$-2^{31}$$ 的情况，由于溢出，算出的值是错误的。

综上所述，如果希望生成和 gcc/clang 相同的 magic，可以将 `max_kmin_lower` 和 `max_preshift` 均设为 31，将 `power_of_2_optimization` 设为 `true`；对于无符号除法，将 `greater_than_half_optimization` 设为 `true`；对于有符号除法，将 `convert_to_unsigned` 设为 `false`。

如果希望避免分支以更高效地实现除数不为常数情况下的计算，可以将 `max_kmin_lower` 和 `max_preshift` 均设为 0，将 `power_of_2_optimization` 设为 `false`；对于无符号除法，将 `greater_than_half_optimization` 设为 `false`；对于有符号除法，将 `convert_to_unsigned` 设为 `true` 或 `false` 均可。

另外，对于无符号除法，如果已知被除数 $$x$$ 的范围，例如 $$x < 2^r, r < 32$$，回顾 _2.2_ 和 _7_ 小节的讨论，$$e < \frac {2^k} {x} $$ 就会有更宽松的条件。对于有符号除法也类似，考虑 $$|x|$$ 的范围即可。  
考虑到这种情况，我们设计了函数 `find_k_m(T d, unsigned x_cap_lower)`，其模板参数包含 `max_kmin_lower`，与前述意义相同；其参数 `d` 即为除数的绝对值，而 `x_cap_lower` 即为 $$32 - r$$ 或者 $$64 - r$$，即已知 $$|x|$$ 所需位数比对应类型的位数少多少位（实际上，在前述讨论中有预移位的情况下，该参数的值即为预移位位数 $$s_0$$）。这个函数返回满足这些条件的最小 $$k$$ 及其对应的 $$m$$ 组成的 pair。  
这样，我们就能够找到更小的 $$k$$ 和 $$m$$，同时无需避免溢出（无符号）或者修正乘法（有符号）。
```

共有 6 篇：<br />[https://ridiculousfish.com/blog/posts/labor-of-division-episode-i.html](https://ridiculousfish.com/blog/posts/labor-of-division-episode-i.html)


## 无符号除法

我们首先讨论无符号整数除法，以 32 位为例。


### 1 基本思路

当我们计算 `x / d` 时，我们实际上在计算 ![](https://g.yuque.com/gr/latex?%5Clfloor%20%5Cfrac%20x%20d%5Crfloor#card=math&code=%5Clfloor%20%5Cfrac%20x%20d%5Crfloor&id=iKYNY) (注：下面的讨论均排除 d 是 2 的幂的情况)

而 ![](https://g.yuque.com/gr/latex?%5Clfloor%20%5Cfrac%20x%20d%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Ccdot%20%5Cfrac%20%7B2%5Ek%7D%20d%5Crfloor#card=math&code=%5Clfloor%20%5Cfrac%20x%20d%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Ccdot%20%5Cfrac%20%7B2%5Ek%7D%20d%5Crfloor&id=biFyQ)；因此如果我们令 ![](https://g.yuque.com/gr/latex?m_e%20%3D%20%5Cfrac%20%7B2%5Ek%7Dd#card=math&code=m_e%20%3D%20%5Cfrac%20%7B2%5Ek%7Dd&id=zWc26)，那么我们就有可能通过计算 ![](https://g.yuque.com/gr/latex?%5Clfloor%20m%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%5Crfloor#card=math&code=%5Clfloor%20m%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%5Crfloor&id=JRrWw) 即 `(x * m) >> k` 的方式来计算 `x / d`。

当然，这里的 m 需要是一个整数。我们希望取整带来的误差不要影响结果。


### 2 m 的选取

在考虑 k 的取值之前，我们先考虑 m 是 ![](https://g.yuque.com/gr/latex?%5Cfrac%20%7B2%5Ek%7Dd#card=math&code=%5Cfrac%20%7B2%5Ek%7Dd&id=CQeoj) 向上取整还是向下取整。

考虑 ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clfloor%20m_e%5Crfloor#card=math&code=m%20%3D%20%5Clfloor%20m_e%5Crfloor&id=gQ8L2)。那么对于 `d / d` (由于 d 不是 2 的幂，因此 ![](https://g.yuque.com/gr/latex?%5Cfrac%20%7B2%5Ek%7D%20d#card=math&code=%5Cfrac%20%7B2%5Ek%7D%20d&id=oK2Uk) 不是整数，因此 ![](https://g.yuque.com/gr/latex?m%20%3C%20m_e#card=math&code=m%20%3C%20m_e&id=IwRIx))，有：

![](https://g.yuque.com/gr/latex?1%20%3D%20%5Cfrac%20d%20d%20%3D%20m_e%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%3E%20m%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%3E%20%5Clfloor%20m%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Ctext%7BResult%7D#card=math&code=1%20%3D%20%5Cfrac%20d%20d%20%3D%20m_e%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%3E%20m%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%3E%20%5Clfloor%20m%20%5Ccdot%20%5Cfrac%20d%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Ctext%7BResult%7D&id=WNSOr)

可见，此时计算结果严格小于 1，即结果是错误的。因此向下取整不可行。

> _不过，_[_这里_](https://ridiculousfish.com/blog/posts/labor-of-division-episode-iii.html)_是使得向下取整也成立的一种方法。我们的实现采用的不是这种方法，因此略。_


考虑 ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clceil%20m_e%20%5Crceil#card=math&code=m%20%3D%20%5Clceil%20m_e%20%5Crceil&id=ooeB6)。事实上，这种情况下 ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%20d%20%5Crceil%20%3D%20%5Cfrac%20%7B2%5Ek%20%2B%20e%7D%20d#card=math&code=m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%20d%20%5Crceil%20%3D%20%5Cfrac%20%7B2%5Ek%20%2B%20e%7D%20d&id=uGLYE)，其中 ![](https://g.yuque.com/gr/latex?e%20%3D%20d%20-%20(2%5Ek%5Cmod%5C%20d)#card=math&code=e%20%3D%20d%20-%20%282%5Ek%5Cmod%5C%20d%29&id=X65yM)，即 e = 1, ..., d - 1。

因此，我们的计算结果

![](https://g.yuque.com/gr/latex?%5Clfloor%20m%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5Ek%20%2B%20e%7D%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5Ek%20%2B%20e%7D%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20x%20d%20%2B%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%5Crfloor#card=math&code=%5Clfloor%20m%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5Ek%20%2B%20e%7D%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5Ek%20%2B%20e%7D%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%5Crfloor%20%3D%20%5Clfloor%20%5Cfrac%20x%20d%20%2B%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%5Crfloor&id=bpdmR)

即，我们的计算结果的误差是 ![](https://g.yuque.com/gr/latex?%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D#card=math&code=%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D&id=Sihr4)；在最差的情况下，![](https://g.yuque.com/gr/latex?x%20%5Cequiv%20d-1%20(%5Ctext%7Bmod%20%7D%20d)#card=math&code=x%20%5Cequiv%20d-1%20%28%5Ctext%7Bmod%20%7D%20d%29&id=q54Uq)，因此我们希望 ![](https://g.yuque.com/gr/latex?%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d#card=math&code=%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d&id=WVrT4)，这样在最差的情况下我们的计算结果也不会由于误差向上进一，导致结果错误。


### 3 控制误差 - k 的选取

注意到 ![](https://g.yuque.com/gr/latex?e%20%5Cle%20d%20-%201#card=math&code=e%20%5Cle%20d%20-%201&id=Issk9)，因此 ![](https://g.yuque.com/gr/latex?2%5Ek%20%3E%20xd%20%5CLeftrightarrow%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d%20%5CRightarrow%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d#card=math&code=2%5Ek%20%3E%20xd%20%5CLeftrightarrow%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d%20%5CRightarrow%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d&id=F0XPW)。又 ![](https://g.yuque.com/gr/latex?x%20%3C%202%5E%7B32%7D#card=math&code=x%20%3C%202%5E%7B32%7D&id=cJO2q)，因此只要 ![](https://g.yuque.com/gr/latex?k%20%3E%2032%20%2B%20%5Clog_2%20d#card=math&code=k%20%3E%2032%20%2B%20%5Clog_2%20d&id=lozAN)，即 ![](https://g.yuque.com/gr/latex?k%20%3D%2032%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil#card=math&code=k%20%3D%2032%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil&id=ZEjXn) 即可完全避免误差的影响。

我们考察这时 m 的值：

![](https://g.yuque.com/gr/latex?%5Crenewcommand%7B%5Carraystretch%7D%7B1.5%7D%5Cbegin%7Barray%7D%7Bll%7D%20%26m%20%5C%5C%0A%3D%20%26%20%5Clceil%5Cfrac%20%7B2%5Ek%7D%20d%20%5Crceil%20%5C%5C%0A%3D%20%26%20%5Clceil%20%5Cfrac%20%7B2%5E%7B32%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil%7D%7D%20d%5Crceil%20%5C%5C%0A%5Cle%20%26%20%5Clceil%20%5Cfrac%20%7B2%5E%7B32%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil%7D%7D%20%7B2%5E%7B%5Clfloor%20%5Clog_2%20d%5Crfloor%7D%7D%5Crceil%20%5C%5C%0A%3D%20%26%202%20%5E%20%7B33%7D%5Cend%7Barray%7D#card=math&code=%5Crenewcommand%7B%5Carraystretch%7D%7B1.5%7D%5Cbegin%7Barray%7D%7Bll%7D%20%26m%20%5C%5C%0A%3D%20%26%20%5Clceil%5Cfrac%20%7B2%5Ek%7D%20d%20%5Crceil%20%5C%5C%0A%3D%20%26%20%5Clceil%20%5Cfrac%20%7B2%5E%7B32%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil%7D%7D%20d%5Crceil%20%5C%5C%0A%5Cle%20%26%20%5Clceil%20%5Cfrac%20%7B2%5E%7B32%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil%7D%7D%20%7B2%5E%7B%5Clfloor%20%5Clog_2%20d%5Crfloor%7D%7D%5Crceil%20%5C%5C%0A%3D%20%26%202%20%5E%20%7B33%7D%5Cend%7Barray%7D&id=SxEua)

可见，`m` 最高可能是一个 33 位的数，在我们最后计算 `(m * x) >> 32` 的乘法时可能会发生溢出。


### 4 解决溢出问题

在这种情况下，我们可以将计算 ![](https://g.yuque.com/gr/latex?m%5Ccdot%20x#card=math&code=m%5Ccdot%20x&id=ORBzh) 转变为计算 ![](https://g.yuque.com/gr/latex?q%20%3D%20%7B(m%20-%202%5E%7B32%7D)x%7D%20%3E%3E%2032#card=math&code=q%20%3D%20%7B%28m%20-%202%5E%7B32%7D%29x%7D%20%3E%3E%2032&id=y2miB)，其中由于 m 是 33 位整数，因此 ![](https://g.yuque.com/gr/latex?m%20-%202%5E%7B32%7D#card=math&code=m%20-%202%5E%7B32%7D&id=ZXjXR) 自然就是一个不超过 32 位的整数 —— 或者说，就是一个 `uint_32` 能保存的整数，其第 33 位已经可以在此前自然溢出舍去了。这样就有：

![](https://g.yuque.com/gr/latex?%5Crenewcommand%7B%5Carraystretch%7D%7B1.5%7D%5Cbegin%7Barray%7D%7Bll%7D%20%26%5Clfloor%20%5Cfrac%20%7Bm%20%5Ccdot%20x%7D%20%7B2%5Ek%7D%20%5Crfloor%20%5C%5C%0A%3D%20%26((m%20-%202%5E%7B32%7D)x%20%2B%202%5E%7B32%7Dx)%20%3E%3E%20k%20%5C%5C%0A%3D%20%26(q%20%2B%20x)%20%3E%3E%20(k%20-%2032)%0A%5Cend%7Barray%7D#card=math&code=%5Crenewcommand%7B%5Carraystretch%7D%7B1.5%7D%5Cbegin%7Barray%7D%7Bll%7D%20%26%5Clfloor%20%5Cfrac%20%7Bm%20%5Ccdot%20x%7D%20%7B2%5Ek%7D%20%5Crfloor%20%5C%5C%0A%3D%20%26%28%28m%20-%202%5E%7B32%7D%29x%20%2B%202%5E%7B32%7Dx%29%20%3E%3E%20k%20%5C%5C%0A%3D%20%26%28q%20%2B%20x%29%20%3E%3E%20%28k%20-%2032%29%0A%5Cend%7Barray%7D&id=Hm99v)

但是，这里的 `q + x` 仍然有可能溢出。我们可以这样实现：

![](https://g.yuque.com/gr/latex?%5Crenewcommand%7B%5Carraystretch%7D%7B1.5%7D%5Cbegin%7Barray%7D%7Bll%7D%20%26(q%20%2B%20x)%20%3E%3E%20(k%20-%2032)%20%5C%5C%0A%3D%20%26(%5Cfrac%20%7Bx%20-%20q%20%2B%202q%7D%202)%20%3E%3E%20(k%20-%2033)%20%5C%5C%0A%3D%20%26(%5Clfloor%5Cfrac%20%7Bx%20-%20q%7D%202%5Crfloor%20%2B%20q)%20%3E%3E%20(k%20-%2033)%0A%5Cend%7Barray%7D#card=math&code=%5Crenewcommand%7B%5Carraystretch%7D%7B1.5%7D%5Cbegin%7Barray%7D%7Bll%7D%20%26%28q%20%2B%20x%29%20%3E%3E%20%28k%20-%2032%29%20%5C%5C%0A%3D%20%26%28%5Cfrac%20%7Bx%20-%20q%20%2B%202q%7D%202%29%20%3E%3E%20%28k%20-%2033%29%20%5C%5C%0A%3D%20%26%28%5Clfloor%5Cfrac%20%7Bx%20-%20q%7D%202%5Crfloor%20%2B%20q%29%20%3E%3E%20%28k%20-%2033%29%0A%5Cend%7Barray%7D&id=CM2sO)

这里的 `x - q` 不会溢出，因为 ![](https://g.yuque.com/gr/latex?q%20%3D%20%5Clfloor%5Cfrac%7B(m%20-%202%5E%7B32%7D)x%7D%20%7B2%5E%7B32%7D%7D%5Crfloor%20%3C%20%5Clfloor%5Cfrac%7B2%5E%7B32%7Dx%7D%20%7B2%5E%7B32%7D%7D%5Crfloor%20%3D%20x#card=math&code=q%20%3D%20%5Clfloor%5Cfrac%7B%28m%20-%202%5E%7B32%7D%29x%7D%20%7B2%5E%7B32%7D%7D%5Crfloor%20%3C%20%5Clfloor%5Cfrac%7B2%5E%7B32%7Dx%7D%20%7B2%5E%7B32%7D%7D%5Crfloor%20%3D%20x&id=ZOCOI)。


### 5 小结

这样，我们就解决了计算中的所有问题。我们将步骤总结如下（不考虑 d 是 2 的幂；r 表示结果）：

-  预计算 magic 
   1. ![](https://g.yuque.com/gr/latex?p%20%3D%20%5Clceil%20%5Clog_2%20d%5Crceil%20%3D%20%5Clfloor%20%5Clog_2%20d%20%5Crfloor%20%2B%201#card=math&code=p%20%3D%20%5Clceil%20%5Clog_2%20d%5Crceil%20%3D%20%5Clfloor%20%5Clog_2%20d%20%5Crfloor%20%2B%201&id=PonwP)
   2. ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5E%7B32%2Bp%7D%7D%20d%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5E%7B32%2Bp%7D%7D%20d%5Crfloor%20%2B%201#card=math&code=m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5E%7B32%2Bp%7D%7D%20d%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5E%7B32%2Bp%7D%7D%20d%5Crfloor%20%2B%201&id=bggbF) (只保留低 32 位)
-  计算结果 
   1. ![](https://g.yuque.com/gr/latex?q%20%3D%20(m%20%5Ccdot%20x)%20%3E%3E%2032#card=math&code=q%20%3D%20%28m%20%5Ccdot%20x%29%20%3E%3E%2032&id=eIYOB)
   2. ![](https://g.yuque.com/gr/latex?t%20%3D%20((x%20-%20q)%20%3E%3E%201)%20%2B%20q#card=math&code=t%20%3D%20%28%28x%20-%20q%29%20%3E%3E%201%29%20%2B%20q&id=rmF08)
   3. ![](https://g.yuque.com/gr/latex?r%20%3D%20t%20%3E%3E%20(p%20-%201)#card=math&code=r%20%3D%20t%20%3E%3E%20%28p%20-%201%29&id=jVPMN)


### 6 优化

显然，虽然 m 有时是 33 位的，但是并不总是如此。在 m 不高于 32 位的情况下，直接计算 ![](https://g.yuque.com/gr/latex?r%20%3D%20(m%5Ccdot%20x)%20%3E%3E%20(32%20%2B%20p)#card=math&code=r%20%3D%20%28m%5Ccdot%20x%29%20%3E%3E%20%2832%20%2B%20p%29&id=aB7fP) 是不会发生溢出的，这样就可以节省若干指令。我们考察这种情况。<br />在 _3 控制误差_ 中可以看出，m 的位数由 k 决定。如果 k 能够减少 1 ，那么 m 就最多只有 32 位了；同时 k 越小，m 的值也就越小。本节中我们讨论两种方式可以减小 k 从而实现这一优化。


#### 6.1 更小的 k

回顾 _3 控制误差_ 中，我们满足 ![](https://g.yuque.com/gr/latex?%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d#card=math&code=%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d&id=BqWzL) 的方式是考虑 e 在最差情况下等于 ![](https://g.yuque.com/gr/latex?d%20-%201#card=math&code=d%20-%201&id=nYPOM)。但是实际上，![](https://g.yuque.com/gr/latex?e%20%3D%20d%20-%202%5Ek%5Cmod%5C%20d#card=math&code=e%20%3D%20d%20-%202%5Ek%5Cmod%5C%20d&id=Kp9ZN)；即给定 d 和<br />k，e 的值是已知的。也就是说：

由于 ![](https://g.yuque.com/gr/latex?%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20%7B2%5E%7B32%7D%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20e%20d%20%5Ccdot%202%5E%7B32-k%7D#card=math&code=%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20%7B2%5E%7B32%7D%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20e%20d%20%5Ccdot%202%5E%7B32-k%7D&id=Kr3Zg)

因此 ![](https://g.yuque.com/gr/latex?e%20%5Cle%202%5E%7Bk-32%7D%20%5CLeftrightarrow%20%5Cfrac%20e%20d%20%5Ccdot%202%5E%7B32-k%7D%20%5Cle%20%5Cfrac%201%20d%5CRightarrow%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d#card=math&code=e%20%5Cle%202%5E%7Bk-32%7D%20%5CLeftrightarrow%20%5Cfrac%20e%20d%20%5Ccdot%202%5E%7B32-k%7D%20%5Cle%20%5Cfrac%201%20d%5CRightarrow%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201d&id=sLqQM)

因此，对于 k = 32, 33, ..., 31 + p, 32 + p，只要 e 分别不大于 1, 2, ..., ![](https://g.yuque.com/gr/latex?2%5E%7Bk-32%7D#card=math&code=2%5E%7Bk-32%7D&id=FqaWz), ..., ![](https://g.yuque.com/gr/latex?2%5E%7Bp-1%7D%20(%3D%202%5E%7B%5Clfloor%20%5Clog_2%20d%5Crfloor%7D)#card=math&code=2%5E%7Bp-1%7D%20%28%3D%202%5E%7B%5Clfloor%20%5Clog_2%20d%5Crfloor%7D%29&id=OSsvd), ![](https://g.yuque.com/gr/latex?2%5Ep%20(%3E%0A2%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D)#card=math&code=2%5Ep%20%28%3E%0A2%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D%29&id=eVT67)，误差就仍然能控制在不影响结果的范围内。可以看到，对于给定的 d，![](https://g.yuque.com/gr/latex?k%20%5Cle%2031%20%2B%20p#card=math&code=k%20%5Cle%2031%20%2B%20p&id=DG0ei) 的概率高达 ![](https://g.yuque.com/gr/latex?1%20-%20%5Cfrac%20%7B2%5E%7B%5Clfloor%20%5Clog_2%20d%5Crfloor%7D%7D%20%7Bd%20-%201%7D#card=math&code=1%20-%20%5Cfrac%20%7B2%5E%7B%5Clfloor%20%5Clog_2%20d%5Crfloor%7D%7D%20%7Bd%20-%201%7D&id=sdR25)。这样的优化大有可为！

同时，我们可以说明，如果 ![](https://g.yuque.com/gr/latex?k%20%3D%20k#card=math&code=k%20%3D%20k&id=WvT2R) 时成立，那么 ![](https://g.yuque.com/gr/latex?k%20%3D%20k%2B1#card=math&code=k%20%3D%20k%2B1&id=f5l9k) 时也一定成立：<br />![](https://g.yuque.com/gr/latex?e'%20%3D%20d%20-%20(2%5E%7Bk%2B1%7D%5Cmod%20d)%3C%202(d%20-%202%5Ek%5Cmod%5C%20d)%20%3D%202e#card=math&code=e%27%20%3D%20d%20-%20%282%5E%7Bk%2B1%7D%5Cmod%20d%29%3C%202%28d%20-%202%5Ek%5Cmod%5C%20d%29%20%3D%202e&id=AJzj1)，而 ![](https://g.yuque.com/gr/latex?e%20%3C%202%5E%7Bk%20-%2032%7D#card=math&code=e%20%3C%202%5E%7Bk%20-%2032%7D&id=vdFDD)，因此一定有 ![](https://g.yuque.com/gr/latex?e'%20%3C%202e%20%3C%202%5E%7B(k%20%2B%201)%20-%2032%7D#card=math&code=e%27%20%3C%202e%20%3C%202%5E%7B%28k%20%2B%201%29%20-%2032%7D&id=g0T8n)。

[libdivide](http://libdivide.com/) 和 gcc/clang 在这种情况使用了不同的处理方式。libdivide 认为，只要 k <= 31 + p，最终的计算指令数就都是一样的，唯一的区别就是 m 的大小以及移位的次数，因此它只考虑 k = 31 + p 和 k = 32 + p 两种情况。而 gcc/clang 会找到最小的 k，从而 m 也是最小的。我们采取与 gcc/clang 相同的方式。

我们从 k = 32 开始尝试。对于每个 k，算出此时 ![](https://g.yuque.com/gr/latex?r_k%20%3D%202%5Ek%5Cmod%20d#card=math&code=r_k%20%3D%202%5Ek%5Cmod%20d&id=BTeU2) 的值，从而判断此时 ![](https://g.yuque.com/gr/latex?e%20%3D%20d%20-%20r#card=math&code=e%20%3D%20d%20-%20r&id=y4S6C) 是否不大于 ![](https://g.yuque.com/gr/latex?2%5E%7Bk-32%7D#card=math&code=2%5E%7Bk-32%7D&id=PNW80)：如果是，则该 k 就是满足要求的最小值；如果不是，则考察 k+1。同时我们关注到，![](https://g.yuque.com/gr/latex?r_%7Bk%2B1%7D%20%3D%20(2r_k)%5Cmod%20d#card=math&code=r_%7Bk%2B1%7D%20%3D%20%282r_k%29%5Cmod%20d&id=rs4NL)，因此我们实际上只需要做一次除法。

> _事实上，从 k = 32 + p 开始向下尝试，进行尝试总次数的期望更小。但是我们似乎无法从 _![](https://g.yuque.com/gr/latex?r_%7Bk%2B1%7D#card=math&code=r_%7Bk%2B1%7D&id=K7oI9)_ 和 d 得到 _![](https://g.yuque.com/gr/latex?r_k#card=math&code=r_k&id=Mn85u)_。_


容易说明，以此法获取的 k 一定是 32, 33, ..., 31 + p, 32 + p 中的一个。如果以此法获取到的 k 不为 32 + p，根据我们之前的讨论，_4 解决溢出问题_ 的操作就不再必要了；也就是说，计算结果中的 ![](https://g.yuque.com/gr/latex?t%20%3D%20((x%20-%20q)%20%3E%3E%201)%20%2B%20q#card=math&code=t%20%3D%20%28%28x%20-%20q%29%20%3E%3E%201%29%20%2B%20q&id=Zkgs7) 步骤就可以省略了，而 ![](https://g.yuque.com/gr/latex?r%20%3D%20t%20%3E%3E%20(p%20-%201)#card=math&code=r%20%3D%20t%20%3E%3E%20%28p%20-%201%29&id=rMNmN) 相应地改为 ![](https://g.yuque.com/gr/latex?r%20%3D%20t%20%3E%3E%20(k%20-%2032)#card=math&code=r%20%3D%20t%20%3E%3E%20%28k%20-%2032%29&id=l08el)。

当然，如果以此法获取的 k 仍然是 32 + p，那么我们仍然回到原先的做法。


#### 6.2 当除数包含因子 2

考察 gcc/clang 对除以 `uint_32(28)` 情形的编译结果可以发现，它在 `x * m` 之前使用了 `x >>= 2`，也就是说它将被除数首先除以 4，从而降低被除数的位数。libdivide 并没有进行这一优化。

进一步考察 gcc/clang 的编译结果，我们发现 gcc/clang 对大多数偶数并没有做这个优化，而是只在原来的 d 算出的 k == 32 + p 的情况下才使用。这也是合理的，因为预先移位本来也会带来更多的指令。

我们可以证明，只要我们预先移位后，结果的 m 一定不会引发溢出。其原理非常简单：预先的移位使得 x 的最大位数降低到 32 - s，其中 s >= 1是提前移位的位数。由于 ![](https://g.yuque.com/gr/latex?%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20%7B2%5E%7B32%20-%20s%7D%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20e%20d%20%5Ccdot%202%5E%7B32-s-k%7D#card=math&code=%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%20e%20d%20%5Ccdot%20%5Cfrac%20%7B2%5E%7B32%20-%20s%7D%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20e%20d%20%5Ccdot%202%5E%7B32-s-k%7D&id=Uw1V7)，只需要 ![](https://g.yuque.com/gr/latex?e%20%5Cle%202%5E%7Bs%2Bk-32%7D#card=math&code=e%20%5Cle%202%5E%7Bs%2Bk-32%7D&id=OkYTz)。因此 k 一定不大于 ![](https://g.yuque.com/gr/latex?32%20%2B%20p%20-%20s%20%5Cle%2031%20%2B%20p#card=math&code=32%20%2B%20p%20-%20s%20%5Cle%2031%20%2B%20p&id=vGULA)。

同时我们可以通过类似的方法，对于每个 k，判断对应的 e 是否不大于 ![](https://g.yuque.com/gr/latex?2%5E%7Bs%2Bk-32%7D#card=math&code=2%5E%7Bs%2Bk-32%7D&id=OEQmq)，从而算出最小的 k。

但是，我们不希望我们得到的 k 小于 32。这是因为，当 k 小于 32 时，我们在最后进行移位的时候需要左移而非右移，这会带来额外的分支。


### 7 当除数大于对应类型最大值的一半

考察 gcc/clang 对除以 `uint_32(0x80000001)` 情形的编译结果可以发现，它直接返回 `x >= 0x80000001`。这是非常合理的，因为当除数大于对应类型最大值的一半时，除法的结果要么是 1 要么是 0。


### 8 总结

集合以上讨论和优化，我们形成了最终的算法。算法分为预计算 magic 和计算结果 2 个步骤。

（下文中 x 表示被除数，r 表示结果，其他字母与前文意义一致。上述讨论和下述算法可以直接推广到除数和被除数为 64 位无符号数的情形。）


#### 8.1 预计算 magic

-  如果除数大于对应类型最大值的一半，标记出这种特殊情况即可 
-  如果除数是 2 的幂次方，则 ![](https://g.yuque.com/gr/latex?k%20%3D%20%5Clog_2%20d#card=math&code=k%20%3D%20%5Clog_2%20d&id=LoEqS) 
-  对于其他一般的情况： 
   1. 找到满足 ![](https://g.yuque.com/gr/latex?d%20-%20(2%5Ek%5Cmod%5C%20d)%20%5Cle%202%5E%7Bk-32%7D#card=math&code=d%20-%20%282%5Ek%5Cmod%5C%20d%29%20%5Cle%202%5E%7Bk-32%7D&id=oKGEw) 的最小 ![](https://g.yuque.com/gr/latex?k#card=math&code=k&id=C2zQz)
   2. ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clceil%20%5Cfrac%7B2%5Ek%7D%20d%20%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%7B2%5Ek%7D%20d%20%5Crfloor%20%2B%201#card=math&code=m%20%3D%20%5Clceil%20%5Cfrac%7B2%5Ek%7D%20d%20%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%7B2%5Ek%7D%20d%20%5Crfloor%20%2B%201&id=Of8BK)
-  当 ![](https://g.yuque.com/gr/latex?k%20%3D%2032%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil#card=math&code=k%20%3D%2032%20%2B%20%5Clceil%20%5Clog_2%20d%5Crceil&id=DADkx) 时，如果 d 是偶数，则我们可以采用 _6.2 优化 - 当除数包含因子 2_。如果采用这种优化，则算法为： 
   1. 找出 d 最大的 2 的整数次幂因子 ![](https://g.yuque.com/gr/latex?2%5Es#card=math&code=2%5Es&id=zVD28)
   2. 找到满足 ![](https://g.yuque.com/gr/latex?d%20-%20(2%5E%7Bk'%7D%5Cmod%5C%20d)%20%5Cle%202%5E%7Bk'%2Bs-32%7D#card=math&code=d%20-%20%282%5E%7Bk%27%7D%5Cmod%5C%20d%29%20%5Cle%202%5E%7Bk%27%2Bs-32%7D&id=oWBHA) 且 ![](https://g.yuque.com/gr/latex?k'%20%5Cge%2032#card=math&code=k%27%20%5Cge%2032&id=O7Ho1) 的最小 ![](https://g.yuque.com/gr/latex?k'#card=math&code=k%27&id=pt7AM)
   3. ![](https://g.yuque.com/gr/latex?m'%20%3D%20%5Clceil%20%5Cfrac%7B2%5E%7Bk'%7D%7D%20d%20%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%7B2%5E%7Bk'%7D%7D%20d%20%5Crfloor%20%2B%201#card=math&code=m%27%20%3D%20%5Clceil%20%5Cfrac%7B2%5E%7Bk%27%7D%7D%20d%20%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%7B2%5E%7Bk%27%7D%7D%20d%20%5Crfloor%20%2B%201&id=NXQqi)


#### 8.2 计算结果

我们将所有情形分成 4 种情况：

a. 除数大于对应类型最大值的一半

1. 如果 ![](https://g.yuque.com/gr/latex?x%20%5Cge%20d#card=math&code=x%20%5Cge%20d&id=mGeVY) 则 r = 1，否则 r = 0

b. 除数是 2 的幂次方

1. ![](https://g.yuque.com/gr/latex?r%20%3D%20x%20%3E%3E%20k#card=math&code=r%20%3D%20x%20%3E%3E%20k&id=hcfVx)

c. 不需要避免溢出的情况<br />该分类适用于 ![](https://g.yuque.com/gr/latex?k%20%3C%2032%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D#card=math&code=k%20%3C%2032%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D&id=xXL8S) 的情形。

1. ![](https://g.yuque.com/gr/latex?q%20%3D%20(m%20%5Ccdot%20x)%20%3E%3E%2032#card=math&code=q%20%3D%20%28m%20%5Ccdot%20x%29%20%3E%3E%2032&id=xifi2)
2. ![](https://g.yuque.com/gr/latex?r%20%3D%20q%20%3E%3E%20(k%20-%2032)#card=math&code=r%20%3D%20q%20%3E%3E%20%28k%20-%2032%29&id=hNtJZ)

d. 需要避免溢出的情况<br />该分类适用于 ![](https://g.yuque.com/gr/latex?k%20%3D%2032%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D#card=math&code=k%20%3D%2032%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D&id=F7K0K) 的情形。

1. ![](https://g.yuque.com/gr/latex?q%20%3D%20(m%20%5Ccdot%20x)%20%3E%3E%2032#card=math&code=q%20%3D%20%28m%20%5Ccdot%20x%29%20%3E%3E%2032&id=WyWft)
2. ![](https://g.yuque.com/gr/latex?t%20%3D%20((x%20-%20q)%20%3E%3E%201)%20%2B%20q#card=math&code=t%20%3D%20%28%28x%20-%20q%29%20%3E%3E%201%29%20%2B%20q&id=sS5Mg)
3. ![](https://g.yuque.com/gr/latex?r%20%3D%20t%20%3E%3E%20(k%20-%2033)#card=math&code=r%20%3D%20t%20%3E%3E%20%28k%20-%2033%29&id=fsEav)

e. 预移位优化<br />对于上述第 4 种情况，如果 d 是偶数，则我们可以采用 _6.2 优化 - 当除数包含因子 2_。如果采用这种优化，则算法为：

1. ![](https://g.yuque.com/gr/latex?x'%20%3D%20x%20%3E%3E%20s#card=math&code=x%27%20%3D%20x%20%3E%3E%20s&id=IVHft)
2. ![](https://g.yuque.com/gr/latex?q%20%3D%20(m'%20%5Ccdot%20x')%20%3E%3E%2032#card=math&code=q%20%3D%20%28m%27%20%5Ccdot%20x%27%29%20%3E%3E%2032&id=RRCX9)
3. ![](https://g.yuque.com/gr/latex?r%20%3D%20q%20%3E%3E%20(k'%20-%2032)#card=math&code=r%20%3D%20q%20%3E%3E%20%28k%27%20-%2032%29&id=ASknP)


## 有符号除法

有符号除法的思路类似，但又一些不同之处。我们仍然以 32 位有符号除法为例进行讨论，同时暂不考虑除数是 2 的整数次幂的情形。

我们的基本思路是将计算 ![](https://g.yuque.com/gr/latex?%5Cfrac%20x%20d#card=math&code=%5Cfrac%20x%20d&id=hNACA) 转化为计算 ![](https://g.yuque.com/gr/latex?%5Cfrac%20x%20%7B%7Cd%7C%7D#card=math&code=%5Cfrac%20x%20%7B%7Cd%7C%7D&id=KzOQH)，然后如果 d 是负数，结果取相反数即可。也就是说，我们仍是计算 ![](https://g.yuque.com/gr/latex?%5Cfrac%20%7Bx%5Ccdot%20m%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D#card=math&code=%5Cfrac%20%7Bx%5Ccdot%20m%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D&id=Kel4K)。


### 9 舍入校准

但是，需要注意的是，我们在无符号除法的讨论中，对所有的结果都是向下取整的；而有符号除法的结果是向 0 舍入而不是向下取整（即向负无穷舍入）的。为了解决这一问题，我们可以仍然按照 ![](https://g.yuque.com/gr/latex?%5Clfloor%20%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D%20%5Crfloor#card=math&code=%5Clfloor%20%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D%20%5Crfloor&id=mn3CO) 计算，但是在 x 为负数的情况下，将结果 +1 进行校准。

> _证明这一做法的正确性，只要证明 _![](https://g.yuque.com/gr/latex?%5Clfloor%20%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D%20%5Crfloor%20%3C%20%5Clceil%20%5Cfrac%20x%20%7B%7Cd%7C%7D%20%5Crceil#card=math&code=%5Clfloor%20%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D%20%5Crfloor%20%3C%20%5Clceil%20%5Cfrac%20x%20%7B%7Cd%7C%7D%20%5Crceil&id=ftArI)_。我的证明思路是，因为 d 不为 2 的整数次幂，所以 _![](https://g.yuque.com/gr/latex?%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%20%3E%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D#card=math&code=%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%20%3E%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D&id=ylrz2)_，因此当 _![](https://g.yuque.com/gr/latex?x%20%3C%200#card=math&code=x%20%3C%200&id=GPHD5)_ 时 _![](https://g.yuque.com/gr/latex?%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D%20%3C%20%5Cfrac%20%7Bx%5Ccdot%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20x%20%7B%7Cd%7C%7D#card=math&code=%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D%20%3C%20%5Cfrac%20%7Bx%5Ccdot%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%7D%20%7B2%5Ek%7D%20%3D%20%5Cfrac%20x%20%7B%7Cd%7C%7D&id=xcW3M)_，因此我们只需要证明 _![](https://g.yuque.com/gr/latex?%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D#card=math&code=%5Cfrac%20%7Bx%5Ccdot%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%7D%20%7B2%5Ek%7D&id=sDSl6)_ 和 _![](https://g.yuque.com/gr/latex?%5Cfrac%20x%20%7B%7Cd%7C%7D#card=math&code=%5Cfrac%20x%20%7B%7Cd%7C%7D&id=J5sYp)_ 不会同时取到整数即可。然后我就不会证了……_



### 10 控制误差 - k 的选取

回顾 _3 控制误差_ 中我们的讨论，我们希望 ![](https://g.yuque.com/gr/latex?%5Cfrac%20e%20%7B%7Cd%7C%7D%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201%7B%7Cd%7C%7D#card=math&code=%5Cfrac%20e%20%7B%7Cd%7C%7D%20%5Ccdot%20%5Cfrac%20x%20%7B2%5Ek%7D%20%3C%20%5Cfrac%201%7B%7Cd%7C%7D&id=nhdLE)，其中 ![](https://g.yuque.com/gr/latex?e%20%3D%20%7B%7Cd%7C%7D%20-%20(2%5Ek%5Cmod%5C%20%7B%7Cd%7C%7D)#card=math&code=e%20%3D%20%7B%7Cd%7C%7D%20-%20%282%5Ek%5Cmod%5C%20%7B%7Cd%7C%7D%29&id=EMagY)。不过在此时，x 的范围不会超过 ![](https://g.yuque.com/gr/latex?%5Cpm%202%5E%7B31%7D#card=math&code=%5Cpm%202%5E%7B31%7D&id=NVEPV)，因此结合 _6 优化_ 中的讨论，我们只需要 ![](https://g.yuque.com/gr/latex?e%20%5Cle%202%5E%7Bs%2Bk-31%7D#card=math&code=e%20%5Cle%202%5E%7Bs%2Bk-31%7D&id=pODiK)，因此 k 一定不大于 31。所以我们并不需要考虑溢出。

因此，我们没有必要使用 _6.2 当除数包含因子 2_ 的预移位优化。当然，gcc/clang 仍然采用了 _6.1 更小的 k_ 这样的方法，找到误差允许范围内最小的 k 从而使得移位位数和 m 的位数尽可能小。我们仍然采用这种方法。

但是，我们仍然不希望得到的 k 小于 32（事实上，这样的 k 也是存在的，例如当 d = 3 或者 d = 715827883 等值的时候）。这是因为，当 k 小于 32 时，我们在最后进行移位的时候需要左移而非右移，这会带来额外的分支。

也就是说，我们选用满足 ![](https://g.yuque.com/gr/latex?e%20%5Cle%202%5E%7Bs%2Bk-31%7D#card=math&code=e%20%5Cle%202%5E%7Bs%2Bk-31%7D&id=nfdKM) 且 ![](https://g.yuque.com/gr/latex?k%20%5Cge%2032#card=math&code=k%20%5Cge%2032&id=EMoRe) 的最小的 k。进一步地，我们计算 ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil#card=math&code=m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil&id=A1R9d)。


### 11 有符号乘法校准

由于 x 可能是负值，我们在计算 ![](https://g.yuque.com/gr/latex?x%20%5Ccdot%20m#card=math&code=x%20%5Ccdot%20m&id=bJVhY) 时会选用有符号乘法。但是，m 本身是一个无符号数；如果将其转换为有符号数作乘法，在 m 的最高位是 1 的情况下会比实际的数值小 ![](https://g.yuque.com/gr/latex?2%5E%7B32%7D#card=math&code=2%5E%7B32%7D&id=rx7mb)。为了校准这一情况，我们需要在 m 的最高位是 1 的情况下，在计算 ![](https://g.yuque.com/gr/latex?(m%5Ccdot%20x)%20%3E%3E%2032#card=math&code=%28m%5Ccdot%20x%29%20%3E%3E%2032&id=L0fll) 之后再将结果再加 x，也就是 ![](https://g.yuque.com/gr/latex?(m%5Ccdot%20x)%20%3E%3E%2032%20%2B%20x%20%3D%20((m%20%2B%202%5E%7B32%7D)%5Ccdot%20x)%20%3E%3E%2032#card=math&code=%28m%5Ccdot%20x%29%20%3E%3E%2032%20%2B%20x%20%3D%20%28%28m%20%2B%202%5E%7B32%7D%29%5Ccdot%20x%29%20%3E%3E%2032&id=eDZjI)。


### 12 总结

算法同样分为预计算 magic 和计算结果 2 个步骤。

（下文中 x 表示被除数，r 表示结果，其他字母与前文意义一致。上述讨论和下述算法可以直接推广到除数和被除数为 64 位无符号数的情形。）


#### 12.1 预计算 magic

-  如果除数的绝对值是 2 的幂次方，则 ![](https://g.yuque.com/gr/latex?k%20%3D%20%5Clog_2%20d#card=math&code=k%20%3D%20%5Clog_2%20d&id=tZC0x) 
-  对于其他一般的情况： 
   1. 找到满足 ![](https://g.yuque.com/gr/latex?%7B%7Cd%7C%7D%20-%20(2%5Ek%5Cmod%5C%20%7B%7Cd%7C%7D)%20%5Cle%202%5E%7Bk-31%7D#card=math&code=%7B%7Cd%7C%7D%20-%20%282%5Ek%5Cmod%5C%20%7B%7Cd%7C%7D%29%20%5Cle%202%5E%7Bk-31%7D&id=DenGT) 且 ![](https://g.yuque.com/gr/latex?k%20%5Cge%2032#card=math&code=k%20%5Cge%2032&id=ou6TI) 的最小的 k
   2. 计算 ![](https://g.yuque.com/gr/latex?m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crfloor%20%2B%201#card=math&code=m%20%3D%20%5Clceil%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crceil%20%3D%20%5Clfloor%20%5Cfrac%20%7B2%5Ek%7D%7B%7Cd%7C%7D%5Crfloor%20%2B%201&id=QG2P7)


#### 12.2 计算结果

a. 如果除数的绝对值是 2 的幂次方

1. 如果 x 是负数，![](https://g.yuque.com/gr/latex?x%20%3D%20x%20%2B%202%5Ek%20-%201#card=math&code=x%20%3D%20x%20%2B%202%5Ek%20-%201&id=q0hQc)，从而将向下取整校准为向 0 舍入
2. ![](https://g.yuque.com/gr/latex?r%20%3D%20x%20%3E%3E%20k#card=math&code=r%20%3D%20x%20%3E%3E%20k&id=jB4eU)
3. 如果 d 是负数，![](https://g.yuque.com/gr/latex?r%20%3D%20-r#card=math&code=r%20%3D%20-r&id=g3U92)

b. 需要校准乘法的情况<br />该分类适用于 ![](https://g.yuque.com/gr/latex?k%20%3D%2031%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D#card=math&code=k%20%3D%2031%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D&id=Hbai9) 的情形。

1. ![](https://g.yuque.com/gr/latex?q%20%3D%20(m%5Ccdot%20x)%20%3E%3E%2032#card=math&code=q%20%3D%20%28m%5Ccdot%20x%29%20%3E%3E%2032&id=Tpqwy)
2. ![](https://g.yuque.com/gr/latex?t%20%3D%20q%20%3E%3E%20(k%20-%2032)#card=math&code=t%20%3D%20q%20%3E%3E%20%28k%20-%2032%29&id=AWrLU)
3. ![](https://g.yuque.com/gr/latex?r%20%3D%20t%20%2B%20x#card=math&code=r%20%3D%20t%20%2B%20x&id=HwIju)
4. 如果 x 是负数，![](https://g.yuque.com/gr/latex?r%20%3D%20r%20%2B%201#card=math&code=r%20%3D%20r%20%2B%201&id=Gfgzk)
5. 如果 d 是负数，![](https://g.yuque.com/gr/latex?r%20%3D%20-r#card=math&code=r%20%3D%20-r&id=Gh8E4)

c. 不需要校准乘法的情况<br />该分类适用于 ![](https://g.yuque.com/gr/latex?k%20%3C%2031%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D#card=math&code=k%20%3C%2031%20%2B%202%5E%7B%5Clceil%20%5Clog_2%20d%5Crceil%7D&id=pAYbd) 的情形。

1. ![](https://g.yuque.com/gr/latex?q%20%3D%20(m%5Ccdot%20x)%20%3E%3E%2032#card=math&code=q%20%3D%20%28m%5Ccdot%20x%29%20%3E%3E%2032&id=rHSwD)
2. ![](https://g.yuque.com/gr/latex?r%20%3D%20q%20%3E%3E%20(k%20-%2032)#card=math&code=r%20%3D%20q%20%3E%3E%20%28k%20-%2032%29&id=Vywqg)
3. 如果 x 是负数，![](https://g.yuque.com/gr/latex?r%20%3D%20r%20%2B%201#card=math&code=r%20%3D%20r%20%2B%201&id=w29YZ)
4. 如果 d 是负数，![](https://g.yuque.com/gr/latex?r%20%3D%20-r#card=math&code=r%20%3D%20-r&id=sSDZw)
