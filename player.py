import pygame
from math import cos, sin
from config import *


class Player:
    def __init__(self, sprites, collisions):
        self.x, self.y = player_pos
        self.wall_collisions = collisions
        self.sprites = sprites
        self.angle = player_angle
        self.sensitivity = 0.002
        """Collision"""
        self.side = 50
        self.rect = pygame.Rect(*player_pos, self.side, self.side)
        """Weapon"""
        self.shot = False

    @property
    def pos(self):
        return self.x, self.y

    @property
    def collision_list(self):
        return self.wall_collisions + [pygame.Rect(*obj.pos, obj.side, obj.side) for obj in self.sprites.list_of_objects if
                                  obj.blocked]

    def check_collision(self, dx, dy):
        next_step = self.rect.copy()
        next_step.move_ip(dx, dy)
        hits = next_step.collidelistall(self.collision_list)

        if hits:
            delta_x, delta_y = 0, 0
            for hit in hits:
                hit_rect = self.collision_list[hit]
                if dx > 0:
                    delta_x += next_step.right - hit_rect.left
                else:
                    delta_x += hit_rect.right - next_step.left
                if dy > 0:
                    delta_y += next_step.bottom - hit_rect.top
                else:
                    delta_y += hit_rect.bottom - next_step.top

            if abs(delta_x - delta_y) < 10:
                dx, dy = 0, 0
            elif delta_x > delta_y:
                dy = 0
            elif delta_y > delta_x:
                dx = 0

        self.x += dx
        self.y += dy

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.rect.center = self.x, self.y
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx = player_speed * cos_a
            dy = player_speed * sin_a
            self.check_collision(dx, dy)
        if keys[pygame.K_s]:
            dx = - player_speed * cos_a
            dy = - player_speed * sin_a
            self.check_collision(dx, dy)
        if keys[pygame.K_a]:
            dx = player_speed * sin_a
            dy = - player_speed * cos_a
            self.check_collision(dx, dy)
        if keys[pygame.K_d]:
            dx = - player_speed * sin_a
            dy = player_speed * cos_a
            self.check_collision(dx, dy)

    def mouse_control(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - H_WIDTH
            pygame.mouse.set_pos((H_WIDTH, H_HEIGHT))
            self.angle += diff * self.sensitivity
