import pygame as pg
from settings import *
vec = pg.math.Vector2
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        # Refactor needed
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
        if dx == 1:
            self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_R))
        if dx == -1:
            self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_L))
        if dy == 1:
            self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_D))
        if dy == -1:
            self.image = pg.image.load(path.join(img_folder, PLAYER_IMG_U))

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE