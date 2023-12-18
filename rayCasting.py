import pygame
from math import sin, cos
from config import *
from map import world_map


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(surface, pos, angle):
    ox, oy = pos
    xm, ym = mapping(ox, oy)
    cur_angle = angle - H_FOV
    for ray in range(NUM_RAYS):
        sin_a = sin(cur_angle)
        cos_a = cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            y = oy + depth_v * sin_a
            if mapping(x + dx, y) in world_map:
                break
            x += dx * TILE

        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            x = ox + depth_h * cos_a
            if mapping(x, y + dy) in world_map:
                break
            y += dy * TILE

        depth = depth_v if depth_v < depth_h else depth_h
        depth *= cos(angle - cur_angle)
        proj_height = PROJ_COEFF / depth
        c = 255 / (1 + depth * depth * 0.00002)
        color = (c, c // 2, c // 3)
        pygame.draw.rect(surface, color, (ray * SCALE, H_HEIGHT - proj_height // 2, SCALE, proj_height))
        cur_angle += DELTA_A
