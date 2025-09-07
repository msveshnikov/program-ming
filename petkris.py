import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import pygame

pygame.mixer.init()

class DesktopPet:
    def __init__(self, window):
        self.window = window
        self.window.title("Desktop Pet")
        # Make window borderless, stay on top, and transparent
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True, '-transparentcolor', 'black')
        self.window.configure(bg='black')
        # Load sprites with transparency
        self.sprites = []
        for sprite in ['l.png', 'r.png']:
            image = Image.open(sprite)
            image = image.resize((128, 128), Image.Resampling.LANCZOS)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            self.sprites.append(ImageTk.PhotoImage(image))
        self.label = tk.Label(window, image=self.sprites[0], bg='black', bd=0)
        self.label.pack()
        # Initialize variables
        self.current_sprite = 0
        self.moving = False
        self.direction = 1  # 1 for right, -1 for left
        self.running = False
        self.dancing = False
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
        self.label.bind('<Button-3>', self.quit_program)
        
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

        # Показать меню действий
        self.show_menu(event)

    def show_menu(self, event):
        menu = tk.Menu(self.window, tearoff=0)
        menu.add_command(label="Сидеть", command=self.sit)
        menu.add_command(label="Бежать", command=self.run)
        menu.add_command(label="Танцевать", command=self.dance)
        # Позиционируем меню над питомцем
        x = self.window.winfo_x() + event.x
        y = self.window.winfo_y() + event.y - 40  # чуть выше
        menu.tk_popup(x, y)

    def sit(self):
        print("Питомец сел!")
        self.moving = False
        self.dancing = False
        self.running = False
        self.move_speed = 2
        self.move_delay = 50
        self.label.configure(image=self.sprites[2])  # если сидячий спрайт — третий
        self.label.image = self.sprites[2]

    def run(self):
        print("Питомец бежит!")
        self.moving = True
        self.running = True
        self.dancing = False
        self.move_speed = 8  # ускорение
        self.move_delay = 20
        self.direction = 1

    def dance(self):
        print("Питомец танцует!")
        self.moving = True
        self.dancing = True
        self.running = False
        self.move_speed = 10
        self.move_delay = 30
    
    def on_drag(self, event):
        x = self.window.winfo_x() + event.x - self.x
        y = self.window.winfo_y() + event.y - self.y
        self.window.geometry(f'+{x}+{y}')
    
    def quit_program(self, event):
        self.window.quit()
    
    def animate(self):
        # Switch between sprites
        self.current_sprite = (self.current_sprite + 1) % 2
        # Отразить изображение, если идём вправо
        if self.direction == 1:
            # Получаем исходное изображение
            from PIL import ImageOps
            sprite_path = ['l.png', 'r.png'][self.current_sprite]
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
        self.window.after(200, self.animate)  # Change sprite every 200ms
    
    def move(self):
        if not self.moving:
            # Randomly decide to start moving (если не сидит)
            if not self.running and not self.dancing:
                self.moving = random.random() < 0.3
                if self.moving:
                    self.direction = random.choice([-1, 1])
        
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
    pet = DesktopPet(root)
    root.mainloop()