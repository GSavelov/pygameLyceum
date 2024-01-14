from objects import *
from map import mini_map


class Drawing:
    def __init__(self, surface, map_surface, player):
        self.surface = surface
        self.map_surface = map_surface
        self.player = player
        self.font = pygame.font.Font(None, 36)
        self.textures = {1: pygame.image.load('textures/brick_wall.png').convert(),
                         2: pygame.image.load('textures/brick_moss_wall.png').convert(),
                         3: pygame.image.load('textures/doom_brick_wall.png').convert(),
                         4: pygame.image.load('textures/doom_metal_wall.png').convert(),
                         5: pygame.image.load('textures/doom_metal_sheet_wall.png').convert(),
                         's': pygame.image.load('textures/doom_skybox.png').convert()}
        """Отрисовка оружия"""
        self.w_base_sprite = pygame.image.load('sprites/shooting/shotgun.png').convert_alpha()
        self.w_shot_animation = deque([pygame.image.load(f'sprites/shooting/shotgun/img_{i}.png') for i in range(20)])
        self.w_rect = self.w_base_sprite.get_rect()
        self.w_pos = (H_WIDTH - self.w_rect.width // 2, HEIGHT - self.w_rect.height)
        self.shot_length = len(self.w_shot_animation)
        self.shot_length_count = 0
        self.shot_anim_speed = 4
        self.shot_anim_count = 0
        self.shot_anim_trigger = True
        self.shot_sound = pygame.mixer.Sound('sounds/shotgun.mp3')
        """Свойства эффекта выстрела"""
        self.sfx = deque([pygame.image.load(f'sprites/shooting/sfx/img_{i}.png') for i in range(9)])
        self.sfx_length_count = 0
        self.sfx_length = len(self.sfx)

    def background(self, angle):
        offset = -5 * math.degrees(angle) % WIDTH
        self.surface.blit(self.textures['s'], (offset, 0))
        self.surface.blit(self.textures['s'], (offset + WIDTH, 0))
        self.surface.blit(self.textures['s'], (offset - WIDTH, 0))
        pygame.draw.rect(self.surface, DARKGRAY, (0, H_HEIGHT, WIDTH, H_HEIGHT))

    def world(self, world_objects):
        for obj in sorted(world_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.surface.blit(object, object_pos)

    def fps(self, clock):
        fps = str(int(clock.get_fps()))
        render = self.font.render(fps, 0, 'green')
        self.surface.blit(render, FPS_DRAW_POS)

    def minimap(self, player, npc):
        self.map_surface.fill('black')
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE
        pygame.draw.circle(self.map_surface, MAP_COLOR, (map_x, map_y), 5)
        pygame.draw.line(self.map_surface, MAP_COLOR, (map_x, map_y), (map_x + 10 * math.cos(player.angle),
                                                                       map_y + 10 * math.sin(player.angle)))
        for obj in npc:
            npc_x, npc_y = obj.x // MAP_SCALE, obj.y // MAP_SCALE
            if obj.flag == 'npc' and not obj.is_dead:
                pygame.draw.circle(self.map_surface, 'green', (npc_x, npc_y), 2)
            elif obj.flag == 'npc' and obj.is_dead:
                pygame.draw.circle(self.map_surface, PALEGREEN, (npc_x, npc_y), 2)
        for x, y in mini_map:
            pygame.draw.rect(self.map_surface, MAP_COLOR, (x, y, MAP_TILE, MAP_TILE), 5)
        self.surface.blit(self.map_surface, MAP_DRAW_POS)

    def weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count:
                self.shot_sound.play()
            self.shot_proj = min(shots)[1] // 2
            self.bullet_sfx()
            shot_sprite = self.w_shot_animation[0]
            self.surface.blit(shot_sprite, self.w_pos)
            self.shot_anim_count += 1
            if self.shot_anim_count == self.shot_anim_speed:
                self.w_shot_animation.rotate(-1)
                self.shot_anim_count = 0
                self.shot_length_count += 1
                self.shot_anim_trigger = False
            if self.shot_length_count == self.shot_length:
                self.player.shot = False
                self.shot_length_count = 0
                self.sfx_length_count = 0
                self.shot_anim_trigger = True
        else:
            self.surface.blit(self.w_base_sprite, self.w_pos)

    def bullet_sfx(self):
        if self.sfx_length_count < self.sfx_length:
            sfx = pygame.transform.scale(self.sfx[0], (self.shot_proj, self.shot_proj))
            sfx_rect = sfx.get_rect()
            self.surface.blit(sfx, (H_WIDTH - sfx_rect.width // 2, H_HEIGHT - sfx_rect.height // 2))
            self.sfx_length_count += 1
            self.sfx.rotate(-1)
