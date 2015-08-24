#!/bin/bash

for i in /root/foreign_news_crawler/*.py
do
	nohup python $i &
done

wait

nohup python /root/foreign_news_crawler/pipeline/pipeline.py &
