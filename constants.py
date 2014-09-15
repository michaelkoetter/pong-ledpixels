import pygame
from pygame.locals import *

# Display
DISPLAY_SIZE = (90, 20)

# Colors
COLOR_BLACK =       pygame.Color(  0,   0,   0)
COLOR_WHITE =       pygame.Color(255, 255, 255)
COLOR_RED   =       pygame.Color(255,   0,   0)
COLOR_DARKGRAY =    pygame.Color( 50,  50,  50)

# Game logic
(PLAYER_LEFT, PLAYER_RIGHT) = (1, 2)
(DIR_UP, DIR_DOWN, DIR_NONE) = (-1, 1, 0)
(KEY_LEFT_UP, KEY_LEFT_DOWN, KEY_RIGHT_UP, KEY_RIGHT_DOWN) = (K_a, K_y, K_k, K_m)
FIELD_RECT = pygame.Rect(0, 0, 90, 20)

