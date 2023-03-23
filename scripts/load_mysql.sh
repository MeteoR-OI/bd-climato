#!/bin/bash

for f in $(cat db.txt)
do
    filename=dina/weewx_"$f".sql;
    echo "loading mysql "$f" from backup " $filename;
    mysql -u nico '-pFuniculi' '-e drop database if exists '$f';';
    mysql -u nico '-pFuniculi' '-e create database '$f';';
    mysql -u nico '-pFuniculi' $f < $filename;
done
