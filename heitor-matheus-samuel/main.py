#!/usr/bin/env python3

"""
Fruit ninja de materiais escolares usando o mouse.
"""
import pygame
import math
import random
import time
from collections import deque
from utils.base import Sound
from utils.clock import Timer
from utils.life import Lifebar
from utils.score import Score

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Heitor Matheus e Samuel")

# Carrega a imagem de fundo (sala de aula)
background = pygame.image.load("img/sala_de_aula.jpg").convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
NOTE_GOOD_COLOR = (194, 187, 163)  # Cor C2BBA3 em RGB

# Frequência inicial das frutas
initial_frequency = 1000  # 1 segundo
frequency_decrement = 10  # A quantidade de redução na frequência por minuto jogado
min_frequency = 500  # Frequência mínima (0.5 segundos)


# Função para alterar a cor da imagem
def change_color(image, color):
    colored_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    colored_image.blit(image, (0, 0))
    colored_image.fill(color, special_flags=pygame.BLEND_MULT)
    return colored_image


# Função para verificar colisão entre duas áreas
def check_collision(pos1, size1, pos2, size2):
    return (
        pos1[0] < pos2[0] + size2[0]
        and pos1[0] + size1[0] > pos2[0]
        and pos1[1] < pos2[1] + size2[1]
        and pos1[1] + size1[1] > pos2[1]
    )


# Classe Fruit
class Fruit:
    gravity = 0.25

    def __init__(self, image_name):
        self.pos = [
            random.randint(0, SCREEN_WIDTH - 200),
            600.0,
        ]  # Ajusta a posição para evitar que saiam da tela
        self.size = [170.0, 170.0]

        # Carrega e redimensiona a imagem de acordo com o parâmetro `image_name`
        self.image_name = image_name
        self.image = pygame.image.load(f"img/{image_name}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        # Altera a cor da imagem se for "Nota Boa"
        if image_name == "Nota Boa":
            self.image = change_color(self.image, NOTE_GOOD_COLOR)

        # Divide a imagem em duas metades
        self.left_half = self.image.subsurface((0, 0, self.size[0] // 2, self.size[1]))
        self.right_half = self.image.subsurface(
            (self.size[0] // 2, 0, self.size[0] // 2, self.size[1])
        )

        self.is_cut = False  # Indica se a fruta foi cortada
        self.split_offset = 50  # Distância entre as duas metades após o corte

        vel_x = (SCREEN_WIDTH / 2 - self.pos[0] + random.randint(-200, 200)) / 40
        vel_y = random.uniform(-17.0, -13.0)
        self.vel = [vel_x, vel_y]

    def move(self):
        if not self.is_cut:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.vel[1] += self.gravity
        else:
            # Movimenta as duas metades em direções opostas após o corte
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
            self.vel[1] += self.gravity
            self.split_offset += 5  # Aumenta a distância entre as metades

    def update(self, display):
        self.move()  # Processa o movimento
        if not self.is_cut:
            display.blit(self.image, self.pos)
        else:
            # Desenha as duas metades da fruta cortada
            display.blit(self.left_half, (self.pos[0] - self.split_offset, self.pos[1]))
            display.blit(
                self.right_half, (self.pos[0] + self.split_offset, self.pos[1])
            )

    def cut(self):
        # Define que a fruta foi cortada
        self.is_cut = True
        self.vel = [self.vel[0], self.vel[1] + 1]  # Ajusta a velocidade após o corte


def reset():
    global life, lives, timer, score, frutas, start_time, game_over
    life = Lifebar(start_value=3, max_value=3, icon=None)
    lives = 3
    timer = Timer(20)
    score = Score(icon=None)
    frutas = []
    start_time = time.time()
    game_over = False


# Variáveis para o sistema de vidas
font = pygame.font.SysFont(None, 55)  # Fonte para exibir o Game Over
lives = 3


# Função para exibir texto na tela
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)


# Variables for slash detection
mouse_positions = deque(maxlen=10)  # Track last 10 mouse positions
min_speed_for_slash = 10  # Threshold for considering motion as a slash

# Variáveis auxiliares
frutas = []
last_fruit_time = pygame.time.get_ticks()
clock = pygame.time.Clock()
slash = Sound("snd/slash.mp3")

# Tempo de jogo
start_time = time.time()
game_over = False
running = True

timer = Timer(20)
life = Lifebar(start_value=3, max_value=3, icon=None)
score = Score(icon=None)

ruler = pygame.image.load(f"img/ruler.png").convert_alpha()
ruler = pygame.transform.scale(ruler, (80, 80))

while running:
    screen.blit(background, (0, 0))  # Desenha a imagem de fundo (sala de aula)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            reset()

    if lives <= 0 or timer.value <= 0:
        # Exibe tela de Game Over
        score.draw(screen)
        elapsed_time = elapsed_time
        draw_text(
            "Game Over", font, RED, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50
        )
        pygame.display.flip()
        continue  # Pausa o jogo

    # Atualiza o tempo de jogo
    elapsed_time = int(time.time() - start_time)

    # Atualiza e desenha frutas
    current_time = pygame.time.get_ticks()
    if current_time - last_fruit_time > initial_frequency and timer.value > 0:
        for _ in range(random.randint(1, 3)):
            # Escolhe aleatoriamente entre "Nota Boa", "Nota Ruim" e "Estojo"
            image_name = random.choices(
                ["Nota Ruim", "Nota Boa", "Estojo"], weights=[0.75, 0.15, 0.5], k=1
            )[0]
            frutas.append(Fruit(image_name))
        last_fruit_time = current_time
        # Reduz a frequência das frutas com o tempo
        frequency = max(
            min_frequency,
            initial_frequency - (elapsed_time // 60 * frequency_decrement),
        )  # Frequência mínima
        initial_frequency = frequency

    for fruta in frutas:
        fruta.update(screen)

    # Get mouse position and add to deque
    mouse_positions.append(pygame.mouse.get_pos())

    x = mouse_positions[-1][0] - 40
    y = mouse_positions[-1][1] - 40
    screen.blit(ruler, (x, y))

    # Draw mouse trail
    for i in range(1, len(mouse_positions)):
        pygame.draw.line(screen, WHITE, mouse_positions[i - 1], mouse_positions[i], 2)

    # Calculate speed and direction
    if len(mouse_positions) > 1:
        dx = mouse_positions[-1][0] - mouse_positions[-2][0]
        dy = mouse_positions[-1][1] - mouse_positions[-2][1]
        distance = math.hypot(dx, dy)  # Euclidean distance between two points

        if distance > min_speed_for_slash:
            # Detect slashing motion based on speed
            pygame.draw.circle(
                screen, (255, 0, 0), mouse_positions[-1], 5
            )  # Visual feedback for slash

            # Go through all fruits and check if they were slashed
            for fruta in frutas:
                if (
                    fruta.pos[0] < mouse_positions[-1][0] < fruta.pos[0] + fruta.size[0]
                    and fruta.pos[1]
                    < mouse_positions[-1][1]
                    < fruta.pos[1] + fruta.size[1]
                    and not fruta.is_cut
                ):
                    print("Fruit slashed!")
                    slash.play()

                    # Verifica se a fruta cortada é "Nota Boa"
                    if fruta.image_name == "Nota Boa":
                        life.value -= 1
                        lives -= 1  # Perde uma vida se for Nota Boa
                        print(f"Lives remaining: {lives}")
                    else:
                        score.value += 1

                    fruta.cut()  # Corta a fruta

    timer.draw(screen)
    life.draw(screen)
    score.draw(screen)
    # Update display
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
