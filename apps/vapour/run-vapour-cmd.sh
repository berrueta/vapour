#!/bin/sh

VAPOUR_BASE_DIR=`pwd`

export PYTHONPATH=$VAPOUR_BASE_DIR/src:$PYTHONPATH

export VAPOUR_RDF_FILES=$VAPOUR_BASE_DIR/../../webpage
export VAPOUR_TEMPLATES=$VAPOUR_BASE_DIR/src/vapour/strainer/templates

export OUTPUT_DIR=../../webpage

# Recipe 1
python2.4 src/vapour/cup/cmdline.py \
    1 \
    "http://localhost/~berrueta/recipes-web/example1" \
    "http://localhost/~berrueta/recipes-web/example1#Concept" \
    "http://localhost/~berrueta/recipes-web/ERRATA/example1#prefLabel" \
    $OUTPUT_DIR/recipe1.html \
    $OUTPUT_DIR/recipe1.rdf

# Recipe 2
python2.4 src/vapour/cup/cmdline.py \
    2 \
    "http://localhost/~berrueta/recipes-web/example2/" \
    "http://localhost/~berrueta/recipes-web/example2/ClassA" \
    "http://localhost/~berrueta/recipes-web/example2/propB" \
    $OUTPUT_DIR/recipe2.html \
    $OUTPUT_DIR/recipe2.rdf

# Recipe 3
python2.4 src/vapour/cup/cmdline.py \
    3 \
    "http://localhost/~berrueta/recipes-web/example3" \
    "http://localhost/~berrueta/recipes-web/example3#Concept" \
    "http://localhost/~berrueta/recipes-web/example3#prefLabel" \
    $OUTPUT_DIR/recipe3.html \
    $OUTPUT_DIR/recipe3.rdf

# Recipe 4
python2.4 src/vapour/cup/cmdline.py \
    4 \
    "http://localhost/~berrueta/recipes-web/example4/" \
    "http://localhost/~berrueta/recipes-web/example4/Concept" \
    "http://localhost/~berrueta/recipes-web/example4/prefLabel" \
    $OUTPUT_DIR/recipe4.html \
    $OUTPUT_DIR/recipe4.rdf

# Recipe 5
python2.4 src/vapour/cup/cmdline.py \
    5 \
    "http://localhost/~berrueta/recipes-web/example5/" \
    "http://localhost/~berrueta/recipes-web/example5/Concept" \
    "http://localhost/~berrueta/recipes-web/example5/prefLabel" \
    $OUTPUT_DIR/recipe5.html \
    $OUTPUT_DIR/recipe5.rdf    
