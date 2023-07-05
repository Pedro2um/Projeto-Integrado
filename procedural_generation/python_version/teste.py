import numpy as np
from typing import List
from random import randint
import math


DEFAULT_SIZE = 20


from numba import jit, int32
from numba.experimental import jitclass

spec = [
    ('x', int32),
    ('y', int32),
    ('width', int32),
    ('height', int32)
]

@jitclass(spec)
class Rectangle:
    
    
    def __init__(self,x, y, width, height):
        self. x = x
        self.y = y
        self.width = width
        self.height = height

@jit(nopython = True)
def collide_with(rec1: Rectangle , rec2: Rectangle):
    r1_top_left_x = rec1.x - rec1.width/2
    r1_top_left_y = rec1.y + rec1.height/2 

    r1_bottom_right_x = rec1.x + rec1.width/2 
    r1_bottom_right_y =  rec1.y - rec1.height/2
    
    r2_top_left_x =  rec2.x -  rec2.width/2
    r2_top_left_y =  rec2.y +  rec2.height/2 

    r2_bottom_right_x =  rec2.x +  rec2.width/2 
    r2_bottom_right_y =   rec2.y - rec2.height/2
    
    if r1_top_left_x > r2_bottom_right_x or r2_top_left_x > r1_bottom_right_x:
        return False
        
    if r1_top_left_y < r2_bottom_right_y or r2_top_left_y < r1_bottom_right_y:
        return False
        
    return True

@jit(nopython = True)
def move(rec1: Rectangle , vector: list):
    rec1.x += round(vector[0])
    rec1.y += round(vector[1])

@jit(nopython = True)
def rec_str(rec: Rectangle):
    string_ = str(rec.x) + ' ' + str(rec.y) + ' ' + str(rec.width) + ' ' + str(rec.height)
    return string_

@jit(nopython = True)
def create_rectangles_and_distribute( numberRectangles: int, radious: int):
    
    rectangles = []
    counter = 0
    for i in range(numberRectangles):
        
        h = None
        w = None
        ratio =1
            
        while True:
            counter +=1
            amostras = np.random.normal(DEFAULT_SIZE, DEFAULT_SIZE/2, 2 )
            h = amostras[0]
            w = amostras[1]
            
            if h ==0 or w == 0:
                continue
            
            h = math.ceil(abs(h))
            w = math.ceil(abs(w))
            
            if h%2 !=0:
                h +=1
            if w%2 != 0:
                w +=1
            
            ratio = w/h
            
            if  (ratio <= 0.5 or ratio >= 2 or w < DEFAULT_SIZE/10 or h < DEFAULT_SIZE/10):
                continue
            break
                    
        x = randint(0 , radious)
        y = randint(0, radious) 
            
        if(randint(0 ,1) == 1):
            x *= -1
        if(randint(0, 1) ==1):
            y *=-1
            
        rec = Rectangle(x, y, w, h)
        rectangles.append(rec)
    
    
    return rectangles



@jit(nopython = True)
def normalize_vector(v: list):
    
    sqrt_sum = 0
    for x in v:
        sqrt_sum += x*x
    sqrt_sum = math.sqrt(sqrt_sum)
    
    N = len(v)
    for i in range(N):
        v[i] /= sqrt_sum

@jit(nopython = True)
def separation_steering(rectangles: List[Rectangle]):


    collision_flag = 0 
    N = len(rectangles)
    
    while True:
        
        collision_flag = 0
        for i in range(N):
            for j in range(N):
                
                if i == j or (not collide_with(rectangles[i], rectangles[j])):
                    continue
                
                collision_flag = 1 
                
                v2d = [0,0]
                v2d[0] = rectangles[j].x - rectangles[i].x
                v2d[1] = rectangles[j].y - rectangles[i].y
                
                if v2d[0] ==0 and v2d[1] ==0:
                    index = randint(0 ,1)
                    v2d[index] =1
                
                normalize_vector(v2d)
                move(rectangles[j], v2d)
                v2d[0] *=-1
                v2d[1] *= -1
                move(rectangles[i], v2d)
                
        if(collision_flag):
            continue
        
        break


@jit(nopython = True)
def generate_map():
    
    rectangles = create_rectangles_and_distribute(100 , DEFAULT_SIZE*2)
    

        
    separation_steering(rectangles= rectangles)

        
    menor_x = rectangles[0].x - rectangles[0].width/2
    maior_y = rectangles[0].y + rectangles[0].height/2
 
        
    for rect in rectangles:
        menor = rect.x - rect.width/2
        maior = rect.y + rect.height/2
        
        if menor < menor_x:
            menor_x = menor
        if maior > maior_y:
            maior_y = maior

    OFFSET = 15
    
    L = -1 
    C = - 1
    
    for rect in rectangles:
        rect.x = rect.x - menor_x + OFFSET
        rect.y = maior_y - rect.y + OFFSET
        
        
        l = rect.y + rect.height/2
        c = rect.x + rect.width/2
        
        if l > L:
            L = l
        if c > C:
            C = c

    L = int(L  + (OFFSET + 1))
    C = int(C + (OFFSET  +1))
    
    print(L, C)
    
  
    
    matrix = []
    
    for i in range(L):
        linha = []
        for j in range(C):
            linha.append(0)
        matrix.append(linha)
    
    
    identifier = 7
    for rect in rectangles:
        print(rec_str(rect))
        top_left_x =  int(rect.x - rect.width/2)
        top_left_y = int(rect.y - rect.height/2) 
        for i in range(rect.height):
            for j in range(rect.width):
                matrix[top_left_y +  i][top_left_x + j] = identifier
    

    for i in range(len(matrix)):
        line = ""
        for j in range(len(matrix[i])):
            line += str(matrix[i][j]) + " "
        print(line)
        
    
generate_map()