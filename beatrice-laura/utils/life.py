#!/usr/bin/env python3

from utils.bar import Bar
from utils.colors import RED, GRAY


class Lifebar(Bar):
    """
    Classe para criar uma barra de vida.
    """

    def __init__(
        self,
        color_front: tuple = RED,
        color_back: tuple = GRAY,
        start_value: int = 10,
        max_value: int = 10,
        bar_height: int = 20,
        bar_width: int = 150,
        text: str = "Life",
        icon: str = None,
        pos: str = "topleft",
    ):
        """
        Inicializa a barra de vida.
        """
        super().__init__(
            color_front=color_front,
            color_back=color_back,
            start_value=start_value,
            max_value=max_value,
            bar_height=bar_height,
            bar_width=bar_width,
            text=text,
            icon=icon,
            pos=pos,
        )
