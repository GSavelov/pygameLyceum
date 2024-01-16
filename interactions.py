from math import sin, cos
import pygame.mixer
from numba import njit
from config import *
from rayCasting import mapping


@njit(fastmath=True, cache=True)
def ray_cast_npc(npc_x, npc_y, world_map, doors, p_pos):
    ox, oy = p_pos
    xm, ym = mapping(ox, oy)
    delta_x, delta_y = ox - npc_x, oy - npc_y
    cur_angle = math.atan2(delta_y, delta_x)
    cur_angle += math.pi

    sin_a = sin(cur_angle)
    sin_a = sin_a if sin_a else 0.000001
    cos_a = cos(cur_angle)
    cos_a = cos_a if cos_a else 0.000001

    x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
    for i in range(0, int(abs(delta_x)) // TILE):
        depth_v = (x - ox) / cos_a
        yv = oy + depth_v * sin_a
        tile_v = mapping(x + dx, yv)
        if tile_v in world_map or tile_v in doors:
            return False
        x += dx * TILE

    y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
    for i in range(0, int(abs(delta_y)) // TILE):
        depth_h = (y - oy) / sin_a
        xh = ox + depth_h * cos_a
        tile_h = mapping(xh, y + dy)
        if tile_h in world_map or tile_h in doors:
            return False
        y += dy * TILE
    return True


class Interaction:
    def __init__(self, player, sprites, drawing, world_map):
        self.player = player
        self.world_map = world_map
        self.sprites = sprites
        self.drawing = drawing
        self.death_sound = pygame.mixer.Sound('sounds/death.mp3')

    def interaction_objects(self):
        if self.player.shot and self.drawing.shot_anim_trigger:
            for obj in sorted(self.sprites.list_of_objects, key=lambda object: object.distance):
                if obj.on_fire[1]:
                    if obj.is_dead != 'immortal' and not obj.is_dead:
                        if ray_cast_npc(obj.x, obj.y, self.world_map, self.sprites.blocked_doors, self.player.pos):
                            if obj.flag == 'npc':
                                self.death_sound.play()
                            obj.is_dead = True
                            obj.blocked = None
                            self.drawing.shot_anim_trigger = False
                    if obj.flag in {'door_v', 'door_h'} and obj.distance < TILE:
                        obj.door_open_trigger = True
                        obj.blocked = None
                    break

    def npc_action(self):
        for obj in self.sprites.list_of_objects:
            if obj.flag == 'npc' and not obj.is_dead:
                if ray_cast_npc(obj.x, obj.y, self.world_map, self.sprites.blocked_doors, self.player.pos):
                    obj.npc_action_trigger = True
                    self.npc_move(obj)
                else:
                    obj.npc_action_trigger = False

    def npc_move(self, obj):
        if obj.distance > TILE:
            dx = obj.x - self.player.pos[0]
            dy = obj.y - self.player.pos[1]
            obj.x = obj.x + 1 if dx < 0 else obj.x - 1
            obj.y = obj.y + 1 if dy < 0 else obj.y - 1

    def clear(self):
        deleted_objects = self.sprites.list_of_objects[:]
        [self.sprites.list_of_objects.remove(obj) for obj in deleted_objects if obj.delete]

    def mixer_init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.load("sounds/Aubrey Hodges - Retribution Dawns.mp3")

    def check_end(self):
        if not [obj for obj in self.sprites.list_of_objects if obj.flag == 'npc' and not obj.is_dead]:
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()
            pygame.mixer.music.load('sounds/Aubrey Hodges - Retribution Dawns.mp3')
            pygame.mixer.music.play(10)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                self.drawing.win()
