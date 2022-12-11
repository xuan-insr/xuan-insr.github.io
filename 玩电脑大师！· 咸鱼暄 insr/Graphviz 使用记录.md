
#### 有向图 - 

#### 结点形状 - 

#### 不可见结点 - 

#### 将多个结点设在一行：
```
digraph G {
    rankdir = TB;
    node [shape = rectangle];
    100 [style = invis];
    
    1 [label = "S→.declaration\ndeclaration→.type var-list\ntype→.float\ntype→.int"]; 
    3 [label = "type→int."]; 
    2 [label = "declaration→type.var-list\nvar-list→.var-list,identifier\nvar-list→.identifier"]; 
    4 [label = "type→float."]; 
    5 [label = "var-list→var-list.,identifier\ndeclaration→type var-list."];
    6 [label = "var-list→identifier."]; 
    7 [label = "var-list→var-list,.identifier"];
    8 [label = "var-list→var-list,identifier."];
    9 [label = "S→declaration."]; 
    
    {rank=same; 1, 9;}
    {rank=same; 2, 6;}
    assis1 [style = invis];
    3->assis1 [style = invis];
    {rank=same; assis1, 2;}
    
    
    100->1;
    1->2 [label = "type"];
    1->3 [label = "int"];
    1->4 [label = "float"];
    1->9 [label = "declaration"];
    2->5 [label = "var-list"];
    2->6 [label = "identifier"];
    5->7 [label = ","];
    7->8 [label = "identifier"];
}
```
![](https://cdn.nlark.com/yuque/__graphviz/3a023ca8e8e917cefe58e5656e2e3aa6.svg#lake_card_v2=eyJ0eXBlIjoiZ3JhcGh2aXoiLCJjb2RlIjoiZGlncmFwaCBHIHtcbiAgICByYW5rZGlyID0gVEI7XG4gICAgbm9kZSBbc2hhcGUgPSByZWN0YW5nbGVdO1xuICAgIDEwMCBbc3R5bGUgPSBpbnZpc107XG4gICAgXG4gICAgMSBbbGFiZWwgPSBcIlPihpIuZGVjbGFyYXRpb25cXG5kZWNsYXJhdGlvbuKGki50eXBlIHZhci1saXN0XFxudHlwZeKGki5mbG9hdFxcbnR5cGXihpIuaW50XCJdOyBcbiAgICAzIFtsYWJlbCA9IFwidHlwZeKGkmludC5cIl07IFxuICAgIDIgW2xhYmVsID0gXCJkZWNsYXJhdGlvbuKGknR5cGUudmFyLWxpc3RcXG52YXItbGlzdOKGki52YXItbGlzdCxpZGVudGlmaWVyXFxudmFyLWxpc3TihpIuaWRlbnRpZmllclwiXTsgXG4gICAgNCBbbGFiZWwgPSBcInR5cGXihpJmbG9hdC5cIl07IFxuICAgIDUgW2xhYmVsID0gXCJ2YXItbGlzdOKGknZhci1saXN0LixpZGVudGlmaWVyXFxuZGVjbGFyYXRpb27ihpJ0eXBlIHZhci1saXN0LlwiXTtcbiAgICA2IFtsYWJlbCA9IFwidmFyLWxpc3TihpJpZGVudGlmaWVyLlwiXTsgXG4gICAgNyBbbGFiZWwgPSBcInZhci1saXN04oaSdmFyLWxpc3QsLmlkZW50aWZpZXJcIl07XG4gICAgOCBbbGFiZWwgPSBcInZhci1saXN04oaSdmFyLWxpc3QsaWRlbnRpZmllci5cIl07XG4gICAgOSBbbGFiZWwgPSBcIlPihpJkZWNsYXJhdGlvbi5cIl07IFxuICAgIFxuICAgIHtyYW5rPXNhbWU7IDEsIDk7fVxuICAgIHtyYW5rPXNhbWU7IDIsIDY7fVxuICAgIGFzc2lzMSBbc3R5bGUgPSBpbnZpc107XG4gICAgMy0-YXNzaXMxIFtzdHlsZSA9IGludmlzXTtcbiAgICB7cmFuaz1zYW1lOyBhc3NpczEsIDI7fVxuICAgIFxuICAgIFxuICAgIDEwMC0-MTtcbiAgICAxLT4yIFtsYWJlbCA9IFwidHlwZVwiXTtcbiAgICAxLT4zIFtsYWJlbCA9IFwiaW50XCJdO1xuICAgIDEtPjQgW2xhYmVsID0gXCJmbG9hdFwiXTtcbiAgICAxLT45IFtsYWJlbCA9IFwiZGVjbGFyYXRpb25cIl07XG4gICAgMi0-NSBbbGFiZWwgPSBcInZhci1saXN0XCJdO1xuICAgIDItPjYgW2xhYmVsID0gXCJpZGVudGlmaWVyXCJdO1xuICAgIDUtPjcgW2xhYmVsID0gXCIsXCJdO1xuICAgIDctPjggW2xhYmVsID0gXCJpZGVudGlmaWVyXCJdO1xufSIsInVybCI6Imh0dHBzOi8vY2RuLm5sYXJrLmNvbS95dXF1ZS9fX2dyYXBodml6LzNhMDIzY2E4ZThlOTE3Y2VmZTU4ZTU2NTZlMmUzYWE2LnN2ZyIsImlkIjoiWWd4bTMiLCJtYXJnaW4iOnsidG9wIjp0cnVlLCJib3R0b20iOnRydWV9LCJjYXJkIjoiZGlhZ3JhbSJ9)
#### 无向图 - 

#### 无边框：
```
graph G {
    rankdir = TB;
    node [penwidth = 0];
    1 [label = "-"];
    2 [label = "+"];
    1 -- 2, 6;
    3;
    0 [label = "*"];
    2 -- 3, 0;
    0 -- 4, 5;
}
```
![](https://cdn.nlark.com/yuque/__graphviz/5460f2349873780fa94a3fd01a5154fe.svg#lake_card_v2=eyJ0eXBlIjoiZ3JhcGh2aXoiLCJjb2RlIjoiZ3JhcGggRyB7XG4gICAgcmFua2RpciA9IFRCO1xuICAgIG5vZGUgW3BlbndpZHRoID0gMF07XG4gICAgMSBbbGFiZWwgPSBcIi1cIl07XG4gICAgMiBbbGFiZWwgPSBcIitcIl07XG4gICAgMSAtLSAyLCA2O1xuICAgIDM7XG4gICAgMCBbbGFiZWwgPSBcIipcIl07XG4gICAgMiAtLSAzLCAwO1xuICAgIDAgLS0gNCwgNTtcbn0iLCJ1cmwiOiJodHRwczovL2Nkbi5ubGFyay5jb20veXVxdWUvX19ncmFwaHZpei81NDYwZjIzNDk4NzM3ODBmYTk0YTNmZDAxYTUxNTRmZS5zdmciLCJpZCI6ImFhbXBZIiwibWFyZ2luIjp7InRvcCI6dHJ1ZSwiYm90dG9tIjp0cnVlfSwiY2FyZCI6ImRpYWdyYW0ifQ==)