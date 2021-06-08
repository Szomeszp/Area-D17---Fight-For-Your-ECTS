from random import randint
from json import load as json_load
from src.items import Key
from src.settings import *
from os import path


class Character:
    def __init__(self, game, x, y, character_type, statistics):
        self.game = game
        self.type = character_type
        self.rect = pg.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.x = x
        self.y = y
        self.statistics = statistics

    def attack(self, player):
        rng = randint(0, 100)
        if 0 <= rng <= self.statistics.critical_damage_chance:
            damage = float(self.statistics.damage * (1 + self.statistics.critical_damage_multiplier / 100))
        else:
            damage = float(self.statistics.damage)
        if type(self.type) == str:  # do poprawy
            self.game.arena.battle_log.add_log("Monster zadał " + str(damage) + " obrażeń")
        else:
            self.game.arena.battle_log.add_log("Player zadał " + str(damage) + " obrażeń")
        return player.hurt(damage)

    def hurt(self, damage):
        self.statistics.current_health = max(self.statistics.current_health - damage, 0)
        if self.statistics.current_health <= 0:
            return 1
        return 0

    def check_opponent_in_range(self, opponent):
        attack_range = self.statistics.attack_range
        for i in range(-attack_range, attack_range + 1):
            for j in range(-attack_range, attack_range + 1):
                if abs(i) + abs(j) <= attack_range:
                    rect = pg.Rect(self.rect.x + i * TILE_SIZE, self.rect.y + j * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if rect.colliderect(opponent):
                        return True
        return False


class Wall(pg.sprite.Sprite):
    def __init__(self, game, tiled_map, x, y, w, h):
        self.groups = tiled_map.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y


class Door(pg.sprite.Sprite):
    def __init__(self, game, map_name, tiled_map, x, y, w, h, out_name):
        self.groups = tiled_map.doors
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.map_name = map_name
        self.out_name = out_name


class NPC(pg.sprite.Sprite):
    def __init__(self, game, tiled_map, x, y, w, h, name):
        self.groups = tiled_map.walls, tiled_map.npcs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.name = name
        self.current_path = 0
        self.current_sub_path = -1

    def dialogue(self):
        with open(path.join(GAME_FOLDER, "../src/dialogues.json"), encoding='utf8') as file:
            dialogues_file = json_load(file)

        def print_dialogue():
            black_bar_rect_pos = (32, self.game.screen.get_height() - 160)
            black_bar_rect_size = (self.game.screen.get_width() - 64, 128)
            pg.draw.rect(self.game.screen, (128, 64, 32), pg.Rect(black_bar_rect_pos, black_bar_rect_size),
                         border_radius=4)

            space_text = self.game.my_small_font.render("Click [space] to continue", 1, (255, 255, 255))
            space_text_size = self.game.my_small_font.size("Click [space] to continue")
            self.game.screen.blit(space_text, (self.game.screen.get_width() - space_text_size[0] - 40,
                                               self.game.screen.get_height() - space_text_size[1] - 40))

            position = 152
            if self.current_path == -1 or self.name not in dialogues_file:
                text = "..."
            elif self.current_path == GET_KEY:
                key = Key(self.game, self.game.map, -100, -100)
                self.game.player.items.append(key)
                self.game.add_message(Message("Dostałeś klucz!"))
                self.current_path = -1
                return
            elif self.current_path == GET_SMALL_MEDICINE:
                if self.game.player.pay(20):
                    self.game.player.heal(self.game.player.statistics.max_health // 2)
                    self.game.add_message(Message("Zostałeś wyleczony"))
                    self.current_path = GET_SMALL_MEDICINE // 1000
                else:
                    self.current_path = NO_MONEY
            elif self.current_path == GET_BIG_MEDICINE:
                if self.game.player.pay(40):
                    self.game.player.heal(self.game.player.statistics.max_health)
                    self.game.add_message(Message("Zostałeś wyleczony"))
                    self.current_path = GET_BIG_MEDICINE // 1000
                else:
                    self.current_path = NO_MONEY
            if self.current_path != -1 and self.name in dialogues_file:
                text = dialogues_file[self.name]["paths"][self.current_path]["main_text"]
            rendered_text = self.game.my_big_font.render(text, 1, (255, 255, 255))
            self.game.screen.blit(rendered_text, (40, self.game.screen.get_height() - position))

            position = position - self.game.my_big_font.size(text)[1] - 8
            if self.current_path != -1 and self.name in dialogues_file:
                for i in range(dialogues_file[self.name]["paths"][self.current_path]["number_of_sub_paths"]):
                    text = dialogues_file[self.name]["paths"][self.current_path]["sub_paths"][i]["text"]

                    if i == self.current_sub_path:
                        text = ">>>  " + text

                    rendered_text = self.game.my_medium_font.render(text, 1, (255, 255, 255))
                    self.game.screen.blit(rendered_text, (40, self.game.screen.get_height() - position))
                    position = position - self.game.my_small_font.size(text)[1] - 8

        cnt = True
        reload = True
        while cnt:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                if reload:
                    print_dialogue()
                reload = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        if self.name in dialogues_file:
                            self.current_path = \
                                dialogues_file[self.name]["paths"][self.current_path]["sub_paths"][
                                    self.current_sub_path][
                                    "go_to"]
                            self.current_sub_path = -1
                            reload = True
                    elif event.key == pg.K_SPACE:
                        self.current_path = 0
                        self.current_sub_path = -1
                        cnt = False
                    elif event.key == pg.K_w:
                        if self.name in dialogues_file:
                            self.current_sub_path = (self.current_sub_path + 1) % \
                                                    dialogues_file[self.name]["paths"][self.current_path][
                                                        "number_of_sub_paths"]
                            reload = True
                    elif event.key == pg.K_s:
                        if self.name in dialogues_file:
                            self.current_sub_path = (self.current_sub_path - 1) % \
                                                    dialogues_file[self.name]["paths"][self.current_path][
                                                        "number_of_sub_paths"]
                            reload = True

                pg.display.flip()
                self.game.clock.tick(FPS) / 1000


class SecretDoor(Door):
    def __init__(self, game, map_name, tiled_map, x, y, w, h, out_name):
        super().__init__(game, map_name, tiled_map, x, y, w, h, out_name)
        self.groups = tiled_map.doors, tiled_map.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = pg.image.load(path.join(IMG_FOLDER, "stairs1.png"))


class Monster(pg.sprite.Sprite, Character):
    def __init__(self, game, tiled_map, spawn, x, y, type, statistics):
        self.groups = tiled_map.walls, tiled_map.monsters, tiled_map.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        Character.__init__(self, game, x, y, type, statistics)
        self.image = self.get_image()
        self.spawn = spawn

    def get_image(self):
        return pg.image.load(path.join(IMG_FOLDER, self.type + ".png"))

    def move_to_opponent(self, opponent):
        def x_move(dx):
            if dx > 0:
                self.rect.x += TILE_SIZE
            else:
                self.rect.x -= TILE_SIZE

        def y_move(dy):
            if dy > 0:
                self.rect.y += TILE_SIZE
            else:
                self.rect.y -= TILE_SIZE

        moves = self.statistics.move_range
        for i in range(moves):
            dy = opponent.y - self.rect.y // TILE_SIZE
            dx = opponent.x - self.rect.x // TILE_SIZE
            if abs(dx) > abs(dy):
                x_move(dx)
            elif abs(dx) < abs(dy):
                y_move(dy)
            else:
                if bool(randint(0, 1)):
                    x_move(dx)
                else:
                    y_move(dy)


class Message:
    def __init__(self, text):
        self.text = text
        self.duration = 100
