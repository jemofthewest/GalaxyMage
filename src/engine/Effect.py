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

import Resources
import gui.Sprite
import gui.ScenarioGUI
import random
import math
import engine.Faction as Faction
import gui.GLUtil
import Constants
from twisted.spread import pb

# DAMAGE TYPES:
# Generic physical/magical damage types
PHYSICAL = 0
MAGICAL = 1
HEALING = 2

# Specific physical damage types
BLUDGEONING = 3
PIERCING = 4
SLASHING = 5


# Specific magical damage types
FIRE = 8
ICE = 9
HOLY = 10


def isPhysicalDamage(damageType):
    return (damageType == PHYSICAL or
            damageType == BLUDGEONING or
            damageType == PIERCING or
            damageType == SLASHING)


class Effect(pb.Copyable, pb.RemoteCopy):
    def affect(self, source, target):
        pass

    def attackIsFromRear(self, source, target):
        (tx, ty) = target.posn()
        (sx, sy) = source.posn()
        dx = tx - sx
        dy = ty - sy
        if target.facing() == Constants.N:
            return -dy - abs(dx) > 0
        elif target.facing() == Constants.S:
            return dy - abs(dx) > 0
        elif target.facing() == Constants.W:
            return -dx - abs(dy) > 0
        elif target.facing() == Constants.E:
            return dx - abs(dy) > 0
        else:
            raise Exception("target.facing() is not legal")

    def attackIsFromFront(self, source, target):
        (tx, ty) = target.posn()
        (sx, sy) = source.posn()
        dx = tx - sx
        dy = ty - sy
        if target.facing() == Constants.N:
            return dy - abs(dx) >= 0
        elif target.facing() == Constants.S:
            return -dy - abs(dx) >= 0
        elif target.facing() == Constants.W:
            return dx - abs(dy) >= 0
        elif target.facing() == Constants.E:
            return -dx - abs(dy) >= 0
        else:
            raise Exception("target.facing() is not legal")


    def attackIsFromSide(self, source, target):
        return False

    def calcAttackAndDefense(self, source, target):
        if target.statusEffects().has(Status.INVULNERABLE):
            return (0, -1)
        if isPhysicalDamage(self._damageType):
            attack = source.watk()
            defense = target.wdef()
            if self.attackIsFromRear(source, target):
                defense *= 0.5
            elif not self.attackIsFromFront(source, target):
                # then it's from the side
                defense *= 0.75
            heightMult = 0.02 * (source.z() - target.z())
            heightMult = max(-0.25, heightMult)
            heightMult = min(0.25, heightMult)
            attack *= 1.0 + heightMult
        else:
            attack = source.matk()
            defense = target.mdef()
        attack = max(1.0, attack)
        defense = max(1.0, defense)
        return (attack, defense)

    def estimateDamage(self, attack, defense):
        if attack <= 0:
            return 0
        baseDamage = attack - defense * 0.5
        damage = baseDamage * self._power
        return damage

    def calcDamage(self, attack, defense, maxDamage):
        if attack <= 0:
            return 0
        baseDamage = attack - defense * 0.5
        damage = baseDamage * self._power
        damage *= random.uniform(0.8, 1.2)
        damage = min(damage, maxDamage)
        damage = int(max(0, damage))
        return damage

    # FIXME BE: Defend ability needs to be fixed
    def getDefenders(self, target):
        (x,y) = target.posn()#FIXME: do this in Range.py
        adjacent = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        if isPhysicalDamage(self._damageType):
            for u in target.defenders():
                if u.posn() in adjacent and random.random() > 0.3:
                    ud = gui.ScenarioGUI.get().unitDisplayer(target)
                    ud.addAnimation(gui.Sprite.DamageDisplayer("Defended", gui.Sprite.NEUTRAL))
                    return u
        return target

class EffectResult(pb.Copyable, pb.RemoteCopy):
    def __init__(self, target, hit):
        self.target = target
        self.hit = hit

class MissResult(EffectResult):
    def __init__(self, target):
        EffectResult.__init__(self, target, False)

class DamageResult(EffectResult):
    def __init__(self, target, damage):
        EffectResult.__init__(self, target, True)
        self.damage = damage

class DamageSPResult(EffectResult):
    def __init__(self, target, damage):
        EffectResult.__init__(self, target, True)
        self.damage = damage

class HealResult(EffectResult):
    def __init__(self, target, damage):
        EffectResult.__init__(self, target, True)
        self.damage = damage

class StatusResult(EffectResult):
    def __init__(self, target, effect, duration, power):
        EffectResult.__init__(self, target, True)
        self.type = effect
        self.duration = duration
        self.power = power
    
class Damage(Effect):
    def __init__(self, power=1.0, hit=1.0, damageType=PHYSICAL):
        self._power = power
        self._hit = hit
        self._damageType = damageType
        
    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]
        
        target = self.getDefenders(target)
        (attack, defense) = self.calcAttackAndDefense(source, target)
        
        # Check if the target evades the attack
        if random.random() < target.evade():
            return [MissResult(target)]
        
        # Damage target and display results
        damage = self.calcDamage(attack, defense, target.hp())
        target.damageHP(damage, self._damageType)
        return [DamageResult(target, damage)]

class DamageSP(Effect):
    def __init__(self, power=1.0, hit=1.0, damageType=PHYSICAL):
        self._power = power
        self._hit = hit
        self._damageType = damageType
        
    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]

        target = self.getDefenders(target)
        (attack, defense) = self.calcAttackAndDefense(source, target)
        
        # Check if the target evades the attack
        if random.random() < target.evade():
            return [MissResult(target)]
        
        # Damage target and display results
        damage = self.calcDamage(attack, defense, target.sp())
        target.damageSP(damage)
        return [DamageSPResult(damage)]
   
class DrainLife(Effect):
    def __init__(self, power=1.0, hit=1.0, percentDamageHealed=1.0,
                 damageType=PHYSICAL):
        self._power = power
        self._hit = hit
        self._damageType = damageType
        self._percentDamageHealed = percentDamageHealed
        
    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]

        target = self.getDefenders(target)
        (attack, defense) = self.calcAttackAndDefense(source, target)

        # Check if the target evades the attack
        if random.random() < target.evade():
            return [MissResult(target)]
        
        # Damage target and display results
        results = []
        damage = self.calcDamage(attack, defense, target.hp())
        target.damageHP(damage,self._damageType)
        results.append(DamageResult(target, damage))
        
        # Heal source and display results
        gain = int(damage * self._percentDamageHealed)
        gain = min(gain, source.mhp() - source.hp())
        source.damageHP(-gain, HEALING)
        results.append(HealResult(source, gain))
        return results

class HealFriendlyDamageHostile(Effect):
    def __init__(self, power=1.0, hit=1.0, damageType=MAGICAL):
        self._power = power
        self._hit = hit
        self._damageType = damageType
        
    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]

        if Faction.friendly(source.faction(), target.faction()):
            (attack, defense) = self.calcAttackAndDefense(source, target)
            
            # Heal target and display results
            healing = self.calcDamage(attack, attack,
                                      target.mhp() - target.hp())
            target.damageHP(-healing, HEALING)
            return [HealResult(target, healing)]
        elif Faction.hostile(source.faction(), target.faction()):
            target = self.getDefenders(target)
            (attack, defense) = self.calcAttackAndDefense(source, target)

            # Check if the target evades the attack
            if random.random() < target.evade():
                return [MissResult(target)]

            # Damage target and display results
            damage = self.calcDamage(attack, defense, target.hp())
            target.damageHP(damage, self._damageType)
            return [DamageResult(target, damage)]

class Healing(Effect):
    def __init__(self, power=1.0, hit=1.0,
                 damageType=MAGICAL):
        self._power = power
        self._hit = hit
        self._damageType = damageType

    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]

        (attack, defense) = self.calcAttackAndDefense(source, target)

        # Heal target and display results
        healing = self.calcDamage(attack, attack, target.mhp() - target.hp())
        target.damageHP(-healing, HEALING)
        return [HealResult(target, healing)]

# FIXME BE: removed Defend ability for now... need a DefendEffect
class Defend(Effect):
    def __init__(self, power=1.0, hit=1.0,
                 damageType=MAGICAL):
        self._power = power
        self._hit = hit
        self._damageType = damageType

    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]
        target.addDefender(source)
        source.defending(target)
        return True
    
class Status(Effect):
    # Types of status effects
    SLEEP = 0   
    FREEZE = 1
    PARALYZE = 2
    PARALYZE_LEGS = 3
    PARALYZE_ARMS = 4
    HASTE = 5
    SLOW = 6   
    PLUS_MOVE = 7
    MINUS_MOVE = 8
    PLUS_WATK = 9
    PLUS_WDEF = 10
    PLUS_MATK = 11
    PLUS_MDEF = 12
    MINUS_WATK = 13
    MINUS_WDEF = 14
    MINUS_MATK = 15
    MINUS_MDEF = 16
    INVULNERABLE = 17
    REGEN = 18
    POISON = 19
    TRIPPED = 20
    NUM_TYPES = 21

    # Names of status effects
    effectNames = [("Sleep"),
                   ("Freeze"),
                   ("Paralyze"),
                   ("Paralyze Legs"),
                   ("Paralyze Arms"),
                   ("Haste"),
                   ("Slow"),
                   ("+ Move"),
                   ("- Move"),
                   ("+ Weapon Atk"),
                   ("+ Weapon Def"),
                   ("+ Magic Atk"),
                   ("+ Magic Def"),
                   ("- Weapon Atk"),
                   ("- Weapon Def"),
                   ("- Magic Atk"),
                   ("- Magic Def"),
                   ("Invulnerable"),
                   ("Regen"),
                   ("Poison"),
                   ("Tripped")]

    effectTextures = [None for i in xrange(0, NUM_TYPES)]
    effectTextures[FREEZE] = (0.0,0.6,0.9,1.0)
    effectTextures[POISON] = (0.2,0.8,0.1,1.0)

    def beneficial(effectType):
        return (effectType == Status.HASTE or
                effectType == Status.PLUS_MOVE or
                effectType == Status.PLUS_WATK or
                effectType == Status.PLUS_WDEF or
                effectType == Status.PLUS_MATK or
                effectType == Status.PLUS_MDEF or
                effectType == Status.INVULNERABLE or
                effectType == Status.REGEN)
    beneficial = staticmethod(beneficial)

    def isColor(effectType):
        return (effectType == Status.FREEZE or
                effectType == Status.POISON)
    isColor = staticmethod(isColor)

    def __init__(self, effectType, power=1.0, hit=1.0, duration=1,
                 damageType=MAGICAL):
        self._effectType = effectType
        self._power = power
        self._hit = hit
        self._damageType = damageType
        self._duration = duration

        # FIXME BE: commented this out -- need to be initialized
        # elsewhere, as the GameServer can't load textures
        #Status.effectTextures[Status.SLEEP] = Resources.texture('effect-sleep')
        #Status.effectTextures[Status.INVULNERABLE] = \
        #    Resources.texture('effect-invulnerable')

    def affect(self, source, target):
        if not target.alive():
            return [MissResult(target)]

        (attack, defense) = self.calcAttackAndDefense(source, target)

        if not Status.beneficial(self._effectType):
            # Hit probability is unchanged if attack = defense
            # Hit probability is 2x is attack = 2 * defense
            # Hit probability is 0.5x if attack = 0.5 * defense
            # ... and so on
            hitProb = 1.0 * self._hit * attack / defense
            hitProb = max(0.05, hitProb)
            hitProb = min(0.95, hitProb)
            if random.random() > hitProb: # the attack missed
                return [MissResult(target)]

        # FIXME: add some variance to duration?
        power = self._power * random.uniform(0.8, 1.2)
        target.addStatusEffect(self._effectType, self._duration, power)
        return [StatusResult(target, self._effectType, self._duration, power)]

