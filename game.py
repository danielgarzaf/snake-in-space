
import random
import pygame
import sys
import time

from pygame.locals import *

import player
import snake
import sky


def quit_requested(event):
    return event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE


def pause_requested(event):
    return event.type == pygame.KEYDOWN and event.key == pygame.K_p


def pause_cancel_requested(event):
    return event.type == pygame.KEYDOWN and event.key == pygame.K_p


def listen_keys(p1, paused):
    for event in pygame.event.get():
        if quit_requested(event):
            pygame.quit()
            sys.exit()
        if not paused:
            if pause_requested(event):
                paused = True
                time.sleep(1)
                continue
            p1.input(event)
        else:
            if pause_cancel_requested(event):
                paused = False
                continue
    return paused


def main():
    pygame.init()
    screen_dim = (1360, 768)
    display = pygame.display.set_mode(screen_dim, FULLSCREEN | HWSURFACE if not sys.gettrace() else HWSURFACE)
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    uc = snake.Snake(screen_dim[0]/3, screen_dim[1]/2, screen_dim[0], screen_dim[1])
    clock = pygame.time.Clock()
    scene = sky.Sky(screen_dim)
    p1 = player.Player()
    paused = False

    while True:
        paused = listen_keys(p1, paused)
        if paused:
            continue

        if len(scene.enemies) < 50 and random.randint(0, 160) == 0:
            scene.inc_enemies()

        if len(scene.bubbles) == 0 and random.randint(0, 160) == 0:
            scene.inc_bubbles()

        surface = pygame.Surface(screen_dim)

        if p1.turning_left():
            uc.go_left()
        if p1.turning_right():
            uc.go_right()
        if p1.firing():
            uc.fire()
        else:
            uc.stop_firing()

        scene.update(uc.x, uc.y)

        if scene.check_hit(uc):
            uc.hit()

        if scene.check_fed(uc):
            uc.fed()

        scene.draw_background(surface)

        if p1.firing():
            line_start, line_end = uc.draw(surface)
            scene.check_targets(line_start, line_end)
        else:
            uc.draw(surface)

        scene.draw_foreground(surface)

        display.blit(surface, (0, 0))
        pygame.display.flip()

        clock.tick(100)


main()
