#!/usr/bin/python3

import datetime, sys, os
from subprocess import check_output as check
from quake_db_class import *

dbQuake = QuakeDatabase('root', 'y11091998', '127.0.0.1', 'stats')

dbQuake.connect()
dbQuake.switch_database()

tmp_match_id = 0
tmp_user_id = 0
data = []
file_name = "data_from_15_53_50.xml"


with open(file_name) as file:
    for line in file.readlines():
        if "matches," in line:
            newline = line.replace('\'', '').replace(' ', '')
            data = newline.strip().split(",")
            print(data)
            qwe = data[2]
            print(qwe)
            data[2] = data[2][ : 10] + " " + data[2][10 : ]
            dbQuake.addMap(data[2], data[3], data[4], int(data[1]), int(data[6]))
        #if "players," in line:

        print("everything else")



dbQuake.disconnect()
