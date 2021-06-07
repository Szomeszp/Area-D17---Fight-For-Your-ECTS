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
        return Statistics(29 + 11 * level,
                          23 + 7 * level,
                          0,
                          0,
                          0,
                          1,
                          1,
                          (2 - 2 * (e ** (level / 13)) * 100),
                          (5 - 5 * (e ** (level / 19)) * 20))

    @staticmethod
    def generate_monster_statistics(level):
        return Statistics(29 + 11 * level,
                          23 + 7 * level,
                          0,
                          0,
                          0,
                          1,
                          1,
                          (2 - 2 * (e ** (level / 13)) * 100),
                          (5 - 5 * (e ** (level / 19)) * 20))
