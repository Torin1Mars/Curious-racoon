import pygame,sys
from settings import screen_width, screen_height, game_difficulty
from tiles import Static_centerTile, Static_centerDoubleTile, AnimatedStaticPict
from buttons import StaticButton, StaticSoundButton
from additional_windows import YesNoWindow
from leaderboard import Leaderboard

from support import CustomTimer

class MenuWindow:
    def __init__(self, screen: pygame.Surface, change_status, mute_status, user_settings):
        self.display_surface = screen

        self.mute_status = mute_status
        self.user_settings = user_settings
        self.change_status = change_status
        self.previous_status = None

        self.internal_status = "menu_window"

        self.returning_data = {'data_from_menu': [],
                               'data_from_settings': []}

        self.images_data = {'bg_menu': '../graphics/menu_window/bg_menu.jpg',

                            'bt_continue_1': '../graphics/menu_window/Bt_continue_1.png',
                            'bt_continue_2': '../graphics/menu_window/Bt_continue_2.png',
                            'bt_continue_code': 1,

                            'bt_menu_1': '../graphics/menu_window/Bt_menu_1.png',
                            'bt_menu_2': '../graphics/menu_window/Bt_menu_2.png',
                            'bt_menu_code': 2,

                            'bt_settings_1': '../graphics/menu_window/Bt_settings_1.png',
                            'bt_settings_2': '../graphics/menu_window/Bt_settings_2.png',
                            'bt_settings_code': 3,

                            'bt_exit_1': '../graphics/menu_window/Bt_exit_1.png',
                            'bt_exit_2': '../graphics/menu_window/Bt_exit_2.png',
                            'bt_exit_code': 0,

                            'bt_sound_1': '../graphics/menu_window/Bt_sound_1.png',
                            'bt_sound_2': '../graphics/menu_window/Bt_sound_2.png',
                            'bt_sound_code': 4,

                            'bt_cup_1': '../graphics/menu_window/Win_cup_1.png',
                            'bt_cup_2': '../graphics/menu_window/Win_cup_2.png',
                            'bt_cup_code': 5
                            }

        self.bg_image = pygame.image.load(self.images_data['bg_menu']).convert_alpha()
        self.bg_rect = self.bg_image.get_rect(center=(screen_width / 2, screen_height / 2))

        self.main_buttons_list = []
        self.sound_button_group = pygame.sprite.Group()

        self._create_main_buttons_()

        self.settings_window = None
        self.exit_question_window = None

    def __reset_returning_data(self):
        self.returning_data = {'data_from_menu': [],
                               'data_from_settings': []}

    def _load_surfaces_(self, paths: tuple):
        surface_list = []
        for path in paths:
            surface = pygame.image.load(path).convert_alpha()
            surface_list.append(surface)
        return surface_list

    def _create_main_buttons_(self):
        continue_surf = self._load_surfaces_((self.images_data['bt_continue_1'], self.images_data['bt_continue_2']))
        continue_bt = StaticButton((screen_width / 2, 100), continue_surf, self.display_surface,
                               self.images_data['bt_continue_code'])

        menu_surf = self._load_surfaces_((self.images_data['bt_menu_1'], self.images_data['bt_menu_2']))
        menu_bt = StaticButton((screen_width / 2, 250), menu_surf, self.display_surface,
                               self.images_data['bt_menu_code'])

        settings_surf = self._load_surfaces_((self.images_data['bt_settings_1'], self.images_data['bt_settings_2']))
        settings_bt = StaticButton((screen_width / 2, 400), settings_surf, self.display_surface,
                                   self.images_data['bt_settings_code'])

        exit_surf = self._load_surfaces_((self.images_data['bt_exit_1'], self.images_data['bt_exit_2']))
        exit_bt = StaticButton((screen_width / 2, 550), exit_surf, self.display_surface,
                               self.images_data['bt_exit_code'])

        bt_sound_surf = self._load_surfaces_((self.images_data['bt_sound_1'], self.images_data['bt_sound_2']))
        bt_sound = StaticSoundButton((screen_width - 80, 80), bt_sound_surf, self.display_surface,
                                     self.images_data['bt_sound_code'], self.mute_status)

        cup_surf = self._load_surfaces_((self.images_data['bt_cup_1'], self.images_data['bt_cup_2']))
        bt_cup = StaticButton((185, 95), cup_surf, self.display_surface, self.images_data['bt_cup_code'])

        self.main_buttons_list.extend([continue_bt, menu_bt, settings_bt, exit_bt, bt_sound, bt_cup])

    def make_exit_question(self):
        row_1 = f"WOULD YOU LIKE TO SAVE"
        row_2 = f"YOUR GAME PROGRESS"
        self.exit_question_window = YesNoWindow(self.display_surface, (screen_width / 2, 300), (400, 300), (row_1, row_2))

    def event_handler(self, button_code):
        if button_code == self.images_data['bt_exit_code']:
            self.make_exit_question()
            self.internal_status = "exit_question"

        elif button_code == self.images_data['bt_continue_code']:
            self.change_status(self.previous_status)

        elif button_code == self.images_data['bt_menu_code']:
            self.returning_data['data_from_menu'].append(self.images_data['bt_menu_code'])

        elif button_code == self.images_data['bt_settings_code']:
            self.internal_status = "settings_window"
            self.settings_window = SettingsWindow(self.display_surface, self.user_settings)

        elif button_code == self.images_data['bt_sound_code']:
            self.returning_data['data_from_menu'].append(self.images_data['bt_sound_code'])

        elif button_code == self.images_data['bt_cup_code']:
            self.internal_status = "leaderboard_window"
            self.leaderboard = Leaderboard(self.display_surface, 25)

    def get_data(self):
        return self.returning_data

    def update(self, mouse_pos, events):
        self.__reset_returning_data()
        if self.internal_status == "menu_window":
            for button in self.main_buttons_list:
                button.update(mouse_pos, events)
                if button.check_pressed():
                    self.event_handler(button.button_code)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.change_status(self.previous_status)

        elif self.internal_status == "settings_window":
            self.settings_window.update(mouse_pos, events)
            self.returning_data['data_from_settings'] = self.settings_window.returning_data
            settings_window_status = self.settings_window.external_status
            if settings_window_status != f"settings_window":
                self.internal_status = "menu_window"

        elif self.internal_status == "leaderboard_window":
            self.leaderboard.update(mouse_pos, events)
            data_from_leaderboard = self.leaderboard.get_data()
            if data_from_leaderboard:
                self.internal_status = "menu_window"

        elif self.internal_status == "exit_question":
            self.exit_question_window.update(mouse_pos, events)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.internal_status = "menu_window"

            payload = self.exit_question_window.get_data()
            if payload:
                if payload == f"ok":
                    print("PASS")
                    #pygame.quit()
                    #sys.exit()
                else:
                    self.internal_status = "menu_window"
                    pygame.quit()
                    sys.exit()

    def draw(self):
        self.display_surface.blit(self.bg_image, self.bg_rect)
        if self.internal_status == "menu_window":
            for button in self.main_buttons_list:
                button.draw()

        elif self.internal_status == "settings_window":
            self.settings_window.draw()

        elif self.internal_status == "leaderboard_window":
            self.leaderboard.draw()

        elif self.internal_status == "exit_question":
            for button in self.main_buttons_list:
                button.draw()
            self.exit_question_window.draw()

#######################################################################################################################
class SettingsWindow:
    def __init__(self, screen: pygame.Surface, user_settings):
        self.display_surface = screen
        self.user_settings = user_settings

        # "settings_window" or "menu_window"
        self.external_status = "settings_window"

        # "settings_window" or "question_window"
        self.settings_internal_status = "settings_window"

        self.returning_data = None

        self.bg_settings_img = pygame.image.load('../graphics/menu_window/settings/bg_settings.png').convert_alpha()
        self.background_sprite = Static_centerTile(self.bg_settings_img, (screen_width / 2, screen_height / 2))
        self.static_sprite_group = pygame.sprite.Group(self.background_sprite)

        self.images_data = {'Bt_save_1': "../graphics/menu_window/settings/Bt_save_1.png",
                            'Bt_save_2': "../graphics/menu_window/settings/Bt_save_2.png",
                            'Bt_save_code': 1,

                            'Bt_cancel_1': "../graphics/menu_window/settings/Bt_cancel_1.png",
                            'Bt_cancel_2': '../graphics/menu_window/settings/Bt_cancel_2.png',
                            'Bt_cancel_code': 0}

        self.slide_buttons = []
        self.static_buttons = []
        self.__create_slide_buttons()
        self.__create_static_buttons()

        self.grass_sprite = pygame.sprite.Group()
        self.__create_grass()

        self.animated_characters = pygame.sprite.Group()
        self.__create_animated_characters()

        # setting proper start position for each button
        self.__set_start_buttons_pos()

        row_1 = f"IF PRESS OK"
        row_2 = f"YOU WILL LOOSE "
        row_3 = f"YOUR LEVEL PROGRESS"
        self.question_window = YesNoWindow(self.display_surface, (screen_width/2, 300), (400, 300), (row_1, row_2, row_3))

        '''additional list to compare game difficulty 
        from settings window and game difficulty keys'''
        self.list_difficulty_keys = list(game_difficulty.keys())

    def __create_grass(self):
        grass_img = pygame.image.load('../graphics/menu_window/settings/grass.png').convert_alpha()
        grass_img = pygame.transform.scale(grass_img, (self.background_sprite.rect.width-115, grass_img.get_height()))
        grass_sprite = Static_centerTile(grass_img, (screen_width/2, 653))
        self.grass_sprite.add(grass_sprite)

    def __create_slide_buttons(self) -> None:
        temp_surf = pygame.image.load('../graphics/menu_window/settings/BTN_ORANGE.png').convert_alpha()
        self.game_difficulty_slider = SlidingStepButton((screen_width / 2, 180), temp_surf)

        temp_surf = pygame.image.load('../graphics/menu_window/settings/BTN_GREEN.png').convert_alpha()
        self.background_sound_button = SlidingBarButton((screen_width / 2, 315), temp_surf)

        temp_surf = pygame.image.load('../graphics/menu_window/settings/BTN_BLUE.png').convert_alpha()
        self.effects_sound_button = SlidingBarButton((screen_width / 2, 458), temp_surf)

        self.slide_buttons.extend([self.background_sound_button, self.effects_sound_button])

    def __create_static_buttons(self):
        first_surf = pygame.image.load(self.images_data['Bt_save_1']).convert_alpha()
        second_surf = pygame.image.load(self.images_data['Bt_save_2']).convert_alpha()
        save_button = StaticButton((770, 610), (first_surf, second_surf), self.display_surface, self.images_data['Bt_save_code'])

        first_surf = pygame.image.load(self.images_data['Bt_cancel_1']).convert_alpha()
        second_surf = pygame.image.load(self.images_data['Bt_cancel_2']).convert_alpha()
        cancel_button = StaticButton((950, 610), (first_surf, second_surf), self.display_surface, self.images_data['Bt_cancel_code'])

        self.static_buttons.extend([save_button, cancel_button])

    def __set_start_buttons_pos(self):
        self.game_difficulty_slider.set_start_pos(self.user_settings['game_difficulty'])
        self.background_sound_button.set_start_pos(self.user_settings['bg_music_volume'])
        self.effects_sound_button.set_start_pos(self.user_settings['effects_sound_volume'])

    def __create_animated_characters(self):
        player_sprite = AnimatedStaticPict(50, 185, 600, "../animation_assets/character/run", 0.1)
        enemy_sprite = AnimatedStaticPict(50, 310, 600, "../graphics/enemy/walk", 0.1)
        enemy_sprite.rect.bottom = player_sprite.rect.bottom
        self.animated_characters.add([player_sprite, enemy_sprite])

    def event_handler(self, button_code):
        if button_code == self.images_data['Bt_cancel_code']:
            self.external_status = "menu_window"

        elif button_code == self.images_data['Bt_save_code']:
            self.settings_internal_status = "question_window"

            for button in self.static_buttons:
                # we need this update to update buttons colors back to standard state
                # here we don't need real mouse pos and events, so we are using just simple zero's
                button.update((0, 0), 0)

    def update(self, mouse_pos, events):
        if self.settings_internal_status == "settings_window":
            self.game_difficulty_slider.update(mouse_pos, events)

            for button in self.slide_buttons:
                button.update(mouse_pos, events)

            for button in self.static_buttons:
                button.update(mouse_pos, events)
                if button.check_pressed():
                    self.event_handler(button.button_code)

            animation_speed: float = 0
            # [f"EASY", f"NORMAL", f"HARD"]
            if self.game_difficulty_slider.active_difficulty == self.list_difficulty_keys[0]:
                animation_speed = 0.2
            elif self.game_difficulty_slider.active_difficulty == self.list_difficulty_keys[1]:
                animation_speed = 0.4
            elif self.game_difficulty_slider.active_difficulty == self.list_difficulty_keys[2]:
                animation_speed = 0.6

            self.animated_characters.update(animation_speed)

        elif self.settings_internal_status == "question_window":
            self.question_window.update(mouse_pos, events)
            question_window_data = self.question_window.get_data()
            if question_window_data:
                if question_window_data == f"no":
                    self.external_status = "menu_window"

                elif question_window_data == f"ok":
                    self.returning_data = {'game_difficulty': self.game_difficulty_slider.get_data(),
                                           'bg_music_volume': self.background_sound_button.get_data(),
                                           'effects_sound_volume': self.effects_sound_button.get_data()}

                    self.external_status = "menu_window"

    def draw(self):
        self.static_sprite_group.draw(self.display_surface)

        for button in self.slide_buttons:
            button.draw(self.display_surface)

        self.game_difficulty_slider.draw(self.display_surface)

        for button in self.static_buttons:
            button.draw()

        self.animated_characters.draw(self.display_surface)
        self.grass_sprite.draw(self.display_surface)

        if self.settings_internal_status == "question_window":
            self.question_window.draw()

#_____________________________________________________________________________________________________________________#
class SlidingBarButton:
    def __init__(self, center_pos: tuple, surface: pygame.Surface):
        self.pos = pygame.math.Vector2(center_pos)
        self.surface = surface
        self.moving_status: bool = False

        self.slide_distance: int = 700

        self.end_points = {'left_end_point': [self.pos.x - self.slide_distance / 2, self.pos.y],
                           'right_end_point': [self.pos.x + self.slide_distance / 2, self.pos.y]}

        self.slider_sprite = Static_centerTile(self.surface, self.pos)
        self.slider_sprite_group = pygame.sprite.GroupSingle(self.slider_sprite)

        self.sound_level_substrate = pygame.image.load('../graphics/menu_window/settings/sound_level.png').convert_alpha()
        self.sound_level_img = None
        self.sound_level_rect = None
        self.__make_sound_level_bar()

        self.button_sound = pygame.mixer.Sound('../audio/effects/jump.wav')

    def __make_sound_level_bar(self):
        self.sound_level_img = pygame.transform.scale(self.sound_level_substrate,\
                                                      (self.slide_distance + 40, self.sound_level_substrate.get_height()))

        self.sound_level_rect = self.sound_level_img.get_rect()

        temp_rect = self.sound_level_rect.copy()
        temp_rect.center = self.pos
        temp_rect.bottom -= 35
        self.true_topleft_pos = temp_rect.topleft
        self.max_sound_level_width = self.sound_level_rect.width

    def __update_sound_level_bar(self):
        translation_coefficient = self.get_data()
        self.sound_level_rect.w = self.max_sound_level_width * translation_coefficient

    def __play_button_sound(self):
        button_sound_level = self.get_data()
        self.button_sound.set_volume(button_sound_level)
        self.button_sound.play(1)

    def set_start_pos(self, settings_data: float) -> None:
        my_start_x = self.end_points['left_end_point'][0] + self.slide_distance * settings_data
        self.slider_sprite.rect.centerx = my_start_x

    def get_data(self):
        max_length = self.end_points['right_end_point'][0] - self.end_points['left_end_point'][0]
        my_length = self.slider_sprite.rect.centerx - self.end_points['left_end_point'][0]
        output = round((my_length/max_length), 2)
        return output

    def update(self, mouse_pos, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self.moving_status:
                self.__play_button_sound()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.slider_sprite.rect.collidepoint(mouse_pos):
                    self.moving_status = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.moving_status = False

        if self.moving_status:
            self.slider_sprite.rect.centerx = mouse_pos[0]
            if self.slider_sprite.rect.centerx > self.end_points['right_end_point'][0]:
                self.slider_sprite.rect.centerx = self.end_points['right_end_point'][0]

            elif self.slider_sprite.rect.centerx < self.end_points['left_end_point'][0]:
                self.slider_sprite.rect.centerx = self.end_points['left_end_point'][0]

        self.__update_sound_level_bar()

        # we put 0 here because we don't use world shift standard parameter
        # we are changing rect.x directly in for cycle upper
        self.slider_sprite.update(0)

    def draw(self, screen):
        screen.blit(self.sound_level_img, self.true_topleft_pos, self.sound_level_rect)
        self.slider_sprite_group.draw(screen)

class SlidingStepButton:
    def __init__(self, center_pos: tuple, surface: pygame.Surface):
        self.pos = pygame.math.Vector2(center_pos)
        self.surface = surface
        self.moving_status: bool = False

        self.button_sprite = Static_centerTile(self.surface, self.pos)
        self.my_font = pygame.font.SysFont("Impact", 20, False, False)

        self.slide_distance: int = 700

        self.active_difficulty = None

        self.point_surf = pygame.image.load('../graphics/menu_window/settings/BTN_END_POINT.png').convert_alpha()
        self.end_points = {'left_end_point': [self.pos.x - self.slide_distance / 2, self.pos.y],
                           'center_end_point': [self.pos.x, self.pos.y],
                           'right_end_point': [self.pos.x + self.slide_distance / 2, self.pos.y]}

        self.slider_group = pygame.sprite.GroupSingle(self.button_sprite)
        self.inscription_sprites = pygame.sprite.Group()
        self.point_sprites = pygame.sprite.Group()
        self.__create_inscription_sprites()

    def __create_inscription_sprites(self):
        list_of_titles = [f"easy", f"normal", f"hard"]
        list_of_points = list(self.end_points)
        temp_instance = 0

        for title in list_of_titles:
            point_sprite = Static_centerTile(self.point_surf, self.end_points[list_of_points[temp_instance]])

            uppercase_title = list_of_titles[temp_instance].upper()

            inscription_sur_1 = self.my_font.render(uppercase_title, 0, "black")
            inscription_sur_2 = self.my_font.render(uppercase_title, 0, "brown4")
            inscription_sprite = Static_centerDoubleTile((inscription_sur_1, inscription_sur_2), self.end_points[list_of_points[temp_instance]], title)

            #Offcet 25 pix to  to pick up sprite
            inscription_sprite.rect.bottom -= 36

            self.inscription_sprites.add(inscription_sprite)
            self.point_sprites.add(point_sprite)
            temp_instance += 1

    def set_button_to_closer_point(self):
        slider_rect_x = self.slider_group.sprite.rect.x
        sector_1 = (self.end_points['left_end_point'][0], self.end_points['left_end_point'][0] + (self.end_points['center_end_point'][0] - self.end_points['left_end_point'][0])/2)
        sector_3 = (self.end_points['center_end_point'][0] + (self.end_points['right_end_point'][0] - self.end_points['center_end_point'][0])/2, self.end_points['right_end_point'][0],)
        sector_2 = (sector_1[1], sector_3[0])
        game_difficulty_keys = list(game_difficulty)

        if slider_rect_x in range(int(sector_2[0]), int(sector_2[1])):
            self.slider_group.sprite.rect.centerx = self.end_points['center_end_point'][0]
            self.active_difficulty = game_difficulty_keys[1]

        elif slider_rect_x in range(int(sector_3[0]), int(sector_3[1])):
            self.slider_group.sprite.rect.centerx = self.end_points['right_end_point'][0]
            self.active_difficulty = game_difficulty_keys[2]
        else:
            self.slider_group.sprite.rect.centerx = self.end_points['left_end_point'][0]
            self.active_difficulty = game_difficulty_keys[0]

    def get_data(self):
        return self.active_difficulty

    def set_start_pos(self, user_difficulty_setting):
        self.active_difficulty = user_difficulty_setting
        game_difficulty_keys = list(game_difficulty.keys())

        if user_difficulty_setting == game_difficulty_keys[0]:
            self.button_sprite.rect.centerx = self.end_points['left_end_point'][0]
        elif user_difficulty_setting == game_difficulty_keys[2]:
            self.button_sprite.rect.centerx = self.end_points['right_end_point'][0]
        else:
            self.button_sprite.rect.centerx = self.end_points['center_end_point'][0]

    def update(self, mouse_pos, events):
        if self.moving_status:
            self.button_sprite.rect.centerx = mouse_pos[0]
            if self.button_sprite.rect.centerx > self.end_points['right_end_point'][0]:
                self.button_sprite.rect.centerx = self.end_points['right_end_point'][0]

            elif self.button_sprite.rect.centerx < self.end_points['left_end_point'][0]:
                self.button_sprite.rect.centerx = self.end_points['left_end_point'][0]

        # we put 0 here because we don't use world shift standard parameter in this case
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_sprite.rect.collidepoint(mouse_pos):
                    self.moving_status = True

            elif event.type == pygame.MOUSEBUTTONUP:
                self.moving_status = False
                self.set_button_to_closer_point()
        self.slider_group.update(0)

        for sprite in self.inscription_sprites:
            if sprite.tile_name == self.active_difficulty:
                sprite.update(f"active")
            else:
                sprite.update(f"disactive")

    def draw(self, screen):
        self.inscription_sprites.draw(screen)
        self.point_sprites.draw(screen)
        self.slider_group.draw(screen)
#######################################################################################################################
