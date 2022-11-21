# 3 Hypothetical and General Judgments | 假言判断与一般性判断

## 3.1 Hypothetical Judgments | 假言判断

2.1 中我们定义了基本判断 (basic judgments)，例如 $a \text{ nat}$ 等，它们用来表明一棵或多棵 ABT 有某种性质或者彼此之间有某种联系。**假言判断 (hypothetical judgment)** 则表示一个或多个 **假设 (hypothesis)** 和一个 **结论 (conclusion)** 之间的 **蕴含关系 (entailment)**。我们首先介绍两种蕴含概念。

### 3.1.1 Derivability | 可导性

给定一个规则集合 $R$，我们用 $R \cup \{J_1, \dots, J_k\}$ 表示利用公理 $\overline{J_1}, \dots, \overline{J_k}$ 对 $R$ 的 **扩展 (expansion)**；这里的 $J_i$ 均为基本判断，这个扩展也就是将这些基本判断对应的公理加入规则集合得到的新的规则集合。

!!! tips
    我们通常用大写希腊字母 $\Gamma$, $\Delta$ 等表示 a finite set of basic judgments。

一个 **可导性判断 (derivability judgment)** $\Gamma \vdash_R K$ 表示：给定一个规则集合 $R$ 和若干基本判断的集合 $\Gamma = \{J_1, \dots, J_k\}$，$R \cup \Gamma$ 能够推导出 $K$。也就是说，我们把该判断的 **假设 (hypothesis)** 或称 **前件 (antecedent)** $J_1, \dots, J_k$ 视为临时公理，和 $R$ 中的规则一同推导出 **结论 (conclusion)** 或称 **后件 (consequent)** $K$。这里的 $J_i$ 和 $K$ 均为基本判断。

$\Gamma \vdash_R K$ 等价于称「规则 $\cfrac{J_1, \dots, J_k}{J}$ 可以从 $R$ 中推导」。说人话就是：根据 $R$，如果 $\Gamma$ 成立，那么可以推导出 $K$ 成立。

!!! example
    例如，记 $R$ 为 2.2 中对 $-\text{ nat}$ 的归纳定义，即：
    
    $$\frac{}{\text{zero nat}}$$

    $$\frac{a \text{ nat}}{\text{succ}(a)\text{ nat}}$$
    
    那么可导性判断的一个例子是：
    
    $$a\text{ nat}\vdash_R \text{succ}(\text{succ}(a))\text{ nat}$$

    也可以表达为，$\cfrac{a \text{ nat}}{\text{succ}(\text{succ}(a))\text{ nat}}$ 可以从规则 $R$ 中推导得出。

    说人话就是：根据 $R$ 可知，对于任意 $a$，如果 $a \text{ nat}$，那么 $\text{succ}(\text{succ}(a))\text{ nat}$。

    可导性判断也是一个判断，也需要通过推导来证明其正确性。事实上，这个判断对于任意 $a$ 的选取都是合法的，其对应的推导是：

    $$\cfrac{\cfrac{a \text{ nat}}{\text{succ}(a))\text{ nat}}}{\text{succ}(\text{succ}(a))\text{ nat}}$$

进一步地，$\Gamma_1 \vdash_R \Gamma_2$ 表示对于 $\Gamma_2$ 中的每个 $J$ 都有 $\Gamma_1 \vdash_R J$。

$\vdash_R J$ 表示 $J$ 可以直接由 $R$ 推导而出。

<br/>

由可导性的定义可得，可导性在扩展新规则时是 **稳定的 (stable)**：

!!! info "定理 3.1 - 稳定性"
    **(稳定性 Stability)** $\quad$ 如果 $\Gamma \vdash_R J$，那么 $\Gamma \vdash_{R\ \cup\ R'} J$

可导性有许多源自其定义的 **结构性质 (structural properties)**，这与 $R$ 的选取无关：

- **自反性 (reflexivity)** $\quad$ $J, \Gamma \vdash_R J$，即 each hypothesis justifies itself as conclusion。
- **弱化 (weakening)** $\quad$ 如果 $\Gamma \vdash_R J$，那么 $\Gamma, K \vdash_R J$，即蕴含不受推导过程中未使用的规则的影响。
- **传递性 (transitivity)** $\quad$ 如果 $\Gamma, K \vdash_R J$ 且 $\Gamma \vdash_R K$，那么 $\Gamma \vdash_R J$。如果我们将一个公理替换为对其的推导，那么就可以得到没有这个假设的情况下对结论的推导。可以在第一个前提下通过规则归纳证明。

!!! bug
    传递性怎么通过规则归纳证明？还没想出来

### 3.1.2 Admissibility | 可纳性

可纳性判断记作 $\Gamma \vDash_R J$，表示 $\vdash_R \Gamma$ 蕴含 $\vdash_R J$；即如果 $\Gamma$ 中的规则都能由 $R$ 推导，那么 $J$ 也能由 $R$ 推导。这是一种较弱的假言判断形式。

可纳性判断 $J_1, \dots, J_k \vDash_R J$ 等价于称「规则 $\cfrac{J_1, \dots, J_k}{J}$ 相对于 $R$ 是 **可纳的 (admissible)**」。

可纳性判断在对规则扩展时并不稳定。

!!! example
    例如，记 $R$ 为 2.5 中对奇自然数和偶自然数的归纳定义，即：

    $$\cfrac{}{\text{zero even}}$$

    $$\cfrac{b \text{ odd}}{\text{succ}(b)\text{ even}}$$

    $$\cfrac{a \text{ even}}{\text{succ}(a)\text{ odd}}$$

    那么可纳性判断 $\text{succ}(a) \text{ even} \vDash_R a\text{ odd}$ 是合法的。它等价于称规则 $\cfrac{\text{succ}(a) \text{ even}}{a\text{ odd}}$ 相对于 $R$ 是可纳的。

    但是，如果用公理 $\cfrac{}{\text{succ(zero) even}}$ 扩展 $R$，则上述规则是不可纳的。因为当 $a = \text{zero}$ 时，刚刚添加的规则能推导出 $\text{succ(zero) even}$，但是没有任何规则可以推导出 $\text{zero odd}$。

    也就是说，可纳性判断在对规则扩展时并不稳定。

可导性的结构特性确保了可导性比可纳性更强。

!!! info "定理 3.2"
    如果 $\Gamma\vdash_R J$，那么 $\Gamma\vDash_R J$。

    证明：即要证，如果 $\Gamma\vdash_R J$ 且 $\vdash_R \Gamma$，那么 $\vdash_R J$。这可以通过可导性判断的传递性证明。

    逆命题是不成立的。一个反例是，在前例中，$\text{succ}(a) \text{ even} \vDash_R a\text{ odd}$ 是合法的，但 $\text{succ}(a) \text{ even} \vdash_R a\text{ odd}$ 是不合法的。

可纳性也有与可导性类似的结构性质：

- **自反性 (reflexivity)** $\quad$ $J, \Gamma \vDash_R J$。
- **弱化 (weakening)** $\quad$ 如果 $\Gamma \vDash_R J$，那么 $\Gamma, K \vDash_R J$。
- **传递性 (transitivity)** $\quad$ 如果 $\Gamma, K \vDash_R J$ 且 $\Gamma \vDash_R K$，那么 $\Gamma \vDash_R J$。

## 3.2 Hypothetical Inductive Definitions | 假言归纳定义

没讲，暂略。

## 3.3 General Judgments | 一般性判断

没看懂，暂略。

## 3.4 Generic Inductive Definitions | 泛型归纳定义

没讲，暂略。
