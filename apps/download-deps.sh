
PIPCMD=pip-2.7
LIB=../lib

mkdir -p $LIB

$PIPCMD install --download=$LIB django==1.5.1 && tar xzf $LIB/Django-1.5.1.tar.gz --strip-components=1 Django-1.5.1/django

$PIPCMD install --download=$LIB Cheetah==2.4.4 && tar xzf $LIB/Cheetah-2.4.4.tar.gz --strip-components=1 Cheetah-2.4.4/cheetah && mv cheetah Cheetah

$PIPCMD install --download=$LIB rdflib==3.4.0 && tar xzf $LIB/rdflib-3.4.0.tar.gz --strip-components=1 rdflib-3.4.0/rdflib

$PIPCMD install --download=$LIB rdfextras==0.4 && tar xzf $LIB/rdfextras-0.4.tar.gz --strip-components=1 rdfextras-0.4/rdfextras

# pyparsing >= 2.0.0 requires python >= 3.0
$PIPCMD install --download=$LIB pyparsing==1.5.7 && unzip -j $LIB/pyparsing-1.5.7.zip pyparsing-1.5.7/pyparsing.py

$PIPCMD install --download=$LIB isodate==0.4.9 && tar xzf $LIB/isodate-0.4.9.tar.gz --strip-components=2 isodate-0.4.9/src/isodate
