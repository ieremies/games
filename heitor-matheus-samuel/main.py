#!/usr/bin/env python3

"""
Fruit ninja de materiais escolares usando o mouse.
"""
import pygame
import math
import random
from collections import deque
from utils.base import Sound

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Heitor Matheus e Samuel")


class Fruit:
    frequency = 5000  # New fruit every 1 second
    gravity = 0.75

    def __init__(self):
        self.pos = [random.randint(0, SCREEN_WIDTH), 600.0]
        self.size = [200.0, 200.0]

        # Carrega e redimensiona a image
        self.image = pygame.image.load("img/estojo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        vel_x = (SCREEN_WIDTH / 2 - self.pos[0]     ) / 40
        vel_y = random.uniform(-40, -32.0)
        self.vel = [vel_x, vel_y]

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        self.vel[1] += self.gravity

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Variables for slash detection
mouse_positions = deque(maxlen=10)  # Track last 10 mouse positions
min_speed_for_slash = 10  # Threshold for considering motion as a slash

# Variáveis auxiliares
frutas = []
last_fruit_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
slash = Sound("snd/slash.mp3")

while True:
    background_image = pygame.image.load("img/Fundo1.png")
    screen.blit(background_image, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    # Update and draw fruits
    current_time = pygame.time.get_ticks()
    if current_time - last_fruit_time > Fruit.frequency:
        for _ in range(random.randint(1, 3)):
            frutas.append(Fruit())
        last_fruit_time = current_time
        Fruit.frequency = random.randint(500, 1500)
    for fruta in frutas:
        fruta.update(screen)

    # Get mouse position and add to deque
    mouse_positions.append(pygame.mouse.get_pos())

    # Draw mouse trail
    for i in range(1, len(mouse_positions)):
        pygame.draw.line(screen, BLACK, mouse_positions[i - 1], mouse_positions[i], 2)

    # Calculate speed and direction
    if len(mouse_positions) > 1:
        dx = mouse_positions[-1][0] - mouse_positions[-2][0]
        dy = mouse_positions[-1][1] - mouse_positions[-2][1]
        distance = math.hypot(dx, dy)  # Euclidean distance between two points

        if distance > min_speed_for_slash:
            # Detect slashing motion based on speed
            pygame.draw.circle(
                screen, (255, 0, 0), mouse_positions[-1], 20
            )  # Visual feedback for slash
            print("Slashing motion detected!")

            # Go through all fruits and check if they were slashed
            for fruta in frutas:
                if (
                    fruta.pos[0] < mouse_positions[-1][0] < fruta.pos[0] + fruta.size[0]
                    and fruta.pos[1]
                    < mouse_positions[-1][1]
                    < fruta.pos[1] + fruta.size[1]
                ):
                    print("Fruit slashed!")
                    slash.play()
                    frutas.remove(fruta)

    # Update display
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
