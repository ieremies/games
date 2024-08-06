#!/usr/bin/env python3
import pygame
import math


class Thing(pygame.sprite.Sprite):
    """
    Classe para criar um objeto genérico.
    """

    def __init__(
        self, icon: str = "img/thing.png", size: int = 20, pos=(0, 0), vel=(0, 0)
    ):
        """
        Inicializa o objeto genérico.
        """
        super().__init__()
        self.image = pygame.image.load(icon)
        self.image = pygame.transform.scale(self.image, (size * 1.6, size))

        self.rect = self.image.get_rect()
        self.rect.center = pos

        self._speed_mult = 10
        self._speed = [vel[0] * self._speed_mult, vel[1] * self._speed_mult]

        # rotate to match vel
        # angle = math.degrees(math.atan2(self._speed[1], self._speed[0]))
        # self.image = pygame.transform.rotate(self.image, -angle)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, display):
        """
        Desenha o objeto genérico na tela.
        """
        self.update()
        display.blit(self.image, self.rect)

    def update(self):
        """
        Atualiza o objeto genérico.
        """
        self.rect.move_ip(self._speed)
