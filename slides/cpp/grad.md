---
title: 毕业论文答辩 解雲暄
verticalSeparator: ===
revealOptions:
  width: 1600
  height: 900
  margin: 0.04
  transition: 'fade'
  slideNumber: true
---

<link rel="stylesheet" href="custom_white.css">
<link rel="stylesheet" href="../custom_white.css">
<link rel="stylesheet" href="custom.css">
<link rel="stylesheet" href="../custom.css">


<!-- .slide: class="custom-background" -->

## 基于 CBMC 的
## OpenHarmony 分布式软总线组件源码
## 自动化验证实践

<br>

<!-- ![](assets/2023-05-26-16-16-17.png) -->

<!-- <br> -->

#### 信息安全1901 解雲暄 3190105871 

<br>

#### 指导教师：赵永望

---

### OpenHarmony 技术架构

![](assets/2023-05-26-16-50-56.png)

智能终端设备操作系统的开源框架和平台

===

### 分布式软总线组件技术架构

<img src="assets/2023-05-26-16-50-35.png" width="40%">

提供统一的分布式通信功能，帮助设备之间快速发现、连接和高效传输数据

---

### CBMC | C Bounded Model Checker

```c++
if ((0 <= t) && (t <= 79))
    switch (t / 20) {
    case 0:
        TEMP2 = ((B AND C) OR (~B AND D));
        TEMP3 = (K1);
        break;
    case 1:
        TEMP2 = ((B XOR C XOR D));
        TEMP3 = (K2);
        break;
    case 2:
        TEMP2 = ((B AND C) OR (B AND D) OR (C AND D));
        TEMP3 = (K3);
        break;
    case 3:
        TEMP2 = (B XOR C XOR D);
        TEMP3 = (K4);
        break;
    default:  assert(0);
    }
```

===

#### 控制流图 | Control Flow Graph

![](assets/2023-05-26-16-56-30.png)

===

#### 利用 SAT / SMT 求解器

<style>
.image-container {
    display: flex;
    justify-content: space-between;
  }
</style>

<div class="image-container">
  <img src="assets/2023-05-26-16-56-37.png" alt="Image 1">
  <img src="assets/2023-05-26-16-58-31.png" alt="Image 2">
</div>

===

#### 循环展开

```c++
while (cond)
    Body;
```

```c++
if (cond) {
    Body;
    if (cond) {
        Body;
        if (cond) {
            Body;
            assume(!cond);
        }
    }
}
```

===

### CBMC | C Bounded Model Checker

![](assets/2023-05-26-17-08-51.png)

===

### 性质

用户给定断言：`__CPROVER_assert( cond );`

自动生成断言：`--pointer-check`
- 缓冲区溢出
- 指针安全
- 内存泄漏
- 除以 0
- NaN
- 算术溢出

---

```c++
bool IsValidString(const char *input, uint32_t maxLen) {
    if (input == NULL) 
        return false;

    uint32_t len = strlen(input);
    if (len >= maxLen) 
        return false;

    return true;
}
```

===

```c++
bool IsValidString(const char *input, uint32_t maxLen);
```

```c++
#include "../../include/xyx_proof_includes.h"
#include "softbus_utils.h"

void harness(void) {
    uint32_t maxLen;
    uint32_t size;

    __CPROVER_assume(size > 0);
    char * str = malloc(size);

    bool res = IsValidString(str, maxLen);

    if (!str)
        __CPROVER_assert(res == false, 
            "IsValidString should return false if str is a null pointer.");
}
```

===

![](assets/string_report1.png)

===

#### Loop unwinding failure

![](assets/unwindFailure.png)

<center>

`--unwind 3`

`--remove-function-body` <!-- .element: class="fragment" -->

</center>

===

```c++
bool IsValidString(const char *input, uint32_t maxLen);
```

```c++
#include "../../include/xyx_proof_includes.h"
#include "softbus_utils.h"

void harness(void) {
    uint32_t maxLen;
    uint32_t size;

    __CPROVER_assume(size > 0);
    char * str = malloc(size);

    if (str)
        __CPROVER_assume(str[size - 1] == 0);

    bool res = IsValidString(str, maxLen);

    if (!str)
        __CPROVER_assert(res == false, 
            "IsValidString should return false if str is a null pointer.");
}
```

===

#### `InitSoftBus`

<center>

解决方案：桩函数<!-- .element: class="fragment" -->

</center>

<img src="assets/2023-05-31-20-44-05.png" width="40%">

===

```c++ [1|3-7|8-12|13-27|28-30]
static int32_t AddClientPkgName(const char *pkgName)
{
    // 拿锁
    if (pthread_mutex_lock(&g_pkgNameLock) != SOFTBUS_OK) {
        SoftBusLog(SOFTBUS_LOG_COMM, SOFTBUS_LOG_ERROR, "lock init failed");
        return SOFTBUS_LOCK_ERR;
    }
    // 检查包名合法
    if (CheckPkgNameInfo(pkgName) == false) {
        (void)pthread_mutex_unlock(&g_pkgNameLock);
        return SOFTBUS_INVALID_PARAM;
    }
    // 创建包名信息，加入包名列表
    PkgNameInfo *info = (PkgNameInfo *)SoftBusCalloc(sizeof(PkgNameInfo));
    if (info == NULL) {
        SoftBusLog(SOFTBUS_LOG_COMM, SOFTBUS_LOG_ERROR, "Create PkgNameInfo malloc fail.");
        pthread_mutex_unlock(&g_pkgNameLock);
        return SOFTBUS_MALLOC_ERR;
    }
    if (strcpy_s(info->pkgName, PKG_NAME_SIZE_MAX, pkgName) != EOK) {
        SoftBusLog(SOFTBUS_LOG_COMM, SOFTBUS_LOG_ERROR, "Add strcpy_s failed.");
        SoftBusFree(info);
        (void)pthread_mutex_unlock(&g_pkgNameLock);
        return SOFTBUS_MEM_ERR;
    }
    ListInit(&info->node);
    ListAdd(&g_pkgNameList, &info->node);
    // 释放锁
    (void)pthread_mutex_unlock(&g_pkgNameLock);
    return SOFTBUS_OK;
}
```

===

#### 桩函数

```c++
static int32_t AddClientPkgName_stub(const char *pkgName)
{
    if (pthread_mutex_lock(&g_pkgNameLock) != SOFTBUS_OK)
        return SOFTBUS_LOCK_ERR;
    
    int32_t ret;
    __CPROVER_assume(ret == SOFTBUS_INVALID_PARAM || 
                     ret == SOFTBUS_MALLOC_ERR ||
                     ret == SOFTBUS_MEM_ERR ||
                     ret == SOFTBUS_OK);
    
    (void)pthread_mutex_unlock(&g_pkgNameLock);
    return ret;
}
```

===

### 结论

在所使用的操作系统相关功能以及其他 OpenHarmony 组件相关函数没有内存安全问题的前提下，以下模块没有内存安全问题：

- 发布服务接口 `PublishLNN`
- 注销服务接口 `StopPublishLNN`
- 发现服务接口 `RefreshLNN`
- 停止发现接口 `StopRefreshLNN`
- 组网请求接口 `JoinLNN` 
- 退网请求接口 `LeaveLNN`

编写的 harness 可供 CI 系统集成。

===

![](assets/2023-05-31-21-24-03.png)

在具体使用场景下不会发生

===

```c++
RetType foo(Para...) {
    __CPROVER_assert(pre_cond);

    return fooImpl(para...);
}
```

===

### 局限性

- 外部函数没有被覆盖<!-- .element: class="fragment" -->
- 回调函数无法覆盖<!-- .element: class="fragment" -->
- CBMC 工具本身仍有问题<!-- .element: class="fragment" -->
- 工作顺序导致的工作量和文档问题<!-- .element: class="fragment" -->

---

## 基于 CBMC 的
## OpenHarmony 分布式软总线组件源码
## 自动化验证实践

<br>

<!-- ![](assets/2023-05-26-16-16-17.png) -->

<!-- <br> -->

#### 信息安全1901 解雲暄 3190105871 

<br>

#### 指导教师：赵永望