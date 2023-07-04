#include "utils.hpp"

#include <iostream>
#include <random>


int randInt(int a , int b){
    if (b < a){
        int aux = a;
        a = b;
        b = aux;
    }
    return a + rand()%( b - a + 1);
}