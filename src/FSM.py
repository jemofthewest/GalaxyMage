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

import pprint
import time

class FSM(object):
    def __init__(self, states):
        """states[0] is the initial state."""
        self.states = states
        self.state = states[0]
        self.entryHooks = {}
        self.exitHooks = {}

    def addEntryHook(self, state, hook):
        """hook(oldState, reason) will be called whenever we
        transition to state."""
        l = self.entryHooks.setdefault(state, [])
        l.append(hook)

    def addExitHook(self, state, hook):
        """hook(newState, reason) will be called whenever we
        transition from state."""
        l = self.exitHooks.setdefault(state, [])
        l.append(hook)

    def trans(self, newState, reason=None):
        """Transitions to the given state, calling hooks as
        appropriate."""
        oldState = self.state
        for hook in self.exitHooks.get(oldState, []):
            hook(newState, reason)
        self.state = newState
        for hook in self.entryHooks.get(newState, []):
            hook(oldState, reason)
