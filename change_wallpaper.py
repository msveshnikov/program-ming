#!/usr/bin/env python3
"""
Простой скрипт для смены фона рабочего стола Windows
Может использоваться отдельно от программы питомца
"""

import ctypes
import os
import random
import shutil
import sys


def set_wallpaper(image_path):
    """Изменяет фоновое изображение рабочего стола Windows"""
    try:
        # Константы для Windows API
        SPI_SETDESKWALLPAPER = 0x0014
        SPIF_UPDATEINIFILE = 0x01
        SPIF_SENDCHANGE = 0x02
        
        # Проверяем, существует ли файл
        if not os.path.exists(image_path):
            print(f"Файл {image_path} не найден!")
            return False
        
        # Получаем абсолютный путь
        abs_path = os.path.abspath(image_path)
        
        # Копируем изображение в папку пользователя (иногда требуется)
        user_folder = os.path.expanduser("~")
        wallpaper_folder = os.path.join(user_folder, "Desktop_Wallpapers")
        if not os.path.exists(wallpaper_folder):
            os.makedirs(wallpaper_folder)
        
        wallpaper_path = os.path.join(wallpaper_folder, os.path.basename(image_path))
        shutil.copy2(abs_path, wallpaper_path)
        
        # Устанавливаем обои через Windows API
        result = ctypes.windll.user32.SystemParametersInfoW(
            SPI_SETDESKWALLPAPER,
            0,
            wallpaper_path,
            SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        
        if result:
            print(f"Фон рабочего стола изменён на: {wallpaper_path}")
            return True
        else:
            print("Не удалось изменить фон рабочего стола")
            return False
            
    except Exception as e:
        print(f"Ошибка при изменении фона: {e}")
        return False


def change_wallpaper_random():
    """Меняет фон на случайное изображение из текущей папки"""
    # Список поддерживаемых форматов изображений
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    
    # Получаем все изображения в текущей папке
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_files = []
    
    for file in os.listdir(current_dir):
        if any(file.lower().endswith(ext) for ext in image_extensions):
            image_files.append(os.path.join(current_dir, file))
    
    if image_files:
        # Выбираем случайное изображение
        selected_image = random.choice(image_files)
        print(f"Выбрано изображение: {os.path.basename(selected_image)}")
        return set_wallpaper(selected_image)
    else:
        print("В папке не найдено подходящих изображений!")
        return False


def main():
    """Главная функция для работы из командной строки"""
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python change_wallpaper.py random          - случайное изображение")
        print("  python change_wallpaper.py <filename>      - конкретный файл")
        print("  python change_wallpaper.py classroom.png   - например")
        return
    
    command = sys.argv[1].lower()
    
    if command == "random":
        change_wallpaper_random()
    else:
        # Предполагаем, что это имя файла
        filename = sys.argv[1]
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, filename)
        set_wallpaper(image_path)


if __name__ == "__main__":
    main()
