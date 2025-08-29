import pygame
import sys
import random

# Инициализация Pygame и mixer
pygame.init()
pygame.mixer.init()

# Настройки окна
WIDTH = 1800
HEIGHT = 1000
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Движущийся персонаж")

# Цвета
hot_pink = (255, 105, 180)

# Загрузка изображений
player_image = pygame.image.load('kris.png')
susie_image = pygame.image.load('susie.png')
ralsei_image = pygame.image.load('ralsei.png')

# Размеры персонажей
player_size = 300
npc_size = 300

# Масштабирование изображений
player_image = pygame.transform.scale(player_image, (player_size, player_size))
susie_image = pygame.transform.scale(susie_image, (npc_size, npc_size))
ralsei_image = pygame.transform.scale(ralsei_image, (npc_size, npc_size))

# Параметры персонажей
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 10

# Параметры NPC
class NPC:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.direction_timer = 0
        self.direction = [0, 0]
        self.speed = 5
    
    def move(self):
        current_time = pygame.time.get_ticks()
        
        # Меняем направление каждые 2 секунды
        if current_time > self.direction_timer:
            self.direction = [random.randint(-1, 1), random.randint(-1, 1)]
            self.direction_timer = current_time + 2000
        
        # Движение NPC
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Проверка границ экрана
        if 0 <= new_x <= WIDTH - npc_size:
            self.x = new_x
        if 0 <= new_y <= HEIGHT - npc_size:
            self.y = new_y

# Создание NPC
susie = NPC(200, 200, susie_image)
ralsei = NPC(WIDTH - 500, HEIGHT - 500, ralsei_image)

# Параметры звука
footstep_sound = pygame.mixer.Sound('footsteps.mp3')
is_playing = False

# Игровой цикл
clock = pygame.time.Clock()

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
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
    
    # Движение NPC
    susie.move()
    ralsei.move()
    
    # Управление звуком
    if moved and not is_playing:
        footstep_sound.play(-1)
        is_playing = True
    elif not moved and is_playing:
        footstep_sound.stop()
        is_playing = False
    
    # Отрисовка
    WINDOW.fill(hot_pink)
    WINDOW.blit(player_image, (player_x, player_y))
    WINDOW.blit(susie.image, (susie.x, susie.y))
    WINDOW.blit(ralsei.image, (ralsei.x, ralsei.y))
    pygame.display.update()
    
    # Ограничение FPS
    clock.tick(60)