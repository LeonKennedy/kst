#!/bin/sh
. ./fixfile.sh

if [ $# == 1 ] && [ -f $1 ]
then 
    filename=$1
    echo "found lib $1"
else
    echo 'not found file'
    exit
fi

#---------- unzip lib to dir --------------
if [ -d 'lib' ]; then
    echo 'remove old dir..'
    rm -rf lib
fi

echo 'create lib dir'
mkdir lib

echo 'unzip lib file into dir..'
unzip -qo $filename -d lib 

#-------------edit files-------------
files="top_bar.pyo side_window.pyo hdhfa"
for file in $files
do
    if [ -f "lib/$file" ];then
        echo "find $file"
    fi
done

#------
uncompyle2 -o . lib/top_bar.pyo
top_bar
python -O -m py_compile lib/top_bar.pyo_dis
mv lib/top_bar.pyo_diso lib/top_bar.pyo

# ----- compile and zip
cd lib
zip -r shared.lib *




