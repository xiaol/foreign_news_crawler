#!/bin/bash

for i in *.py
do
	nohup python $i &
done

nohup python pipeline.py &