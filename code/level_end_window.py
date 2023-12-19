import pygame
from random import randint

from tiles import Static_centerStar
from buttons import StaticButton
from leaderboard import Leaderboard
from additional_windows import YesNoWindow

from settings import screen_width, screen_height

class Level_end_window:
    def __init__(self, screen, status, stars_qtty, my_sound, last_level_flag):
        self.internal_status: str = "level_end_window"
        self.display_surface = screen

        self.status = status
        self.external_data = None

        #playng proper sound in game
        self.my_sound = my_sound
        self.my_sound.play_end_level_music(self.status)

        self.stars_qtty = stars_qtty
        self.last_level_flag = last_level_flag

        self.center_screen = pygame.math.Vector2(screen_width/2, screen_height/2)
        self.bg_img = pygame.image.load('../graphics/level_end_window/Bg_image.jpg').convert_alpha()
        self.bg_img.set_alpha(200)
        self.bg_img_rect = self.bg_img.get_rect(center=self.center_screen)

        self.raccoon_img_pos = pygame.math.Vector2(screen_width/2, screen_height/2)
        self.raccoon_img = None
        self.raccoon_img_alpha:int = 0
        self.raccoon_img_rect = None

        self.raccoon_img_pos = pygame.math.Vector2(screen_width/2, screen_height/2+200)
        self.inscription_img = None
        self.inscription_img_rect = None
        self.inscription_img_state_1: bool = True
        self.inscription_img_state_2: bool = False
        self.inscription_img_finish_y = None
        self.inscription_img_speed:float = 1

        self.stars_status:bool = False
        self.stars_group = pygame.sprite.Group()
        self._make_base_img()
        self._make_stars()

        self.static_button = None
        self._make_static_button()

        self.my_leaderboard = None

        self.question_window = None
        if self.last_level_flag:
            row_1 = f"CONGRATULATIONS"
            row_2 = f"Would you like to reset"
            row_3 = f"your game progress?"
            self.question_window = YesNoWindow(self.display_surface, (screen_width / 2, 300), (460, 350),\
                                           (row_1, row_2, row_3))

    def _make_base_img(self):
        my_choice = randint(1, 2)

        if self.status == "win":
            if my_choice == 1:
                self.raccoon_img = pygame.image.load('../graphics/level_end_window/Im_win_1.png').convert_alpha()
                self.raccoon_img_rect = self.raccoon_img.get_rect(center=(self.center_screen.x, self.center_screen.y-120))
            else:
                self.raccoon_img = pygame.image.load('../graphics/level_end_window/Im_win_2.png').convert_alpha()
                self.raccoon_img_rect = self.raccoon_img.get_rect(center=(self.center_screen.x, self.center_screen.y-120))

            self.raccoon_img.set_alpha(self.raccoon_img_alpha)

            self.inscription_img = pygame.image.load('../graphics/level_end_window/Win.png').convert_alpha()
            self.inscription_img_rect = self.inscription_img.get_rect()
            self.inscription_img_rect.centerx = self.center_screen.x

            self.inscription_img_finish_y = 400
            self.inscription_img_rect.top = screen_height+50

        elif self.status == "loose":
            if my_choice == 1:
                self.raccoon_img = pygame.image.load('../graphics/level_end_window/Im_loose_1.png').convert_alpha()
                self.raccoon_img_rect = self.raccoon_img.get_rect(center=(self.center_screen.x, self.center_screen.y-120))
            else:
                self.raccoon_img = pygame.image.load('../graphics/level_end_window/Im_loose_2.png').convert_alpha()
                self.raccoon_img_rect = self.raccoon_img.get_rect(center=(self.center_screen.x, self.center_screen.y-120))

            self.inscription_img = pygame.image.load('../graphics/level_end_window/Loose.png').convert_alpha()
            self.inscription_img_rect = self.inscription_img.get_rect()
            self.inscription_img_rect.centerx = self.center_screen.x

            self.inscription_img_finish_y = 400
            self.inscription_img_rect.top = screen_height+50

    def _make_stars(self):

        empty_star = pygame.image.load('../graphics/level_end_window/St_empty.png').convert_alpha()
        full_star = pygame.image.load('../graphics/level_end_window/St_full.png').convert_alpha()
        if self.stars_qtty == 1:
            left_star = Static_centerStar(full_star, (0, 0))
            right_star = Static_centerStar(empty_star, (0, 0))
            center_star = Static_centerStar(empty_star, (0, 0))
        elif self.stars_qtty == 2:
            left_star = Static_centerStar(full_star, (0, 0))
            right_star = Static_centerStar(full_star, (0, 0))
            center_star = Static_centerStar(empty_star, (0, 0))
        elif self.stars_qtty == 3:
            left_star = Static_centerStar(full_star, (0, 0))
            right_star = Static_centerStar(full_star, (0, 0))
            center_star = Static_centerStar(full_star, (0, 0))
        else:
            left_star = Static_centerStar(empty_star, (0, 0))
            right_star = Static_centerStar(empty_star, (0, 0))
            center_star = Static_centerStar(empty_star, (0, 0))

        left_star.rect.center = (self.center_screen.x-90, self.inscription_img_finish_y+200)
        right_star.rect.center = (self.center_screen.x+90, self.inscription_img_finish_y+200)
        center_star.rect.center = (self.center_screen.x, self.inscription_img_finish_y+180)

        self.stars_group.add(left_star,
                             right_star,
                             center_star)

    def _make_static_button(self):
        if self.last_level_flag:
            bt_surf_1 = pygame.image.load('../graphics/level_end_window/Bt_top_table_1.png').convert_alpha()
            bt_surf_2 = pygame.image.load('../graphics/level_end_window/Bt_top_table_2.png').convert_alpha()
            bt_code: int = 1
            self.static_button = StaticButton((screen_width-185, screen_height-50), (bt_surf_1, bt_surf_2),
                                              self.display_surface, bt_code)
        else:
            bt_surf_1 = pygame.image.load('../graphics/level_end_window/Bt_next_1.png').convert_alpha()
            bt_surf_2 = pygame.image.load('../graphics/level_end_window/Bt_next_2.png').convert_alpha()
            bt_code: int = 2
            self.static_button = StaticButton((screen_width-100, screen_height-50),(bt_surf_1, bt_surf_2),self.display_surface, bt_code)

    def _animate_racoon_image(self):
        self.raccoon_img.set_alpha(self.raccoon_img_alpha)
        self.raccoon_img_alpha += 10

    def get_data(self):
        if self.external_data:
            return self.external_data
        else:
            return None

    def _animate_inscription_image(self):
        if self.inscription_img_rect.centery > self.inscription_img_finish_y-50 and self.inscription_img_state_1:
            self.inscription_img_rect.centery -= self.inscription_img_speed
            self.inscription_img_speed += 0.8
        elif self.inscription_img_rect.centery < self.inscription_img_finish_y-50 and self.inscription_img_state_1:
            self.inscription_img_state_1 = False
            self.inscription_img_state_2 = True
            self.inscription_img_speed = 2

        if self.inscription_img_rect.top < self.inscription_img_finish_y and self.inscription_img_state_2:
            self.inscription_img_rect.centery += self.inscription_img_speed
            self.inscription_img_speed += 0.4
        elif self.inscription_img_rect.top > self.inscription_img_finish_y and self.inscription_img_state_2:
            self.inscription_img_state_1 = False
            self.inscription_img_state_2 = False
            self.inscription_img_speed = 0
            self.inscription_img_rect.top = self.inscription_img_finish_y

            #starting animate bottom stars
            self.stars_status = True

    def event_handler(self, code):
        if code == 1:
            self.my_leaderboard = Leaderboard(self.display_surface)
            self.internal_status = "leaderboard"

        elif code == 2:
            self.external_data = "no"

        elif code == 3:
            self.internal_status = "question_window"

        elif code == 4:
            self.external_data = "yes"

        elif code == 5:
            self.external_data = "no"

    def update(self, mouse_pos, events):
        if self.raccoon_img_alpha < 250:
            self._animate_racoon_image()
        if self.raccoon_img_alpha >= 250:
            self._animate_inscription_image()

        #this is only stage when buttom stars starting to bliting
        if self.stars_status:
            self.stars_group.update(0)
            self.static_button.update(mouse_pos, events)
            if self.static_button.check_pressed():
                self.event_handler(self.static_button.button_code)

    def draw(self):
        self.display_surface.blit(self.raccoon_img, self.raccoon_img_rect)
        self.display_surface.blit(self.inscription_img, self.inscription_img_rect)

        if self.stars_status:
            self.stars_group.draw(self.display_surface)
            self.static_button.draw()

    def run(self, mouse_pos, events):
        self.display_surface.blit(self.bg_img, self.bg_img_rect)
        if self.internal_status == "level_end_window":
            self.update(mouse_pos, events)
            self.draw()

        elif self.internal_status == "leaderboard":
            self.my_leaderboard.update(mouse_pos, events)
            self.my_leaderboard.draw()

            data_from_leaderboard = self.my_leaderboard.get_data()
            if data_from_leaderboard:
                self.event_handler(3)

        elif self.internal_status == "question_window":
            self.question_window.update(mouse_pos, events)

            self.my_leaderboard.draw()
            self.question_window.draw()

            question_window_data = self.question_window.get_data()
            if question_window_data:
                if question_window_data == f"ok":
                    self.event_handler(4)
                else:
                    self.event_handler(5)
