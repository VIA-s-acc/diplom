import os
import numpy as np
import rasterio
from rasterio.transform import Affine
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from matplotlib.widgets import RectangleSelector

# Создаем папку для данных
os.makedirs('data', exist_ok=True)

# ================================================
# 1. Генерация синтетических данных (исправлено)
# ================================================
np.random.seed(42)

# Параметры данных
num_channels = 100  # 100 спектральных каналов
height, width = 512, 512  # Размер изображения

def generate_hyperspectral_data():
    # Темновой эталон (базовый шум)
    dark_ref = np.random.normal(0, 0.1, num_channels)
    np.save('data/dark_ref.npy', dark_ref)

    # Белый эталон (почти 1 с небольшими вариациями)
    white_ref = np.random.uniform(0.85, 0.95, num_channels)
    np.save('data/white_ref.npy', white_ref)

    # Основное изображение с искусственными "влажными" зонами
    I_raw = np.random.normal(0.4, 0.2, (num_channels, height, width))
    
    # Модифицируем правильные диапазоны (каналы 70-80 для NIR, 90-100 для SWIR)
    I_raw[90:100, 100:200, 300:400] *= 0.3  # SWIR подавление
    I_raw[70:80, 100:200, 300:400] *= 1.5   # NIR усиление
    
    # Сохраняем как GeoTIFF
    transform = Affine.translation(0, 0) * Affine.scale(1, 1)
    with rasterio.open(
        'data/hyperspectral.tif',
        'w',
        driver='GTiff',
        height=height,
        width=width,
        count=num_channels,
        dtype=I_raw.dtype,
        transform=transform,
    ) as dst:
        dst.write(I_raw)

generate_hyperspectral_data()

# ================================================
# 2. Создание масок (добавлена проверка областей)
# ================================================
def create_masks():
    with rasterio.open('data/hyperspectral.tif') as src:
        rgb = np.stack([src.read(30), src.read(20), src.read(10)], axis=-1)

    rgb = (rgb - rgb.min()) / (rgb.max() - rgb.min())

    def create_mask(title, filename):
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.imshow(rgb)
        ax.set_title(f"{title}\n(Выделите несколько областей. 'Q' - завершить)")
        mask = np.zeros((height, width), dtype=bool)

        def on_select(eclick, erelease):
            x1, y1 = int(eclick.xdata), int(eclick.ydata)
            x2, y2 = int(erelease.xdata), int(erelease.ydata)
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            mask[y1:y2, x1:x2] = True
            ax.add_patch(plt.Rectangle(
                (x1, y1), x2-x1, y2-y1, 
                edgecolor='lime', facecolor='none', lw=2))
            plt.draw()

        rs = RectangleSelector(ax, on_select, useblit=True,
                            button=[1], minspanx=5, minspany=5,
                            spancoords='pixels', interactive=True)
        
        def on_key(event):
            if event.key in ['q', 'Q']:
                plt.close()
        
        fig.canvas.mpl_connect('key_press_event', on_key)
        plt.show()
        
        # Проверка выделенной области
        if np.sum(mask) == 0:
            raise ValueError("Не выделено ни одной области!")
        
        np.save(f'data/{filename}.npy', mask)
        return mask

    try:
        print("Создайте маску сухих зон:")
        create_mask("СУХИЕ зоны", "mask_dry")
        print("Создайте маску влажных зон:")
        create_mask("ВЛАЖНЫЕ зоны", "mask_wet")
    except ValueError as e:
        print(f"Ошибка: {e}")
        exit()

# Раскомментируйте для ручного создания масок:
# create_masks()

# ================================================
# 3. Автогенерация масок (добавлена диагностика)
# ================================================
if not os.path.exists('data/mask_dry.npy'):
    with rasterio.open('data/hyperspectral.tif') as src:
        data = src.read()
    
    # Используем средние каналы из модифицированных диапазонов
    nir = data[75]  # NIR: 70-80 (средний 75)
    swir = data[95] # SWIR: 90-100 (средний 95)
    ndwi = (nir - swir) / (nir + swir + 1e-9)
    
    # Автоматические маски с визуализацией
    plt.figure(figsize=(12, 4))
    plt.subplot(131)
    plt.imshow(ndwi, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('NDWI индекс')
    
    mask_wet = (ndwi > 0.3)
    mask_dry = (ndwi < -0.2)
    print(len(mask_dry[mask_dry == True]))
    
    plt.subplot(132)
    plt.imshow(mask_dry, cmap='gray')
    plt.title(f'Сухие зоны: {np.sum(mask_dry)} пикс.')
    
    plt.subplot(133)
    plt.imshow(mask_wet, cmap='gray')
    plt.title(f'Влажные зоны: {np.sum(mask_wet)} пикс.')
    plt.tight_layout()
    plt.show()
    
    np.save('data/mask_dry.npy', mask_dry)
    np.save('data/mask_wet.npy', mask_wet)

# ================================================
# 4. Обработка данных (исправленная версия)
# ================================================
def process_and_visualize():
    # Загрузка данных
    with rasterio.open('data/hyperspectral.tif') as src:
        I_raw = src.read()
    
    dark_ref = np.load('data/dark_ref.npy')
    white_ref = np.load('data/white_ref.npy')

    # Калибровка
    I = (I_raw - dark_ref[:, None, None]) / (
        white_ref[:, None, None] - dark_ref[:, None, None] + 1e-9)
    I = np.clip(I, 0, 1)

    # Расчет NDWI с правильными каналами
    nir_channel, swir_channel = 75, 95  # Средние каналы диапазонов
    ndwi = (I[nir_channel] - I[swir_channel]) / (
        I[nir_channel] + I[swir_channel] + 1e-9)

    # Загрузка масок
    mask_dry = np.load('data/mask_dry.npy')
    mask_wet = np.load('data/mask_wet.npy')

    # Проверка масок
    if np.sum(mask_dry) == 0 or np.sum(mask_wet) == 0:
        raise ValueError("Одна из масок не содержит данных!")

    # Подготовка данных для модели
    X = np.concatenate([
        ndwi[mask_dry].flatten(),
        ndwi[mask_wet].flatten()
    ])
    y = np.concatenate([
        np.zeros(np.sum(mask_dry)),  # Сухие = 0
        np.ones(np.sum(mask_wet))    # Влажные = 1
    ])

    # Нормализация данных
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X.reshape(-1, 1))

    # Обучение модели
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Прогнозирование и нормализация
    moisture = model.predict(scaler.transform(ndwi.reshape(-1, 1)))
    moisture = moisture.reshape(ndwi.shape)
    
    # Масштабирование к [0, 1]
    moisture = (moisture - moisture.min()) / (moisture.max() - moisture.min())

    # Визуализация
        # Визуализация
    plt.figure(figsize=(18, 12))
    
    # Основные графики
    plt.subplot(241)
    plt.imshow(I[[30, 20, 10]].transpose(1, 2, 0))
    plt.title('RGB-композит')
    
    plt.subplot(242)
    plt.imshow(ndwi, cmap='coolwarm', vmin=-1, vmax=1)
    plt.colorbar()
    plt.title('NDWI индекс')
    
    plt.subplot(243)
    plt.imshow(moisture, cmap='Blues', vmin=0, vmax=1)
    plt.colorbar()
    plt.title('Нормализованная влажность')
    
    # Гистограммы
    plt.subplot(244)
    plt.hist(ndwi.flatten(), bins=50, alpha=0.7, color='gray')
    plt.title('Распределение NDWI')
    plt.xlabel('Значение NDWI')
    plt.ylabel('Частота')
    
    # Новый график: сравнение распределений влажности
    plt.subplot(245)
    moisture_dry = moisture[mask_dry]
    moisture_wet = moisture[mask_wet]
    
    plt.hist(moisture_dry, bins=30, alpha=0.5, color='red', 
             label='Сухие зоны', density=True)
    plt.hist(moisture_wet, bins=30, alpha=0.5, color='blue', 
             label='Влажные зоны', density=True)
    
    plt.title('Сравнение распределений влажности')
    plt.xlabel('Уровень влажности')
    plt.ylabel('Нормализованная частота')
    plt.legend()
    
    # Статистические метрики
    plt.subplot(246)
    stats_text = (
        f"Сухие зоны (N={len(moisture_dry)}):\n"
        f"μ = {moisture_dry.mean():.3f}\n"
        f"σ = {moisture_dry.std():.3f}\n\n"
        f"Влажные зоны (N={len(moisture_wet)}):\n"
        f"μ = {moisture_wet.mean():.3f}\n"
        f"σ = {moisture_wet.std():.3f}\n"
    )
    plt.text(0.1, 0.5, stats_text, fontsize=12, 
             family='monospace', va='center')
    plt.axis('off')
    plt.title('Статистика распределений')
    
    # Оставшиеся графики
    plt.subplot(247)
    plt.hist(moisture.flatten(), bins=50, alpha=0.7, color='green')
    plt.title('Общее распределение влажности')
    plt.xlabel('Влажность')
    plt.ylabel('Частота')
    
    plt.subplot(248)
    plt.scatter(X, y, alpha=0.3, label='Данные')
    x_range = np.linspace(X.min(), X.max(), 100)
    plt.plot(x_range, model.predict(scaler.transform(x_range.reshape(-1, 1))), 
            'r-', lw=2, label='Модель')
    plt.xlabel('NDWI')
    plt.ylabel('Влажность')
    plt.legend()
    plt.title('Регрессионная зависимость')
    
    plt.tight_layout()
    plt.show()
process_and_visualize()