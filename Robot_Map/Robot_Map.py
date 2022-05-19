"""
Программа, симулирующая исследование закрытого помещения и отрисовывание карты этого помещения мобильным роботом.
"""

# Пакеты
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
from time import sleep


class Map:
    # Цвета на карте
    unexplored_color = [80, 80, 80]
    explored_color = [0, 255, 0]
    walls_color = [0, 0, 0]
    location_color = [0, 0, 255]
    target_color = [100, 0, 0]
    way_color = [148, 0, 211]
    min_way_color = [255, 0, 0]

    # На сколько клеток видит датчик
    vision = 2

    # Задержка между этапами, для отслеживания работы программы
    sleep_time = 0.3

    def __init__(self, n=25, m=25, location=(3, 3)):
        # Количество строк на карте
        self.n = n
        # Количество столбцов на карте
        self.m = m
        # Местоположение робота на карте
        self.location = location
        # Ориентация робота относительно карты
        self.rotation = 270
        # Неисследованные клетки
        self.unexplored = [(i, j) for i in range(n) for j in range(m)]
        self.unexplored.remove(location)
        # Исследованные клетки
        self.explored = [location]
        # Стены
        self.walls = []
        # Матрица изображения
        self.matrix_color = [[[0, 0, 0] for _ in range(m)] for _ in range(n)]

    # Обновление матрицы изображения
    def update_matrix_color(self, target=list(), way=[], min_way=(-1, -1)):
        for i in range(self.n):
            for j in range(self.m):
                if (i, j) in self.unexplored:
                    self.matrix_color[i][j] = Map.unexplored_color
                if (i, j) in self.explored:
                    self.matrix_color[i][j] = Map.explored_color
                if (i, j) == self.location:
                    self.matrix_color[i][j] = Map.location_color
                if (i, j) in self.walls:
                    self.matrix_color[i][j] = Map.walls_color
                if (i, j) in target:
                    self.matrix_color[i][j] = Map.target_color
                if (i, j) in way:
                    self.matrix_color[i][j] = Map.way_color
                if (i, j) == min_way:
                    self.matrix_color[i][j] = Map.min_way_color


# Волновой алгоритм поиска кратчайшего пути основанный на алгоритме Ли
def lee(points, map_robot, target, matrix_way):
    # Новые точки, для которых нужно найти расстояние
    new_points = []
    # Для каждой точки нужно расмотреть соседние точки, если это не стены и для них не был найден путь,
    # находится путь и записывается в матрицу путей, где на месте каждой точки пишется путь до неё, или -2,
    # если для неё путь находить не понадобилось. Если соседняя точка не является потенциальной,
    # то она будет учавтсвовать в следующей волне. Если алгоритм иследовал все возможные для него точки,
    # то алгоритм завершается
    ## Так же добавлен запрет на движение назад, для этого помимо расстояний в матрице путей
    ## записываются ориентации робта в точках, если он в них приедет.
    for point in points:
        if ((point[0], point[1] + 1) not in map_robot.walls and matrix_way[point[0]][point[1] + 1][0] == -2
                and matrix_way[point[0]][point[1]][1] != 180):
            if (point[0], point[1] + 1) not in target:
                new_points.append((point[0], point[1] + 1))
            matrix_way[point[0]][point[1] + 1] = (matrix_way[point[0]][point[1]][0] + 1, 0)
        if ((point[0] - 1, point[1]) not in map_robot.walls and matrix_way[point[0] - 1][point[1]][0] == -2
                and matrix_way[point[0]][point[1]][1] != 270):
            if (point[0] - 1, point[1]) not in target:
                new_points.append((point[0] - 1, point[1]))
            matrix_way[point[0] - 1][point[1]] = (matrix_way[point[0]][point[1]][0] + 1, 90)
        if ((point[0], point[1] - 1) not in map_robot.walls and matrix_way[point[0]][point[1] - 1][0] == -2
                and matrix_way[point[0]][point[1]][1] != 0):
            if (point[0], point[1] - 1) not in target:
                new_points.append((point[0], point[1] - 1))
            matrix_way[point[0]][point[1] - 1] = (matrix_way[point[0]][point[1]][0] + 1, 180)
        if ((point[0] + 1, point[1]) not in map_robot.walls and matrix_way[point[0] + 1][point[1]][0] == -2
                and matrix_way[point[0]][point[1]][1] != 90):
            if (point[0] + 1, point[1]) not in target:
                new_points.append((point[0] + 1, point[1]))
            matrix_way[point[0] + 1][point[1]] = (matrix_way[point[0]][point[1]][0] + 1, 270)
    if new_points:
        return lee(list(set(new_points)), map_robot, target, matrix_way)
    else:
        matrix_way = [[i[0] for i in j] for j in matrix_way]
        return matrix_way


# Алгоритм востановления обратного пути от точки до которой короче всего до робота
def way_back(way_inverse, matrix_way):
    # Начиная с точки до которой короче всего, если у соседней точки растояние до неё меньше на 1,
    # то она становится следующей точкой маршрута от точки до которой короче всего до робота.
    # Алгоритм повторяется, пока не достигнет робота
    if matrix_way[way_inverse[-1][0] + 1][way_inverse[-1][1]] == matrix_way[way_inverse[-1][0]][way_inverse[-1][1]] - 1:
        way_inverse.append((way_inverse[-1][0] + 1, way_inverse[-1][1]))
    elif matrix_way[way_inverse[-1][0] - 1][way_inverse[-1][1]] == matrix_way[way_inverse[-1][0]][
        way_inverse[-1][1]] - 1:
        way_inverse.append((way_inverse[-1][0] - 1, way_inverse[-1][1]))
    elif matrix_way[way_inverse[-1][0]][way_inverse[-1][1] + 1] == matrix_way[way_inverse[-1][0]][
        way_inverse[-1][1]] - 1:
        way_inverse.append((way_inverse[-1][0], way_inverse[-1][1] + 1))
    else:
        way_inverse.append((way_inverse[-1][0], way_inverse[-1][1] - 1))
    if matrix_way[way_inverse[-1][0]][way_inverse[-1][1]] == 0:
        return way_inverse[1:-1]
    return way_back(way_inverse, matrix_way)


# Начало программы
if __name__ == "__main__":
    # Карта которую будет отрисовывать робот:
    map_robot = Map()
    ## Создаём изображение карты робота
    map_robot.update_matrix_color()
    window_map_robot = tk.Tk()
    window_map_robot.title("Robot Map")
    window_map_robot.geometry('400x400-200+200')
    image_map_robot = ImageTk.PhotoImage(Image.fromarray(np.array(map_robot.matrix_color)
                                                         .astype('uint8')).resize((400, 400), resample=Image.BOX))
    canvas_map_robot = tk.Canvas(window_map_robot, width=400, height=400)
    canvas_map_robot.create_image(200, 200, image=image_map_robot, tags="image_map_robot")
    canvas_map_robot.pack()
    # Зададим свою карту 25x25
    map_real = Map(25, 25)
    map_real.location = (-1, -1)
    map_real.explored = []
    map_real.unexplored = []
    ## Стены на крате
    ### Произвольные
    map_real.walls = [(6, 6), (6, 7), (6, 8), (8, 10), (8, 11), (8, 12), (3, 15), (4, 15), (5, 15), (6, 15),
                      (11, 5), (11, 6), (11, 7), (17, 11), (16, 11), (15, 11), (18, 19), (18, 20), (18, 21), (18, 22),
                      (14, 18), (15, 18), (16, 18), (17, 18), (18, 18), (20, 4), (20, 5), (20, 6), (20, 7)]
    ### Вокруг карты
    for i in range(2, map_real.n - 2):
        map_real.walls.extend([(i, 2), (i, map_real.m - 3)])
    for j in range(2, map_real.m - 2):
        map_real.walls.extend([(2, j), (map_real.n - 3, j)])
    for i in range(2, map_real.n - 2):
        for j in range(2, map_real.m - 2):
            if (i, j) not in map_real.walls:
                map_real.explored.append((i, j))
    ## Всё что за стенами отметим неиследованной зоной
    map_real.unexplored.extend([(i, j) for j in range(map_real.m) for i in [0, 1, map_real.n - 2, map_real.n - 1]])
    map_real.unexplored.extend(
        [(i, j) for j in [0, 1, map_real.m - 2, map_real.m - 1] for i in range(2, map_real.m - 2)])
    ## Создаём изображение реальной карты
    map_real.update_matrix_color()
    window_map_real = tk.Toplevel(window_map_robot)
    window_map_real.title("Real Map")
    window_map_real.geometry('400x400+200+200')
    image_map_real = ImageTk.PhotoImage(Image.fromarray(np.array(map_real.matrix_color)
                                                        .astype('uint8')).resize((400, 400), resample=Image.BOX))
    canvas_map_real = tk.Canvas(window_map_real, width=400, height=400)
    canvas_map_real.create_image(200, 200, image=image_map_real, tags="image_map_real")
    canvas_map_real.pack()
    window_map_robot.update()
    # Номер шага
    step = 0
    # Основной цикл
    while True:
        step += 1
        ## Сбор данных
        ### Данные которые снял датчик растояния при его угле поворота относительно карты
        distance_0 = None
        distance_45 = None
        distance_90 = None
        distance_135 = None
        distance_180 = None
        distance_225 = None
        distance_270 = None
        distance_315 = None
        ### Симулируем сбор данных, 2 клетки перед, слева и справа робота, 1 клетка по диоганали слева и справа
        if map_robot.rotation != 180:
            if (map_robot.location[0], map_robot.location[1] + 1) in map_real.walls:
                distance_0 = 0
            elif (map_robot.location[0], map_robot.location[1] + 2) in map_real.walls:
                distance_0 = 1
            else:
                distance_0 = 2
        if map_robot.rotation != 270:
            if (map_robot.location[0] - 1, map_robot.location[1]) in map_real.walls:
                distance_90 = 0
            elif (map_robot.location[0] - 2, map_robot.location[1]) in map_real.walls:
                distance_90 = 1
            else:
                distance_90 = 2
        if map_robot.rotation != 0:
            if (map_robot.location[0], map_robot.location[1] - 1) in map_real.walls:
                distance_180 = 0
            elif (map_robot.location[0], map_robot.location[1] - 2) in map_real.walls:
                distance_180 = 1
            else:
                distance_180 = 2
        if map_robot.rotation != 90:
            if (map_robot.location[0] + 1, map_robot.location[1]) in map_real.walls:
                distance_270 = 0
            elif (map_robot.location[0] + 2, map_robot.location[1]) in map_real.walls:
                distance_270 = 1
            else:
                distance_270 = 2
        if map_robot.rotation == 0 or map_robot.rotation == 90:
            if (map_robot.location[0] - 1, map_robot.location[1] + 1) in map_real.walls:
                distance_45 = 0
            else:
                distance_45 = 1
        if map_robot.rotation == 90 or map_robot.rotation == 180:
            if (map_robot.location[0] - 1, map_robot.location[1] - 1) in map_real.walls:
                distance_135 = 0
            else:
                distance_135 = 1
        if map_robot.rotation == 180 or map_robot.rotation == 270:
            if (map_robot.location[0] + 1, map_robot.location[1] - 1) in map_real.walls:
                distance_225 = 0
            else:
                distance_225 = 1
        if map_robot.rotation == 270 or map_robot.rotation == 0:
            if (map_robot.location[0] + 1, map_robot.location[1] + 1) in map_real.walls:
                distance_315 = 0
            else:
                distance_315 = 1
        ## Построение карты
        ### Если растояние меньше ожидаемово в одном из направлений, значит перед нами есть стена на этом растоянии
        if distance_0 is not None:
            if distance_0 == 0:
                map_robot.walls.append((map_robot.location[0], map_robot.location[1] + 1))
            elif distance_0 == 1:
                map_robot.explored.append((map_robot.location[0], map_robot.location[1] + 1))
                map_robot.walls.append((map_robot.location[0], map_robot.location[1] + 2))
                if (map_robot.location[0], map_robot.location[1] + 2) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0], map_robot.location[1] + 2))
            else:
                map_robot.explored.append((map_robot.location[0], map_robot.location[1] + 1))
                map_robot.explored.append((map_robot.location[0], map_robot.location[1] + 2))
                if (map_robot.location[0], map_robot.location[1] + 2) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0], map_robot.location[1] + 2))
            if (map_robot.location[0], map_robot.location[1] + 1) in map_robot.unexplored:
                map_robot.unexplored.remove((map_robot.location[0], map_robot.location[1] + 1))
        if distance_90 is not None:
            if distance_90 == 0:
                map_robot.walls.append((map_robot.location[0] - 1, map_robot.location[1]))
            elif distance_90 == 1:
                map_robot.explored.append((map_robot.location[0] - 1, map_robot.location[1]))
                map_robot.walls.append((map_robot.location[0] - 2, map_robot.location[1]))
                if (map_robot.location[0] - 2, map_robot.location[1]) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] - 2, map_robot.location[1]))
            else:
                map_robot.explored.append((map_robot.location[0] - 1, map_robot.location[1]))
                map_robot.explored.append((map_robot.location[0] - 2, map_robot.location[1]))
                if (map_robot.location[0] - 2, map_robot.location[1]) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] - 2, map_robot.location[1]))
            if (map_robot.location[0] - 1, map_robot.location[1]) in map_robot.unexplored:
                map_robot.unexplored.remove((map_robot.location[0] - 1, map_robot.location[1]))
        if distance_180 is not None:
            if distance_180 == 0:
                map_robot.walls.append((map_robot.location[0], map_robot.location[1] - 1))
            elif distance_180 == 1:
                map_robot.explored.append((map_robot.location[0], map_robot.location[1] - 1))
                map_robot.walls.append((map_robot.location[0], map_robot.location[1] - 2))
                if (map_robot.location[0], map_robot.location[1] - 2) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0], map_robot.location[1] - 2))
            else:
                map_robot.explored.append((map_robot.location[0], map_robot.location[1] - 1))
                map_robot.explored.append((map_robot.location[0], map_robot.location[1] - 2))
                if (map_robot.location[0], map_robot.location[1] - 2) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0], map_robot.location[1] - 2))
            if (map_robot.location[0], map_robot.location[1] - 1) in map_robot.unexplored:
                map_robot.unexplored.remove((map_robot.location[0], map_robot.location[1] - 1))
        if distance_270 is not None:
            if distance_270 == 0:
                map_robot.walls.append((map_robot.location[0] + 1, map_robot.location[1]))
            elif distance_270 == 1:
                map_robot.explored.append((map_robot.location[0] + 1, map_robot.location[1]))
                map_robot.walls.append((map_robot.location[0] + 2, map_robot.location[1]))
                if (map_robot.location[0] + 2, map_robot.location[1]) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] + 2, map_robot.location[1]))
            else:
                map_robot.explored.append((map_robot.location[0] + 1, map_robot.location[1]))
                map_robot.explored.append((map_robot.location[0] + 2, map_robot.location[1]))
                if (map_robot.location[0] + 2, map_robot.location[1]) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] + 2, map_robot.location[1]))
            if (map_robot.location[0] + 1, map_robot.location[1]) in map_robot.unexplored:
                map_robot.unexplored.remove((map_robot.location[0] + 1, map_robot.location[1]))
        if distance_45 is not None:
            if (map_robot.location[0], map_robot.location[1] + 1) not in map_robot.walls or (
                    map_robot.location[0] - 1, map_robot.location[1]) not in map_robot.walls:
                if distance_45 == 0:
                    map_robot.walls.append((map_robot.location[0] - 1, map_robot.location[1] + 1))
                else:
                    map_robot.explored.append((map_robot.location[0] - 1, map_robot.location[1] + 1))
                if (map_robot.location[0] - 1, map_robot.location[1] + 1) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] - 1, map_robot.location[1] + 1))
        if distance_135 is not None:
            if (map_robot.location[0], map_robot.location[1] - 1) not in map_robot.walls or (
                    map_robot.location[0] - 1, map_robot.location[1]) not in map_robot.walls:
                if distance_135 == 0:
                    map_robot.walls.append((map_robot.location[0] - 1, map_robot.location[1] - 1))
                else:
                    map_robot.explored.append((map_robot.location[0] - 1, map_robot.location[1] - 1))
                if (map_robot.location[0] - 1, map_robot.location[1] - 1) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] - 1, map_robot.location[1] - 1))
        if distance_225 is not None:
            if (map_robot.location[0], map_robot.location[1] - 1) not in map_robot.walls or (
                    map_robot.location[0] + 1, map_robot.location[1]) not in map_robot.walls:
                if distance_225 == 0:
                    map_robot.walls.append((map_robot.location[0] + 1, map_robot.location[1] - 1))
                else:
                    map_robot.explored.append((map_robot.location[0] + 1, map_robot.location[1] - 1))
                if (map_robot.location[0] + 1, map_robot.location[1] - 1) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] + 1, map_robot.location[1] - 1))
        if distance_315 is not None:
            if (map_robot.location[0], map_robot.location[1] + 1) not in map_robot.walls or (
                    map_robot.location[0] + 1, map_robot.location[1]) not in map_robot.walls:
                if distance_315 == 0:
                    map_robot.walls.append((map_robot.location[0] + 1, map_robot.location[1] + 1))
                else:
                    map_robot.explored.append((map_robot.location[0] + 1, map_robot.location[1] + 1))
                if (map_robot.location[0] + 1, map_robot.location[1] + 1) in map_robot.unexplored:
                    map_robot.unexplored.remove((map_robot.location[0] + 1, map_robot.location[1] + 1))
        # *Обновляем изображение карты робота
        map_robot.update_matrix_color()
        image_map_robot = ImageTk.PhotoImage(Image.fromarray(np.array(map_robot.matrix_color)
                                                             .astype('uint8')).resize((400, 400), resample=Image.BOX))
        canvas_map_robot.delete("image_map_robot")
        canvas_map_robot.create_image(200, 200, image=image_map_robot, tags="image_map_robot")
        canvas_map_robot.pack()
        window_map_robot.update()
        # *Пауза
        sleep(Map.sleep_time)
        ## Вычисление шага
        ### Находим потенциальные клетки, это клетки, которые неиследованные и до них можно добраться
        target = []
        for j in range(map_robot.m):
            for i in range(map_robot.n):
                if (i, j) in map_robot.unexplored:
                    if (i + 1, j) in map_robot.explored or \
                            (i - 1, j) in map_robot.explored or \
                            (i, j + 1) in map_robot.explored or \
                            (i, j - 1) in map_robot.explored:
                        target.append((i, j))
        ### Если потенциальных клеток нету, алгоритм считается завершенным, через 5 секунд программа закроется
        if not target:
            i = 0
            while i < 500:
                sleep(0.01)
                window_map_robot.update()
                i += 1
            break
        # *Обновляем изображение карты робота, указываем потенциальные клетки
        map_robot.update_matrix_color(target=target)
        image_map_robot = ImageTk.PhotoImage(Image.fromarray(np.array(map_robot.matrix_color)
                                                             .astype('uint8')).resize((400, 400),
                                                                                      resample=Image.BOX))
        canvas_map_robot.delete("image_map_robot")
        canvas_map_robot.create_image(200, 200, image=image_map_robot, tags="image_map_robot")
        canvas_map_robot.pack()
        window_map_robot.update()
        # *Пауза
        sleep(Map.sleep_time)
        ### Находим длину путей да каждой клетки, пока не узнаем растояние до всех потенциальных клеток
        ### с помощью волнового алгоритма (алгоритма Ли)
        matrix_way = [[(-2, -1) for i in range(map_robot.n)] for j in range(map_robot.m)]
        matrix_way[map_robot.location[0]][map_robot.location[1]] = (0, map_robot.rotation)
        matrix_way = lee([map_robot.location], map_robot, target, matrix_way)
        ### Уберём те клетки, для которых алгоритм не нашёл расстояний (только при старте сзади)
        possible_target = [e for e in target if matrix_way[e[0]][e[1]] != -2]
        ### Находим клетку с кратчайшим расстоянием до неё
        min_way = possible_target[0]
        for e in possible_target:
            if matrix_way[e[0]][e[1]] < matrix_way[min_way[0]][min_way[1]]:
                min_way = e
        # *Обновляем изображение карты робота, указываем потенциальные клетки, клетку до которой короче всего
        map_robot.update_matrix_color(target=target, min_way=min_way)
        image_map_robot = ImageTk.PhotoImage(Image.fromarray(np.array(map_robot.matrix_color)
                                                             .astype('uint8')).resize((400, 400),
                                                                                      resample=Image.BOX))
        canvas_map_robot.delete("image_map_robot")
        canvas_map_robot.create_image(200, 200, image=image_map_robot, tags="image_map_robot")
        canvas_map_robot.pack()
        window_map_robot.update()
        # *Пауза
        sleep(Map.sleep_time)
        ### Находим обратный путь от клетки до которой короче всего до робота
        way_inverse = [min_way]
        way_inverse = way_back(way_inverse, matrix_way)
        # *Обновляем изображение карты робота, указываем потенциальные клетки, клетку до которой короче всего и путь
        map_robot.update_matrix_color(target=target, way=way_inverse, min_way=min_way)
        image_map_robot = ImageTk.PhotoImage(Image.fromarray(np.array(map_robot.matrix_color)
                                                             .astype('uint8')).resize((400, 400),
                                                                                      resample=Image.BOX))
        canvas_map_robot.delete("image_map_robot")
        canvas_map_robot.create_image(200, 200, image=image_map_robot, tags="image_map_robot")
        canvas_map_robot.pack()
        window_map_robot.update()
        # *Пауза
        sleep(Map.sleep_time)
        ## Движение робота
        ### Устанавлваем новую ориентацию робота относительно карты
        if way_inverse[-1][1] > map_robot.location[1]:
            map_robot.rotation = 0
        elif way_inverse[-1][0] < map_robot.location[0]:
            map_robot.rotation = 90
        elif way_inverse[-1][1] < map_robot.location[1]:
            map_robot.rotation = 180
        else:
            map_robot.rotation = 270
        ### Устанавлваем новое положение робота на карте
        map_robot.location = way_inverse[-1]
        # *Обновляем изображение карты робота
        map_robot.update_matrix_color()
        image_map_robot = ImageTk.PhotoImage(Image.fromarray(np.array(map_robot.matrix_color)
                                                             .astype('uint8')).resize((400, 400),
                                                                                      resample=Image.BOX))
        canvas_map_robot.delete("image_map_robot")
        canvas_map_robot.create_image(200, 200, image=image_map_robot, tags="image_map_robot")
        canvas_map_robot.pack()
        window_map_robot.update()
        # *Пауза
        sleep(Map.sleep_time)
    # Выход из программы
    window_map_robot.destroy()
