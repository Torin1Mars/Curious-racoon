import pygame

from settings import screen_height, screen_width
from decoration import Clouds
from tiles import Static_centerTile, AnimatedNode
from support import CustomTimer

class Overworld:
    def __init__(self, current_level, screen_surface, create_level, change_game_level, total_game_time, game_data, user_login):

        # setup
        self.display_surface = screen_surface

        self.current_level = current_level
        self.create_level = create_level
        self.change_game_level = change_game_level

        self.user_login = user_login
        self.my_game_data = game_data

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 5

        # creating a bottom inscription and timer for biting
        # this sprite
        self.bottom_inscription_surf = None
        self.bottom_inscription_rect = None
        self.create_bottom_inscription()
        self.bottom_inscription_timer = CustomTimer(2)

        #background
        self.bg_image = pygame.image.load('../graphics/overworld/Bg_image.jpg').convert_alpha()
        self.bg_image.set_alpha(150)
        self.clouds = Clouds(3, screen_width, 10)

        # side score bar
        self.my_stars_score = Stars_Score(self.display_surface, len(self.my_game_data), self.my_game_data)
        self.my_time_score = TimeScore(total_game_time, self.display_surface)

        #Local timer to prevent mowing
        self.current_time = pygame.time.get_ticks()/1000
        self.timer_status = False

        self.overworld_shift_x = 0

        # sprites
        self.nodes_list = []
        self.create_nodes()
        self.create_icon()

        self.user_login_inscription = pygame.sprite.Group()
        self.create_user_login()

    def set_to_center_screen(self):
        if not self.current_level == 'level_1':
            current_level_index = list(self.my_game_data).index(self.current_level)
            icon_x = self.icon.sprite.pos.x
            if icon_x >= screen_width/2:
                offset_distance = (icon_x - screen_width/2) * -1
                for node in self.nodes_list:
                    node.translate_x(offset_distance)
                self.icon.sprite.pos = self.nodes_list[current_level_index].pos

    def create_nodes(self):
        for level, node_data in enumerate(self.my_game_data.values()):
            if self.my_stars_score.my_score >= node_data['stars_for_unlock']:
                node_object = Node(node_data, 'available', self.speed, self.display_surface)
            else:
                node_object = Node(node_data, 'locked', self.speed, self.display_surface)

            self.nodes_list.append(node_object)

    def create_user_login(self):
        user_icon_surf = pygame.image.load('../graphics/menu_window/User_icon.png').convert_alpha()
        user_icon_sprite = Static_centerTile(user_icon_surf, (50, screen_height-50))

        user_login_font = pygame.font.SysFont("Impact", 32, False, True)
        user_login_surf = user_login_font.render(f"{self.user_login}", 1, "black")
        user_login_sprite = Static_centerTile(user_login_surf, (user_icon_sprite.rect.center))
        user_login_sprite.rect.left = user_icon_sprite.rect.right + 5
        user_login_sprite.rect.bottom = user_icon_sprite.rect.bottom

        self.user_login_inscription.add(user_icon_sprite, user_login_sprite)

    def update_nodes_stars(self):
        self.my_stars_score.update_score()

        for node in self.nodes_list:
            node.update_stars()

    def draw_paths(self):
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(self.my_game_data.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, 'chartreuse3', False, points, 7)

    def create_icon(self):
        self.icon = pygame.sprite.GroupSingle()

        current_level_index = list(self.my_game_data).index(self.current_level)
        pos = self.nodes_list[current_level_index].main_bg_sprite.rect.center
        icon_sprite = Icon(pos)
        self.icon.add(icon_sprite)

    def create_bottom_inscription(self):
        text = "FOR CHOOSE PRESS SPACE"
        pos = [screen_width/2, screen_height-30]
        text_font = pygame.font.SysFont("Impact", 30, False, True)
        self.bottom_inscription_surf = text_font.render(text, 1, "black")
        self.bottom_inscription_rect = self.bottom_inscription_surf.get_rect(center=pos)

    def input(self):
        keys = pygame.key.get_pressed()
        current_level_index: int = list(self.my_game_data).index(self.current_level)

        if not self.moving and self.timer_status:
            if keys[pygame.K_d] and not self.current_level == len(self.nodes_list):
                target_node_status = self.nodes_list[current_level_index+1].status
                if target_node_status == f"available":
                    current_pos = self.nodes_list[current_level_index].detection_zone.center
                    target_pos = self.nodes_list[current_level_index+1].detection_zone.center
                    self.move_direction = self.get_movement_data(current_pos, target_pos)

                    new_level = list(self.my_game_data)[current_level_index+1]

                    self.current_level = new_level
                    self.moving = True

                    #method from Game class
                    self.change_game_level(self.current_level)

            elif keys[pygame.K_a] and current_level_index > 0:
                current_pos = self.nodes_list[current_level_index].detection_zone.center
                target_pos = self.nodes_list[current_level_index - 1].detection_zone.center
                self.move_direction = self.get_movement_data(current_pos, target_pos)

                new_level = list(self.my_game_data)[current_level_index-1]

                self.current_level = new_level
                self.moving = True

                # method from Game class
                self.change_game_level(self.current_level)

            elif keys[pygame.K_SPACE]:
                self.create_level()

    def get_movement_data(self, current_pos, target_pos):
        my_current_pos = pygame.math.Vector2(current_pos)
        my_target_pos = pygame.math.Vector2(target_pos)
        return (my_target_pos - my_current_pos).normalize()

    def update_icon_pos(self):
        my_icon = self.icon.sprite
        if self.moving and self.move_direction:

            current_level_index = list(self.my_game_data).index(self.current_level)

            levels_keys = list(self.my_game_data)

            first_level_posx = self.my_game_data[levels_keys[0]]['node_pos'][0]
            last_level_posx = self.my_game_data[levels_keys[-1]]['node_pos'][0]

            icon_near_right_border = True if my_icon.pos.x >= screen_width - 400 else False
            icon_near_left_border = True if my_icon.pos.x <= first_level_posx-10 else False

            if icon_near_right_border and self.move_direction.x > 0 or\
                    icon_near_left_border and self.move_direction.x < 0:

                target_node_obj = self.nodes_list[current_level_index]
                if target_node_obj.detection_zone.collidepoint(my_icon.pos):
                    my_icon.pos = pygame.math.Vector2(target_node_obj.detection_zone.center)
                    self.moving = False
                    self.move_direction = pygame.math.Vector2(0, 0)
                    self.overworld_shift_x = 0

                else:
                    current_pos = my_icon.pos
                    target_pos = self.nodes_list[current_level_index].detection_zone.center
                    self.move_direction = self.get_movement_data(current_pos, target_pos)
                    my_icon.pos.y += self.move_direction.y * self.speed
                    self.overworld_shift_x = self.move_direction.x * self.speed * -1

            else:
                my_icon.pos += self.move_direction * self.speed
                target_node_obj = self.nodes_list[current_level_index]
                if target_node_obj.detection_zone.collidepoint(self.icon.sprite.pos):
                    self.moving = False
                    self.move_direction = pygame.math.Vector2(0, 0)
                self.overworld_shift_x = 0

    def waiting_timer(self):
        waiting_seconds = 2
        if self.current_time + waiting_seconds < pygame.time.get_ticks()/1000:
            self.timer_status = True
            self.bottom_inscription_timer.activate()

    def run(self):
        # decorations
        self.display_surface.blit(self.bg_image, (0, 0))
        self.clouds.draw(self.display_surface, 0)

        self.update_icon_pos()

        # update nodes
        for node in self.nodes_list:
            node.update(self.overworld_shift_x)

        # updating icons
        self.icon.update()
        self.icon.draw(self.display_surface)

        # time managment
        if not self.timer_status:
            self.waiting_timer()
        self.input()

        # updating bottom_inscription
        self.bottom_inscription_timer.update()
        if self.bottom_inscription_timer.get_status():
            self.display_surface.blit(self.bottom_inscription_surf, self.bottom_inscription_rect)

        #self.draw_paths()

        # draw additional info
        self.my_stars_score.draw()
        self.my_time_score.draw()
        self.user_login_inscription.draw(self.display_surface)
#######################################################################################################################

class Icon (pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pygame.math.Vector2(pos)
        self.image = pygame.image.load('../graphics/overworld/hud_.png').convert_alpha()
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.rect.center = self.pos

#######################################################################################################################
class Node:
    def __init__(self, node_data: dict, status: str, icon_speed, screen):
        self.node_data = node_data
        self.screen = screen
        self.pos = pygame.math.Vector2(self.node_data['node_pos'])
        self.graphics_path = self.node_data['node_graphics']
        self.stars = self.node_data['node_stars']

        if status == f"available":
            self.status = f"available"
        else:
            self.status = f"locked"

        self.main_group = pygame.sprite.LayeredUpdates()
        self.stars_group = pygame.sprite.AbstractGroup()

        self.create_node()

        # We need this zone for realize proper collision between our character icon and finish trajectory point
        self.detection_zone = pygame.Rect(0, 0, icon_speed*3, icon_speed*3)
        self.detection_zone.center = self.pos

    def create_node(self):
        self.create_bg_sprite()
        self.create_down_stars(self.stars)
        self.create_lock_sigh()

        self.main_group.add(self.main_bg_sprite)
        self.main_group.add(self.stars_group)
        if self.status == f"locked":
            self.main_group.add(self.lock_sigh)

    def create_lock_sigh(self):
        lock_surf = pygame.image.load('../graphics/overworld/UI_LOCK.png').convert_alpha()
        self.lock_sigh = Static_centerTile(lock_surf, (0, 0))
        self.lock_sigh.rect.center = self.pos

    def create_bg_sprite(self):
        if self.status == f"locked":
            self.main_bg_sprite = AnimatedNode(1, self.pos.x, self.pos.y, self.graphics_path, transparent=150)
        else:
            self.main_bg_sprite = AnimatedNode(1, self.pos.x, self.pos.y, self.graphics_path)

    def create_down_stars(self, stars: int = None):
        fill_star_surf = pygame.image.load('../graphics/overworld/UI_STAR_NORMAL.png').convert_alpha()
        empty_star_surf = pygame.image.load('../graphics/overworld/UI_STAR_EMTPY.png').convert_alpha()

        if stars == 1:
            left_star = Static_centerTile(fill_star_surf, (0, 0))
            right_star = Static_centerTile(empty_star_surf, (0, 0))
            center_star = Static_centerTile(empty_star_surf, (0, 0))
        elif stars == 2:
            left_star = Static_centerTile(fill_star_surf, (0, 0))
            right_star = Static_centerTile(fill_star_surf, (0, 0))
            center_star = Static_centerTile(empty_star_surf, (0, 0))
        elif stars == 3:
            left_star = Static_centerTile(fill_star_surf, (0, 0))
            right_star = Static_centerTile(fill_star_surf, (0, 0))
            center_star = Static_centerTile(fill_star_surf, (0, 0))
        else:
            left_star = Static_centerTile(empty_star_surf, (0, 0))
            right_star = Static_centerTile(empty_star_surf, (0, 0))
            center_star = Static_centerTile(empty_star_surf, (0, 0))

        left_star.rect.center = (self.pos.x - 35, self.pos.y + 70)
        right_star.rect.center = (self.pos.x + 35, self.pos.y + 70)
        center_star.rect.center = (self.pos.x, self.pos.y + 60)

        self.stars_group.add(left_star,
                             right_star,
                             center_star)

    def translate_x(self, distance: int):
        self.pos.x += distance
        for sprite in self.main_group:
            sprite.rect.x += distance
        self.detection_zone.x += distance


    def update(self, overworld_shift_x):
        self.main_group.update(overworld_shift_x)
        self.detection_zone.centerx += overworld_shift_x
        self.main_group.draw(self.screen)

#######################################################################################################################
class Stars_Score:
    def __init__(self, screen: pygame.surface.Surface, levels_qtty, my_game_data):
        self.display_surface = screen
        self.max_stars_qtty = levels_qtty*3
        self.my_score = 0
        self.my_game_data = my_game_data

        self.star_img = pygame.image.load('../graphics/overworld/UI_STAR_LARGE.png').convert_alpha()
        self.star_img_rect = self.star_img.get_rect(center=(45, 45))

        self.score_font = pygame.font.SysFont("Impact", 45, False, True)

        self.score_img = self.score_font.render(f"{self.my_score}/{self.max_stars_qtty}", 1, 'black')
        self.score_img_rect = self.score_img.get_rect(topleft=(self.star_img_rect.right + 5,\
                                                               self.star_img_rect.centery-25))
        self.update_score()

    def update_score(self):
        for levels, level_data in enumerate(self.my_game_data.values()):
            self.my_score += level_data['node_stars']
        self.score_img = self.score_font.render(f"{self.my_score}/{self.max_stars_qtty}", 0, 'black')

    def draw(self):
        self.display_surface.blit(self.star_img, self.star_img_rect)
        self.display_surface.blit(self.score_img, self.score_img_rect)

#######################################################################################################################
class TimeScore:
    def __init__(self, time: float, screen: pygame.Surface):
        self.pos = pygame.math.Vector2(45, 135)
        self.my_time = time
        self.showing_time = None
        self.reformat_showing_time()

        self.display_surface = screen

        self.clock_img = pygame.image.load('../graphics/overworld/UI_CLOCK.png').convert_alpha()
        self.clock_sprite = Static_centerTile(self.clock_img, self.pos)

        #Upper inscription
        self.title_font = pygame.font.SysFont("Impact", 25, False, True)
        self.title_font_img = self.title_font.render(f"TOTAL TIME", 1,'black')
        self.title_font_img_sprite = Static_centerTile(self.title_font_img, self.pos)
        self.title_font_img_sprite.rect.left = self.clock_sprite.rect.right + 2
        self.title_font_img_sprite.rect.bottom = self.clock_sprite.rect.centery - 2

        self.time_score_img = self.title_font.render(f"{self.showing_time}", 1,'black')
        self.title_score_img_sprite = Static_centerTile(self.time_score_img, self.pos)
        self.title_score_img_sprite.rect.left = self.clock_sprite.rect.right + 2
        self.title_score_img_sprite.rect.top = self.clock_sprite.rect.centery + 2

        self.main_group = pygame.sprite.Group(self.clock_sprite,
                                              self.title_font_img_sprite,
                                              self.title_score_img_sprite)

    def reformat_showing_time(self):
        if self.my_time > 60:
            minutes = self.my_time // 60
            second = self.my_time % 60 * 0.01
            self.showing_time = round((minutes + second), 2)
        else:
            self.showing_time = self.my_time

    def draw(self):
        self.main_group.draw(self.display_surface)
