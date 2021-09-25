#!/bin/env python3


# IMPORTS

import os
import sys

import pygame
import pygame.draw
import pygame.display
import pygame.image

from point import Point
from constants import *


# GLOBALS

root_point = Point(0, 0)

child_generators = [
    lambda x, y: (x + 7, y),       # 7 up
    lambda x, y: (x - 13, y - 6),  # 13 left, 6 down
    lambda x, y: (x + 1, y + 8),   # right, 8 up
    # lambda x, y: (x, y + 1),       # up
    # lambda x, y: (x, y - 1),       # down
    # lambda x, y: (x + 1, y),       # right
    # lambda x, y: (x - 1, y),       # left
    # lambda x, y: (x + 1, y + 1),   # right up
    # lambda x, y: (x + 1, y - 1),   # right down
    # lambda x, y: (x - 1, y - 1),   # left down
    # lambda x, y: (x - 1, y + 1),   # left up
]


# MAIN

def main():
    pygame.init()
    init()

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


# EVENTS

def init():
    icon_path = os.path.join(sys.path[0], WINDOW_ICON_RELATIVE_PATH)
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_TITLE)


def setup(screen):
    lookup_table = [[0 for _ in range(SYSTEM_WIDTH)]
                    for _ in range(SYSTEM_HEIGHT)]
    create_children(root_point, lookup_table)


def update(screen):
    screen.fill(COLOR_BACKGROUND)
    draw_system_lines(screen)
    draw_system_points(screen)
    # TODO: Animate creation of new child points
    draw_points(screen)


def on_mouse_button_down(pos, button):
    pass


def on_mouse_button_up(pos, button):
    pass


# UTILS

def draw_points(screen):
    draw_children(screen, root_point)

    scaled_pos = scale_pos(root_point)
    pygame.draw.circle(screen, COLOR_POINT_SELECTED,
                       scaled_pos, POINT_RADIUS_SELECTED)


def draw_children(screen, point):
    scaled_pos = scale_pos(point)
    pygame.draw.circle(screen, COLOR_POINT_SELECTED,
                       scaled_pos, POINT_RADIUS_NORMAL)

    for child in point.children:
        draw_children(screen, child)


def draw_system_points(screen):
    for x in range(SYSTEM_WIDTH):
        for y in range(SYSTEM_HEIGHT):
            pos = scale_pos((x, y))
            pygame.draw.circle(screen, COLOR_POINT_NORMAL,
                               pos, POINT_RADIUS_NORMAL)


def draw_system_lines(screen):
    for x in range(SYSTEM_WIDTH):
        scaled_x = (x + 0.5) * GAP_WIDTH
        start = scaled_x, 0
        end = scaled_x, HEIGHT
        pygame.draw.line(screen, COLOR_LINE_NORMAL, start, end)

    for y in range(SYSTEM_HEIGHT):
        scaled_y = (y + 0.5) * GAP_WIDTH
        start = 0, scaled_y
        end = WIDTH, scaled_y
        pygame.draw.line(screen, COLOR_LINE_NORMAL, start, end)


def scale_pos(pos):
    x, y = pos
    scaled_x = (x + 0.5) * GAP_WIDTH
    scaled_y = (SYSTEM_HEIGHT - (y + 0.5)) * GAP_HEIGHT
    scaled_pos = scaled_x, scaled_y
    return scaled_pos


def create_children(point: Point, lookup_table):
    for child_generator in child_generators:
        child = Point(child_generator(point.x, point.y))
        x, y = int(child.x), int(child.y)

        # TODO: Take into account the ones that return from outer space
        if is_in_boundry(x, y) and not lookup_table[y][x]:
            lookup_table[y][x] = 1
            create_children(child, lookup_table)
            point.children.append(child)


def is_in_boundry(x, y) -> bool:
    return 0 <= x < SYSTEM_WIDTH and 0 <= y < SYSTEM_HEIGHT


# FUNCTION CALL

main()
