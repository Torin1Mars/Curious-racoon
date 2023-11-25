from csv import reader
import json

import settings
from settings import tile_size
from os import walk

import pytmx
import pygame


# List of supporting functions
def import_csv_layout(path):
    my_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            my_map.append(list(row))
        return my_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[1] / tile_size)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles

def import_pytmx_surface(tmx_data_path: str, layer_name: str) -> list:
    surfaces_list = []
    tmx_data = pytmx.load_pygame(tmx_data_path, pixelalpha=True)
    for layer in tmx_data.visible_layers:
        if layer.name == layer_name:
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if (tile != None):
                    surface = tile.convert_alpha()
                    pos = pygame.math.Vector2(x, y) * settings.tile_size
                    result_surface = [surface, pos]
                    surfaces_list.append(result_surface)
            return surfaces_list
def import_folder(path):
    surface_list = []
    for _, __, image_files in walk(path):
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def read_json_data(path):
    with open(path, 'r') as file:
        data = json.load(file)
        return data

class CustomTimer():
    def __init__(self, times_per_second: int, time_range: int = None):
        self.times_per_second = round(1 / times_per_second, 3)
        self.time_range = time_range

        self.internal_timer_status = False
        self.status = False

        self.internal_range_time = 0
        self.internal_time = 0

    def activate(self):
        self.internal_timer_status = True
        current_time = round(pygame.time.get_ticks() / 1000, 3)
        self.internal_range_time = current_time
        self.internal_time = current_time

    def __change_status__(self):
        if self.status:
            self.status = False
        elif not self.status:
            self.status = True

    def get_status(self):
        return self.status

    def run(self):
        current_time = round(pygame.time.get_ticks() / 1000, 3)
        if not self.time_range:
            if current_time >= self.internal_time + self.times_per_second:
                self.internal_time = current_time
                self.__change_status__()
        else:
            if self.internal_timer_status and self.internal_range_time + self.time_range >= current_time:
                if current_time >= self.internal_time + self.times_per_second:
                    self.internal_time = current_time
                    self.__change_status__()
            if not self.internal_range_time + self.time_range >= current_time:
                self.internal_timer_status = False

    def update(self):
        if self.internal_timer_status:
            self.run()
