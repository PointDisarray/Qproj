#!/usr/bin/python3

import datetime, sys, os
from subprocess import check_output as check
from quake_db_class import *

dbQuake = QuakeDatabase('root', 'y11091998', '127.0.0.1', 'stats')

dbQuake.connect()
dbQuake.switch_database()

tmp_match_id = 0
tmp_user_id = 0
query_params = []
file_name = "data_from_15_53_50.xml"


with open(file_name,"w+") as file:
    for line in f.readlines():
        if "matches," in line:
            query_params = line.strip().split(",")
            print(query_params)
        #if "players," in line:

        print("everything else")



dbQuake.disconnect()
