#include<bits/stdc++.h>
using namespace std;
int main()
{
	int a,b,c,d,e,f,g;
	d=0;
	g=0;
	f=0;
	cin>>a;
	if(a%b==0)
	{
		b=0;
		b++;
	}
	if(a>4 and a<=12)
	{
		c=0;
		c++;
	}
	if(a+b==2)
	{
		d=0;
		d++;
	}
	if((c==1||b==1)&&d==0)
	{
		e=0;
		e++;
	}
	if(c==1||b==1)
	{
		f++;
	}
	if(a+b==0)
	{
		g++;
	}
	cout<<d<<f<<e<<g;
	return 0;
}

