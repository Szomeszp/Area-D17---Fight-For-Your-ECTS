import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from random import randint

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.last_door = None  # ?
        self.secret_room_entered = False

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, "img")
        self.main_map = 'map_alpha2.tmx'
        self.map_folder = path.join(game_folder, "maps")
        self.map = TiledMap(path.join(self.map_folder, self.main_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = PlayerImg.DOWN

    def render_map(self, door=None):
        if door is not None:
            new_map = door.map
            spawn = door.name + "_spawn"
            if door.name == "secret_door_out":
                self.secret_room_entered = True
        else:
            spawn = " "
            new_map = self.main_map
        self.map = TiledMap(path.join(self.map_folder, new_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        random_door_locations = []

        for tile_object in self.map.tmxdata.objects:
            if door is None:
                if tile_object.name == "player":
                    self.player = Player(self, tile_object.x // TILESIZE, (tile_object.y // TILESIZE))
            if tile_object.name == spawn:
                self.player = Player(self, tile_object.x // TILESIZE, (tile_object.y // TILESIZE))
            if tile_object.name == "wall":
                Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.type == "door":
                Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, tile_object.map, tile_object.name)
            if tile_object.name == "npc":
                NPC(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if not self.secret_room_entered:
                if tile_object.name == "random_door":
                    for dx in range(int(tile_object.width // TILESIZE)):
                        for dy in range(int(tile_object.height // TILESIZE)):
                            random_door_locations.append([int((tile_object.x // TILESIZE) + dx), int((tile_object.y // TILESIZE) + dy)])

        # print(len(random_door_locations))
        if not self.secret_room_entered:
            if len(random_door_locations) > 0:
                random_location = random_door_locations[randint(0, len(random_door_locations) - 1)]
                print(random_location)
                SecretDoor(self, random_location[0] * TILESIZE, random_location[1] * TILESIZE, TILESIZE, TILESIZE, "map_kapitol.tmx", "secret_door_out")

        self.camera = Camera(self.map.width, self.map.height)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.render_map()
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
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pg.display.flip()

    def events(self):
        # catch all events here
        moved = False
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
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
        if not moved:
            self.staticFrames += 1
        else:
            self.staticFrames = 0
        if self.staticFrames > 15:
            self.player.stand()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()