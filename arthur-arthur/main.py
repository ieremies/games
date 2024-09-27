#!/usr/bin/env python3
import pygame
import random
from utils.base import Base, Sound
from utils.score import Score

# Inicializar o Pygame
pygame.init()

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Arthur^2")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


# Classe do jogador
class Player(Base):
    gravity = 1

    def __init__(self):
        self.pos = [50, SCREEN_HEIGHT - 50]
        self.size = [50, 50]
        self.change = [5, 0]
        self.vel = [5, 20]

        self.image = pygame.image.load("img/Quadrado.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

        self.on_ground = True

    def move(self):
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]:
        #     self.change[0] -= self.vel[0]
        # if keys[pygame.K_RIGHT]:
        #     self.change[0] += self.vel[0]
        if keys[pygame.K_SPACE] and self.on_ground:
            self.change[1] -= self.vel[1]
            self.on_ground = False

    def update(self, display, platforms):
        self.move()  # processar movimento
        self.change[1] += self.gravity  # aplicar gravidade

        # Movimentar o jogador na horizontal
        self.x += self.change[0]

        # # Checar colisões horizontais
        # for platform in platforms:  # para cada plataforma
        #     if self.collides_with(platform):  # se colidir com a plataforma
        #         if self.change[0] > 0:  # e estou indo para a direita
        #             self.x = platform.rect.left - self.width
        #         elif self.change[0] < 0:  # e estou indo para a esquerda
        #             self.x = platform.rect.right
        #         self.change[0] = 0

        # Movimentar verticalmente
        self.y += self.change[1]

        # Checar colisões verticais
        for platform in platforms:
            if self.collides_with(platform):
                if self.change[1] > 0:
                    self.y = platform.rect.top - self.size[1]
                    self.on_ground = True
                elif self.change[1] < 0:
                    self.y = platform.rect.bottom
                self.change[1] = 0

        # Impedir o jogador de sair da tela pela esquerda
        if self.pos[0] < 0:
            self.pos[0] = 0

        self.change[0] = 5

        display.blit(self.image, self.pos)


# Classe das plataformas
class Platform(Base):
    def __init__(self, width, height, x, y):
        self.pos = [x, y]
        self.size = [width, height]

        self.image = pygame.Surface((width, height))
        self.image.fill(GREEN)

    def move(self, scroll_offset):
        self.pos[0] -= scroll_offset

    def update(self, display):
        display.blit(self.image, self.pos)


class Trophy(Base):
    def __init__(self, width, height, x, y):
        self.pos = [x, y]
        self.size = [width, height]

        self.image = pygame.image.load("img/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, self.size)

    def move(self, scroll_offset):
        self.pos[0] -= scroll_offset

    def update(self, display):
        display.blit(self.image, self.pos)


# Função para gerar novas plataformas aleatórias
def generate_platforms(last_platform):

    # Se a última plataforma não estiver visível, não gerar novas
    if last_platform.rect.right > SCREEN_WIDTH:
        return

    width = random.randint(100, 200)
    height = 20
    x = SCREEN_WIDTH + random.randint(50, 150)  # espaço entre plataformas

    prop = min(last_platform.y / SCREEN_HEIGHT, 1)
    down = round(last_platform.y + 100 * (1 - prop))
    up = round(last_platform.y - 100 * prop)
    y = random.randint(up, down)

    platforms.append(Platform(width, height, x, y))

    if random.random() < 0.5:
        print("Trophy")
        trophies.append(Trophy(50, 50, SCREEN_WIDTH + width, y - 50))


# Inicialização


def reset():
    global player, platforms, trophies, FPS, score, last_score
    player = Player()
    platforms = [Platform(800, 40, 0, SCREEN_HEIGHT - 40)]
    FPS = 60
    last_score = score.value
    score = Score(icon="img/coin.png")
    trophies = []


player = Player()
platforms = [Platform(800, 40, 0, SCREEN_HEIGHT - 40)]
trophies = []
clock = pygame.time.Clock()
coin = Sound("snd/coin.mp3")
score = Score(icon="img/coin.png")
last_score = 0
FPS = 60

while True:
    screen.fill((0, 0, 156))  # fundo azul claro

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    player.update(screen, platforms)

    # Deslocamento (scrolling)
    scroll_offset = player.x - SCREEN_WIDTH / 2
    if scroll_offset > 0:
        player.x = SCREEN_WIDTH // 2 - 1

        # Mover todas as plataformas para a esquerda, simulando scroll
        for platform in platforms:
            platform.move(scroll_offset)
        for trophy in trophies:
            trophy.move(scroll_offset)

        # Gerar novas plataformas
        generate_platforms(platforms[-1])

    # Desenhar todos os sprites
    for platform in platforms:
        platform.update(screen)

    for trophy in trophies:
        trophy.update(screen)
        if player.collides_with(trophy):
            score.value += 1
            coin.play()
            trophies.remove(trophy)
            FPS += 5

    if player.y > SCREEN_HEIGHT + 100:
        reset()

    if last_score > 0:
        # Write on the topleft
        font = pygame.font.Font(None, 36)
        text = font.render(f"Último score: {last_score}", True, BLACK)
        screen.blit(text, (20, 20))

    score.draw(screen)
    # Atualizar a tela
    pygame.display.flip()

    # Controlar a taxa de quadros
    clock.tick(FPS)

    # Movimento contínuo para a direita (Ex: Geometry Dash)
    # Ao cair, voltar ao inicio
    # Link da imagem do personagem: https://www.reddit.com/r/notinteresting/comments/18kkvld/this_is_a_picture_of_the_geometry_dash_cube/?tl=pt-br&rdt=59585
    # Link da imagem da moeda para substituir o troféu: https://www.pngegg.com/en/png-cbbwy
    # Substituir o audio do cristiano ronaldo por uma coleta de moeda do tipo Super mario Bros
