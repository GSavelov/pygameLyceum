import pygame
import csv
from config import *
from collections import deque
from rayCasting import mapping
from numba.core import types
from numba.typed import Dict
from numba import int32


class SpriteObject:
    def __init__(self, parameters, pos):
        # --- base sprite parameters ---
        self.obj = parameters['sprite'].copy()
        self.view_angles = parameters['view_angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        # --- death parameters ---
        self.death_anim = parameters['death_anim'].copy()
        self.is_dead = parameters['is_dead']
        self.dead_shift = parameters['dead_shift']
        # --- animation parameters ---
        self.animation = parameters['animation'].copy()
        self.anim_dist = parameters['anim_dist']
        self.anim_speed = parameters['anim_speed']
        self.anim_count = 0
        # --- other parameters ---
        self.flag = parameters['flag']
        self.action = parameters['action'].copy()
        self.blocked = parameters['blocked']
        self.side = parameters['side']
        self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.death_anim_count = 0
        self.npc_action_trigger = False
        self.door_open_trigger = False
        self.delete = False
        self.prev_door_pos = self.y if self.flag == 'door_h' else self.y
        self.door_open_sound = pygame.mixer.Sound('sounds/door_open.mp3')
        if self.view_angles:
            if len(self.obj) == 8:
                self.angles = [frozenset(range(338, 360)) | frozenset(range(0, 23))] + \
                              [frozenset(range(i, i + 45)) for i in range(23, 338, 45)]
                # Fixed: углы осмотра спрайта
            else:
                self.angles = [frozenset(range(348, 361)) | frozenset(range(0, 11))] + \
                              [frozenset(range(i, i + 23)) for i in range(11, 348, 23)]
            self.positions = {angle: pos for angle, pos in zip(self.angles, self.obj)}

    @property
    def on_fire(self):
        if CENTER_RAY - self.side // 2 < self.current_ray < CENTER_RAY + self.side // 2 and self.blocked:
            return self.distance, self.proj_height
        return float('inf'), None

    @property
    def pos(self):
        return self.x - self.side // 2, self.y - self.side // 2

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        self.distance = math.sqrt(dx ** 2 + dy ** 2)

        self.theta = math.atan2(dy, dx)
        gamma = self.theta - player.angle

        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        self.theta -= 1.4 * gamma

        delta_rays = int(gamma / DELTA_A)
        self.current_ray = CENTER_RAY + delta_rays
        if self.flag not in {'door_v', 'door_h'}:
            self.distance *= math.cos(H_FOV - self.current_ray * DELTA_A)

        fake_ray = self.current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and self.distance > 30:
            self.proj_height = min(int(PROJ_COEFF / self.distance),
                                   D_HEIGHT if self.flag not in {'door_v', 'door_h'} else HEIGHT)
            # Ограничение проекционной высоты спрайта (В ином случае при приближении падает fps)
            sprite_width = int(self.proj_height * self.scale[0])
            sprite_height = int(self.proj_height * self.scale[1])
            half_sprite_width = sprite_width // 2
            half_sprite_height = sprite_height // 2
            shift = half_sprite_height * self.shift

            if self.flag in {'door_v', 'door_h'}:
                if self.door_open_trigger:
                    self.open_door()
                self.obj = self.sprite_view()
                sprite_object = self.sprite_animation()
            else:
                if self.is_dead and self.is_dead != 'immortal':
                    sprite_object = self.dead_animation()
                    shift = half_sprite_height * self.dead_shift
                    sprite_height = int(sprite_height / 1.3)
                elif self.npc_action_trigger:
                    sprite_object = self.npc_action()
                else:
                    self.obj = self.sprite_view()
                    sprite_object = self.sprite_animation()

            sprite_pos = (self.current_ray * SCALE - half_sprite_width, H_HEIGHT - half_sprite_height + shift)
            sprite = pygame.transform.scale(sprite_object, (sprite_width, sprite_height))
            return self.distance, sprite, sprite_pos
        return (False,)

    def sprite_animation(self):
        if self.animation and self.distance < self.anim_dist:
            sprite_object = self.animation[0]
            if self.anim_count < self.anim_speed:
                self.anim_count += 1
            else:
                self.animation.rotate()
                self.anim_count = 0
            return sprite_object
        return self.obj

    def sprite_view(self):
        if self.view_angles:
            if self.theta <= 0:
                self.theta += DOUBLE_PI
            self.theta = 360 - int(math.degrees(self.theta))

            for angle in self.angles:
                if self.theta in angle:
                    return self.positions[angle]
        return self.obj

    def dead_animation(self):
        if len(self.death_anim):
            if self.death_anim_count < self.anim_speed:
                self.dead_sprite = self.death_anim[0]
                self.death_anim_count += 1
            else:
                self.dead_sprite = self.death_anim.popleft()
                self.death_anim_count = 0
        return self.dead_sprite

    def npc_action(self):
        sprite_object = self.action[0]
        if self.anim_count < self.anim_speed:
            self.anim_count += 1
        else:
            self.action.rotate()
            self.anim_count = 0
        return sprite_object

    def open_door(self):
        self.door_open_sound.play()
        if self.flag == 'door_h':
            self.y -= 3
            if abs(self.y - self.prev_door_pos) > TILE:
                self.delete = True
        elif self.flag == 'door_v':
            self.x -= 3
            if abs(self.x - self.prev_door_pos) > TILE:
                self.delete = True


class Sprites:
    def __init__(self):
        self.sprites = {
            'barrel': {
                'sprite': pygame.image.load('sprites/barrel/barrel.png').convert_alpha(),
                'view_angles': None,
                'shift': 1.5,
                'scale': (0.4, 0.4),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/barrel/animation/img_{i}.png') for i in range(12)]),
                'death_anim': deque(
                    [pygame.image.load(f'sprites/barrel/death_anim/img_{i}.png') for i in range(4)]),
                'is_dead': None,
                'dead_shift': 2.6,
                'anim_dist': 800,
                'anim_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'action': []

            },
            'cacodemon': {
                'sprite': [pygame.image.load(f'sprites/cacodemon/state_{i}.png').convert_alpha() for i in range(8)],
                'view_angles': True,
                'shift': 0.1,
                'scale': (1, 1),
                'side': 50,
                'animation': [],
                'death_anim': deque(
                    [pygame.image.load(f'sprites/cacodemon/death_anim/img_{i}.png') for i in range(6)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'anim_dist': 400,
                'anim_speed': 20,
                'blocked': True,
                'flag': 'npc',
                'action': deque(
                    [pygame.image.load(f'sprites/cacodemon/animation/img_{i}.png') for i in range(9)])
            },
            'soldier': {
                'sprite': [pygame.image.load(f'sprites/soldier/img_{i}.png').convert_alpha() for i in range(8)],
                'view_angles': True,
                'shift': 0.5,
                'scale': (0.4, 0.7),
                'side': 50,
                'animation': [],
                'death_anim': deque(
                    [pygame.image.load(f'sprites/soldier/death_anim/img_{i}.png') for i in range(10)]),
                'is_dead': None,
                'dead_shift': 0.6,
                'anim_dist': 800,
                'anim_speed': 20,
                'blocked': True,
                'flag': 'npc',
                'action': deque(
                    [pygame.image.load(f'sprites/soldier/animation/img_{i}.png') for i in range(4)])
            },
            'flambeau': {
                'sprite': pygame.image.load('sprites/flambeau/flambeau.png').convert_alpha(),
                'view_angles': None,
                'shift': 1.5,
                'scale': (0.5, 0.5),
                'side': 30,
                'animation': [],
                'death_anim': [],
                'is_dead': 'immortal',
                'dead_shift': None,
                'anim_dist': 800,
                'anim_speed': 10,
                'blocked': True,
                'flag': 'decor',
                'action': []
            },
            'orb': {
                'sprite': pygame.image.load('sprites/orb/orb.png').convert_alpha(),
                'view_angles': None,
                'shift': 0.1,
                'scale': (0.5, 0.5),
                'side': 30,
                'animation': deque(
                    [pygame.image.load(f'sprites/orb/animation/img_{i}.png') for i in range(8)]),
                'death_anim': [],
                'is_dead': 'immortal',
                'dead_shift': None,
                'anim_dist': 800,
                'anim_speed': 20,
                'blocked': True,
                'flag': 'decor',
                'action': []
            },
            'door_v': {
                'sprite': [pygame.image.load(f'sprites/doors/vertical/img_{i}.png').convert_alpha() for i in range(16)],
                'view_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_anim': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'anim_dist': 0,
                'anim_speed': 0,
                'blocked': True,
                'flag': 'door_h',
                'action': deque([pygame.image.load('sprites/soldier/img_0.png').convert_alpha()])
            },
            'door_h': {
                'sprite': [pygame.image.load(f'sprites/doors/horizontal/img_{i}.png').convert_alpha() for i in
                           range(16)],
                'view_angles': True,
                'shift': 0.1,
                'scale': (2.6, 1.2),
                'side': 100,
                'animation': [],
                'death_anim': [],
                'is_dead': 'immortal',
                'dead_shift': 0,
                'anim_dist': 0,
                'anim_speed': 0,
                'blocked': True,
                'flag': 'door_v',
                'action': []
            }
        }

        self.list_of_objects = []

    def load_objects(self, name):
        with open('levels/' + name + '.csv', encoding='utf-8') as objects:
            data = list(csv.reader(objects, delimiter=';'))
            self.list_of_objects = [SpriteObject(self.sprites[key], tuple(map(float, pos.split(', ')))) for key, pos in
                                    data]

    @property
    def shot(self):
        return min([obj.on_fire for obj in self.list_of_objects], default=(float('inf'), 0))

    @property
    def blocked_doors(self):
        blocked_doors = Dict.empty(key_type=types.UniTuple(int32, 2), value_type=int32)
        for obj in self.list_of_objects:
            if obj.flag in {'door_h', 'door_v'} and obj.blocked:
                i, j = mapping(obj.x, obj.y)
                blocked_doors[(i, j)] = 0
        return blocked_doors
