import pygame
import pygame.draw

from point import Point
from constants import *


root_point = Point(ROOT_POINT_POSITION)


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    setup(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                on_mouse_button_down(event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                on_mouse_button_up(event.pos, event.button)

        update(screen)
        pygame.display.flip()


def setup(screen):
    pass


def update(screen):
    screen.fill(COLOR_BACKGROUND)
    draw_system(screen)
    draw_points(screen)


def on_mouse_button_down(pos, button): pass
def on_mouse_button_up(pos, button): pass


def draw_points(screen):
    scaled_pos = scale_pos(root_point)
    pygame.draw.circle(screen, COLOR_POINT_SELECTED,
                       scaled_pos, POINT_RADIUS_SELECTED)


def draw_system(screen):
    for x in range(SYSTEM_WIDTH):
        for y in range(SYSTEM_HEIGHT):
            pos = scale_pos((x, y))
            pygame.draw.circle(screen, COLOR_POINT_NORMAL,
                               pos, POINT_RADIUS_NORMAL)


def scale_pos(pos):
    x, y = pos
    scaled_x = (x + 0.5) * GAP_WIDTH
    scaled_y = (SYSTEM_HEIGHT - (y + 0.5)) * GAP_HEIGHT
    scaled_pos = scaled_x, scaled_y
    return scaled_pos


main()
