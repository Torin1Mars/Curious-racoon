import pygame, sys
import settings

from support import read_json_data, update_json_data

from overworld import Overworld
from level import Level
from sound import Soundbar

from start_window import Start_window
from menu_window import MenuWindow
from level_end_window import Level_end_window

from leaderboard import sort_leader_table
from ui import Cursor


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

        self.user_data: dict = {}
        self.user_settings: dict = {}
        self.total_game_time: float = 0

        # audio
        self.my_sound = Soundbar()
        self.game_cursor = Cursor()

        # starting initialization
        self.current_level: str = "level_1"
        self.overworld = None
        self.level = None
        self.menu_window = None
        self.level_end_window = None

        self.start_window = Start_window(screen)
        self.my_sound.start_window_bg_music.play(loops=-1)

    def __load_general_game_data(self):
        self.game_data = read_json_data(f"../code/game_data.json")

    def __apply_game_settings(self, new_settings: dict) -> None:
        self.user_settings = new_settings
        self.my_sound.set_settings(self.user_settings)
        self.user_data['game_settings'] = new_settings

    def __load_user_game_data(self, game_data_from_start_window: dict) -> None:
        self.user_data = game_data_from_start_window
        self.user_login = self.user_data['user_login']
        self.total_game_time = self.user_data['game_time']
        del self.user_data['user_login']
        game_settings = self.user_data['game_settings']
        self.__apply_game_settings(game_settings)

    def _check_new_record(self):
        my_stars: int = 0
        my_levels_stars = self.user_data["levels_stars"]
        for level in my_levels_stars:
            my_stars += my_levels_stars[level]

        my_game_mode = self.user_settings['game_difficulty'].upper()

        my_indicators: dict = {"Total_time": self.total_game_time,
                                "Total_stars": my_stars,
                                "Game_mode": my_game_mode}

        my_data = read_json_data('../code/leader_table.json')
        leaderboard_data = my_data['leaderTable']
        sorted_table = sort_leader_table(leaderboard_data)

        if self.user_login in sorted_table:
            better_time:bool = True if my_indicators["Total_time"] < sorted_table[self.user_login]["Total_time"] else False
            more_stars:bool = True if my_indicators["Total_stars"] > sorted_table[self.user_login]["Total_stars"] else False
            if better_time or more_stars:
                sorted_table[self.user_login] = my_indicators

        elif len(sorted_table) < 10:
            sorted_table[self.user_login] = my_indicators

        else:
            sorted_table[self.user_login] = my_indicators
            sorted_table = sort_leader_table(sorted_table)

            if len(sorted_table) > 10:
                sorted_table.popitem()

        new_data: dict = {'leaderTable': sorted_table}
        update_json_data(new_data, '../code/leader_table.json')

    def _restart_my_game(self):
        #reseting all level's stars
        my_levels = self.user_data['levels_stars']
        for level in my_levels:
            my_levels[level] = 0

        #reseting my game time
        self.total_game_time = 0

    def change_game_level(self, new_level: int):
        self.current_level = new_level

    def change_status(self, new_status: str):
        self.status = new_status

    def update_total_game_time(self, time: float):
        self.total_game_time += time

    def create_level(self):
        self.game_cursor.hide_cursor(flag=True)
        current_level_data = self.game_data[self.current_level]
        self.level = Level(current_level_data, screen, self.my_sound,self.user_data['game_settings']['game_difficulty'])
        self.status = 'level'
        self.my_sound.play_level_bg_music()

    def create_overworld(self):
        self.game_cursor.hide_cursor(flag=False)
        self.overworld = Overworld(self.current_level, screen, self.create_level, self.change_game_level,\
                                   self.total_game_time, self.game_data, self.user_login, self.user_data)
        self.overworld.set_to_center_screen()
        self.status = 'overworld'
        self.my_sound.play_overworld_bg_music()

    def check_menu(self, events: pygame.event.Event = None, flag: bool = None):
        if flag:
            self.game_cursor.hide_cursor(flag=False)
            self.menu_window = MenuWindow(screen, self.change_status, self.my_sound.mute_status, self.user_login, self.user_data, self.game_cursor.hide_cursor)
            self.menu_window.previous_status = self.status
            self.status = 'menu_window'

        elif events:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    #we need this state when game is new and level hasn't been created yet
                    if event.key == pygame.K_ESCAPE and not self.level:
                        self.game_cursor.hide_cursor(flag=False)
                        self.menu_window = MenuWindow(screen, self.change_status, self.my_sound.mute_status, self.user_login, self.user_data, self.game_cursor.hide_cursor)
                        self.menu_window.previous_status = self.status
                        self.status = 'menu_window'

                    # in all another stages we are using this state
                    elif event.key == pygame.K_ESCAPE and not self.level.level_internal_state == 'pause_window':
                        self.game_cursor.hide_cursor(flag=False)
                        self.menu_window = MenuWindow(screen, self.change_status, self.my_sound.mute_status, self.user_login, self.user_data, self.game_cursor.hide_cursor)
                        self.menu_window.previous_status = self.status
                        self.status = 'menu_window'

    def run(self, events):
        mouse_pos = pygame.mouse.get_pos()
        if self.status == 'start_window':
            self.start_window.run(mouse_pos, events)

            if self.start_window.get_status() == 'overworld':
                user_data = self.start_window.get_data()
                self.__load_user_game_data(user_data)

                self.my_sound.start_window_bg_music.stop()
                self.status = 'overworld'
                self.create_overworld()

        elif self.status == 'overworld':
            self.overworld.update(mouse_pos, events)
            self.overworld.run()
            self.check_menu(events)

            pressed_buttons = self.overworld.pressed_buttons_codes
            if self.overworld.static_buttons_data['menu_button']['bt_menu_code'] in pressed_buttons:
                self.check_menu(flag=True)

        elif self.status == 'level':
            self.level.run(events)
            if self.level.player_win or self.level.player_loose:

                self.game_cursor.hide_cursor(flag=False)
                if self.level.player_win:

                    if self.user_data['levels_stars'][self.current_level] < self.level.earned_stars:
                        self.user_data['levels_stars'][self.current_level] = self.level.earned_stars
                        #adding time in secound not in minuts
                        self.update_total_game_time(int(self.level.ui.level_time))
                        self.user_data['game_time'] = self.total_game_time

                    # checking if player completed the game by calculating stars for each level
                    # and if all level have some stars it means that player completed the game
                    game_completed: bool = True
                    my_levels_stars = self.user_data['levels_stars']
                    for level in my_levels_stars:
                        if my_levels_stars[level] == 0:
                            game_completed = False

                    if game_completed:
                        self._check_new_record()
                        self.level_end_window = Level_end_window(screen, f"win", self.level.earned_stars, self.my_sound,
                                                                 last_level_flag=True)
                        self.status = 'level_end_window'

                    else:
                        self.level_end_window = Level_end_window(screen, f"win", self.level.earned_stars, self.my_sound,
                                                                 last_level_flag=False)
                        self.status = 'level_end_window'

                else:
                    # updating player data
                    self.update_total_game_time(int(self.level.ui.level_time))
                    self.user_data['game_time'] = self.total_game_time

                    self.level_end_window = Level_end_window(screen, f"loose", 0, self.my_sound, last_level_flag=False)
                    self.status = 'level_end_window'

            self.check_menu(events)

        elif self.status == 'level_end_window':
            self.level_end_window.run(mouse_pos, events)
            data_from_window = self.level_end_window.get_data()
            if data_from_window == "yes":
                self.my_sound.stop_end_level_music()
                self._restart_my_game()
                self.create_overworld()
            elif data_from_window == "no":
                self.my_sound.stop_end_level_music()
                self.create_overworld()

        elif self.status == 'menu_window':
            self.menu_window.update(mouse_pos, events)
            self.menu_window.draw()
            data = self.menu_window.get_data()
            if data:
                if self.menu_window.images_data['bt_map_code'] in data['data_from_menu']:
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
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
pygame.display.set_caption('Curious Racoon')

app_icon = pygame.image.load('../code/Racoon_preview.png').convert_alpha()
pygame.display.set_icon(app_icon)

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
