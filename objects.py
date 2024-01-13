import pygame
from config import *
from collections import deque


class SpriteObject:
    def __init__(self, parameters, pos):
        self.obj = parameters['sprite']
        self.view_angles = parameters['view_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.anim_dist = parameters['anim_dist']
        self.anim_speed = parameters['anim_speed']
        self.blocked = parameters['blocked']
        self.side = 25
        self.anim_count = 0
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.pos = self.x - self.side // 2, self.y - self.side // 2

        if self.view_angles:
            self.angles = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.positions = {angle: pos for angle, pos in zip(self.angles, self.obj)}

    def object_locate(self, player):
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
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance > 30:
            proj_height = min(int(PROJ_COEFF / distance * self.scale), D_HEIGHT)
            # Ограничение проекционной высоты спрайта (В ином случае при приближении падает fps)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift

            if self.view_angles:
                if theta <= 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))

                for angle in self.angles:
                    if theta in angle:
                        self.obj = self.positions[angle]
                        break
            # TODO: Исправить не статичные спрайты с анимацией
            sprite_object = self.obj
            if self.animation and distance < self.anim_dist:
                sprite_object = self.animation[0]
                if self.anim_count < self.anim_speed:
                    self.anim_count += 1
                else:
                    self.animation.rotate()
                    self.anim_count = 0
            """Анимация спрайтов
            
            Используется массив deque из built-in библиотеки collections,
            так как умеет крайне быстро перемещать первый элемент в конец
            массива.
            """

            sprite_pos = (current_ray * SCALE - half_proj_height, H_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_object, (proj_height, proj_height))
            return distance, sprite, sprite_pos
        return (False,)


class Sprites:
    def __init__(self):
        self.sprites = {
            'barrel': {
                'sprite': pygame.image.load('sprites/barrel/barrel.png').convert_alpha(),
                'view_angles': None,
                'shift': 1.5,
                'scale': 0.4,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/animation/img_{i}.png') for i in range(12)]),
                'anim_dist': 800,
                'anim_speed': 10,
                'blocked': True

            },
            'cacodemon': {
                'sprite': [pygame.image.load(f'sprites/cacodemon/state_{i}.png').convert_alpha() for i in range(8)],
                'view_angles': True,
                'shift': 0.1,
                'scale': 1,
                'animation': deque(
                    [pygame.image.load(f'sprites/cacodemon/animation/img_{i}.png') for i in range(9)]),
                'anim_dist': 800,
                'anim_speed': 20,
                'blocked': True

            },
            'flambeau': {
                'sprite': pygame.image.load('sprites/flambeau/flambeau.png').convert_alpha(),
                'view_angles': None,
                'shift': 1.5,
                'scale': 0.5,
                'animation': None,
                'anim_dist': 800,
                'anim_speed': 10,
                'blocked': True
            },
            'orb': {
                'sprite': pygame.image.load('sprites/orb/orb.png').convert_alpha(),
                'view_angles': None,
                'shift': 0.1,
                'scale': 0.5,
                'animation': deque(
                    [pygame.image.load(f'sprites/orb/animation/img_{i}.png') for i in range(8)]),
                'anim_dist': 800,
                'anim_speed': 20,
                'blocked': True
            }

        }

        self.list_of_objects = [
            SpriteObject(self.sprites['barrel'], (2.2, 3)),
            SpriteObject(self.sprites['barrel'], (2.2, 5)),
            SpriteObject(self.sprites['cacodemon'], (10, 5.5)),
            SpriteObject(self.sprites['flambeau'], (10.9, 4)),
            SpriteObject(self.sprites['flambeau'], (10.9, 7)),
            SpriteObject(self.sprites['orb'], (2.2, 4))
        ]
