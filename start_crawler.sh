#!/bin/bash

for i in *.py
do
	nohup python $i &
done

wait

nohup python pipeline/pipeline.py &
