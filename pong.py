import pygame, sys, os
import led, led.game_controller
import sprites

from pygame.locals import *
from constants import *
from led.game_controller import *

pygame.init()


try:
    serialPort = sys.argv[1]
except IndexError:
    serialPort = None

teensyDisplay = led.teensy.TeensyDisplay(serialPort, DISPLAY_SIZE)
displaySize = teensyDisplay.size()
fieldRect = pygame.Rect((0,0), displaySize)

simDisplay = led.sim.SimDisplay(displaySize)
screen = pygame.Surface(displaySize)

fpsClock = pygame.time.Clock()

leftPaddle = sprites.Paddle(PLAYER_LEFT, fieldRect)
rightPaddle = sprites.Paddle(PLAYER_RIGHT, fieldRect)
leftWall = sprites.Wall(PLAYER_LEFT, fieldRect)
rightWall = sprites.Wall(PLAYER_RIGHT, fieldRect)

allSprites = pygame.sprite.OrderedUpdates()
paddles = pygame.sprite.Group()
walls = pygame.sprite.Group()
ball = pygame.sprite.GroupSingle()

leftWall.add((allSprites, walls))
rightWall.add((allSprites, walls))
leftPaddle.add((allSprites, paddles))
rightPaddle.add((allSprites, paddles))

font = pygame.font.SysFont("Arial", 12)

scores = { PLAYER_LEFT: 0, PLAYER_RIGHT: 0 }

controller = led.game_controller.GameController("/dev/cu.usbmodem621")

def clear_sprite(surf, rect):
    surf.fill(COLOR_BLACK, rect)

def main():
    _ball = None

    while True:
        for event in controller.get_events():
            print event
            if event[1] == 1: # KEYDOWN
                if event[0] == BTN_P1_UP:
                    leftPaddle.move(DIR_UP)
                elif event[0] == BTN_P1_DOWN:
                    leftPaddle.move(DIR_DOWN)
                elif event[0] == BTN_P2_UP:
                    rightPaddle.move(DIR_UP)
                elif event[0] == BTN_P2_DOWN:
                    rightPaddle.move(DIR_DOWN)
            else: #KEYUP
                if event[0] == BTN_P1_UP or event[0] == BTN_P1_DOWN:
                    leftPaddle.move(DIR_NONE)
                elif event[0] == BTN_P2_UP or event[0] == BTN_P2_DOWN:
                    rightPaddle.move(DIR_NONE)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == KEY_LEFT_UP:
                    leftPaddle.move(DIR_UP)
                elif event.key == KEY_LEFT_DOWN:
                    leftPaddle.move(DIR_DOWN)
                elif event.key == KEY_RIGHT_UP:
                    rightPaddle.move(DIR_UP)
                elif event.key == KEY_RIGHT_DOWN:
                    rightPaddle.move(DIR_DOWN)
            elif event.type == KEYUP:
                if event.key == KEY_LEFT_UP or event.key == KEY_LEFT_DOWN:
                    leftPaddle.move(DIR_NONE)
                elif event.key == KEY_RIGHT_UP or event.key == KEY_RIGHT_DOWN:
                    rightPaddle.move(DIR_NONE)

        # create new ball if necessary
        if not bool(ball):
            _ball = sprites.Ball(fieldRect)
            _ball.add((allSprites, ball))

        # check collisions with paddle..
        ball_paddles = pygame.sprite.groupcollide(ball, paddles, False, False)
        if ball_paddles:
            # nothing happens
            pass
        else:
            # .. or wall
            ball_walls = pygame.sprite.groupcollide(ball, walls, True, False)
            if ball_walls:
                # player scores!
                (_ball, _walls) = ball_walls.popitem()
                _player = _walls[0].get_player()
                scores[_player] += 1

        screen.fill(COLOR_BLACK)

        scoreLeft = font.render(str(scores[PLAYER_LEFT]), True, COLOR_DARKGRAY)
        scoreRight = font.render(str(scores[PLAYER_RIGHT]), True, COLOR_DARKGRAY)

        r = scoreLeft.get_rect()
        r.center = (fieldRect.width / 4, fieldRect.centery)
        screen.blit(scoreLeft, r)

        r = scoreRight.get_rect()
        r.center = (fieldRect.width - fieldRect.width / 4, fieldRect.centery)
        screen.blit(scoreRight, r)

        allSprites.update()
        allSprites.draw(screen)

        teensyDisplay.update(screen)
        simDisplay.update(screen)

        fpsClock.tick(30)

main()