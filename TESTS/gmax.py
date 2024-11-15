import numpy as np
from math import e

# Константы и параметры
a = -2
b = 0.3
c = 3
Wp = 0
Ms = 10
Mr = 0.1
Wm = 1
rx = 0  # радиус полива по оси x в метрах
ry = 5  # радиус полива по оси y в метрах
alpha = 0.1
beta = 0
lmbda = 0.5
eta = 0.3
gamma = 0.3
delta = 0
rows = 11  # количество строк (ячейки по вертикали)
cols = 10  # количество столбцов (ячейки по горизонтали)
length_m = 10  # длина поля в метрах
width_m = 5  # ширина поля в метрах
cell_length_m = length_m / cols  # длина ячейки по x
cell_width_m = width_m / rows  # ширина ячейки по y
rx_cells = int(rx / cell_length_m)  # радиус полива в ячейках по x
ry_cells = int(ry / cell_width_m)  # радиус полива в ячейках по y
Deltat = 0.1  # шаг по времени

# Создаем случайное поле влажности
import random
Field = [[random.uniform(0, 0.6) for _ in range(cols)] for _ in range(rows)]
Field[5] = [-1 for _ in range(cols)]  # отметим центральную линию
Line = 5

# Функция для вычисления градиента по W
def dGkdw(Field, x_cur, w, v, t_k):
    start_col = max(0, x_cur - rx_cells)
    end_col = min(cols, x_cur + rx_cells + 1)
    Base = 0
    Water = 4 * eta * Wm * Deltat * e ** (-delta * v) * rx * ry
    
    for r in range(max(0, Line - ry_cells), min(rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r][c] == -1:
                continue
            d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
            Base += 2 * a * (Field[r][c] + w * ((Wm * Deltat) / (d_rc**2 + 1)**beta) * e ** (-alpha * v) - b) * \
                    ((Wm * Deltat) / (d_rc**2 + 1)**beta * e ** (-alpha * v))
    
    return Base - Water

# Функция для вычисления градиента по v
def dGkdv(Field, x_cur, w, v, t_k):
    start_col = max(0, x_cur - rx_cells)
    end_col = min(cols, x_cur + rx_cells + 1)
    Base = 0
    Time = -gamma * lmbda * t_k * e ** (-gamma * t_k)
    Water = -delta * 4 * eta * rx * ry * w * Wm * Deltat * e ** (-delta * v)
    
    for r in range(max(0, Line - ry_cells), min(rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r][c] == -1:
                continue
            d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
            Base += 2 * a * (Field[r][c] + w * ((Wm * Deltat) / (d_rc**2 + 1)**beta) * e ** (-alpha * v) - b) * \
                    (-alpha * Deltat * w * Wm * e ** (-alpha * v) / (d_rc**2 + 1)**beta)
    
    return Base - Time - Water

# Нормировка для критерия остановки
def norm(x, y):
    return (x**2 + y**2)**0.5

# Градиентный шаг для максимизации функции прибыли
def Gradient_Max_step(Field, x_cur, w, v, t_k, learning_rate=0.01):
    max_iter = 100
    eps = 0.001
    for i in range(max_iter):
        d_w = dGkdw(Field, x_cur, w, v, t_k)
        d_v = dGkdv(Field, x_cur, w, v, t_k)
        
        # Обновляем значения w и v с учетом градиентов
        w_new = w + d_w * learning_rate
        v_new = v + d_v * learning_rate
        
        # Ограничения
        w_new = min(max(w_new, 0), 1)
        v_new = min(max(v_new, 0), Ms)
        if abs(v_new - v) > Mr:
            v_new = v + Mr * np.sign(v_new - v)
        
        # Проверка критерия остановки
        if norm(w_new - w, v_new - v) < eps and i != 0:
            break
        
        w, v = w_new, v_new  # обновляем для следующей итерации
        
    return w, v

# Функция для итеративного применения градиентного спуска по всему полю
def Gradient_max_Field(Field, x, w, v, t_k):
    steps = {}
    while x < cols:
        w, v = Gradient_Max_step(Field, x, w, v, t_k)
        start_col = max(0, x - rx_cells)
        end_col = min(cols, x + rx_cells + 1)
        
        for r in range(max(0, Line - ry_cells), min(rows, Line + ry_cells + 1)):
            for c in range(start_col, end_col):
                if Field[r][c] == -1:
                    continue
                d_rc = ((r - Line) ** 2 + (c - x) ** 2) ** 0.5
                Field[r][c] += w * (Wm * Deltat / (d_rc**2 + 1)**beta) * e ** (-alpha * v)
        
        steps[t_k] = {"w": w, "v": v, "x": x}
        print(f"t_k = {t_k:.2f}, w = {w:.4f}, v = {v:.4f}, x = {x}")
        
        # Вычисляем новое положение по скорости
        spc = v * Deltat / cell_length_m
        x += spc
        x = int(round(x))
        t_k += Deltat
    
    return steps

# Запуск и вывод результатов
initial_w = 0
initial_v = 0
t_k_start = 0
Gradient_max_Field(Field, 0, initial_w, initial_v, t_k_start)
