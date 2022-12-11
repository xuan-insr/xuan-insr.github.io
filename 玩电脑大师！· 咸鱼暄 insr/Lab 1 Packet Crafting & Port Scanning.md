**Coverage**   	Packet sniffing, packet crafting, and port scanning<br />**Due** 		March 08, 2022


## Lab 1.1

### Level 1
![image.png](./assets/1645513749831-0622e7fa-be74-4452-9ba7-ee4c0070f823.png)
We press `F12` to use the developer tools of the browser and get the HTML code of the website below. We mark several useful information with (1) ~ (4):
![image.png](./assets/1645513716001-5dea3ba6-9618-4f0b-b199-71b515de0b38.png)
From info (1), we can know the password. If we enter the password, we can go to the next level:
![image.png](./assets/1645513929408-885bbec4-d1fa-4a2d-815b-e7bef03df08c.png)
![image.png](./assets/1645513937268-711c5191-177e-43c6-9f26-bbeb61c13eed.png)
If we check the onclick function (2) of the button, we can find `check()`, which compare the input string with a literal (3), which is the correct password.<br />We can also see that when the password is correct, browser will access the resource `l3vel2.html` which is referenced by the hypertext reference `href`. So we can also directly visit `l3vel2.html`, and we will get a same outcome as the first two methods.


### Level 2
![image.png](./assets/1645514456700-08057e56-9ac9-4df0-9b0a-b14e4412eedf.png)
Level 2 is the same as Level 1 (the 4 corresponding messages are marked on the picture above). So we can directly visit `Y0uR666.php`.


### Level 3
![image.png](./assets/1645514597288-2992cb63-3f76-460d-bf00-27bb67b810a6.png)
We can use the developer tools and get the response packet of the GET request:
![image.png](./assets/1645514719891-f42c3662-c420-4411-9959-65c3e97ad488.png)
And we can find the FLAG in the response headers.

OR we can use Burp Suite to capture the packet.<br />We enter the URL of Level 3, and we can see that the request packet is intercepted by Burp Suite:
![image.png](./assets/1645515044244-58852b84-92b9-4b10-9ec1-2aaf6f3a457c.png)
We press `Forward`, and the website is shown. We check the history and we can also find the flag:
![image.png](./assets/1645515198250-8004f23c-1c5f-45b9-ac47-9a75d291751d.png)
So the flag is: `ACTF{2650e41ce3e251bfd29527b5dff707ee}`


## Lab 1.2

### Level 1
We can find that there is a 302 direction, whose response shows the password.
![image.png](./assets/1645515438344-263b8b71-5f92-4924-8987-60b917a1fa55.png)

### Level 2
The level requires access from localhost:
![image.png](./assets/1645516085529-096d0d39-cf71-4e89-87b0-f1289a8b77a9.png)
So we can change the `Referer`field of the request:
![image.png](./assets/1645516037008-072a5435-eac0-453b-9572-5bd3ec7178e1.png)
And we can get the password:
![image.png](./assets/1645516005722-c99866ce-8d13-40db-b598-0acbc761d43c.png)

### Level 3
Level 3 requires access from admin:
![image.png](./assets/1645516282659-fb6e3bd9-00fa-46ae-ba6a-5ecd5eff744d.png)
We can see there is a Cookie called `admin`, whose original value is `0`. We try to change it to `1`:
![image.png](./assets/1645516195292-222c9985-4de7-4d92-bbf2-43a86ea1da53.png)
And we get the flag:
![image.png](./assets/1645516204429-66a5a91e-1b9b-451b-b9f1-3332ec114f20.png)
The flag is: `ACTF{47ca8aa874ba92a43621d5ff8cde0cdf}`


## Lab 1.3
https://zjusec.com/challenges/19

### Level 1
The source of the page mentioned 1.php.bak:
![image.png](./assets/1645581299071-e12fb9d6-7337-4ce7-b9c0-b5989d0dccc3.png)
So we try to access `/1.php.bak`, and we get the file below, where we find the `href` of the next level:
![image.png](./assets/1645581366068-1f717e3e-dbc3-4473-be3e-b8f6aafff676.png)

### Level 2
When we press the button, we will visit `/3rd.php`, but it shows an alert and send us back:
![image.png](./assets/1645585670085-ed155192-9f21-4a6e-9828-7776b7c5637a.png)
We can find in the request that there is no `Referer`field, so we add one:
![image.png](./assets/1645584242142-b0d88222-c43a-44aa-a33f-b97dc020dc75.png)
(Actually, my Firefox can directly visit the right Level 3 page, so I compared the request of Firefox with that of Burp Suite, and I find that the main difference was the existance of `Referer`field, which gave me some hints:)
![image.png](./assets/1645584193920-10d03ee7-2361-4734-b94e-41f4f496b827.png)
And we got to Level 3.

### Level 3
![image.png](./assets/1645584142824-7522fecc-7861-4df0-9a50-6a401f08fb08.png)
From the response header, we can find the URL of the next level:
![image.png](./assets/1645584315364-6ba58b92-daee-4b23-9410-f605253d0e26.png)

### Level 4
Level 4 asks us to press the button, but the button will disappear when mouse moves on it. We can check the source code and find the field `onmouseover="joy()"`, and the `joy()`function change the value of `display`field of the div to `none`.
![image.png](./assets/1645584408490-11aae516-41f7-49cf-89fa-9fad05cfd255.png)
We delete the `onmouseover`field, and we can press the button to get the flag:
![image.png](./assets/1645584480174-1d7d975f-145f-4967-a459-009382257f18.png)
![image.png](./assets/1645584500279-10680389-2d2f-4bde-b667-43633c689e4b.png)
The flag is:`AAA{y0u_2a_g0od_front-end_Web_developer}`


## Lab 1.4

### Step 1
We can use nmap command `nmap 8.136.83.180`(actually `nmap -p 8000-10000 8.136.83.180` is better as the possible ports are given), and get the result below:
![image.png](./assets/1645607533336-46506577-57eb-489d-a692-81fe0de47709.png)
Port 22, 80 are common ports, and 8080, 8081 are the first 2 games. So we try 8083:
![image.png](./assets/1645608351484-43541a86-66d0-413c-b390-517a74858161.png)

### Step 2
Then we use DirBuster:
![image.png](./assets/1645607769381-bb6d59f7-520b-4091-970a-acf603a53944.png)
And we can find...
![image.png](./assets/1645607748730-e78ce37e-2a9d-44c4-91b4-654d7df8b8f4.png)
![image.png](./assets/1645607828474-a1647133-488c-4eb3-9a91-93c59e54fe30.png)
Finally the flag!
![image.png](./assets/1645607863489-d658724e-6c66-4074-ac2f-4137534c5d21.png)
So the flag is `AAA{Earth_Three-body-Organization}`!

