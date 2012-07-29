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

import Name
import Resources
import engine.Equipment as Equipment
import engine.Effect as Effect
import logging
import gui.ScenarioGUI # FIXME PB: remove ScenarioGUI from this
import Constants
import random
from twisted.spread import pb

logger = logging.getLogger("batt")
#logger.setLevel(logging.DEBUG)

NEUTER = 0
FEMALE = 1
MALE = 2
FEMALE_OR_MALE = 3

def genderAsString(gender):
    # Purposely NOT translated, so that sprite loading works properly
    # (we use these names for determining which sprite files to try to
    # load first.)
    if gender == NEUTER:
        return "neuter"
    elif gender == FEMALE:
        return "female"
    return "male"

class Unit(pb.Copyable, pb.RemoteCopy):
    nextID = 0

    def update(self, newUnit):
        self.__dict__.update(newUnit.__dict__)

    def __init__(self, gender):
        self.unitID = Unit.nextID
        Unit.nextID += 1
        
        self._faction = 0

        self._level = 0
        self._class = None
        self._gender = gender
        self._name = Name.random(self._gender)
        self._abilities = {}
        self._classLevels = {}

        # Main stats        
        self._mhp = 0
        self._msp = 0
        self._watk = 0
        self._wdef = 0
        self._matk = 0
        self._mdef = 0
        self._speed = 0

        # Growth mods - set randomly when character is created
        self._mhpGrowthMod = 0
        self._mspGrowthMod = 0
        self._watkGrowthMod = 0
        self._wdefGrowthMod = 0
        self._matkGrowthMod = 0
        self._mdefGrowthMod = 0
        self._speedGrowthMod = 0      

        # Temp stats used for battles
        self._x = 0
        self._y = 0
        self._z = 0
        self._hp = 0
        self._sp = 0
        self._ct = 0
        self._hasMove = False
        self._hasCancel = False
        self._hasAct = False
        self._alive = False
        self._facing = Constants.N
        self._defenders = []
        self._defending = []
        
        # List of sprites
        self._spriteRoot = None # Set by Resources (FIXME)
        self._sprites = None
        self._overSprites = None

        self._weapon = Resources.equipment(Equipment.WEAPON, "hands")
        self._armor = None

        self._statusEffects = StatusEffects()

    def setMoveActCancel(self, move, act, cancel):
        self._hasMove = move
        self._hasAct = act
        self._hasCancel = cancel

    def setFacing(self, facing):
        self._facing = facing

    def facing(self):
        return self._facing

    def setSprites(self, sprites):
        self._sprites = sprites

    def _loadSprites(self):
        genderStr = genderAsString(self._gender)
        spriteRoot = self._spriteRoot
        
        # Get the sprite types we're looking for
        spriteTypes = ['standing', 'melee', 'bow', 'throw', 'hand', 'defend']
        
        sprites = {}
        oversprites = {}# part of the sprite that shows above the weapon

        # Search for sprites of each type
        for t in spriteTypes:
            foundGender = None
            spriteName = "%s-%s-%s-%d" % (spriteRoot, genderStr, t, 1)
            # FIXME: don't use _getFilename
            if Resources._getFilename("images", spriteName + ".png"):
                foundGender = genderStr
            else:
                spriteName = "%s-%s-%s-%d" % (spriteRoot, "unisex", t, 1)
                if Resources._getFilename("images", spriteName + ".png"):
                    foundGender = "unisex"
            
            # if we've found a sprite of this type, add it to the sprites
            if foundGender != None:
                sprites[t] = []
                oversprites[t] = []
                i = 1
                while Resources._getFilename("images", spriteName + ".png"):
                    sprites[t].append(spriteName)
                    if Resources._getFilename("images", spriteName + "-over.png"):
                        oversprites[t].append(spriteName + "-over")
                    i += 1
                    spriteName = "%s-%s-%s-%d" % (spriteRoot, foundGender, t, i)
        #Finally setting the sprites    
        self.setSprites(sprites)
        self.setOverSprites(oversprites)


    def getSprites(self, spriteName):
        if self._sprites == None:
            self._loadSprites()
        if self._sprites.has_key(spriteName):
            return self._sprites[spriteName]
        else:
            return []

    def setOverSprites(self, sprites):
        self._overSprites = sprites

    def getOverSprites(self, spriteName):
        if self._overSprites == None:
            self._loadSprites()
        if self._overSprites.has_key(spriteName):
            return self._overSprites[spriteName]
        else:
            return []

    def battleInit(self):
        self._alive = True
        self._hp = self.mhp()
        self._sp = self.msp()
        self._ct = 0
        self._hasAct = False
        self._hasMove = False
        self._hasCancel = False
        self._defenders = []
        self._defending = []
        self._statusEffects.clear()
        self._facing = random.choice([Constants.N,
                                      Constants.E,
                                      Constants.S,
                                      Constants.W])

    def setPosn(self, x, y, z):
        self._x = x
        self._y = y
        self._z = z

    def posn(self):
        return (self._x, self._y)

    def posn3d(self):
        return (self._x, self._y, self._z)

    def readyTurn(self):
        self._hasAct = True
        self._hasMove = True
        self._hasCancel = False
        
    def x(self):
        return self._x

    def y(self):
        return self._y
    
    def z(self):
        return self._z
    
    def hp(self):
        return self._hp 

    def sp(self):
        return self._sp

    def setSP(self, sp):
        self._sp = sp

    def equipment(self):
        return [self._weapon, self._armor]

    def mhp(self):
        result = int(self._mhp * self._class.mhpMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.mhp()
        return result

    def msp(self):
        result = int(self._msp * self._class.mspMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.msp()
        return result
    
    def watk(self):
        result = int(self._watk * self._class.watkMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.watk()

        increase = self._statusEffects.power(Effect.Status.PLUS_WATK)
        decrease = self._statusEffects.power(Effect.Status.MINUS_WATK)
        result *= self.statusEffectMult(increase, decrease)
        result = int(result)
        return result

    def wdef(self):
        result = int(self._wdef * self._class.wdefMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.wdef()
        
        increase = self._statusEffects.power(Effect.Status.PLUS_WDEF)
        decrease = self._statusEffects.power(Effect.Status.MINUS_WDEF)
        result *= self.statusEffectMult(increase, decrease)
        if self._statusEffects.has(Effect.Status.TRIPPED):
            result *= 0.5
        result = int(result)
        return result

    def matk(self):
        result = int(self._matk * self._class.matkMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.matk()
        
        increase = self._statusEffects.power(Effect.Status.PLUS_MATK)
        decrease = self._statusEffects.power(Effect.Status.MINUS_MATK)
        result *= self.statusEffectMult(increase, decrease)
        result = int(result)
        return result

    def mdef(self):
        result = int(self._mdef * self._class.mdefMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.mdef()
        
        increase = self._statusEffects.power(Effect.Status.PLUS_MDEF)
        decrease = self._statusEffects.power(Effect.Status.MINUS_MDEF)
        result *= self.statusEffectMult(increase, decrease)
        result = int(result)
        return result

    def speed(self):
        result = int(self._speed * self._class.speedMult)
        for eq in self.equipment():
            if eq != None:
                result += eq.speed()
                
        increase = self._statusEffects.power(Effect.Status.HASTE)
        decrease = self._statusEffects.power(Effect.Status.SLOW)
        result *= self.statusEffectMult(increase, decrease)
        result = int(result)
        return max(1, result)

    def move(self):
        result = self._class.move
        for eq in self.equipment():
            if eq != None:
                result += eq.move()
        result += self._statusEffects.power(Effect.Status.PLUS_MOVE)
        result -= self._statusEffects.power(Effect.Status.MINUS_MOVE)
        result = int(result)
        return result

    def jump(self):
        result = self._class.jump
        for eq in self.equipment():
            if eq != None:
                result += eq.jump()
        return result

    # Stuff below here might not be in constructor
    def name(self):
        return self._name

    def level(self):
        return self._level

    def className(self):
        return self._class.name

    def faction(self):
        return self._faction

    def setFaction(self, faction):
        self._faction = faction

    def setCT(self, ct):
        self._ct = ct

    def ct(self):
        return self._ct

    def addDefender(self, unit):
        if not unit in self._defenders:
            self._defenders.append(unit)
                
    def removeDefender(self, unit):
        self._defenders.remove(unit)
               
    def defenders(self):
        return self._defenders
                
    def defending(self, unit):
        self._defending.append(unit)
         
    def damageHP(self, amount, damageType):
        self._hp -= amount
        self._hp = min(self._hp, self.mhp())
        if self._hp <= 0:
            self._hp = 0
            self._alive = False

    def damageSP(self, amount):
        self._sp -= amount
        self._sp = min(self._sp, self._msp)
        self._sp = max(self._sp, 0)

    def slow(self,modifier,duration):
        self._slow.append([modifier,duration])
        
    def alive(self):
        return self._alive

    def active(self):
        return self._alive

    def getAI(self):
        return self._ai

    def __str__(self):
        return "%s (Lv. %d %s)" % (self._name, self._level, self._class.name)

    def __repr__(self):
        return self._name

    def addAbility(self, abilityName):
        if self._abilities.has_key(abilityName):
            return
        ability = Resources.ability(abilityName)
        self._abilities[abilityName] = ability

    def incrementClassLevel(self, className):
        if not self._classLevels.has_key(className):
            self._classLevels[className] = 0
        self._classLevels[className] += 1
        self._level += 1

    def classLevel(self, className):
        if not self._classLevels.has_key(className):
            self._classLevels[className] = 0       
        return self._classLevels[className]

    def abilities(self):
        return self._abilities.values()

    def allAbilities(self):
        result = self.abilities()
        result.append(self.attack())
        return result

    def attack(self):
        return self._weapon.attack()

    def equipWeapon(self, weapon):
        self._weapon = weapon

    def weapon(self):
        return self._weapon

    def equipArmor(self, armor):
        self._armor = armor

    def armor(self):
        return self._armor

    def evade(self): # FIXME: actually do this right
        if not self.canMove():
            return 0.0
        return 0.1

    def hasMove(self):
        return self._hasMove

    def hasAct(self):
        return self._hasAct

    def hasCancel(self):
        return self._hasCancel

    def canMove(self):
        return not (self._statusEffects.has(Effect.Status.PARALYZE_LEGS) or
                    self._statusEffects.has(Effect.Status.TRIPPED) or
                    self._statusEffects.has(Effect.Status.SLEEP) or
                    self._statusEffects.has(Effect.Status.FREEZE) or
                    self._statusEffects.has(Effect.Status.PARALYZE))

    def canAct(self):
        return not (self._statusEffects.has(Effect.Status.PARALYZE_ARMS) or
                    self._statusEffects.has(Effect.Status.SLEEP) or
                    self._statusEffects.has(Effect.Status.FREEZE) or
                    self._statusEffects.has(Effect.Status.PARALYZE))


    def addStatusEffect(self, effectType, duration, power):
        logger.debug(("Added status effect to %s " +
                      "(type=%d, duration=%d, power=%f)") %
                     (str(self), effectType, duration, power))
        self._statusEffects.add(effectType, duration, power)

    def statusEffects(self):
        return self._statusEffects

    def statusEffectMult(self, increase, decrease):
        statusEffectMult = 1.0
        if increase > 0.0:
            statusEffectMult = 1.0 + increase
        if decrease > 0.0:
            statusEffectMult *= 1.0 / (1.0 + decrease)
        return statusEffectMult

class StatusEffects(pb.Copyable, pb.RemoteCopy):
    def __init__(self):
        self._effects = [
            None for i in xrange(0, Effect.Status.NUM_TYPES)]
        self._colorStatus = []
        self._textureStatus = []
        
    def clear(self):
        self._effects = [
            None for i in xrange(0, Effect.Status.NUM_TYPES)]
        self._colorStatus = []
        self._textureStatus = []

    def has(self, effectType):
        return self._effects[effectType] != None

    def duration(self, effectType):
        if not self.has(effectType):
            return 0.0
        return self._effects[effectType][0]       

    def power(self, effectType):
        if not self.has(effectType):
            return 0.0
        return max(0.0, self._effects[effectType][1])

    def add(self, effectType, duration, power):
        self._effects[effectType] = (duration, power)
        if Effect.Status.isColor(effectType):
            self._colorStatus.append(effectType)
        else:
            self._textureStatus.append(effectType)

    def update(self):
        # Decrement status-effect counters
        for i in xrange(0, len(self._effects)):
            e = self._effects[i]
            if e == None:
                continue
            (duration, power) = e
            duration -= 1
            if duration == 0:
                logger.debug(("Removed status effect (type=%d)") % i)
                newE = None
                if Effect.Status.isColor(i):
                    self._colorStatus.remove(i)
                else:
                    self._textureStatus.remove(i)
            else:
                newE = (duration, power)
            self._effects[i] = newE

    def color(self):
        return self._colorStatus

    def texture(self):
        return self._textureStatus

