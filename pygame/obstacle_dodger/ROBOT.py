import pygame
import math
import numpy as np

def distance(point1, point2):  # Definir una función para calcular la distancia entre dos puntos
    point1 = np.array(point1)  # Convertir point1 a un arreglo de NumPy
    point2 = np.array(point2)  # Convertir point2 a un arreglo de NumPy
    return np.linalg.norm(point1 - point2)  # Devolver la distancia euclidiana entre los dos puntos

class Robot:
    traveled_position = []
    
    def __init__(self, startpos, width):
        
        self.m2p = 3779.52  # Factor de conversión de metros a píxeles
        # Dimensiones del robot
        self.w = width  # Ancho del robot
        self.x = startpos[0]  # Coordenada inicial x del robot
        self.y = startpos[1]  # Coordenada inicial y del robot
        self.heading = 0  # Orientación inicial del robot (ángulo)
        self.vl = 0.01 * self.m2p  # Velocidad de la rueda izquierda (metros/s)
        self.vr = 0.01 * self.m2p  # Velocidad de la rueda derecha (metros/s)
        self.maxspeed = 0.02 * self.m2p  # Velocidad máxima permitida
        self.minspeed = 0.01 * self.m2p  # Velocidad mínima permitida
        self.min_obs_dist = 65  # Distancia mínima a un obstáculo
        self.count_down = 5  # Temporizador de cuenta regresiva para la evitación de obstáculos (segundos)
        self.action= None
        self.angle_actual= None
        self.objetivo_angle= None
        
    def avoid_obstacles(self, point_cloud, dt):
        closest_obstacle = min(point_cloud, key=lambda point: distance([self.x, self.y], [point[0], point[1]]), default=None)

        if closest_obstacle is None:
            # No hay obstáculos cercanos, avanzar recto
            dist_half = distance([self.x, self.y], [point_cloud[3][0], point_cloud[3][1]])
            self.move_forward(dist_half)  # Realizar movimiento de avance
            
        else:
            obstacle_distance = distance([self.x, self.y], [closest_obstacle[0], closest_obstacle[1]])
            
            if obstacle_distance <= self.min_obs_dist:
                # Hay un obstáculo lo suficientemente cercano como para evitarlo
                if closest_obstacle[2] < 4:
                    self.move_right()
                else:
                    self.move_left()
            else:
                # No hay obstáculos cercanos, avanzar recto
                dist_half = distance([self.x, self.y], [point_cloud[3][0], point_cloud[3][1]])
                self.move_forward(dist_half)  # Realizar movimiento de avance


    def move_backward(self):
        self.vr = -self.minspeed  # Establecer velocidad de la rueda derecha para retroceder
        self.vl = -self.minspeed  # Establecer velocidad de la rueda izquierda para retroceder

    def move_forward(self, point):
        self.vr = self.escalar(point)  # Establecer velocidad de la rueda derecha para avanzar
        self.vl = self.escalar(point)  # Establecer velocidad de la rueda izquierda para avanzar

    def move_left(self):
        self.vr = self.minspeed/2  # Establecer velocidad de la rueda derecha para avanzar
        self.vl = -self.minspeed/ 2**7  # Establecer velocidad de la rueda izquierda para avanzar

    def move_right(self):
        self.vr = -self.minspeed/ 2**7  # Establecer velocidad de la rueda derecha para avanzar
        self.vl = self.minspeed/2  # Establecer velocidad de la rueda izquierda para avanzar
        
    def escalar(self,data):
        return (data-self.min_obs_dist)*((self.maxspeed - self.minspeed/ 2**2 )/( 350 - self.min_obs_dist)) + self.minspeed/ 2**2
    
    def kinematics(self, dt):
        # Calcular la cinemática del movimiento del robot
        self.x += ((self.vl + self.vr) / 2) * math.cos(self.heading) * dt
        self.y -= ((self.vl + self.vr) / 2) * math.sin(self.heading) * dt
        self.heading += (self.vr - self.vl) / self.w * dt

        Robot.traveled_position.append((self.x, self.y))
                                 
        # Asegurarse de que el ángulo de orientación esté dentro del rango (-2*pi a 2*pi)
        if self.heading > 2 * math.pi or self.heading < -2 * math.pi:
            self.heading = 0

        # Limitar las velocidades de las ruedas dentro de los rangos permitidos
        self.vr = max(min(self.maxspeed, self.vr), self.minspeed)
        self.vl = max(min(self.maxspeed, self.vl), self.minspeed)        

class Graphics:
    # Definir constantes para colores
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)

    def __init__(self, dimensiones, robot_img_path, map_img_path):
        pygame.init()
        self.width, self.height = dimensiones
        self.sensor_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.robot = pygame.image.load(robot_img_path)
        self.map_img = pygame.image.load(map_img_path)

        pygame.display.set_caption("Evitación de Obstáculos")
        self.map = pygame.display.set_mode((self.width, self.height))
        self.map.blit(self.map_img, (0, 0))

    def rastro(self):
        if Robot.traveled_position:
            for x,y in Robot.traveled_position:
                pygame.draw.circle(self.map, Graphics.GREEN, (x, y), 38, 0)
            
    def draw_robot(self, x, y, heading):
      
        rotated = pygame.transform.rotozoom(self.robot, math.degrees(heading), 1)
        rect = rotated.get_rect(center=(x, y))
        self.map.blit(rotated, rect)

        self.info_robot(heading*180/math.pi)

    def draw_sensor_data(self, point_cloud):
        #self.sensor_overlay.fill((0, 0, 0, 0))

        for point in point_cloud:
             pygame.draw.circle(self.map, Graphics.RED, [point[0], point[1]], 3, 0)  # Dibujar un círculo en el mapa (representa datos del sensor)

    def info_robot(self, heading):
        fuente = pygame.font.Font(None, 24)
        texto = fuente.render(f"Angulo ={heading:.2f}", True, Graphics.GREEN)
        rect_width = texto.get_width() + 20
        rect_height = texto.get_height() + 20
        rect = pygame.Rect(50, self.height - 50, rect_width, rect_height) # Crear un rectángulo en la posición deseada
        pygame.draw.rect(self.map , Graphics.WHITE, rect) # Dibujar el rectángulo en la pantalla
        pygame.draw.rect(self.map , Graphics.BLACK, rect, 2) # Dibujar el contorno del rectángulo
        self.map.blit(texto, (50 +10, self.height - 50+10)) # Dibujar el texto sobre el rectángulo
        
    def update(self):
        pygame.display.flip()
        

class Ultrasonic:
    def __init__(self, sensor_range, map_img):
        self.sensor_range = sensor_range
        self.map_width, self.map_height = pygame.display.get_surface().get_size()
        self.map = map_img

    def sense_obstacles(self, x, y, heading):
        obstacles = []
        a, b = x, y 
        start_angle = heading - self.sensor_range[1]
        finish_angle = heading + self.sensor_range[1]
        interpolation_steps = 100

        start_angle = heading - self.sensor_range[1]  # Ángulo de inicio del rango del sensor
        finish_angle = heading + self.sensor_range[1]  # Ángulo final del rango del sensor
        conta = 8
        for angle in np.linspace(start_angle, finish_angle, 7, True):
            conta -= 1
            sensor_offset = 45  # Distancia desde el centro al borde del robot

            # Calcula el punto de origen del sensor desplazado
            x1 = a + sensor_offset * math.cos(angle)
            y1 = b - sensor_offset * math.sin(angle)
            
            x2 = x1 + self.sensor_range[0] * math.cos(angle)  # Calcular coordenada x del punto final del sensor
            y2 = y1 - self.sensor_range[0] * math.sin(angle)  # Calcular coordenada y del punto final del sensor
            
            for i in range(interpolation_steps):
                u = i / (interpolation_steps - 1)
                x = int(x2 * u + x1 * (1 - u))
                y = int(y2 * u + y1 * (1 - u))

                if 0 < x < self.map_width and 0 < y < self.map_height:
                    color = self.map.get_at((x, y))
                    self.map.set_at((x, y), (0, 208, 255))

                    if color == Graphics.BLACK:
                        obstacles.append([x, y, conta])
                        break
            else:
                obstacles.append([x, y, conta])
        return obstacles
