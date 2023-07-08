

#include "Rectangle.hpp"
#include <iostream>


using namespace std;

template<typename T>
Rectangle<T>::Rectangle(T x , T y , T width, T height){

    this->x = x;
    this->y = y;
    this->width = width;
    this->height = height;

}

template<typename T>
bool Rectangle<T>::collide_with(const Rectangle<T>& r) const{
    int r1_top_left_x = this->x - this->width/2;
    int r1_top_left_y = this->y + this->height /2;

    int r1_bottom_right_x = this->x + this->width/2;
    int r1_bototm_right_y = this->y - this->height/2;

    int r2_top_left_x = r.x  - r.width/2;
    int r2_top_left_y = r.y + r.height/2;

    int r2_bottom_right_x = r.x + r.width/2;
    int r2_bottom_right_y = r.y - r.height/2;

    if (r1_top_left_x > r2_bottom_right_x || r2_top_left_x > r1_bottom_right_x){
        return false;
    }

    if(r1_top_left_y < r2_bottom_right_y || r2_top_left_y < r1_bototm_right_y){
        return false;
    }

    return true;

}


template class Rectangle<int>;
template class Rectangle<double>;