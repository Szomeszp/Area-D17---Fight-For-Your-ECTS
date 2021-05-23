import random

import pygame as pg
from settings import *
import pytmx

from sprites import Monster
from statistics import Statistics


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.map_name = filename.split("/")[-1]
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.monsters_spawns = []
        self.secretdoors_spawns = []

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                                y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Spawn:
    def __init__(self, game, map, x, y, w, h):
        self.game = game
        self.map = map
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.last_seen = -1

    # Wersja Demo Tylko Dla Spawna Monstera
    def spawn_n_objects(self, n):
        for i in range(n):
            while True:
                dx = random.randint(0, int(self.width // TILESIZE) - 1)
                dy = random.randint(0, int(self.height // TILESIZE) - 1)
                x = int((self.x // TILESIZE) + dx) * TILESIZE
                y = int((self.y // TILESIZE) + dy) * TILESIZE
                rect = pg.Rect(x, y, TILESIZE, TILESIZE)
                for monster in self.map.monsters:
                    if rect.colliderect(monster):
                        continue
                break
            stats = Statistics.generateMonsterStatistics(self, 1)
            Monster(self.game, self.map, x, y, "monster", stats)




class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        # players moves to the right sa offset moves to the left
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

