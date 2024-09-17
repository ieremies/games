#!/usr/bin/env python3

"""
Pegar blusas caindo do céu e, conforme você pega camisas do elite, carrega uma barra que, quando carregada
você aperta espaço e grita, destruindo as outras blusas.
"""
import pygame
import random
from utils.base import Base, Sound

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Manuela e Pietro")
# Cores
elite = (255, 165, 0)
polie = (0, 255, 0)
player = (255, 165, 0)
oficina = (128, 0, 128)
PINK = (255, 192, 203)
RED = (255, 0, 0)


# Classes
class Player(Base):
    friction = 0.9

    def __init__(self, color):
        self.size = [60, 60]  # (largura, altura) do jogador
        self.pos = [500.0, SCREEN_HEIGHT - self.tam]  # (x, y) da posição do jogador

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.tam, self.tam))

        self.impulso = [0.0, 0.0]
        self.vel = 5

        self.color = color

    @property
    def tam(self):
        return self.size[0]

    @tam.setter
    def tam(self, value):
        self.size = [value, value]
        self.image = pygame.transform.scale(self.image, (self.tam, self.tam))

    def move(self):
        keys = pygame.key.get_pressed()

        # comandos do usuário
        if keys[pygame.K_LEFT]:
            self.impulso[0] = -self.vel
        if keys[pygame.K_RIGHT]:
            self.impulso[0] = self.vel

        # movimento
        self.pos[0] += self.impulso[0]
        self.pos[1] += self.impulso[1]

        # limites da tela
        if self.x < 0:
            self.x = 0
            self.impulso[0] = 0
        if self.x > SCREEN_WIDTH - self.tam:
            self.x = SCREEN_WIDTH - self.tam
            self.impulso[0] = 0

        # diminui a velocidade
        self.impulso[0] *= self.friction

    def update(self, display):
        self.move()  # processa o input
        display.blit(self.image, self.pos)

    def collides_with(self, obstacle):
        return self.rect.colliderect(obstacle.rect)


class Obstacle(Base):
    frequency = 1000  # Novo obstáculo a cada 1.5 segundos
    gravity = 0.15

    def __init__(self, x, color):
        self.size = [50, 50]  # (largura, altura) do obstáculo
        self.pos = [x, -self.size[1]]  # (x, y) da posição do obstáculo

        # Carrega e redimensiona a imagem
        if color == elite:
            self.image = pygame.image.load("img/elite.png")
            self.image = pygame.transform.scale(self.image, self.size)
        if color == polie:    
            self.image = pygame.image.load("img/polie.png")
            self.image = pygame.transform.scale(self.image, self.size)
        if color == oficina:
            self.image = pygame.image.load("img/oficina.jpg")
            self.image = pygame.transform.scale(self.image, self.size)
        
        self.vel = [0, 5.0]
        self.color = color
    def move(self):
        self.pos[1] += self.vel[1]
        self.vel[1] += self.gravity

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


player = Player(player)
obstacles = []
clock = pygame.time.Clock()
last_obstacle = pygame.time.get_ticks()
BLUSAS = [elite, oficina, polie]

while True:
    print("do balaco baco")
    screen.fill((135, 206, 235))  # fundo azul claro
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    player.update(screen)

    if current_time - last_obstacle > Obstacle.frequency:
        obstacles.append(
            Obstacle(random.randint(0, SCREEN_WIDTH - 60), random.choice(BLUSAS))
        )
        last_obstacle = current_time
        Obstacle.frequency = random.randint(500, 1500)

    for obstacle in obstacles:
        obstacle.update(screen)
    obstacles = [obstacle for obstacle in obstacles if obstacle.y < SCREEN_HEIGHT]

    for obstacle in obstacles:
        if player.collides_with(obstacle):
            obstacles.remove(obstacle)
            if player.color == obstacle.color:
                player.tam += 5
                player.y -= 5
            else:
                player.tam -= 5
                player.y += 5

    # Atualiza o jogador
    player.update(screen)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)
