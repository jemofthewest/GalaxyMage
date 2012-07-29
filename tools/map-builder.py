#!/usr/bin/env python

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

import os, sys

if len(sys.argv) != 3:
    print "Usage: map-builder.py INFILE OUTFILE"
    sys.exit(0)

sys.path.append(os.path.join(sys.path[0], "..", "src"))

import engine.MapGenerator
    
infile = sys.argv[1]
outfile = sys.argv[2]

f = file(infile, "rU")
data = f.read()
f.close()

globalvars = {}
localvars = {}
module = compile("from engine.MapGenerator import *",
                 "MapGenerator.py", "exec")
eval(module, globalvars)

compiled = compile(data, infile, 'exec')
eval(compiled, globalvars, localvars)

output = localvars['MAP']

f = file(outfile + ".py", "wU")
f.write(output)
f.close()

os.chdir(os.path.join(sys.path[0], ".."))
os.system("python GalaxyMage.py -m %s" % outfile)
