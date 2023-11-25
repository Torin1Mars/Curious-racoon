import pygame
import pytmx

from settings import*

class TiledMap :
    def __init__(self, filename):
        self.filename = filename
        tmx_data = pytmx.load_pygame(self.filename, pixelalpha = True)
        self.width = tmx_data.width*tmx_data.tilewidth
        self.height =(tmx_data.height+1)*tmx_data.tilewidth

        self.tmx_map = tmx_data

    def render(self):
        tmx_layers = self.tmx_map.visible_layers

        for layer in tmx_layers:
            if layer.name == "test":
                for x, y, gid, in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    if (tile != None):
                        print(gid)
                        print(tile)
                        print (type(tile))

    def make_map (self):
        temp_surface = pygame.Surface((self.width,self.height))
        self.render()
        return temp_surface


'''pygame.init()
screen = pygame.display.set_mode((800,600))
tile = TiledMap('../levels/level_data/level_0.tmx')
tile.render(screen)'''

