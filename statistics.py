import pygame as pg
from settings import *

vec = pg.math.Vector2
from os import path


class Statistics:
    def __init__(self, hp, dmg, agility, intelligence, strength, moveRange, attackRange, critMultiplier, critChance):
        self.health = hp
        self.damage = dmg
        self.agility = agility
        self.intelligence = intelligence
        self.strength = strength
        self.moveRange = moveRange
        self.attackRange = attackRange
        self.criticalDamageMultiplier = critMultiplier
        self.criticalDamageChance = critChance

    @staticmethod
    def generateMonsterStatistics(self, level):
        return Statistics(20 + 10 * level, 5 * level, 0, 0, 0, 1, 1, 10, 10)
