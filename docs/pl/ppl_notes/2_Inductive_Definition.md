# 2 Inductive Definition | 归纳定义

## 2.1 Judgments | 判断

**判断 (judgment)** 是关于某种类别的一棵或者多棵 ABT 的陈述，表明一棵或多棵 ABT 有某种性质或者彼此之间有某种联系。

!!! example "一些 judgment"
    - $n \text{ nat}$ ( $n$ 是一个自然数 )
    - $n_1 + n_2 = n$
    - $\tau \text{ type}$ ( $\tau$ 是一个类型 )
    - $e : \tau$ ( 表达式 $e$ 具有 $\tau$ 类型 )
    - $e \Downarrow v$ ( 表达式 $e$ 的值为 $v$ )

这些「性质或联系」本身称为 **判断形式 (judgment form)**，而「一个或多个 ABT 具有这种性质或联系」称为判断形式的 **实例 (instance)**。

判断形式也称为 **谓词 (predicate)**，而构成实例的 ABT 称为实例的 **主语 / 主词 (subject)**。

我们将判断「ABT $a$ 具有 $J$ 性质」记为 $a\ J$ 或者 $J\ a$；相应地，我们也可以将判断形式 $J$ 记为 $-\ J$ 或者 $J\ -$，其中 $-$ 代表 $J$ 缺少的参数，从而强调判断的主语。

## 2.2 Rules | 规则

**规则 (rule)** 规定一个 judgment 有效的充要条件。因而完全决定了这个 judgment 的含义。

一个 judgment form 的 **归纳定义 (inductive definition)** 由一组形如 $\cfrac{J_1\cdots J_k}{J}$ 的 rules 组成，表明当 **前提 (premise)** $J_1, \cdots, J_k$ 都成立时，足以让 **结论 (conclusion)** $J$ 成立，反之不一定成立。

如果一个规则没有任何前提，即 $k = 0$，则称该规则为 **公理 (axiom)**，否则称为 **正常规则 (proper rule)**。

> 我们早上去食堂，可能会想「如果有油条，我就吃油条；如果有拌面，我就吃拌面」；但是我们一般不会给判断中加上「否则」，变成：「如果有油条，我就吃油条；否则，如果有拌面，我就吃拌面」；除非作为一个 "default" 条款时才会用「否则」。但是我们在编程中可能会更加频繁地使用 "else"。

!!! example
    Judgment form 「$- \text{ nat}$」的归纳定义可以是：

    $$\frac{}{\text{zero nat}}$$

    $$\frac{a \text{ nat}}{\text{succ}(a)\text{ nat}}$$

    类似地，判定两个自然数相同的 judgment form 「$- \text{ is } -$」的归纳定义可以是：

    $$\frac{}{\text{zero is zero}}$$

    $$\frac{a \text{ is } b}{\text{succ}(a)\text{ is succ}(b)}$$

    定义二叉树的 judgment form 「$- \text{ tree}$」的归纳定义可以是：

    $$\frac{}{\text{empty tree}}$$

    $$\frac{a_1\text{ tree  }a_2\text{ tree}}{\text{node}(a_1; a_2)\text{ tree}}$$

在上面的例子中，我们通过有限数量的 **规则模式 (rule scheme)**，指定了无限的规则族。

<br/>

**一组规则被看作能够定义封闭于这些规则的最强判断形式。**  
**A collection of rules is considered to define the strongest judgment form that is closed under these rules.**

「封闭于这些规则 (closed under these rules)」说明这些规则足以证明一个判断的有效性。即，如果利用给定的规则能够得到判断 $J$，则 $J$ 一定成立。这意味着我们能够通过组合这些规则 **推导 (derive)** 出 $J$ 来证明 $J$ 成立。

「封闭于这些规则的最强判断形式 (the strongest judgment form that is closed under these rules)」说明所有的规则都是必要的。即，只有通过这些规则得出 $J$ 时，$J$ 才成立。这意味着我们可以通过 **规则归纳 (rule induction)** 来证明 $J$ 成立。

在下面两节中，我们将讨论「推导」和「规则归纳」的细节。


## 2.3 Derivations | 推导

一个 judgment 的推导过程是规则的有限组合，从公理开始，以判断结束。

例如，$\text{node(node(empty; empty); empty) tree}$ 的推导过程如下：

$$\cfrac{\cfrac{\cfrac{}{\text{empty tree}}\quad \cfrac{}{\text{empty tree}}}{\text{node(empty; empty) tree}}\quad \cfrac{}{\text{empty tree}}}{\text{node(node(empty; empty); empty) tree}}$$

要说明一个 judgment 是 **可推导的 (derivable)**，只需要找到一个推导过程。

从公理开始的推导称为 **前向连接 (forwarding chainning)** 或 **自底向上构造 (bottom-up construction)**。它类似 BFS，维护一个可推导的判断集，并扩展这个集合，直到目标判断出现在集合中时终止这个过程。但是它在算法上通常无法决定何时终止推导并得出目标判断不可推导的结论。

从结论开始的推导称为 **反向链接 (backwarding chainning)** 或 **自顶向下构造 (top-down construction)**。它维护一个队列，这个队列刚开始只有目标判断，每次从队头取出一条判断，并将其所有前提加入队列。当队列为空时，说明我们已经达到了所有目标。但同样的，反向链接也没有通用的算法来判定当前目标是否可推导。

## 2.4 Rule Induction | 规则归纳

我们说，「**一组规则被看作能够定义封闭于这些规则的最强判断形式**」。也就是说，如果给定一组规则，它定义的「封闭于这些规则的最强判断形式」是 $J$；而我们证明了另一个判断形式 $P$ 也封闭于这些规则，那么由于 $J$ 是封闭于这些规则的判断形式中最强的，那么就可以证明「只要 $a\ J$ 可推导，那么 $a\ P$ 成立」。这就是 **规则归纳 (rule induction)** 的原理。

更准确地说，如果我们要证明当 **归纳假设 (inductive hypotheses)** $P(a_1), \cdots, P(a_n)$ 成立时 **归纳结论 (inductive conclusion)** $P(a)$ 成立，则需要证明性质 $P$ 封闭于规则 $\cfrac{a_1\ J\cdots a_k\ J}{a\ J}$。

例如，要证明当 $a\text{ nat}$ 时 $P(a)$ 成立，只需要证明：

1. $P(\text{zero})$
2. $\forall a,\  P(a) \to P(\text{succ}(a))$

!!! info "引理 2.1"
    !!! info ""
        **引理 2.1** 要证明当 $a\text{ nat}$ 时 $P(a)$ 成立，只需要证明：

       1. $P(\text{zero})$
       2. $\forall a,\  P(a) \land a\text{ nat} \to P(\text{succ}(a))$

    _Proof_. 定义 $Q(a) = P(a) \land a\text{ nat}$，显然 $Q(a)\to P(a)$。

!!! info "引理 2.2"
    !!! info ""
        **引理 2.2** 如果 $\text{succ}(a) \text{ nat}$ 成立，那么 $a\text{ nat}$ 成立。

    _Proof_. 即证明，$\forall a,b,\ (b = \text{succ}(a) \land b\text{ nat}) \to a\text{ nat}$。

    $$\begin{array}{rl} \\
    &\forall a,b,\  (b = \text{succ}(a) \land b\text{ nat}) \to a\text{ nat}\\
    \Leftrightarrow & \forall a,b,\  b = \text{succ}(a) \to (b\text{ nat} \to a\text{ nat})\\
    \Leftrightarrow & \forall a,b,\  b\text{ nat} \to (b = \text{succ}(a) \to a\text{ nat})\\
    \Leftrightarrow & \forall b,\  b\text{ nat} \to (\forall a,\  b = \text{succ}(a) \to a\text{ nat})\\
    \end{array}
    $$

    记 $P(b) = (\forall a,\  b = \text{succ}(a) \to a\text{ nat})$，我们要证明当 $b\text{ nat}$ 时 $P(b)$ 成立。

    !!! tips
        这是这里的技巧所在，即当要证的形式不能直接使用规则归纳时，借用新的变量来构造规则归纳的形式。
        
        同时请注意，这里的 $b = \text{succ}(a)$ 和 $b \text{ is succ}(a)$ 有一点不同：后者来自于我们对 $\text{is}$ 这个 judgment form 的定义，而前者则来自 ABT 的相等关系。
    
    进行规则归纳：
    
    1. $P(\text{zero}) \Leftrightarrow \forall a,\  \text{zero} = \text{succ}(a) \to a\text{ nat}$。而由于满足 $\text{zero} = \text{succ}(a)$ 的 $a$ 不存在，该式成立。
    2. $\cfrac{\forall a,\  b = \text{succ}(a) \to a\text{ nat}\quad b\text{ nat}}{\forall a,\  \text{succ}(b) = \text{succ}(a) \to a\text{ nat}}$。而 $\text{succ}(b) = \text{succ}(a) \to b = a$，又 $b \text{ nat}$，因此 $a \text{ nat}$，该式成立。

    证毕。

    （所以可以看到，归纳假设是有可能用不到的。）

!!! info "引理 2.3"
    !!! info ""
        **引理 2.3** $\forall a, a\text{ nat}\to a \text{ is }a$。

    证明暂略。

!!! info "引理 2.4"
    !!! info ""
        **引理 2.4** $\text{succ}(a_1)\text{ is succ}(a_2) \to a_1\text{ is }a_2$。

    证明与 **引理 2.2** 类似，暂略。

## 2.5 Iterated and Simultaneous Inductive Definitions | 迭代和联立归纳定义

之前展示的归纳定义都是 **迭代的 (iterated)**，即一个归纳定义建立在另一个归纳定义之上；而一个 **联立归纳定义 (simultaneous inductive definitions)** 由一个规则集组成，这些规则能导出多个不同判断形式的实例。

!!! example
    下面这些规则构造了对奇自然数和偶自然数的联立归纳定义：
    
    $$\cfrac{}{\text{zero even}}$$

    $$\cfrac{b \text{ odd}}{\text{succ}(b)\text{ even}}$$

    $$\cfrac{a \text{ even}}{\text{succ}(a)\text{ odd}}$$

针对上例中的规则，其规则归纳原理表明，要证明 $a\text{ even}$ 时有 $P(a)$ 且 $b\text{ odd}$ 时有 $Q(b)$，只需要证明：

1. $P(\text{zero})$
2. $\forall b,\ Q(b)\to P(\text{succ}(b))$
3. $\forall a,\ P(a)\to Q(\text{succ}(a))$

## 2.6 Defining Functions by Rules | 用规则定义函数

例如，我们可以定义自然数的加法函数 $\text{sum}(a; b; c)$，表示 $c$ 是 $a$ 与 $b$ 的和：

$$\frac{b\text{ nat}}{\text{sum}(\text{zero};b;b)}$$

$$\frac{\text{sum}(a;b;c)}{\text{sum}(\text{succ}(a);b;\text{succ}(c))}$$

!!! info "定理 2.5"
    !!! info ""
        **定理 2.5** 对于每个 $a\text{ nat}$ 和 $b\text{ nat}$，存在唯一的 $c\text{ nat}$ 使得 $\text{sum}(a; b; c)$。

    先证存在性，即如果 $a\text{ nat}$ 且 $b\text{ nat}$，存在 $c\text{ nat}$ 使得 $\text{sum}(a; b; c)$。

    设 $P(a)$ 为：如果 $b\text{ nat}$，存在 $c\text{ nat}$ 使得 $\text{sum}(a; b; c)$。用规则归纳证明如果 $a\text{ nat}$ 则 $P(a)$ 成立：

    1. $P(\text{zero}) \Leftrightarrow \text{sum}(\text{zero};b;c)$，则显然存在 $c \text{ is } b$；
    2. $\cfrac{P(a)}{P(\text{succ}(a))} \Leftrightarrow \cfrac{\text{sum}(a; b; c_1)}{\text{sum}(\text{succ}(a); b; c)}$，则显然存在 $c \text{ is } \text{succ}(c_1)$。

    再证唯一性，即如果 $\text{sum}(a; b; c)$ 且 $\text{sum}(a; b; c')$，则 $c\text{ is }c'$。亦即：
    
    $$\begin{array}{rl}
    &\forall a, b, c, c',\ (\text{sum}(a; b; c) \land \text{sum}(a; b; c')) \to c\text{ is }c' \\
    \Leftrightarrow &\forall a, b, c, c',\ \text{sum}(a; b; c) \to (\text{sum}(a; b; c') \to c\text{ is }c') \\
    \Leftrightarrow &\forall a, b, c, \ \text{sum}(a; b; c) \to (\forall c',\ \text{sum}(a; b; c') \to c\text{ is }c')
    \end{array}
    $$

    （这里使用了 **引理 2.2** 证明中提到的技巧。）

    设 $P(a; b; c)$ 为：$\forall c',\ \text{sum}(a; b; c') \to c\text{ is }c'$。用规则归纳证明 $\forall a, b, c, \ \text{sum}(a; b; c) \to P(a; b; c)$：

    1. 根据 $\text{sum}$ 的第一条定义 $\cfrac{b\text{ nat}}{\text{sum}(\text{zero};b;b)}$，我们需要证明 $\cfrac{b\text{ nat}}{P(\text{zero};b;b)}$；也就是要证 $\forall c',\ (b\text{ nat} \land \text{sum}(\text{zero};b;c'))\to b\text{ is }c'$。这不是显然的，因此我们仍然要通过规则归纳证明之：
        - 我们将其改写为：$\forall a', b', c', \ (b\text{ nat} \land \text{sum}(a';b';c') \land a' = \text{zero} \land b' = b) \to b \text{ is } c$，亦即 $\forall a', b', c', \ (b\text{ nat} \land \text{sum}(a';b';c')) \to (a' = \text{zero} \to (b' = b \to b \text{ is } c))$。
        - 我们记 $Q(a';b';c')$ 为 $a' = \text{zero} \to (b' = b \to b\text{ is }c)$，即我们需要证明 $\forall a', b', c', \ (b\text{ nat} \land \text{sum}(a';b';c')) \to Q(a';b';c')$。可以看到，这里我们仍然使用了前述技巧来将待证的问题转化为规则归纳的形式。我们用规则归纳证明之（这就是课本提到的「内层归纳」）：
            1. 首先要证 $\cfrac{b'\text{ nat}}{Q(\text{zero};b';b')}$，这里 $Q(\text{zero};b';b') \Leftrightarrow \text{zero} = \text{zero} \to (b' = b \to b \text{ is } b')$。根据 **引理 2.3**，该式为真。
            2. 然后证 $\cfrac{Q(a';b';c')\quad \text{sum}(a';b';c')}{Q(\text{succ}(a'); b'; \text{succ}(c'))}$。这里 $Q(\text{succ}(a'); b'; \text{succ}(c')) \Leftrightarrow \text{succ}(a') = \text{zero} \to (b' = b \to b \text{ is } \text{succ}(c'))$。由于不存在 $a'$ 使得 $\text{succ}(a') = \text{zero}$，因此该式为真。
    2. 根据 $\text{sum}$ 的第二条定义 $\cfrac{\text{sum}(a;b;c)}{\text{sum}(\text{succ}(a);b;\text{succ}(c))}$，我们需要证明 $\cfrac{P(a;b;c)\quad \text{sum}(a;b;c)}{P(\text{succ}(a);b;\text{succ}(c))}$；也就是要证 $\forall c',\ (P(a;b;c)\land \text{sum}(a;b;c))\to (\text{sum}(\text{succ}(a);b;c') \to \text{succ}(c)\text{ is } c')$。这也不是显然的，因此我们也要通过规则归纳证明之：
        - 我们将其改写为：$\forall a', b', c',\ (P(a;b;c)\land \text{sum}(a;b;c) \land \text{sum}(a';b';c')) \to (a' = \text{succ}(a) \to (b' = b \to \text{succ}(c)\text{ is } c')))$
        - 记 $Q(a';b';c')$ 为 $a' = \text{succ}(a) \to (b' = b \to \text{succ}(c)\text{ is } c')$，我们用规则归纳证明 $\forall a', b', c',\ (P(a;b;c)\land \text{sum}(a;b;c) \land \text{sum}(a';b';c')) \to Q(a';b';c')$：
            1. 首先要证 $\cfrac{b'\text{ nat}}{Q(\text{zero};b';b')}$，类似上述 2.b 的证明，不存在 $a'$ 使得 $\text{succ}(a') = \text{zero}$，因此该式为真。
            2. 然后证 $\cfrac{Q(a';b';c')\quad \text{sum}(a';b';c')\quad P(a;b;c)}{Q(\text{succ}(a'); b'; \text{succ}(c'))}$：
                - 其中，结论 $Q(\text{succ}(a'); b'; \text{succ}(c'))$ 等价于 $\text{succ}(a') = \text{succ}(a) \to (b' = b \to \text{succ}(c)\text{ is } \text{succ}(c'))$
                - 根据 ABT 的相等关系以及 **引理 2.4**，该式等价于 $a' = a \to (b' = b \to c\text{ is } c')$
                - 要证的规则即为 $\cfrac{Q(a';b';c')\quad \text{sum}(a';b';c')\quad P(a;b;c)}{a' = a \to (b' = b \to c\text{ is } c')}$
                - 亦即 $\cfrac{Q(a';b';c')\quad \text{sum}(a';b';c')\quad P(a;b;c)\quad a' = a\quad b' = b}{c\text{ is } c'}$
                - 而由 $\text{sum}(a';b';c')\land a' = a\land b' = b$ 有前提 $\text{sum}(a; b; c')$，又 $P(a;b;c) \Leftrightarrow \forall c',\ \text{sum}(a; b; c') \to c\text{ is }c'$，因此结论得证。

    证毕。

!!! example "习题 1"
    !!! example ""
        给定判断 $max(m;n;p)$ 的一个归纳定义，其中 $m\text{ nat}, n\text{ nat}, p\text{ nat}$，且 $p$ 是 $m$ 和 $n$ 中的较大者。证明：通过这个判断，每个 $m$ 和 $n$ 都与唯一的 $p$ 相关。