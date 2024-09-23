#!/usr/bin/env python3
import pygame
import random
from utils.base import Base, Sound

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beatrice e Luisa")


# Classes
class Player(Base):
    def __init__(self):
        self.pos = [270, 670]  # (x, y) da posição do jogador
        self.size = [60, 120]  # (largura, altura) do jogador

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = (10, 0)

    def move(self, lanes):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.pos[0] > lanes[0]:
            self.pos[0] -= self.vel[0]
        if keys[pygame.K_RIGHT] and self.pos[0] < lanes[-1]:
            self.pos[0] += self.vel[0]

    def update(self, display, lanes):
        self.move(lanes)  # processa o input
        display.blit(self.image, self.pos)


class Obstacle(Base):
    frequency = 1500  # Novo obstáculo a cada 1.5 segundos

    def __init__(self, x, obstacle_type):
        self.size = [60, 60]  # (largura, altura) do obstáculo
        self.pos = [x, -self.size[1]]  # (x, y) da posição do obstáculo

        # Carrega e redimensiona a imagem
        self.type = obstacle_type
        if obstacle_type == "test":
            self.image = pygame.image.load("img/test.png").convert_alpha()
        else:  # 'chair'
            self.image = pygame.image.load("img/chair.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = (0, 5)

    def move(self):
        self.pos[1] += self.vel[1]

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


class Bullet(Base):
    def __init__(self, x, y):
        self.size = [10, 20]  # (largura, altura) do tiro
        self.pos = [
            x - self.size[0] // 2,
            y - self.size[1] // 2,
        ]  # (x, y) da posição do tiro centrado no jogador

        self.image = pygame.image.load("img/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = (0, -15)

    def move(self):
        self.pos[1] += self.vel[1]

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


# Variáveis auxiliáres
FAIXAS = [100, 250, 400]  # Três faixas
last_obstacle = pygame.time.get_ticks()
obstacles: list[Obstacle] = []
bullets: list[Bullet] = []
clock = pygame.time.Clock()
player = Player()
explosion = Sound("snd/explosion.wav")

while True:
    screen.fill((0, 100, 0))  # Fundo verde
    current_time = pygame.time.get_ticks()

    # Término do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    # Tiro
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bullets.append(Bullet(player.x + player.width // 2, player.y))

    # Atualizar posição das balas
    for bullet in bullets:
        bullet.update(screen)
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Gerar novos obstáculos
    if current_time - last_obstacle > Obstacle.frequency:
        lane = random.choice(FAIXAS)  # onde o obstáculo vai aparecer
        type = random.choice(["test", "chair"])  # qual o tipo do obstáculo
        obstacles.append(Obstacle(lane, type))
        last_obstacle = current_time
        Obstacle.frequency -= 10  # Aumenta a frequência de obstáculos

    # Atualizar posição dos obstáculos
    for obstacle in obstacles:
        obstacle.update(screen)
    obstacles = [obstacle for obstacle in obstacles if obstacle.pos[1] < SCREEN_HEIGHT]

    # Verificar colisões jogador-obstáculo
    for obstacle in obstacles:  # para cada obstáculo
        if player.collides_with(obstacle):  # se colidiu
            if obstacle.type == "chair":
                print("Colidiu com uma cadeira!")
            elif obstacle.type == "test":
                print("Colidiu com um teste!")

    # Verificar colisões tiro-teste
    for bullet in bullets:
        for obstacle in obstacles:
            if obstacle.type == "test" and bullet.collides_with(obstacle):
                print("Teste destruído!")
                explosion.play()
                obstacles.remove(obstacle)
                bullets.remove(bullet)  # Remove o tiro
                break

    # Atualiza o jogador
    player.update(screen, FAIXAS)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)
