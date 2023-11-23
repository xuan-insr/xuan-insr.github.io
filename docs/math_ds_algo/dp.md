# 动态规划 | Dynamic Programming

!!! abstract
    这是 [咸鱼肆力扣分肆](https://github.com/SaltyfishShop/leetcode_subshop/wiki/%E6%AF%94%E8%B5%9B%E8%AE%B0%E5%BD%95#20231023--2023115) 第一个周期的周赛的 ~~掉分惩罚~~ 复盘。
    
    大半年没打比赛，对 DP 的「感觉」又失去了，这也让我不得不承认从来没有学明白过 DP。我希望在这篇文章里能分享和梳理一些对于 DP 的思考模式，也尽可能帮助新来者理解 DP。

    受水平限制，这篇文章可能不会一次成型。在后面看到新的有启发的 DP 题目时会继续在这里补充。（等我觉得补充好了我就把这句话删了）

$W_{0, V} = 0$, $W_{i, v} = \max(W_{i - 1, v}, W_{i - 1, v + w_i} + c_i)$

```
W[0, V] = 0;
for (int i = 1; i < n; i++) {
    for (int j = 0; j < i; j++) {
        
    }
}
```

$C_{i} = \min(\min_{1 \le j < i}(C_{j} + C_{i - j}), \min_{0 \le j < n}(C_{j - n} + 1))$

完全背包问题：

https://leetcode.cn/problems/coin-change/

