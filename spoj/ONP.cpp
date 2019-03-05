/*  Author : Pratik Patil 
    Problem : https://www.spoj.com/problems/ONP/       
*/
#include<bits/stdc++.h>
using namespace std;

#define FOR(i,a,b) for(int i=a;i<b;i++)
#define FORD(i,a,b) for(int i=a;i>=b;i--)
#define REP(i,n) FOR(i,0,n)
#define PB push_back
#define ITER(i,a) for( typeof(a.begin()) i=a.begin();i!=a.end();i++)	
#define mod 1000000007
#define MAXN 1000010
#define MP make_pair
#define INF mod
typedef pair<int,int>   PI;
typedef vector<int> VI;
typedef long long int LL;

int main(){

	int t;
	scanf("%d\n",&t);
	while(t--)
	{
	    string inputs;
	    cin>>inputs;
	    string ans;
	    std::stack<char> st ;
	    FOR(i,0,inputs.length()){
	        if(inputs[i]-'a'>=0 && inputs[i]-'z'<=0){
	            ans+=inputs[i];
	        }
	        else if(inputs[i]=='(') st.push('(');
	        else if(inputs[i]==')') {
	            while(st.top()!='('){ ans+=st.top();st.pop();}
	            st.pop();
	        }
	        else st.push(inputs[i]);
	    }
	    std::cout << ans << std::endl;
	}
	return 0;
}
