#include<iostream>
#include<vector>

using namespace std;

int main(void){
	int x = 5;
	cout << x << endl;
	x = x << 2;
	cout << x << endl;

	return 0;
}
/*
in order to shift the bits, 
5 = 101
shifting it two places results in 
x = 10100 = 20
*/