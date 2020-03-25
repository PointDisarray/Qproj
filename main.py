#!/usr/bin/python3

import datetime, sys, os
from subprocess import check_output as check
from quake_db_class import *

dbQuake = QuakeDatabase('eridan', 'forfun', '127.0.0.1', 'stats')

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
            print(data)
            dbQuake.addMap(data[2], data[3], data[4], data[1], int(data[6]))
            tmp_match_id = dbQuake.getMatchIDbyDate(data[2])[0]
            #print(tmp_match_id)
            print("match inserted")
        if "players," in line:
            data = newline.strip().split(",")
            #print(data)
            dbQuake.addPlayer(data[1])
            print("player inserted")
            tmp_user_id = dbQuake.getUserIDbyName(data[1])[0]
            #print(tmp_user_id)
            dbQuake.addUserMatches(tmp_user_id, tmp_match_id)
            print("player match inserted")
        if "stats," in line:
            data = newline.strip().split(",")
            # print(data)
            dbQuake.addStats(data[1], int(data[2]), tmp_user_id, tmp_match_id)
            print("stat inserted")
        if "weapons," in line:
            data = newline.strip().split(",")
            dbQuake.addWeapons(data[1], int(data[2]), int(data[3]), int(data[4]), tmp_user_id, tmp_match_id)
            print("weapon stat inserted")
        if "items," in line:
            data = newline.strip().split(",")
            dbQuake.addItem(data[1], int(data[2]), tmp_user_id, tmp_match_id)
            print("item stat inserted")
        if "powerups," in line:
            data = newline.strip().split(",")
            dbQuake.addPowerUps(data[1], int(data[2]), int(data[3]), tmp_user_id, tmp_match_id)


dbQuake.disconnect()
