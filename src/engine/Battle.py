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
import Faction
import Sound
import threading
import logging
import FSM
import engine.Effect
import Constants
from twisted.spread import pb

logger = logging.getLogger('batt')

def get():
    return _battle

_battle = None

class Battle(pb.Copyable, pb.RemoteCopy):
    def __init__(self, endingConditions, units, map):
        global _battle
        _battle = self
        self._units = units
        self._steps = 0
        self._turns = 0
        self.unitQueue = []
        for u in self._units:
            u.battleInit()
        self.activeUnit = None
        self._oldUnitPosn = (0, 0)
        self.endingConditions = endingConditions
        self._map = map

    def units(self):
        return self._units
        
    def map(self):
        return self._map

    def _step(self):
        self._steps += 1
        self._statusCheck()
        self._slowActionCharging()
        self._slowActionResolution()
        self._ctCharging()
        return self._activeTimeResolution()

    # Check time-dependent status effect
    def _statusCheck(self):
        pass

    # Slow-action charging
    def _slowActionCharging(self):
        pass

    # Slow-action resolution
    def _slowActionResolution(self):
        pass

    # CT charging
    def _ctCharging(self):
        for u in self._units:
            if u.alive():
                u.setCT(u.ct() + u.speed())
            else:
                u.setCT(0)

    # AT resolution
    def _activeTimeResolution(self):
        ready = [u for u in self._units if u.ct() >= 1000]
        return ready

    def unitMoved(self, x, y):
        u = self.activeUnit
        if not u.hasMove():
            return False
        r = self._map.reachable(u)
        if not (x, y) in r:
            return False
        u._hasMove = False
        u._hasCancel = True
        (oldx, oldy) = self.activeUnit.posn()
        self._oldUnitPosn = (oldx, oldy)
        self._map.squares[oldx][oldy].unit = None
        sq = self._map.squares[x][y]
        sq.unit = u
        u.setPosn(sq.x, sq.y, sq.z)
        u.setCT(u.ct() - 300)
        return True

    def unitCanceled(self):
        u = self.activeUnit
        if not u.hasCancel():
            return

        # Actually move the unit
        (newx, newy) = self._oldUnitPosn
        (oldx, oldy) = self.activeUnit.posn()
        self._map.squares[oldx][oldy].unit = None
        sq = self._map.squares[newx][newy]
        sq.unit = u
        u.setPosn(sq.x, sq.y, sq.z)

        # Adjust CT
        u.canceled()
        u.setCT(u.ct() + 300)

    def unitActed(self, action, x, y):
        posn = (x, y)
        u = self.activeUnit
        if not u.hasAct():
            return False
        if u.sp() < action.cost():
            return False
        if posn not in action.range(self._map, self.activeUnit):
            return False
        targets = action.affectedUnits(self._map, u, posn)
        if not targets:
            return False        

        u._hasAct = False
        u._hasCancel = False

        affectedUnits = list(targets)
        affectedUnits.append(u)
        # Maps target ID to a list of all effect results for that target
        allEffectResults = {} 
        for target in targets:
            for e in action.effects():
                effectResults = e.affect(u, target)
                for e in effectResults:
                    targetID = e.target.unitID
                    allEffectResults.setdefault(targetID, [])
                    allEffectResults[targetID].append(e)
                miss = False
                for r in effectResults:
                    if not r.hit:
                        miss = True
                if not target.alive():
                    x, y = target.posn()
                    self._map.squares[x][y].unit = None
                if miss:
                    break
        u.setSP(u.sp() - action.cost())

        # Adjust CT
        u.setCT(u.ct() - 200)
        return affectedUnits, allEffectResults

    def unitSetFacing(self, facing):
        if facing != None:
            if not (Constants.N <= facing <= Constants.NW):
                return False
            u = self.activeUnit
            u.setFacing(facing)
        return True

    def unitDone(self):
        u = self.activeUnit
        if u == None:
            return False
        self.activeUnit = None
        u.setCT(u.ct() - 500)
        u.setCT(min(u.ct(), 500))
        return True

    def status(self):
        endingCondition = LastTeamStanding()
        result = endingCondition(self)
        return result
#         for i in xrange(0, len(self.endingConditions)):
#             c = self.endingConditions[i]
#             if c(self):
#                 return i
#         return -1

    def pickNextUnit(self):
        #logger.debug2('picking a unit')
        active = [u for u in self._units if u.active()]
        self._turns += 1
        self.unitQueue = [u for u in self.unitQueue if u.active()]
        while not self.unitQueue:
            self.unitQueue = self._step()
        u = self.unitQueue.pop(0)
        self.activeUnit = u
        u.readyTurn()
        u.statusEffects().update()
        return u
        # FIXME BE: add defenders and regen/poison back in
#         for u in self._defending:
#             u.removeDefender(self)
#             self._defending.remove(u)
        # See if any status effects have affects at beginning of turn
#         if self._statusEffects.has(Effect.Status.REGEN):
#             damage = self._statusEffects.power(Effect.Status.REGEN)
#             damage *= self.mhp()
#             damage = int(damage)
#             damage = min(self.mhp() - self.hp(), damage)
#             self.damageHP(-damage, Effect.HEALING)
#             ud = gui.ScenarioGUI.get().unitDisplayer(self)        
#             ud.addAnimation(gui.Sprite.DamageDisplayer(damage, gui.Sprite.BENEFICIAL, 0.5))
#         if self._statusEffects.has(Effect.Status.POISON):
#             damage = self._statusEffects.power(Effect.Status.POISON)
#             damage *= self.mhp()
#             damage = int(damage)
#             damage = min(self.hp(), damage)
#             self.damageHP(damage, Effect.PHYSICAL)
#             ud = gui.ScenarioGUI.get().unitDisplayer(self)        
#             ud.addAnimation(gui.Sprite.DamageDisplayer(damage, gui.Sprite.NEGATIVE, 0.5))
            

class UnitTurn(object):

    MOVE_FIRST = 0
    ACT_FIRST = 1
    
    def __init__(self,
                 turnOrder=MOVE_FIRST,
                 moveTarget=None,
                 action=None,
                 actionTarget=None,
                 facing=None):
        self._turnOrder = turnOrder
        self._moveTarget = moveTarget
        self._action = action
        self._actionTarget = actionTarget
        self._facing = facing

    def turnOrder(self):
        return self._turnOrder

    def moveTarget(self):
        return self._moveTarget

    def setMoveTarget(self, moveTarget):
        self._moveTarget = moveTarget

    def action(self):
        return self._action

    def actionTarget(self):
        return self._actionTarget

    def facing(self):
        return self._facing

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self._action == None:
            return "Move: %s" % str(self._moveTarget)
        else:
            if self._turnOrder == UnitTurn.MOVE_FIRST:
                return "Move: %s, %s: %s" % (self._moveTarget,
                                             self._action.name(),
                                             self._actionTarget)
            else:
                return "%s: %s, Move: %s" % (self._action.name(),
                                             self._actionTarget,
                                             self._moveTarget)

class EndingCondition(pb.Copyable, pb.RemoteCopy):
    def __call__(self, battle):
        """@return: True iff the ending condition is met."""
        return False

    def description():
        return ""

class DefeatAllEnemies(EndingCondition):
    def __call__(self, battle):
        """@return: True iff all enemy units have been rendered
        inactive."""
        active = [u for u in battle.units() if u.active()]
        for u in active:
            if Faction.hostile(Faction.PLAYER_FACTION, u.faction()):
                return False
        return True

    def description():
        return "Defeat all enemies!"

class PlayerDefeated(EndingCondition):
    def __call__(self, battle):
        """@return: True iff all the player's units have been rendered
        inactive."""
        active = [u for u in battle.units() if u.active()]
        for u in active:
            if Faction.playerControlled(u.faction()):
                return False
        return True


class LastTeamStanding(EndingCondition):
    def __call__(self, battle):
        teamRemaining = None
        active = [u for u in battle.units() if u.active()]
        for u in active:
            if teamRemaining == None:
                teamRemaining = u.faction()
            elif teamRemaining != u.faction():
                return -1
        return teamRemaining
        
PLAYER_DEFEATED = PlayerDefeated()
DEFEAT_ALL_ENEMIES = DefeatAllEnemies()
LAST_TEAM_STANDING = LastTeamStanding()
NEVER_ENDING = EndingCondition()
