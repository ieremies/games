#!/usr/bin/env python3
"""
Módulo para implementar um elemento composto de ICONE, TEXTO, VALOR.
Ele pode ser colocado em qualquer canto da tela.
"""
import pygame
from colors import BLACK


class Element:
    """
    Classe para criar um elemento composto de icone, texto e valor.
    """

    def __init__(
        self, icon: str = None, text: str = None, value: int = None, pos="topleft"
    ):
        self._pos = pos
        self._font = pygame.font.Font(None, 36)
        self._padding = 10

        self.icon = icon
        self.text = text
        self.value = value

    # === Icon ===============================================================
    @property
    def icon(self):
        return self._icon

    @icon.setter
    def icon(self, path: str, size: int = 20):
        self._icon = path

        if self._icon is None:
            self._icon_img = pygame.Surface((0, 0))
        else:
            self._icon_img = pygame.image.load(self._icon)
            self._icon_img = pygame.transform.scale(self._icon_img, (size, size))

    # === Text ===============================================================
    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value: str):
        self._text = value

        if self._text is None:
            self._text_img = pygame.Surface((0, 0))
        else:
            self._text_img = self._font.render(f"{self.text}", True, BLACK)

    # === Value ===============================================================
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value

        if self._value is None:
            self._value_img = pygame.Surface((0, 0))
        else:
            self._value_img = self._font.render(f"{self._value}", True, BLACK)

    # ========================================================================
    @property
    def width(self):
        """
        Largura do elemento.

        É igual a soma das larguras de cada um dos valores mais o valor de "padding"
        entre cada elemento que não é vazio.
        """
        sum_width = 0
        if self._icon_img.get_width() > 0:
            sum_width += self._icon_img.get_width()
            sum_width += self._padding
        if self._text_img.get_width() > 0:
            sum_width += self._text_img.get_width()
            sum_width += self._padding
        if self._value_img.get_width() > 0:
            sum_width += self._value_img.get_width()
            sum_width += self._padding
        return sum_width

    @property
    def height(self):
        """
        Altura do elemento.

        Igual à maior das alturas entre os valores.
        """
        return max(
            self._icon_img.get_height(),
            self._text_img.get_height(),
            self._value_img.get_height(),
        )

    # ========================================================================
    def _translate_position(self, display) -> tuple:
        """
        Traduz a posição do elemento para a posição real na tela.
        """
        if self._pos.startswith("top"):
            y = self._padding
        elif self._pos.startswith("center"):
            y = (display.get_height() - self.height) // 2
        else:
            y = display.get_height() - self._padding - self.height

        if self._pos.endswith("left"):
            x = self._padding
        elif self._pos.endswith("center"):
            x = (display.get_width() - self.width) // 2
        else:
            x = display.get_width() - self.width - self._padding

        return x, y

    def draw(self, display):
        """
        Desenha o elemento na tela baseado na posição indicada (self._pos).

        As posições possíveis são combinações de (top, center, bottom) com
        (left, center, right).
        """

        x, y = self._translate_position(display)

        display.blit(self._icon_img, (x, y))
        x += self._icon_img.get_width() + self._padding

        display.blit(self._text_img, (x, y))
        x += self._text_img.get_width() + self._padding

        display.blit(self._value_img, (x, y))
        x += self._value_img.get_width() + self._padding

    # === Special Methods ====================================================

    def __add__(self, other: int):
        return self.value + other

    def __iadd__(self, other: int):
        self.value += other
        return self

    def __str__(self):
        return f"{self._icon} | {self.text}: {self.value}"
