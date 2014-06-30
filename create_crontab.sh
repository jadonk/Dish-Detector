#!/bin/sh
echo "*/5 6,7,8,9,10,11,12,13,14,15,16,17,18,19,20 * * * python /var/lib/cloud9/Dish-­Detector/test-­sink-­and-­email.py > /var/lib/cloud9/Dish-Detector/cronlog.txt 2&>1" | crontab -
