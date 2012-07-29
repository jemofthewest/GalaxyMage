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

import time
import random
import copy
import logging
import traceback
import engine.Battle as Battle
import engine.Faction as Faction
import engine.Ability as Ability
import engine.Effect as Effect
import Constants

logger = logging.getLogger('ai')
#logger.setLevel(logging.DEBUG)


class Base(object):
    """Base is the base class of all unit AIs. By default, it
    returns a no-op action. Override the calc() method to change its
    behavior."""
    def __init__(self, unit):
        self._unit = unit
        self._result = None

    def result(self):
        return self._result
        
    def __call__(self):
        startTime = time.time()
        name = self.__class__.__name__ + ' unit AI'
        logger.debug(name + " started for " + str(self._unit))
        try:
            b = Battle.get()
            self._result = self.calc(b)
            logger.debug("Result: " + str(self._result))
        except Exception, e:
            self._result = Battle.UnitTurn()
            logger.error(traceback.format_exc())
        if self._result.moveTarget() == self._unit.posn():
            self._result.setMoveTarget(None)
        timeElapsed = time.time() - startTime
        logger.debug("%s finished (%.2fs elasped)" % (name, timeElapsed))

    def calc(self, battle, unit):
        """@return an instance of Battle.UnitTurn."""
        return Battle.UnitTurn()
            

class TurnEvaluator(object):
    def __call__(self, unit, map_, turns):
        if len(turns) == 0:
            return Battle.UnitTurn()
        else:
            return turns[0]

class HealWeakest(TurnEvaluator):
    def __call__(self, battle, unit, turns):
        map_ = battle.map()
        unitCopy = copy.copy(unit)

        # Get a list of targets, sorted by lowest HP.
        targets = []
        for t in battle.units():
            if (t.alive() and 
                Faction.friendly(unit.faction(), t.faction()) and
                t.hp() < t.mhp()):
                targets.append(t)
        targets.sort(lambda x,y: cmp(x.hp(), y.hp()))
        
        # Get all turns that heal the weakest possible target
        
        # FIXME: could optimize by keeping a map from units -> attacks
        # that hit that unit
        bestTurns = []
        for target in targets:
            for turn in turns:
                action = turn.action()
                if action == None:
                    continue
                # FIXME: more general way of filtering abilities
                # FIXME: we don't consider FRIENDLY_AND_HOSTILE yet
                if action.targetType() != Ability.FRIENDLY:
                    continue   
                heals = False
                for e in action.effects():    
                    if issubclass(e.__class__, Effect.Healing):
                        heals = True
                        break
                if not heals:
                    continue

                # FIXME: modifying map == ugly
                # Temporarily modify the map for our new
                # position... have to make sure to roll this back!
                if turn.moveTarget() != None:
                    (mtx, mty) = turn.moveTarget()
                else:
                    (mtx, mty) = unit.posn()
                map_.squares[unit.x()][unit.y()].unit = None
                map_.squares[mtx][mty].unit = unit
                unitCopy.setPosn(mtx, mty, map_.squares[mtx][mty].z)
                
                # Find out who's affected
                affected = action.affectedUnits(map_,
                                                unitCopy,
                                                turn.actionTarget())
               
                # Roll back the map modification
                map_.squares[mtx][mty].unit = None
                map_.squares[unit.x()][unit.y()].unit = unit               
                
                if target in affected:
                    bestTurns.append(turn)
            if bestTurns:
                return bestTurns
        return bestTurns


class DamageWeakest(TurnEvaluator):
    def __call__(self, battle, unit, turns):
        map_ = battle.map()

        # Get a list of targets, sorted by lowest HP.
        targets = []
        for t in battle.units():
            if t.alive() and Faction.hostile(unit.faction(), t.faction()):
                targets.append(t)
        targets.sort(lambda x,y: cmp(x.hp(), y.hp()))
        
        # Get all turns that hit the weakest possible target
        
        # FIXME: could optimize by keeping a map from units -> attacks
        # that hit that unit
        bestTurns = []
        for target in targets:
            for turn in turns:
                action = turn.action()
                if action == None:
                    continue
                # FIXME: more general way of filtering abilities
                # FIXME: we don't consider FRIENDLY_AND_HOSTILE yet
                if action.targetType() != Ability.HOSTILE:
                    continue
                doesDamage = False
                for e in action.effects():    
                    if (issubclass(e.__class__, Effect.Damage) or
                        issubclass(e.__class__, Effect.DrainLife) or
                        issubclass(e.__class__,
                                   Effect.HealFriendlyDamageHostile)):
                        doesDamage = True
                        break
                if not doesDamage:
                    continue
                
                affected = action.affectedUnits(map_,
                                                unit,
                                                turn.actionTarget())
                if target in affected:
                    bestTurns.append(turn)
            if bestTurns:
                # We have some candidate turns, now evaluate them to
                # see which does the most total damage
                maxDamage = 0.1
                newBestTurns = []
                unitCopy = copy.copy(unit)
                for turn in bestTurns:
                    if turn.moveTarget() != None:
                        (mtx, mty) = turn.moveTarget()
                    else:
                        (mtx, mty) = unitCopy.posn()
                    unitCopy.setPosn(mtx, mty, map_.squares[mtx][mty].z)
                    action = turn.action()
                    damage = 0
                    affected = action.affectedUnits(map_,
                                                    unitCopy,
                                                    turn.actionTarget())
                    for target in affected:
                        for e in action.effects():
                            if issubclass(e.__class__, Effect.Damage):
                                (att, df) = e.calcAttackAndDefense(unitCopy,
                                                                   target)
                                dmg = e.estimateDamage(att, df)
                                damage += dmg
                    if damage > maxDamage:
                        maxDamage = damage
                        newBestTurns = [turn]
                    elif damage == maxDamage:
                        newBestTurns.append(turn)
                if newBestTurns:
                    # Filter again - prefer turns with the lowest SP cost
                    newNewBestTurns = []
                    lowestCost = 1000000
                    for turn in newBestTurns:
                        if turn.action().cost() < lowestCost:
                            lowestCost = turn.action().cost()
                            newNewBestTurns = [turn]
                        elif turn.action().cost() == lowestCost:
                            newNewBestTurns.append(turn)
                    # Filter again - prefer a turn with no move
                    for turn in newNewBestTurns:
                        if turn.moveTarget() == None:
                            return [turn]
                    return newNewBestTurns
        return bestTurns

class MoveToWeakest(TurnEvaluator):
    def __call__(self, battle, unit, turns):
        map_ = battle.map()

        # Get a list of targets, sorted by lowest HP.
        targets = []
        for t in battle.units():
            if t.alive() and Faction.hostile(unit.faction(), t.faction()):
                targets.append(t)
        targets.sort(lambda x,y: cmp(x.hp(), y.hp()))

        # Get as close as possible to the weakest target
        map_.fillDistances(unit, targets[0].posn())
        bestDistance = 1000000
        bestTurns = []
        for turn in turns:
            move = turn.moveTarget()
            action = turn.action()
            if move == None or action != None:
                continue
            search = map_.squares[move[0]][move[1]].search
            if search == None:
                continue
            distance = search[0]
            if distance < bestDistance:
                bestDistance = distance
                bestTurns = [turn]
            elif distance == bestDistance:
                bestTurns.append(turn)
        return bestTurns

class Exhaustive(Base):
    def __init__(self, unit):
        Base.__init__(self, unit)
        self._turnEvaluators = [HealWeakest(), DamageWeakest(),
                                MoveToWeakest()]
    
    def allAbilities(self):
        abilities = []
        for a in self._unit.allAbilities():
            if a.cost() > self._unit.sp():
                continue
            abilities.append(a)
        return abilities

    def generateAllTurns(self, battle, moveTargets, abilities):
        startTime = time.time()
        u = copy.copy(self._unit)
        map_ = battle.map()
        result = []
        turnsConsidered = 0

        # This calculates all move-then-attack turns.
        if u.hasMove() and u.hasAct():
            logger.debug('Considering move-attack turns')
            for mt in moveTargets:
                (mtx, mty) = mt
                u.setPosn(mtx, mty, map_.squares[mtx][mty].z)

                # FIXME: modifying map == ugly
                # Temporarily modify the map for our new
                # position... have to make sure to roll this back!
                map_.squares[self._unit.x()][self._unit.y()].unit = None
                map_.squares[mtx][mty].unit = self._unit
                
                for ability in abilities:
                    for abilityTarget in ability.range(map_, u):
                        turnsConsidered += 1
                        if ability.hasEffect(map_, u, abilityTarget):
                            result.append(Battle.UnitTurn
                                          (Battle.UnitTurn.MOVE_FIRST,
                                           mt, ability, abilityTarget))

                # Roll back the map modification.
                map_.squares[mtx][mty].unit = None
                map_.squares[self._unit.x()][self._unit.y()].unit = self._unit
                            
        # This calculates all just-move turns.
        # FIXME: we need to calculate all attack-then-move turns.
        if u.hasMove():
            logger.debug('Considering move-only turns')
            for mt in moveTargets:
                result.append(Battle.UnitTurn(Battle.UnitTurn.MOVE_FIRST,
                                              mt))
                turnsConsidered += 1

        if turnsConsidered == 0:
            logger.debug('No turns considered')
        else:
            logger.debug(('%d/%d turns are useful ' +
                         '(%.2fs elapsed, %.4f each)') %
                         (len(result), turnsConsidered,
                          time.time() - startTime,
                          (1.0 * len(result) / turnsConsidered *
                           (time.time() - startTime))))
        return result

    def calc(self, battle):
        turn = self.getTurn(battle)
        facing = self.getFacing(battle, turn.moveTarget())
        return Battle.UnitTurn(turn.turnOrder(),
                               turn.moveTarget(),
                               turn.action(),
                               turn.actionTarget(),
                               facing)

    def getFacing(self, battle, moveTarget):
        u = self._unit
        if moveTarget == None:
            moveTarget = (u.x(), u.y())
        
        # Calculate the centroid of enemy units
        targets = []
        for t in battle.units():
            if t.alive() and Faction.hostile(u.faction(), t.faction()):
                targets.append(t)
        centroidX = 0.0
        centroidY = 0.0
        for t in targets:
            centroidX += t.x()
            centroidY += t.y()
        centroidX /= len(targets)
        centroidY /= len(targets)

        # Face toward the centroid
        dx = centroidX - moveTarget[0]
        dy = centroidY - moveTarget[1]
        total = abs(dx)+abs(dy)
        if total == 0.0:
            return None
        rnd = random.uniform(0.0, total)
        if rnd < dx:
            # Face based on X-coord
            if dx > 0:
                return Constants.E
            else:
                return Constants.W
        else:
            if dy > 0:
                return Constants.S
            else:
                return Constants.N

    def getTurn(self, battle):
        abilities = self.allAbilities()
        logger.debug('Abilities: ' + str(abilities))

        moveTargets = battle.map().reachable(self._unit)
        moveTargets.append(self._unit.posn())
        logger.debug('Move targets: ' + str(len(moveTargets)))

        allTurns = self.generateAllTurns(battle, moveTargets, abilities)
        for evaluator in self._turnEvaluators:
            startTime = time.time()
            logger.debug('Trying evaluator %s' % evaluator.__class__.__name__)
            result = evaluator(battle, self._unit, allTurns)
            logger.debug('Evaluator finished ' +
                         '(%d actions returned, %.2fs elapsed)' %
                         (len(result), (time.time() - startTime)))
            if result:
                return random.choice(result)
        return Battle.UnitTurn()




