#!/usr/bin/env python3

"""
Implementa uma barra de "progresso" que pode ser usada como barra de vida ou de pontuação.
"""

import pygame
from element import Element
from colors import BLUE, GRAY, BLACK


class Bar(Element):

    def __init__(
        self,
        color_front: tuple = BLUE,
        color_back: tuple = GRAY,
        start_value: int = 0,
        max_value: int = 100,
        bar_height: int = 10,
        bar_width: int = 200,
        text: str = "Bar",
        icon: str = "img/star.png",
        pos: str = "bottomright",
    ):
        """
        Inicializa a barra de progresso.

        Ela será no formato:

        [ICONE] [TEXTO] [VALOR] [#######......]
        onde # é a color_front e . é a color_back.
        """

        self._color_front = color_front
        self._color_back = color_back
        self._max_value = max_value
        self._bar_height = bar_height
        self._bar_width = bar_width
        self._value = start_value

        super().__init__(icon=icon, text=text, value=start_value, pos=pos)

        self._bar_background_img = pygame.Surface((self._bar_width, self._bar_height))
        self._bar_background_img.fill(self._color_back)

    @Element.value.setter
    def value(self, value: int):
        """
        Define o valor da barra de progresso.
        """
        Element.value.fset(self, value)

        if self.value < 0:
            front_width = 0
        else:
            front_width = self._bar_width * self.value // self._max_value

        self._bar_foreground_img = pygame.Surface((front_width, self._bar_height))
        self._bar_foreground_img.fill(self._color_front)

    @property
    def width(self):
        return super().width + self._padding + self._bar_width

    @property
    def height(self):
        return max(super().height, self._bar_height)

    def draw(self, display):
        """
        Desenha a barra de progresso na tela.
        """

        super().draw(display)

        x, y = self._translate_position(display)
        x += super().width + self._padding
        y += (self.height - self._bar_height) // 2

        # Desenha a barra de fundo
        display.blit(self._bar_background_img, (x, y))

        # Desenha a barra de progresso
        display.blit(self._bar_foreground_img, (x, y))
