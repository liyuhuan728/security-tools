#include<bits/stdc++.h>
using namespace std;
int main()
{
	int x,y;
	cin>>x>>y;
	if(x>=y)
	{
		if(x==y)
		{
			cout<<"equal probability";
		}
		else{
			cout<<"NO";
		}
	}
	else{
		cout<<"YES";
	}
	return 0;
}

