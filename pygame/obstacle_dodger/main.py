import math
import pygame
from ROBOT import Graphics, Robot, Ultrasonic  # Importar las clases y funciones del módulo ROBOT

# Definir las dimensiones del mapa
MAP_DIMENSIONS = (1300, 700)

# Crear una instancia de Graphics para manejar la representación gráfica del entorno
gfx = Graphics(MAP_DIMENSIONS, 'DDR.png', 'ObstacleMap.png')  # Rutas de las imágenes

# Configurar la posición inicial del robot y crear una instancia de la clase Robot
start = (300, 520)
robot = Robot(start, 0.01 * 3779.52)  # Posición inicial y ancho del robot

# Configurar el rango y el ángulo de visión del sensor ultrasónico, y crear una instancia de Ultrasonic
sensor_range = (350, math.radians(90))
ultra_sonic = Ultrasonic(sensor_range, gfx.map)  # Rango y referencia a la ventana gráfica

# Inicializar variables para medir el tiempo y la frecuencia de actualización
dt = 0
last_time = pygame.time.get_ticks()

running = True

# Bucle principal de simulación
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Cambiar running a False para salir del bucle si se cierra la ventana
    
    # Calcular el intervalo de tiempo dt desde la última actualización
    dt = (pygame.time.get_ticks() - last_time) / 1000
    last_time = pygame.time.get_ticks()

    # Actualizar la imagen del mapa en la ventana gráfica
    gfx.map.blit(gfx.map_img, (0, 0))
    
    gfx.rastro()
    
    # Actualizar la cinemática del robot y dibujar su representación gráfica
    robot.kinematics(dt)
    gfx.draw_robot(robot.x, robot.y, robot.heading)  
    
    # Utilizar el sensor ultrasónico para detectar obstáculos y tomar decisiones de movimiento
    point_cloud = ultra_sonic.sense_obstacles(robot.x, robot.y, robot.heading)
    robot.avoid_obstacles(point_cloud, dt)
    gfx.draw_sensor_data(point_cloud)  # Dibujar datos del sensor en la ventana
    
    # Actualizar la pantalla con los cambios realizados
    gfx.update()

# Cerrar la ventana de pygame al finalizar la simulación
pygame.quit()
