# 美团 计算引擎

98 看到的。2.27 投的。

### 3.5 笔试

120 分钟，有一份 4 题的和一份 1 题的，先做了 4 题的交卷才能做 1 题的；可以用自己的 IDE，提交就出结果

115 分钟 AK 了，开心！我的顺序是 3 4 2 1 5

总体的感觉是数据很弱，数据范围很小

#### T1
输入一个 n(~100000)，给一个大小为 n 的可重集，数据范围是 1~200000，求一个最大的子集，使得其中任意两个元素的差不小于 2。

??? success "我的答案"
    ```c++
    #include <iostream>
    #include <cstdio>
    #include <algorithm>
    using namespace std;

    int n;
    bool exist[200005];
    int dp[2][200005];

    int main() {
        cin >> n;
        int tmp;
        for (int i = 0; i < n; i++) {
            scanf("%d", &tmp);
            exist[tmp] = true;
        }

        for (int i = 1; i <= 200000; i++) {
            dp[0][i] = max(dp[0][i - 1], dp[1][i - 1]);
            if (exist[i])
                dp[1][i] = max(dp[0][i - 1], dp[1][i - 2]) + 1;
        }

        cout << max(dp[0][200000], dp[1][200000]);

        return 0;
    }
    ```
    还是不敢做 DP 的题，看见就会绕着走

#### T2
输入一个 n(~100000)，给一个数组，数据范围是 -1000~1000，求将一个子数组进行翻转（例如 1 -2 3 -5 4 2 可以将后三个元素翻转得到 1 -2 3 2 4 -5）后的最大区间和。

??? success "我的答案"
    分析了一下，觉得其实是找不重叠的两个区间，使它们的和最大，这样做一次翻转肯定能翻过去。刚开始是想贪心，找最大的然后删掉然后找次大的，能得 72% 的分：

    ```c++
    #include <iostream>
    #include <cstdio>
    #include <algorithm>
    using namespace std;

    int n;
    int a[100005];
    int preSum[100005];
    int minn[100005];
    int minx[100005];
    int maxn = -1000, maxx;

    int main() {
        cin >> n;
        for (int i = 0; i < n; i++) scanf("%d", &a[i]);
        preSum[0] = minn[0] = 0; minx[0] = -1; maxn = a[0];
        for (int i = 0; i < n; i++) {
            preSum[i + 1] = preSum[i] + a[i];
            minn[i + 1] = min(minn[i], preSum[i]);
            minx[i + 1] = preSum[i + 1] <= minn[i] ? i : minx[i];
            if (preSum[i + 1] - minn[i + 1] >= maxn)     maxn = preSum[i + 1] - minn[i + 1], maxx = i;
        }
        int result = maxn;

        for (int i = minx[maxx] + 1; i <= maxx; i++)
            a[i] = -1001;

        for (int i = 0; i < n; i++)
            cout << a[i] << " ";
        cout << endl;

        preSum[0] = minn[0] = 0; maxn = a[0];
        for (int i = 0; i < n; i++) {
            preSum[i + 1] = preSum[i] + a[i];
            minn[i + 1] = min(minn[i], preSum[i]);
            if (preSum[i + 1] - minn[i + 1] >= maxn)     maxn = preSum[i + 1] - minn[i + 1];
        }

        for (int i = 0; i <= n; i++)
            cout << preSum[i] << " ";
        cout << endl;

        for (int i = 0; i <= n; i++)
            cout << minn[i] << " ";
        cout << endl;

        cout << result << " " << maxn << endl;

        cout << result + maxn << endl;
        return 0;
    }
    ```

    但是显然贪心不对，考虑到两个区间不重叠就可以把数组分成 2 份，而最大区间和是有 dp 性质的，所以正着和倒着各做一次最大区间和，然后遍历每个点，以它为界分成两边。

    ```c++
    #include <iostream>
    #include <cstdio>
    #include <algorithm>
    using namespace std;

    int n;
    int a[100005];
    int preSumForw[100005], preSumBackw[100005];
    int minForw[100005], minBackw[100005];
    int maxForw[100005], maxBackw[100005];

    int main() {
        cin >> n;
        for (int i = 0; i < n; i++) scanf("%d", &a[i]);

        preSumForw[0] = a[0];
        minForw[0] = min(a[0], 0);
        maxForw[0] = a[0] - minForw[0];
        for (int i = 1; i < n; i++) {
            preSumForw[i] = preSumForw[i - 1] + a[i];
            minForw[i] = min(minForw[i - 1], preSumForw[i]);
            maxForw[i] = max(maxForw[i - 1], preSumForw[i] - minForw[i]);
        }

        preSumBackw[n - 1] = a[n - 1];
        minBackw[n - 1] = min(a[n - 1], 0);
        maxBackw[n - 1] = a[n - 1] - minBackw[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            preSumBackw[i] = preSumBackw[i + 1] + a[i];
            minBackw[i] = min(minBackw[i + 1], preSumBackw[i]);
            maxBackw[i] = max(maxBackw[i + 1], preSumBackw[i] - minBackw[i]);
        }

        int maxn = maxForw[0] + maxBackw[1];
        for (int i = 1; i < n; i++) {
            maxn = max(maxn, maxForw[i] + maxBackw[i + 1]);
        }

        cout << maxn << endl;

        return 0;
    }
    ```

#### T3 
有一块长宽高为 n 的豆腐，固定好了，现在切 m(~1000) 刀，每刀是从 x / y / z 轴上坐标为 a 的位置垂直切一刀；输出 m 行，每行表示切对应一刀之后最大块的豆腐是多大

例如，刚开始是 `3*3*3` 的豆腐，在 `x 1` 处切一刀变成了 `1*3*3` 和 `2*3*3` 两块，再在 `y 2` 处切一刀变成了 `1*2*3` `1*1*3` `2*2*3` `2*1*3` 四块，以此类推

??? success "我的答案"
    本来想用优先队列的，后来发现那样就不知道砍在哪块了，所以用了链表。每次结果是 x y z 三条边上各取最大长度的乘积，因此维护链表的最大值。用了比较愚蠢的方式维护。

    ```c++
    #include <iostream>
    #include <queue>

    using namespace std;

    struct node {
        int val;
        node *next;
    };

    int main() {
        int n, m;
        cin >> n >> m;
        int dir[1005], val[1005];
        char temp;
        for (int i = 0; i < m; i++) {
            cin >> temp;
            if (temp == 'x')        dir[i] = 0;
            else if (temp == 'y')   dir[i] = 1;
            else                    dir[i] = 2;
            getchar();
        }
        for (int i = 0; i < m; i++) {
            cin >> val[i];
        }

        node *sz[3];
        for (auto & i : sz) {
            i = new node{0, new node{n, nullptr}};
        }

        int maxn[3] = {n, n, n};

        for (int i = 0; i < m; i++) {
            int count = 0;
            node *tmp = sz[dir[i]];
            while (tmp->next) {
                if (count + tmp->next->val == val[i])    break;

                else if (count + tmp->next->val > val[i]) {
                    int a = val[i] - count;
                    int b = tmp->next->val - a;
                    tmp->next->val = a;
                    tmp->next->next = new node{b, tmp->next->next};
                    if (a + b == maxn[dir[i]]) {
                        tmp = sz[dir[i]];
                        maxn[dir[i]] = tmp->val;
                        while (tmp) {
                            maxn[dir[i]] = max(maxn[dir[i]], tmp->val);
                            tmp = tmp->next;
                        }
                    }
                    break;
                }

                count += tmp->next->val;
                tmp = tmp->next;
            }

            cout << maxn[0] * maxn[1] * maxn[2] << endl;
        }

        return 0;
    }
    ```

#### T4 
输入 n(~5000), m(~500)，输入一个有 n 个元素的数组，然后输入 m 次查询，查询有 2 种格式：`1 l r` 表示查询 [l, r] 范围的区间和，`2 l r k` 表示将 [l, r] 范围内的元素 +k。在查询开始之前，我们可以任意排列这个数组的顺序，输出所有查询区间和结果的 **总和** 的最大值（不要求输出每次查询的结果）。

??? success "我的答案"
    首先，显然不考虑增加的情况下，将越大的元素放在求和次数越多的位置上就可以得到最大值。同时容易证明，排列的顺序不影响区间 +k 对结果造成的影响。

    ```c++
    #include <iostream>
    #include <cstdio>
    #include <algorithm>
    using namespace std;

    struct query {
        int type;
        int l;
        int r;
        int k;
    } q[505];

    int n, m;
    int a[5005];
    int cnt[5005];
    int addK[5005];
    long long addSum = 0;

    int main() {
        cin >> n >> m;
        for (int i = 0; i < n; i++)
            scanf("%d", &a[i]);

        for (int i = 0; i < m; i++) {
            scanf("%d%d%d", &q[i].type, &q[i].l, &q[i].r);
            q[i].l--, q[i].r--;
            if (q[i].type == 2) {
                scanf("%d", &q[i].k);
                for (int j = q[i].l; j <= q[i].r; j++)
                    addK[j] += q[i].k;
            }
            else {
                for (int j = q[i].l; j <= q[i].r; j++) {
                    cnt[j]++;
                    addSum += addK[j];
                }
            }
        }

        sort(a, a + n);
        sort(cnt, cnt + n);

        for (int i = 0; i < n; i++) {
            addSum += a[i] * cnt[i];
        }

        cout << addSum << endl;
        return 0;
    }
    ```

#### T5
猜数字游戏：系统随机生成一个 n(<=8) 位、不含重复数字的数字串，当玩家猜一个数字时，系统返回两个数字作为提示：a 表示位置和数字都正确的数目，b 表示位置不对但是数字存在的数目。现在给出 n 以及 m(~100) 次猜测的内容和结果（一个数字串以及对应的 a, b），求一个字典序最小且符合猜测结果的数字串。如果不存在，输出 `?`。

??? success "我的答案"
    就。。爆搜）也能过 比较友善）

    ```c++
    #include <iostream>
    #include <cstdio>
    #include <algorithm>
    using namespace std;

    int n, m;
    string str[105];
    int a[105], b[105];

    string s;

    bool check(int i) {
        int thisA = 0, thisB = 0;
        bool aEx[10] = {false}, bEx[10] = {false};
        for (int j = 0; j < n; j++) {
            if (str[i][j] == s[j])  thisA++;
            else aEx[str[i][j] - '0'] = true, bEx[s[j] - '0'] = true;
        }
        if (thisA != a[i])  return false;
        for (int j = 0; j < 10; j++)
            if (aEx[j] && bEx[j])
                thisB++;
        if (thisB != b[i])  return false;
        return true;
    }

    bool check() {
        //cout << s << endl;
        /*if (s[2] == '3') {
            cout << "1" << endl;
        }*/
        for (int i = 0; i < m; i++)
            if (!check(i))   return false;
        return true;
    }

    void gen(int level) {
        if (level == n) {
            if (check()) {
                cout << s << endl;
                exit(0);
            }
            return;
        }

        static bool used[10] = {false};
        for (int i = 0; i < 10; i++) {
            if (used[i])
                continue;

            if (s.size() <= level)
                s += (char)(i + '0');
            else s[level] = (char)(i + '0');
            used[i] = true;
            gen(level + 1);
            used[i] = false;
        }
    }

    int main() {
        cin >> n >> m;
        for (int i = 0; i < m; i++) {
            cin >> str[i] >> a[i] >> b[i];
        }
        gen(0);

        cout << "?" << endl;
        return 0;
    }
    ```

### 3.15 一面

这个面试官很客气诶，一直都称呼「您」，会各种肯定，并且在反问面试表现的时候表示「不用寻求我们的肯定」。

开始介绍了面试的流程，介绍了部门信息。让我进行自我介绍，并介绍自己的优势。

问了高中竞赛的情况。问了哪些场景会需要 C++ 的新特性，如何学习的。介绍了用到 lambda 和智能指针的场景。

问了项目经历里咸鱼雀的设计，主要解决什么问题，用了哪些方式。介绍了密码的加密存储、列表的权限问题、多人同时修改的支持、蓝绿发布和自动保存等。

问了 SQL 语句的执行步骤。

让写了两段代码，一段是二叉树的层序遍历，一段是多叉树的后序遍历。

反问阶段问了面试总体评价和技术栈。没听懂。

### 3.21 二面

自我介绍。提到专业，问了安全的三要素，我说不知道。问为什么选信安，我说怕计科进不去。

让介绍哪个项目最能体现水平，我介绍了解释器，介绍了闭包。问了为什么要有闭包。对闭包展开了讨论。

问解释器分几个部分。我怀疑他想问编译那一套，所以先介绍了编译器有几个部分
，然后介绍了 MUA 可以直接边解释边运行。

问了进程间通信有哪些方式。问了内存管理的机制，问了一个页的大小，为什么要这么大。问是不是了解操作系统中的 I/O 模型，例如多路复用。

问了 TCP 四次挥手的过程。

因为对我的解释器比较感兴趣，所以让写了一个自然数四则运算的处理程序。没有考虑括号。（但是我感觉没什么关系）））

??? success "我的答案"

    ```c++
    #include <iostream>
    #include <stack>
    using namespace std;

    int getInt(string &expr, int &index) {
        int currentInt = 0;
        bool isReadingInt = false;
        while (expr[index] >= '0' && expr[index] <= '9') {
            currentInt = currentInt * 10 + expr[index] - '0';
            isReadingInt = true;
            index++;
        }
        if (!isReadingInt)
            throw "Expected an integer, got " + expr[index];
        
        return currentInt;
    }

    /* 0 - add, 1 - sub, 2 - mul, 3- div*/
    int getOp(string &expr, int &index) {
        index++;
        switch (expr[index - 1]) {
            case '+':    return 0;
            case '-':    return 1;
            case '*':    return 2;
            case '/':    return 3;
            default:
                throw "Expected an operation, got " + expr[index];
        }
    }

    double calc(string &expr) {
        double result = 0, currentValue = 0;
        
        int index = 0;
        int lastOp = 0;
        
        while (index < expr.size()) {
            currentValue = getInt(expr, index);
            if (index == expr.size()) {
                result += (lastOp == 0 ? 1 : -1) * currentValue;
                break;
            }
            char currentOp = getOp(expr, index);
            if (currentOp <= 1) {
                result += (lastOp == 0 ? 1 : -1) * currentValue;
                lastOp = currentOp;
            }
            else {
                while (index < expr.size()) {
                    int temp = getInt(expr, index);
                    if (currentOp == 2)
                        currentValue *= temp;
                    else {
                        if (temp == 0) {
                            throw "Divided by 0!";
                        }
                        currentValue /= temp;
                    }
                    
                    if (index == expr.size()) {
                        result += (lastOp == 0 ? 1 : -1) * currentValue;
                        break;
                    }
                    
                    currentOp = getOp(expr, index);
                    if (currentOp <= 1)    {
                        result += (lastOp == 0 ? 1 : -1) * currentValue;
                        lastOp = currentOp;
                        break;
                    }
                }
            }
        }
        
        return result;
    }

    int main() {
        string expr;
        cin >> expr;
        try {
            cout << calc(expr) << endl;
        }
        catch (const char *ex) {
            cout << ex << endl;
        }
        return 0;
    }
    ```

    同时也介绍了用栈解决的思路。

问了实习时间。

---

3.21 的二面结束杳无音信，直到 4.25 给了 offer。