import pygame as pg
from settings import *
vec = pg.math.Vector2
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.image_type = game.player_img
        self.image = pg.image.load(path.join(self.img_folder, game.player_img.value))
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        door = self.collide_with_door()
        if door:
            self.game.render_map(door)
        else:
            if not self.collide_with_walls(dx, dy):
                self.x += dx
                self.y += dy
            if dx == 1:
                self.change_player_img(PlayerImg.RIGHT2, PlayerImg.RIGHT)
            if dx == -1:
                self.change_player_img(PlayerImg.LEFT2, PlayerImg.LEFT)
            if dy == 1:
                self.change_player_img(PlayerImg.DOWN2, PlayerImg.DOWN)
            if dy == -1:
                self.change_player_img(PlayerImg.UP2, PlayerImg.UP)

    def stand(self):
        if self.image_type == PlayerImg.RIGHT or self.image_type == PlayerImg.RIGHT2:
            self.image_type = PlayerImg.STATIC_RIGHT
            self.image = pg.image.load(path.join(self.img_folder, PlayerImg.STATIC_RIGHT.value))
        elif self.image_type == PlayerImg.LEFT or self.image_type == PlayerImg.LEFT2:
            self.image_type = PlayerImg.STATIC_LEFT
            self.image = pg.image.load(path.join(self.img_folder, PlayerImg.STATIC_LEFT.value))
        elif self.image_type == PlayerImg.DOWN or self.image_type == PlayerImg.DOWN2:
            self.image_type = PlayerImg.STATIC_DOWN
            self.image = pg.image.load(path.join(self.img_folder, PlayerImg.STATIC_DOWN.value))
        elif self.image_type == PlayerImg.UP or self.image_type == PlayerImg.UP2:
            self.image_type = PlayerImg.STATIC_UP
            self.image = pg.image.load(path.join(self.img_folder, PlayerImg.STATIC_UP.value))

    def change_player_img(self, image1, image2):
        if self.image_type == image1:
            self.image_type = image2
            self.image = pg.image.load(path.join(self.img_folder, image2.value))
        else:
            self.image_type = image1
            self.image = pg.image.load(path.join(self.img_folder, image1.value))

    def collide_with_walls(self, dx=0, dy=0):
        rect_copy = self.rect
        rect_copy.x += dx * TILESIZE
        rect_copy.y += dy * TILESIZE
        # pygame.rect.collidelistall instead of for loop
        for wall in self.game.walls:
            if rect_copy.colliderect(wall.rect):
                return True
        return False

    def collide_with_door(self, dx=0, dy=0):
        rect_copy = self.rect
        rect_copy.x += dx * TILESIZE
        rect_copy.y += dy * TILESIZE
        # pygame.rect.collidelistall instead of for loop
        for door in self.game.doors:
            if rect_copy.colliderect(door.rect):
                return door
        return None

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, map):
        self.groups = game.doors  # ?
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map = map


class SecretDoor(Door):
    def __init__(self, game, x, y, w, h, map):
        super().__init__(game, x, y, w, h, map)
        self.groups = game.doors, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.image = pg.image.load(path.join(self.img_folder, "stairs1.png"))
        # self.image.fill(GREEN)
