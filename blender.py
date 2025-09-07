import bpy
import bmesh
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import os

class BlenderModelViewer:
    def __init__(self, blend_file_path):
        self.blend_file_path = blend_file_path
        self.vertices = []
        self.faces = []
        self.rotation_x = 0
        self.rotation_y = 0
        self.zoom = -5
        self.mouse_x = 0
        self.mouse_y = 0
        self.mouse_pressed = False
        self.render_mode = 0  # 0 - красивый градиент, 1 - металлик, 2 - пастельный
        self.auto_rotate = False
        
    def load_blend_file(self):
        """Загружает .blend файл и извлекает геометрию"""
        try:
            # Очищаем сцену
            bpy.ops.wm.read_factory_settings(use_empty=True)
            
            # Загружаем .blend файл
            bpy.ops.wm.open_mainfile(filepath=self.blend_file_path)
            
            # Получаем все mesh объекты
            mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
            
            if not mesh_objects:
                print("В файле не найдено mesh объектов")
                return False
                
            # Берем первый mesh объект
            obj = mesh_objects[0]
            
            # Переходим в режим редактирования
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            
            # Создаем bmesh из mesh
            bm = bmesh.from_edit_mesh(obj.data)
            
            # Применяем триангуляцию
            bmesh.ops.triangulate(bm, faces=bm.faces)
            
            # Извлекаем вертексы
            self.vertices = [(v.co.x, v.co.y, v.co.z) for v in bm.verts]
            
            # Извлекаем грани (треугольники)
            self.faces = [[v.index for v in face.verts] for face in bm.faces]
            
            # Возвращаемся в объектный режим
            bpy.ops.object.mode_set(mode='OBJECT')
            
            print(f"Загружено {len(self.vertices)} вертексов и {len(self.faces)} граней")
            return True
            
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
            return False
    
    def init_pygame(self):
        """Инициализация pygame и OpenGL"""
        pygame.init()
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Beautiful Blender Model Viewer")
        
        # Настройки OpenGL для красивого рендеринга
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_NORMALIZE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glShadeModel(GL_SMOOTH)
        
        # Настройка материалов
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Основное освещение (тёплый белый свет)
        glLightfv(GL_LIGHT0, GL_POSITION, [2, 3, 5, 1])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.95, 0.8, 1.0])  # Тёплый белый
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.4, 1.0])   # Мягкий синеватый ambient
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])  # Яркие блики
        
        # Дополнительное освещение (заполняющий свет)
        glLightfv(GL_LIGHT1, GL_POSITION, [-2, -1, 3, 1])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.4, 0.5, 0.8, 1.0])   # Холодный голубой
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.1, 0.1, 0.2, 1.0])
        
        # Настройка материала
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64.0)
        
        # Красивый фон
        glClearColor(0.1, 0.1, 0.15, 1.0)  # Тёмно-синий фон
        
        # Настройка перспективы
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        
        # Начальная позиция камеры
        glTranslatef(0.0, 0.0, self.zoom)
        
    def get_vertex_color(self, vertex, face_index, vertex_index_in_face):
        """Получает цвет вертекса в зависимости от режима рендеринга"""
        height_factor = (vertex[1] + 2) / 4
        height_factor = max(0, min(1, height_factor))
        
        if self.render_mode == 0:  # Градиент розовый-голубой
            r = 0.9 - height_factor * 0.4
            g = 0.3 + height_factor * 0.4
            b = 0.4 + height_factor * 0.5
            
        elif self.render_mode == 1:  # Металлический
            base_metallic = 0.6 + height_factor * 0.3
            r = base_metallic * 0.8
            g = base_metallic * 0.85
            b = base_metallic * 0.9
            
        else:  # Пастельные тона
            r = 0.8 + height_factor * 0.15
            g = 0.7 + height_factor * 0.25
            b = 0.6 + height_factor * 0.35
        
        # Добавляем вариацию по граням
        face_variation = (face_index % 15) / 30.0
        r += face_variation * 0.1
        g += face_variation * 0.05
        b += face_variation * 0.1
        
        return (max(0, min(1, r)), max(0, min(1, g)), max(0, min(1, b)))
        
    def draw_model(self):
        """Отрисовка 3D модели с красивыми материалами"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        # Автоповорот если включён
        if self.auto_rotate:
            self.rotation_y += 0.5
        
        # Применяем вращение
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        # Отрисовка модели с красивыми материалами
        glEnable(GL_LIGHTING)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        
        # Основные грани с красивыми материалами
        glBegin(GL_TRIANGLES)
        for i, face in enumerate(self.faces):
            if len(face) >= 3:
                v1 = np.array(self.vertices[face[0]])
                v2 = np.array(self.vertices[face[1]])
                v3 = np.array(self.vertices[face[2]])
                
                # Вычисляем нормаль для освещения
                normal = np.cross(v2 - v1, v3 - v1)
                if np.linalg.norm(normal) > 0:
                    normal = normal / np.linalg.norm(normal)
                    glNormal3fv(normal)
                
                # Отрисовываем треугольник с красивыми цветами
                for j, vertex_index in enumerate(face):
                    vertex = self.vertices[vertex_index]
                    r, g, b = self.get_vertex_color(vertex, i, j)
                    glColor3f(r, g, b)
                    glVertex3fv(vertex)
        glEnd()
        
        # Добавляем тонкие контуры для большей детализации
        glDisable(GL_LIGHTING)
        glLineWidth(0.8)
        glColor4f(0.15, 0.15, 0.25, 0.4)  # Полупрозрачные контуры
        
        glBegin(GL_LINES)
        edge_count = 0
        for face in self.faces:
            if len(face) >= 3 and edge_count < len(self.faces) * 2:  # Ограничиваем количество линий
                for i in range(len(face)):
                    if (i + edge_count) % 3 == 0:  # Рисуем только каждую третью линию
                        v1 = self.vertices[face[i]]
                        v2 = self.vertices[face[(i + 1) % len(face)]]
                        glVertex3fv(v1)
                        glVertex3fv(v2)
                        edge_count += 1
        glEnd()
        
        glPopMatrix()
        pygame.display.flip()
    
    def handle_events(self):
        """Обработка событий мыши и клавиатуры"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    self.mouse_pressed = True
                    self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                    
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_pressed = False
                    
            elif event.type == pygame.MOUSEMOTION:
                if self.mouse_pressed:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    dx = mouse_x - self.mouse_x
                    dy = mouse_y - self.mouse_y
                    
                    self.rotation_y += dx * 0.5
                    self.rotation_x += dy * 0.5
                    
                    self.mouse_x = mouse_x
                    self.mouse_y = mouse_y
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    self.zoom += 0.5
                    glTranslatef(0, 0, 0.5)
                elif event.key == pygame.K_MINUS:
                    self.zoom -= 0.5
                    glTranslatef(0, 0, -0.5)
                elif event.key == pygame.K_SPACE:
                    # Переключение режима рендеринга
                    self.render_mode = (self.render_mode + 1) % 3
                    mode_names = ["Градиент", "Металлик", "Пастель"]
                    print(f"Режим рендеринга: {mode_names[self.render_mode]}")
                elif event.key == pygame.K_r:
                    # Включение/выключение автоповорота
                    self.auto_rotate = not self.auto_rotate
                    print(f"Автоповорот: {'включён' if self.auto_rotate else 'выключен'}")
                elif event.key == pygame.K_h:
                    # Показать справку
                    print("\n=== УПРАВЛЕНИЕ ===")
                    print("Мышь: вращение модели")
                    print("+/-: приближение/отдаление")
                    print("SPACE: смена материала")
                    print("R: автоповорот")
                    print("H: эта справка")
                    print("ESC: выход\n")
                    
        return True
    
    def run(self):
        """Главный цикл программы"""
        print("Загрузка .blend файла...")
        if not self.load_blend_file():
            print("Не удалось загрузить модель")
            return
            
        print("Инициализация графики...")
        self.init_pygame()
        
        print("Запуск красивого viewer'а...")
        print("🎨 УПРАВЛЕНИЕ:")
        print("🖱️  Левая кнопка мыши + перемещение: вращение модели")
        print("🔍 + / -: приближение/отдаление")
        print("🎭 SPACE: смена стиля материала (Градиент/Металлик/Пастель)")
        print("🔄 R: автоповорот")
        print("❓ H: показать справку")
        print("🚪 ESC: выход")
        print("\nТекущий материал: Градиент (розовый-голубой)")
        
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.draw_model()
            clock.tick(60)
            
        pygame.quit()

def main():
    # Путь к .blend файлу
    blend_file = "susie.blend"
    
    # Проверяем существование файла
    if not os.path.exists(blend_file):
        print(f"Файл {blend_file} не найден в текущей директории")
        return
    
    # Создаем и запускаем viewer
    viewer = BlenderModelViewer(blend_file)
    viewer.run()

if __name__ == "__main__":
    main()