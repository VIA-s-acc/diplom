from math import e
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

a = 2 # коэффициент F(X) зависимотси от влажности
b = 0.3 # пороговая влажность
c = 3 # коэфициент F(X) базовая урожайность
Wp = 0 # давление 
Ms = 10 # максимальная скорость 
Mr = 0.1 # максимальное изменение скорости
Wm = 10 # максимальный объем воды
alpha = 0.1 # Коэффициент влияния скорости
beta = 0 # Коэффициент распределения воды 
lmbda = 0.5 # Коэффициент учета времени
eta = 1e-4 #  Коэффициент учета расхода воды 
gamma = 0.5 # Коэффициент затухания времени 
delta = 0.1 # Коэффициент затухания площади полива
Deltat = 0.1
l_r = 1e-3
eps = 1e-5
max_iter = 1000

def choose_cols(length_m, eps):
    return int(length_m / eps)

length_m = 100
width_m = 10
rows = 11
cols = 100
rx = 0.1 # радиус полива по оси x в метрах
ry = 50 # радиус полива по оси y в метрах

cell_length_m = length_m / cols  
cell_width_m = width_m / rows  
rx_cells = int(rx / cell_length_m)
ry_cells = int(ry / cell_width_m)
# spc = v / cell_length_m

import random
import pprint
    
Field = np.random.uniform(0, 0.1513, (rows, cols))
Line = rows // 2
Field[Line] = [-1 for _ in range(cols)]





def avg_field(Field):
    valid_cells = Field[Field != -1]  # Убираем все ячейки со значением -1
    return np.mean(valid_cells)



def dGkdw(Field, x_cur, w, v, t_k):
    start_col = max(0, x_cur) #+1
    end_col = min(cols, x_cur + rx_cells + 1) 
    Base = 0
    Time = 0
    Water = 4*eta*Wm*Deltat*e**(-delta*v) *rx*ry
    
    exp_alpha_v = e**(-alpha*v)
    if start_col == end_col: 
        start_col -= rx_cells  

    for r in range(max(0, Line - ry_cells), min(rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                term = Wm*Deltat/(d_rc**2+1)**beta * exp_alpha_v
                Base += -2*a*(Field[r, c] + w*term - b) * term
    
    return Base - Water

def dGkdv(Field, x_cur, w, v, t_k):
    start_col = max(0, x_cur - rx_cells) #+1
    end_col = min(cols, x_cur + 1) 
    if start_col == end_col: 
        start_col -= rx_cells  
    Base = 0
    Time = -gamma * lmbda * t_k * e**(-gamma*v) 
    
    Water = -delta * 4 * eta * rx * ry * w * Wm * Deltat * e**(-delta*v)
    
    exp_alpha_v = e**(-alpha*v)
    for r in range(max(0, Line - ry_cells), min(rows, Line + ry_cells + 1)):
        for c in range(start_col, end_col):
            if Field[r, c] == -1:
                continue
            else:
                d_rc = ((r - Line) ** 2 + (c - x_cur) ** 2) ** 0.5
                Base += -2*a*(Field[r, c] + w * ((Wm * Deltat)/(d_rc**2+1)**beta) * exp_alpha_v - b) * (-alpha*Deltat*w*Wm*exp_alpha_v/(d_rc**2+1)**beta)
    return Base - Time - Water
    




def Gradient_Max_step(Field, x_cur, w, v, t_k, l_r = 0.01, max_iter = 100, eps = 0.00001):
    start_v = v

    for i in range(max_iter):
        # print(f"Iteration {i}: w = {w}, v = {v}")

        w_new = w + dGkdw(Field, x_cur, w, v, t_k) * l_r 
        v_new = v + dGkdv(Field, x_cur, w, v, t_k) * l_r
        if w_new > 1:
            w_new = 1
        if v_new > Ms:
            v_new = Ms
        if w_new < 0:   
            w_new = 0
        if v_new < 0:
            v_new = 0
            
        if abs(v_new - start_v) > Mr:
            if v_new > start_v:
                v_new = start_v + Mr
            else:
                v_new = start_v - Mr
                
        if abs (w_new - w) < eps and abs(v_new - v) < eps and i != 0: 
            break
        else:
            w = w_new
            v = v_new
            
    return w, v

def update_cell(r, c, x, w, v, alpha, beta, Wm, Deltat, rx, ry, Line):
    if Field[r][c] == -1:
        return 0
    d_rc = ((r - Line) ** 2 + (c - x) ** 2) ** 0.5
    term = w * (Wm * Deltat / (d_rc**2 + 1)**beta) * np.exp(-alpha * v)
    Field[r][c] += term
    return term  # Для дальнейшей проверки или использования результата

def parallel_update_field(Field, x, w, v, Line, rx_cells, ry_cells, alpha, beta, Wm, Deltat):
    start_col = max(0, x - rx_cells)
    end_col = min(cols, x + 1)
    if start_col == end_col:
        start_col -= rx_cells
    max_workers = multiprocessing.cpu_count()
    # Создание пула потоков
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        for r in range(max(0, Line - ry_cells), min(rows, Line + ry_cells + 1)):
            for c in range(start_col, end_col):
                # Добавление задачи в пул
                futures.append(executor.submit(update_cell, r, c, x, w, v, alpha, beta, Wm, Deltat, rx, ry, Line))
        
        # Ожидание завершения всех задач
        results = [future.result() for future in futures]

    # Параллельное обновление завершено
    return results  # В случае необходимости можем вернуть результаты (например, обновления для анализа)


def Gradien_max_Field(Field, x, w, v, t_k, l_r = 0.1, max_iter = 1000, eps = 0.0001):
    steps = {}
    x_met = 0
    counter = 0
    while x <= cols+rx_cells:
        w, v = Gradient_Max_step(Field, x, w, v, t_k, l_r = 0.01, max_iter = 100, eps = 0.0001)
        start_col = max(0, x - rx_cells) #+1
        end_col = min(cols, x + 1)
        if start_col == end_col:
            start_col -= rx_cells
        parallel_update_field(Field, x, w, v, Line, rx_cells, ry_cells, alpha, beta, Wm, Deltat)
        steps[t_k] = {
            "w": round(w, 5),
            "v": round(v, 5),
            "x (cell)": x,
            "x (m)": round(x_met,5)  
        }
        # print(f"t_k = {t_k:.2f}, w = {w:.4f}, v = {v:.4f}, x = {x}")
        change = v * Deltat
        if change <= 0.001:
            counter += 1
            if counter == 3:
                # print("Error | x_met + change <= x_met | break")
                v+=Mr
        else:
            counter = 0
        x_met += change
        
        x = int(round(x_met / cell_length_m))
        t_k += Deltat
    return steps



print(avg_field(Field))
steps = Gradien_max_Field(Field, 0, 0, 0, 0, l_r, max_iter, eps)
# pprint.pprint(steps)
print(avg_field(Field))

# for i in range(5):
#     Field  = np.random.uniform(0, 0, (rows, cols))

#     avg = avg_field(Field)
    
#     steps = Gradien_max_Field(Field, 0, 0, 0, 0, l_r, max_iter, eps)
#     # pprint.pprint(steps)
    
#     print(f"eta: {eta} | avg: {avg} -> {avg_field(Field)}")
#     eta *= 10