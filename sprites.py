import pygame

from constants import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, player, fieldRect):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1, 5))
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_WHITE)

        self._direction = DIR_NONE
        self._player = player
        self._fieldRect = fieldRect

        if player == PLAYER_LEFT: self.rect.midleft = self._fieldRect.midleft
        else: self.rect.midright = self._fieldRect.midright

    def move(self, direction):
        self._direction = direction

    def update(self, *args):
        _rect = self.rect.move(0, self._direction).clamp(self._fieldRect)
        self.rect = _rect

class Ball(pygame.sprite.Sprite):
    def __init__(self, fieldRect, speed = 0.4):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.image.fill(COLOR_WHITE)
        self.rect.center = fieldRect.center

        self._fieldRect = fieldRect
        self._dirx = 1
        self._diry = 1
        self._speed = speed
        self._movement = 0.0

    def update(self, *args):

        self._movement += self._speed
        if self._movement >= 1.0:
            if self.rect.top <= self._fieldRect.top or self.rect.bottom >= self._fieldRect.bottom:
                self._diry *= -1
            if self.rect.left <= self._fieldRect.left or self.rect.right >= self._fieldRect.right:
                self._dirx *= -1

            _rect = self.rect.move(self._movement * self._dirx, self._movement * self._diry)
            self.rect = _rect
            self._movement -= 1.0

class Wall(pygame.sprite.Sprite):
    def __init__(self, player, fieldRect):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((1, fieldRect.height))
        self.rect = self.image.get_rect()
        #self.image.fill(COLOR_RED)

        self._player = player
        self._fieldRect = fieldRect

        if player == PLAYER_RIGHT: self.rect.midleft = self._fieldRect.midleft
        else: self.rect.midright = self._fieldRect.midright

    def get_player(self):
        return self._player
