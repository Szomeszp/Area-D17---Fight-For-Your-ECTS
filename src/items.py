import pygame as pg
from os import path
from settings import IMG_FOLDER, TILE_SIZE


class Item(pg.sprite.Sprite):
    def __init__(self, game, map, x, y):
        self.groups = map.all_sprites, map.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.map = map
        self.game = game
        self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y


class HealthPotion(Item):
    def __init__(self, game, map, x, y, health, image_name):
        super().__init__(game, map, x, y)
        self.health = health
        self.image = pg.image.load(path.join(IMG_FOLDER, image_name + ".png"))


class Key(pg.sprite.Sprite):
    def __init__(self, game, map, x, y):
        self.groups = map.all_sprites, map.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.map = map
        self.game = game
        self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y
        self.image = pg.image.load(path.join(IMG_FOLDER, "key" + ".png"))
