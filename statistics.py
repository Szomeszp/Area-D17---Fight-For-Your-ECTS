import pygame as pg
from settings import *
from os import path
from numpy import e


class Statistics:
    def __init__(self, hp, dmg, agility, intelligence, strength, moveRange, attackRange, critMultiplier, critChance):
        self.current_health = hp
        self.max_health = hp
        self.damage = dmg
        self.agility = agility
        self.intelligence = intelligence
        self.strength = strength
        self.move_range = moveRange
        self.attack_range = attackRange
        self.critical_damage_multiplier = critMultiplier
        self.critical_damage_chance = critChance

    @staticmethod
    def generateMonsterStatistics(self, level):
        return Statistics(29 + 11 * level, 23 + 7*level, 0, 0, 0, 1, 1, (2 - 2 * (e ** (level / 13)) * 100),  (5 - 5 * (e ** (level / 19)) * 20))
