import pygame
import settings
from support import import_folder, CustomTimer

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, display_surface, create_jump_particles, change_health, bg_shift_x, sound, game_difficulty):
        super().__init__()
        # Animation settings
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.2
        self.image = self.animations['idle'][self.frame_index]

        # Additional player effects
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_run_animation_speed = 0.15

        self.create_jump_particles = create_jump_particles

        # Health management
        self.change_health = change_health
        self.invincible = False
        self.invincibilyty_duration = 2000
        self.hurt_time = 0

        # Player status
        self.status = 'idle'
        self.saved_status = self.status
        self.right_facing_direction = True
        self.player_on_ground = False
        self.player_on_ceiling = False
        self.player_on_left = False
        self.player_on_right = False

        # General settings
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.display_surface = display_surface

        # Player movement
        self.player_direction = pygame.math.Vector2(0, 0)
        self.gravity = settings.default_gravity
        self.speed = game_difficulty
        self.jump_height = settings.default_jump_height
        self.collision_rect = pygame.Rect(self.rect)
        self.collision_rect = pygame.Rect(self.rect.left+7, self.rect.top+5, 45, 60)

        # Audio
        self.player_sound = sound

        # Timer for invisible status
        self.timer = CustomTimer(10, 3)

        # Custom inertia parameters for control shift background
        self.max_inertia = 10
        self.inertia_speed_x = 0.35
        self.inertia_speed_y = 1
        self.inertia_x = 0
        self.inertia_y = 0

        # Callable Bg shift y method when player is jumping
        self.bg_shift_x = bg_shift_x

    def import_character_assets(self):
        character_path = '../animation_assets/character/'
        self.animations = {'idle': [],
                           'run': [],
                           'jump': [],
                           'fall': []}
        for animation in self.animations.keys():
            full_path = character_path+animation
            self.animations[animation] = import_folder (full_path)
    def import_dust_run_particles(self):
        self.dust_run_particles = \
            import_folder('../animation_assets/character/dust_particles/run')

    def animate(self):
        animation = self.animations[self.status]

        #Loop over animation frame index
        if self.saved_status != self.status:
            self.frame_index = 0
        else:
            self.frame_index += self.animation_speed

        #Next
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.right_facing_direction==True:
            self.image = image
            self.rect.bottomleft = self.collision_rect.bottomleft
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
            self.rect = self.image.get_rect()
            self.rect.bottomright = self.collision_rect.bottomright

        if self.invincible:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def run_dust_animation(self):
        if self.status == 'run' and self.player_on_ground and not self.invincible:
            self.dust_frame_index += self.dust_run_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

        #Positioning of dust particles
            if self.right_facing_direction:
                pos = self.rect.bottomleft - pygame.math.Vector2(10, 8)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(0, 8)
                reversed_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(reversed_dust_particle, pos)

    def get_status(self):
        if self.player_direction.y < 0:
            self.status = 'jump'
        elif self.player_direction.y > settings.default_gravity+0.5:
            self.status = 'fall'
        else:
            if self.player_direction.x != 0:
                self.status = 'run'
                # This is local coefficient for increasing speed of run animation
                self.frame_index += 0.3
            else:
                self.status = 'idle'

    def save_actual_status(self, status):
        self.saved_status = status

    # Character's moving
    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_direction.x = -1
            self.right_facing_direction = False
            self.inertia_x += self.inertia_speed_x

        elif keys[pygame.K_d]:
            self.player_direction.x = 1
            self.right_facing_direction = True
            self.inertia_x += self.inertia_speed_x

        else:
            self.player_direction.x = 0
            self.inertia_x = 0

        if keys[pygame.K_SPACE] and self.player_on_ground:
            self.player_jump()
            self.player_sound.play_effect_sound('jump_sound')

            if not self.invincible:
                self.create_jump_particles(self.rect.midbottom)

    def apply_gravity(self):
        self.player_direction.y += self.gravity
        self.collision_rect.y += self.player_direction.y
    def player_jump(self):
        self.player_direction.y = self.jump_height

    def get_damage(self):
        if not self.invincible:
            self.change_health(-15)
            self.invincible = True
            self.hurt_time = pygame.time.get_ticks()
            self.player_sound.play_effect_sound('hit_sound')
            self.timer.activate()

    def check_invisibility(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.hurt_time >= self.invincibilyty_duration:
                self.invincible = False

    def wave_value(self) -> int:
        '''
        :return: alfa parameter
        '''
        if self.timer.get_status():
            return 255
        elif not self.timer.get_status():
            return 0

    def recalculate_inertia(self):
        #Additional function for increase inertia y mass when player in air
        if not self.status == 'fall' or not self.status == 'jump':
            self.inertia_y = 0

        if self.inertia_x >= self.max_inertia:
            self.inertia_x = self.max_inertia - 1

        if self.inertia_y >= self.max_inertia:
            self.inertia_y = self.max_inertia - 1

    def reset_inertia(self, direction):
        if direction == "x":
            self.inertia_x = 0
        if direction == "y":
            self.inertia_y = 0

    def update(self):
        self.get_input()
        self.get_status()

        self.animate()
        self.run_dust_animation()

        self.save_actual_status(self.status)
        self.check_invisibility()
        self.timer.update()
        self.recalculate_inertia()

        #DEBUG
        #pygame.draw.rect(self.display_surface, 'red', self.collision_rect,5,5)