#!/bin/sh
. ./fixfile.sh

if [ $# == 1 ] && [ -f $1 ]
then 
    filename=$1
    echo "FOUND LIB $1"
else
    echo 'not found file'
    exit
fi

#---------- unzip lib to dir --------------
if [ -d 'lib' ]; then
    echo 'REMOVE OLD DIR..'
    rm -rf lib
fi

echo 'CREATE LIB DIR..'
mkdir lib

echo 'UNZIP FILE INTO DIR..'
unzip -qo $filename -d lib 

#-------------edit files-------------
files="top_bar.pyo side_window.pyo"
for file in $files
do
    if [ -f "lib/$file" ];then
        echo "FOUND $file"
    else
        echo "Not Found $file"
        exit
    fi
done

#------
uncompyle2 -o . lib/top_bar.pyo
top_bar
python -O -m py_compile lib/top_bar.pyo_dis
mv lib/top_bar.pyo_diso lib/top_bar.pyo



uncompyle2 -o . lib/side_window.pyo
side_windows
python -O -m py_compile lib/side_window.pyo_dis
mv lib/side_window.pyo_diso lib/side_window.pyo

# ----- compile and zip
cd lib
zip -qr shared.lib *




