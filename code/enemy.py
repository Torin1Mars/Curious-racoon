import pygame
from tiles import AnimatedTile
from random import randint
from settings import game_difficulty

class Enemy(AnimatedTile):
    def __init__(self,size, x, y, my_game_difficulty, offset_x=None, offset_y=None):
        super().__init__(size, x, y, '../graphics/enemy/walk')
        self.my_game_difficulty = my_game_difficulty

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

        self.speed:int = 0
        self.__apply_game_dificulty()

        #This instruction needs to set proper start directions of characters
        self.speed *= -1
        self.goes_right = True

    def __apply_game_dificulty(self):
        if self.my_game_difficulty == game_difficulty['hard']:
            self.speed = randint(3, 6)
        elif self.my_game_difficulty == game_difficulty['normal']:
            self.speed = randint(2, 4)
        else:
            # game_difficulty['easy']:
            self.speed = randint(1, 3)

    def move (self):
        self.rect.x -= self.speed
    def reverse_image (self):
        if self.speed >= 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1
    def animate (self):
        self.frame_index += 0.3
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift_x):
        self.rect.x += shift_x

        self.animate()
        self.move()

        self.reverse_image()
