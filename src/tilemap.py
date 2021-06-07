from random import randint
from os import path

from src.items import Coin
from src.settings import *
from pytmx import load_pygame, TiledTileLayer
from src.sprites import Monster, SecretDoor
from src.statistics import Statistics


class TiledMap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename, pixelalpha=True)
        self.map_name = filename.split(path.sep)[-1]
        self.width = self.tmx_data.width * self.tmx_data.tilewidth
        self.height = self.tmx_data.height * self.tmx_data.tileheight
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.monsters_spawns = []
        self.secret_doors_spawns = []

    def render(self, surface):
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmx_data.tilewidth,
                                                y * self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


class Spawn:
    def __init__(self, game, tiled_map, x, y, w, h):
        self.game = game
        self.map = tiled_map
        self.x = x
        self.y = y
        self.width = w
        self.height = h


class SecretDoorSpawn(Spawn):
    def __init__(self, game, tiled_map, x, y, w, h):
        super().__init__(game, tiled_map, x, y, w, h)

    def spawn_secret_door(self):
        dx = randint(0, int(self.width // TILE_SIZE) - 1)
        dy = randint(0, int(self.height // TILE_SIZE) - 1)
        x = int((self.x // TILE_SIZE) + dx) * TILE_SIZE
        y = int((self.y // TILE_SIZE) + dy) * TILE_SIZE
        out_map_name = "secret_room.tmx"
        SecretDoor(self, out_map_name, self.map, x, y, TILE_SIZE, TILE_SIZE, "door_secret_room_in")


class MonsterSpawn(Spawn):
    def __init__(self, game, map, x, y, w, h, max_monsters, name, spawn_time):
        super().__init__(game, map, x, y, w, h)
        self.max_monsters = max_monsters
        self.current_monsters = 0
        self.last_spawn = -30001
        self.monster_name = name
        self.level = 1
        self.spawn_time = spawn_time

    def spawn_n_monsters(self, n):
        self.last_spawn = self.game.current_time
        i = 0
        while i < n and self.current_monsters < self.max_monsters:
            while True:
                dx = randint(0, int(self.width // TILE_SIZE) - 1)
                dy = randint(0, int(self.height // TILE_SIZE) - 1)
                x = int((self.x // TILE_SIZE) + dx) * TILE_SIZE
                y = int((self.y // TILE_SIZE) + dy) * TILE_SIZE
                rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                for monster in self.map.monsters:
                    if rect.colliderect(monster):
                        continue
                break
            stats = Statistics.generate_monster_statistics(self.level)
            Monster(self.game, self.map, self, x, y, self.monster_name, stats)
            self.current_monsters += 1
            i += 1


class MoneySpawn(Spawn):
    def __init__(self, game, map, x, y, w, h, max_coins):
        super().__init__(game, map, x, y, w, h)
        self.max_coins = max_coins
        self.spawn_coins()

    def spawn_coins(self):
        i = 0
        while i < self.max_coins:
            while True:
                dx = randint(0, int(self.width // TILE_SIZE) - 1)
                dy = randint(0, int(self.height // TILE_SIZE) - 1)
                x = int((self.x // TILE_SIZE) + dx) * TILE_SIZE
                y = int((self.y // TILE_SIZE) + dy) * TILE_SIZE
                rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
                for item in self.map.items:
                    if rect.colliderect(item):
                        continue
                break
            Coin(self.game, self.map, x, y)
            i += 1


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
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        self.camera = pg.Rect(x, y, self.width, self.height)

