# 蚂蚁 Java / C++

蚂蚁都是电话面试，但是有的时候会给个协作页面让写代码，比较迷惑

蚂蚁这里有点复杂……故事是，我在官网投了某个组，同时又在 98 上找了一位前辈的微信直接投了他所在的组。但是其实我在面试过程中并没有成功分清楚哪个是哪个QAQ

2.27 投了 Java 后端，3.2 投了 C++。最后的实习意向上的岗位名称是「蚂蚁集团-CTO线-数据与平台技术事业群-蚂蚁智能引擎与数据中台技术事业部-计算智能技术部  研发工程师C/C++」。

3.2 做了逻辑测试，限时的阅读理解、读图表、找规律啥的，好多来不及或者找不出来；个性测试和拼多多的是同一套题

因为分不清，所以下面就用 A 和 B 代替具体的组了，不确定有没有写错的地方。我猜 A 组是 C++ 那个。

### 3.10 一面 (A)

全程电话聊天，没用纸笔。面试官比较友善且也有点社恐。
开局自我介绍。说了专业、成绩排名、常用语言（分别说了相关的项目经历）。

问了大项目相关问题：人数、为什么会有这个项目、有什么挑战的地方。说了调用链的梳理、C++ 不支持的写法、内存管理之类的。

追问解决方法。主要说了智能指针防止内存泄露。

追问智能指针的劣势。不会，所以大概说了一下智能指针的实现思路。尝试说了劣势，只想到了统计引用数的时空开销，还说了使用不当会导致堆上的空间破坏（不过好像并没有。。）；查了一下好像也就查到循环引用啥的。

追问直接用 shared_ptr 和 make_ptr 的区别。说错了。参考这个 https://blog.csdn.net/misterdo/article/details/105844139  https://www.jianshu.com/p/03eea8262c11。

问了 C++ 的 virtual 以及实现。

追问构造函数和析构函数能不能是 virtual。刚开始说都不能，面试官让再想想。仔细分析了一下说对了。

问了 static 能不能和 const 一起。其实问的是这个 https://www.yuque.com/xianyuxuan/coding/diyz36。刚开始以为是问成员变量，后来才知道是成员函数。差点没说出来。

问了有什么常见的排序方法。说的不多……记不清））甚至忘了归并排序的名字，就大概描述了一下算法思路）

问数组、链表和集合有什么优缺点和应用场景。很奇怪，反正就说了数组、链表是线性表的实现方式，集合是一种更高级的容器。说了数组适合有序、随机访问，链表适合有序、经常插入删除，集合适合有重和顺序无关的数据。

问如果有一个装了一块 4G 内存卡的操作系统 32 位的机器，写一个程序可以访问的物理内存和虚拟内存分别是多少；然后问了如果内存是 128M 的话是多少。

然后问了，虚拟内存比物理内存大是怎么实现的。大概说了一下；面试官实际上想听“缺页中断”这个词，但是我并没有想起来））操作系统太差了qwq

问了进程间通信的手段。说了文件、公共内存和消息队列。查了一下其实还有信号量、管道、socket 之类的。

问 3 个线程，分别输出 ABC，如何设计使得 ABCABCABC 这样输出不乱。我的想法大概是这样：
```c++
int val = 0;
void job(char output) {
    while (true) {
        while (val + 'a' != output);
        print(val + 'a');
        val++;
    }
}
```
现在看一眼发现忘加锁了 乐

问淘宝有很多店铺，每个店铺有很多商品，现在给定某个店铺的某个商品，怎么访问到它。我说用一个 B+ 树存店铺，每个店铺用一个 B+ 树存商品。聊了一会儿发现面试官好像并不是想问我数据库的细节，而是想问如果一台机器存不下所有的数据，如何找到数据存在哪个机器上。我说将每个店铺的商品在哪台机器上存在存店铺的 B+ 树里面。后来面试官说其实可以找一个映射规则，比如前 10000 个数据存在第 1 台机器，10001~20000 在第 2 台之类的。

问了后面关于考研出国之类的规划。
反问阶段。问了我进去会做些啥，以及要求面试官给点面试反馈。没有得到什么有用的信息。

总共大概 50 分钟，面试官也挺耐心的，不错qwq

### 3.14 笔试

好多 Linux 题，我又没正经用过！上过 Linux 小学期的可能好一点？我不知道

选择题：

- 有一个名为 test 的文件，给了内容；让选出执行命令 `awk -F "_" '{print $1 " " $2}' test | sort -nk2 | tr -s " " "_"` 的结果
- 有 SQL 的题，让选运行结果，大概就是从视图里插入和删除的结果
- 有七根木棒，其长度分别为 8,8,3,5,7,2,10。若将两个木棒拼接在一起所需的体力为两根木棒的长度之和，则将七根木棒拼接成一根所需的最少体力为多少
- 给了个要求，让选正确的 chmod 指令
- 给了数据库描述，和一个需求，让选正确的 SQL 语句来建立满足需求的视图
- 让选哪些情况下会进程切换（不定项，时钟中断、trap、file open、page fault）
- 考 best fit
- 问 UDP 流的缺点
- 给了 IP 聚合后的地址，让选聚合前的地址可以是哪些

其他题没记，也不记得有没有编程题了。

### 3.17 一面 (B)

前面的不记得了。

问了堆是怎么建出来的，以及增加一个元素之后如何调整。

搜索引擎，有一堆文章，进行一次搜索，已知各个文章的相关度的情况下排出前 100 个结果。我的回答是维护一个 100 个元素的小根堆，保存前 100 个，复杂度是 $O(N\log 100)$ 的。

让介绍网络的分层结构。问了 TCP 和 UDP 的区别；回答了一堆，让用一两句话总结一下。问了如何保证某个数据包没收到的时候发送方能够知道这个事情并且需要重传。问有没有应用层协议用 UDP 的。

写代码。用基础数据结构实现一个队列的功能，队列一般对外提供 pop push 的方法

??? success "我的答案"
    循环数组实现队列，并用 vector 的思路实现动态调整。

    ```c++
    class Queue {
    private:
        int *data;
        int front;
        int tail;
        int capacity;
        int size{0};
    public:
        Queue(int capa = 16) {
            capacity = capa;
            data = new int[capacity];
            front = 0;
            tail = capacity - 1;  // empty
        }
        int pop() {
            if (size == 0) {
                throw "The queue is empty";
            }
            size--;
            int value = data[front];
            front = (front + 1) % capacity;
            return value;
        }
        void push(int value) {
            if (size == capacity) {
                int *newData = new int[capacity * 2];
                for (int i = 0; i < capacity; i++) {
                    newData[i] = data[(front + i) % capacity];
                }

                newData[capacity] = value;
                front = 0;
                tail = capacity;

                size++;
                capacity *= 2;
                delete []data;
                data = newData;
            }
            else {
                tail = (tail + 1) % capacity;
                data[tail] = value;
                size++;
            }
        }
    };
    ```

    好像忘记写析构函数了）））

给一个多叉树，父节点和子节点之间有条边，边有长度，求最长的一条根到叶子的路径 

??? success "我的答案"
    ```c++
    class TreeNode {
    public:
        int ID;
        TreeNode *firstChild;
        TreeNode *nextSibling;
        int distanceToFather;
        
        TreeNode *farthestChild{nullptr};
        int distanceToFarthestChild{0};
    };

    void doFindLongestPath(TreeNode *root) {
        if (!root || !root->firstChild)  return;

        int distanceToFarthestChild = 0;
        TreeNode *farthestChild = nullptr;

        TreeNode *tmp = root->firstChild;
        while (tmp) {
            doFindLongestPath(tmp);
            if (tmp->distanceToFather + tmp->distanceToFarthestChild > distanceToFarthestChild) {
                distanceToFarthestChild = tmp->distanceToFather + tmp->distanceToFarthestChild;
                farthestChild = tmp;
            }
            tmp = tmp->nextSibling;
        }

        root->distanceToFarthestChild = distanceToFarthestChild ;
        root->farthestChild = farthestChild;
    }

    void findLongestPath(TreeNode *root) {
        doFindLongestPath(root);
        std::cout << "The length of the longest path is " << root->distanceToFarthestChild << std::endl
                << "The path is: ";
        while (root) {
            std::cout << root->ID << "->";
            root = root->farthestChild;
        }
    }
    ```

这次的面试官感觉没有非常厉害，也有一些比较迷惑的发言。

### 3.10 二面 (A)

这场只有 30 min。

自我介绍。问了未来规划，是不是打算保研。

问了计算机相关的课程哪门学的最好。

问了用 C / C++ 时比较常见哪些问题，如何解决。回答了递归和循环的边界问题，比较习惯通过测试而非静态查代码。

问了知不知道智能指针。介绍了 shared_ptr。

问了 C++ 函数返回一个地址，这个地址是物理地址还是虚拟地址。

如果一段代码形如 `malloc(100); while(1);`，这个时候操作系统已经把内存分配给进程了吗？考 lazy allocation，但是当时我不会。

让解释 page fault。

让解释 C++ 中多态的概念。

让介绍一个印象最深刻的、对编程能力提高最高的项目。做了什么事情、遇到什么困难，如何解决的。

### 3.23 HR 面 (A)

这部分有大概 40 min。

介绍了一下岗位的基本信息。

让自我介绍、自我评价。问了有没有社团经历、竞赛经历，为什么没有竞赛经历。问了有没有论文和专利。问了毕设的情况。

问了个人规划。回答了保研和就业两手准备。追问了就业方面考虑什么样的公司和岗位，回答了实习本身是为了找方向。问了投了哪些其他公司和岗位。

问了蚂蚁对于我的吸引力在哪里。回答了去语雀大会的时候看到大家的氛围还不错；蚂蚁本身技术比较成熟，能够更好地提升自己。问了对工作内容的了解和期望。

问了如果其他公司也给了 offer 怎么选。回答了很重要的基础条件是实习的时间和地点，具体的内容不是特别重要。

问为什么喜欢开发和写代码。回答了比较喜欢有逻辑的工作，对于写代码比较熟悉，比大多数同龄人经验丰富，同时比较有成就感。追问了丰富经验的过程可能是比较艰难和枯燥的，是什么支撑我坚持下来的。

问了这几年最高点是什么时候，发生了什么事。问了大学学习了各个专业课，涉及各个领域，其中最扎实的领域是什么。问了学习过程中通过哪些方式实现知识和技术的积累。

问喜欢压力大一点还是比较平缓可控的环境。回答了喜欢时间安排紧一点但是工作难度不太大的安排。

问有没有面对过同时多条任务并行而且都比较有挑战的，是怎么解决的。

问了这几年最低点是什么时候，发生了什么事，怎么走出来的。问了如何评价现在的状态。

问了有什么样的合作项目和在其中的角色、产出。

设想一下工作中的哪些场景可以吸引我。

---

4.14 收到了录用的实习意向书，19 号拒掉了。

## 9.21 秋招面试

之前找的前辈问我要不要面秋招，就面了一下。

问了暑期实习是怎么选择的。回答了传统互联网可以通过周围的人了解，但是周围从事量化行业的人不多，所以只能自己去体验一下。更重要的原因是和推荐我的同学是比较好的学习合作伙伴，希望趁这个机会多交流一下。

问了实习的时间段和感受。回答了确实能学到很多东西，需要独当一面，成长很快；不过量化做的很多内容是比较极致的细分优化，这种技术在传统互联网应用程度不高，没办法给自己留退路。另一方面是量化行业更有可能收到国家监管因此稳定性欠佳。

让介绍了实习期间做的一个具体的工作。

问关于工作更看重什么，如果很多公司都给发 offer，大致的倾向是什么。回答了希望培养的能力能够更有竞争力和市场。追问我如何去判断哪个公司能让我更有竞争力。我回答更看重对相应领域未来发展的期望，例如我因为编程语言应用比较窄所以没有选择保研。

问了如果蚂蚁的方向比较好，但是给的 offer 比别的公司少 5k，我怎么选。我回答虽然最后的目的都是赚钱，但是最开始更希望有一个好的平台和方向。

问了我意愿中有哪些方向是我觉得好的方向。我回答不出来，所以说我觉得互联网需要的技术都差不太多。他追问那既然差不太多怎么选择呢？我答不出来，哑口无言，开始扯比较关心能够拿到什么样的项目、成长速度怎么样。

作为总结我给了个排序，大方向 > 项目和成长 > 薪资。然后追问了大概做什么事情。

（现在想来不应该绕那么多的。就直接说谁给的多去那就好了。）

---

然后就没消息了，确实自己再回去看的时候也觉得自己诚意太不足了。乐）