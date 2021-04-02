from character import Player
from settings import *
import pygame
import pytmx
import sys
# from data import setup
# from data.main import main


__author__ = 'Delekta Kamil, Kolaszyński Przeymsław'


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sprite Example")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    player = Player()
    #all_sprites.add(player)
    # Game loop
    gameMap = pytmx.load_pygame("map_alpha.tmx")
    running = True
    while running:
        # keep loop running at the right speed
        clock.tick(FPS)
        # Process input (events)
        for event in pygame.event.get():
            # check for closing window
            if event.type == pygame.QUIT:
                running = False

        # Update
        all_sprites.update()

        # Draw / render
        for layer in gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = gameMap.get_tile_image_by_gid(gid)
                if tile != None:
                    screen.blit(tile, (x * gameMap.tilewidth, y * gameMap.tileheight))

        all_sprites.draw(screen)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()