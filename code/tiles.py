import pygame
from support import import_folder, tile_size
class Tile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift_x):
        self.rect.x += shift_x

class Static_pytmxTile(pygame.sprite.Sprite):
    def __init__(self, surface, pos):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)

    def update(self,shift_x):
        self.rect.x += shift_x

class Water_pytmxTile (Static_pytmxTile):
    def __init__(self, surface, pos):
        super().__init__(surface, pos)
        self.animation_speed = 0.3
        self.animation_index = 0

    def animate(self):
        animation_limit = 5
        self.animation_index += self.animation_speed
        if self.animation_index >= animation_limit:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.animation_index = 0

    def update(self, shift_x):
        self.rect.x += shift_x
        self.animate()
class StaticTile(Tile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface

class Static_centerTile(pygame.sprite.Sprite):
    def __init__(self, surface, pos):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect(center=pos)

    def update(self, shift_x):
        self.rect.x += shift_x

class Static_centerStar(Static_centerTile):
    def __init__(self, surface, pos):
        Static_centerTile.__init__(self, surface, pos)

        self.original_scale_image = self.image
        self.original_scale_image_rect = self.original_scale_image.get_rect()

        self.animation_status: bool = True
        #prcent of scaling
        self.animation_speed: int = 2

    def _animate(self):
        if self.animation_status:
            scaling = self.animation_speed/100
            self.image = pygame.transform.scale(self.original_scale_image,\
                                                (self.original_scale_image_rect.width*scaling, self.original_scale_image_rect.height*scaling))
            self.animation_speed += 3

    def update(self, shift_x):
        self.rect.x += shift_x
        self._animate()
        if self.animation_speed >= 100:
            self.animation_status = False

class Static_centerDoubleTile(pygame.sprite.Sprite):
    def __init__(self, surfaces: tuple, pos, name:str):
        super().__init__()
        self.this_surfaces = surfaces
        self.image = self.this_surfaces[0]
        self.rect = self.image.get_rect(center=pos)
        self.tile_name = name

    def update(self, state):
        if state == f"active":
            self.image = self.this_surfaces[1]
        else:
            self.image = self.this_surfaces[0]

class Static_grassTile(Static_centerTile):
    def __init__(self, surface, pos):
        super().__init__(surface, pos)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left = pos.x
        self.rect.bottom = pos.y + tile_size + 22
class Static_snowTile(Static_centerTile):
    def __init__(self, surface, pos):
        super().__init__(surface, pos)
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left = pos.x
        self.rect.bottom = pos.y + tile_size


class CloudTile (StaticTile):
    def __init__(self,size, x, y, surface, speed_ratio):
        super().__init__(size, x, y, surface)
        self.external_speed_ratio = speed_ratio
        self.current_speed_ratio = 0
        self.name = f"cloud"

    def update(self, shift_x):
        self.current_speed_ratio += self.external_speed_ratio
        if self.current_speed_ratio >= 1.2:
            self.current_speed_ratio = 0
        self.rect.x += shift_x
        self.rect.x -= self.current_speed_ratio


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(topleft = (x,y))

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift_x):
        self.animate()
        self.rect.x += shift_x

class AnimatedNode(AnimatedTile):
    def __init__(self, size, x, y, path, transparent: int = None):
        AnimatedTile.__init__(self, size, x, y, path)
        self.frames = import_folder(path)

        if transparent:
            self.apply_transparency(transparent)

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def animate(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def apply_transparency(self, transparency):
        for frame in self.frames:
            frame.set_alpha(transparency)

class AnimatedCoin (AnimatedTile):
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(tile_size/2)
        center_y = y + int(tile_size/2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.value = value

class AnimatedPalm (AnimatedTile):
    def __init__(self, size, x, y, path, offset_x=None, offset_y=None):
        super().__init__(size, x, y, path)
        if offset_x and offset_y:
            my_offset_x = x - offset_x
            my_offset_y = y - offset_y
            self.rect.topleft = (my_offset_x, my_offset_y)
        elif offset_y:
            my_offset_y = y - offset_y
            self.rect.topleft = (x, my_offset_y)
        elif offset_x:
            my_offset_x = x - offset_x
            self.rect.topleft = (my_offset_x, y)
class AnimatedStaticPict(AnimatedTile):
    def __init__(self, size, x, y, path: str, animation_speed: float):
        AnimatedTile.__init__(self, size, x, y, path)
        self.animation_speed = animation_speed

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, animation_speed):
        self.animation_speed = animation_speed
        self.animate()
