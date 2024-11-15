import numpy as np
import matplotlib.pyplot as plt

# Определяем функцию F(x)
def F(x, a, b, c):
    return -a * (x - b)**2 + c

# Параметры
b = 50  # оптимальная влажность
c = 100  # базовая урожайность

# Значения a для разных кривых
a_values = [0.1, 0.5, 1.0]
x = np.linspace(0, 100, 400)

# Создаем график
plt.figure(figsize=(10, 6))
for a in a_values:
    plt.plot(x, F(x, a, b, c), label=f'a = {a}')

# Добавляем элементы графика
plt.title('График функции F(x) при разных значениях a')
plt.xlabel('Влажность')
plt.ylabel('Урожайность')
plt.axvline(x=b, color='grey', linestyle='--', label='Оптимальная влажность (b)')
plt.legend()
plt.grid()
plt.ylim(0, 120)
plt.xlim(0, 100)

# Показываем график
plt.show()
