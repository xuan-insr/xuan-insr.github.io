# 咸鱼暄的代码空间！

<img src="index.assets/image.png" alt="image" style="zoom: 67%;" />

正在从 [语雀](https://www.yuque.com/xianyuxuan/coding) 逐步迁移！

## 颜色主题

### 日间 / 夜间

<div class="tx-switch">
  <button data-md-color-scheme="default"><code>default</code></button>
  <button data-md-color-scheme="slate"><code>slate</code></button>
</div>

<script>
  var buttons = document.querySelectorAll("button[data-md-color-scheme]")
  buttons.forEach(function(button) {
    button.addEventListener("click", function() {
      var attr = this.getAttribute("data-md-color-scheme")
      document.body.setAttribute("data-md-color-scheme", attr)
      var name = document.querySelector("#__code_0 code span:nth-child(7)")
      name.textContent = attr
    })
  })
</script>

### 主色

<div class="tx-switch">
  <button class="button1" data-md-color-primary="red" style="background-color:red">red</button>
  <button class="button1" data-md-color-primary="pink" style="background-color:pink;color:black">pink</button>
  <button class="button1" data-md-color-primary="purple" style="background-color:purple">purple</button>
  <button class="button1" data-md-color-primary="indigo" style="background-color:indigo">indigo</button>
  <button class="button1" data-md-color-primary="blue" style="background-color:blue">blue</button>
  <button class="button1" data-md-color-primary="cyan" style="background-color:cyan;color:black">cyan</button>
  <button class="button1" data-md-color-primary="teal" style="background-color:teal">teal</button>
  <button class="button1" data-md-color-primary="green" style="background-color:green">green</button>
  <button class="button1" data-md-color-primary="lime" style="background-color:lime;color:black">lime</button>
  <button class="button1" data-md-color-primary="orange" style="background-color:orange;color:black">orange</button>
  <button class="button1" data-md-color-primary="brown" style="background-color:brown;border-radius=3px">brown</button>
  <button class="button1" data-md-color-primary="grey" style="background-color:grey">grey</button>
  <button class="button1" data-md-color-primary="black" style="background-color:black">black</button>
  <button class="button1" data-md-color-primary="white" style="background-color:white;color:black">white</button>
</div>

<script>
  var buttons = document.querySelectorAll("button[data-md-color-primary]")
  buttons.forEach(function(button) {
    button.addEventListener("click", function() {
      var attr = this.getAttribute("data-md-color-primary")
      document.body.setAttribute("data-md-color-primary", attr)
      var name = document.querySelector("#__code_2 code span:nth-child(7)")
      name.textContent = attr.replace("-", " ")
    })
  })
</script>
