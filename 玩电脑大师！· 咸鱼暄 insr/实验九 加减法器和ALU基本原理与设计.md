学生姓名：解雲暄                         专业：信息安全                           学号：3190105871      <br />同组学生姓名：郭长洁                  指导老师：蔡铭   <br />实验地点：紫金港东四 - 509         实验日期：2020 年 11 月 23 日


## 1 实验原理

### 1.1 多位串行进位加减法器
实验 8 中，我们设计了全加器。在其基础上实现减法器，只需要对减数补码求负，与被减数相加即可。即如果是加法，我们正常使用加法器；如果是减法，我们求减数相反数之后再作加法。<br />用“异或”门控制求反，低位进位 C0 为 1：
![image.png](./assets/1606727063524-14079539-fe2f-4368-967c-192b4c6105ea.png)
![image.png](./assets/1606727077290-3fd19418-8058-4a20-9a8f-ab41636fa068.png)

据此，我们可以利用 Adder1b 设计出 AddSub1b：
![image.png](./assets/1606727111991-fba45d9a-3c08-4daf-adf2-c834421f4c2c.png)
↓
![image.png](./assets/1606727120524-ddb4fe3e-8ce6-44fa-8f82-86598d8917cc.png)
从而设计出 4 位加减法器：
![image.png](./assets/1606727185778-6c2c3185-65d5-4207-9369-1483952f9419.png)


### 1.2 4 位 ALU
结合先前实验设计的各种模块，我们可以设计出 4 位 ALU：
![image.png](./assets/1606727248821-b9fd63e7-aa43-4681-a695-6db5ff61d4e1.png)


## 2 实验内容与步骤

### 2.1 原理图方式设计 4 位加减法器
新建工程 MyALU，新建 Schematic 文件 AddSub1b，绘制原理图如下：
![image.png](./assets/1606727383490-05311a4d-9d7e-49c2-92a4-16e835cf6d69.png)
实现了 1 位进位加减法器。

新建 Schematic 文件 AddSub4b，绘制原理图如下：
![image.png](./assets/1606727591926-5b3416e8-581e-436c-b316-661f1c8d0d90.png)
实现了 4 位加减法器。

对模块进行仿真，设计激励代码如下：
```verilog
module AddSub4b_AddSub4b_sch_tb();

// Inputs
   reg Ctrl;
   reg [3:0] A;
   reg [3:0] B;

// Output
   wire [3:0] S;
   wire Co;

// Instantiate the UUT
   AddSub4b UUT (
		.Ctrl(Ctrl), 
		.A(A), 
		.B(B), 
		.S(S), 
		.Co(Co)
   );
// Initialize Inputs
   integer i, j, k;
    initial begin
      for(k = 0; k < 16; k = k + 1) begin
        for(j = 0; j < 16; j = j + 1) begin
          for(i = 0; i < 2; i = i + 1) begin
            Ctrl = i;
            A = j;
            B = k;
            #50;
          end
        end
      end
    end
endmodule
```
得到波形图（部分）如下：
![image.png](./assets/1606727958104-0d22c768-a824-40ab-93bc-cd175b737a30.png)
![image.png](./assets/1606727973590-69feeef4-76d8-4104-9849-ff51eb621513.png)
可见，ctrl 为 0 时作加法，为 1 时作减法，且加减法的结果及其进位是正确的。


### 2.2 实现 4 位 ALU 及应用设计
新建 Schematic 文件 MyALU，绘制原理图如下：
![image.png](./assets/1606728250319-2d477e5a-8d8d-48cc-9cd9-8bcb5e9588d6.png)

对模块进行仿真，设计激励代码如下：
```verilog
// Instantiate the UUT
   myALU UUT (
		.S(S), 
		.A(A), 
		.B(B), 
		.C(C), 
		.Co(Co)
   );
// Initialize Inputs
  integer i, j, k;
  initial begin
      S = 1;
      for(j = 0; j < 16; j = j + 1) begin
          for(k = 0; k < 16; k = k + 1) begin
              for(i = 0; i < 4; i = i + 1) begin
                  S = i;
                  A = j;
                  B = k;
                  #50;
              end
          end
      end
	end
endmodule
```
得到波形图（部分）如下：
![image.png](./assets/1606725230123-4dc27008-bb72-4efc-bddd-78e28fc5b6d1.png)
![image.png](./assets/1606728411620-276cffd4-789e-4791-acc6-a04a91fc273b.png)
其中 S 为 00, 01, 10, 11 时，分别实现加法、减法、与、或操作。可见，我们正确实现了 4 位 ALU。

新建 Verilog Module 文件 Top，编写代码如下：
```verilog
module Top(
     input wire clk,
		 input wire [1:0]BTN,
		 input wire [1:0]SW1,
		 input wire [1:0]SW2,
		 output wire [3:0]AN,
		 output wire [7:0]SEGMENT,
		 output wire BTNX4
       );
		 wire [15:0] num;
		 wire [1:0] btn_out;
		 wire [3:0] C;
		 wire Co;
		 wire [31:0] clk_div;
		 wire [15:0] disp_hexs;
		 assign disp_hexs[15:12] = num[3:0]; //A
		 assign disp_hexs[11:8] = num[7:4]; //B
		 assign disp_hexs[7:4] = {3'b000,Co};
		 assign disp_hexs[3:0] = C[3:0];
		 
     pbdebounce m0(clk_div[17], BTN[0],btn_out[0]);
		 pbdebounce m1(clk_div[17],BTN[1],btn_out[1]);
		 clkdiv m2(.clk(clk),.rst(1'b0),.clkdiv(clk_div));
		 CreateNumber m3(.btn(btn_out),.sw(SW1),.num(num));
		 myALU m4(.S(SW2),.A(num[3:0]),.B(num[7:4]),.C(C),.Co(Co));
		 DispNum m6(.clk(clk),.HEXS(disp_hexs),.LES(4'b0),.points(4'b0),.RST(1'b0),.AN(AN),.Segment(SEGMENT));
		 assign BTNX4 = 1'b0; //Enable button inputs
	  
endmodule
```
View RTL Schematic，查看设计结果：
![image.png](./assets/1606728534088-34a9e9d8-308f-45a4-8786-4cc08c7239f4.png)

UCF 引脚定义如下：
```verilog
NET "clk"LOC = AC18 | IOSTANDARD = LVCMOS18;
NET "BTN[0]" LOC = V14 | IOSTANDARD = LVCMOS18;
NET "BTN[1]" LOC = W14 | IOSTANDARD = LVCMOS18;
NET "BTNX4" LOC = W16 | IOSTANDARD = LVCMOS18;
NET "SEGMENT[0]"LOC = AB22 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[1]" LOC = AD24 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[2]" LOC = AD23 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[3]" LOC = Y21 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[4]" LOC = W20 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[5]" LOC = AC24 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[6]" LOC = AC23 | IOSTANDARD = LVCMOS33;
NET "SEGMENT[7]" LOC = AA22 | IOSTANDARD = LVCMOS33;
NET "AN[0]" LOC = AD21 | IOSTANDARD = LVCMOS33;
NET "AN[1]" LOC = AC21 | IOSTANDARD = LVCMOS33;
NET "AN[2]" LOC = AB21 | IOSTANDARD = LVCMOS33;
NET "AN[3]" LOC = AC22 | IOSTANDARD = LVCMOS33;
NET "SW1[0]"LOC = AB10 | IOSTANDARD = LVCMOS15;
NET "SW1[1]"LOC = AA10 | IOSTANDARD = LVCMOS15;
NET "SW2[0]"LOC = AA13 | IOSTANDARD = LVCMOS15;
NET "SW2[1]"LOC = AA12 | IOSTANDARD = LVCMOS15;
```
下载到 SWORD 板上进行验证：<br />S = 00，加法：<br />1 + 8 = 9
![image.png](./assets/1606728906905-f4aac7cf-5f43-41c5-912d-5f7c3006e441.png)
C + 8 = 14 （12 + 8 = 20）
![image.png](./assets/1606728850373-c41c0f16-eb56-4701-92a1-c3feb2911791.png)
S = 01，减法：<br />4 - 6 = -2
![image.png](./assets/1606729144943-203a18e6-0b86-4fc6-a1b6-19e184528635.png)
S = 10，与：<br />1 AND 8 = 0 (0001 AND 0100 = 0000)
![image.png](./assets/1606728976257-c1e9db81-1cb3-4c9e-9db6-0a12ad3ac1c6.png)
2 AND d = 0 (0010 AND 1101 = 0000)
![image.png](./assets/1606729033348-4726814c-6753-4914-bd8f-b64a1bdf44b4.png)
S = 11，或：<br />2 OR d = F (0010 AND 1101 = 1111)
![image.png](./assets/1606729083795-83d55747-9f18-4cf4-83ed-3c97993bccb8.png)
2 OR 2 = 2
![image.png](./assets/1606729123199-ac55cb47-09d4-4c68-91fe-fc6da6b3dda9.png)
另外还测试了按钮的递增、递减和使能等开关。<br />上述实验结果验证，我们的设计是正确的。


## 3 讨论与心得
本次实验集合了之前很多次实验的结果，实现一个 ALU 是比较有成就感的。<br />本次实验的主要挑战仍在于从 Schematic 绘图过渡到 Verilog 的编写。虽然更加高效，但由于较为抽象且语法比较陌生，这个部分仍然出现了不少问题，花费了一些时间一一解决。
