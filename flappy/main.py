#!/usr/bin/env python3

import pygame
import sys
from random import random, randint
from conf import HEIGHT, WIDTH, FPS
from element import Element
from score import Score
from clock import Stopwatch, Timer
from life import Lifebar
from player import Player
from thing import Thing
from sound import Sound


def create_bad_thing(bad):
    x = WIDTH
    y = randint(0, HEIGHT)

    bad.add(
        Thing(
            icon="img/thing.png",
            size=20,
            pos=(x, y),
            vel=(-1, 0),
        )
    )


def create_cloud_thing(cloud):
    x = WIDTH + 500
    y = randint(0, HEIGHT)

    cloud.add(
        Thing(
            icon="img/cloud.png",
            size=200,
            pos=(x, y),
            vel=(-0.7, 0),
        )
    )


def main():
    """
    Função principal que controla o fluxo do jogo.
    """

    pygame.init()  # inicia o jogo
    clock = pygame.time.Clock()  # inicia o relógio
    display = pygame.display.set_mode((WIDTH, HEIGHT))  # inicia a tela

    life = Lifebar()
    t = Timer(value=100, pos="bottomcenter")
    p = Player(pos=(HEIGHT // 2, WIDTH // 2))
    p.pos_limits = ((0, 0), (WIDTH, HEIGHT))

    bad = pygame.sprite.Group()
    bad_counter = 0

    cloud = pygame.sprite.Group()
    cloud_counter = 0
    bullet_freq = 1

    fart = Sound("sound/fart.mp3")

    while True:
        # Processa os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            p.move("up")

        bad_counter += bullet_freq
        if bad_counter >= FPS * 1:
            create_bad_thing(bad)
            bad_counter = 0
            bullet_freq += 0.05

        cloud_counter += 1
        if cloud_counter == FPS * 1:
            create_cloud_thing(cloud)
            cloud_counter = 0

        # check colision with bad things
        for b in bad:
            if pygame.sprite.collide_rect(p, b):
                b.kill()
                fart.play()
                life.value -= 1

            # se estiver fora da tela
            if b.rect.right < 0:
                b.kill()

        display.fill((173, 216, 230))

        cloud.update()
        cloud.draw(display)

        bad.update()
        bad.draw(display)

        life.draw(display)
        t.draw(display)
        p.draw(display)

        pygame.display.flip()

        clock.tick(FPS)


main()
