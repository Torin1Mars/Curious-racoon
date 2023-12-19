import pygame
from settings import screen_width, screen_height
from support import CustomTimer, read_json_data
from additional_windows import YesNoWindow
from buttons import StaticButton, StaticClickButton

class Start_window:
    def __init__(self, screen):
        self.screen = screen
        self.output_status = 'start_window'

        self.showing_time = 5

        self.bg_surface = pygame.image.load('../graphics/start_window/Jungle_bg.jpg').convert_alpha()
        self.bg_rect = self.bg_surface.get_rect(topleft=(0, 0))

        # Animation settings
        # case for pygame image
        self.pygame_image_state_1 = False
        self.pygame_image_state_2 = False
        self.pygame_image_animation_speed = 2
        self.pygame_image_start_pos = pygame.math.Vector2(-screen_width / 2, 445)
        self.pygame_image_finish_pos = pygame.math.Vector2(screen_width / 2, 445)
        # case for racoon image
        self.racoon_image_state_1 = True
        self.racoon_image_state_2 = False
        self.racoon_image_animation_speed = 2
        self.racoon_image_start_pos = pygame.math.Vector2(screen_width / 2, -500)
        self.racoon_image_finish_pos = pygame.math.Vector2(screen_width / 2, 100)

        self.botton_title_pos = pygame.math.Vector2(screen_width / 2, 560)
        self.botton_input_title = Bottom_input_field(self.screen, self.botton_title_pos)

        self.import_data()

        # For button inscription  title
        self.button_inscription_surf = pygame.image.load('../graphics/start_window/Title.png').convert_alpha()
        self.button_inscription_rect = self.button_inscription_surf.get_rect(center=(screen_width / 2, 630))
        self.button_title_surf_status = False

        self.user_data:dict = {}
        self.users_savings:dict = {}

    def import_data(self):
        self.pygame_image = pygame.image.load('../graphics/start_window/pygame_logo.png').convert_alpha()
        self.pygame_image_rect = self.pygame_image.get_rect(center=self.pygame_image_start_pos)

        self.racoon_image = pygame.image.load('../graphics/start_window/racoon.png').convert_alpha()
        self.racoon_image_rect = self.pygame_image.get_rect(center=self.racoon_image_start_pos)

    def get_status(self):
        return self.output_status

    def animate_pygame_image(self):
        if self.pygame_image_rect.centerx < self.pygame_image_finish_pos.x + 150 and self.pygame_image_state_1:
            self.pygame_image_rect.x += self.pygame_image_animation_speed
            self.pygame_image_animation_speed += 2
        elif self.pygame_image_rect.centerx >= self.pygame_image_finish_pos.x and self.pygame_image_state_1:
            self.pygame_image_state_1 = False
            self.pygame_image_state_2 = True
            self.pygame_image_animation_speed = 2

        if self.pygame_image_rect.centerx > self.pygame_image_finish_pos.x and self.pygame_image_state_2:
            self.pygame_image_rect.x -= self.pygame_image_animation_speed
            self.pygame_image_animation_speed += 2
        elif self.pygame_image_rect.centerx <= self.pygame_image_finish_pos.x and self.pygame_image_state_2:
            self.pygame_image_state_2 = False
            self.pygame_image_animation_speed = 2

            self.botton_input_title.title_external_status = True
            self.button_title_surf_status = True

    def animate_racoon_image(self):
        if self.racoon_image_rect.centery < self.racoon_image_finish_pos.y + 200 and self.racoon_image_state_1:
            self.racoon_image_rect.y += self.racoon_image_animation_speed
            self.racoon_image_animation_speed += 2
        elif self.racoon_image_rect.centery >= self.racoon_image_finish_pos.y and self.racoon_image_state_1:
            self.racoon_image_state_1 = False
            self.racoon_image_state_2 = True
            self.racoon_image_animation_speed = 2

        if self.racoon_image_rect.centery > self.racoon_image_finish_pos.y and self.racoon_image_state_2:
            self.racoon_image_rect.y -= self.racoon_image_animation_speed
            self.racoon_image_animation_speed += 3
        elif self.racoon_image_rect.centery <= self.racoon_image_finish_pos.y and self.racoon_image_state_2:
            self.racoon_image_state_2 = False
            self.pygame_image_state_1 = True
            self.racoon_image_animation_speed = 2

    def draw(self):
        self.screen.blit(self.bg_surface, self.bg_rect)
        self.screen.blit(self.pygame_image, self.pygame_image_rect)
        self.screen.blit(self.racoon_image, self.racoon_image_rect)

        if self.button_title_surf_status:
            self.screen.blit(self.button_inscription_surf, self.button_inscription_rect)

    def update(self):
        self.animate_racoon_image()
        self.animate_pygame_image()
        self.output_status = self.botton_input_title.status

    def get_data(self):
        if self.user_data:
            return self.user_data
        else:
            return 0

    def run(self, mouse_pos, events):
        self.update()
        self.botton_input_title.update(mouse_pos, events)

        if self.botton_input_title.user_data:
            self.user_data = self.botton_input_title.user_data

        self.draw()
        self.botton_input_title.draw()

class Bottom_input_field:
    def __init__(self, screen: pygame.Surface, pos: pygame.math.Vector2):
        self.screen = screen
        self.pos = pos
        # Saving time when object was created

        self.existing_users_savings:dict = {}
        self.load_users_savings()

        self.status = "start_window"

        # template surface
        self.template_surface = pygame.image.load('../graphics/start_window/UI_BAR.png').convert_alpha()
        self.template_surface.set_alpha(150)
        self.template_surface_rect = self.template_surface.get_rect(center=(pos.x + 25, pos.y - 10))
        self.template_surface_state = False

        # Settings for text title
        self.title_status = False
        self.title_external_status = False
        self.title_font = pygame.font.Font('../graphics/start_window/ARCADEPI.ttf', 20)
        self.input_font = pygame.font.Font('../graphics/start_window/ARCADEPI.ttf', 25)
        self.bottom_inscription_surf = self.title_font.render('Please set name :', False, 'white')
        self.bottom_inscription_rect = self.bottom_inscription_surf.get_rect(right=pos.x - 5, bottom=pos.y)

        # Settings for input_text title
        self.input_box_surf = self.input_font.render(f"", False, 'white')
        self.input_box_rect = self.input_box_surf.get_rect(left=self.pos.x + 5, bottom=self.pos.y + 2)
        self.allowed_litters_low = str("qwertyuiopasdfghjklzxcvbnm")
        self.allowed_litters_top = self.allowed_litters_low.upper()
        self.allowed_litters:str
        self._construct_allowed_litres()

        self.input_text = ''
        self.user_login: str = ""
        self.input_text_status = False

        # Additional timer for invisible status
        self.template_surface_timer = CustomTimer(4, 4)
        self.image_status = False

        self.user_data: dict = {}
        self.question_window = None

        #pop-up menu
        self.arrow_button = None
        self._make_arrow_button()

        self.substrate_surf: pygame.Surface = None
        self.substrate_rect: pygame.rect.Rect = None
        self.substrate_topleft_pos = pygame.math.Vector2(590, 254)
        self._make_substrate()


        self.logins_buttons_font = pygame.font.Font('../graphics/start_window/ARCADEPI.ttf', 20)
        self.logins_buttons_list: list = []
        self._make_logins_list_buttons()

        self.animation_speed: int = 3
        self.substrate_area_rect = self.substrate_rect.copy()
        self.substrate_area_rect.topleft = (0, 0)
        self.substrate_area_rect.height = 0

        self.animation_state: bool = False
        self.animation_direction: str = 'None'
        self.current_y: int = self.substrate_topleft_pos.y + self.substrate_rect.height

    def _animate_users_login_list(self):
        if self.animation_state and (self.animation_direction == "up"):
            if self.substrate_area_rect.height < self.substrate_rect.height:
                self.substrate_area_rect.height += self.animation_speed
                self.substrate_area_rect.top = self.substrate_rect.height - self.substrate_area_rect.height
                self.current_y = (self.substrate_topleft_pos.y + self.substrate_rect.height) - self.substrate_area_rect.height
                self.animation_speed += 0.5

            else:
                self.substrate_area_rect.top = 0
                self.substrate_area_rect.height = self.substrate_rect.height
                self.current_y = self.substrate_topleft_pos.y
                self.animation_state = False

                self.animation_speed: int = 3

        elif self.animation_state and (self.animation_direction == "down"):
            if self.substrate_area_rect.height > 0:
                self.substrate_area_rect.height -= self.animation_speed
                self.substrate_area_rect.top = self.substrate_rect.height - self.substrate_area_rect.height
                self.current_y = (self.substrate_topleft_pos.y + self.substrate_rect.height) - self.substrate_area_rect.height

                self.animation_speed += 0.5
            else:
                self.substrate_area_rect.top = self.substrate_rect.height
                self.substrate_area_rect.height = 0
                self.current_y = self.substrate_topleft_pos.y + self.substrate_rect.height
                self.animation_state = False

                self.animation_speed: int = 3

                # update images buttons to set them to default
                for button in self.logins_buttons_list:
                    button.clicked = False

    def _construct_allowed_litres(self):
        allowed_litters_low = str("qwertyuiopasdfghjklzxcvbnm")
        allowed_litters_top = self.allowed_litters_low.upper()
        allowed_litters_symbols = str("._-1234567890")

        self.allowed_litters = allowed_litters_top + allowed_litters_low + allowed_litters_symbols

    def _make_arrow_button(self):
        img_btn_1 = pygame.image.load('../graphics/start_window/Btn_Sizing_1.png').convert_alpha()
        img_btn_2 = pygame.image.load('../graphics/start_window/Btn_Sizing_2.png').convert_alpha()
        img_btn_code: int = 1
        pos = (self.template_surface_rect.right-40, self.template_surface_rect.centery)
        self.arrow_button = StaticClickButton(pos, (img_btn_1, img_btn_2), self.screen, img_btn_code)

    def _make_substrate(self):
        self.substrate_surf = pygame.image.load('../graphics/start_window/Bg_substrate.png').convert_alpha()
        self.substrate_rect = self.substrate_surf.get_rect()
        self.substrate_rect.topleft = self.substrate_topleft_pos

    def _make_logins_list_buttons(self):
        users_logins = list(self.existing_users_savings['users_logins'])
        users_logins.pop(0)

        pos_x = self.substrate_rect.left+30
        pos_y = self.substrate_rect.bottom-15
        y_space = 25

        for user in users_logins:
            surf_1 = self.logins_buttons_font.render(f"{user}", False, 'white')
            surf_2 = self.logins_buttons_font.render(f"{user}", False, 'brown4')
            button_code = user
            button = StaticClickButton((0, 0), (surf_1, surf_2), self.screen, button_code)
            button.image_rect.left = pos_x
            button.image_rect.bottom = pos_y
            self.logins_buttons_list.append(button)

            pos_y -= y_space

    def load_users_savings(self):
        self.existing_users_savings = read_json_data(f"../code/users_data.json")

    def update_input(self, mouse_pos, events):
        # updating buttons
        self.arrow_button.update(mouse_pos, events)
        if self.arrow_button.pressed:
            if self.animation_direction == "up":
                self.animation_direction = "down"
                self.animation_state = True
            else:
                self.animation_direction = "up"
                self.animation_state = True

        self._animate_users_login_list()

        #updating user's logins buttons
        for button in self.logins_buttons_list:
            if button.image_rect.top > self.current_y:
                button.update(mouse_pos, events)
                if button.pressed:
                    self.input_text = button.button_code
                    self.animation_state = True
                    self.animation_direction = "down"

        max_sight = 14
        for event in events:
            if event.type == pygame.KEYDOWN:
                if self.input_text and event.key == pygame.K_ESCAPE:
                    self.input_text = ""

                elif self.input_text and event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text.rstrip(self.input_text[-1])

                elif len(self.input_text) >= max_sight:
                    self.input_text = self.input_text

                elif event.unicode in self.allowed_litters:
                    self.input_text += event.unicode

                if event.key == pygame.K_RETURN and self.input_text:
                    self.user_login = self.input_text

                    if self.user_login in self.existing_users_savings['users_logins']:
                        row_1 = f"Welcome back"
                        row_2 = f"{self.user_login}"
                        row_3 = f"Would you like to load"
                        row_4 = f" your game progress?"
                        self.question_window = YesNoWindow(self.screen, (screen_width / 2, 300), (460, 350), (row_1, row_2, row_3, row_4))
                        self.question_window.inscription_font = pygame.font.SysFont("Impact", 20, False, True)
                        self.status = "question_window"
                    else:
                        self.user_data = self.existing_users_savings['users_logins']['default']
                        self.user_data['user_login'] = self.user_login
                        self.status = "overworld"

            self.input_box_surf = self.input_font.render(f"{self.input_text}", False, 'white')

    def update(self, mouse_pos, events: pygame.event.Event):
        '''
        Timer is controlling image state in period of time which given by parameter when timer was initialised
        '''
        self.template_surface_timer.update()
        if self.status == "start_window":
            if self.title_external_status:
                self.template_surface_timer.activate()
                self.title_external_status = False
                self.template_surface_state = True
                self.input_text_status = True

            if self.template_surface_timer.get_status():
                self.image_status = True
            elif not self.template_surface_timer.get_status():
                self.image_status = False

            if self.input_text_status:
                self.update_input(mouse_pos, events)

        elif self.status == "question_window":
            self.question_window.update(mouse_pos, events)
            question_window_data = self.question_window.get_data()
            if question_window_data:
                if question_window_data == f"no":
                    data = read_json_data(f"../code/users_data.json")
                    self.user_data = data['users_logins']['default']
                    self.user_data['user_login'] = self.user_login

                    #self.__pack_user_data(self.user_login, data['users_logins']['default_settings'], f"new")
                    self.status = "overworld"

                elif question_window_data == f"ok":
                    data = read_json_data(f"../code/users_data.json")
                    self.user_data = data['users_logins'][self.user_login]
                    self.user_data['user_login'] = self.user_login

                    #self.__pack_user_data(self.user_login, data['users_logins'][self.user_login], f"existing")
                    self.status = "overworld"

    def draw(self):
        if self.template_surface_state:
            self.screen.blit(self.template_surface, self.template_surface_rect)

        if self.image_status:
            self.screen.blit(self.bottom_inscription_surf, self.bottom_inscription_rect)

        if self.input_text_status:
            self.screen.blit(self.input_box_surf, self.input_box_rect)

            self.screen.blit(self.substrate_surf, (self.substrate_topleft_pos.x, self.current_y), self.substrate_area_rect)

            # updating buttons
            self.arrow_button.draw()
            for button in self.logins_buttons_list:
                if button.image_rect.top > self.current_y:
                    button.draw()

        if self.status == "question_window":
            self.question_window.draw()
