#ifndef RECTANGLE_HPP
#define RECTANGLE_HPP

using namespace std;

template<typename T>
class Rectangle{
    public:

    T x;
    T y;
    T width;
    T height;

    Rectangle(T x, T y , T width, T height);

    bool collide_with(const Rectangle<T>& r) const;


};



#endif 