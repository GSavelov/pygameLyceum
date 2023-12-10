import pygame
from config import *
from map import world_map


def ray_casting(surface, pos, angle):
    cur_angle = angle - H_FOV
    x0, y0 = pos
    for ray in range(NUM_RAYS):
        sin_a = math.sin(cur_angle)
        cos_a = math.cos(cur_angle)
        for depth in range(MAX_DEPTH):
            x = x0 + depth * cos_a
            y = y0 + depth * sin_a
            pygame.draw.line(surface, 'white', pos, (x, y), 1)
            if (x // TILE * TILE, y // TILE * TILE) in world_map:
                break
        cur_angle += DELTA_A
