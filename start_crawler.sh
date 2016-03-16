#!/bin/bash

for i in /data/foreign_news_crawler/*.py
do
	nohup python $i &
done
