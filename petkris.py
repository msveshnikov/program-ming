
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
            # Resize image to a larger size (128x128 pixels)
            image = image.resize((128, 128), Image.Resampling.LANCZOS)
            # Convert image to RGBA if it isn't already
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            self.sprites.append(ImageTk.PhotoImage(image))
        
        # Create label to display the pet with transparent background
        self.label = tk.Label(window, image=self.sprites[0], bg='black', bd=0)
        self.label.pack()
        
        # Initialize variables
        self.current_sprite = 0
        self.moving = False
        self.direction = 1  # 1 for right, -1 for left
        
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
        
        fart = pygame.mixer.Sound('fart.mp3')
        fart.play()
        
    
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
            # Randomly decide to start moving
            self.moving = random.random() < 0.3
            if self.moving:
                self.direction = random.choice([-1, 1])
        
        if self.moving:
            # Move the pet
            x = self.window.winfo_x() + (2 * self.direction)
            y = self.window.winfo_y()
            
            # Check boundaries (adjusted for 128px width)
            if x < 0 or x > self.screen_width - 128:
                self.direction *= -1
                x = max(0, min(x, self.screen_width - 128))
                self.moving = False
            
            self.window.geometry(f'+{x}+{y}')
            
            # Randomly stop moving
            if random.random() < 0.02:
                self.moving = False
        
        self.window.after(50, self.move)  # Update position every 50ms

if __name__ == "__main__":
    root = tk.Tk()
    pet = DesktopPet(root)
    root.mainloop()