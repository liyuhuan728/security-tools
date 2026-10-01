#include<bits/stdc++.h>
using namespace std;
int main()
{
	double m,h;
	cin>>m>>h;
	h=h*h;
	m=m/h;
	if(m<18.5)
	{
		cout<<"Underweight";
	}
	else if(m>=24)
	{
		cout<<m<<endl;
		cout<<"Overweight";
	}
	else{
		cout<<"Normal";
	}
	return 0;
}

