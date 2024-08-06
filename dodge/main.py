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
    x, y = 0, 0
    if randint(0, 1):
        x = randint(0, WIDTH)
    else:
        y = randint(0, HEIGHT)

    # vector de velocidade normalizado em direção ao centro da tela
    vel_x = WIDTH // 2 - x
    vel_y = HEIGHT // 2 - y
    norm = (vel_x**2 + vel_y**2) ** 0.5
    vel_x /= norm
    vel_y /= norm

    bad.add(
        Thing(
            icon="img/thing.png",
            size=20,
            pos=(x, y),
            vel=(vel_x, vel_y),
        )
    )


def create_good_thing(good):
    x, y = 0, 0
    if randint(0, 1):
        x = randint(0, WIDTH)
    else:
        y = randint(0, HEIGHT)

    # vector de velocidade normalizado em direção ao centro da tela
    vel_x = WIDTH // 2 - x
    vel_y = HEIGHT // 2 - y
    norm = (vel_x**2 + vel_y**2) ** 0.5
    vel_x /= norm
    vel_y /= norm

    good.add(
        Thing(
            icon="img/heart.png",
            size=20,
            pos=(x, y),
            vel=(vel_x * 0.5, vel_y * 0.5),
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
    bad_freq = 1
    good = pygame.sprite.Group()
    good_counter = 0

    fart = Sound("sound/fart.mp3")
    star = Sound("sound/star.mp3")

    while True:
        # Processa os eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            p.move("left")
        if keys[pygame.K_RIGHT]:
            p.move("right")
        if keys[pygame.K_UP]:
            p.move("up")
        if keys[pygame.K_DOWN]:
            p.move("down")

        bad_counter += bad_freq
        if bad_counter >= FPS * 1:
            create_bad_thing(bad)
            bad_counter = 0
            bad_freq += 0.05

        good_counter += 1
        if good_counter == FPS * 3:
            create_good_thing(good)
            good_counter = 0

        # check colision with bad things
        for b in bad:
            if pygame.sprite.collide_rect(p, b):
                b.kill()
                fart.play()
                life.value -= 1

        # check colision with good things
        for g in good:
            if pygame.sprite.collide_rect(p, g):
                g.kill()
                star.play()
                life.value += 1

        # white background
        display.fill((255, 255, 255))

        bad.update()
        bad.draw(display)

        good.update()
        good.draw(display)

        life.draw(display)
        t.draw(display)
        p.draw(display)

        pygame.display.flip()

        clock.tick(FPS)


main()
