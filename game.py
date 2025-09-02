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
background_image = pygame.image.load('classroom.png')
player_image = pygame.image.load('kris.png')
susie_image = pygame.image.load('susie.png')
ralsei_image = pygame.image.load('ralsei.png')
svenka_image = pygame.image.load('svenka.png')  # Добавляем нового NPC
background_battle = pygame.image.load('background_battle.png')
background_battle = pygame.transform.scale(background_battle, (WIDTH, HEIGHT))

# Размеры персонажей
player_size = 100
npc_size = 100

# Масштабирование фона под размер окна
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
player_image = pygame.transform.scale(player_image, (player_size, player_size))
susie_image = pygame.transform.scale(susie_image, (npc_size, npc_size))
ralsei_image = pygame.transform.scale(ralsei_image, (npc_size, npc_size))
svenka_image = pygame.transform.scale(svenka_image, (npc_size, npc_size))  # Масштабирование изображений

player_battle_size = 400
npc_battle_size = 400

# Создадим масштабированные версии изображений для боя
player_battle_image = pygame.transform.scale(player_image, (player_battle_size, player_battle_size))
susie_battle_image = pygame.transform.scale(susie_image, (npc_battle_size, npc_battle_size))
ralsei_battle_image = pygame.transform.scale(ralsei_image, (npc_battle_size, npc_battle_size))
svenka_battle_image = pygame.transform.scale(svenka_image, (npc_battle_size, npc_battle_size))

# Параметры персонажей
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 10
game_over = False  # Добавляем переменную для отслеживания конца игры

# Параметры NPC
class NPC:
    def __init__(self, x, y, image, hunting=False):
        self.x = x
        self.y = y
        self.image = image
        self.base_speed = 5  # Базовая скорость
        self.speed = self.base_speed
        self.hunting = hunting
        self.random_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.direction_timer = 0
        self.health = 100  # Добавляем здоровье NPC
        self.damage = 20   # Урон NPC
        self.in_battle = False  # Флаг боевого режима
    
    def move(self, target_x, target_y):
        self.speed = self.base_speed + random.uniform(-2, 2)
        
        if self.hunting:
            # Охотящийся NPC движется к игроку
            dx = target_x - self.x
            dy = target_y - self.y
        else:
            # Обновляем случайное направление каждые 60 кадров
            if self.direction_timer <= 0:
                self.random_direction = [random.uniform(-1, 1), random.uniform(-1, 1)]
                self.direction_timer = 60
            self.direction_timer -= 1
            
            dx, dy = self.random_direction
        
        # Нормализуем вектор движения
        distance = math.sqrt(dx**2 + dy**2)
        if distance != 0:
            dx = dx / distance
            dy = dy / distance
        
        # Движение NPC
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Проверка границ экрана и отражение при достижении границ
        if not (0 <= new_x <= WIDTH - npc_size):
            self.random_direction[0] *= -1
            new_x = max(0, min(new_x, WIDTH - npc_size))
        if not (0 <= new_y <= HEIGHT - npc_size):
            self.random_direction[1] *= -1
            new_y = max(0, min(new_y, HEIGHT - npc_size))
            
        self.x = new_x
        self.y = new_y
    
    def check_collision(self, player_x, player_y):
        # Проверяем столкновение с игроком
        player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
        npc_rect = pygame.Rect(self.x, self.y, npc_size, npc_size)
        return player_rect.colliderect(npc_rect)

# Создание NPC с параметром hunting
susie = NPC(0, 0, susie_image, hunting=False)
ralsei = NPC(00, 500, ralsei_image, hunting=False)
svenka = NPC(WIDTH - 100, HEIGHT - 100, svenka_image, hunting=True)  # Добавляем злого NPC

# Параметры звука
footstep_sound = pygame.mixer.Sound('footsteps.mp3')
background_music = pygame.mixer.Sound('music.mp3')  # Добавляем фоновую музыку
battle_music = pygame.mixer.Sound('battle.mp3')
is_playing = False

# Запускаем фоновую музыку
background_music.play(-1)  # -1 означает бесконечное воспроизведение

# Игровой цикл
clock = pygame.time.Clock()

# В начале файла добавим глобальные переменные для боевого режима
player_health = 100
battle_mode = False
current_enemy = None
battle_timer = 0
BATTLE_COOLDOWN = 60  # Задержка между атаками (в кадрах)
battle_font = pygame.font.Font(None, 36)
battle_instructions_font = pygame.font.Font(None, 74)  # Больший шрифт для инструкций

# Функция для отрисовки боевого интерфейса
def draw_health_bar(x, y, health, max_health, width=200, height=20):
    ratio = health / max_health
    pygame.draw.rect(WINDOW, (255, 0, 0), (x, y, width, height))
    pygame.draw.rect(WINDOW, (0, 255, 0), (x, y, width * ratio, height))

def draw_battle_ui():
    # Отрисовка здоровья игрока
    draw_health_bar(50, HEIGHT - 100, player_health, 100)
    player_health_text = battle_font.render(f'HP: {player_health}', True, (255, 255, 255))
    WINDOW.blit(player_health_text, (150, HEIGHT - 130))
    
    # Отрисовка здоровья врага
    if current_enemy:
        draw_health_bar(WIDTH - 250, HEIGHT - 100, current_enemy.health, 100)
        enemy_health_text = battle_font.render(f'HP: {current_enemy.health}', True, (255, 0, 0))
        WINDOW.blit(enemy_health_text, (WIDTH - 250, HEIGHT - 130))
    
    # Добавим инструкцию про лечение
    battle_instructions = battle_instructions_font.render('Z - атака, X - лечение, ESC - побег', True, (255, 255, 0))
    instructions_rect = battle_instructions.get_rect(center=(WIDTH/2, HEIGHT - 50))
    WINDOW.blit(battle_instructions, instructions_rect)

# Глобальные переменные для анимации
player_battle_x = WIDTH // 4 - player_battle_size // 2
enemy_battle_x = (WIDTH * 3) // 4 - npc_battle_size // 2
player_battle_shake = 0
enemy_battle_shake = 0
SHAKE_AMOUNT = 20
SHAKE_SPEED = 5

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
        svenka.move(player_x, player_y)  # В игровом цикле добавляем движение и проверку столкновений
        
        # Проверка столкновений
        if svenka.check_collision(player_x, player_y) and not battle_mode:
            battle_mode = True
            current_enemy = svenka
            background_music.stop()
            battle_music.play(-1)  # Запускаем боевую музыку

        # При выходе из боевого режима
        if battle_mode and (current_enemy.health <= 0 or (keys[pygame.K_ESCAPE] and random.random() < 0.3)):
            battle_mode = False
            current_enemy = None
            battle_music.stop()
            background_music.play(-1)
        
        # Добавляем обработку боевого режима
        if battle_mode:
            keys = pygame.key.get_pressed()
            if battle_timer <= 0:
                if keys[pygame.K_z]:  # Атака
                    damage = random.randint(15, 25)
                    current_enemy.health -= damage
                    enemy_battle_shake = SHAKE_AMOUNT
                    battle_timer = BATTLE_COOLDOWN
                    
                    # Ответная атака врага
                    player_damage = random.randint(10, 20)
                    player_health -= player_damage
                    player_battle_shake = SHAKE_AMOUNT
        
                elif keys[pygame.K_x]:  # Лечение
                    player_health = 100  # Полное восстановление здоровья
                    battle_timer = BATTLE_COOLDOWN
                    
                    # Враг всё равно атакует
                    player_damage = random.randint(10, 20)
                    player_health -= player_damage
                    player_battle_shake = SHAKE_AMOUNT

                if keys[pygame.K_ESCAPE]:  # Попытка сбежать
                    if random.random() < 0.3:  # 30% шанс сбежать
                        battle_mode = False
                        current_enemy = None
                        battle_music.stop()
                        background_music.play(-1)
                    else:
                        player_health -= random.randint(5, 15)  # Урон при неудачной попытке
                    battle_timer = BATTLE_COOLDOWN
            
            battle_timer = max(0, battle_timer - 1)
            
            # Проверка окончания боя
            if current_enemy and current_enemy.health <= 0:
                battle_mode = False
                current_enemy = None
                background_music.play(-1)
            
            if player_health <= 0:
                game_over = True
                background_music.stop()
    
    # Отрисовка
    if battle_mode:
        WINDOW.blit(background_battle, (0, 0))
        
        # Позиционирование персонажей с учетом тряски
        current_player_x = player_battle_x + player_battle_shake
        current_enemy_x = enemy_battle_x - enemy_battle_shake
        player_battle_y = HEIGHT // 2 - player_battle_size // 2
        enemy_battle_y = HEIGHT // 2 - npc_battle_size // 2
        
        # Отрисовка только сражающихся персонажей
        WINDOW.blit(player_battle_image, (current_player_x, player_battle_y))
        if current_enemy:
            if current_enemy == svenka:
                WINDOW.blit(svenka_battle_image, (current_enemy_x, enemy_battle_y))
            elif current_enemy == susie:
                WINDOW.blit(susie_battle_image, (current_enemy_x, enemy_battle_y))
            elif current_enemy == ralsei:
                WINDOW.blit(ralsei_battle_image, (current_enemy_x, enemy_battle_y))
        
        draw_battle_ui()
    else:
        WINDOW.blit(background_image, (0, 0))
        if not game_over:
            WINDOW.blit(player_image, (player_x, player_y))
            # Отрисовка NPC только вне боевого режима
            if not battle_mode:
                WINDOW.blit(susie.image, (susie.x, susie.y))
                WINDOW.blit(ralsei.image, (ralsei.x, ralsei.y))
                WINDOW.blit(svenka.image, (svenka.x, svenka.y))
    
    if game_over:
        # Отображаем текст Game Over
        font = pygame.font.Font(None, 74)
        text = font.render('Game Over', True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        WINDOW.blit(text, text_rect)
    
    pygame.display.update()
    
    # Ограничение FPS
    clock.tick(60)