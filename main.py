#!/usr/bin/python3

import datetime, sys, os
from subprocess import check_output as check
from quake_db_class import *

dbQuake = QuakeDatabase('root', 'forfun', '127.0.0.1', 'stats')

dbQuake.connect()
dbQuake.switch_database()

tmp_match_id = 0
tmp_user_id = 0
data = []
file_name = "data_from_15_53_50.xml"


with open(file_name) as file:
    for line in file.readlines():
        newline = line.replace('\'', '').replace(' ', '')
        if "matches," in line:
            data = newline.strip().split(",")
            data[2] = data[2][ : 10] + " " + data[2][10 : ]
            dbQuake.addMap(data[2], data[3], data[4], int(data[1]), int(data[6]))
            tmp_match_id = dbQuake.getMatchIDbyDate(data[2])[0]
            print(tmp_match_id)
        if "players," in line:
            data = newline.strip().split(",")
            print(data)
            dbQuake.addPlayer(data[1])
            tmp_user_id = dbQuake.getUserIDbyName(data[1])[0]
            print(tmp_user_id)
            #insert into user_matches function will be here + temp_user_id, temp_match_id will be used
        if "stats," in line:
            data = newline.strip().split(",")
            #insert into stats function will be here + temp_user_id, temp_match_id will be used


dbQuake.disconnect()
