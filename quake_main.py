#!/usr/bin/python3

import datetime
from quake_db_class import *

dbQuake = QuakeDatabase('root', 'y11091998', '127.0.0.1', 'stats')

dbQuake.connect()
dbQuake.switch_database()

#dbQuake.showDatabase()
#print("================")
#dbQuake.showTables()
#print("================")
dbQuake.addPlayer("yurii")
#print("Player id = "+str(player_id))
#print("================")
#game_date='2019-09-03 15:46:21'
user_name = 'yurii'
result = dbQuake.getUserIDbyName(user_name)
print(result[0])
#dbQuake.addMap("2020-01-03 20:42:26","map10","FFA",0,472)
#print("Map id = "+str(map_id))
print("================")
dbQuake.disconnect()
