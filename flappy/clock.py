#!/usr/bin/env python3

import pygame
import time
from element import Element


class Stopwatch(Element):
    """
    Classe para criar um relógio.
    """

    def __init__(
        self,
        value: int = 0,
        icon: str = "img/clock.png",
        text: str = "Clock",
        pos="topcenter",
    ):
        """
        Inicializa o relógio.
        """
        super().__init__(icon=icon, text=text, value=value, pos=pos)
        self._start = time.time()

    def draw(self, display):
        """
        Desenha o relógio na tela.
        """
        self.value = int(time.time() - self._start)
        super().draw(display)


class Timer(Element):
    """
    Classe para criar um temporizador.
    """

    def __init__(
        self,
        value: int = 100,
        icon: str = "img/clock.png",
        text: str = "Timer",
        pos="topcenter",
    ):
        """
        Inicializa o temporizador.
        """
        super().__init__(icon=icon, text=text, value=value, pos=pos)
        self._end = time.time() + value

    def draw(self, display):
        """
        Desenha o temporizador na tela.
        """
        self.value = max(int(self._end - time.time()), 0)
        super().draw(display)
