#!/usr/bin/env python3

import pygame
import random
from utils.base import Base, Sound
from utils.clock import Timer
from utils.colors import RED, GREEN
from images import load_images_from_folder, combine_npc_images

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Melhor Jogo da Turma")

heads = load_images_from_folder("img/heads")
body_correct = pygame.image.load("img/body_correct.png").convert_alpha()
body_wrong = pygame.image.load("img/body_wrong.png").convert_alpha()


# Classes
class Player(Base):
    def __init__(self):
        self.pos = [
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
        ]  # (x, y) da posição do jogador
        self.size = [50, 80]  # (largura, altura) do jogador

        # Carrega e redimensiona a imagem
        self.image = pygame.image.load("img/dir.webp").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.vel = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.pos[0] > 0:
            self.pos[0] -= self.vel
        if keys[pygame.K_RIGHT] and self.pos[0] < SCREEN_WIDTH - self.size[0]:
            self.pos[0] += self.vel
        if keys[pygame.K_UP] and self.pos[1] > 0:
            self.pos[1] -= self.vel
        if keys[pygame.K_DOWN] and self.pos[1] < SCREEN_HEIGHT - self.size[1]:
            self.pos[1] += self.vel

    def update(self, display):
        self.move()  # processa o input
        display.blit(self.image, self.pos)


class Students(Base):
    def __init__(self, x, y):
        self.pos = [x, y]  # (x, y) da posição do aluno
        self.size = [40, 40]  # (largura, altura) do jogador

        # Carrega e redimensiona a imagem
        head = random.choice(heads)
        self.image_right = combine_npc_images(head, body_correct)
        self.image_right = pygame.transform.scale(self.image_right, self.size)

        self.image_wrong = combine_npc_images(head, body_wrong)
        self.image_wrong = pygame.transform.scale(self.image_wrong, self.size)

        self.correct = random.choice([True, False])

        self.change = [0.0, 0.0]
        self.vel = 1

    def change_uniform(self):
        if not self.correct:
            aaa.play()
        self.correct = True

    def move(self, player):
        if self.change == [0.0, 0.0]:
            self.change = [random.randint(-10, 10), random.randint(-10, 10)]

        if self.change[0] > 0:
            self.pos[0] += self.vel
            self.change[0] -= self.vel
        elif self.change[0] < 0:
            self.pos[0] -= self.vel
            self.change[0] += self.vel

        if self.change[1] > 0:
            self.pos[1] += self.vel
            self.change[1] -= self.vel
        elif self.change[1] < 0:
            self.pos[1] -= self.vel
            self.change[1] += self.vel

        if self.pos[0] < 0:
            self.pos[0] = 0
        if self.pos[0] > SCREEN_WIDTH - self.size[0]:
            self.pos[0] = SCREEN_WIDTH - self.size[0]
        if self.pos[1] < 0:
            self.pos[1] = 0
        if self.pos[1] > SCREEN_HEIGHT - self.size[1]:
            self.pos[1] = SCREEN_HEIGHT - self.size[1]

    def update(self, display, player):
        self.move(player)  # processa o input
        if self.correct:
            display.blit(self.image_right, self.pos)
        else:
            display.blit(self.image_wrong, self.pos)


def start_game():
    global player, students, clock
    player = Player()
    students = [
        Students(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
        for _ in range(100)
    ]
    clock = Timer(time)


def lose_screen():
    text = font.render("Você não foi contratada", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))


def win_screen():
    text = font.render("Você foi contratada!", True, GREEN)
    screen.blit(text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100))


def check_students():
    for student in students:
        if not student.correct:
            return False
    return True


player = Player()
students = [
    Students(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    for _ in range(100)
]
time = 25
clock = Timer(time)
font = pygame.font.SysFont(None, 50)
start_game()
aaa = Sound("snd/fart.mp3")

while True:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            start_game()

    if clock.value <= 0:
        lose_screen()

    if check_students():
        win_screen()
    else:
        player.update(screen)

        for student in students:
            student.update(screen, player)

            if student.collides_with(player):
                student.change_uniform()

        clock.draw(screen)

    pygame.display.flip()
    pygame.time.Clock().tick(60)
