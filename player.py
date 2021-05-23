import random

import pygame as pg
from sprites import Character
from statistics import *
from settings import *
vec = pg.math.Vector2
from os import path

class Player(pg.sprite.Sprite, Character):
    def __init__(self, game, map, x, y, type, stats=None):
        Character.__init__(self, game, x, y, type, Statistics(1000, 40, 10, 10, 10, 1, 2, 20, 50))
        self.groups = map.all_sprites
        self.map = map
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.getImage()

    def getImage(self):
        return pg.image.load(path.join(IMG_FOLDER, self.game.player_img.value))

    def move(self, dx=0, dy=0):
        door = self.collide_with_door()
        if door:
            self.game.get_through_door(door)
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
        if self.game.arena:
            self.type = PlayerImg.STATIC_UP
            self.image = pg.image.load(path.join(IMG_FOLDER, PlayerImg.STATIC_UP.value))
        elif self.type == PlayerImg.RIGHT or self.type == PlayerImg.RIGHT2:
            self.type = PlayerImg.STATIC_RIGHT
            self.image = pg.image.load(path.join(IMG_FOLDER, PlayerImg.STATIC_RIGHT.value))
        elif self.type == PlayerImg.LEFT or self.type == PlayerImg.LEFT2:
            self.type = PlayerImg.STATIC_LEFT
            self.image = pg.image.load(path.join(IMG_FOLDER, PlayerImg.STATIC_LEFT.value))
        elif self.type == PlayerImg.DOWN or self.type == PlayerImg.DOWN2:
            self.type = PlayerImg.STATIC_DOWN
            self.image = pg.image.load(path.join(IMG_FOLDER, PlayerImg.STATIC_DOWN.value))
        elif self.type == PlayerImg.UP or self.type == PlayerImg.UP2:
            self.type = PlayerImg.STATIC_UP
            self.image = pg.image.load(path.join(IMG_FOLDER, PlayerImg.STATIC_UP.value))

    def change_player_img(self, image1, image2):
        if self.type == image1:
            self.type = image2
            self.image = pg.image.load(path.join(IMG_FOLDER, image2.value))
        else:
            self.type = image1
            self.image = pg.image.load(path.join(IMG_FOLDER, image1.value))

    def collide_with_walls(self, dx=0, dy=0):
        rect_copy = self.rect
        rect_copy.x += dx * TILESIZE
        rect_copy.y += dy * TILESIZE
        # pygame.rect.collidelistall instead of for loop
        for wall in self.map.walls:
            if rect_copy.colliderect(wall.rect):
                return True
        return False

    def collide_with_door(self, dx=0, dy=0):
        rect_copy = self.rect
        rect_copy.x += dx * TILESIZE
        rect_copy.y += dy * TILESIZE
        # pygame.rect.collidelistall instead of for loop
        for door in self.map.doors:
            if rect_copy.colliderect(door.rect):
                return door
        return None

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def interact(self):
        flag = False
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if not flag:
                    if 0 <= x < self.game.map.width // TILESIZE and 0 <= y < self.game.map.height // TILESIZE:
                        rect = self.rect
                        rect.x = x * TILESIZE
                        rect.y = y * TILESIZE
                        for npc in self.map.npcs:
                            print(rect.x, rect.y)
                            if rect.colliderect(npc.rect):
                                npc.dialogue()
                                flag = True
                                break

    def fight(self):
        flag = False
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if not flag:
                    if 0 <= x < self.game.map.width // TILESIZE and 0 <= y < self.game.map.height // TILESIZE:
                        rect = self.rect
                        rect.x = x * TILESIZE
                        rect.y = y * TILESIZE
                        for monster in self.map.monsters:
                            print(rect.x, rect.y)
                            if rect.colliderect(monster.rect):
                                self.game.create_arena(monster, BATTLE_ARENA)
                                self.game.arena.enter_battle_arena()
                                break