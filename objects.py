import pygame
from config import *


class SpriteObject:
    def __init__(self, obj, static, pos, shift, scale):
        self.obj = obj
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        dx, dy = self.x - player.x, self.y - player.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_A)
        current_ray = CENTER_RAY + delta_rays
        distance *= math.cos(H_FOV - current_ray * DELTA_A)

        if 0 <= current_ray < NUM_RAYS - 1 and distance < walls[current_ray][0]:
            proj_height = int(PROJ_COEFF / distance * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            sprite_pos = (current_ray * SCALE - half_proj_height, H_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.obj, (proj_height, proj_height))
            return distance, sprite, sprite_pos
        return (False,)


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'rock': pygame.image.load('sprites/rock.png').convert_alpha()
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['rock'], True, (3, 3), 2, 0.4),
            SpriteObject(self.sprite_types['rock'], True, (5, 5), 2, 0.4)
        ]
