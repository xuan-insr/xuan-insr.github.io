解雲暄 3190105871

## 4 使用惯性传感器

### 4.1 环境配置

- Windows 10
- Arduino 1.8.19
   - ![image.png](./assets/1651106111282-fcd268fa-6fb4-472b-bdf9-3d6fd35f521c.png)


### 4.2 Arduino
Arduino 的代码大概是这样的：
```c
void setup() {
  // 初始化，只运行一次
}

void loop() {
  // 主要内容，初始化后循环执行
}
```
	对于 BMI160，控制寄存器包括：

- 寄存器名：CMD
   - 寄存器地址：0x7e 
   - 默认值：0x00。
   - 该寄存器可以读也可以写。
   - 我们通过向该地址写⼊不同的值来控制加速度或者陀螺仪的⼯作模式 
      - 0x11：通过写⼊该命令值，可以使加速度模块切换到正常⼯作模式 
      - 0x15：通过写⼊该命令值，可以使陀螺仪模块切换到正常⼯作模式 
- 寄存器名：ACC_CONF 
   - 寄存器地址：0x40 
   - 设置加速度传感器的输出数据速率，带宽，以及加速度传感器的读模式 
- 寄存器名：GYR_CONF 
   - 寄存器地址：0x42 
   - 设置惯性传感器的输出数据速率，带宽，以及惯性传感器的读模式  


### 4.3 补全代码

#### 4.3.1 GYRO | 陀螺仪
补全寄存器：
```c
#define ACC_CONF 0x40
#define GYR_CONF 0x42
    writeReg(CMD, 0x15);
    writeReg(ACC_CONF, 0x29);  // TODO, acc_conf register
    writeReg(GYR_CONF, 0x29);  // TODO, gyro_conf register
```
这里 CMD 寄存器的值写入为 0x15，使得陀螺仪模块切换到正常⼯作模式。

我们将串口的波特率设为 9600，这需要与后面串口监视器的波特率一致：<br />`Serial.begin(9600);   // TODO, Baud rate`

打印 x, y, z：
```c
/* TODO: print the x,y,z */
  Serial.print("[GYRO]");
  Serial.print(" X="); Serial.print(x);
  Serial.print(" Y="); Serial.print(y);
  Serial.print(" Z="); Serial.print(z);
  Serial.print("\n");
```

尝试编译烧录，在串口监视器可以读取到数据：
![image.png](./assets/1651109891512-af6d9dae-db60-41a8-88f6-2b7e06b0eee7.png)


#### 4.3.2 ACC | 加速度
补全寄存器：
```c
#define ACC_CONF 0x40
#define GYR_CONF 0x42
    writeReg(CMD, 0x11);
    writeReg(ACC_CONF,0x29);  // TODO, acc_conf register
    writeReg(GYR_CONF,0x29);  // TODO, gyro_conf register
```
这里 CMD 寄存器的值写入为 0x11，使得加速度模块切换到正常⼯作模式。

我们同样将串口的波特率设为 9600，这需要与后面串口监视器的波特率一致：<br />`Serial.begin(9600);   // TODO, Baud rate`

打印 x, y, z：
```c
/* TODO: print the x,y,z */
  Serial.print("[ACC]");
  Serial.print(" X="); Serial.print(acc_x);
  Serial.print(" Y="); Serial.print(acc_y);
  Serial.print(" Z="); Serial.print(acc_z);
  Serial.print("\n");
```

尝试编译烧录，在串口监视器可以读取到数据：
![image.png](./assets/1651110226759-2279cbd3-6dc0-4b69-8ad5-1f73eefc753e.png)


## 5 使用超声波干扰传感器  
我们通过 MATLAB 代码生成不同频率的超声波：
```matlab
Fs = 48000;
t = 1:1/Fs:5;
for f = 18000:1000:24000
    y = cos(2 * pi * f * t);
    name = 'ultrasound' + string(f) + '.wav';
    audiowrite(name,y,Fs);
end
```
生成的结果为：
![image.png](./assets/1651405280503-360db1ce-3bc7-4be1-a64b-f1bdfa8a5e18.png)
其中文件名指示了不同超声波文件的频率信息。

我们分别对比不播放超声波、播放不同频率的超声波时陀螺仪和加速度的数据信息。由于篇幅限制，我们只分别展示 3 种不同情况的结果：

### 5.1 陀螺仪

#### 5.1.1 不播放超声波
![image.png](./assets/1651110032881-d9f85f15-c0ef-4dad-b4ab-cfa33acb1875.png)

#### 5.1.2 播放频率为 18000Hz 的声波信号

#### ![image.png](./assets/1651110041943-b3833427-278b-441a-995d-55313c42547b.png)

#### 5.1.3 播放频率为 22000Hz 的声波信号
![image.png](./assets/1651110049251-ac22985b-34b8-449e-b6a4-f05d33e5796a.png)

### 5.2 加速度

#### 5.2.1 不播放超声波
![image.png](./assets/1651110226759-2279cbd3-6dc0-4b69-8ad5-1f73eefc753e.png)

#### 5.2.2 播放频率为 18000 Hz 的声波信号![image.png](./assets/1651110243572-8f6a90bb-30cf-4d3a-bb13-29cd507a05b0.png)

#### 5.2.3 播放频率为 22000 Hz 的声波信号![image.png](./assets/1651110265168-67ec5dfc-d286-4ec9-bfc5-c39cf9776718.png)

### 5.3 结果分析
比较遗憾的是，从上述结果以及其他的一些尝试结果中发现，我们的尝试效果并不显著；但与其他同学进行交流后发现，大家也均未得到比较明显的效果。<br />分析来说，出现这样的情况的主要可能原因是超声波的播放问题。在大家的实验过程中我们也注意到，不同的同学使用各自的电脑、手机等设备播放出的同一个频率的声波文件效果千差万别，这可能是因为设备厂商并不理应支持比较高频率的声波播放和保真。因为这样的原因，我们比较难保证超声波是否能正确播放；以及人耳并不都能听到这些频率的声音，也并没有专业设备用来检测，因此我们甚至无法得知这些声波信息是否真的被播放了。<br />另外，一些其他的因素可能也会对实验结果产生影响。例如，我们的实验板上，惯性传感器是一个外置的、用线连接的器件，线本身带来的振动导致的陀螺仪和加速度的变化甚至有可能大于超声波信息预期带来的影响。其他的问题包括电脑的风扇等其他声音和振动源带来的影响也是显著的。<br />综上所述，虽然我们能够理解超声波对传感器干扰效果的理论可能，但囿于设备限制，我们并没有能够成功复现出这种干扰。
