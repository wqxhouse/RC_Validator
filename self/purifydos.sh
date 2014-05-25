#!/bin/bash
for file in *.rc;
do
    dos2unix -n $file $file
done

