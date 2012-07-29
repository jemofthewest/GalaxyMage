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


# To run a particular test from the commandline, run something like this:
# python TestSuite.py enginetests.MapTest


# Add main source file dir to our module path
import os, sys
if os.path.isdir(sys.path[0]):
    os.chdir(sys.path[0])
sys.path.append("..")

# Hackish fix: import and setup a Translate instance.
import Translate
testdir = sys.path[0] # remember the dir we are in
os.chdir(os.path.join ('..','..')) # move back to the root dir
translateConfig = Translate.Translate() # setup translation support
os.chdir(testdir) # change back to the test dir

# Get unittest support so we can run suites
import unittest
import getopt


def usage():
    """display usage information"""
    print """Run alone, this will run all tests.
  -h print this help
  -m test only the module given (ex. 'enginetests/MapTest')
  -p tests an entire test package (ex. 'enginetests')
  -v print each test and its result"""

def getTests(testpackage=None):
    '''return all the tests available'''
    tests = []
    if testpackage != None:
        for mod in os.listdir(testpackage):
            if mod[-7:] == "Test"+os.extsep+"py":
                module = mod[:-3]
                tests.append(testpackage+'.'+module)
    else:
        for package in os.listdir('.'):
            if package[-5:] == "tests":
                for mod in os.listdir(package):
                    if mod[-7:] == "Test"+os.extsep+"py":
                        module = mod[:-3]
                        tests.append(package+'.'+module)
    return tests

if __name__ == "__main__":
    #parse comman line options
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'm:hvp:')
    except getopt.GetoptError, e:
        print 'Error parsing command-line arguments: %s' % e
        usage()
        sys.exit(1)
    singlemodule = False
    singlepackage = False
    tests = []
    verbosity = 1
    for o, a in opts:
        if o == '-h': # Print the help file and exit.
            usage()
            sys.exit(0)
        if o == '-m': # Only run this single test.
            singlemodule = True
            a = a.replace('/', '.')
            a = a.replace('\\', '.')
            tests.append(a)
        if o == '-p': # Run all tests in a given package.
            singlepackage = True
            tests = getTests(a)
        if o == '-v': # Show all tests and results individually
            verbosity = 2
    
    # If specific tests weren't given, load all tests
    if singlemodule != True and singlepackage != True:
        tests = getTests()
    
    # Collect all the tests
    suites = []
    for module in tests:
        modulename = __import__(module, globals(), locals(), [''])
        suite = unittest.defaultTestLoader.loadTestsFromModule(modulename)
        suites.append(suite)
    
    # Assemble a suite list
    allTests = unittest.TestSuite(suites)
    # Run the full test suite
    unittest.TextTestRunner(verbosity=verbosity).run(allTests)
