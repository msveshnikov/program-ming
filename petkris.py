import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import pygame
import ctypes
from ctypes import wintypes
import shutil

pygame.mixer.init()

class DesktopPet:
    def reset_action(self):
        self.moving = False
        self.running = False
        self.dancing = False
        self.sitting = False
        self.eating = False
        self.move_speed = 2
        self.move_delay = 50

    def __init__(self, window, sprites, title="Desktop Pet"):
        self.window = window
        self.window.title(title)
        self.eating = False
        # Make window borderless, stay on top, and transparent
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True, '-transparentcolor', 'black')
        self.window.configure(bg='black')
        # Load sprites with transparency
        self.sprite_paths = sprites  # сохраняем пути для зеркалирования
        self.sprites = []
        for sprite in sprites:
            image = Image.open(sprite)
            image = image.resize((128, 128), Image.Resampling.LANCZOS)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            self.sprites.append(ImageTk.PhotoImage(image))

        self.eating_sprite = None
        if title == "Susie":  # Only for Susie pet
            try:
                eat_image = Image.open('susie_eat/susie_eat1.png')
                eat_image = eat_image.resize((128, 128), Image.Resampling.LANCZOS)
                if eat_image.mode != 'RGBA':
                    eat_image = eat_image.convert('RGBA')
                self.eating_sprite = ImageTk.PhotoImage(eat_image)
            except FileNotFoundError:
                print("susie_eat/susie_eat1.png not found, using default sprites")
        
        
        # Load sitting sprite if available
        self.sitting_sprite = None
        if title == "Kris":  # Only for Kris pet
            try:
                sit_image = Image.open('kris_sit.png')
                sit_image = sit_image.resize((128, 128), Image.Resampling.LANCZOS)
                if sit_image.mode != 'RGBA':
                    sit_image = sit_image.convert('RGBA')
                self.sitting_sprite = ImageTk.PhotoImage(sit_image)
            except FileNotFoundError:
                print("kris_sit.png not found, using default sprites")
        
        self.label = tk.Label(window, image=self.sprites[0], bg='black', bd=0)
        self.label.pack()
        # Initialize variables
        self.current_sprite = 0
        self.moving = False
        self.direction = 1  # 1 for right, -1 for left
        self.running = False
        self.dancing = False
        self.sitting = False
        self.move_speed = 2
        self.move_delay = 50
        
        # Window dimensions
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        
        # Set initial position (adjusted for 128px size)
        self.x = random.randint(0, self.screen_width - 128)
        self.y = random.randint(0, self.screen_height - 128)
        self.window.geometry(f'+{self.x}+{self.y}')
        
        # Bind mouse events
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.on_drag)
        self.label.bind('<Button-3>', self.show_menu)
        
        # Bind keyboard events for background changing
        # self.window.bind('<Control-b>', lambda e: self.change_background_random())
        # self.window.bind('<Control-1>', lambda e: self.change_background_specific("classroom.png"))
        # self.window.bind('<Control-2>', lambda e: self.change_background_specific("background_battle.png"))
        # self.window.bind('<Control-3>', lambda e: self.change_background_specific("Krisroom.png"))
        
        # Make window focusable for keyboard events
        self.window.focus_set()
        
        # Start animation
        self.animate()
        self.move()
    
    def start_drag(self, event):
        self.moving = False
        self.x = event.x
        self.y = event.y
        # Питомец "пукает" при клике
        # try:
        #     fart = pygame.mixer.Sound('fart.mp3')
        #     fart.play()
        # except Exception as e:
        #     print(f"Ошибка воспроизведения звука: {e}")
        # ...existing code...

    def show_menu(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Сидеть", command=self.sit)
        menu.add_command(label="Бежать", command=self.run)
        menu.add_command(label="Танцевать", command=self.dance)
        menu.add_command(label="Лежать", command=self.lie_down)
        menu.add_command(label="Стоять", command=self.stand)
        menu.add_command(label="Гулять", command=self.walk)
        menu.add_command(label="Спать", command=self.sleep)
        menu.add_command(label="Есть", command=self.eat)
        menu.add_command(label="Пить", command=self.drink)
        menu.add_separator()
        
        # Подменю для смены фона
        # background_menu = tk.Menu(menu, tearoff=0)
        # background_menu.add_command(label="Случайный фон", command=self.change_background_random)
        # background_menu.add_command(label="Фон из класса", command=lambda: self.change_background_specific("classroom.png"))
        # background_menu.add_command(label="Фон битвы", command=lambda: self.change_background_specific("background_battle.png"))
        # background_menu.add_command(label="Комната Криса", command=lambda: self.change_background_specific("Krisroom.png"))
        
        # menu.add_cascade(label="Сменить фон", menu=background_menu)
        # menu.add_separator()
        menu.add_command(label="Выйти", command=self.quit_program)
        # Позиционируем меню над питомцем
        x = self.window.winfo_x() + event.x
        y = self.window.winfo_y() + event.y - 40  # чуть выше
        menu.tk_popup(x, y)

    def sit(self):
        print("Питомец сел!")
        self.moving = False
        self.dancing = False
        self.running = False
        self.sitting = True
        self.move_speed = 0
        self.move_delay = 50
        self.window.after(300000, self.reset_action)

    def run(self):
        print("Питомец бежит!")
        self.moving = True
        self.running = True
        self.dancing = False
        self.move_speed = 8  # ускорение
        self.move_delay = 20
        self.direction = 1
        self.window.after(3000, self.reset_action)

    def dance(self):
        print("Питомец танцует!")
        self.moving = True
        self.dancing = True
        self.running = False
        self.move_speed = 10
        self.move_delay = 30
        self.window.after(200000, self.reset_action)

    def lie_down(self):
        print("Питомец лежит!")
        self.moving = False
        self.dancing = False
        self.running = False
        self.move_speed = 0
        self.window.after(5000, self.reset_action)

    def stand(self):
        print("Питомец стоит!")
        self.reset_action()

    def walk(self):
        print("Питомец гуляет!")
        self.moving = True
        self.running = False
        self.dancing = False
        self.move_speed = 2
        self.move_delay = 50
        self.direction = random.choice([-1, 1])
        self.window.after(5000, self.reset_action)

    def sleep(self):
        print("Питомец спит!")
        self.moving = False
        self.dancing = False
        self.running = False
        self.move_speed = 0
        self.window.after(10000, self.reset_action)

    def eat(self):
        print("Питомец ест!")
        self.moving = False
        self.dancing = False
        self.running = False
        self.eating = True
        self.move_speed = 0
        self.window.after(300000, self.reset_action)

    def drink(self):
        print("Питомец пьёт!")
        self.moving = False
        self.dancing = False
        self.running = False
        self.move_speed = 0
        self.window.after(3000, self.reset_action)

    # def set_wallpaper(self, image_path):
    #     """Изменяет фоновое изображение рабочего стола Windows"""
    #     try:
    #         # Константы для Windows API
    #         SPI_SETDESKWALLPAPER = 0x0014
    #         SPIF_UPDATEINIFILE = 0x01
    #         SPIF_SENDCHANGE = 0x02
            
    #         # Проверяем, существует ли файл
    #         if not os.path.exists(image_path):
    #             print(f"Файл {image_path} не найден!")
    #             return False
            
    #         # Получаем абсолютный путь
    #         abs_path = os.path.abspath(image_path)
            
    #         # Копируем изображение в папку пользователя (иногда требуется)
    #         user_folder = os.path.expanduser("~")
    #         wallpaper_folder = os.path.join(user_folder, "Desktop_Wallpapers")
    #         if not os.path.exists(wallpaper_folder):
    #             os.makedirs(wallpaper_folder)
            
    #         wallpaper_path = os.path.join(wallpaper_folder, os.path.basename(image_path))
    #         shutil.copy2(abs_path, wallpaper_path)
            
    #         # Устанавливаем обои через Windows API
    #         result = ctypes.windll.user32.SystemParametersInfoW(
    #             SPI_SETDESKWALLPAPER,
    #             0,
    #             wallpaper_path,
    #             SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
    #         )
            
    #         if result:
    #             print(f"Фон рабочего стола изменён на: {wallpaper_path}")
    #             return True
    #         else:
    #             print("Не удалось изменить фон рабочего стола")
    #             return False
                
    #     except Exception as e:
    #         print(f"Ошибка при изменении фона: {e}")
    #         return False

    # def change_background_random(self):
    #     """Меняет фон на случайное изображение из рабочей папки"""
    #     # Список поддерживаемых форматов изображений
    #     image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
        
    #     # Получаем все изображения в текущей папке
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     image_files = []
        
    #     for file in os.listdir(current_dir):
    #         if any(file.lower().endswith(ext) for ext in image_extensions):
    #             image_files.append(os.path.join(current_dir, file))
        
        # if image_files:
        #     # Выбираем случайное изображение
        #     selected_image = random.choice(image_files)
        #     print(f"Выбрано изображение: {os.path.basename(selected_image)}")
        #     return self.set_wallpaper(selected_image)
        # else:
        #     print("В папке не найдено подходящих изображений!")
        #     return False

    # def change_background_specific(self, filename):
    #     """Меняет фон на конкретное изображение"""
    #     current_dir = os.path.dirname(os.path.abspath(__file__))
    #     image_path = os.path.join(current_dir, filename)
    #     return self.set_wallpaper(image_path)
    
    def on_drag(self, event):
        x = self.window.winfo_x() + event.x - self.x
        y = self.window.winfo_y() + event.y - self.y
        self.window.geometry(f'+{x}+{y}')
    
    def quit_program(self):
        self.window.quit()
    
    def animate(self):
        # If sitting and has sitting sprite, use it
        if self.sitting and self.sitting_sprite:
            self.label.configure(image=self.sitting_sprite)
            self.label.image = self.sitting_sprite
        elif self.eating and self.eating_sprite:
            self.label.configure(image=self.eating_sprite)
            self.label.image = self.eating_sprite
        else:
            # Switch between sprites
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites)
            # Отразить изображение, если идём вправо
            if self.direction == 1:
                from PIL import ImageOps
                sprite_path = self.sprite_paths[self.current_sprite]
                image = Image.open(sprite_path)
                image = image.resize((128, 128), Image.Resampling.LANCZOS)
                if image.mode != 'RGBA':
                    image = image.convert('RGBA')
                image = ImageOps.mirror(image)
                mirrored_sprite = ImageTk.PhotoImage(image)
                self.label.configure(image=mirrored_sprite)
                self.label.image = mirrored_sprite  # чтобы не удалялось GC
            else:
                self.label.configure(image=self.sprites[self.current_sprite])
                self.label.image = self.sprites[self.current_sprite]
        self.window.after(200, self.animate)  # Change sprite every 200ms
    
    def move(self):
        if not self.moving:
            # Randomly decide to start moving (если не сидит)
            if not self.running and not self.dancing and not self.sitting:
                self.moving = random.random() < 0.3
                if self.moving:
                    self.direction = random.choice([-1, 1])
                    self.move_speed = 2  # восстановить обычную скорость
        
        if self.moving:
            x = self.window.winfo_x()
            y = self.window.winfo_y()
            if self.dancing:
                # Хаотичное движение
                dx = random.randint(-self.move_speed, self.move_speed)
                dy = random.randint(-self.move_speed, self.move_speed)
                x += dx
                y += dy
            else:
                # Обычное или ускоренное движение
                x += self.move_speed * self.direction
            # Проверка границ
            x = max(0, min(x, self.screen_width - 128))
            y = max(0, min(y, self.screen_height - 128))
            self.window.geometry(f'+{x}+{y}')
            # Остановить если не run/dance
            if not self.running and not self.dancing and random.random() < 0.02:
                self.moving = False
        self.window.after(self.move_delay, self.move)

if __name__ == "__main__":
    root = tk.Tk()
    # Первый питомец (Крис) — сложная анимация ходьбы
    kris_sprites = [
        'kris1.png', 'kris2.png', 'kris3.png', 'kris4.png'
    ]
    pet_kris = DesktopPet(root, kris_sprites, title="Kris")

    # Второй питомец (Сьюзи) — сложная анимация ходьбы
    susie_sprites = [
        'susie1.png', 'susie2.png', 'susie3.png', 'susie4.png'
    ]
    root2 = tk.Toplevel(root)
    pet_susie = DesktopPet(root2, susie_sprites, title="Susie")
    root.mainloop()