
### 1 VIVADO 工具学习
![image.png](./assets/1615352465049-9165694c-99b8-441e-b034-e0b89c25f5dc.png)
![image.png](./assets/1615352593462-94c9f8ad-2d1c-4d83-b9c3-9b507ef4a776.png)
```verilog
`timescale 1ns / 1ps
module Water_LED(
        input CLK_i,
        input RSTn_i,
        output reg [3:0] LED_o
    );
    reg [31:0] C0;
    
  always @(posedge CLK_i) begin
      if (!RSTn_i) begin
          LED_o <= 1;
          C0 <= 0;
      end
      else begin
          if (C0 == 32'd100_000_000) begin
              C0 <= 32'h0;
              if (LED_o == 4'b1000)
                  LED_o <= 4'b1;
              else LED_o <= LED_o << 1;
          end
          else begin
              C0 <= C0 + 1;
          end
      end
  end

endmodule
```
![image.png](./assets/1615352948274-82b14fae-2ed5-48f9-97b3-310b90fd9631.png)
Change Line 15 of the program above to be `if (C0 == 32'd100_00) begin` temporarily for faster simulation.
```verilog
`timescale 1ns / 1ps
module Water_LED_tb;
    reg CLK_i;
    reg RSTn_i;
    wire [3:0] LED_o;
    
    Water_LED wled(CLK_i, RSTn_i, LED_o);
    always #5 CLK_i = ~CLK_i;
    
    initial begin
        CLK_i = 0;
        RSTn_i = 0;
        #100 RSTn_i = 1;
    end
endmodule
```
![image.png](./assets/1615353134768-e957ce2a-55e3-42af-9035-39f96daf2f67.png)
![image.png](./assets/1615353263138-f6b41c61-f2c3-4712-b193-134c3498358c.png)
![image.png](./assets/1615353348880-1113a009-3a60-4436-a110-3468696e8449.png)
![image.png](./assets/1615359385357-8c97ff4a-c8a9-4de3-b449-1f02a166b50d.png)

如综合前，脚本约束引脚，则综合后直接进行实现步骤；若综合后，工具约束引脚，则需再次进行综合，再进行实现步骤 点击IMPLEMENTATION下的Run Implementation,在弹窗中直接点击OK，开始实现步骤 
![image.png](./assets/1615359981633-7dd2c8bd-cdc0-4363-befd-6d0f0b54b00e.png)
![IMG_20210310_151131.jpg](./assets/1615360361979-122a8237-cf8a-4b3f-8b6a-b51286e876c4.jpeg)


### 2 自定义模块设计学习
