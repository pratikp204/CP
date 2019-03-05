/*  Author : Pratik PAtil 
    Problem : https://www.spoj.com/problems/STPAR/       
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
	    int n;
	    cin>>n;
	    VI inputs(n);
	    REP(i,n) std::cin >> inputs[i];
	    int curr_order_no=1;
	    bool flag=true;
	    stack<int> lane;
	    REP(i,n){
	        if(curr_order_no==inputs[i]){
	            curr_order_no++;
	        }
	        else if(!lane.empty() && lane.top()==curr_order_no){
	                lane.pop();
	                curr_order_no++;
	        }
	        else {
	            lane.push(inputs[i]);
	        }
	    }
	   // while(!lane.empty()){std::cout << lane.top()<<" "<<curr_order_no << std::endl;curr_order_no++;lane.pop();}
	    while(!lane.empty()){
	        if(lane.top()==curr_order_no){curr_order_no++;lane.pop();}
	        else{flag=false;break;}
	    }
	    if(flag) cout<<"yes \n";
	    else cout<<"no \n";
	}
    
    
    
    return 0;
}
