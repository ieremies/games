#!/usr/bin/env python3
import pygame
import random
from utils.base import Base, Sound
from utils.score import Score
from utils.life import Lifebar

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 1244
SCREEN_HEIGHT = 700
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
    gravity = 0.25
    speed = -5

    def __init__(self, y):
        self.size = [80, 80]  # (largura, altura) do obstáculo
        self.pos = [
            SCREEN_WIDTH + random.randint(10, 300),
            y,
        ]  # (x, y) da posição do obstáculo

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/prova a+.jfif").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = [self.speed, -5]

        self.offset_jump = random.randint(-2, 2)
        if y / SCREEN_HEIGHT > 0.6:
            self.offset_jump = random.randint(0, 2)
        elif y / SCREEN_HEIGHT < 0.4:
            self.offset_jump = random.randint(-2, 0)

        self.offset_speed = random.randint(-2, 2)

    def move(self):
        self.pos[0] += self.vel[0] + self.offset_speed
        self.pos[1] += self.vel[1]
        self.vel[1] += self.gravity

        if self.vel[1] > 5 - self.offset_jump:
            self.vel[1] = -5

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


class Bullet(Base):
    def __init__(self, x, y):
        self.size = [200, 20]  # (largura, altura) do tiro
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


def reset():
    global player, obstacles, bullets, score, lifebar, cooldown
    player = Player()
    obstacles = []
    bullets = []
    score.value = 0
    life.value = 5
    cooldown = 0


player = Player()
obstacles: list[Obstacle] = []
bullets: list[Bullet] = []
life = Lifebar(start_value=5, max_value=5, icon=None)
score = Score(icon="img/prova a+.jfif")
cooldown = 0

bg = pygame.image.load("img/patioelite.jpg").convert_alpha()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
explosion = Sound("snd/verde.mp3")
oof = Sound("snd/oof.mp3")

while True:
    screen.blit(bg, (0, 0))
    current_time = pygame.time.get_ticks()

    # Término do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            reset()

    if life.value <= 0:
        obstacles = []

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

    Obstacle.frequency += Obstacle.speed / -30
    print(Obstacle.speed)
    if life.value > 0 and random.randint(0, 1000) < Obstacle.frequency:
        for i in range(int(-Obstacle.speed // 3)):
            obstacles.append(Obstacle(random.randint(0, SCREEN_HEIGHT - 60)))
        Obstacle.frequency = 0
        Obstacle.speed -= 0.15

    # Atualizar posição dos obstáculos
    for obstacle in obstacles:
        obstacle.update(screen)
    obstacles = [obstacle for obstacle in obstacles if obstacle.pos[1] < SCREEN_HEIGHT]

    # Verificar colisões jogador-obstáculo
    for obstacle in obstacles:  # para cada obstáculo
        if player.collides_with(obstacle):  # se colidiu
            print("Colidiu com o Flappy Bird")
            life.value -= 1
            oof.play()
            obstacles.remove(obstacle)

    # Verificar colisões tiro-bird
    for bullet in bullets:
        for obstacle in obstacles:
            if bullet.collides_with(obstacle):
                print("Flappy destruído!")
                score.value += 1
                explosion.play()
                obstacles.remove(obstacle)
                bullets.remove(bullet)
                break

    score.draw(screen)
    life.draw(screen)

    # Atualiza o jogador
    player.update(screen)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(60)
