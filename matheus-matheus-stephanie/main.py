#!/usr/bin/env python3
import pygame
import random
from utils.base import Base, Sound

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Matheus^2 e Stephanie")


# Classes
class Player(Base):
    gravity = 0.5

    def __init__(self):
        self.pos = [100.0, 400.0]  # (x, y) da posição do jogador
        self.size = [85, 85]  # (largura, altura) do jogador

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/elitecol.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.impulso = 0

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE]:
            self.impulso = -10

        self.impulso += self.gravity
        self.pos[1] += self.impulso

        if self.pos[1] > SCREEN_HEIGHT - self.size[1]:
            self.pos[1] = SCREEN_HEIGHT - self.size[1]
            self.impulso = 0

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.impulso = 0

    def update(self, display):
        self.move()  # processa o input
        display.blit(self.image, self.pos)


class Obstacle(Base):
    frequency = 1500  # Novo obstáculo a cada 1.5 segundos

    def __init__(self, y):
        self.size = [80, 80]  # (largura, altura) do obstáculo
        self.pos = [SCREEN_WIDTH, y]  # (x, y) da posição do obstáculo

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/prova a+.jfif").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = [-5, 0]

    def move(self):
        self.pos[0] += self.vel[0]

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


class Bullet(Base):
    def __init__(self, x, y):
        self.size = [100, 100]  # (largura, altura) do tiro
        self.pos = [
            x - self.size[0] // 2,
            y - self.size[1] // 2,
        ]  # (x, y) da posição do tiro centrado no jogador

        self.image = pygame.image.load("img/caneta.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = (15, 0)

    def move(self):
        self.pos[0] += self.vel[0]

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


player = Player()
last_obstacle = pygame.time.get_ticks()
obstacles: list[Obstacle] = []
bullets: list[Bullet] = []
clock = pygame.time.Clock()
explosion = Sound("snd/verde.mp3")
cooldown = 0

bg = pygame.image.load("img/patioelite.jpg").convert_alpha()
bg= pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))


while True:
    screen.blit(bg, (0,0))
    current_time = pygame.time.get_ticks()

    # Término do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    # Tiro
    keys = pygame.key.get_pressed()
    cooldown -= 1
    if keys[pygame.K_RETURN] and cooldown <= 0:
        bullets.append(Bullet(player.x + player.width, player.y + player.height // 2))
        cooldown = 30

    # Atualizar posição das balas
    for bullet in bullets:
        bullet.update(screen)
    bullets = [bullet for bullet in bullets if bullet.y < SCREEN_HEIGHT]

    # Gerar novos obstáculos
    if current_time - last_obstacle > Obstacle.frequency:
        obstacles.append(Obstacle(random.randint(0, SCREEN_HEIGHT - 60)))
        last_obstacle = current_time
        Obstacle.frequency# Aumenta a frequência de obstáculos

    # Atualizar posição dos obstáculos
    for obstacle in obstacles:
        obstacle.update(screen)
    obstacles = [obstacle for obstacle in obstacles if obstacle.pos[1] < SCREEN_HEIGHT]

    # Verificar colisões jogador-obstáculo
    for obstacle in obstacles:  # para cada obstáculo
        if player.collides_with(obstacle):  # se colidiu
            print("Colidiu com o Flappy Bird")

    # Verificar colisões tiro-bird
    for bullet in bullets:
        for obstacle in obstacles:
            if bullet.collides_with(obstacle):
                print("Flappy destruído!")
                explosion.play()
                obstacles.remove(obstacle)
                bullets.remove(bullet)
                break

    # Atualiza o jogador
    player.update(screen)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)
