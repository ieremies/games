#!/usr/bin/env python3
"""
Jogo de pular para cima infinitamente.

Pegar estrelinhas faz você voar pra cima muito rápido por X tempo.
"""
import pygame
import random
from utils.base import Base, Sound

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Claudia, Laura e Marina")


# Classes
class Player(Base):
    gravity = 0.25
    friction = 0.9
    jump = -10

    def __init__(self):
        self.pos = [250.0, 700.0]  # (x, y) da posição do jogador
        self.size = [60, 60]  # (largura, altura) do jogador

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/caramelu.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.impulso = [0.0, 0.0]
        self.vel = 5

    def move(self):
        keys = pygame.key.get_pressed()

        # comandos do usuário
        if keys[pygame.K_LEFT]:
            self.impulso[0] = -self.vel
        if keys[pygame.K_RIGHT]:
            self.impulso[0] = self.vel

        # ação da gravidade
        self.impulso[1] += self.gravity

        # movimento
        self.pos[0] += self.impulso[0]
        self.pos[1] += self.impulso[1]

        # limites da tela
        if self.x < 0:
            self.x = 0
            self.impulso[0] = 0
        if self.x > SCREEN_WIDTH - self.size[0]:
            self.x = SCREEN_WIDTH - self.size[0]
            self.impulso[0] = 0

        # diminui a velocidade
        self.impulso[0] *= self.friction

    def update(self, display, platform):
        self.move()  # processa o input

        for platform in platforms:
            if self.impulso[1] >= 0 and self.collides_with(platform):
                if platform.special:
                    self.impulso[1] = 3 * self.jump
                    mola.play()
                else:
                    self.impulso[1] = self.jump
                    jump.play()

        display.blit(self.image, self.pos)


class Platform(Base):
    image = pygame.image.load("img/blocodegrama.jpg").convert_alpha()

    def __init__(self, x=200, y=-20, special=False):
        self.size = [100, 20]  # (largura, altura) da plataforma
        self.pos = [x, y]  # (x, y) da posição da plataforma
        self.special = special

        # Carrega e redimensiona a imagem
        if not special:
            self.image = pygame.image.load("img/blocodegrama.jpg").convert_alpha()
        if special:
            self.image = pygame.image.load("img/slime.png").convert_alpha()

        self.image = pygame.transform.scale(self.image, self.size)

    def move(self, scroll_offset):
        self.pos[1] += scroll_offset

    def update(self, display):
        display.blit(self.image, self.pos)


# Função para gerar novas plataformas aleatórias
def generate_platforms(last_platform):
    # Espaço mínimo entre plataformas
    if last_platform.rect.bottom < 125:
        return
    platforms.append(
        Platform(random.randint(0, SCREEN_WIDTH - 100), special=random.random() < 0.15)
    )


bg = pygame.image.load("img/fundoqaschelerfez.png").convert_alpha()


def reset():
    global player, platforms, y, won
    player = Player()
    platforms = [Platform(x=random.randint(1, 4) * 100, y=i * 100) for i in range(8)]
    platforms.append(Platform(x=200, y=800))
    Player.gravity = 0.25
    won = False
    y = -bg.get_height() + SCREEN_HEIGHT


# Inicialização
player = Player()
platforms = [Platform(x=random.randint(1, 4) * 100, y=i * 100) for i in range(8)]
platforms.append(Platform(x=200, y=800))
y = -bg.get_height() + SCREEN_HEIGHT
clock = pygame.time.Clock()
won = False
jump = Sound("snd/jump.mp3")
win = Sound("snd/win.mp3")
mola = Sound("snd/mola.mp3")


while True:
    screen.fill((0, 50, 100))
    screen.blit(bg, (0, y))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    player.update(screen, platforms)

    if y >= -50:  # you win
        if not won:
            win.play()
            won = True
        Player.gravity = 0

    # Deslocamento (scrolling)
    scroll_offset = (SCREEN_HEIGHT / 2) - player.y
    if y < -50 and scroll_offset > 0:
        player.y += scroll_offset + 1

        # Mover todas as plataformas para baixo, simulando scroll
        for platform in platforms:
            platform.move(scroll_offset)
        y = y + scroll_offset * 0.1
        Player.gravity = -y * 0.25 / bg.get_height() + 0.10
        print(Player.gravity)

        # Gerar novas plataformas
        generate_platforms(platforms[-1])

    # Desenhar todas as plataformas
    for platform in platforms:
        platform.update(screen)

    if player.y > SCREEN_HEIGHT + 100 or player.y < -500:
        reset()

    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros
    clock.tick(60)
