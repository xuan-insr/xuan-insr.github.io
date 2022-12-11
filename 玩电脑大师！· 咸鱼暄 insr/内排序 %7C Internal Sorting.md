
#### 排序的稳定性
稳定性是指相等的元素经过排序之后相对顺序是否发生了改变。如果没有，我们称这种排序方式是稳定 (stable) 的。


#### 基于比较的排序算法的复杂度下界


#### 插入排序 | Insertion Sort
插入排序将数列划分为“已排序的”和“未排序的”两部分，每次从“未排序的”元素中选择一个插入到“已排序的”元素中的正确位置。
```c
for (int i = 1; i < N; i++) {
    int temp = a[i];
    for (int j = i; j > 0 && a[j-1] > temp; j--)
        a[j] = a[j-1];
    a[j] = temp;
}
```
插入排序的最坏情况时间复杂度和平均情况时间复杂度都为 ![](https://cdn.nlark.com/yuque/__latex/8e9c5fee65a4f32abccd0e83ff203e39.svg#card=math&code=O%28N%5E2%29&height=23&width=49)，但其在数列几乎有序时效率很高，在数列是完全有序的情况下时间复杂度是 ![](https://cdn.nlark.com/yuque/__latex/33697ce7dfa48ba80980d298c8089378.svg#card=math&code=O%28N%29&height=20&width=41) 的。插入排序是稳定排序。<br />最坏和最好情况下的时间复杂度是显然的。下面我们简单分析平均情况下插入排序的时间复杂度：

:::info
我们用 ![](https://cdn.nlark.com/yuque/__latex/7034fdb35b4713878ff726d1748f70e2.svg#card=math&code=A%28k%29&height=20&width=34) 表示待排序数列中的第 ![](https://cdn.nlark.com/yuque/__latex/8ce4b16b22b58894aa86c421e8759df3.svg#card=math&code=k&height=16&width=8) 项（从 1 开始），那么 ![](https://cdn.nlark.com/yuque/__latex/7034fdb35b4713878ff726d1748f70e2.svg#card=math&code=A%28k%29&height=20&width=34) 的正确位置 ![](https://cdn.nlark.com/yuque/__latex/37776ef04e8a6a01d5ffe1dcf1322214.svg#card=math&code=p_k&height=14&width=16) 可能是 ![](https://cdn.nlark.com/yuque/__latex/8210d2c88b9a9ca6f3a86f4d63ca9d60.svg#card=math&code=1%2C%202%2C%20%5Ccdots%2C%20k&height=18&width=70)  中的任一个，且概率均为 ![](https://cdn.nlark.com/yuque/__latex/e80affdefa19b956154d5d5e53557d3b.svg#card=math&code=%5Ccfrac%201k&height=52&width=14)。则找到正确位置需要交换 ![](https://cdn.nlark.com/yuque/__latex/3aa816bc07d5be1710bb8535c3163e7c.svg#card=math&code=k-p_k%20%2B%201&height=18&width=74) 次，期望为 ![](https://cdn.nlark.com/yuque/__latex/e1e26b6eb1f7fd87d27ae7394d482a2a.svg#card=math&code=k-%5Ccfrac%20%7Bk%2B1%7D2%3D%5Ccfrac%20%7Bk%2B1%7D2&height=52&width=139)。因此将整个数列进行排序的期望比较次数为 ![](https://cdn.nlark.com/yuque/__latex/8cfa12a26615dbece9d13c8646b853fb.svg#card=math&code=%5Csum%5EN_%7Bk%3D1%7D%5Ccfrac%20%7Bk%2B1%7D2%20%3D%20%5Ccfrac%20%7BN%5E2%2B3N%7D4%20&height=53&width=166)，因此均摊复杂度为 ![](https://cdn.nlark.com/yuque/__latex/8e9c5fee65a4f32abccd0e83ff203e39.svg#card=math&code=O%28N%5E2%29&height=23&width=49)。
:::


#### 选择排序 | Selection Sort
对一组数据，每次将其中的一个数据放在它最终要放的位置。第一步是找到整个数据中最小的数据并把它放在最终要放的第一个位置上，第二步是在剩下的数据中找最小的数据并把它放在第二个位置上。对所有数据重复这个过程，最终将得到按从小到大顺序排列的一组数据。<br />复杂度：![](https://cdn.nlark.com/yuque/__latex/9f84a66d88d24c3b1bc91df5b5346a13.svg#card=math&code=O%28n%5E2%29&height=23&width=43)。选择排序不是稳定排序。


#### 冒泡排序 | Bubble Sort
以升序为例，冒泡排序每次检查相邻两个元素，如果前面的元素大于后面的元素，就将相邻两个元素交换。当没有相邻的元素需要交换时，排序就完成了。<br />经过 i 次扫描后，数列的末尾 i 项必然是最大的 i 项，因此最多需要扫描 n - 1 遍数组就能完成排序。<br />在序列完全有序时，该算法只需遍历一遍数组，不用执行任何交换操作，时间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/7ba55e7c64a9405a0b39a1107e90ca94.svg#card=math&code=O%28n%29&height=20&width=36) 。在最坏情况下，冒泡排序要执行 ![](https://cdn.nlark.com/yuque/__latex/15c09a929654f7dca65a774f4b6fda6b.svg#card=math&code=%5Cfrac%7Bn%28n-1%29%7D%7B2%7D&height=41&width=68) 次交换操作，时间复杂度为 ![](https://cdn.nlark.com/yuque/__latex/9f84a66d88d24c3b1bc91df5b5346a13.svg#card=math&code=O%28n%5E2%29&height=23&width=43) 。在平均情况下，冒泡排序的时间复杂度也是 ![](https://cdn.nlark.com/yuque/__latex/9f84a66d88d24c3b1bc91df5b5346a13.svg#card=math&code=O%28n%5E2%29&height=23&width=43) 。冒泡排序是稳定排序。


#### 希尔排序 | Shellsort


#### 堆排序 | Heapsort


#### 归并排序 | Merge Sort
归并排序采用了分治思想。
