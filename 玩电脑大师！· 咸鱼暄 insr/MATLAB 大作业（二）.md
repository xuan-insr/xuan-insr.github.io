**作业报告**

3190105871   解雲暄<br />2020 年 9 月 20 日


## 作业内容及代码实现

- 读入一个灰度/真彩色图像，利用Haar小波进行编码，得到中间数据文件，存储
   - Harr.m 中读入，按层调用 HarrEncode 函数，以 8*8 为单位作 Harr 小波变换，存入 harrImg.mat。
   - 这里我们没有对边界进行处理。

- 针对编码后的中间存储文件，利用matlab内嵌的huffman编码函数进行二进制编码， 并存为压缩文件
   - 调用相关函数创建字典、编码后，存入 huffEnco.mat。
   - **由于浮点数比较存在误差，这里将浮点数转为整型后再进行编码。鉴于之前作 Harr 小波变换时是以 8*8 为单位，因此这里采取的取整方法为全部乘 8 转为 int16。这样可以确保不超范围且均精准转为整型。**

**

- 读取压缩文件，解码得到原始图像进行显示并对比压缩效率
   - 读取后解码、按层调用 HarrDecode 函数，以 8*8 为单位作 Harr 小波还原，并和原图展示对比。



## 压缩效率对比

##### 真彩色图像 12.png
![image.png](./assets/1600536303002-5102122a-34f4-4a81-8bfa-7861315af078.png)
![](https://cdn.nlark.com/yuque/__latex/46f2d013b667cdb6033d3ca335d90644.svg#card=math&code=%284107692%5Cdiv%208%29%5Cdiv%28543%5Ctimes958%5Ctimes3%29%5Capprox32.9%5C%25&height=20&width=300)


##### 真彩色图像 a.jpg
![image.png](./assets/1600537002437-d9bf2250-c9d2-4d65-b038-11080510d161.png)
![](https://cdn.nlark.com/yuque/__latex/86bbc7def9def0cb6d5278323a394146.svg#card=math&code=%282776972%5Cdiv8%29%5Cdiv%28276%5Ctimes579%5Ctimes3%29%5Capprox72.4%5C%25&height=20&width=300)


##### 灰度图像 moon2.tif
![image.png](./assets/1600537113176-a39284c5-eb55-4a74-a3cd-52fc4e5e965e.png)
![](https://cdn.nlark.com/yuque/__latex/fb280fe8a42523e89429934195ff215c.svg#card=math&code=%28946006%5Cdiv%208%29%5Cdiv%28540%5Ctimes466%29%5Capprox47.0%5C%25&height=20&width=263)


##### 灰度图像 gray.png
![image.png](./assets/1600537283898-1782fb06-131d-44dd-bccf-369c34d7001f.png)
![](https://cdn.nlark.com/yuque/__latex/118888aa7723f597a18422ffaed26fa8.svg#card=math&code=%283565493%5Cdiv8%29%5Cdiv%28899%5Ctimes728%29%5Capprox68.1%5C%25&height=20&width=271)
