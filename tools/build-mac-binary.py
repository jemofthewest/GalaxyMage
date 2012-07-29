#!/usr/bin/env python

# python build-mac-binary.py py2app --argv-emulation
# scp user@download.gna.org:/upload/tactics

import os.path

def collect(arg, dirname, filenames):
    filenames = [f for f in filenames if os.path.isfile(f)]
    if filenames:
        arg.append((dirname, filenames))

if __name__ == "__main__":
    import sys, os, string
    import py2app
    from distutils.sysconfig import *
    from distutils.core import setup,Extension
    from distutils.command.build_ext import build_ext
    from distutils.command.install import install
    from distutils.command.install_data import install_data

    os.chdir(sys.path[0])
    os.chdir('..')
    sys.path.append('src')

    os.system('rm -rf build dist')
    os.system('mkdir dist')
    os.system('svn export data dist/data')
    os.system('svn export doc dist/doc')
    os.system('svn export locale dist/locale')

    os.chdir('dist')
    allData = [('', ['COPYRIGHT.txt', 'CREDITS.txt', 'README.txt'])]
    os.path.walk('data', collect, allData)
    os.path.walk('doc', collect, allData)
    #os.system('rm -rf data doc')
    os.chdir('..')

    #print allData
    #sys.exit(0)
  
    setup (
            name = "GalaxyMage",
            version = "0.1.0",
            author = "Colin McMillen",
            author_email = "mcmillen@cs.cmu.edu",
            url = "http://www.galaxymage.org",
            description = "GalaxyMage Tactical RPG",
            license = "GNU GPL",
            app = [ 'GalaxyMage.py', ],
            data_files= allData
            )
#    os.system('mv dist GalaxyMage')
#    os.system('rm -f GalaxyMage.zip')
#    os.system('zip -r -9 GalaxyMage.zip GalaxyMage')
#    os.system('rm -rf build/ GalaxyMage/')
