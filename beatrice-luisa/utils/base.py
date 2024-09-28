import pygame


class Base:
    def __init__(self, x, y, width, height):
        self.pos = [x, y]
        self.size = [width, height]

    @property
    def width(self):
        return self.size[0]

    @width.setter
    def width(self, value):
        self.size[0] = value

    @property
    def height(self):
        return self.size[1]

    @height.setter
    def height(self, value):
        self.size[1] = value

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, value):
        self.pos[0] = value

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, value):
        self.pos[1] = value

    @property
    def rect(self):
        return pygame.Rect(self.pos, self.size)

    def collides_with(self, other):
        return self.rect.colliderect(other.rect)


pygame.mixer.init()


class Sound:
    def __init__(self, sound: str):
        self.sound = pygame.mixer.Sound(sound)

    def play(self):
        self.sound.play()
