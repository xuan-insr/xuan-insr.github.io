解雲暄	3190105871

### 1 DDoS

#### a. What is the difference between DoS attacks and DDoS attacks?
DoS attack - Denial of Service attack. The attacker overload victim by exhausting its resources (bandwidth, computing resources or queue spaces), making it unable to response for some normal legal requests.<br />DDoS attack - Distributed DoS attack. The attacker use a large amount of devices to perform DoS attack on a victim, in the same way and for the same results. <br />The difference is that, DDoS attackes are performed by many devices which are usually in different subnets. If DoS attack is performed by a single device, the victim can easily defend it by blocking its IP or subnet, but as for DDoS attack, the attacking devices are widely distributed, so it's kind of hard to defend.


#### b. How does the TCP SYN Flood attack work?
When we send a SYN (1st handshake) to the victim, it will allocate some resources to save informations like the SEQ of the coming packet, and this packet will be pushed into SYN queue (SYN backlog). However, the SYN queue is small, normally 128 entries. If the attacker only send SYN but not response to the SYN+ACK (2nd handshake) segment, then the SYN packet will be stored in the queue until the time is exceeded, which is normally 3 minutes. So if the attacker send no less than 128 SYN packet each 3 minutes without responsing to any SYN+ACK packet, the SYN backlog of the victim will always be full and the legal requests of other devices will not be fulfilled, resulting in a Denial of Service.


#### c. How does the solution of SYN Cookies against TCP SYN Flood attacks work?
We can see from the principle of TCP SYN Flood that, the weakness is the limitation of SYN queue. The aim of this queue is to store the information of the coming SYN packets, so we can find ways to avoid this kind of storage. Instead, SYN Cookies try to hide the information of the SYN packets into the SYN+ACK packet. As we know, the 3 steps of TCP handshake is to exchange their initial sequence, which is related to time. But if SYN Cookies is used, the sequence of SYN+ACK packet sent by the server is a digest of the data of SYN packet and other information like time. When the ACK (3rd handshake) comes, it can check its acknowledge number and know whether it is legal. In this way, the SYN queue is not needed, so the TCP SYN Flood attack will not work.


#### d. How does the DNS Amplification Attack work? How to defend against it?
DNS Amplification Attack uses open DNS resolvers, which provide an open DNS service for all internet users. The attacker uses a spoofed IP address which is actually the IP address of the victim to send a query to the open DNS resolver, and it will send a response to the victim. There is a kind of DNS request `ANY`, which will return **all** types of information of a given name, which is a huge amount of data. <br />Defense: reduce the number of open DNS solvers, or disable the `ANY` request of them, or use techniques like ingress filtering, or disable UDP service of the victim.


### 2 DDoS 

#### a. How does Memcached attack work?
Memcached attack uses memcached servers, which provide (distributed) cache service for speeding up website accessing. Memcached services also use UDP so there is no need to setup a connection. The attacker pre-load the memcached server with some related information with methods like accessing it, and then send a request to the memcached server with spoofed IP address which is actually the IP address of the victim. The server will then send a very large amount of data to the victim, and the victim will be overwhelmed.


#### b. What is the difference between HTTP Flood and Fragmented HTTP Flood? 
HTTP Flood mainly exhausts the server by GET or POST some large contents, and the server will need to take them from or store them into database, which is time consuming; the server may also need to encrypt or decrypt the contents, which will consume the computing resources of the server.<br />Fragmented HTTP Flood trys to split a HTTP segment into many small fragments, and to send it very slowly but not exceed the timeout, so that the server will always keep the connection which is resource consuming.


#### c. Why is Fragmented HTTP Flood relatively more challenging to detect?
Because the content, traffic and source are very normal. For other DDoS attacks, there are useless large-scale data or abnormal requests, which is easy to detect. But Fragmented HTTP Flood looks just like a normal user.


#### d. How does Ingress Filtering work?
Ingress Filtering asks the source ASes to check each packet before routing them on the public net whether the source IP address is in the subnet of the outcoming AS. If not, this packet should not be routed.


#### e. How does IP Traceback work?
Some information should be added into the packet so that the receiver can check whether the path is valid.<br />The easiest way is to add all the path information into the packet, but it will make the packet too large.<br />Another way is use edge sampling, by using propability, each packet will sample different routers on the way as well as a distance to the sampled router. As a session will normally send many packets, we can restore she whole path.


### 3 Secure Routing

#### a. What are the key features of the five typical delivery schemes?

- **Unicast**		Send to a single host.
- **Boardcast	**Send to all hosts in the same network or subnet.
- **Multicast	**Send to a group of hosts.
- **Anycast		**Send to any one host in a group.
- **Geocast 		**A special case of multicast, where the _group_ is defined by the hosts' geographical locations.


#### b. What is the framework of the Dijkstra algorithm?
```cpp
struct edge {
  int v, w;
};

vector<edge> e[maxn];
int dis[maxn], vis[maxn];

void dijkstra(int n, int s) {
  memset(dis, 63, sizeof(dis));
  dis[s] = 0;
  for (int i = 1; i <= n; i++) {
    int u = 0, mind = 0x3f3f3f3f;
    for (int j = 1; j <= n; j++)
      if (!vis[j] && dis[j] < mind) u = j, mind = dis[j];
    vis[u] = true;
    for (auto ed : e[u]) {
      int v = ed.v, w = ed.w;
      if (dis[v] > dis[u] + w) dis[v] = dis[u] + w;
    }
  }
}
```


#### c. What is the framework of the Bellman-Ford algorithm?
```cpp
struct edge {
    int v, w;
};

vector<edge> e[maxn];
int dis[maxn];
const int inf = 0x3f3f3f3f;

bool bellmanford(int n, int s) {
    memset(dis, 63, sizeof(dis));
    dis[s] = 0;
    bool flag; 
    for (int i = 1; i <= n; i++) {
        flag = false;
        for (int u = 1; u <= n; u++) {
            if (dis[u] == inf) continue;
            for (auto ed : e[u]) {
                int v = ed.v, w = ed.w;
                if (dis[v] > dis[u] + w) {
                    dis[v] = dis[u] + w;
                    flag = true;
                }
            }
        }
        if (!flag) break;
    }
    return flag;
}
```


#### d. How does prefix hijacking work?
The first method is to pretend to be a certain prefix. When routers exchanges their messages, they will think that the attacker has this prefix and they renew their routing table. So the traffic towards that prefix will acturally routed to the attacker.<br />The second method is to pretend to be near to a certain prefix. As the routing algorithms tend to find a short path toward the destination, some of the routers will route the packets to the attacker.


#### e. How does RPKI work? Why is it insufficient for secure routing?
RPKI, Resource Public Key Infrastructure, provides a certified mapping from ASes to prefixes (as well as public keys). So when an attacker AS pretend to have a certain prefix, other ASes can find from the RPKI that it is not valid, so that the first method of prefix hijacking will not work.<br />But as for the second method, RPKI can do nothing, so it is insufficient for secure routing.


### 4 Anonymous Communication 

#### a. Why is current Internet communication vulnerable to anonymity or privacy leakage? 
Because Internet uses IP address to identify a host, and each router on the path from source to destination needs to know about the exact IP address of the destination to make the routing decision. But the IP address itself as well as the communication source and destination can leak some anonymity and privacy, because knowing the existance of communication without the exact contents is enough to infer some information on the user, who is easy to find by its IP address.


#### b. In which scenarios do users require the communication anonymity or privacy as concerned in sub-question a?
There are cases where users try to access some medical, voting or other kind of information related to privacy. If one is known to usually access the website of a party or candidate, he is inclined to vote for the candidate, which is a privacy leakage. Also, when an attacker is trying to spy on or modify some data, he is also not willing to be known about his IP address, which can find him easily.


#### c. How to use proxies to secure communication anonymity? What are the possible limitations?
The sender send message to the proxy instead of the destination, and the destination is encrypted and placed in the packet. The proxy will decrypt it and send the corresponding message to the destination. If the attacker sniffs between the sender and proxy, he will not know about the destination, and if it sniffs between the proxy and destination, he will not know about the source.<br />However, if the attacker sniffs both between the sender and proxy, and between the proxy and destination, the anonymity will fail. So will it fail in the case where the proxy itself is malicious.


#### d. How does Onion Routing provide a better guarantee for anonymity?
The proxy nodes are randomly selected and each node can only decrypt one layer and will encrypt when it pass to next node. Unless there are enough number of nodes collude with each other, they know nothing about the source or destination.


#### e. How to infer anonymity or privacy of Onion Routing traffic?
Each node only knows about the immediately preceding and following node in a relay. The source and destination of messages is obscured by layers of encryption. And because of the layers of encryption and randomization, none of the nodes can know whether the next and last node is the source or destination or not.


### 5 Web Security

#### a. How does Same Origin Policy work?
Browsers are set to isolate sites from different origins. Here _isolate_ means that they cannot access resources like cookies from each other in order to prevent malicious sites from spying on or modify the private information.<br />Sites with the same **protocol, hostname and port number** will be are seen as same-origin, while it doesn't matter if the paths are different. For example, `http://a.com/a` and `http://a.com/b`are same-origin, but `http://a.com/a` and `https://a.com/b` are not as the protocol are different. Nor are `http://a.com` and `http://www.a.com`as the hostname are not the same.<br />It's worth noting that the default port number of HTTP protocol is 80, so `http://a.com`and `http://a.com:81` are not same-origin either.


#### b. How does SQL Injection work? How to defend against it?
If the user input are not filtered or checked properly, part of the malicious input will be seen by SQL parser as code instead of data, which can enable attacker to operate some attack like get or modify or delete some data.<br />For example, there can be a library website designed to show the information of books given a name, and the query can be `SELECT * FROM books WHERE name = '[1]'`, where `[1]` is the user input. Then the user can input `1' or '1' = '1`, which will make the whole query `SELECT * FROM books WHERE name = '1' or '1' = '1'`. As we can see, this query will return all the data in `books`, which is not meant to.

There are 2 kinds of defenses mentioned in our course. <br />The first one is **Input Sanitization**, which is to ensure there are no instructions or queries in user input. We can make a blacklist of illegal or dangerous input characters or patterns (or maybe a whitelist is securer), or escape some special characters like quotes which can be essential part of malicious inputs.<br />The second one is **Prepared Statement**, which is originally meant to speed up some recurring queries. It enables users to send a template of query with its parameters unbinded, which will be parsed and optimized by the DBMS. When the user data comes, it will execute which can make the query faster. However, we can find it useful in defending SQL injection. We can notice that the main reason of SQL injection is that the input data is not isolated from code, which will make SQL parser sometimes treat some input as query, which is vulnerable. But prepared statement will pre-parse the query template, and the input data will be directly put into execution without being parsed, which can never be treated as code, and can prevent SQL Injection.


#### c. Please refer to the slides or search online and provide two concrete examples of SQL Injection.
We can take Problem 5 and 6 in Lab 3 as examples. 

In problem 5, the website will return the `first_name` and `last_name` of a given `user_id`by directly insert user input into `SELECT first_name, last_name FROM users WHERE user_id = '[1]'`, where `[1]` is the user input. So if we input`1' union SELECT first_name, password as last_name FROM users #`, the query will be:`SELECT first_name, last_name FROM users WHERE user_id = '1' union SELECT first_name, password as last_name FROM users #'`, which will also return the `first_name` and `password`of all users.

In problem 6, the website only returns the existance of a certain `user_id` in the database with the same query of problem 5. However, we can also get some data in this case. For example, the following query can show whether the length is 32 by the existance of the outcome:`SELECT first_name, last_name FROM users WHERE user_id = 'x' or length(select password from users limit 1, 1) = 32`. In this way, if we can write a script to test the length of each field in each tuple, and get the value by guessing the content character by character.


### 6 Web Security

#### a. How does a DNS hijacking attack affect network security?
DNS, Domain Name Server, is to translate domain name into actural IP address. So if one on Internet want to access a website by a domain name, he will need to turn to DNS to get the IP address. If the DNS server is malicious or disguised, it may return a wrong IP address which can lead to a phishing website. If the user didn't find the problem and trust the website, he or she may be under attack like CSRF or XSS, or leak some private information.


#### b. In HTTPS, how does a user verify a certificate for determining the authenticity of the website it connects to?
During connection, the user will receive the certificate and its digital signature. The user (maybe a browser) will check whether the domain name is the same and the term of validity is not exceeded, and will turn to CA (Certificate Authority) which is a trusted third party to certify the public key. The user get these message and check whether the digest of the certificate is same to the given one, so the user can know whether the certificate is modified. If not, then the website is reliable.


#### c. Please provide a concrete example to showcase CSRF.
Also take Lab 3 as an example. We write an HTML like this:
```html
<!DOCTYPE HTML>
<html>
  <head>
    <meta charset = "utf-8">
    <title>盗号网页</title>
  </head>
  <body>
    <img src="http://127.0.0.1/DVWA/vulnerabilities/csrf/?password_new=xyx&password_conf=xyx&Change=Change#" alt="">
  </body>
</html>
```
If the victim opening this webpage has logged in to `http://127.0.0.1/DVWA`, the browser will store the cookie. When the browser tries to access the img, it will send a GET request to the src, which is actually will request to chang the password to `xyx`. As the browser holds the cookie and adds it into the request header, the server will think that it's the user himself sent this request, and the password is modified.


#### d. Please provide two concrete examples to showcase Stored XSS and Reflective XSS.
In Lab 3, Problem 10 is a website of message board, where the messages are stored in the database without proper filtering. If we sometime submit message like below:<br />![](./assets/1648235603575-65139fa8-64d6-4a49-8d25-cc8f7eac692b.png)
When the webpage is trying to display our message without filtering, it enables us to insert some scripts. This is an example of Stored XSS.

In Problem 9, the webpage will echo our input (name) to welcome us. But if we make a URL like this: `[http://127.0.0.1/DVWA/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E#](http://127.0.0.1/DVWA/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28document.cookie%29%3C%2Fscript%3E#)`, where the name is acturally `<script>alert(document.cookie)</script>`, then when the server is trying to show this string, it is acturally inserting a script into HTML, and the browser will run it. If we send this URL to some other users, their private data like cookies might be stolen. This is an example of Reflected XSS.


### 7 Email Security

#### a. Please describe common threats against Email security.

- **Authentication-related Threats**: unauthorised access to email systems 
- **Integrity-related Threats**: unauthorized modification of email contents 
- **Confidential-related Threats**: unauthorized disclosure of sensitive information 
- **Availability-related Threats**: block users from sending and receiving emails  


#### b. How should an Email be protected to support both Authentication and Confidentiality?

- **Authentication**	The sender generate a SHA-256 digest and use its private key to encrypt it, add it and the sender's information into the message. The receiver then use the public key to decrypt the digest and can check whether the message was modified.
- **Confidentiality**	The sender generate a random 128-bit key for each message, and use it to encrypt the content. Then the sender encrypt the key with the public key of the receiver and append it into the message. The receiver need to first decrypt the key and use it to decrypt the content.


#### c. Please describe the differences among DANE, SPF, and DKIM.

- **DANE** is based on DNSSEC protocol, is to ensure the destination's certificate.
- **SPF** is just part of DNS, which certificate the mails sent from the mail servers in the domain.
- **DKIM** is to certificate by signiture.


### 8 Traffic Analysis

#### a. Please describe the properties of the four types of commonly used Firewall.

- **Packet Filtering Firewall** 		Only making filtering decisions on single packet, check nothing about higher-layer contents. 
- **Stateful Insepction Firewall** 	Check both the packet and its context.
- **Application Proxy Firewall** 		A relay of application-level traffic.
- **Circuit-Level Proxy Firewall** 	Check nothing about the contents, only a rely of TCP segments.


#### b. What are the differences among Firewall, IDS, and IPS?
**Firewall** limits access to ports by given settings, and cannot filter intrusion. **IDS** will report but not filter the intrusion. **IPS** can both filter and report intrusion.


#### c. Please list commonly used methods for obfuscating traffic to evade detection?

- Encrypt traffic to hide payloads
- Use proxy to hide entire packets
- Introduce noise traffic to hide patterns


### 9 Open Question - Authentication Efficiency
> Consider a time-consuming authentication scenario where a database records all secret keys of a large number of users. When the system authenticates a user, it first issues a challenge message to the user. The user then uses his/her key to encrypt the challenge and then returns the encrypted challenge to the system. The system then encrypts the challenge using one key in the database after another and compares the result with the received encrypted message. Once a match is found, the system accepts the user. Otherwise, the user is denied. This authentication protocol surely takes a lot of time and computation.
> 
> Design a possible solution to speed up the authentication process.

We can ask each user to set an identifier, when returning the encrypted challenge, the user also send its identifier. So that the authentication process can be: first find the identifier in the database, and use its private key to encrypt the challenge message and check whether it matches. If so, then the user is accepted. 

We here to prove that sending the identifier will leak no extra information of the user.

- First, adding an identifier will make no difference on the server side. The private key itself has been an identifier for the server to identify the user, so the user leaks no extra information on the server side.
- If there is someone sniffing the traffic of the user, the extra identifier means nothing as it can be a totally random sequence. Only knowing one's identifier will do no help on getting its private key.
- If there is someone sniffing the traffic of the server, the extra identifier will not leak privacy either, because:
   - If the packet is directly sent from user to server, then the sniffer will directly know the IP address of the user, the identifier makes no sense
   - If the packed is relayed because of anonymity, then only getting the identifier does no help on knowing who the user is, as the identifier can be randomly generated.

There can also be method to change the identifier, for example after each session.


### Share your thoughts on the course

#### a. To what extent do you devote your time and energy to labs? How do you overcome the associated challenges?
There is adequate hints on Lab 1, so I actually only got stuck no more than 3 times in it. But as for Lab 2, the environment is not so easy to setup, which took me some time. Also, I tried to dig deeper on Lab 2 so that the victim can really access the phishing website; Though I finally failed because I couldn't sniff any TCP packets (maybe also because of the environment), I learnt a lot during this trial. Lab 3 took me several days as the solutions were not that straightforward. Although we could find the solutions to these challenges, they are doing not the same thing as the lab requirements. So I spent a lot of time understanding the source code or the solutions and find my way to complete the challenges (I even learnt to write web crawler to do the Blind SQL Injection 😵).


#### b. Do you think that you have gradually cultivated a research/security mindset? What is the most useful idea that you learned during this process?
Yes. In my opinion, other courses like software security or system security is kind of far from us if we are not deep into those fields, but network security is actually more close to our daliy life. The vulnerabilities of network, especially websites are obvious and kind of easy to exploit (where we need not to use gdb and read the assembly codes🤢), so they can impress me deeper.<br />The most useful idea might be avoiding to leave vulneralibities on SQL queries or website paths or other related issues when writing a web service (as this might be the only related thing I will work on 😜).


#### c. Provide an example to showcase how you leverage that useful idea to facilitate problem solving in study or life.
In last semester, I took a course where we were asked to write a website for note management. We were told not to directly put the actual path in the server into the URL, and were asked to use some tools instead of directly construct SQL queries in our codes. I was not so clear about why we would do that, but after taking Network Security, especially after finishing Lab 3, I was totally clear about that. After learning about these, when I write a website or some other service, I can have a basic knowledge on the risks of it and can take some actions to avoid them.


### Design a question that you think is feasible as an exam question 

#### a. Which topic among the lectures you would like to consider?
Web security!


#### b. Describe a (sufficiently complex) question;
Give a webpage (maybe screenshot + HTML), where user can login, change password, change name, and the changes are in the URL like `?change_name=xyx`. After logging in, the website will show some words like `Welcome, <name>`, and there will be a list of login record of all users in a table in a format like `name, id, login time`. Users can also query the login record of a given name.

Question: list 2 of the possible vulnerablilites, show an example and propose defenses.


#### c. Provide also a correctsample solution, thanks.
If the query input is not filtered properly, there are risks on SQL injection. The changing name and password methods has a risk of CSRF. The welcome message has a risk of reflected XSS. The login record has a risk of stored XSS.
