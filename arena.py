import random
from time import sleep

import pygame as pg

from sprites import Monster
from player import Player
from statistics import *
from settings import *
from tilemap import TiledMap, Camera
from os import path
import copy


class Arena:
    def __init__(self, game, player, monster, arena):
        self.player = player
        self.monster = monster
        self.map = map
        self.turn = 0
        self.game = game
        self.game.map = TiledMap(path.join(MAP_FOLDER, arena))
        self.game.map_img = self.game.map.make_map()
        self.game.map_rect = self.game.map_img.get_rect()
        # self.game.clear_groups()
        self.show_move_range = False
        self.move_rects = []

    def draw_arena(self):
        self.monster_hp_bar.draw_health()
        self.player_hp_bar.draw_health()
        self.battle_info.draw_info()
        self.control_panel.draw_buttons()
        self.battle_log.draw_logs()
        self.draw_target_in_range()
        if self.show_move_range:
            self.draw_move_range()
    
    def enter_battle_arena(self):
        self.player.stand()
        self.control_panel = ControlPanel(self)

        for tile_object in self.game.map.tmxdata.objects:
            if str(tile_object.name)[:6] == "button":
                btn = Button(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                             tile_object.name, tile_object.name)
                self.control_panel.add_button(btn)
            # Olek zrobił spoko wykorzystanie mapy
            if str(tile_object.name)[-6:] == "Button":
                if str(tile_object.name)[:-6] == "left":
                    btn = Button(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2190', tile_object.name)
                elif str(tile_object.name)[:-6] == "right":
                    btn = Button(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2192', tile_object.name)
                elif str(tile_object.name)[:-6] == "forward":
                    btn = Button(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2191', tile_object.name)
                elif str(tile_object.name)[:-6] == "backward":
                    btn = Button(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2193', tile_object.name)
                elif str(tile_object.name)[:-6] == "center":
                    btn = Button(self.game, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2022', tile_object.name)
                self.control_panel.add_button(btn)

            if tile_object.name == "monsterHealthBar":
                # print(tile_object.x, tile_object.y, tile_object.width, monster.statistics.health)
                self.monster_hp_bar = HealthBar(self.game, tile_object.x, tile_object.y, tile_object.width,
                                               tile_object.height, self.monster)
            if tile_object.name == "playerHealthBar":
                self.player_hp_bar = HealthBar(self.game, tile_object.x, tile_object.y, tile_object.width,
                                              tile_object.height, self.game.player)
            if tile_object.name == "battleInfo":
                self.battle_info = BattleInfo(self.game, tile_object.x, tile_object.y, tile_object.width,
                                         tile_object.height, "Monster Staś")
            if tile_object.name == "battleLog":
                self.battle_log = BattleLog(self.game, tile_object.x, tile_object.y, tile_object.width,
                                       tile_object.height)

            if tile_object.type == "arena":
                self.ring = pg.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.type == "spawnPlayer":
                dx = random.randint(0, int(tile_object.width // TILESIZE) - 1)
                dy = random.randint(0, int(tile_object.height // TILESIZE) - 1)

                self.player.x = int((tile_object.x // TILESIZE) + dx)
                self.player.y = int((tile_object.y // TILESIZE) + dy)
                self.game.map.all_sprites.add(self.player)
            if tile_object.type == "spawnMonster":
                dx = random.randint(0, int(tile_object.width // TILESIZE) - 1)
                dy = random.randint(0, int(tile_object.height // TILESIZE) - 1)

                self.monster.rect.x = int((tile_object.x // TILESIZE) + dx) * TILESIZE
                self.monster.rect.y = int((tile_object.y // TILESIZE) + dy) * TILESIZE
                self.game.map.all_sprites.add(self.monster)
                self.game.map.monsters.add(self.monster)
                self.game.map.walls.add(self.monster)

        self.game.arena.battle_log.add_log("Walka się rozpoczeła!")
        self.game.camera = Camera(self.game.map.width, self.game.map.height)

    def exit_arena(self):
        self.player.x = self.game.last_position[0][0]
        self.player.y = self.game.last_position[0][1]
        self.monster.rect.x = self.game.last_position[1][0]
        self.monster.rect.y = self.game.last_position[1][1]
        self.game.load_map(self.game.last_position[2].map_name)
        self.game.render_map(self.player, "", 1)
        self.game.arena = None

    def arena_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if self.turn % 2 == 0:
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    for btn in self.control_panel.buttons:
                        if btn.rect.collidepoint(pos):
                            print(btn.text + " clicked!")
                            if btn.text == "button1":
                                # quit when hp == 0
                                if self.game.arena.player.attack(self.game.arena.monster):
                                    # print(self.game.last_position[2].map_name)
                                    # print(self.game.maps)
                                    # print(self.game.maps.get(self.game.last_position[2].map_name))
                                    self.game.maps.get(self.game.last_position[2].map_name).monsters.remove(self.monster)
                                    self.game.maps.get(self.game.last_position[2].map_name).all_sprites.remove(self.monster)
                                    self.monster.spawn.last_spawn = pg.time.get_ticks()
                                    self.monster.spawn.current_monsters -= 1
                                    self.monster.kill()
                                    self.exit_arena()
                                    break
                                self.turn += 1
                            elif btn.type == "leftButton":
                                self.player.move(dx=-1)
                            elif btn.type == "rightButton":
                                self.player.move(dx=1)
                            elif btn.type == "forwardButton":
                                self.player.move(dy=-1)
                            elif btn.type == "backwardButton":
                                self.player.move(dy=1)
                            elif btn.type == "centerButton":
                                print("Center Clicked!")
                                self.player.check_opponent_in_range(self.monster)
                            elif btn.type == "button5":
                                self.exit_arena()
                            self.player.stand()  # zeby podczas całej areny był do nas plecami
                    if self.player.rect.collidepoint(pos):
                        print("Player clicked!")
                        if self.show_move_range:
                            self.show_move_range = False
                        else:
                            self.show_move_range = True
                    if self.show_move_range:
                        for move_rect in self.move_rects:
                            if move_rect.rect.collidepoint(pos):
                                print("przed")
                                print(self.player.x, self.player.y)
                                self.player.x = move_rect.x // TILESIZE
                                self.player.y = move_rect.y // TILESIZE
                                print("po")
                                print(self.player.x, self.player.y)
                                self.turn += 1
                    if self.player.check_opponent_in_range(self.monster):
                        if self.monster.rect.collidepoint(pos):
                            if self.game.arena.player.attack(self.game.arena.monster):
                                # print(self.game.last_position[2].map_name)
                                # print(self.game.maps)
                                # print(self.game.maps.get(self.game.last_position[2].map_name))
                                self.game.maps.get(self.game.last_position[2].map_name).monsters.remove(self.monster)
                                self.game.maps.get(self.game.last_position[2].map_name).all_sprites.remove(self.monster)
                                self.monster.spawn.last_spawn = pg.time.get_ticks()
                                self.monster.spawn.current_monsters -= 1
                                self.monster.kill()
                                self.exit_arena()
                                break
                            self.turn += 1
                            print("Monster zaatakowany")

                    # do przmyslenia gdzie to dac
                    self.create_move_rects()
            else:
                sleep(1)
                # if in range -> attack
                # else -> move
                if self.monster.check_opponent_in_range(self.player):
                    if self.game.arena.monster.attack(self.game.arena.player):
                        # co jak my zginiemy
                        self.exit_arena()
                        break
                else:
                    self.monster.move_to_opponent(self.player)
                self.turn += 1
                pg.event.clear()

    def draw_move_range(self):
        for rect in self.move_rects:
            rect.draw_rect()

    def create_move_rects(self):
        self.move_rects = []
        move_range = self.player.statistics.move_range
        for i in range(-move_range, move_range + 1):
            for j in range(-move_range, move_range + 1):
                if abs(i) + abs(j) <= move_range:
                    if i == 0 and j == 0:
                        continue
                    rect = pg.Rect((self.player.x + i) * TILESIZE, (self.player.y + j) * TILESIZE, TILESIZE, TILESIZE)
                    if rect.colliderect(self.ring) and not rect.colliderect(self.monster):
                        self.move_rects.append(MoveRect(self.game, (self.player.x + i) * TILESIZE, (self.player.y + j) * TILESIZE))

    # def create_rect(self, x, y):
    #     color = (65, 105, 225)
    #     border = 2
    #     gap = 3
    #     border_color = BLACK
    #     # draw border
    #     pg.draw.rect(self.game.screen, border_color, pg.Rect((x + gap, y + gap), (TILESIZE - 2*gap, TILESIZE - 2*gap)))
    #     # draw rect
    #     pg.draw.rect(self.game.screen, color, pg.Rect((x + border + gap, y + border + gap), (TILESIZE - 2*(border + gap), TILESIZE - 2*(border + gap))))

    def draw_target_in_range(self):
        if self.player.check_opponent_in_range(self.monster):
            x = self.monster.rect.x
            y = self.monster.rect.y
            print(x, y)
            pg.draw.circle(self.game.screen, RED, (x + TILESIZE/2, y + TILESIZE/2), 16)
            print("Circle drawn!")


class MoveRect:
    def __init__(self, game, x, y):
        self.game = game
        self.rect = pg.Rect(x, y, TILESIZE, TILESIZE)
        self.x = x
        self.y = y

    def draw_rect(self):
        color = (65, 105, 225)
        border = 2
        gap = 3
        border_color = BLACK
        # draw border
        pg.draw.rect(self.game.screen, border_color, pg.Rect((self.x + gap, self.y + gap), (TILESIZE - 2*gap, TILESIZE - 2*gap)))
        # draw rect
        pg.draw.rect(self.game.screen, color, pg.Rect((self.x + border + gap, self.y + border + gap), (TILESIZE - 2*(border + gap), TILESIZE - 2*(border + gap))))


class HealthBar:
    def __init__(self, game, x, y, w, h, character):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.character = character

    def draw_health(self):
        ratio = self.character.statistics.current_health / self.character.statistics.max_health


        if ratio == 1:
            pg.draw.rect(self.game.screen, GREEN, pg.Rect((self.x, self.y), (self.width, self.height)), border_radius=4)
        elif ratio == 0:
            pg.draw.rect(self.game.screen, RED, pg.Rect((self.x, self.y), (self.width, self.height)), border_radius=4)
        else:
            pg.draw.rect(self.game.screen, GREEN, pg.Rect((self.x, self.y), (self.width * ratio, self.height)), border_bottom_left_radius=4, border_top_left_radius=4)
            pg.draw.rect(self.game.screen, RED, pg.Rect((self.x + self.width * ratio, self.y), (self.width * (1 - ratio), self.height)), border_bottom_right_radius=4, border_top_right_radius=4)


class BattleInfo:
    def __init__(self, game, x, y, w, h, info):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.info = info

    def draw_info(self):
        text = self.game.my_big_font.render(self.info, 1, (255, 255, 255))
        text_size = self.game.my_big_font.size(self.info)
        self.game.screen.blit(text, (self.x + self.width / 2 - text_size[0]/2, self.y + self.height / 2 - text_size[1] / 2))


class BattleLog:
    def __init__(self, game, x, y, w, h):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.max_len = 19
        self.line_height = 18
        self.logs = []

    def add_log(self, str):
        if len(self.logs) + 1 > self.max_len:
            self.logs.pop(0)
        self.logs.append(str)

    def draw_logs(self):
        pos = (self.x, self.y)
        size = (self.width, self.height)
        pg.draw.rect(self.game.screen, BLACK, pg.Rect(pos, size), border_radius=4)
        for idx, log in enumerate(self.logs):
            text = self.game.my_small_font.render(log, 1, (255, 255, 255))
            self.game.screen.blit(text, (self.x + 4, self.y + idx * self.line_height + 4))


class ControlPanel:
    def __init__(self, game):
        self.game = game
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw_buttons(self):
        for btn in self.buttons:
            btn.draw_button()


class Button:
    def __init__(self, game, x, y, w, h, text, type):
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
        pg.draw.rect(self.game.screen, BLACK, pg.Rect(pos, size), border_radius=4)
        # draw text
        btn = self.game.my_medium_font.render(self.text, 1, (255, 255, 255))
        btn_size = self.game.my_medium_font.size(self.text)
        self.game.screen.blit(btn, (self.x + self.width / 2 - btn_size[0] / 2, self.y + self.height / 2 - btn_size[1] / 2))
