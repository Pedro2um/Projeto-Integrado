from typing import List
from random import randint
from random import choice
import math
from scipy.spatial import Delaunay
from kruskal import kruskal_algorithm

from numpy.random import normal

DEFAULT_SIZE = 20

## classe retangulo que será usada tanto para salas como corredores, guarda as posições x e y como topleft do retangulo e outras informações
class Rectangle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.distance_from_center = 0
        self.area = width * height

    ## define a distancia do centro do retângulo para o cetro de um plano --> (0,0)
    def set_distance_from_center(self):
        x_center = self.x + self.width//2
        y_center = self.y  - self.height //2
        self.distance_from_center = math.sqrt(x_center*x_center + y_center*y_center)

    ## verifica se o retângulo collide com outro 'other'
    def collide_with(self, other):
        r1_top_left_x = self.x
        r1_top_left_y = self.y

        r1_bottom_right_x = self.x + self.width - 1
        r1_bottom_right_y = self.y - self.height + 1

        r2_top_left_x = other.x 
        r2_top_left_y = other.y

        r2_bottom_right_x = other.x + other.width - 1
        r2_bottom_right_y = other.y - other.height + 1

        if r1_top_left_x > r2_bottom_right_x or r2_top_left_x > r1_bottom_right_x:
            return False

        if r1_top_left_y < r2_bottom_right_y or r2_top_left_y < r1_bottom_right_y:
            return False

        return True

    ## move o retangulo na direção e na unidade do vetor passado ( vetor 2D )
    def move(self, vector: List):

        self.x += round(vector[0])
        self.y += round(vector[1])

    ## formatação de string de um retângulo para impressão e debug
    def __str__(self) -> str:
        string_ = str(self.x) + ' ' + str(self.y) + ' ' + str(self.width) + ' ' + str(self.height)
        return string_


DESVIO_PADRAO = DEFAULT_SIZE / 4

## cria os retangulos e os distribui dentro de um circulo de raio passado 
def create_rectangles_and_distribute(numberRectangles, radious):
    rectangles = []

    for i in range(numberRectangles):

        h = None
        w = None
        ratio = 1

        while True:
            ## criando largura e altura randomizadas
            amostras = normal(DEFAULT_SIZE, DESVIO_PADRAO, 2)
            h = amostras[0]
            w = amostras[1]

            if h == 0 or w == 0:
                continue

            h = math.ceil(abs(h))
            w = math.ceil(abs(w))

            ## impede retângulos de terem tamanho impar para que tenha um meio (center) bem definido no campo dos inteiros 
            if h % 2 == 0:
                h += 1
            if w % 2 == 0:
                w += 1

            if (randint(0, 1)):
                aux = h
                h = w
                w = aux

            ratio = w / h
            ## limitações para as salas nao ficarem muito pequenas e nem muito esticadas 
            if (ratio <= 0.5 or ratio >= 2 or w < 10 or h < 10):
                continue
            break


        ## escolhendo coordenadas para o centro do retângulo 
        x = randint(0, radious)
        y = randint(0, radious)

        if (randint(0, 1) == 1):
            x *= -1
        if (randint(0, 1) == 1):
            y *= -1

        ## ajustando para passar o top left 
        rec = Rectangle(x - w//2, y + h//2, w, h)
        rectangles.append(rec)

    return rectangles

## função que normaliza um vetor
def normalize_vector(v: List):
    sqrt_sum = 0
    for x in v:
        sqrt_sum += x * x
    sqrt_sum = math.sqrt(sqrt_sum)

    N = len(v)
    for i in range(N):
        v[i] /= sqrt_sum

## função de separação dos retângulos 
def separation_steering(rectangles):
    collision_flag = 0
    N = len(rectangles)
    counter = 0
    while True:

        collision_flag = 0
        for i in range(N):
            for j in range(N):

                if i == j or (not rectangles[i].collide_with(rectangles[j])):
                    continue

                counter += 1
                collision_flag = 1

                v2d = [0, 0]
                v2d[0] = (rectangles[j].x + rectangles[j].width//2 ) - (rectangles[i].x + rectangles[i].width//2 )
                v2d[1] = (rectangles[j].y - rectangles[j].height//2 ) - (rectangles[i].y - rectangles[j].height//2 )

                if v2d[0] == 0 and v2d[1] == 0:
                    index = randint(0, 1)
                    v2d[index] = 1

                ## movendo retangulos em direções opostas
                normalize_vector(v2d)
                rectangles[j].move(v2d)
                v2d[0] *= -1
                v2d[1] *= -1
                rectangles[i].move(v2d)

        if (collision_flag):
            continue

        break


N_RECTANGLES = 30

## distancia entre dois pontos de mesma dimensão genérica
def point_distance(tuple1, tuple2):
    N = len(tuple1)
    sum_ = 0;
    for i in range(N):
        sum_ += (tuple1[i] - tuple2[i]) * (tuple1[i] - tuple2[i])
    return math.sqrt(sum_)


## função com a lógica para o desenhar os corredores na matrix
def draw_halls(matrix , halls):
   
    for hall in halls:
        
        hall_topleft_x = hall.x
        hall_topleft_y = hall.y 
        width = hall.width
        height = hall.height
        
        for i in range(height):
            for j in range(width):
                i_ = i + hall_topleft_y
                j_ = j + hall_topleft_x
                value = matrix[i_][j_]
                
                if value ==2 :
                    continue
                
                if j == 0 or j == width -1 or i ==0 or i == height -1:
                    if value != 8 and value !=7 :
                        matrix[i_][j_] = 5
                else:
                    matrix[i_][j_] = 8
                    
        ## ta de lado 
        if  height == 5:
            for i in range(3):
                value = matrix[(i + 1)  + hall_topleft_y][hall_topleft_x]
                if value == 7:
                    matrix[(i + 1)  + hall_topleft_y][hall_topleft_x] = 8
                
                value =  matrix[(i + 1)  + hall_topleft_y][hall_topleft_x + width -1 ]
                if value == 7:
        
                    matrix[(i + 1)  + hall_topleft_y][hall_topleft_x + width -1 ] = 8
        else: ## ta em pé
            
            for i in range(3):
                value = matrix[hall_topleft_y][hall_topleft_x + (i +1)]
                if value == 7:
                    value = matrix[hall_topleft_y][hall_topleft_x + (i +1)] = 8
                value = matrix[hall_topleft_y + height - 1][hall_topleft_x +  (i + 1 ) ]
                if value == 7:
                    matrix[hall_topleft_y + height - 1][hall_topleft_x +  (i + 1 ) ] = 8
        
    return matrix

## gera os corredores
def make_halls(mst, main_rooms):

    corredores = []
    
    for edge in mst:
        rect1 = main_rooms[edge[0]]
        rect2 = main_rooms[edge[1]]

        ## escolhendo retângulo mais abaixo como rect1 
        if rect1.y < rect2.y :
            aux = rect1
            rect1 = rect2
            rect2 = aux
        
        rect1_center = (rect1.x  + rect1.width //2, rect1.y + rect1.height//2 )
        rect2_center = (rect2.x + rect2.width //2 , rect2.y + rect2.height //2)
    
        ## separação em casos
        
        ## rect1 está mais para a esquerda
        if rect1_center[0] >= rect2_center[0]:
            
            x1 = rect1.x
            x2 = rect1.x  + rect1.width - 1

            y1 = rect2.y
            y2 = rect2.y + rect2.height - 1 

            
            ## rect1 está mas abaixo de rect2
            if x1 <= rect2_center[0] <= x2:
                
                n = int(rect2_center[0] - x1)
                x_0 = rect2_center[0] - 2

                if n < 2:
                    x_0 += (2 - n)

                y_0 = rect1.y

                y_ = int(y_0)
                x_ = int(x_0)

              
                
                y_lim = rect2.y + rect2.height - 1
                corredores.append(Rectangle(x_0 , y_lim ,5, (y_ - y_lim + 1 ) ))
            
            ## rect1 está mais ao lado direito de rect2
            elif y1 <= rect1_center[1] <= y2:
            
    
                n = y2 - rect1_center[1]

                y_0 = rect1_center[1] + 2

                if n < 2:
                    y_0 -= (2 - n)

                x_0 = rect1.x

                x_ = int(x_0)
                y_ = int(y_0)

                x_lim = rect2.x + rect2.width - 1 
                corredores.append(Rectangle( x_lim , y_0 -5 + 1 , x_ - x_lim + 1 , 5))
            
            ##rect1 está abaixo e ao lado de rect2
            else:
            
                x_0 = rect1.x 
                y_0 = rect1_center[1]

                n = y_0 - (rect2.y + rect2.height -1)
                n -= 1

                if n < 2:
                    y_0 += (2 - n)
               
                y_0 += 2 
                x_ = int(x_0)
                y_ = int(y_0)

                
                x_lim = rect2_center[0] + 1
                
                corredores.append(Rectangle(x_lim, y_0 -5 + 1,  (x_ - x_lim + 1), 5 ))
              
                n = x_0 - rect2_center[0]
                n -=1 
               
                x_0 = rect2_center[0] + 2
                
                if n < 2:
                    x_0 -= (2 - n)

                y_ = int(y_0)
                x_ = int(x_0)
                
                
                y_lim = rect2.y + rect2.height - 1
                corredores.append( Rectangle (x_ - 5 + 1, y_lim, 5, y_ - y_lim + 1 ))
        
        ## caso rect1 está a esquerda de rect2  
        elif rect1.x < rect2.x:
          
            x1 = rect1.x
            x2 = rect1.x + rect1.width -1 
            
            y1 = rect2.y 
            y2 = rect2.y + rect2.height - 1

            ## rect1 embaixo de rect2 mais a esquerda
            if x1 <= rect2_center[0] <= x2:
                
            
                n = x2 - rect2_center[0]
                
                x_0 = rect2_center[0] + 2
                if n < 2:
                    x_0 -= (2 - n)

                y_0 = rect1.y
               
                x_ = int(x_0)
                y_ = int(y_0)
                

                y_lim = rect2.y + rect2.height - 1
                corredores.append(Rectangle(x_0 -5 + 1, y_lim, 5, (y_ - y_lim + 1)))
            
            ## rect1 está mais a esquerda e acima ao lado de rect2
            elif y1 <= rect1_center[1] <= y2:
                
        
                n = y2 - rect1_center[1]
                
                
                y_0 = rect1_center[1] + 2

                if n < 2:
                    y_0 -= (2 -n)
                    
                x_0 = rect1.x + rect1.width - 1 
                x_ = int(x_0) 
                y_ = int(y_0)

                x_lim = rect2.x
                corredores.append(Rectangle(x_0, y_0 -5  + 1, (x_lim - x_ + 1 ), 5))
                
            ## rect1 está ao lado esquerdo e abaixo de rect2 
            else:
                
                
                x_0 = rect1.x + rect1.width - 1 
                y_0 = rect1_center[1]
                
                
                n = y_0 - (rect2.y + rect2.height - 1 )
                n -= 1

                if n < 2:
                    y_0 += (2 - n)

                y_0 += 2
                x_ = int(x_0) 
                y_ = int(y_0) 
                
                
                x_lim = rect2_center[0] - 1 
                
                corredores.append(Rectangle(x_0, y_0 -5 + 1, (x_lim - x_ + 1 ), 5))
                
               
               
                n = rect2_center[0] - x_0
                n -=1 

                x_0 = rect2_center[0] - 2

                if n < 2:
                    x_0 += (2 - n)

                y_ = int(y_0)
                x_ = int(x_0)
                
                y_lim = rect2.y + rect2.height - 1

                corredores.append(Rectangle(x_0, y_lim, 5 , (y_ - y_lim + 1)))
                
    
    
    return corredores

## função que retorna as arestas não repetidas da triangução do centro dos retângulos
def make_triangulation_edges(points):
    
    triangles = Delaunay(points).simplices

    edges_ids = set({})
    edges = []

    for tri in triangles:

        for i in range(2):
            p1 = tri[i]
            p2 = tri[i + 1]

            if p1 > p2:
                aux = p1
                p1 = p2
                p2 = aux

            edge = (p1, p2, point_distance(points[p1], points[p2]))

            id_tuple = (p1, p2)
            if id_tuple not in edges_ids:
                edges.append(edge)
                edges_ids.add(id_tuple)

        p1 = tri[2]
        p2 = tri[0]

        if p1 > p2:
            aux = p1
            p1 = p2
            p2 = aux

        edge = (p1, p2, point_distance(points[p1], points[p2]))

        id_tuple = (p1, p2)
        if id_tuple not in edges_ids:
            edges.append(edge)
            edges_ids.add(id_tuple)
    
    return edges


## converte as coordenadas de vários pontos cartesianos para uma matriz, o ponto mais acima e esquerda define a origem da matriz, o ponto mais a direita e abaixo define a largura e altura da matrix
def convert_coordenates_and_make_matrix(rectangles):
   
    ## PROCURANDO PONTO NO PLANO MAIS A ESQUERDA E MAIS ACIMA, OU SEJA, A PONTA SUPERIOR ESQUERDA QUE LIMITA O MAPA
    menor_x = int(rectangles[0].x)
    maior_y = int(rectangles[0].y)

    for rect in rectangles:
        menor = rect.x
        maior = rect.y

        if menor < menor_x:
            menor_x = menor
        if maior > maior_y:
            maior_y = maior

    
    ## ESPAÇO A MAIS CRIADO EM VOLTA DO MAPA OU SEJA, SERAO 15 LINHAS ANTES E DEPOIS E 15 COLUNAS ANTES E DEPOIS A MAIS QUE SERAO GERADAS PARA PREENCHER UM GAP NO MAPA
    OFFSET = 15

    L = -1
    C = - 1

    ##RECALCULANDO AS NOVAS COORDENADAS PARA GERAR A MATRIZ, COMO PONTO 0,0 DA MATRIZ SENDO O PONTO SUPERIOR ESQUERDO 
    for rect in rectangles:
        rect.x = rect.x - menor_x + OFFSET
        rect.y = maior_y - rect.y + OFFSET

        l = rect.y + rect.height - 1 
        c = rect.x + rect.width  - 1

        if l > L:
            L = l
        if c > C:
            C = c

    L = int(L + (OFFSET + 1))
    C = int(C + (OFFSET + 1))


    matrix = []

    for i in range(L):
        linha = []
        for j in range(C):
            linha.append(0)
        matrix.append(linha)
    
    return matrix

## função com a lógica para o desenho das salas na matriz
def draw_rooms(matrix , main_rooms):
    
    rectangles = main_rooms
    
    wall_id = 7
    inter_id = 2
    for rect in rectangles:
        top_left_x = rect.x
        top_left_y = rect.y
        for i in range(rect.height):
            for j in range(rect.width):

                if i == 0 or j == 0 or i == rect.height - 1 or j == rect.width - 1:
                    matrix[top_left_y + i][top_left_x + j] = wall_id
                else:
                    matrix[top_left_y + i][top_left_x + j] = inter_id

    return (matrix, rectangles)

# printa matrix no arquivo para visualização
def print_matrix_on_file( matrix, path):
    N = len(matrix)
    M = len(matrix[0])

    arquivo = open(path, 'w', encoding='utf-8')

    for i in range(N):
        for j in range(M):
            if j != M - 1:
                print(matrix[i][j], end=',', file=arquivo)
            else:
                print(matrix[i][j], end='', file=arquivo)
        print('', file=arquivo)

    arquivo.close()

def generate_map():
    
    
    ## cria 
    rectangles: List[Rectangle] = create_rectangles_and_distribute(N_RECTANGLES, DEFAULT_SIZE//2)

    
    ## sapara
    separation_steering(rectangles=rectangles)

    
    ## selecionando maiores como principais
    for rect in rectangles:
        rect.set_distance_from_center()

    rectangles.sort(key=lambda rect: rect.area, reverse=True)

    percent = math.ceil(N_RECTANGLES * (1 / 2))
    biggest_rectangles = []

    for i in range(percent):
        biggest_rectangles.append(rectangles[i])


    main_rooms = []

    for i in range(randint(3, 5)):
        main_rooms.append(biggest_rectangles[i])

    
    ## transformando centro em pontos para triangulação
    points = []
    for rect in main_rooms:
        points.append((rect.x + rect.width//2, rect.y - rect.height//2 ))

 
    
    edges = make_triangulation_edges(points)
    mst = kruskal_algorithm(points, edges)


    ## convertendo coordenadas
    matrix = convert_coordenates_and_make_matrix(main_rooms)
    # criando corredores
    halls = make_halls(mst, main_rooms)
    ## desenhando as salas na matriz
    draw_rooms(matrix, main_rooms)
    ## desenhando corredores na matriz 
    draw_halls(matrix, halls)
    
    ## printando matriz no arquivo 
    print_matrix_on_file(matrix, 'map_generated/map.csv')
    
    ## retornando matriz para o programa principal
    return (matrix, main_rooms)

generate_map()
