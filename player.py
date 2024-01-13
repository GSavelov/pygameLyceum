import pygame
from math import cos, sin
from config import *


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.sensitivity = 0.002

    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
        if keys[pygame.K_s]:
            self.x += - player_speed * cos_a
            self.y += - player_speed * sin_a
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += - player_speed * cos_a
        if keys[pygame.K_d]:
            self.x += - player_speed * sin_a
            self.y += player_speed * cos_a

    def mouse_control(self):
        if pygame.mouse.get_focused():
            diff = pygame.mouse.get_pos()[0] - H_WIDTH
            pygame.mouse.set_pos((H_WIDTH, H_HEIGHT))
            self.angle += diff * self.sensitivity
