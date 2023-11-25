import pygame
from settings import screen_width, screen_height
from tiles import Static_centerTile
from buttons import StaticButton
from support import CustomTimer


class TournamentWindow:
    def __init__(self, screen: pygame.surface.Surface, tournament_data: dict):
        self.display_surface = screen
        self.tournament_data = tournament_data

        self.main_sprite_group = pygame.sprite.Group
        self.__make_tournament_window()

    def __make_tournament_window(self):
        pass

    def draw(self):
        self.main_sprite_group.draw(self.display_surface)


#######################################################################################################################
class PauseWindow:
    def __init__(self, change_level_internal_state, ui_push_time):
        self.change_level_internal_state = change_level_internal_state
        self.ui_push_time = ui_push_time
        self.bg_surface = pygame.surface.Surface((screen_width + 10, screen_height + 10),
                                                 pygame.SRCALPHA).convert_alpha()
        self.bg_rect = self.bg_surface.get_rect(center=(screen_width / 2, screen_height / 2))

        self.pause_logo = pygame.image.load('../graphics/pause_window/Bt_pause_1.png').convert_alpha()
        self.pause_logo_rect = self.pause_logo.get_rect(center=(screen_width / 2, 250))

        # settings fo bottom inscription
        self.bottom_inscription_text = 'PRESS SPACE FOR CONTINUE'
        self.inscription_font = pygame.font.SysFont('impact', 30)
        self.inscription_surf = self.inscription_font.render(self.bottom_inscription_text, 0, 'black')
        self.inscription_surf_rect = self.inscription_surf.get_rect(
            center=(screen_width / 2, self.pause_logo_rect.bottom + 50))
        self.bottom_inscription_status = True

        # timer settings
        self.my_timer = CustomTimer(2, 3)

    def grab_screen(self, surface):
        self.bg_surface = surface.copy()
        self.bg_surface.set_alpha(120)
        self.bg_rect = self.bg_surface.get_rect(center=(screen_width / 2, screen_height / 2))

    def update(self, events):
        self.my_timer.update()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.change_level_internal_state('level')
                    self.ui_push_time()

        if self.my_timer.get_status():
            self.bottom_inscription_status = True
        else:
            self.bottom_inscription_status = False

    def draw(self, screen):
        screen.blit(self.bg_surface, self.bg_rect)
        screen.blit(self.pause_logo, self.pause_logo_rect)
        if self.bottom_inscription_status:
            screen.blit(self.inscription_surf, self.inscription_surf_rect)


#######################################################################################################################
class YesNoWindow:
    def __init__(self, screen: pygame.Surface, pos: tuple, size: tuple, question_inscription: tuple):
        self.display_surface = screen
        self.pos = pygame.math.Vector2(pos)
        self.size = size
        self.returning_data = None

        self.bg_surface = pygame.image.load(
            '../graphics/additional_windows/yes_no_window/Bg_template.png').convert_alpha()
        self.bg_surface = pygame.transform.scale(self.bg_surface, (self.size))
        self.bg_surface_rect = self.bg_surface.get_rect()
        self.bg_surface_sprite = Static_centerTile(self.bg_surface, self.pos)

        self.question_inscription = question_inscription
        self.inscription_font = pygame.font.SysFont("Impact", 30, False, True)
        self.line_spacing: int = 10
        self.static_sprites = pygame.sprite.LayeredUpdates(self.bg_surface_sprite)

        self.surf_path: dict = {'Bt_ok_1': f"../graphics/additional_windows/yes_no_window/Bt_ok_1.png",
                                'Bt_ok_2': f"../graphics/additional_windows/yes_no_window/Bt_ok_2.png",

                                'Bt_no_1': f"../graphics/additional_windows/yes_no_window/Bt_no_1.png",
                                'Bt_no_2': f"../graphics/additional_windows/yes_no_window/Bt_no_2.png"}

        self.buttons = []
        self.__create_buttons()
        self.__create_inscription()

    def __create_buttons(self):
        temp_surf_1 = pygame.image.load(self.surf_path['Bt_ok_1']).convert_alpha()
        temp_surf_2 = pygame.image.load(self.surf_path['Bt_ok_2']).convert_alpha()
        button_ok = StaticButton((50, 50), (temp_surf_1, temp_surf_2), self.display_surface, f"ok")
        button_ok.image_rect.bottom = self.bg_surface_sprite.rect.bottom - 45
        button_ok.image_rect.right = self.bg_surface_sprite.rect.centerx - 35

        temp_surf_1 = pygame.image.load(self.surf_path['Bt_no_1']).convert_alpha()
        temp_surf_2 = pygame.image.load(self.surf_path['Bt_no_2']).convert_alpha()
        button_no = StaticButton((50, 50), (temp_surf_1, temp_surf_2), self.display_surface, f"no")
        button_no.image_rect.bottom = self.bg_surface_sprite.rect.bottom - 45
        button_no.image_rect.left = self.bg_surface_sprite.rect.centerx + 35

        self.buttons.extend([button_ok, button_no])

    def __create_inscription(self):
        substrate_width: float = 0
        substrate_height: float = 0
        for row in self.question_inscription:
            text_img = self.inscription_font.render(row, 1, 'black')
            if substrate_width < text_img.get_width():
                substrate_width = text_img.get_width() + 40
            substrate_height += text_img.get_height()

        substrate_height += self.line_spacing * len(self.question_inscription) - 2

        substrate_surf = pygame.image.load('../graphics/additional_windows/yes_no_window/Substrate.png').convert_alpha()
        substrate_surf = pygame.transform.scale(substrate_surf, (substrate_width, substrate_height))
        substrate_sprite = Static_centerTile(substrate_surf, (self.pos.x, 0))

        substrate_sprite.rect.top = self.bg_surface_sprite.rect.centery - 105
        self.static_sprites.add(substrate_sprite)

        temp_height_pos: int = 0
        for row in self.question_inscription:
            text_img = self.inscription_font.render(row, 1, 'black')
            img_height = text_img.get_height()

            text_img_sprite = Static_centerTile(text_img, (self.pos.x, 0))
            text_img_sprite.rect.top = substrate_sprite.rect.top + self.line_spacing + temp_height_pos

            self.static_sprites.add(text_img_sprite)
            temp_height_pos += img_height

    def get_data(self):
        return self.returning_data

    def update(self, mouse_pos, events):
        for button in self.buttons:
            button.update(mouse_pos, events)
            if button.check_pressed():
                self.returning_data = button.button_code

        self.static_sprites.update(0)

    def draw(self):
        self.static_sprites.draw(self.display_surface)
        for button in self.buttons:
            button.draw()
