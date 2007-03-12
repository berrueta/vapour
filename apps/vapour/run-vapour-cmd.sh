#!/bin/sh

VAPOUR_BASE_DIR=`pwd`

export PYTHONPATH=$VAPOUR_BASE_DIR/src:$PYTHONPATH

export VAPOUR_RDF_FILES=$VAPOUR_BASE_DIR/../../webpage
export VAPOUR_TEMPLATES=$VAPOUR_BASE_DIR/src/vapour/strainer/templates

python2.4 src/vapour/cup/cmdline.py \
    1 \
    "http://vapour.sourceforge.net/recipes-web/example1" \
    "http://vapour.sourceforge.net/recipes-web/example1#Concept" \
    "http://vapour.sourceforge.net/recipes-web/ERRATA/example1#prefLabel"

python2.4 src/vapour/cup/cmdline.py \
    2 \
    "http://isegserv.itd.rl.ac.uk/VM/http-examples/example2/" \
    "http://isegserv.itd.rl.ac.uk/VM/http-examples/example2/ClassA" \
    "http://isegserv.itd.rl.ac.uk/VM/http-examples/example2/propB"
