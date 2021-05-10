import random

import pygame as pg
from statistics import *
from settings import *
vec = pg.math.Vector2
from os import path


class Arena:
    def __init__(self, game, player, monster, player_health_bar, monster_health_bar, battle_info, control_panel):
        self.player = player
        self.monster = monster
        self.game = game
        self.player_hp_bar = player_health_bar
        self.monster_hp_bar = monster_health_bar
        self.battle_info = battle_info
        self.control_panel = control_panel

    def draw_arena(self):
        self.monster_hp_bar.draw_health()
        self.player_hp_bar.draw_health()
        self.battle_info.draw_info()
        self.control_panel.draw_buttons()


class HealthBar:
    def __init__(self, game, x, y, w, h, character):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.character = character

    def draw_health(self):
        # ratio = 0.5
        ratio = self.character.statistics.current_health / self.character.statistics.max_health
        pos = (self.x, self.y)
        redSize = (self.width, self.height)
        pg.draw.rect(self.game.screen, RED, pg.Rect(pos, redSize))
        greenSize = (self.width * ratio, self.height)
        pg.draw.rect(self.game.screen, GREEN, pg.Rect(pos, greenSize))
        # potrzbne do wyswietlania bo tak to znika od razu, ale tez jak to zmienisz to sie zacina


class BattleInfo:
    def __init__(self, game, x, y, w, h, info):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.info = info

    def draw_info(self):
        text = self.game.my_small_font.render(self.info, 1, (255, 255, 255), (0, 0, 0))
        text_size = self.game.my_small_font.size(self.info)
        self.game.screen.blit(text, (self.x + self.width / 2 - text_size[0]/2, self.y + self.height / 2 - text_size[1] / 2))


class ControlPanel:
    def __init__(self, game):
        self.game = game
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw_button()


class Button(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, text, type):
        self.groups = game.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.type = type

    def draw_button(self):
        # draw background
        pos = (self.x, self.y)
        size = (self.width, self.height)
        pg.draw.rect(self.game.screen, BLACK, pg.Rect(pos, size))
        # draw text
        btn = self.game.my_small_font.render(self.text, 1, (255, 255, 255), (0, 0, 0))
        btn_size = self.game.my_small_font.size(self.text)
        self.game.screen.blit(btn, (self.x + self.width / 2 - btn_size[0] / 2, self.y + self.height / 2 - btn_size[1] / 2))
