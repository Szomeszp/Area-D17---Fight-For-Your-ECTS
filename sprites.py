import random

import pygame as pg
from statistics import *
from settings import *
vec = pg.math.Vector2
from os import path


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, stats=None):
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

        self.statistics = Statistics(100, 20, 10, 10, 10, 1, 2, 20, 50)

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

    def attack(self, monster):
        rng = random.randint(0, 100)

        if 0 <= rng <= self.statisctics.criticalDamageChance:
            damage = self.statisctics.damage * (1 + self.statisctics.criticalDamageMultiplier / 100)
        else:
            damage = self.statisctics.damage

        monster.hurt(damage)

    def hurt(self, damage):
        self.statisctics.health = self.statisctics.health - damage




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
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, "img")
        self.image = pg.image.load(path.join(self.img_folder, "stairs1.png"))
        # self.image.fill(GREEN)


class Monster(pg.sprite.Sprite):
    def __init__(self, game, x, y, statistics):
        self.groups = game.walls, game.monsters, game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.x = x
        self.y = y
        self.statisctics = statistics

        self.image = self.getImage()

    def getImage(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        return pg.image.load(path.join(img_folder, "bullet.png"))

    def attack(self, player):
        rng = random.randint(0, 100)

        if 0 <= rng <= self.statisctics.criticalDamageChance:
            damage = self.statisctics.damage * (1 + self.statisctics.criticalDamageMultiplier / 100)
        else:
            damage = self.statisctics.damage

        player.hurt(damage)

    def hurt(self, damage):
        self.statisctics.health = self.statisctics.health - damage
