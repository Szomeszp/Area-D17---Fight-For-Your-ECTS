from math import ceil

from numpy import e


class Statistics:
    def __init__(self, hp, dmg, agility, intelligence, strength, move_range,
                 attack_range, crit_multiplier, crit_chance):
        self.current_health = hp
        self.max_health = hp
        self.damage = dmg
        self.agility = agility
        self.intelligence = intelligence
        self.strength = strength
        self.move_range = move_range
        self.attack_range = attack_range
        self.critical_damage_multiplier = crit_multiplier
        self.critical_damage_chance = crit_chance

    # def generate_statistics(self, hp, dmg, agility, intelligence, strength, move_range,
    #                        attack_range, crit_multiplier, crit_chance):
    #     return Statistics(self, hp, dmg, agility, intelligence, strength, move_range, attack_range,
    #                       crit_multiplier, crit_chance)

    @staticmethod
    def generate_player_statistics(level):
        return Statistics(100 + 10 * level,
                          10 + 5 * level,
                          0,
                          0,
                          0,
                          ceil(3 - 3 * (e ** (-level * 0.16))),
                          ceil(3 - 3 * (e ** (-level * 0.16))),
                          ceil(200 - 200 * (e ** (-level * 0.123))),
                          ceil(100 - 100 * (e ** (-level * 0.15))))

    @staticmethod
    def generate_monster_statistics(level):
        return Statistics(50 + 5 * level,
                          10 + 1 * level,
                          0,
                          0,
                          0,
                          1,
                          1,
                          ceil(200 - 200 * (e ** (-level * 0.0223))),
                          ceil(100 - 100 * (e ** (-level * 0.05))))
