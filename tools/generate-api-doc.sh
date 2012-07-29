#!/bin/sh

# Generates API documentation and puts it in doc/api. Requires the
# "epydoc" command.

cd ../src
find . -name "*.pyc" | xargs rm -f
find . -name "*.pyo" | xargs rm -f
epydoc -o ../doc/api -t trees.html --no-private -n GalaxyMage -u http://www.galaxymage.org *.py gui
