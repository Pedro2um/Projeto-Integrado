from typing import List
from random import randint
from random import choice
import math
from scipy.spatial import Delaunay
from kruskal import kruskal_algorithm

from numpy.random import normal

DEFAULT_SIZE = 20


class Rectangle:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.distance_from_center = 0
        self.area = width * height

    def set_distance_from_center(self):
        self.distance_from_center = math.sqrt(self.x * self.x + self.y * self.y)

    def collide_with(self, other):
        r1_top_left_x = self.x - self.width / 2
        r1_top_left_y = self.y + self.height / 2

        r1_bottom_right_x = self.x + self.width / 2
        r1_bottom_right_y = self.y - self.height / 2

        r2_top_left_x = other.x - other.width / 2
        r2_top_left_y = other.y + other.height / 2

        r2_bottom_right_x = other.x + other.width / 2
        r2_bottom_right_y = other.y - other.height / 2

        if r1_top_left_x > r2_bottom_right_x or r2_top_left_x > r1_bottom_right_x:
            return False

        if r1_top_left_y < r2_bottom_right_y or r2_top_left_y < r1_bottom_right_y:
            return False

        return True

    def move(self, vector: List):

        self.x += round(vector[0])
        self.y += round(vector[1])

    def __str__(self) -> str:
        string_ = str(self.x) + ' ' + str(self.y) + ' ' + str(self.width) + ' ' + str(self.height)
        return string_


DESVIO_PADRAO = DEFAULT_SIZE / 4


def create_rectangles_and_distribute(numberRectangles, radious):
    rectangles = []

    for i in range(numberRectangles):

        h = None
        w = None
        ratio = 1

        while True:

            amostras = normal(DEFAULT_SIZE, DESVIO_PADRAO, 2)
            h = amostras[0]
            w = amostras[1]

            if h == 0 or w == 0:
                continue

            h = math.ceil(abs(h))
            w = math.ceil(abs(w))

            if h % 2 != 0:
                h += 1
            if w % 2 != 0:
                w += 1

            if (randint(0, 1)):
                aux = h
                h = w
                w = aux

            ratio = w / h

            if (ratio <= 0.5 or ratio >= 2 or w < 10 or h < 10):
                continue
            break

        x = randint(0, radious)
        y = randint(0, radious)

        if (randint(0, 1) == 1):
            x *= -1
        if (randint(0, 1) == 1):
            y *= -1

        rec = Rectangle(x, y, w, h)
        rectangles.append(rec)

    return rectangles


def normalize_vector(v: List):
    sqrt_sum = 0
    for x in v:
        sqrt_sum += x * x
    sqrt_sum = math.sqrt(sqrt_sum)

    N = len(v)
    for i in range(N):
        v[i] /= sqrt_sum


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
                v2d[0] = rectangles[j].x - rectangles[i].x
                v2d[1] = rectangles[j].y - rectangles[i].y

                if v2d[0] == 0 and v2d[1] == 0:
                    index = randint(0, 1)
                    v2d[index] = 1

                normalize_vector(v2d)
                rectangles[j].move(v2d)
                v2d[0] *= -1
                v2d[1] *= -1
                rectangles[i].move(v2d)

        if (collision_flag):
            continue

        break


N_RECTANGLES = 30


def point_distance(tuple1, tuple2):
    N = len(tuple1)
    sum_ = 0;
    for i in range(N):
        sum_ += (tuple1[i] - tuple2[i]) * (tuple1[i] - tuple2[i])
    return math.sqrt(sum_)


def all_rooms(mst, main_rooms, rectangles):
    minor_rooms = []

    for edge in mst:
        rect1 = main_rooms[edge[0]]
        rect2 = main_rooms[edge[1]]

        dy = rect1.y - rect2.y
        dx = rect1.x - rect2.x

        if dy == 0:

            Y = rect1.y

            if rect1.x > rect2.x:
                aux = rect1
                rect1 = rect2
                rect2 = aux

            x1 = rect1.x + rect1.width // 2
            x2 = rect2.x - rect2.width // 2

            for rectangle in rectangles:
                y1 = rectangle.y - rectangle.height // 2
                y2 = rectangle.y + rectangle.height // 2
                if (x1 < rectangle.x < x2) and (y1 < Y < y2):
                    minor_rooms.append(rectangle)


        elif dx == 0:
            X = rect1.x

            if rect1.y > rect2.y:
                aux = rect1
                rect1 = rect2
                rect2 = aux

            y1 = rect1.y + rect1.height // 2
            y2 = rect2.y - rect2.height // 2

            for rectangle in rectangles:
                x1 = rectangle.x - rectangle.width // 2
                x2 = rectangle.x + rectangle.width // 2
                if (y1 < rectangle.y < y2) and (x1 < X < x2):
                    minor_rooms.append(rectangle)


        else:

            if rect1.y > rect2.y:
                aux = rect1
                rect1 = rect2
                rect2 = aux

            X = rect1.x
            Y = rect2.y

            for rectangle in rectangles:
                x1 = rectangle.x - rectangle.width // 2
                x2 = rectangle.x + rectangle.width // 2
                y1 = rectangle.y - rectangle.height // 2
                y2 = rectangle.y + rectangle.height // 2

                if (x1 < X < x2) and (y1 < Y < y2):
                    minor_rooms.append(rectangle)

    return minor_rooms


def fazer_corredores(matrix, mst, main_rooms):
    ## aqui as corrdenadas estao em coordenadas da matrix
    TAM = 5

    corredor_direcao = set({})

    for edge in mst:
        rect1 = main_rooms[edge[0]]
        rect2 = main_rooms[edge[1]]

        ##print('retangulos')
        ##print(rect1)
        ##print(rect2)

        if rect1.y < rect2.y:
            aux = rect1
            rect1 = rect2
            rect2 = aux

        if rect1.x >= rect2.x:

            x1 = rect1.x - rect1.width // 2
            x2 = rect1.x + rect1.width // 2

            y1 = rect2.y - rect2.height // 2
            y2 = rect2.y + rect2.height // 2

            if x1 <= rect2.x <= x2:

                n = int(rect2.x - x1)
                x_0 = rect2.x - 2

                if n < 2:
                    x_0 = int(x1)

                y_0 = int(rect1.y - rect1.height // 2)

                y_ = int(y_0)
                x_ = int(x_0)

                ## botei esse menos 1 aqui 
                while y_ >= rect2.y + rect2.height // 2 - 1:

                    for i in range(5):
                        value = matrix[y_][x_ + i]

                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            if value != 8:
                                matrix[y_][x_ + i] = 5
                        else:
                            matrix[y_][x_ + i] = 8

                    y_ -= 1

            elif y1 < rect1.y < y2:

                ##print('estou aqui 1')

                n = y2 - rect1.y

                y_0 = rect1.y + 2

                if n < 2:
                    y_0 = y2

                x_0 = rect1.x - rect1.width // 2

                x_ = int(x_0)
                y_ = int(y_0) - 1

                ## consertrando erro do caso < --- nesse diminui 1 
                while x_ >= rect2.x + rect2.width // 2 - 1:

                    for i in range(5):
                        value = matrix[y_ - i][x_]

                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            if value != 8:
                                matrix[y_ - i][x_] = 5
                        else:
                            matrix[y_ - i][x_] = 8

                    x_ -= 1



            else:

                x_0 = rect1.x - rect1.width // 2

                y_0 = rect1.y

                n = y_0 - (rect2.y + rect2.height // 2)
                n -= 1

                if n < 2:
                    y_0 += (2 - n)

                ## concertando erro pcasusa do que descobri que merda vai se fuder
                x_ = int(x_0)
                y_ = int(y_0) + 1

                while x_ > rect2.x:

                    for i in range(5):

                        value = matrix[y_ - i][x_]
                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            if value != 8:
                                matrix[y_ - i][x_] = 5
                        else:
                            matrix[y_ - i][x_] = 8

                    x_ -= 1

                    ## não conta a parede
                n = x_0 - rect2.x - 1

                x_ = rect2.x + 2

                if n < 2:
                    x_ -= (2 - n)

                y_ = int(y_0) + 1
                x_ = int(x_)

                while y_ >= rect2.y + rect2.height // 2 - 1:

                    for i in range(5):

                        value = matrix[y_][x_ - i]
                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            # so coloca parede fora do corredor 

                            if value != 8:
                                matrix[y_][x_ - i] = 5
                        else:
                            matrix[y_][x_ - i] = 8

                    y_ -= 1

                y_ = int(y_0) + 1
                x_ = int(rect2.x) - 1
                for i in range(5):
                    value = matrix[y_][x_ + i]
                    if matrix[y_ + 1][x_ + i] != 8:
                        if value == 2:
                            continue
                        matrix[y_][x_ + i] = 5


        elif rect1.x < rect2.x:

            x1 = rect1.x - rect1.width // 2
            x2 = rect1.x + rect1.width // 2

            y1 = rect2.y - rect2.height // 2
            y2 = rect2.y + rect2.height // 2

            if x1 <= rect2.x <= x2:

                n = int(x2 - rect2.x)

                x_0 = rect2.x + 2
                if n < 2:
                    x_0 = x2

                y_0 = rect1.y - rect1.height // 2

                ## menos 1 de correção, também nao entendi direito do porque , mas funcionou 
                x_ = int(x_0) - 1
                y_ = int(y_0)

                ## correção de erro aqui
                while y_ >= rect2.y + rect2.height // 2 - 1:

                    for i in range(5):
                        value = matrix[y_][x_ - i]

                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            if value != 8:
                                matrix[y_][x_ - i] = 5
                        else:
                            matrix[y_][x_ - i] = 8
                    y_ -= 1

            elif y1 < rect1.y < y2:

                ##print('estou aqui 2')

                n = y2 - rect1.y

                y_0 = rect1.y + 2

                if n < 2:
                    y_0 = y2

                x_0 = rect1.x + rect1.width // 2

                x_ = int(x_0) - 1
                ## concertando aqui
                y_ = int(y_0) - 1

                while x_ <= rect2.x - rect2.width // 2:

                    for i in range(5):

                        value = matrix[y_ - i][x_]
                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            if value != 8:
                                matrix[y_ - i][x_] = 5
                        else:
                            matrix[y_ - i][x_] = 8

                    x_ += 1


            else:

                x_0 = rect1.x + rect1.width // 2

                y_0 = rect1.y

                n = y_0 - (rect2.y + rect2.height // 2)
                n -= 1

                if n < 2:
                    y_0 += (2 - n)

                ## concertando erro pcasusa do que descobri que merda vai se fuder
                x_ = int(x_0) - 1
                y_ = int(y_0) + 1

                while x_ < rect2.x:

                    for i in range(5):

                        value = matrix[y_ - i][x_]
                        if value == 2:
                            continue
                        if i == 0 or i == 4:
                            if value != 8:
                                matrix[y_ - i][x_] = 5
                        else:
                            matrix[y_ - i][x_] = 8

                    x_ += 1

                    ## não conta a parede
                n = rect2.x - x_0 - 1

                x_ = rect2.x - 2

                if n < 2:
                    x_ += (2 - n)

                y_ = int(y_0) + 1
                x_ = int(x_)

                while y_ >= rect2.y + rect2.height // 2 - 1:

                    for i in range(5):

                        value = matrix[y_][x_ + i]

                        if value == 2:
                            continue
                        if i == 0 or i == 4:

                            # so coloca parede fora do corredor 
                            if matrix[y_][x_ + i] != 8:
                                matrix[y_][x_ + i] = 5
                        else:
                            matrix[y_][x_ + i] = 8

                    y_ -= 1

                y_ = int(y_0) + 1
                x_ = int(rect2.x) + 1

                for i in range(5):
                    value = matrix[y_][x_ - i]
                    if matrix[y_ + 1][x_ - i] != 8:
                        if value == 2:
                            continue
                        matrix[y_][x_ - i] = 5

    return matrix


def generate_map():
    
    rectangles: List[Rectangle] = create_rectangles_and_distribute(N_RECTANGLES, DEFAULT_SIZE)

    separation_steering(rectangles=rectangles)

    for rect in rectangles:
        rect.set_distance_from_center()

    rectangles.sort(key=lambda rect: rect.area, reverse=True)

    percent = math.ceil(N_RECTANGLES * (1 / 2))
    biggest_rectangles = []

    for i in range(percent):
        biggest_rectangles.append(rectangles[i])

    ##biggest_rectangles.sort(key = lambda rect: rect.distance_from_center)

    main_rooms = []

    for i in range(randint(3, 5)):
        main_rooms.append(biggest_rectangles[i])

    points = []
    for rect in main_rooms:
        points.append((rect.x, rect.y))

    # points = [(0, 0), (0, 1), (1, 0), (1, 1)]
    triangles = Delaunay(points).simplices

    # print(points)
    # print(triangles)

    ## o set verifica se as arestas ja existem 
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

    mst = kruskal_algorithm(points, edges)

    # r1 = Rectangle(0, 0 , 10, 10)
    # r2 = Rectangle(-40, -23 , 10 ,10)
    # main_rooms = [r1, r2]
    # mst = [(0, 1)]

    ##separation_steering(main_rooms)

    ##minor_rooms = all_rooms(mst, main_rooms, rectangles)

    ##for m in minor_rooms:
    ##main_rooms.append(m)

    ## fazer corredores

    ## considerar que um dos pontos é a orige

    rectangles = main_rooms

    menor_x = rectangles[0].x - rectangles[0].width / 2
    maior_y = rectangles[0].y + rectangles[0].height / 2

    for rect in rectangles:
        menor = rect.x - rect.width / 2
        maior = rect.y + rect.height / 2

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

        l = rect.y + rect.height / 2
        c = rect.x + rect.width / 2

        if l > L:
            L = l
        if c > C:
            C = c

    L = int(L + (OFFSET + 1))
    C = int(C + (OFFSET + 1))

    ##print(L, C)

    matrix = []

    for i in range(L):
        linha = []
        for j in range(C):
            linha.append(0)
        matrix.append(linha)

    wall_id = 7
    inter_id = 2
    for rect in rectangles:
        # print(rect)
        top_left_x = int(rect.x - rect.width / 2)
        top_left_y = int(rect.y - rect.height / 2)
        for i in range(rect.height):
            for j in range(rect.width):

                if i == 0 or j == 0 or i == rect.height - 1 or j == rect.width - 1:
                    matrix[top_left_y + i][top_left_x + j] = wall_id
                else:
                    matrix[top_left_y + i][top_left_x + j] = inter_id

    matrix = fazer_corredores(matrix, mst, main_rooms)

    N = len(matrix)
    M = len(matrix[0])

    arquivo = open('map.csv', 'w', encoding='utf-8')

    for i in range(N):
        for j in range(M):
            if j != M - 1:
                print(matrix[i][j], end=',', file=arquivo)
            else:
                print(matrix[i][j], end='', file=arquivo)
        print('', file=arquivo)

    arquivo.close()

    return (matrix, rectangles)


generate_map()
