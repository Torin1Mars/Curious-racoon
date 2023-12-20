import pygame
from settings import fps
from support import CustomTimer


class UI:
    def __init__(self, screen: pygame.surface.Surface, max_level_time: int):
        # setup
        self.display_surface = screen
        self.max_level_time = max_level_time

        # health
        self.health_bar = pygame.image.load('../graphics/ui/health_bar_2.png').convert_alpha()
        self.health_bar_topleft = (40, 35)
        self.bar_max_width = 182
        self.bar_height = 12

        # coins
        self.coin = pygame.image.load('../graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(center=(38, 85))
        self.font = pygame.font.SysFont("Impact", 30, False, True)

        # timer settings
        self.time_per_frame = round(1 / fps, 3)
        self.level_time = 0
        self.showing_time = 0
        self.timer_font = pygame.font.SysFont("Impact", 25, False, True)
        self.clock_surf = pygame.image.load('../graphics/ui/clock.png').convert_alpha()
        self.clock_rect = self.clock_surf.get_rect(center=(39, 135))

        # internal status
        self.pause = False

        # my local timer settings
        self.my_timer = CustomTimer(3)
        self.timer_status = False

    def __update_timer(self):
        if not self.pause:
            self.level_time += self.time_per_frame
            time_in_second = int(self.level_time)

            if time_in_second > 60:
                minutes = time_in_second // 60
                second = time_in_second % 60 * 0.01
                self.showing_time = round((minutes + second), 2)
            else:
                self.showing_time = time_in_second

        if self.timer_status:
            self.my_timer.update()

    def __draw_timer(self):
        # if we're staying in level more than 15 sec, timer will be red
        if (self.max_level_time - self.level_time) <= 20:
            self.timer_surf = self.timer_font.render(f"{self.showing_time}", 1, "brown3")
            if not self.timer_status:
                self.timer_status = True
                self.my_timer.activate()
        else:
            self.timer_surf = self.timer_font.render(f"{self.showing_time}", 1, "black")
        self.timer_rect = self.timer_surf.get_rect(topleft=(self.clock_rect.right + 10, self.clock_rect.top + 8))
        self.display_surface.blit(self.clock_surf, self.clock_rect)
        self.display_surface.blit(self.timer_surf, self.timer_rect)

    def show_health(self, current, full):
        self.display_surface.blit(self.health_bar, (12, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio
        health_bar_rect = pygame.Rect((55, 40), (current_bar_width, self.bar_height))
        pygame.draw.rect(self.display_surface, 'chartreuse3', health_bar_rect, 0, 4)

    def pause_time(self):
        self.pause = True

    def push_time(self):
        self.pause = False

    def show_coins(self, amount, max_level_amount):
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(f"{amount}/{max_level_amount}", False, 'black')
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 5, self.coin_rect.centery))
        self.display_surface.blit(coin_amount_surf, coin_amount_rect)

    def show_timer(self):
        self.__update_timer()
        # time image would be blinking when time runs out
        if not self.timer_status:
            self.__draw_timer()
        elif self.timer_status and self.my_timer.get_status():
            self.__draw_timer()


#######################################################################################################################
class Cursor:
    def __init__(self):
        self.my_cursor_surf_1 = pygame.image.load('../graphics/ui/CRS_HAND.png').convert_alpha()
        self.my_cursor_surf_2 = pygame.Surface((self.my_cursor_surf_1.get_width(), self.my_cursor_surf_1.get_height()),
                                               pygame.SRCALPHA)

        self.my_cursor_1 = pygame.cursors.Cursor((0, 0), self.my_cursor_surf_1)
        self.my_cursor_2 = pygame.cursors.Cursor((0, 0), self.my_cursor_surf_2)
        pygame.mouse.set_cursor(self.my_cursor_1)

    def hide_cursor(self, flag: bool) -> None:
        # if flag is True we are hiding game cursor
        if flag:
            pygame.mouse.set_cursor(self.my_cursor_2)
        else:
            pygame.mouse.set_cursor(self.my_cursor_1)
