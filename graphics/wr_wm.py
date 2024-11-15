import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Параметры
center = (0, 0)  # Координаты центра точки
radius = (1, 2)  # Радиус полива

# Создание графика
fig, ax = plt.subplots()

# Загрузка фонового изображения (нежно-зеленый цвет)
background_color = np.array([0.7, 1, 0.7])  # Светло-зеленый цвет
ax.set_facecolor(background_color)

# Добавление прямоугольника вокруг точки
rect = patches.Rectangle((center[0] - radius[0], center[1] - radius[1]), 
                         2 * radius[0], 2 * radius[1], 
                         linewidth=1, edgecolor='blue', facecolor='none', label='Радиус полива')
ax.add_patch(rect)

# Добавление точки с надписью
ax.plot(center[0], center[1], 'ro')  # Рисуем точку
ax.text(center[0], center[1], 'Машина', fontsize=12, ha='left', va='bottom', color='red')

# Настройки графика
ax.set_xlim(-radius[0] - 1, radius[0] + 1)
ax.set_ylim(-radius[1] - 1, radius[1] + 1)
ax.set_aspect('equal', adjustable='box')
ax.axhline(0, color='grey', lw=0.5, ls='--')
ax.axvline(0, color='grey', lw=0.5, ls='--')
ax.set_title('Радиус полива')
ax.legend()

# Показ графика
plt.grid()
plt.show()
