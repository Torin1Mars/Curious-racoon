import pygame

class StaticButton:
    def __init__(self, pos: tuple, surfaces: tuple, screen: pygame.Surface, button_code: int):
        self.button_code = button_code
        self.pressed = False
        self.pos = pos
        self.display_surface = screen
        self.surfaces_dict = {'first_image': surfaces[0],
                              'second_image': surfaces[1]}

        self.image_rect = self.surfaces_dict['first_image'].get_rect()
        self.image_rect.center = pos

        self.collision = False

    def check_pressed(self):
        if self.pressed:
            return True
        else:
            return False

    def update(self, mouse_pos, events):
        self.pressed = False
        if self.image_rect.collidepoint(mouse_pos):
            self.collision = True
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pressed = True
        else:
            self.collision = False

    def draw(self):
        if self.collision:
            self.display_surface.blit(self.surfaces_dict['second_image'], self.image_rect)
        else:
            self.display_surface.blit(self.surfaces_dict['first_image'], self.image_rect)

class StaticSoundButton:
    def __init__(self, pos: tuple, surfaces: tuple, screen, button_code: int, mute_status):
        self.pos = pos

        self.display_surface = screen
        self.button_code = button_code
        self.pressed: bool = False
        self.mute_status: bool = mute_status

        self.mouse_collide: bool = False

        self.surfaces = surfaces

        self.active_surface = self.surfaces[0]

        # main rectangle for whole button
        self.main_rect = self.active_surface.get_rect(center=self.pos)

        self.active_surface_with_circle = self.active_surface.copy()
        pygame.draw.circle(self.active_surface_with_circle, "white",\
                           (self.main_rect.width / 2, self.main_rect.height / 2),\
                           self.main_rect.height / 2, width=5)

        self.deactivated_surface = self.surfaces[1]
        self.deactivated_surface_with_circle = self.deactivated_surface.copy()
        pygame.draw.circle(self.deactivated_surface_with_circle, "white",\
                            (self.main_rect.width/2, self.main_rect.height/2),\
                             self.main_rect.height/2, width=5)

    def __change_mute_status(self):
        if self.mute_status:
            self.mute_status = False
        else:
            self.mute_status = True

    def draw(self):
        if self.mouse_collide:
            if self.mute_status:
                self.display_surface.blit(self.deactivated_surface_with_circle, self.main_rect)
            else:
                self.display_surface.blit(self.active_surface_with_circle, self.main_rect)
        else:
            if self.mute_status:
                self.display_surface.blit(self.deactivated_surface, self.main_rect)
            else:
                self.display_surface.blit(self.active_surface, self.main_rect)

    def check_pressed(self):
        if self.pressed:
            return True
        else:
            return False

    def update(self, mouse_pos, events):
        self.pressed = False
        if self.main_rect.collidepoint(mouse_pos):
            self.mouse_collide = True
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__change_mute_status()
                    self.pressed = True
        else:
            self.mouse_collide = False

