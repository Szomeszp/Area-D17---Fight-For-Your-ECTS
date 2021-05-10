import random

import pygame as pg
from statistics import *
from settings import *
vec = pg.math.Vector2
from os import path


class Character:
    def __init__(self, game, x, y, type, statistics):
        self.game = game
        self.type = type
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.x = x
        self.y = y
        self.statistics = statistics

    def attack(self, player):
        rng = random.randint(0, 100)

        if 0 <= rng <= self.statistics.critical_damage_chance:
            damage = self.statistics.damage * (1 + self.statistics.critical_damage_multiplier / 100)
        else:
            damage = self.statistics.damage

        player.hurt(damage)

    def hurt(self, damage):
        self.statistics.current_health = self.statistics.current_health - damage


class Player(pg.sprite.Sprite, Character):
    def __init__(self, game, x, y, type, stats=None):
        Character.__init__(self, game, x, y, type, Statistics(100, 5, 10, 10, 10, 1, 2, 20, 50))
        self.groups = game.all_sprites
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

    def interact(self):
        flag = False
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if not flag:
                    if 0 <= x < self.game.map.width // TILESIZE and 0 <= y < self.game.map.height // TILESIZE:
                        rect = self.rect
                        rect.x = x * TILESIZE
                        rect.y = y * TILESIZE
                        for npc in self.game.npcs:
                            print(rect.x, rect.y)
                            if rect.colliderect(npc.rect):
                                npc.dialogue("Siema siema siema czesc")
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
                        for monster in self.game.monsters:
                            print(rect.x, rect.y)
                            if rect.colliderect(monster.rect):
                                self.game.enterBattleArena(monster, BATTLE_ARENA)
                                break


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
    def __init__(self, game, x, y, w, h, map, name):
        self.groups = game.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map = map
        self.name = name


class NPC(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls, game.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

    def dialogue(self, text):
        print("Dialog")

        if text:
            blackBarRectPos = (0, self.game.screen.get_height() - 64)
            blackBarRectSize = (self.game.screen.get_width(), 64)
            pg.draw.rect(self.game.screen, (0, 0, 0), pg.Rect(blackBarRectPos, blackBarRectSize))

            space_text = self.game.my_small_font.render("Click [space] to continue", 1, (255, 255, 255), (0, 0, 0))
            space_text_size = self.game.my_small_font.size("Click [space] to continue")
            self.game.screen.blit(space_text, (self.game.screen.get_width() - space_text_size[0] - 5, self.game.screen.get_height() - space_text_size[1] - 5))

            textSurf = self.game.my_big_font.render(text, 1, (255, 255, 255), (0, 0, 0))
            self.game.screen.blit(textSurf, (0, self.game.screen.get_height() - 64))
            cnt = True
            while cnt:
                pg.event.pump()
                if pg.key.get_pressed()[pg.K_SPACE]:
                    cnt = False
                pg.display.flip()
                self.game.clock.tick(60)


class SecretDoor(Door):
    def __init__(self, game, x, y, w, h, map, name):
        super().__init__(game, x, y, w, h, map, name)
        self.groups = game.doors, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(path.join(IMG_FOLDER, "stairs1.png"))
        # self.image.fill(GREEN)


class Monster(pg.sprite.Sprite, Character):
    def __init__(self, game, x, y, type, statistics):
        self.groups = game.walls, game.monsters, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Character.__init__(self, game, x, y, type, statistics)
        self.image = self.getImage()

    def getImage(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        return pg.image.load(path.join(img_folder, self.type + ".png"))


