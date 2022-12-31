# 拼多多 服务端

98 看到的。第一个投的，也没想去，主要是想积攒一点笔试和面试经验。

2.26 投的，2.27 做了个性测试，题很多很烦人。

### 3.6 笔试

安排了 3.6 的笔试，120 分钟，4 个题，可以用自己的 IDE，是在牛客网进行的。

T1 5分钟，T2 10分钟，T4 写了 45 分钟，T3 没做出来，剩十分钟的时候不想做了。

#### T1
字符串编码，输入形如 `aaaaaaaaaaBBBCddddDDDaa`，输出形如 `10a3B1C4d3D2a`。

??? success "我的答案"
    ```c++
    #include <iostream>
    #include <vector>
    #include <string>

    using namespace std;

    int main() {
        string s;
        cin >> s;
        vector<pair<int, char>> v;
        char last = s[0];
        int cnt = 0;
        for (auto c : s) {
            if (c == last)  cnt++;
            else {
                v.push_back(make_pair(cnt, last));
                last = c;
                cnt = 1;
            }
        }
        if (cnt)    v.push_back(make_pair(cnt, last));

        for (auto &i : v)
            cout << i.first << i.second;

        return 0;
    }
    ```

#### T2
给定一个字符串 S，可以做两种操作之一：S + R(S) 或 R(S) + S，其中 + 是字符串拼接，R(S) 是字符串逆转。求给定 S 和操作次数 k，S 恰好经过 k 次操作后可能的结果数目。输入 T(~100) 表示询问组数，每组询问包含 k, l, str，其中 k(0~多少忘了) 表示操作次数，l 表示字符串长度，str 是字符串。

例如 aabb 经过一次变换可以变成 aabbbbaa 或者 bbaaaabb，再经过一次变换可以变成 aabbbbaaaabbbbaa 或者 bbaaaabbbbaaaabb，因此 k = 2, str = aabb 时应当输出 2。

题目保证结果不超过 1,000,000,000。

??? success "我的答案"
    容易证明 R(R(S) + S) = R(S) + S, R(S + R(S)) = S + R(S), 
    所以只要不是回文串而且变过那就是 2

    或者说，S + R(S) 和 R(S) + S 都是回文串，而对于任意回文串 T，R(T) = T

    ```c++
    #include <iostream>
    #include <vector>
    #include <string>

    using namespace std;

    bool check(string &str) {
        int left = 0, right = str.size() - 1;
        while (left < right) {
            if (str[left] != str[right])
                return false;
            left++;
            right--;
        }
        return true;
    }

    int main() {
        int t, k, l;
        string str;

        cin >> t;
        while (t--) {
            cin >> k >> l >> str;
            if (!k || check(str))      cout << 1 << endl;
            else                        cout << 2 << endl;
        }
        return 0;
    }
    ```

#### T3
多多和皮皮虾打架，分别有 N(~100000) 和 M(~100000) 支军队，每支军队有攻击力 a(~10000) 和防御力 d(~10000)。每次双方各派出一支军队交战，如果一方攻击大于等于对方防御，则该方攻击成功，对方防御失败。因此每次交战的结果可能有 4 种。军队不能重复使用。

现在要求寻找一种交战策略，使得多多在攻击成功皮皮虾的所有军队的前提下，有最大可能的防御成功次数，输出这个值。如果不存在交战策略使得多多能攻击成功皮皮虾的所有军队，输出 -1。

??? quote "回顾"
    理解错题意了，所以只得了 50% 的分）不想看了 反正是贪心

    没有地方提交，所以不想自己做了，做了也不知道对不对 XD

#### T4
有 T(~100) 组询问，每组询问包含 2 行，每行 6 个数，分别表示一个骰子的上、下、左、右、前、后四个面上的点数。我们每次操作可以对骰子做 4 种旋转之一：

- 左、右不动，向上方旋转一次，即原来的前面变成上面，下面变成前面等
- 这种旋转反过来，即左、右不动，原来的上面变成前面等
- 前、后不动，向右边旋转一次，即原来的上面变成右面等
- 这种旋转反过来，即前、后不动，原来的右面变成上面等

对于每组询问，找到操作数最小的方案使得输入的两个骰子变成一样的，输出这个最小的操作数。如果不可能变成一样的，则输出 -1。

??? success "我的答案"
    一个骰子只有 24 种可能的位置，即 6 个不同的点数向上的情况下，每种情况前后左右可以转 4 次，总共 24 * 6 种。因此可以 BFS。

    注意到根据两个相邻面的点数就可以唯一确定一个骰子的位置状态，因此我们用 visited[7][7] （其实可以用 [6][6]）记录一种状态是否被考虑过。

    没有太注意一些优化，因为能过，没必要）

    ```c++
    #include <iostream>
    #include <vector>
    #include <queue>

    using namespace std;

    int a[6], b[6];

    bool isEqual(vector<int> &v) {
        for (int i = 0; i < 6; i++)
            if (v[i] != b[i])   return false;
        return true;
    }

    const int ro[4][6] = {{4, 5, 2, 3, 1, 0},
                        {5, 4, 2, 3, 0, 1},
                        {2, 3, 1, 0, 4, 5},
                        {3, 2, 0, 1, 4, 5}};

    int solve() {
        vector<int> v;
        queue<pair<int, vector<int>>> q;
        for (auto i : a)    v.push_back(i);
        q.push(make_pair(0, v));
        
        bool visited[7][7] = {false};    // 1, 2
        visited[v[1]][v[2]] = true;

        while (!q.empty()) {
            if (isEqual(q.front().second))      return q.front().first;
            for (const auto & i : ro) {
                vector<int> tmp;
                for (auto j : i)
                    tmp.push_back(q.front().second[j]);
                if (visited[tmp[1]][tmp[2]])    continue;
                visited[tmp[1]][tmp[2]] = true;
                q.push(make_pair(q.front().first + 1, tmp));
            }
            q.pop();
        }

        return -1;
    }

    int main() {
        int t;
        cin >> t;
        while (t--) {
            for (int & i : a)     cin >> i;
            for (int & i : b)     cin >> i;
            cout << solve() << endl;
        }
        return 0;
    }
    ```

### 3.14 一面
面试官迟到了快五分钟，非常的神奇。

刚开始是一个自我介绍。

让介绍一个项目，以及学习到的东西。讲了去年年底到今年年初做的化工模拟项目。（面试官极度纠结这个项目为什么要做、为什么要用 Qt、这些化学反应的模拟到底是怎么实现的，感觉他不太清醒。）

追问：假设需要增加一种反应的模拟，应该怎么改代码。我理解他应该是想问继承之类的东西，就说新增一种 reactor 就从基类新派生一个对象就行了。

问 C++ 和别的语言有什么区别。很新奇的问题，大概说了 C++ 没有单根结构、C++ 比别的高级语言更自由一些，所以可以做更多的事，对应地也需要更多安全的关注。

问了虚函数的实现。追问了很多；感觉说的并不是非常的到位，回头再学一下。

问了 override 和 overload 的区别。

问了动态链接的实现。不会，猜了一下。

让写了一个题，给一个字符串表示的整数，返回一个 int，内容为字符串表示的整数。

??? success "我的解法"
    发现不太会用 exception。

    ```c++
    #include <iostream>

    int str2int(const std::string &str) {
        int i = 0, result = 0;
        
        while (i < str.size() && (str[i] == ' ' || str[i] == '\t' || str[i] == '\n'))
            i++;
            
        if (i == str.size()) {
            throw "The input is empty";
        }
        
        int negFlag = 1;
        if (str[i] == '-')  {
            negFlag = -1;
            i++;
        }
            
        while (str[i] >= '0' && str[i] <= '9') {
            result = result * 10 + str[i] - '0';
            if (result < 0) {
                throw "The integer is too large";
            }
            
            i++;
            if (i == str.size()) {
                return negFlag * result;
            }
        }
        
        while (i < str.size() && (str[i] == ' ' || str[i] == '\t' || str[i] == '\n'))
            i++;
            
        if (i == str.size()) {
            return negFlag * result;
        }
        
        throw "The string is not an integer";
        
        return 0;
    }

    int main() {
        std::string cases[] = {"0", "123", "-123", "1.1", "  12345  ", "  -123456   ",
            "11111111111111111111111111", "-11111111111111111111111111"};
        
        for (auto &str : cases) {
            try {
                int result = str2int(str);
                std::cout << result << std::endl;
            } catch (const char *ex) {
                std::cout << ex << std::endl;
            }
        }
        
        return 0;
    }
    ```

### 3.20 二面

面试官把我忘了，换了一个时间。品位和素养都很差。

刚开始还是自我介绍。

问了知道什么排序算法。问了归并算法的原理，让写了一下。

??? success "我的解法"
    确实没写过QAQ

    ```c++
    void sort(int array[], int n) {
        if (n == 1) return;
        
        int mid = n / 2;
        sort(array, mid);
        sort(array + mid, n - mid);
        
        int i = 0, j = mid;
        
        std::vector<int> temp;
        while (i < mid && j < n) {
            if (array[i] < array[j])
                temp.push_back(i++);
            else
                temp.push_back(j++);
        }
        while (i < mid)
            temp.push_back(i++);
        while (j < n)
            temp.push_back(j++);
            
        for (int k = 0; k < n; k++)
            array[k] = temp[k];
    }
    ```

问对 SQL 熟不熟悉，我说基本知道，不保证熟悉，他说那就先放后面一点。

问对 C++ 或者 Java 有没有稍微透彻了解一点的。我说对 C 比较了解，问他对了解的要求是什么样的。他举例问我 C++ 的虚函数表是怎么实现的，追问了虚函数表是和类绑定的还是和对象绑定的。

问是不是了解智能指针。我介绍了 shared_ptr，因为别的没用过。

问学没学过操作系统。问了线程的同步是用来做什么的。问了操作系统有哪些对象可以用来实现同步，我说我没写过多线程。

问对 Java 了解程度怎么样，问知不知道 Java 的 GC，我说不知道。

问 C++ 的 `delete` 和 `delete[]` 的区别。他声称是有没有调用析构函数的区别。但是他说的好像是错的，不配对的使用就是 UB。

### 3.22 三面（技术主管面）

问了前两面的面试官让写了什么代码，但是我忘了。

给了二叉树的结构，让写 LCA，但是我不会。我写了 `find_path(node)` 用 dfs 找 root 到 node 的 path，然后用 path 比较。

让讲了一下自己写过的代码，让讲了一下遇到了哪些问题和难点，如何解决的。讲了 MUA 解释器里实现闭包。讨论了一些但是好像没有什么营养。然后介绍了化工的那个工程，难点在于在大量多态的环境下梳理调用链、内存泄漏、函数式写法，我们使用了 debug 梳理调用链，用智能指针解决内存泄漏，用 lambda 当一等函数。

问了为什么要用多态。问有没有做过写接口给别人用的需求，如果有的话可能会对多态理解深刻一点。

问有没有用过静态链接库和动态链接库，我说没用过。

问对网络或者操作系统有没有学的好一点的。我说了网络。他问网络的分层设计是为什么要这么设计的。我大概介绍了一下这几层是干什么的。

问了和别的同学相比的优点和弱项。我介绍了弱项是，虽然在信息安全但是对安全没有太大兴趣，另外没有特别专精的项目。优势是，基础知识比较扎实，因为成绩高、有笔记、带朋辈辅学，另外编程方面比大家的经验丰富。

问了绩点，问了是哪里人，为什么会选择来浙大。

### 3.31 HR 面

简单的自我介绍。介绍了排名、个人博客、朋辈辅学、项目经历、志愿者、社会工作。

问了博客的内容和动机。问了高中 OI 是否有加分和高报选择。问了成绩，讲了大一状态不太好所以成绩没有很好。问了大一为什么没有很好，解释了没有压力、不感兴趣之类的问题。

问了对于实习的期望。回答了希望体验工作、积累实际经验、找到发展方向。问了未来的规划。回答了对编程语言和编译器的兴趣，以及倾向于保研；如果没有找到方向或者没保研就会选择不读。

问了暑假合理的时间，回答了只能在暑假开始实习。问了家庭工作情况和对我未来的期望。问了有没有对象（没有 TAT）。问了在大学主要的兴趣爱好。

问了不了解拼多多的工作时间，并且自称工作强度是比较大的。给了介绍。研发岗是 11~20 点打卡，其中 12~13, 18~19 是午餐晚餐时间，晚上 20 点之后通常都有加班。每周一般都是 6 天，实习生至少要呆 5 天。问能不能接受。我说还好，自己平常学习也可能有这个时间。

问了身边的同学如何评价我。问了成长过程中最沮丧的事情是什么，最近有什么事情很影响情绪；回答了没什么东西很影响情绪。问有没有什么事情是很想做到但是最终没有成功的；回答了没有什么事情很想做到。

问了还投了哪些公司，回答投了美团和华为，美团二面完不理了，华为笔试完不理了，可能挂了。

问了校内论坛和网上存在对于拼多多很多方面的评价，我怎么看。我回答可能大家主要的不满是营销手段，但是营销手段如何和我在这里面做技术没什么关系。另外也不满是工作强度，我认为比较年轻的时候通过这种方式快速成长也是可以接受的。

反问阶段。问了如果七月中旬才能入职的话可不可以，回答虽然有点晚但是月底之前去就不会错过培训。问了培训是什么，回答主要是公司文化、公司制度。问了对于时长的要求，回答至少两个月，多数人会在三个人最右。问了如果某个组不太适合，有没有机会调整，回答分配好了之后基本没有。问了是否有转正机会，回答如果满两个月之后就有机会，由主管评估。

---

然后就挂了 XD