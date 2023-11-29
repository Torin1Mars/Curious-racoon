import pygame, sys
import settings
from testing import TiledMap

pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height),pygame.SRCALPHA)
clock = pygame.time.Clock()
my_map = TiledMap('../levels/level_data/level_0.tmx')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("grey")
    level_map = my_map.make_map()
    map_rect = level_map.get_rect()
    screen.blit(level_map,map_rect)
    pygame.display.update()
    clock.tick(settings.fps)
