import pygame
from math import sin, cos
from config import *
from map import world_map, WORLD_WIDTH, WORLD_HEIGHT


def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(player, textures):
    walls = []
    texture_v, texture_h = 1, 1
    """Фикс ошибки при выходе за карту
    
    Устанавливается значение текстуры 'по умолчанию'.
    В случае если пересечение луча со стеной по горизонтали
    или вертикали не будет найдено программа не вылетит с ошибкой.
    """
    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    cur_angle = player.angle - H_FOV
    for ray in range(NUM_RAYS):
        sin_a = sin(cur_angle)
        cos_a = cos(cur_angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORLD_WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in world_map:
                texture_v = world_map[tile_v]
                break
            x += dx * TILE

        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORLD_HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in world_map:
                texture_h = world_map[tile_h]
                break
            y += dy * TILE

        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= cos(player.angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = min((PROJ_COEFF / depth), P_HEIGHT)

        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_WIDTH)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))

        wall_pos = (ray * SCALE, H_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))

        cur_angle += DELTA_A
    return walls
