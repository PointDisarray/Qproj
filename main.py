#!/usr/bin/python3

import datetime, sys, os, re, subprocess
from subprocess import check_output as check
from quake_db_class import *

dbQuake = QuakeDatabase('eridan', 'forfun', '127.0.0.1', 'stats')

dbQuake.connect()
dbQuake.switch_database()


tmp_match_id = 0
tmp_user_id = 0
data = []
parser_path = ""
root_dir = ""

def wrong_arguments_error():
    print("Provide absolute path to directory you want to walkthrough as the first argument")
    print("Provide absolute path to the parsing file as the second argument")


if len(sys.argv) == 3:
    if os.path.isdir(sys.argv[1]) and os.path.isfile(sys.argv[2]):
        root_dir = str(sys.argv[1])
        parser_path = str(sys.argv[2])
    else:
        wrong_arguments_error()
        sys.exit()
else:
    print("Script requires 2 arguments")
    wrong_arguments_error()
    sys.exit()

def string_handler(file_name):
    with open(file_name) as file:
        for line in file.readlines():
            newline = line.replace('\'', '').replace(' ', '')
            if "matches," in line:
                data = newline.strip().split(",")
                data[2] = data[2][ : 10] + " " + data[2][10 : ]
                print(data)
                dbQuake.addMap(data[2], data[3], data[4], data[5], int(data[6]))
                tmp_match_id = dbQuake.getMatchIDbyDate(data[2])[0]
                #print(tmp_match_id)
                print("match inserted")
            if "players," in line:
                data = newline.strip().split(",")
                if not dbQuake.getUserIDbyName(data[1]):
                    dbQuake.addPlayer(data[1])
                    print("player inserted")
                tmp_user_id = dbQuake.getUserIDbyName(data[1])[0]
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
                print("powerup stat is inserted")


def recursive_insert(rootdir):
    subprocess.call(['tar', '-zcvf', root_dir+"_backup.tar.gz", rootdir])
    print("inside rec func")
    for path, dirs, files in os.walk(rootdir):
        for filename in files:
            # cur_file_path = os.path.abspath(filename)
            # print(cur_file_path)
            # print("inside file for")
            if re.search('^[0-2][0-9]_[0-5][0-9]_[0-5][0-9]\.xml$',filename):
                # print("inside if")
                filename_string = path+"/"+filename
                subprocess.call([parser_path, filename_string])
                string_handler(filename_string+".parsed")
                os.remove(filename_string+".parsed")
                os.rename(filename_string, path+"/"+"_INSERTED_"+filename)


recursive_insert(root_dir)
dbQuake.disconnect()


