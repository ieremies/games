#!/usr/bin/env python3


"""
O destruidor de bloquinhos usando a bolinha.

Os blocos são livros e a barra embaixo é uma régua.

"""

import pygame
import random
from utils.base import Base, Sound

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moriyyaa")


# Classes
class Player(Base):
    def __init__(self, x, y):
        self.size = [100, 20]  # (largura, altura) do bloco
        self.pos = [x, y]  # (x, y) da posição do bloco

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/tuler.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = [5, 0]

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.pos[0] -= self.vel[0]
        if keys[pygame.K_RIGHT]:
            self.pos[0] += self.vel[0]

        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > SCREEN_WIDTH - self.size[0]:
            self.pos[0] = SCREEN_WIDTH - self.size[0]

    def update(self, display):
        self.move()
        display.blit(self.image, self.pos)


class Block(Base):
    def __init__(self, x, y, vida, powerup=False):
        self.size = [40, 25]  # (largura, altura) do bloco
        self.pos = [x, y]  # (x, y) da posição do bloco

        # Carrega e redimensiona a imagem
        self.image1 = pygame.image.load("img/book1.png").convert_alpha()
        self.image1 = pygame.transform.scale(self.image1, self.size)
        self.image2 = pygame.image.load("img/book2.png").convert_alpha()
        self.image2 = pygame.transform.scale(self.image2, self.size)
        self.image3 = pygame.image.load("img/book3.png").convert_alpha()
        self.image3 = pygame.transform.scale(self.image3, self.size)

        self.vida = vida
        self.powerup = powerup

        if powerup:
            self.glow = pygame.image.load("img/glow.png").convert_alpha()
            self.glow = pygame.transform.scale(self.glow, self.size)
            self.image1.blit(self.glow, (0, 0))
            self.image2.blit(self.glow, (0, 0))
            self.image3.blit(self.glow, (0, 0))

    def update(self, display):
        if self.vida == 1:
            display.blit(self.image1, self.pos)
        if self.vida == 2:
            display.blit(self.image2, self.pos)
        if self.vida == 3:
            display.blit(self.image3, self.pos)


class Ball(Base):
    def __init__(self, x, y):
        self.size = [20, 20]  # (largura, altura) da bola
        self.pos = [x, y]  # (x, y) da posição da bola

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/ball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = [4, -4]

    def move(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        if self.pos[0] < 0 or self.pos[0] > SCREEN_WIDTH - self.size[0]:
            self.vel[0] *= -1
            self.pos[0] += self.vel[0]
        if self.pos[1] < 0:
            self.vel[1] *= -1
            self.pos[1] += self.vel[1]

    def update(self, display):
        self.move()
        display.blit(self.image, self.pos)

    def collides_with(self, other):
        """
        Return None se não há colisão.
        Return "Vertical" se houve colisão vertical.
        Return "Horizontal" se houve colisão horizontal.
        """
        if self.rect.colliderect(other.rect):
            x = self.rect.center[0] - other.rect.center[0]
            y = self.rect.center[1] - other.rect.center[1]

            if abs(x) > abs(y):
                return "Vertical"
            else:
                return "Horizontal"

        return None


class PowerUp(Base):
    def __init__(self, x, y):
        self.size = [20, 20]  # (largura, altura) do bloco
        self.pos = [x, y]  # (x, y) da posição do bloco

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/power.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = [0, 3]

    def move(self):
        self.pos[1] += self.vel[1]

    def update(self, display):
        self.move()
        display.blit(self.image, self.pos)


balls = [Ball(300, 400)]
player = Player(250, 550)
power_ups = []
blocks = [
    Block(x, y, random.randint(1, 3))
    for x in range(0, SCREEN_WIDTH, 40)
    for y in range(0, 200, 20)
]
clock = pygame.time.Clock()
power_up_sound = Sound("snd/power_up.mp3")
block_break_sound = Sound("snd/block_break.mp3")
boing_sound = Sound("snd/boing.mp3")

image = pygame.image.load("img/image.webp").convert_alpha()
image = pygame.transform.scale(image, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 320))

while True:
    screen.fill((251, 251, 248))
    screen.blit(image, (50, 270))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    player.update(screen)

    for block in blocks:
        block.update(screen)

    for power_up in power_ups:
        power_up.update(screen)

        if power_up.collides_with(player):
            power_ups.remove(power_up)
            power_up_sound.play()
            balls.append(Ball(player.x + 20, player.y - 20))

    for ball in balls:
        ball.update(screen)

        # Check collision with player
        if ball.collides_with(player):
            ball.vel[1] = -ball.vel[1]
            alpha = (ball.x - player.x) / player.width
            ball.vel[0] = 10 * alpha - 5

        new_vel = ball.vel.copy()
        for block in blocks:
            c = ball.collides_with(block)
            if c:  # Se há colisão
                boing_sound.play()
                block.vida = block.vida - 1
                if block.vida == 0:
                    if block.powerup:
                        power_ups.append(PowerUp(*block.pos))
                    blocks.remove(block)
                    block_break_sound.play()
            if c == "Vertical":
                new_vel[0] = -ball.vel[0]
            if c == "Horizontal":
                new_vel[1] = -ball.vel[1]
        ball.vel = new_vel

    pygame.display.flip()
    clock.tick(60)
