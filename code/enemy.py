import pygame
from random import choice, randint

from tiles import AnimatedTile
from support import import_folder
from settings import screen_height, screen_width, tile_size

class Enemy(AnimatedTile):
    def __init__(self,size, x, y, my_game_mode, offset_x=None, offset_y=None):
        super().__init__(size, x, y, '../graphics/enemy/walk')
        self.my_game_mode = my_game_mode

        if offset_x and offset_y:
            my_offset_x = x - offset_x
            my_offset_y = y - offset_y
            self.rect.topleft = (my_offset_x, my_offset_y)
        elif offset_y:
            my_offset_y = y - offset_y
            self.rect.topleft = (x, my_offset_y)
        elif offset_x:
            my_offset_x = x - offset_x
            self.rect.topleft = (my_offset_x, y)

        self.speed:int = 0
        self.__apply_game_mode()

        #This instruction needs to set proper start directions of characters
        self.speed *= -1
        self.goes_right = True

    def __apply_game_mode(self):
        if self.my_game_mode == f"hard":
            self.speed = randint(3, 6)
        elif self.my_game_mode == f"normal":
            self.speed = randint(2, 4)
        else:
            # if my_game_mode['easy']:
            self.speed = randint(1, 3)

    def move(self):
        self.rect.x -= self.speed

    def reverse_image(self):
        if self.speed >= 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def animate(self):
        self.frame_index += 0.3
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift_x):
        self.rect.x += shift_x
        self.animate()
        self.move()
        self.reverse_image()

#######################################################################################################################
class EnemyStaticBird(pygame.sprite.Sprite):
    def __init__(self, screen, pos, game_mode):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.center_pos = pygame.math.Vector2(pos)

        self.my_game_mode = game_mode

        self.image = None
        self.rect = None

        # animation
        self.character_status: str = 'fly'
        self.animation_assets_paths: dict = {'fly': "C:/My_projects/Game_project/graphics/enemy_bird/fly",
                                             'hit': 'C:/My_projects/Game_project/graphics/enemy_bird/hited'}
        self.animation_assets: dict = {}
        self.frame_index: float = 1
        self.animation_speed: float = 0.2

        self.original_speed: float = 0
        self.current_speed: float = 0
        self.move_direction = pygame.math.Vector2(0, 0)

        # states
        self.terrain_collision: bool = False

        # akcepted zone
        self.movement_zone = pygame.rect.Rect(0, 0, 170, 170)
        self.movement_zone.center = self.center_pos
        self.target_rect = pygame.rect.Rect(0, 0, 20, 20)
        self.target_rect.center = self.center_pos
        self.current_sector: str = "sector_2"
        self.movement_sectors: dict = {'sector_1': None,
                                       'sector_2': None,
                                       'sector_3': None,
                                       'sector_4': None}
        self._make_sectors()
        self._apply_game_mode()
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
    # ___________________________________CENTER___________________________________
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

    def _apply_game_mode(self):
        if self.my_game_mode == f"hard":
            self.original_speed = randint(2, 5)
        elif self.my_game_mode == f"normal":
            self.original_speed = randint(2, 3)
        else:
            # if my_game_mode['easy']:
            self.original_speed = randint(1, 3)

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
                self.current_speed = self.original_speed
                self.terrain_collision = False

            if self.target_rect.collidepoint(self.rect.center):
                self._change_target_zone()
                self.current_speed = self.original_speed
            else:
                self.move_direction = self._get_movement_data(self.rect.center, self.target_rect.center)
                self.rect.center += self.move_direction * self.current_speed
                self.current_speed += 0.05

        elif self.character_status == "hit":
            self.move_direction = self._get_movement_data(self.rect.center, self.target_rect.center)
            self.rect.center += self.move_direction * self.current_speed
            self.current_speed += 0.1

        if self.move_direction.x < 0:
            self.image = pygame.transform.flip(self.image, 1, 0)

    def _get_movement_data(self, current_pos, target_pos):
        my_current_pos = pygame.math.Vector2(current_pos)
        my_target_pos = pygame.math.Vector2(target_pos)
        return (my_target_pos - my_current_pos).normalize()

    def set_hit(self):
        if not self.character_status == 'hit':
            self.character_status = 'hit'
            self.target_rect.centerx = self.center_pos.x - 200
            self.target_rect.centery = screen_height + 150

    def set_target_to_center(self):
        self.target_rect.center = self.center_pos

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

        # FOR DEBUG
        # pygame.draw.rect(self.screen, 'red', self.target_rect, 5, 5)

#######################################################################################################################
class EnemyFlyingBird(pygame.sprite.Sprite):
    def __init__(self, screen, pos, game_mode, my_sound):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.trap_rect = pygame.rect.Rect(0, 0, tile_size*4, tile_size*4)
        self.trap_rect.bottomleft = pos
        self.center_pos = pygame.math.Vector2(self.trap_rect.center)
        self.my_game_mode = game_mode
        self.my_sound = my_sound

        # active or deactivated
        self.internal_status:str = "inactive"

        self.transparent_image = None
        self.image = None
        self.rect = None

        #animation
        self.character_status:str = 'fly'
        self.animation_assets_paths: dict = {'fly': "../graphics/enemy_bird_2/fly",
                                    'hit': '../graphics/enemy_bird_2/hited'}
        self.animation_assets:dict = {}
        self.frame_index:float = 1
        self.animation_speed:float = 0.2

        self.x_acceleration: float = 0
        self.y_acceleration: float = 0
        self.enemy_direction = pygame.math.Vector2(1, 1)

        self.direction_x_way:str = "right"
        self.direction_y_way:str = "up"
        self.move_direction = pygame.math.Vector2(0, 0)

        #akcepted zone
        self.movement_zone_height:int = 120
        self.upper_zone_limit:float = 0
        self.lower_zone_limit: float = 0

        self._make_sprite_way_zone()
        self._apply_game_mode()
        self._make_character()

    # AI LOGIC
    # When we are initializing our class we are creating TRAP ZONE RECT which controls activation  of our bird sprite
    # When player didn't activate our sprite image will be transparent
    # When player trap to TRAP ZONE RECT he activates sprite and birds starts flying
    # Depending on player x position we choose side where start flying from left or from right
    # If player has jump on bird it cause sprite kill
    # If player doesn't kill this sprite bird will be appearing in game infinitely when player will be in TRAP ZONE RECT again
    # Sprite will reload his state automatically when sprite x leave allowable x zone

    #
    #                                          _____________________________
    #                                         |                             |  <- TRAP ZONE RECT
    #                                         |                             |
    #     ________________________________________________________________________________<- UPPER ZONE LIMIT
    #       FLYING DIRECTION ->               |                             |
    #            ___                          |                             |
    #           |   |                         |                             |
    #           |___|  <- FLYING BIRD         |                             |
    #     ________________________________________________________________________________<- LOVER ZONE LIMIT
    #                                         |                             |
    #                                         |_____________________________|
    #

    def _make_character(self):
        for asset in self.animation_assets_paths:
            self.animation_assets[asset] = import_folder(self.animation_assets_paths[asset])

        temp_img = self.animation_assets[self.character_status][self.frame_index-1]

        size = (temp_img.get_width(), temp_img.get_height())
        self.transparent_image = pygame.Surface(size, pygame.SRCALPHA)
        self.image = self.transparent_image

        self.rect = self.image.get_rect()
        self.rect.center = (self.trap_rect.center)

    def _apply_game_mode(self):
        if self.my_game_mode == f"hard":
            self.x_acceleration = 0.08
            self.y_acceleration = 0.04
        elif self.my_game_mode == f"normal":
            self.x_acceleration = 0.05
            self.y_acceleration = 0.02
        else:
            # if my_game_mode['easy']:
            self.x_acceleration = 0.03
            self.y_acceleration = 0.01

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

    def _reset_sprite(self):
        self.rect.center = self.trap_rect.center
        self.image = self.transparent_image
        self.direction_x_way = "right"
        self.direction_y_way = "up"
        self.move_direction.x = 0
        self.move_direction.y = 0
        self.internal_status = "inactive"

    def _move_character(self):
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

            if self.direction_x_way == "left":
                self.move_direction.x -= self.x_acceleration
            elif self.direction_x_way == "right":
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

    def set_active(self, my_player_center_x):
        if not self.internal_status == "active":
            self.my_sound.play_effect_sound('eagle')
            self.internal_status = "active"
            if my_player_center_x <= screen_width/2:
                self.direction_x_way = "left"
                self.rect.centerx = screen_width+50
                self.move_direction.x = 0
            else:
                self.direction_x_way = "right"
                self.rect.centerx = -50
                self.move_direction.x = 0

    def update(self, shift_x):
        if shift_x:
            self.rect.centerx += shift_x
            self.trap_rect.centerx += shift_x

        if self.internal_status == "active":
            self._animate_character()
            self._move_character()

            if (self.rect.centerx < -500) or (self.rect.centerx > screen_width+500):
                self._reset_sprite()

            # FOR DEBUG
            #pygame.draw.line(self.screen, "green", (0, self.upper_zone_limit), (screen_width, self.upper_zone_limit), 5)
            #pygame.draw.line(self.screen, "red", (0, self.lower_zone_limit), (screen_width, self.lower_zone_limit), 5)

        # FOR DEBUG
        # pygame.draw.rect(self.screen, "red", self.trap_rect, 5, 5)
