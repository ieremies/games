#!/usr/bin/env python3
import pygame
import random
from utils.base import Base, Sound
from utils.life import Lifebar
from utils.score import Score

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
        self.size = [100, 100]  # (largura, altura) do jogador

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
    base_speed = [0, 5]

    def __init__(self, x, obstacle_type):
        self.size = [80, 80]  # (largura, altura) do obstáculo
        self.pos = [x, -self.size[1]]  # (x, y) da posição do obstáculo

        # Carrega e redimensiona a imagem
        self.type = obstacle_type
        if obstacle_type == "test":
            self.image = pygame.image.load("img/test.png").convert_alpha()
        else:  # 'chair'
            self.image = pygame.image.load("img/chair.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = self.base_speed

    def move(self):
        self.pos[1] += self.vel[1]

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


class Bullet(Base):
    def __init__(self, x, y):
        self.size = [40, 40]  # (largura, altura) do tiro
        self.pos = [
            x - self.size[0] // 2,
            y - self.size[1] // 2,
        ]  # (x, y) da posição do tiro centrado no jogador

        self.image = pygame.image.load("img/ervilha.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = (0, -15)

    def move(self):
        self.pos[1] += self.vel[1]

    def update(self, display):
        self.move()  # processa o movimento
        display.blit(self.image, self.pos)


def start_game():
    global last_obstacle, obstacles, bullets, player, life, score, cooldown, FPS
    last_obstacle = pygame.time.get_ticks()
    obstacles = []
    bullets = []
    player = Player()
    life = Lifebar(start_value=3, max_value=3, icon=None)
    score = Score(icon="img/dna.png")
    FPS = 60
    cooldown = 0


# Variáveis auxiliáres
FAIXAS = [100, 250, 400]  # Três faixas
last_obstacle = pygame.time.get_ticks()
obstacles = []
bullets = []
clock = pygame.time.Clock()
player = Player()
explosion = Sound("snd/explosion.wav")
explosion.sound.set_volume(0.1)
oof = Sound("snd/oof.mp3")
life = Lifebar(start_value=3, max_value=3, icon=None)
score = Score(icon="img/dna.png")
cooldown = 0
background = pygame.image.load("img/background.jpg").convert_alpha()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60

while True:
    screen.blit(background, (0, 0))  # Desenha a imagem de fundo
    current_time = pygame.time.get_ticks()

    # Término do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            start_game()

    # Tiro
    keys = pygame.key.get_pressed()
    cooldown -= 1
    if keys[pygame.K_SPACE]:
        if cooldown <= 0:
            bullets.append(Bullet(player.x + player.width // 2, player.y))
            cooldown = 60  # 1 segundo de cooldown

    # Atualizar posição das balas
    for bullet in bullets:
        bullet.update(screen)
    bullets = [bullet for bullet in bullets if bullet.y > 0]

    # Gerar novos obstáculos
    if life.value > 0 and current_time - last_obstacle > Obstacle.frequency:
        lane = random.randint(100, 400)  # onde o obstáculo vai aparecer
        type = random.choice(["test", "chair"])  # qual o tipo do obstáculo
        obstacles.append(Obstacle(lane, type))
        last_obstacle = current_time
        FPS += 2
        # Obstacle.frequency -= 10  # Aumenta a frequência de obstáculos
        # Obstacle.base_speed[1] = Obstacle.base_speed[1] + 0.15

    # Atualizar posição dos obstáculos
    for obstacle in obstacles:
        obstacle.update(screen)
    obstacles = [obstacle for obstacle in obstacles if obstacle.pos[1] < SCREEN_HEIGHT]

    # Verificar colisões jogador-obstáculo
    for obstacle in obstacles:  # para cada obstáculo
        if player.collides_with(obstacle):  # se colidiu
            oof.play()
            life.value -= 1
            obstacles.remove(obstacle)

    # Verificar colisões tiro-teste
    for bullet in bullets:
        for obstacle in obstacles:
            if obstacle.type == "test" and bullet.collides_with(obstacle):
                print("Teste destruído!")
                score.value += 1
                explosion.play()
                obstacles.remove(obstacle)
                bullets.remove(bullet)  # Remove o tiro
                break

    life.draw(screen)
    score.draw(screen)

    # Atualiza o jogador
    player.update(screen, FAIXAS)

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(FPS)
