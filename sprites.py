import random
import json

import pygame as pg
from statistics import *
from settings import *
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
            damage = float(self.statistics.damage * (1 + self.statistics.critical_damage_multiplier / 100))
        else:
            damage = float(self.statistics.damage)
        if type(self.type) == str:  # do poprawy
            self.game.arena.battle_log.add_log("Monster zadał " + str(damage) + " obrażeń")
        else:
            self.game.arena.battle_log.add_log("Player zadał " + str(damage) + " obrażeń")
        return player.hurt(damage)

    def hurt(self, damage):
        # usunięcie ujemnego hp
        self.statistics.current_health = max(self.statistics.current_health - damage, 0)
        if self.statistics.current_health <= 0:
            return 1
        return 0

    def check_opponent_in_range(self, opponent):
        attack_range = self.statistics.attack_range
        # print("Rect")
        # print(self.rect)
        # print(opponent.rect)
        for i in range(-attack_range, attack_range + 1):
            for j in range(-attack_range, attack_range + 1):
                if abs(i) + abs(j) <= attack_range:
                    # musialem zmienic na recty zeby dzialalo tez dla monstera
                    rect = pg.Rect(self.rect.x + i * TILESIZE, self.rect.y + j * TILESIZE, TILESIZE, TILESIZE)
                    if rect.colliderect(opponent):
                        # print("Opponent in range!")
                        return True
        return False


class Wall(pg.sprite.Sprite):
    def __init__(self, game, map, x, y, w, h):
        self.groups = map.walls
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
    def __init__(self, game, map_name, map, x, y, w, h, name):
        print(map_name)
        self.groups = map.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map_name = map_name
        self.name = name


class NPC(pg.sprite.Sprite):
    def __init__(self, game, map, x, y, w, h, name):
        self.groups = map.walls, map.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

        self.name = name

        self.current_path = 0
        self.current_sub_path = 0

    def dialogue(self):
        print("Dialog")

        with open('dialogues.json') as file:
            dialogues_file = json.load(file)

        def print_dialogue():
            blackBarRectPos = (32, self.game.screen.get_height() - 160)
            blackBarRectSize = (self.game.screen.get_width() - 64, 128)
            pg.draw.rect(self.game.screen, (128, 64, 32), pg.Rect(blackBarRectPos, blackBarRectSize),
                         border_radius=4)

            space_text = self.game.my_small_font.render("Click [space] to continue", 1, (255, 255, 255))
            space_text_size = self.game.my_small_font.size("Click [space] to continue")
            self.game.screen.blit(space_text, (self.game.screen.get_width() - space_text_size[0] - 40,
                                               self.game.screen.get_height() - space_text_size[1] - 40))

            position = 152
            text = dialogues_file[self.name]["main_text"]
            rendered_text = self.game.my_big_font.render(text, 1, (255, 255, 255))
            self.game.screen.blit(rendered_text, (40, self.game.screen.get_height() - position))

            position = position - self.game.my_big_font.size(text)[1] - 8

            for i in range(dialogues_file[self.name]["number_of_sub_paths"]):
                text = dialogues_file[self.name]["sub_paths"][i]["text"]

                if i == self.current_sub_path:
                    text = ">>>  " + text

                rendered_text = self.game.my_medium_font.render(text, 1, (255, 255, 255))
                self.game.screen.blit(rendered_text, (40, self.game.screen.get_height() - position))
                position = position - self.game.my_small_font.size(text)[1] - 8


        print(dialogues_file[self.name])

        cnt = True
        reload = True
        while cnt:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game.quit()

                if reload:
                    print_dialogue()
                reload = False

                if event.type == pg.KEYDOWN:
                    # pg.event.pump()
                    if event.key == pg.K_SPACE:
                        self.current_path = 0
                        self.current_sub_path = 0
                        cnt = False
                    if event.key == pg.K_w:
                        self.current_sub_path = (self.current_sub_path + 1) % dialogues_file[self.name]["number_of_sub_paths"]
                        reload = True
                    if event.key == pg.K_s:
                        self.current_sub_path = (self.current_sub_path - 1) % dialogues_file[self.name]["number_of_sub_paths"]
                        reload = True

                pg.display.flip()
                self.game.clock.tick(FPS) / 1000


class SecretDoor(Door):
    def __init__(self, game, map_name, map, x, y, w, h, name):
        super().__init__(game, map_name, map, x, y, w, h, name)
        self.groups = map.doors, map.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(path.join(IMG_FOLDER, "stairs1.png"))
        # self.image.fill(GREEN)


class Monster(pg.sprite.Sprite, Character):
    def __init__(self, game, map, spawn, x, y, type, statistics):
        self.groups = map.walls, map.monsters, map.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Character.__init__(self, game, x, y, type, statistics)
        self.image = self.getImage()
        self.spawn = spawn

        # print(self.image)

    def getImage(self):
        return pg.image.load(path.join(IMG_FOLDER, self.type + ".png"))

    def move_to_opponent(self, opponent):
        # zmieniam tylko recty bo w arenie operuje na rectach
        # to dzialanie na rectach, jest mega nie intuicyjne
        def x_move(dx):
            if dx > 0:
                self.rect.x += TILESIZE
            else:
                self.rect.x -= TILESIZE

        def y_move(dy):
            if dy > 0:
                self.rect.y += TILESIZE
            else:
                self.rect.y -= TILESIZE
        moves = self.statistics.move_range
        for i in range(moves):
            dy = opponent.y - self.rect.y // TILESIZE
            dx = opponent.x - self.rect.x // TILESIZE
            print(dx, dy)
            if abs(dx) > abs(dy):
                x_move(dx)
            elif abs(dx) < abs(dy):
                y_move(dy)
            else:
                if bool(random.randint(0, 1)):
                    x_move(dx)
                else:
                    y_move(dy)



