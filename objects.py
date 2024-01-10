import pygame
from config import *


class SpriteObject:
    def __init__(self, obj, static, pos, shift, scale):
        self.obj = obj
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

        if not static:
            self.angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.positions = {angle: pos for angle, pos in zip(self.angles, self.obj)}

    def object_locate(self, player, walls):
        fake_walls = [walls[0] for _ in range(FAKE_RAYS)] + walls + [walls[-1] for _ in range(FAKE_RAYS)]

        dx, dy = self.x - player.x, self.y - player.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI

        delta_rays = int(gamma / DELTA_A)
        current_ray = CENTER_RAY + delta_rays
        distance *= math.cos(H_FOV - current_ray * DELTA_A)

        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= NUM_RAYS - 1 + 2 * FAKE_RAYS and distance < fake_walls[fake_ray][0]:
            proj_height = int(PROJ_COEFF / distance * self.scale)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if not self.static:
                if theta <= 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angle in self.angles:
                    if theta in angle:
                        self.obj = self.positions[angle]
                        break

            sprite_pos = (current_ray * SCALE - half_proj_height, H_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(self.obj, (proj_height, proj_height))
            return distance, sprite, sprite_pos
        return (False,)


class Sprites:
    def __init__(self):
        self.sprite_types = {
            'barrel': pygame.image.load('sprites/barrel/frame_0.png').convert_alpha(),
            'column': pygame.image.load('sprites/flambeau/frame_0.png').convert_alpha(),
            'cacodemon': [pygame.image.load(f'sprites/cacodemon/state_{i}.png').convert_alpha() for i in range(8)]
        }
        self.list_of_objects = [
            SpriteObject(self.sprite_types['barrel'], True, (2.2, 3), 1.5, 0.5),
            SpriteObject(self.sprite_types['barrel'], True, (2.2, 5), 1.5, 0.5),
            SpriteObject(self.sprite_types['column'], True, (9.8, 3), 1.5, 0.5),
            SpriteObject(self.sprite_types['column'], True, (9.8, 5), 1.5, 0.5),
            SpriteObject(self.sprite_types['cacodemon'], False, (9, 4), 0.2, 1)
        ]
