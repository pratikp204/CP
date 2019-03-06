/* Author : Pratik Patil */
#include<bits/stdc++.h>
using namespace std;
char a[1000004];
char expr[1000004];
int top;
void push(char c){
    if(top==1000003)return;
    top +=1;
    a[top]=c;
}
int pop(){
    top -=1;
    return top;
}
int main(){
    int t;
    cin>>t;
    while(t--){
        top=-1;
        cin>>expr;
        int n=strlen(expr);
        int i,x,l=0;
        for(i=0;i<n;i++){
            if(expr[i]=='<'){ cout<<top<<"\n";push(expr[i]);}
            else{
                x=pop();
                if(x==-1) l=i+1;
                else if(x==-2) break;
            }
        }
        cout<<l<<endl;
    }
    return 0;
}
