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

import unittest
import safepickle

class IntPair(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def pack(self):
        return [self.x, self.y]
    
    def unpack(x, y):
        return IntPair(x, y)
    unpack = staticmethod(unpack)


class TestPickle(unittest.TestCase):
    
    def setUp(self):
        self.p = safepickle.SafePickler()
        self.p.addPicklableClass("TwoInts",
                                 IntPair,
                                 IntPair.pack,
                                 IntPair.unpack)
        self.data1 = [1, 2, (3, 4), "five", [6, 7, {8: 9}, 10, "eleven"], True]
    
    def testdumpnone(self):
        self.assertEqual(self.p.dumps(None), 'N')
    
    def testloadnone(self):
        self.assertEqual(self.p.loads('N'), None)
    
    def testdumpstring(self):
        self.assertEqual(self.p.dumps("foo"), 'S foo /S')
    
    def testloadstring(self):
        self.assertEqual(self.p.loads('S foo /S'), 'foo')
    
    def testdumpescapedstring(self):
        self.assertEqual(self.p.dumps("foo /S"), 'S foo //S /S')
    
    def testloadescapedstring(self):
        self.assertEqual(self.p.loads('S foo //S /S'), "foo /S")
    
    def testdumpemptylist(self):
        self.assertEqual(self.p.dumps([]), 'L /L')
    
    def testloademptylist(self):
        self.assertEqual(self.p.loads('L /L'), [])
    
    def testdumplist(self):
        self.assertEqual(self.p.dumps([1, 2, 3]), 'L I 1 I 2 I 3 /L')
    
    def testloadlist(self):
        self.assertEqual(self.p.loads('L I 1 I 2 I 3 /L'), [1, 2, 3])
    
    def testdumpemptytuple(self):
        self.assertEqual(self.p.dumps(()), 'T /T')
    
    def testloademptytuple(self):
        self.assertEqual(self.p.loads('T /T'), ())
    
    def testdumptuple(self):
        self.assertEqual(self.p.dumps((3, 4, 5)), 'T I 3 I 4 I 5 /T')
    
    def testloadtuple(self):
        self.assertEqual(self.p.loads('T I 3 I 4 I 5 /T'), (3, 4, 5))
    
    def testdumptrue(self):
        self.assertEqual(self.p.dumps(True), 'B +')
    
    def testloadtrue(self):
        self.assertEqual(self.p.loads('B +'), True)
    
    def testdumpfalse(self):
        self.assertEqual(self.p.dumps(False), 'B -')
    
    def testloadfalse(self):
        self.assertEqual(self.p.loads('B -'), False)
    
    def testdumpint(self):
        self.assertEqual(self.p.dumps(-42), 'I -42')
    
    def testloadint(self):
        self.assertEqual(self.p.loads("I -42"), -42)
    
    def testdumpfloat(self):
        self.assert_(self.p.dumps(43.5).startswith('F 43.5'))
    
    def testloadfloat(self):
        self.assertAlmostEqual(self.p.loads("F 43.5"), 43.5, 1)
    
    def testdumpobj(self):
        self.assertEqual(self.p.dumps(IntPair(3, 4)),
                     "O TwoInts L I 3 I 4 /L /O")
    
    def testloadobj(self):
        ip = self.p.loads("O TwoInts L I 3 I 4 /L /O")
        self.assertEqual(ip.x, 3)
        self.assertEqual(ip.y, 4)
    
    def testdumpemptydict(self):
        self.assertEqual(self.p.dumps({}), "D /D")
    
    def testdumpdict(self):
        self.assertEqual(self.p.dumps({1: 2}), "D I 1 I 2 /D")
    
    def testdumpdictnested(self):
        self.assertEqual(self.p.dumps({1: {2: 3}}), "D I 1 D I 2 I 3 /D /D")
    
    def testloaddict(self):
        self.assertEqual(self.p.loads("D I 1 I 2 /D"), {1: 2})
    
    def testloadnested(self):
        self.assertEqual(self.p.loads("D I 1 D I 2 I 3 /D /D"), {1: {2: 3}})
    
    def testdumpload(self):
        self.assertEqual(self.data1, self.p.loads(self.p.dumps(self.data1)))
    
    def testgzipped(self):
        self.p.compress(True)
        self.assertEqual(self.data1, self.p.loads(self.p.dumps(self.data1)))
    
    def testdumpobjfailure(self):
        self.assertRaises(safepickle.PicklingError, self.p.dumps, self.p)
    
    def testloadodddictfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "D I 1 /D")
    
    def testloademptyfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "")
    
    def testloadtoolongfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "I 5 I 6")
    
    def testloadunclosedlistfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "L I 1")
    
    def testloadunclosedtuplefailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "T I 1")
    
    def testloadunclosedstringfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "S I 1")
    
    def testloadbadbooleanfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "B =")
    
    def testloadbadintfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "I 43.5")
    
    def testloadbadfloatfailure(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads, "F bar")
    
    def testobjargsneedtobelist(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads,
                          "O tests.safepickleTest.IntPair I 3 I 4 /O")
    
    def testobjterminatornotfound(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads,
                          "O tests.safepickleTest.IntPair L I 3 I 4 /L")
    
    def testobjwrongargnumbers(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads,
                          "O tests.safepickleTest.IntPair I 3 /L /O")
    
    def testloadinvalidclass(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads,
                          "O someClass L /L /O")
    
    def testloadinvalidtoken(self):
        self.assertRaises(safepickle.UnpicklingError, self.p.loads,
                          "R")
