#!/bin/env python3


# IMPORTS

import os
import sys
from typing import List, Tuple

import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.image
from pygame.surface import Surface

from point import Point
from constants import *


# TYPES

OrderedPair = Tuple[int, int]
AreaMatrix = List[List[int]]


# GLOBALS

root_point = Point(0, 0)


child_functions = [
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

    screen = pygame.display.set_mode(WINDOW_SIZE)
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


def setup(screen: Surface):
    lookup_table = [[0 for _ in range(AREA_WIDTH)] for _ in range(AREA_HEIGHT)]
    init_child_points(root_point, lookup_table)

    screen.fill(BACKGROUND_COLOR)
    draw_grid_lines(screen)
    draw_grid_points(screen)
    draw_child_points(screen, root_point)
    draw_root_point(screen)


def update(screen: Surface):
    pass


def on_mouse_button_down(position: OrderedPair, button: int):
    pass


def on_mouse_button_up(position: OrderedPair, button: int):
    pass


# DRAW HELPERS

def draw_root_point(screen: Surface):
    scaled_pos = scale_position(root_point.x, root_point.y)
    pygame.draw.circle(screen, ROOT_POINT_COLOR, scaled_pos, POINT_RADIUS)


def draw_child_points(screen: Surface, point: Point):
    scaled_pos = scale_position(point.x, point.y)
    pygame.draw.circle(screen, CHILD_POINT_COLOR, scaled_pos, POINT_RADIUS)

    for child in point.children:
        draw_child_points(screen, child)


def draw_grid_points(screen: Surface):
    for x in range(AREA_WIDTH):
        for y in range(AREA_HEIGHT):
            pos = scale_position(x, y)
            pygame.draw.circle(screen, GRID_POINT_COLOR, pos, POINT_RADIUS)


def draw_grid_lines(screen: Surface):
    for x in range(AREA_WIDTH):
        start = scale_position(x, 0)
        end = scale_position(x, AREA_WIDTH - 1)
        pygame.draw.line(screen, GRID_LINE_COLOR, start, end)

    for y in range(AREA_HEIGHT):
        start = scale_position(0, y)
        end = scale_position(AREA_WIDTH - 1, y)
        pygame.draw.line(screen, GRID_LINE_COLOR, start, end)


# UTILS

def scale_position(x: int, y: int) -> OrderedPair:
    scaled_x = (x + 0.5) * GAP_WIDTH
    scaled_y = (AREA_HEIGHT - (y + 0.5)) * GAP_HEIGHT
    return scaled_x, scaled_y


def init_child_points(point: Point, lookup_table: AreaMatrix):
    for child_generator in child_functions:
        child = Point(child_generator(point.x, point.y))
        x, y = int(child.x), int(child.y)

        if is_in_boundry(x, y) and not lookup_table[y][x]:
            lookup_table[y][x] = 1
            init_child_points(child, lookup_table)
            point.children.append(child)


def is_in_boundry(x: int, y: int) -> bool:
    return 0 <= x < AREA_WIDTH and 0 <= y < AREA_HEIGHT


# EXECUTION

main()
