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

import FSM
import unittest

class FSMTest(unittest.TestCase):

    def testNormalLoop(self):
        # Example of what a standard FSM loop might look like:
        fsm = FSM.FSM('state1', ['state1', 'state2', 'state3'])        
        try:
            fsm.startLoop()
            while fsm.running:
                if fsm.state == 'state1':
                    fsm.trans('state2')
                    continue
                elif fsm.state == 'state2':
                    fsm.trans('state3')
                    continue
                elif fsm.state == 'state3':
                    fsm.endLoop()
        except FSM.FSMError, error:
            print 'FSM Error:', str(error)
            fsm.endLoop()
        
        # This is unit-testing code and wouldn't appear here for a
        # normal FSM loop.
        self.failIf(fsm.running)

    def testLoopDetection(self):
        fsm = FSM.FSM('state1', ['state1', 'state2'])
        fsm.startLoop()
        fsm.trans('state2')
        fsm.trans('state1')
        self.assertRaises(FSM.FSMError, fsm.trans, 'state2')

