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

def sign(n):
    if n == 0.0:
        return 0
    elif n > 0.0:
        return 1
    else:
        return -1

def delay(f, *args):
    return lambda: f(*args)


# Lock class with traceback functionality. Currently unused, but
# didn't want to delete the code entirely, so moved it here.
class Lock(object):
    import traceback
    
    def __init__(self, lock):
        self._lock = lock
    
    def release(self):
        tb = traceback.extract_stack(limit=2)
        line = "rel %s:%d %s()" % tb[0][0:3]
        logger.debug(line)
        self._lock.release()
        logger.debug("rel done")

    def acquire(self):
        tb = traceback.extract_stack(limit=2)
        line = "acq %s:%d %s()" % tb[0][0:3]
        logger.debug(line)
        self._lock.acquire()
        logger.debug("acq done")

