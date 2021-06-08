from random import randint
from time import sleep
from src.settings import *
from src.items import HealthPotion
from src.tilemap import TiledMap, Camera


class Arena:
    def __init__(self, game, player, monster, arena):
        self.game = game
        self.player = player
        self.monster = monster
        self.game.map = TiledMap(path.join(MAP_FOLDER, arena))
        self.game.map_img = self.game.map.make_map()
        self.game.map_rect = self.game.map_img.get_rect()
        self.turn = 0
        self.result = 0
        self.show_move_range = False
        self.cant_move_logged = False
        self.move_rects = []
        self.control_panel = None
        self.monster_hp_bar = None
        self.player_hp_bar = None
        self.battle_info = None
        self.battle_log = None
        self.statistics_panel = None
        self.ring = None
        self.random_token = randint(0, 1)
        self.possible_moves = player.statistics.move_range
        self.possible_attacks = 1

    def draw_arena(self):
        self.monster_hp_bar.draw_health()
        self.player_hp_bar.draw_health()
        self.battle_info.draw_info()
        self.control_panel.draw_buttons()
        self.battle_log.draw_logs()
        self.draw_target_in_range()
        self.statistics_panel.draw_stats()
        if self.show_move_range:
            self.draw_move_range()

    def enter_battle_arena(self):
        self.player.stand()
        self.control_panel = ControlPanel(self)

        for tile_object in self.game.map.tmx_data.objects:
            if str(tile_object.name)[:6] == "button":
                get_name = {
                    "1": BUTTON_ONE,
                    "2": BUTTON_TWO,
                    "3": BUTTON_THREE,
                    "4": BUTTON_FOUR,
                    "5": BUTTON_FIVE
                }

                self.control_panel.add_button(
                    Button(
                        self.game,
                        tile_object.x,
                        tile_object.y,
                        tile_object.width,
                        tile_object.height,
                        get_name[str(tile_object.name)[-1:]],
                        tile_object.name
                    )
                )

            if tile_object.name == "item1":
                if len(self.player.items) > 0 and isinstance(self.player.items[0], HealthPotion):
                    self.player.items[0].rect.x = tile_object.x
                    self.player.items[0].rect.y = tile_object.y
                    self.game.map.all_sprites.add(self.player.items[0])
                    self.game.map.items.add(self.player.items[0])
            if tile_object.name == "item2":
                if len(self.player.items) > 1 and isinstance(self.player.items[0], HealthPotion):
                    self.player.items[1].rect.x = tile_object.x
                    self.player.items[1].rect.y = tile_object.y
                    self.game.map.all_sprites.add(self.player.items[1])
                    self.game.map.items.add(self.player.items[1])

            if tile_object.name == "monsterHealthBar":
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
            if tile_object.name == "statistics":
                self.statistics_panel = StatisticsPanel(self, tile_object.x, tile_object.y, tile_object.width,
                                                        tile_object.height)
            if tile_object.type == "arena":
                self.ring = pg.Rect(tile_object.x, tile_object.y, tile_object.width, tile_object.height)

            if tile_object.type == "spawnPlayer":
                dx = randint(0, int(tile_object.width // TILE_SIZE) - 1)
                dy = randint(0, int(tile_object.height // TILE_SIZE) - 1)
                self.player.x = int((tile_object.x // TILE_SIZE) + dx)
                self.player.y = int((tile_object.y // TILE_SIZE) + dy)
                self.game.map.all_sprites.add(self.player)
            if tile_object.type == "spawnMonster":
                dx = randint(0, int(tile_object.width // TILE_SIZE) - 1)
                dy = randint(0, int(tile_object.height // TILE_SIZE) - 1)
                self.monster.rect.x = int((tile_object.x // TILE_SIZE) + dx) * TILE_SIZE
                self.monster.rect.y = int((tile_object.y // TILE_SIZE) + dy) * TILE_SIZE
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
        self.game.add_objects(self.player, "", 1)
        self.game.arena = None

    def button_handler(self, pos):
        for btn in self.control_panel.buttons:
            if btn.rect.collidepoint(pos):
                if btn.type == "button1":
                    if self.possible_attacks:
                        if self.player.check_opponent_in_range(self.monster):
                            if self.player.attack(self.monster):
                                self.result = 1
                            self.possible_attacks -= 1
                        else:
                            self.battle_log.add_log("MONSTER OUT OF RANGE!", RED)
                    else:
                        self.battle_log.add_log("YOU ALREADY ATTACKED!", RED)
                elif btn.type == "button2":
                    pass
                elif btn.type == "button3":
                    pass
                elif btn.type == "button4":
                    self.turn += 1
                elif btn.type == "button5":
                    self.exit_arena()

                self.player.stand()

    def arena_events(self):
        def quit_game():
            pg.quit()
            exit()

        self.result = 0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit_game()

            if self.turn % 2 == self.random_token:
                self.create_move_rects()
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    self.button_handler(pos)

                    if self.player.rect.collidepoint(pos):
                        if self.show_move_range:
                            self.show_move_range = False
                        else:
                            self.show_move_range = True
                        if len(self.move_rects) == 0 and not self.cant_move_logged:
                            self.cant_move_logged = True
                            self.battle_log.add_log("YOU CAN'T MOVE ANYMORE!", RED)

                    if self.show_move_range:
                        for move_rect in self.move_rects:
                            if move_rect.rect.collidepoint(pos):
                                prev_x = self.player.x
                                prev_y = self.player.y
                                self.player.x = move_rect.x // TILE_SIZE
                                self.player.y = move_rect.y // TILE_SIZE
                                dx = self.player.x - prev_x
                                dy = self.player.y - prev_y
                                self.possible_moves -= abs(dx) + abs(dy)
                                self.battle_log.add_log("Player poruszyl sie")

                    if self.player.check_opponent_in_range(self.monster):
                        if self.monster.rect.collidepoint(pos):
                            if self.possible_attacks:
                                if self.player.attack(self.monster):
                                    self.result = 1
                                self.possible_attacks -= 1
                            else:
                                self.battle_log.add_log("YOU ALREADY ATTACKED!", RED)

                    for item in self.game.map.items:
                        if item.rect.collidepoint(pos):
                            hp = self.player.use_potion(item)
                            self.battle_log.add_log(f"Player uleczyl się za {hp} hp")

            else:
                if self.monster.check_opponent_in_range(self.player):
                    if self.monster.attack(self.game.arena.player):
                        self.result = -1
                else:
                    self.monster.move_to_opponent(self.player)
                    self.battle_log.add_log("Monster poruszyl sie")
                self.possible_moves = self.player.statistics.move_range
                self.possible_attacks = 1
                self.cant_move_logged = False
                self.turn += 1

            # PLAYER WON
            if self.result == 1:
                self.game.last_position[2].monsters.remove(self.monster)
                self.game.last_position[2].all_sprites.remove(self.monster)
                self.player.money += self.monster.statistics.max_health
                self.monster.spawn.last_spawn = pg.time.get_ticks()
                self.monster.spawn.current_monsters -= 1
                self.monster.spawn.level += 1
                self.monster.kill()
                self.game.arena.player.level_up(200)
                self.battle_log.add_log("Player wygrał")

            # PLAYER LOST
            elif self.result == -1:
                self.player.is_dead = True
                self.player.remaining_respawn_time = self.player.respawn_time
                self.player.money //= 2
                self.game.last_position[0][0] = 30
                self.game.last_position[0][1] = 21
                self.game.last_position[2] = self.game.maps[self.game.respawn_map]
                self.battle_log.add_log("Player zginal")

            self.game.update()
            self.game.draw()

            if self.result != 0:
                sleep(1)
                self.exit_arena()
                break
            else:
                pg.event.clear()

    def draw_move_range(self):
        for rect in self.move_rects:
            self.game.screen.blit(CAN_MOVE_IMG, (rect.x, rect.y))

    def create_move_rects(self):
        self.move_rects = []
        move_range = self.possible_moves
        for i in range(-move_range, move_range + 1):
            for j in range(-move_range, move_range + 1):
                if abs(i) + abs(j) <= move_range:
                    if i == 0 and j == 0:
                        continue
                    rect = pg.Rect((self.player.x + i) * TILE_SIZE, (self.player.y + j) * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(self.ring) and not rect.colliderect(self.monster):
                        self.move_rects.append(MoveRect(self.game, (self.player.x + i) * TILE_SIZE,
                                                        (self.player.y + j) * TILE_SIZE))

    def draw_target_in_range(self):
        if self.player.check_opponent_in_range(self.monster):
            x = self.monster.rect.x
            y = self.monster.rect.y
            self.game.screen.blit(CAN_ATTACK_IMG, (x, y))


class MoveRect:
    def __init__(self, game, x, y):
        self.game = game
        self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y

    def draw_rect(self):
        color = (65, 105, 225)
        border = 2
        gap = 3
        border_color = BLACK
        # draw border
        pg.draw.rect(self.game.screen, border_color, pg.Rect((self.x + gap, self.y + gap), (TILE_SIZE - 2 * gap,
                                                                                            TILE_SIZE - 2 * gap)))
        # draw rect
        pg.draw.rect(self.game.screen, color, pg.Rect((self.x + border + gap, self.y + border + gap),
                                                      (TILE_SIZE - 2 * (border + gap), TILE_SIZE - 2 * (border + gap))))


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
            pg.draw.rect(self.game.screen, GREEN, pg.Rect((self.x, self.y), (self.width * ratio, self.height)),
                         border_bottom_left_radius=4, border_top_left_radius=4)
            pg.draw.rect(self.game.screen,
                         RED,
                         pg.Rect((self.x + self.width * ratio, self.y),
                                 (self.width * (1 - ratio), self.height)),
                         border_bottom_right_radius=4,
                         border_top_right_radius=4)


class StatisticsPanel:
    def __init__(self, arena, x, y, w, h):
        self.arena = arena
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def draw_stats(self):
        pg.draw.rect(self.arena.game.screen, BLACK, pg.Rect((self.x, self.y),
                                                            (self.width, self.height)), border_radius=4)
        i = 0
        text = self.arena.game.my_small_font.render(f"DMG: {self.arena.player.statistics.damage}", True, WHITE)
        text_size = self.arena.game.my_small_font.size(f"DMG: {self.arena.player.statistics.damage}")
        self.arena.game.screen.blit(text,
                                    (self.x + 4, self.y + 4 + i * text_size[1]))
        i = i + 1

        if self.arena.possible_moves == 0:
            color = RED
        else:
            color = WHITE
        text = self.arena.game.my_small_font.render(f"MOVE RANGE: {self.arena.possible_moves} /"
                                                    f" {self.arena.player.statistics.move_range}", True, color)
        text_size = self.arena.game.my_small_font.size(f"MOVE RANGE: {self.arena.possible_moves} /"
                                                       f" {self.arena.player.statistics.move_range}")
        self.arena.game.screen.blit(text,
                                    (self.x + 4, self.y + 4 + i * text_size[1]))
        i = i + 1

        text = self.arena.game.my_small_font.render(f"ATTACK RANGE: {self.arena.player.statistics.attack_range}",
                                                    True, WHITE)
        text_size = self.arena.game.my_small_font.size(f"ATTACK RANGE: {self.arena.player.statistics.attack_range}")
        self.arena.game.screen.blit(text, (self.x + 4, self.y + 4 + i * text_size[1]))
        i = i + 1


class BattleInfo:
    def __init__(self, game, x, y, w, h, info):
        self.game = game
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.info = info

    def draw_info(self):
        text = self.game.my_big_font.render(self.info, True, (255, 255, 255))
        text_size = self.game.my_big_font.size(self.info)
        self.game.screen.blit(text, (self.x + self.width / 2 - text_size[0] / 2,
                                     self.y + self.height / 2 - text_size[1] / 2))


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

    def add_log(self, text, color=WHITE):
        if len(self.logs) + 1 > self.max_len:
            self.logs.pop(0)
        self.logs.append([text, color])

    def draw_logs(self):
        pos = (self.x, self.y)
        size = (self.width, self.height)
        pg.draw.rect(self.game.screen, BLACK, pg.Rect(pos, size), border_radius=4)
        for idx, log in enumerate(self.logs):
            text = self.game.my_small_font.render(log[0], 1, log[1])
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
    def __init__(self, game, x, y, w, h, text, btn_type):
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.type = btn_type

    def draw_button(self):
        # draw background
        pos = (self.x, self.y)
        size = (self.width, self.height)
        pg.draw.rect(self.game.screen, BLACK, pg.Rect(pos, size), border_radius=4)
        # draw text
        btn = self.game.my_medium_font.render(self.text, 1, (255, 255, 255))
        btn_size = self.game.my_medium_font.size(self.text)
        self.game.screen.blit(btn, (self.x + self.width / 2 - btn_size[0] / 2,
                                    self.y + self.height / 2 - btn_size[1] / 2))
