#!/bin/env python3


# IMPORTS

import os
import sys
from typing import Iterable, List, Tuple

import pygame
import pygame.display
import pygame.draw
import pygame.event
import pygame.image
import pygame.time
from pygame.surface import Surface

from point import Point, RootPoint
from constants import *

sys.setrecursionlimit(8192)


# GLOBALS

root_point = RootPoint(0, 0, [
    lambda x, y: (x + 7, y),       # 7 up
    # lambda x, y: (x - 13, y - 6),  # 13 left, 6 down
    lambda x, y: (x + 1, y + 8),   # right, 8 up
    # lambda x, y: (x, y + 1),       # up
    # lambda x, y: (x, y - 1),       # down
    # lambda x, y: (x + 1, y),       # right
    # lambda x, y: (x - 1, y),       # left
    # lambda x, y: (x + 1, y + 1),   # right up
    # lambda x, y: (x + 1, y - 1),   # right down
    # lambda x, y: (x - 1, y - 1),   # left down
    # lambda x, y: (x - 1, y + 1),   # left up
], AREA_WIDTH, AREA_HEIGHT)


# MAIN

def main():
    print(root_point)

    pygame.init()
    init()

    screen = pygame.display.set_mode(WINDOW_SIZE)
    setup(screen)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

        clock.tick(FPS)


# EVENTS

def init():
    icon_path = os.path.join(sys.path[0], WINDOW_ICON_RELATIVE_PATH)
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
    pygame.display.set_caption(WINDOW_TITLE)


def setup(screen: Surface):
    screen.fill(BACKGROUND_COLOR)
    draw_grid_lines(screen)
    draw_grid_points(screen)
    draw_marked_points(screen, root_point)


def update(screen: Surface):
    pass


# DRAW HELPERS

def draw_marked_points(screen: Surface, point: Point):
    if 0 <= point.x < AREA_WIDTH and 0 <= point.y < AREA_HEIGHT:
        scaled_pos = scale_position(point.x, point.y)
        pygame.draw.circle(screen, ROOT_POINT_COLOR, scaled_pos, POINT_RADIUS)

    for child in point.children:
        draw_marked_points(screen, child)


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

def scale_position(x: int, y: int) -> Tuple[int, int]:
    scaled_x = (x + 0.5) * GAP_WIDTH
    scaled_y = (AREA_HEIGHT - (y + 0.5)) * GAP_HEIGHT
    return scaled_x, scaled_y


def is_in_boundry(x: int, y: int) -> bool:
    return 0 <= x < AREA_WIDTH and 0 <= y < AREA_HEIGHT


# EXECUTION

main()
