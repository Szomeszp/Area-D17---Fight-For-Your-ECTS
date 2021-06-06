from time import sleep

import pygame as pg
import sys
from os import path

from items import HealthPotion
from player import *
from settings import *
from sprites import *
from tilemap import *
from statistics import *
from random import randint
from arena import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF, 32)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.main_map = "map_alpha2.tmx"
        self.maps = {}
        self.secret_room_entered = False
        self.my_small_font = pg.font.SysFont('Arial Unicode MS', 16)
        self.my_medium_font = pg.font.SysFont('Arial Unicode MS', 24)
        self.my_big_font = pg.font.SysFont('Arial Unicode MS', 32)
        self.arena = None
        self.load_map(self.main_map)
        self.load_data()
        self.current_time = 0
        # self.init_groups()

    # def init_groups(self):
    #     self.all_sprites = pg.sprite.Group()
    #     self.walls = pg.sprite.Group()
    #     self.doors = pg.sprite.Group()
    #     self.npcs = pg.sprite.Group()
    #     self.monsters = pg.sprite.Group()
    #     self.buttons = pg.sprite.Group()

    # def clear_groups(self):
    #     self.all_sprites.empty()
    #     self.walls.empty()
    #     self.doors.empty()
    #     self.npcs.empty()
    #     self.monsters.empty()
    #     self.buttons.empty()

    def load_data(self):
        self.load_map(self.main_map)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = PlayerImg.DOWN

    def load_map(self, map_name):
        print(map_name)
        if map_name not in self.maps:
            self.init_map(map_name)
        self.map = self.maps.get(map_name)

    def init_map(self, map_name):
        print(map_name)
        map = TiledMap(path.join(MAP_FOLDER, map_name))
        self.maps[map_name] = map
        return map

    def get_through_door(self, door=None):
        if door is not None:
            new_map = door.map_name
            spawn = door.out_name + "_spawn"
            if door.out_name == "secret_door_out":
                # jak wejdziesz juz w secret door to je usun
                door.kill()
        else:
            spawn = " "
            new_map = self.main_map
        print(new_map)
        self.load_map(new_map)
        # self.clear_groups()
        self.render_map(self.player, spawn)

    # funkcja powinna sie nazywac add_objects
    def render_map(self, player, spawn, arena_exited=0):
        # self.map = new_map
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        random_door_locations = []
        self.map.all_sprites.add(player)
        self.player.map = self.map

        objs_created = False
        if len(self.map.walls.sprites()) > 0:
            objs_created = True

        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player" and not arena_exited:
                self.player.x = int(tile_object.x // TILESIZE)
                self.player.y = int(tile_object.y // TILESIZE)
            if tile_object.name == spawn:
                self.player.x = int(tile_object.x // TILESIZE)
                self.player.y = int(tile_object.y // TILESIZE)
            if not objs_created:
                if tile_object.name == "wall":
                    # print("sciana")
                    Wall(self, self.map, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                if tile_object.type == "door":
                    print(tile_object.map)
                    Door(self, tile_object.map, self.map, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                         tile_object.name)
                if tile_object.type == "npc":
                    print("Npc")
                    NPC(self, self.map, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.name)
                # if tile_object.type == "monster":
                #     stats = Statistics.generateMonsterStatistics(self, 1)
                #     Monster(self, self.map, int(tile_object.x // TILESIZE) * TILESIZE,
                #             int(tile_object.y // TILESIZE) * TILESIZE,
                #             "monster", stats)
                if tile_object.type == "monster_spawn":
                    self.map.monsters_spawns.append(MonsterSpawn(self, self.map, tile_object.x, tile_object.y,
                                                                 tile_object.width, tile_object.height, 2))
                if tile_object.type == "secret_door_spawn":
                    self.map.secret_doors_spawns.append(SecretDoorSpawn(self, self.map, tile_object.x,tile_object.y,
                                                                        tile_object.width, tile_object.height))
        if not objs_created:
            print(self.map.map_name)
            if self.map.map_name == "map_alpha2.tmx":
                print("Potions spawned")
                HealthPotion(self, self.map, 480, 1664, 500, "big_potion")
                HealthPotion(self, self.map, 512, 1696, 100, "small_potion")
            for secret_door in self.map.secret_doors_spawns:
                secret_door.spawn_secret_door()
        self.camera = Camera(self.map.width, self.map.height)

    def create_arena(self, monster, arena):
        self.last_position = [[self.player.x, self.player.y], [monster.rect.x, monster.rect.y], self.map]
        self.arena = Arena(self, self.player, monster, arena)
        self.render_map(self.player, "", 1)

    def new(self):
        # initialize all variables and do all the setup for a new game
        # self.clear_groups()
        self.player = Player(self, self.map, 5, 5, self.player_img)
        self.render_map(self.player, self.main_map, "")
        self.staticFrames = 0

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.current_time = pg.time.get_ticks()
            self.dt = self.clock.tick(FPS) / 1000
            # self.events()
            if not self.arena:
                if self.player.is_dead:
                    pass
                else:
                    self.game_events()

                self.update()
                self.draw()
            else:
                self.arena.arena_events()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        for spawn in self.map.monsters_spawns:
            if self.current_time - spawn.last_spawn > 10000:
                spawn.spawn_n_monsters(1)
        self.map.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        if self.arena:
            self.arena.draw_arena()
        for sprite in self.map.all_sprites:
            if sprite != self.player:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.player.image, self.camera.apply(self.player))

        # TODO
        if not self.arena:
            if self.player.is_dead:
                print("PLAYER IS DEAD!")
                self.player.dead_screen()
                print("IM BACK!!!!")
            else:
                self.player.draw_gui()

        pg.display.flip()

    def game_events(self):
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
                    if event.key == pg.K_LEFT or event.key == pg.K_a:
                        self.player.move(dx=-1)
                    if event.key == pg.K_RIGHT or event.key == pg.K_d:
                        self.player.move(dx=1)
                    if event.key == pg.K_UP or event.key == pg.K_w:
                        self.player.move(dy=-1)
                    if event.key == pg.K_DOWN or event.key == pg.K_s:
                        self.player.move(dy=1)
                    if event.key == pg.K_e:
                        self.player.interact()
                    if event.key == pg.K_q:
                        self.player.fight()
                    if event.key == pg.K_c:
                        self.player.collect_item()
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
