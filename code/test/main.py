import pygame, sys
import settings

from game import Game


pygame.init()
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('Curious Racoon')
my_game = Game(screen)

if __name__ == '__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('white')
        my_game.run(events)
        pygame.display.update()
        clock.tick(settings.fps)
