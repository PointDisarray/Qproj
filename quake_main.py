#!/usr/bin/python3

from quake_db_class import *

dbQuake = QuakeDatabase('jeffrey', 'mypass', '127.0.0.1', 'stats')

dbQuake.connect()
dbQuake.switch_database()
                                                                                        
dbQuake.showDatabase()
print("================")
dbQuake.showTables()
print("================")
player_id = dbQuake.addPlayer("Jasio")
print("Player id = "+str(player_id))
print("================")
#map_id = dbQuake.addMap("2019/09/03 15:46:21","cpm19","FFA",0,472)
#print("Map id = "+str(map_id))
#print("================")
dbQuake.disconnect()
