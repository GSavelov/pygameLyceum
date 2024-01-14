import pygame
from math import sin, cos
from numba import njit
from config import *
from map import world_map
from rayCasting import mapping


@njit(fastmath=True, cache=True)
def ray_cast_npc(npc_x, npc_y, world_map, p_pos):
    ox, oy = p_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = sin(cur_angle)
    cos_a = cos(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = cos_a if cos_a else 0.000001

    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map:
            return False
        x += dx * TILE

    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing):
        self.player = player
        self.sprites = sprites
        self.drawing = drawing

    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_anim_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda obj: obj.distance):
                if obj.on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_cast_npc(obj.x, obj.y, world_map, self.player.pos):
                            obj.is_dead = True
                            obj.blocked = None
                            self.drawing.shot_anim_trigger = False
                    break
