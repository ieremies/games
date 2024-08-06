#!/usr/bin/env python3

"""
Módulo para implementar uma pontuação no jogo no canto superior direito da tela.
"""
import pygame
from element import Element
from conf import HEIGHT, WIDTH


class Score(Element):
    """
    Classe para criar um placar.
    """

    def __init__(
        self,
        icon: str = "img/star.png",
        text: str = "Score",
        value: int = 0,
        pos="topright",
    ):
        """
        Inicializa o placar.
        """
        super().__init__(icon=icon, text=text, value=value, pos=pos)
