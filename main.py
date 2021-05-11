from time import sleep

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from statistics import *
from random import randint
from arena import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.secret_room_entered = False
        self.my_small_font = pg.font.SysFont('Arial Unicode MS', 14)
        self.my_big_font = pg.font.SysFont('Arial Unicode MS', 30)
        self.arena = None
        self.init_groups()

    def init_groups(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.buttons = pg.sprite.Group()

    def clear_groups(self):
        self.all_sprites.empty()
        self.walls.empty()
        self.doors.empty()
        self.npcs.empty()
        self.monsters.empty()
        self.buttons.empty()

    def load_data(self):
        self.main_map = 'map_alpha2.tmx'
        self.map_folder = path.join(GAME_FOLDER, "maps")
        self.map = TiledMap(path.join(self.map_folder, self.main_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = PlayerImg.DOWN

    def get_through_door(self, door=None):
        if door is not None:
            new_map = door.map
            spawn = door.name + "_spawn"
            if door.name == "secret_door_out":
                self.secret_room_entered = True
        else:
            spawn = " "
            new_map = self.main_map
        map = TiledMap(path.join(self.map_folder, new_map))
        self.render_map(self.player, map, spawn)

    def render_map(self, player, new_map, spawn, arena_exited=0):
        self.map = new_map
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.clear_groups()
        random_door_locations = []
        self.all_sprites.add(player)

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player" and not arena_exited:
                self.player.x = int(tile_object.x // TILESIZE)
                self.player.y = int(tile_object.y // TILESIZE)

            if tile_object.name == spawn:
                self.player.x = int(tile_object.x // TILESIZE)
                self.player.y = int(tile_object.y // TILESIZE)
            if tile_object.name == "wall":
                print("sciana")
                Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.type == "door":
                Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.map,
                     tile_object.name)
            if tile_object.name == "npc":
                NPC(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.type == "monster":
                stats = Statistics.generateMonsterStatistics(self, 1)
                Monster(self, int(tile_object.x // TILESIZE) * TILESIZE, int(tile_object.y // TILESIZE) * TILESIZE,
                        "bullet",
                        stats)
            if not self.secret_room_entered:
                if tile_object.name == "random_door":
                    for dx in range(int(tile_object.width // TILESIZE)):
                        for dy in range(int(tile_object.height // TILESIZE)):
                            random_door_locations.append(
                                [int((tile_object.x // TILESIZE) + dx), int((tile_object.y // TILESIZE) + dy)])
        # print(len(random_door_locations))
        if not self.secret_room_entered:
            if len(random_door_locations) > 0:
                random_location = random_door_locations[randint(0, len(random_door_locations) - 1)]
                print(random_location)
                SecretDoor(self, random_location[0] * TILESIZE, random_location[1] * TILESIZE, TILESIZE, TILESIZE,
                           "map_kapitol.tmx", "secret_door_out")
        self.camera = Camera(self.map.width, self.map.height)

    def enterBattleArena(self, monster, arena):
        self.last_position = (self.player.x, self.player.y, self.map)
        self.map = TiledMap(path.join(self.map_folder, arena))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.clear_groups()

        control_panel = ControlPanel(self)

        for tile_object in self.map.tmxdata.objects:
            if str(tile_object.name)[:6] == "button":
                btn = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                             tile_object.name, tile_object.name)
                control_panel.add_button(btn)
            if str(tile_object.name)[-6:] == "Button":
                if str(tile_object.name)[:-6] == "left":
                    btn = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2190', tile_object.name)
                elif str(tile_object.name)[:-6] == "right":
                    btn = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2192', tile_object.name)
                elif str(tile_object.name)[:-6] == "forward":
                    btn = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2191', tile_object.name)
                elif str(tile_object.name)[:-6] == "backward":
                    btn = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2193', tile_object.name)
                elif str(tile_object.name)[:-6] == "center":
                    btn = Button(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                                 '\u2022', tile_object.name)
                control_panel.add_button(btn)

            if tile_object.name == "monsterHealthBar":
                # print(tile_object.x, tile_object.y, tile_object.width, monster.statistics.health)
                monster_health_bar = HealthBar(self, tile_object.x, tile_object.y, tile_object.width,
                                               tile_object.height, monster)
            if tile_object.name == "playerHealthBar":
                player_health_bar = HealthBar(self, tile_object.x, tile_object.y, tile_object.width,
                                              tile_object.height, self.player)
            if tile_object.name == "battleInfo":
                battle_info = BattleInfo(self, tile_object.x, tile_object.y, tile_object.width,
                                         tile_object.height, "Monster Staś")
            if tile_object.name == "battleLog":
                battle_log = BattleLog(self, tile_object.x, tile_object.y, tile_object.width,
                                       tile_object.height)

            if tile_object.type == "spawnPlayer":
                dx = random.randint(0, int(tile_object.width // TILESIZE) - 1)
                dy = random.randint(0, int(tile_object.height // TILESIZE) - 1)

                self.player = Player(self, int((tile_object.x // TILESIZE) + dx), int((tile_object.y // TILESIZE) + dy),
                                     self.player_img)

            if tile_object.type == "spawnMonster":
                dx = random.randint(0, int(tile_object.width // TILESIZE) - 1)
                dy = random.randint(0, int(tile_object.height // TILESIZE) - 1)

                Monster(self, int((tile_object.x // TILESIZE) + dx) * TILESIZE,
                        int((tile_object.y // TILESIZE) + dy) * TILESIZE, "bullet", monster.statistics)

        self.arena = Arena(self, self.player, monster, player_health_bar, monster_health_bar, battle_info,
                           control_panel, battle_log)
        self.arena.battle_log.add_log("Walka się rozpoczeła!")
        self.camera = Camera(self.map.width, self.map.height)

    def exit_arena(self):
        self.player.x = self.last_position[0]
        self.player.y = self.last_position[1]
        self.render_map(self.player, self.last_position[2], "", 1)
        self.arena = None

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.player = Player(self, 5, 5, self.player_img)
        self.render_map(self.player, self.map, "")
        self.staticFrames = 0

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        if self.arena:
            self.arena.draw_arena()
        pg.display.flip()

    def events(self):
        # catch all events here
        moved = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if not self.arena:
                if event.type == pg.KEYDOWN:
                    moved = True
                    if event.key == pg.K_ESCAPE:
                        self.quit()
                    if event.key == pg.K_LEFT:
                        self.player.move(dx=-1)
                    if event.key == pg.K_RIGHT:
                        self.player.move(dx=1)
                    if event.key == pg.K_UP:
                        self.player.move(dy=-1)
                    if event.key == pg.K_DOWN:
                        self.player.move(dy=1)
                    if event.key == pg.K_e:
                        self.player.interact()
                    if event.key == pg.K_a:
                        self.player.fight()
            else:
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    for btn in self.buttons:
                        if btn.rect.collidepoint(pos):
                            print(btn.text + " clicked!")
                            if btn.text == "button1":
                                if self.arena.player.attack(self.arena.monster):
                                    self.exit_arena()
                                    break
                                self.draw()
                                sleep(1)
                                if self.arena.monster.attack(self.arena.player):
                                    self.exit_arena()
                                    break
                            elif btn.type == "leftButton":
                                self.player.move(dx=-1)
                            elif btn.type == "rightButton":
                                self.player.move(dx=1)
                            elif btn.type == "forwardButton":
                                self.player.move(dy=-1)
                            elif btn.type == "backwardButton":
                                self.player.move(dy=1)
                            elif btn.type == "button5":
                                self.exit_arena()

        # print(self.player.x, self.player.y)
        if not moved:
            if self.staticFrames > 15:
                self.player.stand()
            else:
                self.staticFrames += 1
        else:
            self.staticFrames = 0

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
g.new()
g.run()
g.show_go_screen()
