import pygame.image

import settings
from support import import_folder
from settings import vertical_tile_number, tile_size, screen_width, screen_height
from tiles import CloudTile, Static_centerTile

from random import choice, randint

class Background:
    def __init__(self, screen, image_path):
        self.screen = screen
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image.set_alpha(150)
        self.rect = self.image.get_rect()
        self.orig_pos = pygame.math.Vector2(self.screen.get_rect().center)
        self.rect.center = self.orig_pos

        self.swipe_distance = 15
        self.swipe_speed = 4

        self.swipe_x_stage_1 = False
        self.swipe_x_stage_2 = False
        self.swipe_x = 0
        self.swipe_x_direction = None

        self.swipe_y_stage_1 = False
        self.swipe_y_stage_2 = False
        self.swipe_y = 0
        self.swipe_y_direction = None

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def __make_shift_x(self):
        additional_offset = 15
        additional_speed = 2
        if self.swipe_x_stage_1 and self.swipe_x_direction == "right":
            if self.swipe_x < (self.swipe_distance+additional_offset):
                self.swipe_x += self.swipe_speed+additional_speed
                self.rect.centerx += self.swipe_speed+additional_speed

            else:
                self.swipe_x_stage_1 = False
                self.swipe_x_stage_2 = True
                self.swipe_x_direction = "left"

        elif self.swipe_x_stage_1 and self.swipe_x_direction == "left":
            if self.swipe_x > (self.swipe_distance+additional_offset)*-1:
                self.swipe_x -= self.swipe_speed+additional_speed
                self.rect.centerx -= self.swipe_speed+additional_speed
            else:
                self.swipe_x_stage_1 = False
                self.swipe_x_stage_2 = True
                self.swipe_x_direction = "right"

        if self.swipe_x_stage_2 and self.swipe_x_direction == "left":
            if self.swipe_x >= 0:
                self.swipe_x -= self.swipe_speed+additional_speed
                self.rect.centerx -= self.swipe_speed+additional_speed
            else:
                self.rect.centerx = self.orig_pos.x
                self.swipe_x_stage_2 = False
                self.swipe_x = 0
                self.swipe_x_direction = None
        elif self.swipe_x_stage_2 and self.swipe_x_direction == "right":

            if self.swipe_x <= 0:
                self.swipe_x += self.swipe_speed+additional_speed
                self.rect.centerx += self.swipe_speed+additional_speed
            else:
                self.rect.centerx = self.orig_pos.x
                self.swipe_x_stage_2 = False
                self.swipe_x = 0
                self.swipe_x_direction = None


    def __make_shift_y(self):
        if self.swipe_y_stage_1 and self.swipe_y_direction == "up":
            if self.swipe_y > self.swipe_distance*-1:
                self.swipe_y -= self.swipe_speed
                self.rect.centery -= self.swipe_speed

            else:
                self.swipe_y_stage_1 = False
                self.swipe_y_stage_2 = True
                self.swipe_y_direction = "down"

        elif self.swipe_y_stage_1 and self.swipe_y_direction == "down":
            if self.swipe_y < self.swipe_distance:
                self.swipe_y += self.swipe_speed
                self.rect.centery += self.swipe_speed
            else:
                self.swipe_y_stage_1 = False
                self.swipe_y_stage_2 = True
                self.swipe_y_direction = "up"

        if self.swipe_y_stage_2 and self.swipe_y_direction == "up":
            if self.swipe_y >= 0:
                self.swipe_y -= self.swipe_speed
                self.rect.centery -= self.swipe_speed
            else:
                self.rect.centery = self.orig_pos.y
                self.swipe_y_stage_2 = False
                self.swipe_y = 0
                self.swipe_y_direction = None

        elif self.swipe_y_stage_2 and self.swipe_y_direction == "down":
            if self.swipe_y <= 0:
                self.swipe_y += self.swipe_speed
                self.rect.centery += self.swipe_speed
            else:
                self.rect.centery = self.orig_pos.y
                self.swipe_y_stage_2 = False
                self.swipe_y = 0
                self.swipe_y_direction = None

    def make_swipe_x(self, direction: str):
        if not self.swipe_x_stage_1 and not self.swipe_x_stage_2:
            self.swipe_x_stage_1 = True
            self.swipe_x_direction = direction


    def make_swipe_y(self, direction: str):
        if not self.swipe_y_stage_1 and not self.swipe_y_stage_2:
            self.swipe_y_stage_1 = True
            self.swipe_y_direction = direction

    def update(self):
        if self.swipe_x_stage_1 or self.swipe_x_stage_2:
            self.__make_shift_x()

        if self.swipe_y_stage_1 or self.swipe_y_stage_2:
            self.__make_shift_y()

        self.draw()

class Clouds:
    def __init__(self, horizon, level_width, clouds_quantity):
        self.cloud_surf_list = import_folder('../graphics/decoration/clouds')
        self.min_x = -screen_width
        self.max_x = level_width + 500
        self.min_y = -tile_size * 2
        self.max_y = horizon * tile_size
        self.current_x = 0

        self.cloud_sprites = pygame.sprite.Group()
        self.new_cloud(clouds_quantity)

    def new_cloud(self, clouds_quantity, min_x=None):
        if min_x:
            my_min_x = min_x
        else:
            my_min_x = self.min_x
        for cloud in range(clouds_quantity):
            cloud = choice(self.cloud_surf_list)
            x = randint(my_min_x, self.max_x)
            y = randint(self.min_y, self.max_y)
            speed_ratio = (randint(1, 3)) / 8
            sprite = CloudTile(tile_size, x, y, cloud, speed_ratio)
            self.cloud_sprites.add(sprite)

    def sprite_kill(self, sprite):
        sprite.kill()

    def draw(self, screen, shift_x):
        self.cloud_sprites.update(shift_x)
        self.cloud_sprites.draw(screen)

    def update(self, world_shift_x):
        # This section needs for save real map zero point
        self.current_x += world_shift_x
        for cloud in self.cloud_sprites:
            if cloud.rect.x < self.current_x - 500:
                cloud.kill()
                self.new_cloud(1, self.max_x-settings.tile_size)
