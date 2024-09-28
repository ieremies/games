#!/usr/bin/env python3

import pygame

pygame.mixer.init()


class Sound:
    def __init__(self, sound: str):
        self.sound = pygame.mixer.Sound(sound)

    def play(self):
        self.sound.play()
