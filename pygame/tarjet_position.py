import pygame
import sys
import math
import time

# Inicializar Pygame
pygame.init()

# Definir la escala
metros_por_pixel = 1 / 300

# Dimensiones de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simulación con Pygame")

# Frecuencia de actualización de la simulación (FPS)
FPS = 60
clock = pygame.time.Clock()

# Función para convertir coordenadas del mundo real a coordenadas en la simulación
def metros_a_pixeles(metros):
    return int(metros / metros_por_pixel)

# Función para convertir velocidad del mundo real a velocidad en la simulación
def mps_a_pps(velocidad_mps):
    return velocidad_mps / metros_por_pixel

# Punto de inicio y punto final en el mundo real (metros)
punto_inicio_x = 0.0
punto_inicio_y = 0.0
punto_final_x = 0.5
punto_final_y = 0.5

# Convertir coordenadas a la simulación (pixeles)
punto_inicio_simulacion_x = metros_a_pixeles(punto_inicio_x)
punto_inicio_simulacion_y = metros_a_pixeles(punto_inicio_y)
punto_final_simulacion_x = metros_a_pixeles(punto_final_x)
punto_final_simulacion_y = metros_a_pixeles(punto_final_y)

# Calcular distancia entre el punto de inicio y el punto final
distancia_x = punto_final_simulacion_x - punto_inicio_simulacion_x
distancia_y = punto_final_simulacion_y - punto_inicio_simulacion_y
distancia_total_pixeles = math.sqrt(distancia_x**2 + distancia_y**2)

# Coordenadas actuales del círculo en la simulación (pixeles)
coordenada_simulacion_x = punto_inicio_simulacion_x
coordenada_simulacion_y = punto_inicio_simulacion_y

# Velocidad en la simulación (pixeles por segundo)
velocidad_simulacion = mps_a_pps(0.1)  # Por ejemplo, 1 metro por segundo

# Calcular el tiempo requerido para llegar al objetivo
tiempo_requerido_segundos = distancia_total_pixeles / velocidad_simulacion

# Contador de tiempo en segundos
tiempo_transcurrido_segundos = 0

# Variables para el texto de llegada al destino
llegada_destino = False
# Definir la fuente para el texto de llegada al destino
font_llegada = pygame.font.Font(None, 36)

tiempo= 0
desplazamiento_simulacion_total = 0
desplazamiento_metros_total = 0
coordenada_simulacion_x= 0
coordenada_simulacion_y= 0
angulo_radianes = math.radians(45)  # Convertimos 45 grados a radianes

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))
    # Lógica de la simulación aquí

    if not llegada_destino:
        # Calcular el tiempo transcurrido desde la última iteración en segundos
        tiempo_transcurrido_segundos = clock.tick(60) / 1000.0
        tiempo += tiempo_transcurrido_segundos
        desplazamiento_simulacion = velocidad_simulacion * tiempo_transcurrido_segundos 

        # Actualizar la variable tiempo_anterior_milisegundos para la siguiente iteración
        tiempo_anterior_milisegundos = tiempo_transcurrido_segundos

        # Actualizar las coordenadas de la simulación
        if desplazamiento_simulacion_total < distancia_total_pixeles:
            coordenada_simulacion_x += desplazamiento_simulacion * math.sin(angulo_radianes)
            coordenada_simulacion_y += desplazamiento_simulacion * math.cos(angulo_radianes)
            desplazamiento_simulacion_total += desplazamiento_simulacion
        else:
            coordenada_simulacion_x = punto_final_simulacion_x
            coordenada_simulacion_y = punto_final_simulacion_y

            # Mostrar texto de llegada al destino
            llegada_destino = True

    # Dibujar el punto de inicio y el punto final
    pygame.draw.circle(screen, (0, 255, 0), (punto_inicio_simulacion_x, punto_inicio_simulacion_y), 5)
    pygame.draw.circle(screen, (255, 0, 0), (punto_final_simulacion_x, punto_final_simulacion_y), 5)

    # Dibujar el círculo en la simulación usando las coordenadas convertidas
    if llegada_destino:
        pygame.draw.circle(screen, (255, 255, 255), (int(punto_final_simulacion_x), int(punto_final_simulacion_y)), 10)
        
        # Mostrar texto de llegada al destino en el centro de la pantalla
        texto_llegada = font_llegada.render("¡Llegaste al destino!", True, (0, 255, 0))
        text_rect = texto_llegada.get_rect(center=(width//2, height//2))
        screen.blit(texto_llegada, text_rect)

    else:
        pygame.draw.circle(screen, (255, 255, 255), (coordenada_simulacion_x, coordenada_simulacion_y), 10)

    # Mostrar el contador de tiempo en segundos en la esquina superior izquierda
    font = pygame.font.Font(None, 20)
    tiempo_texto = font.render(f"Tiempo: {round(tiempo, 3)} segundos", True, (255, 255, 255))
    screen.blit(tiempo_texto, (10, 10))

    # Mostrar la distancia total a recorrer en metros 
    distancia_texto = font.render(f"Distancia: {round(distancia_total_pixeles * metros_por_pixel, 3)} metros", True, (255, 255, 255))
    screen.blit(distancia_texto, (300, 10))

    # Mostrar el tiempo requerido para llegar al objetivo en la esquina superior derecha
    tiempo_requerido_texto = font.render(f"Tiempo requerido: {round(tiempo_requerido_segundos, 2)} segundos", True, (255, 255, 255))
    screen.blit(tiempo_requerido_texto, (width - tiempo_requerido_texto.get_width() - 10, 10))

    # Mostrar la distancia recorrida en metros 
    distancia_texto = font.render(f"Distancia: {round(desplazamiento_simulacion_total * metros_por_pixel, 3)} metros", True, (255, 255, 255))
    screen.blit(distancia_texto, (400, 400))

    # Actualizar pantalla
    pygame.display.flip()

