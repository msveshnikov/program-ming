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
        pygame.display.set_caption("Blender Model Viewer")
        
        # Настройки OpenGL
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Настройка освещения
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
        
        # Настройка перспективы
        gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
        
        # Начальная позиция камеры
        glTranslatef(0.0, 0.0, self.zoom)
        
    def draw_model(self):
        """Отрисовка 3D модели"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        # Применяем вращение
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)
        
        # Отрисовка модели
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            # Вычисляем нормаль для освещения
            if len(face) >= 3:
                v1 = np.array(self.vertices[face[0]])
                v2 = np.array(self.vertices[face[1]])
                v3 = np.array(self.vertices[face[2]])
                
                # Вычисляем нормаль
                normal = np.cross(v2 - v1, v3 - v1)
                normal = normal / np.linalg.norm(normal)
                
                glNormal3fv(normal)
                
                # Отрисовываем треугольник
                for vertex_index in face:
                    glVertex3fv(self.vertices[vertex_index])
        glEnd()
        
        # Отрисовка wireframe
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glColor3f(0.2, 0.2, 0.2)
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex_index in face:
                glVertex3fv(self.vertices[vertex_index])
        glEnd()
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glColor3f(0.8, 0.8, 0.8)
        
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
                    
        return True
    
    def run(self):
        """Главный цикл программы"""
        print("Загрузка .blend файла...")
        if not self.load_blend_file():
            print("Не удалось загрузить модель")
            return
            
        print("Инициализация графики...")
        self.init_pygame()
        
        print("Запуск viewer'а...")
        print("Управление:")
        print("- Левая кнопка мыши + перемещение: вращение модели")
        print("- + / -: приближение/отдаление")
        print("- ESC: выход")
        
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