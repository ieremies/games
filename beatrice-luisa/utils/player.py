#!/usr/bin/env python3

import pygame


class Player(pygame.sprite.Sprite):
    """
    Classe para criar um jogador.
    """

    def __init__(
        self, pos: tuple = (0, 0), icon: str = "img/player.png", size: int = 30
    ):
        """
        Inicializa o jogador.
        """
        super().__init__()
        self.image = pygame.image.load(icon)
        self.image = pygame.transform.scale(self.image, (size, size))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.speed = [0, 0]  # medido em pixels por segundo
        self.max_speed = 5  # módulo máximo da velocidade
        self.move_acceleration = (0, 3)  # aceleração causada pelo input de movimento
        self.friction = 0.9  # coeficiente de fricção

        self.forces = [(0, 1)]  # lista de forças de campo que atuam sobre o jogador

        self.input = [0, 0]  # acumula o input dado

    @property
    def pos(self):
        """
        Retorna a posição do jogador.
        """
        return self.rect.center

    @property
    def dir(self):
        """
        Retorna a direção do jogador.
        """
        dir = [0, 0]
        if self.speed[0] > 0:
            dir[0] = 1
        elif self.speed[0] < 0:
            dir[0] = -1
        if self.speed[1] > 0:
            dir[1] = 1
        elif self.speed[1] < 0:
            dir[1] = -1
        return tuple(dir)

    def clamp_pos(self):
        if self.limits_init is None or self.limits_end is None:
            return

        if self.rect.right >= self.limits_end[0]:
            self.rect.right = self.limits_end[0]
            self.speed[0] = 0
        if self.rect.left <= self.limits_init[0]:
            self.rect.left = self.limits_init[0]
            self.speed[0] = 0
        if self.rect.bottom >= self.limits_end[1]:
            self.rect.bottom = self.limits_end[1]
            self.speed[1] = 0
        if self.rect.top <= self.limits_init[1]:
            self.rect.top = self.limits_init[1]
            self.speed[1] = 0

    def update(self):
        """
        Atualiza a posição do jogador.
        """

        # Aplica as forças de campo
        for f in self.forces:
            self.speed[0] += f[0]
            self.speed[1] += f[1]

        # Aplica o movimento do input
        self.speed[0] += self.input[0] * self.move_acceleration[0]
        self.speed[1] += self.input[1] * self.move_acceleration[1]

        # Se não houve input, aplica a fricção
        self.speed[0] *= self.friction
        self.speed[1] *= self.friction

        # Limitando a velocidade
        # Calcula o módulo da velocidade
        mod = (self.speed[0] ** 2 + self.speed[1] ** 2) ** 0.5
        if mod > self.max_speed:
            # Normaliza a velocidade
            self.speed[0] = self.speed[0] * self.max_speed / mod
            self.speed[1] = self.speed[1] * self.max_speed / mod

        # Arredonda a velocidade
        self.speed[0] = round(self.speed[0] * 10000) / 10000
        self.speed[1] = round(self.speed[1] * 10000) / 10000

        # Atualiza a posição
        self.rect.move_ip(self.speed)
        self.clamp_pos()

        # Redefine o input
        self.input = [0, 0]

    def add_force(self, force: tuple):
        """
        Adiciona uma força de campo que atua sobre o jogador.
        """
        self.forces.append(force)

    def move(self, dir: str = ""):
        """
        Move o jogador na direção especificada.
        """
        if dir == "up" and self.input[1] > -1:
            self.input[1] -= 1
        elif dir == "down" and self.input[1] < 1:
            self.input[1] += 1
        elif dir == "left" and self.input[0] > -1:
            self.input[0] -= 1
        elif dir == "right" and self.input[0] < 1:
            self.input[0] += 1

    def draw(self, display):
        """
        Desenha o jogador na tela.
        """
        self.update()

        display.blit(self.image, self.rect)

    @property
    def pos_limits(self):
        """
        Limites da posição do jogador.
        """
        return self.limits_init, self.limits_end

    @pos_limits.setter
    def pos_limits(self, limits: tuple):
        """
        Define os limites da posição do jogador.
        """
        init, end = limits
        self.limits_init = init
        self.limits_end = end

    def grow(self, x):
        """
        Aumenta o tamanho do jogador.
        """
        self.rect.inflate_ip(x, x)
        self.image = pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height)
        )

    def shrink(self, x):
        """
        Diminui o tamanho do jogador.
        """
        self.rect.inflate_ip(-x, -x)
        self.image = pygame.transform.scale(
            self.image, (self.rect.width, self.rect.height)
        )
