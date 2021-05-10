import random

import pygame as pg
from statistics import *
from settings import *
vec = pg.math.Vector2
from os import path


class Arena:
    def __init__(self, game, player, monster, player_health_bar, monster_health_bar, battle_info):
        self.player = player
        self.monster = monster
        self.game = game
        self.player_hp_bar = player_health_bar
        self.monster_hp_bar = monster_health_bar
        self.battle_info = battle_info

    def draw_arena(self):
        self.monster_hp_bar.draw_health()
        self.player_hp_bar.draw_health()
        self.battle_info.draw_info()


class HealthBar:
    def __init__(self, game, x, y, w, h, max_hp):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.max_hp = max_hp  # testy bo byl blad type error tuple
        self.curr_hp = max_hp

    def draw_health(self):
        ratio = 0.5
        # ratio = self.curr_hp / self.max_hp
        pos = (self.x, self.y)
        redSize = (self.width, self.height)
        pg.draw.rect(self.game.screen, RED, pg.Rect(pos, redSize))
        greenSize = (self.width * ratio, self.height)
        pg.draw.rect(self.game.screen, GREEN, pg.Rect(pos, greenSize))
        # potrzbne do wyswietlania bo tak to znika od razu, ale tez jak to zmienisz to sie zacina

    def take_damage(self, dmg):
        if self.curr_hp - dmg >= 0:
            self.curr_hp -= dmg
        else:
            self.curr_hp = 0
        self.draw_health()  # moze niepotrzebne


class BattleInfo:
    def __init__(self, game, x, y, w, h, info):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.info = info

    def draw_info(self):
        # można zrobic wyswietlani
        text = self.game.my_small_font.render(self.info, 1, (255, 255, 255), (0, 0, 0))
        # potrzebne zeby wysrodkowac tekst
        text_size = self.game.my_small_font.size(self.info)
        self.game.screen.blit(text, (self.x + self.width / 2 - text_size[0]/2, self.y + self.height / 2 - text_size[1] / 2))


class ControlPanel:
    def __init__(self, game, attack_btn):
        self.game = game
        self.attack_btn = attack_btn
        # To do
