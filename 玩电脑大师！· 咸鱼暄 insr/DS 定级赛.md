```cpp
#include<iostream>

using namespace std;

int main(){
	int n;
	cin >> n;
	cout << n / 15 << " " << n / 20 << " " << n * 90 << endl;
	
	return 0;
}
```
```cpp
#include<iostream>

using namespace std;

int sc[] = {11500/2, 27500/2, 43500/2, 59500/2, 0, 0, 0, 0, 0, 155500/2, 0x7fffffff};
			/* 10   	9		8		7		6  5  4  3  2   1			0*/
int main(){
	int d = (sc[9] - sc[3]) / 6;
	for(int i = 4; i < 10; i++)
		sc[i] = sc[i-1] + d;
	
/*	for(int i = 0; i < 11; i++)
		cout << sc[i] << " ";
	cout << endl;*/
	
	int acc, ans = 0;
	cin >> acc;
	for(; ans < 11; ans++)
		if(acc <= sc[ans])	break;
	cout << 10 - ans << endl;
}
```
```cpp
#include<iostream>

using namespace std;

int main(){
	int n;
	cin >> n;
	while(n--){
		int x, y, z;
		cin >> x >> y >> z;
		if(x*x + y*y + z*z == 3*x*y*z)
			cout << "Yes" << endl;
		else
			cout << "No" << endl;
	}
	return 0;
}
```
```cpp
#include<iostream>

using namespace std;
int sheng[] = {0, 3, 4, 2, 5, 1}, ke[] = {0, 2, 5, 4, 1, 3};

int main(){
	int n;
	cin >> n;
	while(n--){
		int x, y;
		cin >> x >> y;
		if(sheng[x] == y)		cout << x << " sheng " << y << endl;
		else if(sheng[y] == x)	cout << y << " sheng " << x << endl;
		else if(ke[x] == y)		cout << x << " ke " << y << endl;
		else if(ke[y] == x)		cout << y << " ke " << x << endl;
	}
	return 0;
}
```
```cpp
#include<iostream>
#include<string>
#include<cstring>
using namespace std;
char text[100];
void judge(int len){
	int i = 0;
	while(i <= len - 3){
		if(text[i] == 'P' && text[i+1] == 'T' && text[i+2] == 'A'){
			cout << "Yes!" << endl;
			return;
		}
		i++;
	}
	cout << "No." << endl;
	return;
}

int main(){
	int n;
	cin >> n;
	getchar();
	while(n--){
		cin.getline(text, 100);
		int textLength = strlen(text);
		if(text[textLength - 1] != '?')
			cout << "enen" << endl;
		else 
			judge(textLength);
	}
	return 0;
}
```
```cpp
#include<iostream>
#include<string>
#include<cstring>
using namespace std;
int n, k, x, mat[105][105], sum[105], temp, flag;
int main(){
	cin >> n >> k >> x;
	for(int i = 0; i < n; i++)
		for(int j = 0; j < n; j++)
			cin >> mat[i][j];
	for(int j = 1, cnt = 0; j < n; j += 2, cnt = (cnt + 1) % k){
		for(int i = n - 1; i > cnt; i--)
			mat[i][j] = mat[i - cnt - 1][j];
		for(int i = 0; i <= cnt; i++)
			mat[i][j] = x;
	}
	/*for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++)
			cout << mat[i][j] << " ";
		cout << endl;
	}*/
	for(int i = 0; i < n; i++){
		int tot = 0;
		for(int j = 0; j < n; j++)
			tot += mat[i][j];
		cout << tot;
		if(i != n - 1) cout << " ";
	}
	cout << endl;
	return 0;
}
```
```cpp
#include<iostream>
#include<string>
#include<cstring>
#include<algorithm>
using namespace std;
struct node{
	string no;
	int scr, rk, lv;
}stu[1005];

bool cmp(node x, node y){
	if (x.scr == y.scr)
		return x.no < y.no;
	return x.scr > y.scr;
}

int lx(int x){
	if(x == 0)	return 0;
	if(x <= 30)	return 1;
	if(x <= 50)	return 2;
	if(x <= 60)	return 3;
	if(x <= 80) return 4;
	if(x <= 100)return 5;
}

int n, l, fullScr[] = {0, 30, 50, 60, 80, 100}, cnt[6], cntb[6];
 
int lev(int x){
	int lv = lx(x);
	if(lv > l)	lv = l;
	return lv;
}

int main(){
	cin >> n >> l;
	for(int i = 0; i < n; i++)
		cin >> stu[i].no >> stu[i].scr;
	int a[] = {1, 3, 4, 2, 5};
	sort(stu, stu + n, cmp);
	
	stu[0].rk = 1;
	stu[0].lv = lev(stu[0].scr);
	for(int j = stu[0].lv; j < 6; j++)
		cnt[j]++;
	for(int j = 0; j <= stu[0].lv; j++)
		cntb[j]++;
		
	for(int i = 1; i < n; i++){
		stu[i].lv = lev(stu[i].scr);
		for(int j = stu[i].lv; j < 6; j++)
			cnt[j]++;
		
		if(stu[i].scr == stu[i-1].scr)	stu[i].rk = stu[i-1].rk;
		else	stu[i].rk = i + 1 - cntb[stu[i].lv+1];
		
		for(int j = 0; j <= stu[i].lv; j++)
			cntb[j]++;
	}
	
	for(int i = 0; i < n; i++){
		cout << stu[i].no;
		if(stu[i].lv){
			cout << " " << stu[i].lv << " " << stu[i].scr << "/"
				 << fullScr[stu[i].lv] << " " << stu[i].rk << "/"
				 << cnt[stu[i].lv];
		}
		cout << endl;
	}
	return 0;
}
```
