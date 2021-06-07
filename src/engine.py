from sys import path, exit
from src.items import HealthPotion
from src.sprites import *
from src.tilemap import *
from src.arena import *
from src.player import Player


class Game:
    def __init__(self):
        pg.init()
        pg.key.set_repeat(500, 100)
        pg.display.set_caption(TITLE)
        self.map_img = None
        self.map_rect = None
        self.player_img = None
        self.map = None
        self.camera = None
        self.arena = None
        self.last_position = None
        self.player = None
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.DOUBLEBUF, 32)
        self.clock = pg.time.Clock()
        self.main_map = "map_alpha2.tmx"
        self.respawn_map = "map_hospital.tmx"
        self.maps = {}
        self.my_small_font = pg.font.SysFont('Arial Unicode MS', 16)
        self.my_medium_font = pg.font.SysFont('Arial Unicode MS', 24)
        self.my_big_font = pg.font.SysFont('Arial Unicode MS', 32)
        self.load_map(self.main_map)
        self.load_map(self.respawn_map)
        self.load_data()
        self.current_time = 0
        self.messages = []

    def load_data(self):
        self.load_map(self.main_map)
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = PlayerImg.STATIC_DOWN

    def load_map(self, map_name):
        if map_name not in self.maps:
            self.init_map(map_name)
        self.map = self.maps.get(map_name)

    def init_map(self, map_name):
        tiled_map = TiledMap(path.join(MAP_FOLDER, map_name))
        self.maps[map_name] = tiled_map
        return tiled_map

    def get_through_door(self, door=None):
        if door is not None:
            new_map = door.map_name
            spawn = door.out_name + "_spawn"
            if door.out_name == "door_secret_room_in":
                self.last_position = [door.x, door.y, door.map_name]
                door.kill()
            elif door.out_name == "door_secret_room_out":
                self.player.x = self.last_position[0] // TILE_SIZE
                self.player.y = self.last_position[1] // TILE_SIZE
        else:
            spawn = " "
            new_map = self.main_map
        self.load_map(new_map)
        self.add_objects(self.player, spawn)

    def add_objects(self, player, spawn, arena_exited=False):
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.map.all_sprites.add(player)
        self.player.map = self.map

        objs_created = False
        if len(self.map.walls.sprites()) > 0:
            objs_created = True

        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == "player" and not arena_exited:
                self.player.x = int(tile_object.x // TILE_SIZE)
                self.player.y = int(tile_object.y // TILE_SIZE)
            if tile_object.name == spawn:
                self.player.x = int(tile_object.x // TILE_SIZE)
                self.player.y = int(tile_object.y // TILE_SIZE)
            if not objs_created:
                if tile_object.name == "wall":
                    Wall(self, self.map, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
                if tile_object.type == "door":
                    Door(self, tile_object.map, self.map, tile_object.x, tile_object.y, tile_object.width,
                         tile_object.height,
                         tile_object.name)
                if tile_object.type == "npc":
                    NPC(self, self.map, tile_object.x, tile_object.y, tile_object.width, tile_object.height,
                        tile_object.name)
                if tile_object.type == "monster_spawn":
                    self.map.monsters_spawns.append(MonsterSpawn(self, self.map, tile_object.x, tile_object.y,
                                                                 tile_object.width, tile_object.height, 1,
                                                                 tile_object.name, randint(20000, 30000)))
                if tile_object.type == "secret_door_spawn":
                    self.map.secret_doors_spawns.append(SecretDoorSpawn(self, self.map, tile_object.x, tile_object.y,
                                                                        tile_object.width, tile_object.height))
                if tile_object.type == "money_spawn":
                    MoneySpawn(self, self.map, tile_object.x, tile_object.y,
                               tile_object.width, tile_object.height, 20)
                if tile_object.name == "small_potion":
                    HealthPotion(self, self.map, tile_object.x, tile_object.y, 100, "small_potion")
                if tile_object.name == "big_potion":
                    HealthPotion(self, self.map, tile_object.x, tile_object.y, 500, "big_potion")

        if not objs_created:
            for secret_door in self.map.secret_doors_spawns:
                secret_door.spawn_secret_door()
        self.camera = Camera(self.map.width, self.map.height)

    def create_arena(self, monster, arena):
        self.last_position = [[self.player.x, self.player.y], [monster.rect.x, monster.rect.y], self.map]
        self.arena = Arena(self, self.player, monster, arena)
        self.add_objects(self.player, "", True)

    def new(self):
        self.player = Player(self, self.map, 5, 5, self.player_img)
        self.add_objects(self.player, self.main_map, False)

    def run(self):
        while True:
            self.current_time = pg.time.get_ticks()
            if not self.arena:
                if self.player.is_dead:
                    pass
                else:
                    self.game_events()
                self.update()
                self.draw()
            else:
                self.arena.arena_events()

            pg.time.Clock().tick(30)

    def update(self):
        for spawn in self.map.monsters_spawns:
            if self.current_time - spawn.last_spawn > spawn.spawn_time:
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

        if not self.arena:
            if self.player.is_dead:
                self.player.dead_screen()
            else:
                self.player.draw_gui()
                if len(self.messages) > 0:
                    self.show_message()

        pg.display.flip()

    def add_message(self, message):
        self.messages.append(message)

    def show_message(self):
        text = self.messages[0].text
        message = self.my_medium_font.render(text, True, (255, 255, 255))
        message_size = self.my_medium_font.size(text)

        x = self.camera.apply_rect(self.map_rect).x + self.player.rect.x
        y = self.camera.apply_rect(self.map_rect).y + self.player.rect.y

        pos = (x - message_size[0] / 2 + 12, y - message_size[1] - 2)
        size = (message_size[0] + 8, message_size[1] + 4)
        pg.draw.rect(self.screen, BLACK, pg.Rect(pos, size), border_radius=4)

        self.screen.blit(message, (x - message_size[0] / 2 + 16, y - message_size[1] + 1))
        self.messages[0].duration -= 1

        if self.messages[0].duration == 0:
            self.messages.pop(0)

    def game_events(self):
        def quit_game():
            pg.quit()
            exit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()
            if not self.arena:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        quit_game()
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

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass
