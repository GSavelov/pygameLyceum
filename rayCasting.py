import pygame
from numba import njit
from math import sin, cos
from config import *
from map import world_map, WORLD_WIDTH, WORLD_HEIGHT


@njit(fastmath=True)
def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


@njit(fastmath=True)
def ray_casting(player_pos, player_angle, world_map):
    casted_walls = []
    texture_v, texture_h = 1, 1
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - H_FOV
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
        depth *= cos(player_angle - cur_angle)
        depth = max(depth, 0.00001)
        proj_height = (PROJ_COEFF / depth)

        casted_walls.append((depth, offset, proj_height, texture))

        cur_angle += DELTA_A
    return casted_walls


def walls_ray_cast(player, textures):
    casted_walls = ray_casting(player.pos, player.angle, world_map)
    walls = []
    for ray, casted_values in enumerate(casted_walls):
        depth, offset, proj_height, texture = casted_values
        if proj_height > HEIGHT:
            coeff = proj_height / HEIGHT
            texture_height = TEXTURE_HEIGHT / coeff
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE,
                                                       TEXTURE_HEIGHT // 2 - texture_height // 2, TEXTURE_SCALE,
                                                       texture_height)
            wall_column = pygame.transform.scale(wall_column, (SCALE, HEIGHT))
            wall_pos = (ray * SCALE, 0)
        else:
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE, TEXTURE_WIDTH)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            wall_pos = (ray * SCALE, H_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
    return walls
