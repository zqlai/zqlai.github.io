#!/usr/bin/bash
BASEDIR=`pwd`
GITHUB_PAGES_BRANCH=master
OUTPUTDIR=$BASEDIR/output
INPUTDIR=$BASEDIR/content
PUBLISHCONF=$BASEDIR/publishconf.py

DATE=`date +%Y-%m-%d:%H:%M:%S`

echo $DATE

#$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)
pelican $INPUTDIR -o $OUTPUTDIR -s $PUBLISHCONF  
ghp-import -m "Generate Pelican site @ $DATE" -b $GITHUB_PAGES_BRANCH $OUTPUTDIR
git push origin $GITHUB_PAGES_BRANCH
