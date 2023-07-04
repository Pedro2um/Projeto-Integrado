#include <bits/stdc++.h>
#include <random>
using namespace std;

int main(int argc, char* argv[]){
	//precisa de 3 argumentos na hora de executar
	if(argc<=4){
		cout<<"falta argumentos\n";
		return 1;
	}
	srand(time(NULL));	
	int N = atoi(argv[1]); //linhas
	int M = atoi(argv[2]); //colunas
	int A = atoi(argv[3]); //min numero de inimigos
	int B = atoi(argv[4]); //max numero de inimigos
	int a = 1, b = 10, x = 8, y = 10;
	
	random_device rd;
    	mt19937 gen(rd());	
	//gen.seed(time(NULL));
	uniform_int_distribution<int> d1(A,B), d2(a,b), d3(x,y);

	const int number_of_experiments = d1(gen);
	const int WALL = 395, FLOOR = -1;	
	for(int i = 0; i < N; i++){
		for(int j = 0; j < M; j++){
			if( i == 0 || i == N-1 || j == 0 || j == M-1){
				cout<<WALL;
			}
			else{
				if( d2(gen) == 5  ){
					cout<<d3(gen);	
				}
				else{
					cout<<FLOOR;
				}
			}

			if(j < M-1) cout << ',';
		}
		cout<<'\n';
	}
		
	return 0;
}
