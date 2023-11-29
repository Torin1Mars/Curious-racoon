import pygame
from settings import screen_height, screen_width
from tiles import StaticTile, Static_centerTile
from buttons import StaticButton
from support import read_json_data
import random

class Leaderboard:
    def __init__(self, screen: pygame.surface.Surface, leader_table_data):
        self.display_surface = screen
        self.leader_data = leader_table_data

        self.returning_data = None

        self.static_tiles = pygame.sprite.Group()
        self.__create_static_sprites()

        self.buttons_list: list = []
        self.__create_buttons()

        self.table_font = pygame.font.SysFont("Arial", 18, True, True)
        self.table_group = pygame.sprite.Group()

        self.sorted_table: dict = {}
        self._make_leader_table()
        self._render_leader_table()

    def __create_static_sprites(self):
        center_screen = (screen_width/2, screen_height/2)
        bg_image = pygame.image.load('../graphics/menu_window/leaderboard/bg_leaderboard.png').convert_alpha()
        bg_image_sprite = Static_centerTile(bg_image, center_screen)

        bg_cup_image = pygame.image.load('../graphics/menu_window/leaderboard/bg_cup.png').convert_alpha()
        bg_cup_image.set_alpha(150)
        bg_cup_sprite = Static_centerTile(bg_cup_image, center_screen)
        bg_cup_sprite.rect.centery -= 40

        table_image = pygame.image.load('../graphics/menu_window/leaderboard/win_table.png').convert_alpha()
        table_sprite = Static_centerTile(table_image, center_screen)
        #table_sprite.rect.centery -= 40

        self.static_tiles.add(bg_image_sprite,bg_cup_sprite,table_sprite)

    def __create_buttons(self):
        temp_surf_1 = pygame.image.load('../graphics/menu_window/leaderboard/Bt_ok_1.png').convert_alpha()
        temp_surf_2 = pygame.image.load('../graphics/menu_window/leaderboard/Bt_ok_2.png').convert_alpha()
        pos = (screen_width/2, screen_height-80)
        button_ok = StaticButton(pos, (temp_surf_1, temp_surf_2), self.display_surface, 1)
        self.buttons_list.append(button_ok)

    def __sort_leader_table(self, leader_table):
        def get_sorted_key(item):
            my_item = item[1]
            time = my_item['Total_time']
            stars = my_item['Total_stars']
            return time, -stars

        sorted_table = {}
        sorted_list = sorted(leader_table.items(), key=get_sorted_key, reverse=False)
        for key, value in sorted_list:
            sorted_table[key] = value

        return sorted_table

    def _make_leader_table(self):
        my_data = read_json_data('../code/leader_table.json')
        leader_table: dict = my_data['leaderTable']

        self.sorted_table = self.__sort_leader_table(leader_table)

    def _render_leader_table(self):
        center_screen_x = screen_width/2
        start_y = 190
        spacing = 42

        inscriptions_list = []
        for key, value in self.sorted_table.items():
            row: list = []
            row.append(key)
            for key, data in value.items():
                row.append(data)
            inscriptions_list.append(row)

        top_list: int = 3
        for row in inscriptions_list:
            substrate_height: float = 0
            substrate_width: float = 700

            inscriptions_in_row: list = []
            for inscription in row:
                if top_list:
                    text_inscription = self.table_font.render(str(inscription), 1, 'darkred')
                    text_inscription_height = text_inscription.get_height()
                    if substrate_height < text_inscription_height:
                        substrate_height = text_inscription_height
                    inscriptions_in_row.append(text_inscription)
                else:
                    text_inscription = self.table_font.render(str(inscription), 1, 'black')

                    text_inscription_height = text_inscription.get_height()
                    if substrate_height < text_inscription_height:
                        substrate_height = text_inscription_height
                    inscriptions_in_row.append(text_inscription)

            substrate_surface = pygame.surface.Surface((substrate_width, substrate_height), pygame.SRCALPHA)

            left_pos_list: list = [65, 275, 450, 600]
            pos_index: int = 0
            for my_inscription in inscriptions_in_row:
                if not pos_index:
                    substrate_surface.blit(my_inscription, (left_pos_list[pos_index], 0))
                    pos_index += 1

                else:
                    substrate_surface.blit(my_inscription, (left_pos_list[pos_index], 0))
                    pos_index += 1

            substrate_sprite = Static_centerTile(substrate_surface, (center_screen_x, start_y))
            start_y += spacing
            self.table_group.add(substrate_sprite)

            if top_list:
                top_list -= 1

    def get_data(self):
        return self.returning_data if self.returning_data else None

    def update(self, mouse_pos, events):
        for button in self.buttons_list:
            button.update(mouse_pos, events)
            if button.check_pressed():
                self.returning_data = button.button_code

        self.table_group.update(0)

    def draw(self):
        self.static_tiles.draw(self.display_surface)
        self.table_group.draw(self.display_surface)

        for button in self.buttons_list:
            button.draw()
