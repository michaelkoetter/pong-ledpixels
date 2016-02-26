import sys
import led
import sprites

from constants import *
from led.PixelEventHandler import *

pygame.init()

fallbackSize = (90, 20)

teensyDisplay = led.dsclient.DisplayServerClientDisplay('localhost', 8123, fallbackSize)
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

pygame.joystick.init()

# Initialize first joystick
if pygame.joystick.get_count() > 0:
    stick = pygame.joystick.Joystick(0)
    stick.init()


def clear_sprite(surf, rect):
    surf.fill(COLOR_BLACK, rect)

def main():
    _ball = None

    while True:
        for pgevent in pygame.event.get():
            if pgevent.type == QUIT:
                pygame.quit()
                sys.exit()

            event = process_event(pgevent)

            if event.button == EXIT:
                pygame.quit()
                sys.exit()

            if event.type == PUSH: # KEYDOWN
                if event.button == UP and event.player == PLAYER1:
                    leftPaddle.move(DIR_UP)
                elif event.button == DOWN and event.player == PLAYER1:
                    leftPaddle.move(DIR_DOWN)
                elif event.button == UP and event.player == PLAYER2:
                    rightPaddle.move(DIR_UP)
                elif event.button == DOWN and event.player == PLAYER2:
                    rightPaddle.move(DIR_DOWN)

            elif event.type == RELEASE and (event.button == DOWN or event.button == UP): #KEYUP
                if event.player == PLAYER1:
                    leftPaddle.move(DIR_NONE)
                elif event.player == PLAYER2:
                    rightPaddle.move(DIR_NONE)

        # create new ball if necessary
        if not bool(ball):
            _ball = sprites.Ball(fieldRect)
            _ball.add((allSprites, ball))

        # check collisions with paddle..
        ball_paddles = pygame.sprite.groupcollide(ball, paddles, False, False)
        if ball_paddles:
            _ball.increase_speed()
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