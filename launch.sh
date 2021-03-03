#!/bin/bash
for i in {1..1000}
do
   /usr/local/bin/python puzzlesolver.py
   echo $i
done
