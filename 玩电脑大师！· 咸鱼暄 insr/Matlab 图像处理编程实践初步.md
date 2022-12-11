
## 开始之前
等闲下来了再整理笔记 QAQ

- MATLAB: MATrix + LABoratory
- 脚本语言
- 时间

理论 9:00 - 11:00<br />实验 14:00 - 16:00

- 成绩

Lab        10% * 6 = 60%<br />Project   20% * 2 = 40%

- ftp

ftp://10.214.160.119<br />ftpuser<br />10214160119

---


### 基础知识

#### 数值
十进制数：109  -35.9<br />科学计数法：10e-10  1.36E+7  12e13 （e 和 E 不区分）<br />虚数：12i  2+13.2j （i 和 j 作为虚数标记）

#### 数据显示格式
关键字 format

**

#### 变量


### 矩阵

#### 创建矩阵

   - 直接输入 

## 

### 图像处理基础

#### 一些术语


#### Hough 变换提取直线

##### 直角坐标中的 Hough 变换
将 xOy 中的一条直线 ![](./assets/1598495757484-136adaf1-5846-4f2e-adb2-d20f5237e2d2.png)

##### 利用 Hough 变换寻找最长直线
建立二维数组 ![](./assets/1598495746797-aece5522-b968-4e4f-b4fd-5e1ebdf98592.png)

##### 极坐标中的 Hough 变换
将直角坐标 xOy 平面中的一条直线 ![](./assets/1598495571296-eabbbb16-2b83-4bd5-a017-a5d76a6d28ef.png)

##### MATLAB 中的相关函数
`[[H,theta,rho] = hough(BW,Name,Value,...)](https://ww2.mathworks.cn/help/images/ref/hough.html?s_tid=srchtitle#d120e14425)`


## 

