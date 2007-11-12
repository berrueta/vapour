#!/bin/sh

VAPOUR_BASE_DIR=`pwd`

export PYTHONPATH=$VAPOUR_BASE_DIR/src:$PYTHONPATH

export VAPOUR_RDF_FILES=$VAPOUR_BASE_DIR/../../webpage
export VAPOUR_TEMPLATES=$VAPOUR_BASE_DIR/src/vapour/strainer/templates
export VAPOUR_LOG=$VAPOUR_BASE_DIR/log.txt

#export OUTPUT_DIR=../../webpage

python2.4 src/vapour/cup/webclient.py
