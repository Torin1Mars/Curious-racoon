import pygame
from settings import screen_height, screen_width
from tiles import Static_centerTile
from buttons import StaticButton


class Leaderboard:
    def __init__(self, screen: pygame.surface.Surface, leader_data):
        self.display_surface = screen
        self.leader_data = leader_data

        self.returning_data = None

        self.static_tiles = pygame.sprite.Group()
        self.__create_static_sprites()

        self.buttons_list: list = []
        self.__create_buttons()

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

    def get_data(self):
        return self.returning_data if self.returning_data else None
    def update(self, mouse_pos, events):
        for button in self.buttons_list:
            button.update(mouse_pos, events)
            if button.check_pressed():
                self.returning_data = button.button_code
    def draw(self):
        self.static_tiles.draw(self.display_surface)

        for button in self.buttons_list:
            button.draw()
