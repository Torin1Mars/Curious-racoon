import pygame, sys
import settings

from support import read_json_data

from overworld import Overworld
from level import Level
from sound import Soundbar

from settings import game_difficulty
from start_window import Start_window
from menu_window import MenuWindow

#######################################################################################################################
#######################################################################################################################
class Game:
    def __init__(self):
        # game attributes
        self.status = 'start_window'
        # 'start_window'
        # 'menu_window'
        # 'overworld'
        # 'level'
        self.user_login: str = ""
        self.game_data: dict = {}
        self.__load_general_game_data()

        # game_difficulty parameter controls characters and enemy's speed
        self.user_settings: dict = {'game_difficulty': "normal",
                                    'bg_music_volume': 0.8,
                                    'effects_sound_volume': 0.3,
                                    'mute_status': False}
        self.total_game_time: float = 0

        # audio
        self.my_sound = Soundbar(self.user_settings)

        # starting initialization
        self.current_level: str = "level_1"
        self.overworld = None
        self.level = None
        self.menu_window = None

        self.start_window = Start_window(screen)
        self.my_sound.start_window_bg_music.play(loops=-1)

    def __load_general_game_data(self):
        self.game_data = read_json_data(f"../code/game_data.json")

    def __apply_game_settings(self, user_settings: dict) -> None:
        self.user_settings['game_difficulty'] = user_settings['game_difficulty']
        self.user_settings['bg_music_volume'] = user_settings['bg_music_volume']
        self.user_settings['effects_sound_volume'] = user_settings['effects_sound_volume']

        self.my_sound.set_settings(user_settings)

    def __load_existing_game_progress(self, my_progress: dict) -> None:
        progress = my_progress
        self.total_game_time = progress['game_time']

        for level in progress['levels_stars']:
            self.game_data[level]['node_stars'] = progress['levels_stars'][level]

    def __load_existing_game_data(self, game_data_from_start_window: dict) -> None:
        my_player_settings = game_data_from_start_window
        self.user_login = my_player_settings['user_login']
        self.__apply_game_settings(my_player_settings['user_data']['game_settings'])
        if my_player_settings['user_status'] == f"existing":
            my_progress = my_player_settings['user_data']
            self.__load_existing_game_progress(my_progress)

    def change_game_level(self, new_level: int):
        self.current_level = new_level

    def change_status(self, new_status: str):
        self.status = new_status

    def update_total_game_time(self, time: float):
        self.total_game_time += time
    def create_level(self):
        current_level_data = self.game_data[self.current_level]
        self.level = Level(current_level_data, screen, self.my_sound, game_difficulty[self.user_settings['game_difficulty']])
        self.status = 'level'
        self.my_sound.play_level_bg_music()

    def create_overworld(self):
        self.overworld = Overworld(self.current_level, screen, self.create_level, self.change_game_level,\
                                   self.total_game_time, self.game_data)
        self.overworld.set_to_center_screen()
        self.status = 'overworld'
        self.my_sound.play_overworld_bg_music()

    def check_menu(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and not self.level:
                    self.menu_window = MenuWindow(screen, self.change_status, self.my_sound.mute_status, self.user_settings)
                    self.menu_window.previous_status = self.status
                    self.status = 'menu_window'

                elif event.key == pygame.K_ESCAPE and not self.level.level_internal_state == 'pause_window':
                    self.menu_window = MenuWindow(screen, self.change_status, self.my_sound.mute_status, self.user_settings)
                    self.menu_window.previous_status = self.status
                    self.status = 'menu_window'

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.status == 'start_window':
            self.start_window.run(events)

            if self.start_window.get_status() == 'overworld':
                user_data = self.start_window.get_data()
                if user_data:
                    self.__load_existing_game_data(user_data)

                self.my_sound.start_window_bg_music.stop()
                self.status = 'overworld'
                self.create_overworld()

        elif self.status == 'overworld':
            self.overworld.run()
            self.check_menu(events)

        elif self.status == 'level':
            self.level.run(events)
            if self.level.player_win or self.level.player_lose:
                if self.level.player_win:
                    if self.game_data[self.current_level]['node_stars'] < self.level.earned_stars:
                        self.game_data[self.current_level]['node_stars'] = self.level.earned_stars

                #adding time in secound not in minuts
                    self.total_game_time += int(self.level.ui.level_time)
                else:
                    self.total_game_time += int(self.level.ui.level_time)
                self.create_overworld()
            self.check_menu(events)

        elif self.status == 'menu_window':
            self.menu_window.update(mouse_pos, events)
            self.menu_window.draw()
            data = self.menu_window.get_data()
            if data:
                if 0 in data['data_from_menu']:
                    self.status = self.menu_window.previous_status
                elif self.menu_window.images_data['bt_menu_code'] in data['data_from_menu']:
                    self.my_sound.overworld_bg_music.stop()
                    self.create_overworld()
                elif self.menu_window.images_data['bt_sound_code'] in data['data_from_menu']:
                    self.my_sound.change_mute_mode()

                if data['data_from_settings']:
                    self.__apply_game_settings(data['data_from_settings'])
                    self.create_overworld()


#######################################################################################################################
#######################################################################################################################

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Curious Racoon')
my_game = Game()

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('white')
        my_game.run(events)
        pygame.display.update()
        clock.tick(settings.fps)
