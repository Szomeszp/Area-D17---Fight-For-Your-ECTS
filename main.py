import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.last_door = None  # ?

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
        else:
            new_map = self.main_map
        self.map = TiledMap(path.join(self.map_folder, new_map))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == "player":
                # do przemyślenia moze obiekt do spawnu przed drzwiami
                # albo z tym last_door ale tez zapisujemy ruchem w którą strone weszlismy w drzwi
                if new_map != self.main_map:
                    offset = -1
                else:
                    offset = 1
                if self.last_door != None:
                    self.player = Player(self, self.last_door.x // TILESIZE, (self.last_door.y // TILESIZE) + offset)
                else:
                    # moze nie zawsze działac zaleznie jak sa polozone drzwi
                    self.player = Player(self, tile_object.x // TILESIZE, (tile_object.y // TILESIZE))
                self.last_door = door
            if tile_object.name == "wall":
                Wall(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == "door":
                if new_map != self.main_map:
                    Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, self.main_map)
                else:
                    # bo narazie mamy tylko jedne drzwi
                    Door(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height, "map_d17.tmx")
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