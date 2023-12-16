import pygame
import settings

from support import import_csv_layout, import_pytmx_surface
from tiles import Tile, StaticTile, Static_pytmxTile, \
                Water_pytmxTile, AnimatedCoin, AnimatedPalm, Static_snowTile, Static_grassTile

from enemy import Enemy, EnemyStaticBird, EnemyFlyingBird
from decoration import Background, Clouds

from player import Player
from particles import ParticleEffect

from additional_windows import PauseWindow
from ui import UI

class Level:
    def __init__(self, current_level, screen, sound, game_mode):
        # general setup
        self.my_map_dict = None
        self.display_surface = screen
        self.world_shift_x = 0

        # level settings
        self.game_mode = game_mode
        self.current_level = current_level
        self.level_width = self.__get_level_width()

        # ui window data
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        self.max_coins_amount = 0

        self.goal = pygame.sprite.GroupSingle()
        self.enemy_effect = pygame.sprite.Group()
        self.dust_sprites = pygame.sprite.Group()

        # audio
        self.my_sound = sound

        # load_level_data
        self.load_level()
        self.level_internal_state = 'level'

        ###############################################################################################################
        # additional decorations
        self.level_background = Background(self.display_surface, self.current_level['bg_image'])
        self.clouds_horizon_x = 3
        self.clouds = Clouds(self.clouds_horizon_x, self.level_width + settings.screen_width, 20)
        ###############################################################################################################

        # max time level (sec)
        self.max_level_time = 180
        self.ui = UI(self.display_surface, self.max_level_time)

        # player settings
        self.player = pygame.sprite.GroupSingle()
        self.create_player()

        # variables for additional effects
        self.player_on_ground = False
        self.player_previous_x = 0

        # these variables we will change when player get win or get lose
        self.player_win: bool = False
        self.earned_stars: int = 0

        self.player_lose: bool = False

        # pause window initialization
        self.pause_window = PauseWindow(self.change_level_internal_state, self.ui.push_time)

    def __get_level_width(self):
        terrain_layout = import_csv_layout(self.current_level['terrain'])
        level_width = len(terrain_layout[0]) * settings.tile_size
        return level_width

    def load_level(self):
        self.my_map_dict = {}
        tmx_path = self.current_level['tmx_map']
        for key in self.current_level:
            if key == f"terrain":
                # pytmx loader
                self.pytmx_terrain_sprites = self.create_Pytmx_tile_group(tmx_path, 'terrain_tiles')

                self.my_map_dict[key] = self.pytmx_terrain_sprites

            elif key == f"crates":
                # pytmx loader
                self.pytmx_crates_sprites = self.create_Pytmx_tile_group(tmx_path, 'crates')

                self.my_map_dict[key] = self.pytmx_crates_sprites

            elif key == f"fence":
                # pytmx loader
                self.pytmx_fence_sprites = self.create_Pytmx_tile_group(tmx_path, 'fence')

                self.my_map_dict[key] = self.pytmx_fence_sprites

            elif key == f"water":
                # pytmx loader
                self.pytmx_water_sprites = self.create_Pytmx_tile_group(tmx_path, 'water')

                self.my_map_dict[key] = self.pytmx_water_sprites

            elif key == f"decorations":
                # pytmx loader
                self.pytmx_decorations_sprites = self.create_Pytmx_tile_group(tmx_path, 'decorations')

                self.my_map_dict[key] = self.pytmx_decorations_sprites

            elif key == f"snow":
                # pytmx loader
                self.pytmx_snow_sprites = self.create_Pytmx_tile_group(tmx_path, 'snow')

                self.my_map_dict[key] = self.pytmx_snow_sprites

            elif key == f"forest_trees":
                # pytmx loader
                self.pytmx_forest_trees_sprites = self.create_Pytmx_tile_group(tmx_path, 'forest_trees')

                self.my_map_dict[key] = self.pytmx_forest_trees_sprites

            elif key == f"cactus":
                # pytmx loader
                self.pytmx_cactus_sprites = self.create_Pytmx_tile_group(tmx_path, 'cactus')

                self.my_map_dict[key] = self.pytmx_cactus_sprites

            elif key == f"grass":
                # pytmx loader
                self.pytmx_grass_sprites = self.create_Pytmx_tile_group(tmx_path, 'grass')

                self.my_map_dict[key] = self.pytmx_grass_sprites

            ############################################
            # Pygame loader
            ############################################

            elif key == f"coins":
                # pygame loader
                coin_layout = import_csv_layout(self.current_level['coins'])
                self.coins_sprites = self.create_tile_group(coin_layout, 'coins')

                self.my_map_dict[key] = self.coins_sprites

            elif key == f"fg_palms":
                # pygame loader
                fg_palms_layout = import_csv_layout(self.current_level['fg_palms'])
                self.fg_palms_sprites = self.create_tile_group(fg_palms_layout, 'fg_palms')

                self.my_map_dict[key] = self.fg_palms_sprites

            elif key == f"bg_palms":
                # pygame loader
                bg_palms_layout = import_csv_layout(self.current_level['bg_palms'])
                self.bg_palms_sprites = self.create_tile_group(bg_palms_layout, 'bg_palms')

                self.my_map_dict[key] = self.bg_palms_sprites

            elif key == f"enemies":
                # pygame loader
                enemies_layout = import_csv_layout(self.current_level['enemies'])
                self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

                self.my_map_dict[key] = self.enemies_sprites

            elif key == f"static_bird":
                # pygame loader
                static_bird_layout = import_csv_layout(self.current_level['static_bird'])
                self.static_bird_sprites = self.create_tile_group(static_bird_layout, 'static_bird')

                self.my_map_dict[key] = self.static_bird_sprites

            elif key == f"flying_bird":
                # pygame loader
                flying_bird_layout = import_csv_layout(self.current_level['flying_bird'])
                self.flying_bird_sprites = self.create_tile_group(flying_bird_layout, 'flying_bird')

                self.my_map_dict[key] = self.flying_bird_sprites

            elif key == f"constrains":
                # pygame loader
                constrains_layout = import_csv_layout(self.current_level['constrains'])
                self.constrains_sprites = self.create_tile_group(constrains_layout, 'constrains')

                self.my_map_dict[key] = self.constrains_sprites

    def create_Pytmx_tile_group(self, pytmx_level_path, tiles_name) -> pygame.sprite.Group:
        sprite_group = pygame.sprite.Group()
        my_surfaces_list = import_pytmx_surface(pytmx_level_path, tiles_name)
        if tiles_name == f'decorations':
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                this_pos.y += settings.tile_size + 5
                tile = Static_pytmxTile(this_surface, this_pos)
                tile.rect.bottomleft = this_pos
                sprite_group.add(tile)

        elif tiles_name == f'water':
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                tile = Water_pytmxTile(this_surface, this_pos)
                sprite_group.add(tile)

        elif tiles_name == f'snow':
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                tile = Static_snowTile(this_surface, this_pos)
                sprite_group.add(tile)

        elif tiles_name == f'grass':
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                tile = Static_grassTile(this_surface, this_pos)
                tile.rect.bottom -= 22
                sprite_group.add(tile)

        elif tiles_name == f'forest_trees':
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                tile = Static_grassTile(this_surface, this_pos)
                tile.rect.bottom -= 10
                sprite_group.add(tile)

        elif tiles_name == f'cactus':
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                tile = Static_grassTile(this_surface, this_pos)
                tile.rect.bottom -= 20
                sprite_group.add(tile)

        else:
            for surface in my_surfaces_list:
                this_surface = surface[0]
                this_pos = pygame.math.Vector2(surface[1])
                tile = Static_pytmxTile(this_surface, this_pos)
                sprite_group.add(tile)

        return sprite_group

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                if cell != '-1':
                    x = cell_index * settings.tile_size
                    y = row_index * settings.tile_size

                    if type == 'coins':
                        if cell == "0":
                            sprite = AnimatedCoin(settings.tile_size, x, y,
                                                  '../graphics/coins/gold', 5)
                            self.max_coins_amount += 5
                        else:
                            sprite = AnimatedCoin(settings.tile_size, x, y,
                                                  '../graphics/coins/silver', 1)
                            self.max_coins_amount += 1

                    if type == 'fg_palms':
                        if cell == "2":
                            sprite = AnimatedPalm(settings.tile_size, x, y,
                                                  '../graphics/terrain/palm_small',
                                                  offset_y=38)
                        elif cell == "3":
                            sprite = AnimatedPalm(settings.tile_size, x, y,
                                                  '../graphics/terrain/palm_large',
                                                  offset_y=70)

                    if type == 'bg_palms':
                        sprite = AnimatedPalm(settings.tile_size, x, y,
                                              '../graphics/terrain/palm_bg', offset_x=20,
                                              offset_y=60)

                    if type == 'enemies':
                        sprite = Enemy(settings.tile_size, x, y, self.game_mode, offset_y=30)

                    if type == 'constrains':
                        sprite = Tile(settings.tile_size, x, y)

                    if type == 'static_bird':
                        sprite = EnemyStaticBird(self.display_surface, (x,y), self.game_mode)

                    if type == 'flying_bird':
                        y += settings.tile_size
                        sprite = EnemyFlyingBird(self.display_surface, (x, y), self.game_mode, self.my_sound)

                    sprite_group.add(sprite)

        return sprite_group
    ###################################################################################################################

    # player settings section
    def create_player(self):
        layout = import_csv_layout(self.current_level['player'])
        for row_index, row in enumerate(layout):
            for cell_index, cell in enumerate(row):
                if cell != '-1':
                    x = cell_index * settings.tile_size
                    y = row_index * settings.tile_size
                    if cell == '1':
                        sprite = Player((x, y), self.display_surface, self.create_jump_particles, self.change_health,\
                                        self.level_background.make_swipe_x, self.my_sound, self.game_mode)
                        self.player.add(sprite)

                    if cell == '0':
                        surface = pygame.image.load('../graphics/character/end_point.png').convert_alpha()
                        sprite = StaticTile(settings.tile_size, x, y, surface)
                        self.goal.add(sprite)

    def horizontal_movement_collision(self):
        my_player = self.player.sprite
        my_player.collision_rect.x += my_player.player_direction.x * my_player.speed
        collideble_sprites = self.pytmx_terrain_sprites.sprites() + self.pytmx_crates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collideble_sprites:
            if sprite.rect.colliderect(my_player.collision_rect):

                '''Here I would like check was there any character movement'''

                player_distance = abs(self.player.sprite.collision_rect.centerx - self.player_previous_x)
                if not player_distance > 6:
                    my_player.reset_inertia(direction="x")

                '''This variable set the height of imaginable collide line witch gives overall high dimensions
                upper point sets the up point of our overall dimension
                lower_point sets the low point of our overall dimension'''

                my_player_overall_height = {'upper_point': my_player.collision_rect.top,
                                            'lower_point': my_player.collision_rect.bottom-1}
                height_colliding = False

                if my_player_overall_height['upper_point'] in range(int(sprite.rect.top),
                                                                    int(sprite.rect.bottom)):
                    height_colliding = True
                if my_player_overall_height['lower_point'] in range(int(sprite.rect.top),
                                                                    int(sprite.rect.bottom)):
                    height_colliding = True

                if my_player.player_direction.x > 0 and height_colliding:  # This means that we are moving to the right
                    my_player.collision_rect.right = sprite.rect.left - 3  #-3 is a parameter to compensation incorrect size of animation images
                    my_player.player_on_right = True
                    my_player.player_on_left = False

                    if my_player.inertia_x >= my_player.max_inertia - 1:
                        self.level_background.make_swipe_x("left")
                        my_player.reset_inertia(direction="x")

                elif my_player.player_direction.x < 0 and height_colliding:  # This means that we're moving to the left
                    my_player.collision_rect.left = sprite.rect.right + 3  # +3 is a parameter to compensation incorrect size of animation images
                    my_player.player_on_left = True
                    my_player.player_on_right = False

                    if my_player.inertia_x >= my_player.max_inertia - 1:
                        self.level_background.make_swipe_x("right")
                        my_player.reset_inertia(direction="x")

                # Here we are checking case when player speed is 0 but world shift parameter isn't zero
                elif self.world_shift_x < 0:  # This means that we're moving to the right
                    my_player.collision_rect.centerx -= 2  # -3 is a parameter to compensation incorrect size of animation images
                    my_player.player_on_left = False
                    my_player.player_on_right = True

                elif self.world_shift_x > 0:  # This means that we're moving to the left
                    my_player.collision_rect.centerx += 2  # +3 is a parameter to compensation incorrect size of animation images
                    my_player.player_on_left = True
                    my_player.player_on_right = False

                # In this final stage we are lastly checking what to do with collision situation
                # And for prevent unresolved situation we translate player sprite on a few pixels
                else:
                    if self.player.sprite.collision_rect.centerx - self.player_previous_x > 0:
                        self.player.sprite.collision_rect.centerx -= 3
                    elif self.player.sprite.collision_rect.centerx - self.player_previous_x < 0:
                        self.player.sprite.collision_rect.centerx += 3
                    else:
                        self.player.sprite.collision_rect.centerx = self.player_previous_x

                self.player_previous_x = self.player.sprite.collision_rect.centerx



    def vertical_movement_collision(self):
        my_player = self.player.sprite
        my_player.apply_gravity()
        collideble_sprites = self.pytmx_terrain_sprites.sprites() + self.pytmx_crates_sprites.sprites() + self.fg_palms_sprites.sprites()
        for sprite in collideble_sprites:
            if sprite.rect.colliderect(my_player.collision_rect):
                #DEBUG
                '''pygame.draw.line(self.display_surface,'red', (my_player.collision_rect.right, my_player_overall_height['upper_point']),
                                 #(my_player.collision_rect.right, my_player_overall_height['lower_point']), 5)'''

                # Main review
                if my_player.player_direction.y > 0:  # In case when falling
                    my_player.collision_rect.bottom = sprite.rect.top
                    my_player.player_direction.y = 0
                    my_player.player_on_ground = True


                elif my_player.player_direction.y < 0:  # In case when jumping
                    my_player.collision_rect.top = sprite.rect.bottom+2
                    my_player.player_direction.y = 0
                    my_player.player_on_ceiling = True

        # This for recheking state of player positioning
        if my_player.player_on_ground and my_player.player_direction.y < 0 or \
                my_player.player_direction.y > 1:
            my_player.player_on_ground = False

    def get_player_on_ground(self):
        if self.player.sprite.player_on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_jump_particles(self, pos):
        if self.player.sprite.right_facing_direction:
            pos -= pygame.math.Vector2(5, 15)
        else:
            pos += pygame.math.Vector2(5, -15)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprites.add(jump_particle_sprite)

    def create_landing_dust_particles(self):
        if not self.player_on_ground and self.player.sprite.player_on_ground and not self.dust_sprites.sprites():
            if self.player.sprite.right_facing_direction:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprites.add(fall_dust_particle)

            my_player = self.player.sprite
            if my_player.inertia_y >= my_player.inertia_y - 1:
                self.level_background.make_swipe_y("down")
                my_player.reset_inertia(direction="y")

    ###################################################################################################################
    def check_enemy_constrains_collision(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constrains_sprites, False):
                offset = 10
                ''' Next statement we need for prevent stacking of enemy sprite that is why we gives 
                2 pixels extra offset to prevent that problem'''
                if enemy.goes_right == True:
                    enemy.goes_right = False
                    enemy.rect.x -= offset
                    enemy.reverse()

                elif enemy.goes_right == False:
                    enemy.goes_right = True
                    enemy.rect.x += offset
                    enemy.reverse()

    def make_world_shift_x(self):
        my_player = self.player.sprite
        my_player_x = my_player.rect.centerx
        direction_x = my_player.player_direction.x

        if my_player_x < settings.tile_size * 5 and direction_x < 0:
            self.world_shift_x = settings.player_speed
            my_player.speed = 0
        elif my_player_x > settings.screen_width - settings.tile_size * 5 and direction_x > 0:
            self.world_shift_x = -settings.player_speed
            my_player.speed = 0
        else:
            self.world_shift_x = 0
            my_player.speed = settings.player_speed

    def check_win(self):
        def calculate_score():
            if self.coins >= self.max_coins_amount*0.9:
                return 3
            elif self.coins >= self.max_coins_amount*0.55:
                return 2
            else:
                return 1

        my_player_center = self.player.sprite.collision_rect.center
        if self.goal.sprite.rect.collidepoint(my_player_center):
            self.player_win = True
            self.earned_stars = calculate_score()

    def check_coins_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collided_coins:
            self.my_sound.play_effect_sound("coin_sound")
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        #my_player = self.player.sprite
        #enemies_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_sprites, False)
        my_player = self.player.sprite
        for enemy_sprite in self.enemies_sprites:
            if my_player.collision_rect.colliderect(enemy_sprite.rect) and not my_player.invincible:
                enemy_center = enemy_sprite.rect.centery
                enemy_top = enemy_sprite.rect.top
                player_bottom = my_player.collision_rect.bottom

                if int(self.player.sprite.player_direction.y) >= 0 and enemy_top < player_bottom < enemy_center:
                    self.my_sound.play_effect_sound("stomp_sound")
                    self.player.sprite.player_direction.y = -10
                    explosion_sprite = ParticleEffect(enemy_sprite.rect.center, "enemy_collision")
                    self.enemy_effect.add(explosion_sprite)
                    enemy_sprite.kill()
                else:
                    self.player.sprite.get_damage()

        if not self.enemies_sprites:
            self.my_map_dict.pop("enemies")

    def check_enemy_static_bird_collisions(self):
        my_player = self.player.sprite

        for bird in self.static_bird_sprites:
            if not bird.character_status == 'hit':
                for tile in self.pytmx_terrain_sprites:
                    if bird.rect.colliderect(tile.rect):
                        bird.set_target_to_center()

            if my_player.collision_rect.colliderect(bird.rect) and not my_player.invincible:
                bird_center = bird.rect.centery
                bird_top = bird.rect.top
                player_bottom = my_player.collision_rect.bottom

                if not bird.character_status == 'hit':
                    if bird_top < player_bottom < bird_center:
                        self.my_sound.play_effect_sound("stomp_sound")
                        self.player.sprite.player_direction.y = -10
                        explosion_sprite = ParticleEffect(bird.rect.center, "enemy_collision")
                        self.enemy_effect.add(explosion_sprite)
                        bird.set_hit()

                    else:
                        self.player.sprite.get_damage()

            if bird.rect.centery > settings.screen_height+20:
                bird.kill()

        if not self.static_bird_sprites:
            self.my_map_dict.pop("static_bird")

    def check_enemy_flying_bird_collisions(self):
        my_player = self.player.sprite
        for bird in self.flying_bird_sprites:
            if bird.trap_rect.collidepoint(my_player.rect.center):
                bird.set_active(my_player.rect.centerx)

        for bird in self.flying_bird_sprites:
            if bird.internal_status == "active":
                if my_player.collision_rect.colliderect(bird.rect) and not my_player.invincible:
                    bird_center = bird.rect.centery
                    bird_top = bird.rect.top
                    player_bottom = my_player.collision_rect.bottom

                    if not bird.character_status == 'hit':
                        if bird_top < player_bottom < bird_center:
                            self.my_sound.play_effect_sound("stomp_sound")
                            self.player.sprite.player_direction.y = -10
                            explosion_sprite = ParticleEffect(bird.rect.center, "enemy_collision")
                            self.enemy_effect.add(explosion_sprite)
                            bird.set_hit()

                        else:
                            self.player.sprite.get_damage()

            if bird.rect.centery > settings.screen_height+20:
                bird.kill()

        if not self.flying_bird_sprites:
            self.my_map_dict.pop("flying_bird")

    def check_pause(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.level_internal_state = 'pause_window'
                    self.pause_window.grab_screen(self.display_surface)
                    self.pause_window.my_timer.activate()
                    self.ui.pause_time()

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        def check_death():
            if self.current_health <= 0:
                return 1
            else:
                return 0

        def check_fall():
            if self.player.sprite.rect.y > settings.screen_height:
                return 1
            else:
                return 0

        def check_overtime():
            if self.max_level_time < self.ui.level_time:
                return 1
            else:
                return 0

        def reset_level_indicators():
            self.current_health = 100
            self.coins = 0

        if check_death() or check_fall() or check_overtime():
            reset_level_indicators()
            self.player_lose = True

    def change_level_internal_state(self, new_state: str):
        self.level_internal_state = new_state

    def draw_level(self):
        # decorations_sprites
        self.level_background.update()
        self.level_background.draw()

        # clouds sprites
        self.clouds.update(self.world_shift_x)
        self.clouds.draw(self.display_surface, self.world_shift_x)

        # decorations_sprites
        self.pytmx_decorations_sprites.draw(self.display_surface)
        self.pytmx_decorations_sprites.update(self.world_shift_x)

        if f"forest_trees" in self.my_map_dict:
            self.pytmx_forest_trees_sprites.draw(self.display_surface)
            self.pytmx_forest_trees_sprites.update(self.world_shift_x)

        if f"cactus" in self.my_map_dict:
            self.pytmx_cactus_sprites.draw(self.display_surface)
            self.pytmx_cactus_sprites.update(self.world_shift_x)

        # dust sprites
        self.dust_sprites.update(self.world_shift_x)
        self.dust_sprites.draw(self.display_surface)

        # bg_palms_sprites
        self.bg_palms_sprites.draw(self.display_surface)
        self.bg_palms_sprites.update(self.world_shift_x)

        # coins_sprites
        self.coins_sprites.draw(self.display_surface)
        self.coins_sprites.update(self.world_shift_x)

        # enemies_sprites
        if f"enemies" in self.my_map_dict:
            self.constrains_sprites.update(self.world_shift_x)
            self.enemies_sprites.update(self.world_shift_x)
            self.check_enemy_constrains_collision()
            self.enemies_sprites.draw(self.display_surface)

        # create terrain_sprites
        self.pytmx_terrain_sprites.draw(self.display_surface)
        self.pytmx_terrain_sprites.update(self.world_shift_x)

        # crates_sprites
        self.pytmx_crates_sprites.draw(self.display_surface)
        self.pytmx_crates_sprites.update(self.world_shift_x)

        # static birds sprites
        if f"static_bird" in self.my_map_dict:
            self.static_bird_sprites.update(self.world_shift_x)
            self.check_enemy_static_bird_collisions()
            self.static_bird_sprites.draw(self.display_surface)

        # flying birds sprites
        if f"flying_bird" in self.my_map_dict:
            self.flying_bird_sprites.update(self.world_shift_x)
            self.check_enemy_flying_bird_collisions()
            self.flying_bird_sprites.draw(self.display_surface)

        # player sprite
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust_particles()

        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift_x)
        # self.goal.draw(self.display_surface)

        # fence_sprites
        self.pytmx_fence_sprites.update(self.world_shift_x)
        self.pytmx_fence_sprites.draw(self.display_surface)

        # water_sprites
        self.pytmx_water_sprites.draw(self.display_surface)
        self.pytmx_water_sprites.update(self.world_shift_x)

        # enemy_effect
        self.enemy_effect.update(self.world_shift_x)
        self.enemy_effect.draw(self.display_surface)

        # grass sprites
        if f"grass" in self.my_map_dict:
            self.pytmx_grass_sprites.draw(self.display_surface)
            self.pytmx_grass_sprites.update(self.world_shift_x)

        # fg_palms_sprites
        self.fg_palms_sprites.draw(self.display_surface)
        self.fg_palms_sprites.update(self.world_shift_x)

        # snow sprites
        if f"snow" in self.my_map_dict:
            self.pytmx_snow_sprites.update(self.world_shift_x)
            self.pytmx_snow_sprites.draw(self.display_surface)

    def run(self, events):
        if self.level_internal_state == 'pause_window':
            self.pause_window.update(events)
            self.pause_window.draw(self.display_surface)

        else:
            # run the entire level/game
            self.make_world_shift_x()
            self.draw_level()

            # goals section
            self.check_coins_collisions()
            self.check_enemy_collisions()

            # draw ui
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins, self.max_coins_amount)
            self.ui.show_timer()

            # check game over
            self.check_win()
            self.check_game_over()

            # check pause if pause window
            self.check_pause(events)
