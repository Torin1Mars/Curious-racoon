import pygame, sys
import settings

from tiles import Static_pytmxTile
from enemy import Enemy, Enemy_2
from support import import_pytmx_surface


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.my_level = level(self.screen)
        self.enemy_character = Enemy(self.screen, (350, 250), 5)
        self.enemy_sprite = pygame.sprite.GroupSingle(self.enemy_character)

        self.enemy_character_2 = Enemy_2(self.screen, (50, 400), 5)
        self.enemy_sprite_2 = pygame.sprite.GroupSingle(self.enemy_character_2)

    def update(self):
        shift_x = -1
        self.my_level.update(shift_x)
        self.enemy_sprite.update(shift_x)

        self.enemy_sprite_2.update(shift_x)

        #if self.enemy_sprite.sprite.rect.centery > settings.screen_height:
            #self.enemy_sprite.sprite.kill()

        if self.enemy_sprite_2.sprite.rect.centery > settings.screen_height:
            self.enemy_sprite_2.sprite.kill()


    def run(self, events):
        self.update()

        self.my_level.draw()
        self.enemy_sprite.draw(self.screen)
        self.enemy_sprite_2.draw(self.screen)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.enemy_sprite.sprite.set_hit()
                self.enemy_sprite_2.sprite.set_hit()

#######################################################################################################################


class level:
    def __init__(self, screen):
        self.screen = screen
        self.level_path = f"C:/My_projects/Game_project/levels/1/level_1.tmx"
        self.my_terrain_group = pygame.sprite.Group()
        self._load_level()

    def _load_level(self):
        my_surfaces_list = import_pytmx_surface(self.level_path, f"terrain_tiles")

        for surface in my_surfaces_list:
            this_surface = surface[0]
            this_pos = pygame.math.Vector2(surface[1])
            tile = Static_pytmxTile(this_surface, this_pos)
            self.my_terrain_group.add(tile)

    def update(self, shift_x):
        self.my_terrain_group.update(shift_x)

    def draw(self):
        self.my_terrain_group.draw(self.screen)
