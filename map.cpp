#include <iostream>
#include <vector>
#include <cstdlib>





#define PLAYER 394

using namespace std;



int rand_(int a, int b){
    return a + int(rand() % (b - a + 1));
}



int main(int argc, char* argv[]){
    if(argc <= 1){
        puts("falta seed como argumento");
        return 1;
    }
    srand(atoi(argv[1]));

    int N, M ;
    cin >> N;
    cin >> M;

    int min_e, max_e;
    cin >> min_e;
    cin >>max_e;

    vector<vector<int>> m;

    for (int i = 0; i < N ; i ++){
        m.push_back(vector<int>(M));
        for(int j=0 ; j <  M   ; j ++){
            
            if ( i ==0 || j==0 || i == N -1 || j == M -1){
                m[i][j] = 395;
            }else {
                m[i][j] = -1;
            }
        }
        
    }

    FILE * f=  fopen("../map/map.csv", "wb");

    int limit = rand_(min_e, max_e);
    for (int i = 0; i < limit ; i ++ ){
        int e = rand_(390, 393);
        
        int k = rand_(1, N - 2);
        int w = rand_(1, M - 2);
        m[k][w] = e;
    }

    int k = rand_(1, N - 2);
    int w = rand_(1, M - 2);
    m[k][w] = PLAYER;

    for(int i =0; i < N; i ++){
        for(int j =0; j < M ; j ++){
            fprintf(f, "%d", m[i][j]);
            if ( j != M - 1 ){
                fprintf(f, ",");
            }

        }
        fprintf(f,"\n");
    }


    fclose(f);

    return 0;
}