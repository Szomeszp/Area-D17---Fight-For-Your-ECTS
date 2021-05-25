from os import path

import pygame as pg

from settings import IMG_FOLDER, TILESIZE


class Item(pg.sprite.Sprite):
    def __init__(self, game, map, x, y):
        self.game = game
        self.map = map
        self.groups = map.all_sprites, map.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.x = x
        self.y = y


class HealthPotion(Item):
    def __init__(self, game, map, x, y, health, image_name):
        super().__init__(game, map, x, y)
        self.health = health
        self.image = pg.image.load(path.join(IMG_FOLDER, image_name + ".png"))
