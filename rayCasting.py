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
            if (x // TILE * TILE, y // TILE * TILE) in world_map:
                depth *= math.cos(angle - cur_angle)
                c = 255 / (1 + depth * depth * 0.00002)
                color = (c, c // 2, c // 3)
                proj_height = PROJ_COEFF / (depth + 0.000001)
                pygame.draw.rect(surface, color, (ray * SCALE, H_HEIGHT - proj_height // 2, SCALE, proj_height))
                break
        cur_angle += DELTA_A
