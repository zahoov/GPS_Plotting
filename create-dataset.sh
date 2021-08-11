#!/usr/bin/env bash

unzip -f $1

tif=$(ls *.tif)

OUTDIR="./data"
if [ ! -e $OUTDIR ] ; then
    echo $OUTDIR does not exist!
fi

CUR_DIR=$(pwd)

set -eu

cd $OUTDIR
bash ../create-tiles.sh $tif 10 10
rm -rf tif

cd $CUR_DIR
