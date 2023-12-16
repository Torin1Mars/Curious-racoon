import pygame
from random import choice, randint
from support import import_folder
from settings import screen_height, screen_width
from tiles import Static_centerTile
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, pos, game_mode):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.center_pos = pygame.math.Vector2(pos)

        self.my_game_mode = game_mode

        self.image = None
        self.rect = None

        #animation
        self.character_status:str = 'fly'
        self.animation_assets_paths: dict = {'fly': "C:/My_projects/Game_project/graphics/enemy_bird/fly",
                                    'hit': 'C:/My_projects/Game_project/graphics/enemy_bird/hited'}
        self.animation_assets:dict = {}
        self.frame_index:float = 1
        self.animation_speed:float = 0.2

        self.speed:float = 2
        self.move_direction = pygame.math.Vector2(0,0)

        #states
        self.terrain_collision:bool = False

        #akcepted zone
        self.movement_zone = pygame.rect.Rect(0, 0, 170, 170)
        self.movement_zone.center = self.center_pos
        self.target_rect = pygame.rect.Rect(0, 0, 20, 20)
        self.target_rect.center = self.center_pos
        self.current_sector:str = "sector_2"
        self.movement_sectors:dict = {'sector_1': None,
                                      'sector_2': None,
                                      'sector_3': None,
                                      'sector_4': None}
        self._make_sectors()

        self._make_character()

    # AI LOGIC
    # bird sprite each frame goes to TARGET MOVEMENT ZONE and if bird rect collide with target rect it
    # means that we reach the target, and we need reset target to new pos
    # to reset target we choose random coordinates from three another free sectors
    # (current bird sector we don't choose) to prevent strange movement and make bird way longer
    # also if bird rect collide with terrain tile , we put TARGET MOVEMENT ZONE again to center
    # and when bird rect reach to center , we again choose TARGET MOVEMENT ZONE from all four possible sectors

    #                                      |
    #                                      |
    #                                      |
    #        SECTOR_1                      |                      SECTOR_2
    #                                      |       ____
    #                                      |      |    |
    #                                      |      |____| <- TARGET MOVEMENT RECT ZONE
    #                                      |
    #___________________________________CENTER___________________________________
    #                                      |
    #                                      |
    #                                      |
    #                                      |
    #        SECTOR_4                      |                      SECTOR_3
    #                                      |
    #                                      |
    #                                      |

    def _make_character(self):
        for asset in self.animation_assets_paths:
            self.animation_assets[asset] = import_folder(self.animation_assets_paths[asset])

        self.image = self.animation_assets[self.character_status][self.frame_index-1]
        self.rect = self.image.get_rect()
        self.rect.center = self.center_pos

    def _make_sectors(self):
        sector_original_rect = pygame.rect.Rect(0, 0, 60, 60)

        sector_1 = sector_original_rect.copy()
        sector_1.topleft = self.movement_zone.topleft
        self.movement_sectors['sector_1'] = sector_1

        sector_2 = sector_original_rect.copy()
        sector_2.topright = self.movement_zone.topright
        self.movement_sectors['sector_2'] = sector_2

        sector_3 = sector_original_rect.copy()
        sector_3.bottomright = self.movement_zone.bottomright
        self.movement_sectors['sector_3'] = sector_3

        sector_4 = sector_original_rect.copy()
        sector_4.bottomleft = self.movement_zone.bottomleft
        self.movement_sectors['sector_4'] = sector_4

    def _animate_character(self):
        if self.frame_index > len(self.animation_assets[self.character_status]):
            self.frame_index = 0
            self.image = self.animation_assets[self.character_status][self.frame_index]
        else:
            self.image = self.animation_assets[self.character_status][int(self.frame_index)]

        self.frame_index += self.animation_speed

    def _change_target_zone(self):
        possible_sectors = list(self.movement_sectors)
        possible_sectors.remove(self.current_sector)

        new_sector = choice(possible_sectors)
        new_sector_rect = self.movement_sectors[new_sector]

        new_x_range = (new_sector_rect.left, new_sector_rect.right)
        new_x_pos = randint(new_x_range[0], new_x_range[1])

        new_y_range = (new_sector_rect.top, new_sector_rect.bottom)
        new_y_pos = randint(new_y_range[0], new_y_range[1])

        self.current_sector = new_sector
        self.target_rect.center = (new_x_pos, new_y_pos)

    def _move_character(self):
        if self.character_status == "fly":
            # check if we get collide with some terrain
            if self.terrain_collision:
                self.target_rect.center = self.center_pos
                self.terrain_collision = False

            if self.target_rect.collidepoint(self.rect.center):
                self._change_target_zone()
                self.speed = 2
            else:
                self.move_direction = self._get_movement_data(self.rect.center, self.target_rect.center)
                self.rect.center += self.move_direction * self.speed
                self.speed += 0.05

        elif self.character_status == "hit":
            self.move_direction = self._get_movement_data(self.rect.center, self.target_rect.center)
            self.rect.center += self.move_direction * self.speed
            self.speed += 0.1

        if self.move_direction.x < 0:
           self.image = pygame.transform.flip(self.image, 1, 0)

    def _get_movement_data(self, current_pos, target_pos):
        my_current_pos = pygame.math.Vector2(current_pos)
        my_target_pos = pygame.math.Vector2(target_pos)
        return (my_target_pos - my_current_pos).normalize()

    def set_target_to_center(self):
        self.target_rect.center = self.center_pos

    def set_hit(self):
        if not self.character_status == 'hit':
            self.character_status = 'hit'
            self.target_rect.centerx = self.center_pos.x-200
            self.target_rect.centery = screen_height+100

    def update(self, shift_x):
        if shift_x:
            self.center_pos.x += shift_x
            self.movement_zone.centerx += shift_x
            for sector in self.movement_sectors:
                this_rect = self.movement_sectors[sector]
                this_rect.centerx += shift_x

            self.target_rect.centerx += shift_x
            self.rect.centerx += shift_x

        self._animate_character()
        self._move_character()

        #DEBUG
        #pygame.draw.rect(self.screen, 'red', self.target_rect, 5, 5)


class Enemy_2(pygame.sprite.Sprite):
    def __init__(self, screen, pos, game_mode):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.center_pos = pygame.math.Vector2(pos)

        self.my_game_mode = game_mode

        # active or deactivated
        self.internal_staus:str = "active"

        self.image = None
        self.rect = None

        #animation
        self.character_status:str = 'fly'
        self.animation_assets_paths: dict = {'fly': "C:/My_projects/Game_project/graphics/enemy_bird_2/fly",
                                    'hit': 'C:/My_projects/Game_project/graphics/enemy_bird_2/hited'}
        self.animation_assets:dict = {}
        self.frame_index:float = 1
        self.animation_speed:float = 0.2

        self.x_acceleration: float = 0.05
        self.y_acceleration: float = 0.02
        self.enemy_direction = pygame.math.Vector2(1, 1)


        self.direction_y_way:str = "up"
        self.move_direction = pygame.math.Vector2(0, 0)

        #states
        self.terrain_collision:bool = False

        #akcepted zone
        self.movement_zone_height:int = 100
        self.upper_zone_limit:float = 0
        self.lower_zone_limit: float = 0

        self._make_sprite_way_zone()

        self._make_character()



    # AI LOGIC


    #
    #
    #
    #
    #     ________________________________________________________________________________<- UPPER ZONE LIMIT
    #
    #            ___
    #           |   |
    #           |___|  <- FLYING BIRD
    #     ________________________________________________________________________________<- LOVER ZONE LIMIT
    #
    #
    #

    def _make_character(self):
        for asset in self.animation_assets_paths:
            self.animation_assets[asset] = import_folder(self.animation_assets_paths[asset])

        self.image = self.animation_assets[self.character_status][self.frame_index-1]
        self.rect = self.image.get_rect()
        self.rect.center = self.center_pos

    def _make_sprite_way_zone(self):
        self.upper_zone_limit = self.center_pos.y-self.movement_zone_height/2
        self.lower_zone_limit = self.center_pos.y+self.movement_zone_height/2

    def _animate_character(self):
        if self.frame_index > len(self.animation_assets[self.character_status]):
            self.frame_index = 0
            self.image = self.animation_assets[self.character_status][self.frame_index]
        else:
            self.image = self.animation_assets[self.character_status][int(self.frame_index)]

        self.frame_index += self.animation_speed

    def _move_character(self):
        if self.internal_staus == "active":
            if self.character_status == "fly":
                if self.rect.top < self.upper_zone_limit:
                    self.direction_y_way = "down"
                    self.move_direction.y *= -1
                elif self.rect.bottom > self.lower_zone_limit:
                    self.direction_y_way = "up"
                    self.move_direction.y *= -1

                if self.direction_y_way == "up":
                    self.move_direction.y -= self.y_acceleration
                elif self.direction_y_way == "down":
                    self.move_direction.y += self.y_acceleration

                self.move_direction.x += self.x_acceleration

                self.rect.centery += self.move_direction.y
                self.rect.centerx += self.move_direction.x

            elif self.character_status == "hit":
                self.rect.centerx += self.move_direction.x
                self.rect.centery += self.move_direction.y

                self.move_direction.x += self.x_acceleration
                self.move_direction.y += self.y_acceleration

        if self.move_direction.x < 0:
           self.image = pygame.transform.flip(self.image, 1, 0)

    def set_hit(self):
        if not self.character_status == 'hit':
            self.character_status = 'hit'
            if self.move_direction.y < 0:
                self.move_direction.y *= -1

    def update(self, shift_x):
        if shift_x:
            self.rect.centerx += shift_x

        self._animate_character()
        self._move_character()

        pygame.draw.line(self.screen, "green", (0,self.upper_zone_limit),(screen_width, self.upper_zone_limit),5)
        pygame.draw.line(self.screen, "red", (0,self.lower_zone_limit),(screen_width, self.lower_zone_limit),5)