# Copyright (C) 2005 Colin McMillen <mcmillen@cs.cmu.edu>
#
# This file is part of GalaxyMage.
#
# GalaxyMage is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# GalaxyMage is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GalaxyMage; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.

import random
import Unit
from twisted.spread import pb

class Class(pb.Copyable, pb.RemoteCopy):

    _allStats = ["mhp", "msp", "watk", "wdef", "matk", "mdef", "speed"]
    
    def __init__(self,
                 name,
                 abilities,
                 spriteRoot,
                 move, jump,
                 mhpBase, mhpGrowth, mhpMult,
                 mspBase, mspGrowth, mspMult,
                 watkBase, watkGrowth, watkMult,
                 wdefBase, wdefGrowth, wdefMult,
                 matkBase, matkGrowth, matkMult,
                 mdefBase, mdefGrowth, mdefMult,
                 speedBase, speedGrowth, speedMult):
        self.name = name
        self.abilities = abilities
        self._spriteRoot = spriteRoot
        self.move = move
        self.jump = jump
        self.mhpBase = mhpBase
        self.mhpGrowth = mhpGrowth
        self.mhpMult = mhpMult
        self.mspBase = mspBase
        self.mspGrowth = mspGrowth
        self.mspMult = mspMult
        self.watkBase = watkBase
        self.watkGrowth = watkGrowth
        self.watkMult = watkMult
        self.wdefBase = wdefBase
        self.wdefGrowth = wdefGrowth
        self.wdefMult = wdefMult
        self.matkBase = matkBase
        self.matkGrowth = matkGrowth
        self.matkMult = matkMult
        self.mdefBase = mdefBase
        self.mdefGrowth = mdefGrowth
        self.mdefMult = mdefMult
        self.speedBase = speedBase
        self.speedGrowth = speedGrowth
        self.speedMult = speedMult
        
    def createUnit(self, gender):
        u = Unit.Unit(gender)
        self.equip(u)
        for stat in Class._allStats:
            base = self.__dict__[stat + "Base"]
            x = base / 20
            y = (random.randint(0, 2*x) +
                 random.randint(0, 2*x) -
                 random.randint(0, 2*x) -
                 random.randint(0, 2*x)) / 2
            u.__dict__["_" + stat] = base + x + y
            growthMod = random.gauss(1, 0.1)
            growthMod = min(1.5, growthMod)
            growthMod = max(0.5, growthMod)
            u.__dict__["_" + stat + "GrowthMod"] = growthMod
        u.incrementClassLevel(self.name)
        self.addAbilities(u)
        return u

    # FIXME: move the creation / levelup code into unit?
    def levelUp(self, u):
        for stat in Class._allStats:
            growth = self.__dict__[stat + "Growth"]
            growth *= u.__dict__["_" + stat + "GrowthMod"]
            u.__dict__["_" + stat] += int(growth)
            if random.random() < growth - int(growth):
                u.__dict__["_" + stat] += 1
        u.incrementClassLevel(self.name)
        self.addAbilities(u)
        self.equip(u)

    def addAbilities(self, u):
        for (requiredLevel, ability) in self.abilities:
            if u.classLevel(self.name) == requiredLevel:
                u.addAbility(ability)

    # Called when the unit equips this class
    def equip(self, u):
        u._class = self

    def spriteRoot(self):
        return self._spriteRoot

