#!/usr/bin/python3

from quake_db_class import *

dbQuake = QuakeDatabase('jeffrey', 'mypass', '127.0.0.1', 'stats')
                                                                                                         
dbQuake.showDatabase()
print("================")
dbQuake.showTables()
print("================")
dbQuake.insertPlayer("Fredie")
