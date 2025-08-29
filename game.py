import pygame
import sys
import random
import math

# Инициализация Pygame и mixer
pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH = 1800
HEIGHT = 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("my deltarune")

# Загрузка изображений
background_image = pygame.image.load('krisroom.png')  # Добавляем загрузку фона
player_image = pygame.image.load('kris.png')
susie_image = pygame.image.load('susie.png')
ralsei_image = pygame.image.load('ralsei.png')

# Размеры персонажей
player_size = 100
npc_size = 100

# Масштабирование фона под размер окна
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.transform.scale(player_image, (player_size, player_size))
susie_image = pygame.transform.scale(susie_image, (npc_size, npc_size))
ralsei_image = pygame.transform.scale(ralsei_image, (npc_size, npc_size))


# Параметры персонажей
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 10
game_over = False  # Добавляем переменную для отслеживания конца игры

# Параметры NPC
class NPC:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.base_speed = 5  # Базовая скорость
        self.speed = self.base_speed
    
    def move(self, target_x, target_y):
        # Случайное изменение скорости в пределах ±2 от базовой скорости
        self.speed = self.base_speed + random.uniform(-2, 2)
        
        # Вычисляем направление к игроку
        dx = target_x - self.x
        dy = target_y - self.y
        
        # Нормализуем вектор движения
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx = dx / distance
            dy = dy / distance
        
        # Движение NPC к игроку
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Проверка границ экрана
        if 0 <= new_x <= WIDTH - npc_size:
            self.x = new_x
        if 0 <= new_y <= HEIGHT - npc_size:
            self.y = new_y
    
    def check_collision(self, player_x, player_y):
        # Проверяем столкновение с игроком
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        npc_rect = pygame.Rect(self.x, self.y, npc_size, npc_size)
        return player_rect.colliderect(npc_rect)

# Создание NPC
susie = NPC(0, 0, susie_image)
ralsei = NPC(00, 500, ralsei_image)
zuza = NPC(50, 50, susie_image)

# Параметры звука
footstep_sound = pygame.mixer.Sound('footsteps.mp3')
background_music = pygame.mixer.Sound('music.mp3')  # Добавляем фоновую музыку
is_playing = False

# Запускаем фоновую музыку
background_music.play(-1)  # -1 означает бесконечное воспроизведение

# Игровой цикл
clock = pygame.time.Clock()

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    if not game_over:
        # Управление персонажем
        keys = pygame.key.get_pressed()
        moved = False
        
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
            moved = True
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
            moved = True
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
            moved = True
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_size:
            player_y += player_speed
            moved = True
        
        # Движение NPC к игроку
        susie.move(player_x, player_y)
        ralsei.move(player_x, player_y)
        zuza.move(player_x, player_y)
        
        # Проверка столкновений
        if (susie.check_collision(player_x, player_y) or 
            ralsei.check_collision(player_x, player_y) or 
            zuza.check_collision(player_x, player_y)):
            game_over = True
            background_music.stop()
        
        # Управление звуком
        if moved and not is_playing:
            footstep_sound.play(-1)
            is_playing = True
        elif not moved and is_playing:
            footstep_sound.stop()
            is_playing = False
    
    # Отрисовка
    WINDOW.blit(background_image, (0, 0))
    
    if not game_over:
        WINDOW.blit(player_image, (player_x, player_y))
    WINDOW.blit(susie.image, (susie.x, susie.y))
    WINDOW.blit(susie.image, (zuza.x, zuza.y))
    WINDOW.blit(ralsei.image, (ralsei.x, ralsei.y))
    
    if game_over:
        # Отображаем текст Game Over
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        WINDOW.blit(text, text_rect)
    
    pygame.display.update()
    
    # Ограничение FPS
    clock.tick(60)