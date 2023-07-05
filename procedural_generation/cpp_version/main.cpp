#include <iostream>
#include <vector>
#include <time.h>
#include <random>
#include <algorithm>

#include "utils.hpp"
#include "Rectangle.hpp"


using namespace std;

#define DEFAULT_SIZE 20



vector<Rectangle<int>> create_rectangles_and_distribute(int N, int radious){
    vector<Rectangle<int>> v;

    random_device rd;
    default_random_engine generator(rd());
    normal_distribution<double> distribuition (DEFAULT_SIZE , DEFAULT_SIZE/1.1);

   
    for (int i =0  ; i < N ; i ++){
        
        int h;
        int w;
        double ratio= 1;
        do{
          
            double aux = distribuition(generator);
            h = ceil(abs(aux));
            if (h %2 !=0) h ++;
            aux = distribuition(generator);
            w = ceil(abs(aux));
            if (w %2 !=0) w++;
            ratio = ((double)h)/w;

        }while(ratio < 0.7 || ratio > 1.42 || w < DEFAULT_SIZE/10 || h < DEFAULT_SIZE/10);
        
        int x = randInt(0 , radious);
        if( randInt(0, 1)){
            x *= -1;
        }

        int y = randInt(0 , radious);
        if(randInt(0, 1)){
            y*=-1;
        }

        Rectangle<int> r (x , y, w, h);
        v.push_back(r);
    }

    return v;
}



void normalized(double* vec2d){
    double sum = sqrt(vec2d[0]*vec2d[0] + vec2d[1]*vec2d[1]);
   
    vec2d[0] /= sum;
    vec2d[1] /= sum;
}

void move(Rectangle<int>& r, double* vec2d){
    r.x += round(vec2d[0]);
    r.y += round(vec2d[1]);
}

void separation_steering(vector<Rectangle<int>>& rectangles){

    int collision_flag = 0;
    do{

        collision_flag =0 ;
        for(int i =0; i < rectangles.size(); i ++){

            for(int j =0; j < rectangles.size(); j ++){

                if(i == j  || !rectangles[i].collide_with(rectangles[j]) ){
                    continue;
                }

                collision_flag ++;

                double vec2d[2];
                vec2d[0] = rectangles[j].x - rectangles[i].x;
                vec2d[1] = rectangles[j].y - rectangles[i].y;

                if (vec2d[0] ==0 && vec2d[1] ==0){
                    int index = randInt(0 ,1 );
                    vec2d[index] = 1;
                }
                // normalizando
                normalized(vec2d);
                move(rectangles[j], vec2d);
                vec2d[0] *=-1;
                vec2d[1] *=-1;
                move(rectangles[i], vec2d);

            }
        }


    }while(collision_flag);


}


bool sort_comparation_function(Rectangle<int> a, Rectangle<int> b){
    double a_area = a.width*a.height;
    double b_area = b.width*b.height;
    if( a_area > b_area){
        if(a.width > b.width){
            if(a.height > b.height){
                return false;
            }
        }
    }

    return true;
}




int main(void){

    srand(time(0));


    vector<Rectangle<int>> rectangles = create_rectangles_and_distribute( 150 , DEFAULT_SIZE);
    
    
    //cout << "depois" << '\n';

    
    separation_steering(rectangles);

    

    int menor_x = rectangles[0].x - rectangles[0].width/2;
    int maior_y = rectangles[0].y + rectangles[0].height/2;
    

    //procurando o ponto mais a esquerda e mais ao topo 
    for (const auto& r : rectangles){
        int menor = r.x - r.width/2;
        int maior = r.y + r.height/2;

        if(menor < menor_x){
            menor_x = menor;
        }
        if(maior > maior_y){
            maior_y = maior;
        }

    }

    int offset = 15;


    
    
    int L = -1, C = -1;

    // usando o ponto achado anteriormente como ponto 0,0 de uma matriz, porem, todos vao ser afastados por um offset pra baixo e pra direita
    for(auto& r: rectangles){
        r.x = r.x -  menor_x + offset;
        r.y = maior_y - r.y + offset;

        int l, c;

        l = r.y + r.height/2;
        c = r.x + r.width/2;

        if( l > L){
            L = l;
        }

        if(c > C){
            C = c;
        }
       

    }

    

   
    // do ponto mais a direita e mais abaixo, adicionamos também uma quantidade de offset pra direita e pra baixo 
    L += (offset + 1);
    C += (offset + 1);

    vector<vector<int>> m;

    for(int i =0; i< L; i ++){
        vector<int> aux;
        for(int j=0; j < C; j ++){
            aux.push_back(0);
        }
        m.push_back(aux);
    }

    //cout << L << ' ' << C << endl;
    
    /*
        for (const auto& x : rectangles){
        int w = x.width;
        int h = x.height;
        int x_= x.x;
        int y = x.y;
        cout << x_ << ' ' << y << ' ' << w << ' ' << h << '\n';
    }

    */
   
    
    int id = 7;
    for(auto& rec : rectangles){

        int topleft_x = rec.x -rec.width/2;
        int topleft_y = rec.y - rec.height/2;

        for(int i = 0 ; i < rec.height ; i ++){
            for(int j =0; j < rec.width; j ++){
                m[topleft_y+ i][topleft_x + j] = id;
            }
        }
    }

    

    
    
    for(int i =0; i< L; i ++){
        
        for(int j=0; j < C; j ++){
            cout << m[i][j];
            if(j < C -1){
                cout << ',';
            }
        }
        cout << '\n';
       
    }
    
    /*
    double porcentagem = 1.3;
    int threshold = DEFAULT_SIZE*porcentagem;

    vector<Rectangle<int>> big_rooms;
    for(auto & rec: rectangles){

        if(rec.height > threshold && rec.width > threshold){
            big_rooms.push_back(rec);  
        }
    }

    sort(big_rooms.begin(), big_rooms.end(), sort_comparation_function);

    */

    /*
    cout << "big rooms" << endl;
    for(auto& x : big_rooms){
        int w = x.width;
        int h = x.height;
        int x_= x.x;
        int y = x.y;
        cout << x_ << ' ' << y << ' ' << w << ' ' << h << '\n';
    }
    */

    return 0;
}