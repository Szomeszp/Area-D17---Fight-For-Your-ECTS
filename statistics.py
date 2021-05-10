import pygame as pg
from settings import *

vec = pg.math.Vector2
from os import path


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
        return Statistics(2000 + 10 * level, 10 * level, 0, 0, 0, 1, 1, 20, 40)
