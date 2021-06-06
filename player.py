import random
from time import sleep

import pygame as pg

from items import Key
from sprites import Character, SecretDoor
from statistics import *
from settings import *
from numpy import e
from os import path
import math
from statistics import Statistics


class Player(pg.sprite.Sprite, Character):
    def __init__(self, game, map, x, y, type):
        self.level = 1
        self.experience = 0
        Character.__init__(self, game, x, y, type, Statistics.generatePlayerStatistics(self.level))
        self.groups = map.all_sprites
        self.map = map
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = self.getImage()
        self.items = []

        self.is_dead = False
        self.respawn_time = 5
        self.remaining_respawn_time = 0

    def level_up(self, experience):
        tmp_level = self.level
        self.experience = min(self.experience + experience, -5000 * math.log(- 7 / 8 + 1))
        self.level = min(math.ceil(8 - 8 * (e ** (-self.experience * 0.0002))), 7)
        if tmp_level - self.level != 0:
            self.statistics = Statistics.generatePlayerStatistics(self.level)

    def getImage(self):
        return pg.image.load(path.join(IMG_FOLDER, self.game.player_img.value))

    def move(self, dx=0, dy=0):
        door = self.collide_with_door()
        if door:
            if isinstance(door, SecretDoor):
                if not any(isinstance(item, Key) for item in self.items):
                    self.game.add_message(Message("Nie masz klucza!"))
                    print("Nie masz klucza!")
                    door = None
                else:
                    self.game.get_through_door(door)
            else:
                self.game.get_through_door(door)
        if not door:
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

    def draw_gui(self):
        # HEALTH BAR
        ratio = self.statistics.current_health / self.statistics.max_health

        pg.draw.rect(self.game.screen, BLACK, pg.Rect((31, 7), (98, 18)),
                     border_radius=4)

        if ratio == 1:
            pg.draw.rect(self.game.screen, GREEN, pg.Rect((32, 8), (96, 16)),
                         border_radius=4)
        elif ratio == 0:
            pg.draw.rect(self.game.screen, RED, pg.Rect((32, 8), (96, 16)),
                         border_radius=4)
        else:
            pg.draw.rect(self.game.screen, GREEN, pg.Rect((32, 8), (96 * ratio, 16)),
                         border_bottom_left_radius=4, border_top_left_radius=4)
            pg.draw.rect(self.game.screen, RED,
                         pg.Rect((32 + 96 * ratio, 8), (96 * (1 - ratio), 16)),
                         border_bottom_right_radius=4, border_top_right_radius=4)

        text = self.game.my_small_font.render(f"HEALTH", 1, (0, 0, 0))
        text_size = self.game.my_small_font.size(f"HEALTH")
        self.game.screen.blit(text, (80 - text_size[0] / 2, 17 - text_size[1] / 2))

        # EXP BAR
        def get_exp(level):
            return -5000 * math.log(- (level - 1) / 8 + 1)

        ratio = (self.experience - get_exp(self.level)) / (get_exp(self.level + 1) - get_exp(self.level))

        pg.draw.rect(self.game.screen, BLACK, pg.Rect((159, 7), (98, 18)),
                     border_radius=4)

        if ratio == 1:
            pg.draw.rect(self.game.screen, YELLOW, pg.Rect((160, 8), (96 * ratio, 16)),
                         border_radius=4)
        elif ratio == 0:
            pg.draw.rect(self.game.screen, LIGHTGREY, pg.Rect((160, 8), (96, 16)),
                         border_radius=4)
        else:
            pg.draw.rect(self.game.screen, YELLOW, pg.Rect((160, 8), (96 * ratio, 16)),
                         border_bottom_left_radius=4, border_top_left_radius=4)
            pg.draw.rect(self.game.screen, LIGHTGREY, pg.Rect((160 + 96 * ratio, 8), (96 * (1 - ratio), 16)),
                         border_bottom_right_radius=4, border_top_right_radius=4)

        text = self.game.my_small_font.render(f"LEVEL {self.level}", 1, (0, 0, 0))
        text_size = self.game.my_small_font.size(f"HEALTH")
        self.game.screen.blit(text, (208 - text_size[0] / 2, 17 - text_size[1] / 2))

    def dead_screen(self):
        sleep(1)

        if self.remaining_respawn_time == 0:
            self.is_dead = False
            return

        print(self.remaining_respawn_time)

        pg.draw.rect(self.game.screen, BLACK, pg.Rect((0, 0), (WIDTH, HEIGHT)),
                     border_radius=4)

        info = f"Dziekanka byq: {self.remaining_respawn_time}..."
        text = self.game.my_big_font.render(info, 1, (255, 255, 255))
        text_size = self.game.my_big_font.size(info)

        self.game.screen.blit(text, ((WIDTH - text_size[0]) / 2, (HEIGHT - text_size[1]) / 2))
        self.remaining_respawn_time -= 1

    def collect_item(self):
        for item in self.map.items:
            if self.rect.colliderect(item):
                self.items.append(item)
                self.map.items.remove(item)
                self.map.all_sprites.remove(item)
                print("Zebrałeś item")

    def heal(self, potion):
        prev_hp = self.statistics.current_health
        self.statistics.current_health = min(self.statistics.current_health + potion.health, self.statistics.max_health)
        hp = self.statistics.current_health - prev_hp
        self.items.remove(potion)
        potion.kill()
        return hp
