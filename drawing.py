import sys
from random import randrange
from objects import *


class Drawing:
    def __init__(self, surface, map_surface, player, clock, mini_map, select):
        self.surface = surface
        self.mini_map = mini_map
        self.map_surface = map_surface
        self.player = player
        self.clock = clock
        self.font = pygame.font.Font(None, 36)
        self.label_font = pygame.font.Font('fonts/better-vcr-5.4.ttf', 150)
        self.score_font = pygame.font.Font('fonts/better-vcr-5.4.ttf', 20)
        if select == 'level_1':
            skybox = pygame.image.load('textures/skybox.png').convert()
        else:
            skybox = pygame.image.load('textures/doom_skybox.png').convert()
        self.textures = {1: pygame.image.load('textures/brick_wall.png').convert(),
                         2: pygame.image.load('textures/brick_moss_wall.png').convert(),
                         3: pygame.image.load('textures/doom_brick_wall.png').convert(),
                         4: pygame.image.load('textures/doom_metal_wall.png').convert(),
                         5: pygame.image.load('textures/doom_metal_sheet_wall.png').convert(),
                         's': skybox}
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
            elif obj.flag == 'door_v':
                pygame.draw.rect(self.map_surface, 'red', (npc_x - 2.5, npc_y - 5, 100 // MAP_SCALE, 50 // MAP_SCALE))
            elif obj.flag == 'door_h':
                pygame.draw.rect(self.map_surface, 'red', (npc_x - 2.5, npc_y - 5, 50 // MAP_SCALE, 100 // MAP_SCALE))
            else:
                pygame.draw.circle(self.map_surface, 'red', (npc_x, npc_y), 2)

        for x, y in self.mini_map:
            pygame.draw.rect(self.map_surface, MAP_COLOR, (x, y, MAP_TILE, MAP_TILE), 5)
        self.surface.blit(self.map_surface, MAP_DRAW_POS)

    def weapon(self, shots):
        if self.player.shot:
            if not self.shot_length_count and self.sfx_length_count % self.shot_anim_speed == 0:
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

    def win(self, score):
        render = self.label_font.render('you win!', 1, (randrange(150, 200), 0, 0))
        score_render = self.score_font.render('Score: ' + str(round(score)), 1, 'white')
        rect = pygame.Rect(0, 0, 1000, 250)
        rect.center = H_WIDTH, H_HEIGHT
        pygame.draw.rect(self.surface, 'black', rect, border_radius=10)
        self.surface.blit(render, (rect.centerx - 430, rect.centery - 90))
        self.surface.blit(score_render, (500, 480))
        pygame.display.flip()
        self.clock.tick(15)


class MenuDrawing:
    def __init__(self, surface, clock):
        self.surface = surface
        self.clock = clock
        self.button_font = pygame.font.Font('fonts/better-vcr-5.4.ttf', 100)
        self.label_font = pygame.font.Font('fonts/better-vcr-5.4.ttf', 150)
        self.score_font = pygame.font.Font('fonts/better-vcr-5.4.ttf', 25)
        self.menu_pic = pygame.image.load('textures/menu.png').convert()
        self.menu_trigger = True
        self.select = 'level_1'

    def mixer_init(self):
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.load('sounds/Aubrey Hodges - Retribution Dawns.mp3')

    def draw_buttons(self, button, shift_h, shift_v, text, color, font, width=0, selected=False):
        if selected:
            field = font.render(text, 1, 'red')
        else:
            field = font.render(text, 1, color)
        pygame.draw.rect(self.surface, 'black', button, border_radius=20, width=width)
        self.surface.blit(field, (button.centerx - shift_h, button.centery - shift_v))

    def menu(self):
        with open('levels/score.txt', 'r') as score:
            last_score = round(float(score.readline().strip()))

        button_start = pygame.Rect(0, 0, 400, 150)
        button_start.center = H_WIDTH, H_HEIGHT
        button_exit = pygame.Rect(0, 0, 400, 150)
        button_exit.center = H_WIDTH, H_HEIGHT + 200

        button_level_1 = pygame.Rect(0, 0, 180, 50)
        button_level_1.center = 490, 280
        button_level_2 = pygame.Rect(0, 0, 180, 50)
        button_level_2.center = 710, 280

        pygame.mixer.music.play()

        while self.menu_trigger:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            self.surface.blit(self.menu_pic, (0, 0))

            if self.select == 'level_1':
                self.draw_buttons(button_level_1, 50, 10, 'Earth', 'white', self.score_font, selected=True)
                self.draw_buttons(button_level_2, 40, 10, 'Mars', 'white', self.score_font)
            else:
                self.draw_buttons(button_level_1, 50, 10, 'Earth', 'white', self.score_font)
                self.draw_buttons(button_level_2, 40, 10, 'Mars', 'white', self.score_font, selected=True)

            self.draw_buttons(button_start, 185, 50, 'START', 'white', self.button_font)
            self.draw_buttons(button_exit, 150, 50, 'EXIT', 'white', self.button_font)

            label = self.label_font.render('PyDOOM', 1, (randrange(150, 200), 0, 0))
            self.surface.blit(label, (280, 70))

            score = self.score_font.render('Last score:' + str(last_score), 1, 'white')
            self.surface.blit(score, (50, 20))

            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()
            if button_start.collidepoint(mouse_pos):
                self.draw_buttons(button_start, 185, 40, 'START', (randrange(150, 200), 0, 0), self.button_font)
                if mouse_click[0]:
                    self.menu_trigger = False
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sounds/3D0 Doom - At Doom's Gate.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(10, 0.0, 5000)
            elif button_exit.collidepoint(mouse_pos):
                self.draw_buttons(button_exit, 150, 40, 'EXIT', (randrange(150, 200), 0, 0), self.button_font)
                if mouse_click[0]:
                    pygame.quit()
                    sys.exit()
            elif button_level_1.collidepoint(mouse_pos):
                if mouse_click[0]:
                    self.select = 'level_1'
            elif button_level_2.collidepoint(mouse_pos):
                if mouse_click[0]:
                    self.select = 'level_2'

            pygame.display.flip()
            self.clock.tick(10)
