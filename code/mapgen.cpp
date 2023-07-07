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

	int cnt = d1(gen);
	const int WALL = 395, FLOOR = -1;
	ofstream f;
	f.open("../map/map.csv", ios::out | ios::in | ios::trunc); 
	if(f.is_open()){	
	for(int i = 0; i < N; i++){
		for(int j = 0; j < M; j++){
			if( i == 0 || i == N-1 || j == 0 || j == M-1){
				f<<WALL;
			}
			else{
				if( cnt && d2(gen) == 5  ){
					f<<d3(gen);	
					cnt--;
				}
				else{
					f<<FLOOR;
				}
			}

			if(j < M-1) f << ',';
		}
		f<<'\n';
	}
	f.close();
	}
	else{
	cout << "deu ruim\n";
}		
	return 0;
}
