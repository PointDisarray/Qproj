#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import os
import datetime

class QuakeDatabase:

    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database

    def connect(self):
        try:
           print("Connecting to " + self.database + " database, please wait ...")
           os.system("sleep 1")
           self.mydb = mysql.connector.connect(user=self.username, password=self.password,
                                          host=self.host, database=self.database)
           self.cursor = self.mydb.cursor()
        except mysql.connector.Error as err:
           if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
              print("Something is wrong with your user name or password")
              exit(1)
           elif err.errno == errorcode.ER_BAD_DB_ERROR:
              print("Database does not exist")
              exit(1)
           else:
              print(err)
              exit(1)

    def disconnect(self):
        self.mydb.close()
        print("Disconnect from " + self.database + " database ...")
        os.system("sleep 1")

    def switch_database(self):
        self.cursor.execute("USE " + self.database + ";")

    #def __dbInfoUpdate__(self, record, database_name):
    #    print(record.upper()+" has been added to "+database_name.upper()+" database sucesfully")

    def showDatabase(self):
        self.cursor.execute("SHOW DATABASES;")
        result = self.cursor.fetchall()
        for db in result:
            print(db)
    
    def showTables(self):
        self.cursor.execute("SHOW TABLES;")
        result = self.cursor.fetchall()
        for db in result:
            print(db)
    
    def addPlayer(self, player_name):
        
        query = "INSERT INTO players (name) VALUES (\"%s\")" % player_name
        
        try:
           self.cursor.execute(query)
           self.mydb.commit()
           print(player_name.upper()+" has been added to "+self.database.upper()+" database sucesfully")
           return True
        except Error as e:
           print("Error:", e)
           self.mydb.rollback()
           return False 

    def addMap(self, match_date, match_map, match_type, match_isTeamGame, match_duration):
        try: 
           query = "INSERT INTO matches (datetime,map,type,isTeamGame,duration) VALUES (\"%s\",\"%s\",\"%s\",%d,%d)" % (match_date, match_map,match_type,match_isTeamGame,match_duration)

           self.cursor.execute(query)
           self.mydb.commit()
           print("Record has been added successfully")
           return True
        except Error as e:
           print("Error:", e)
           self.mydb.rollback()
           return False

    def addItem(self, item_name, item_pickup, item_player_id, item_match_id):
        try:
           query = "INSERT INTO items (name, pickups, players_id_player, matches_id_match) VALUES (\"%s\",%d,%d,%d)" % (item_name, item_pickup, item_player_id, item_match_id)

           self.cursor.execute(query)
           self.mydb.commit()
           print("Record has been added successfully")
           return True
        except Error as e:
           print("Error:", e)
           self.mydb.rollback()
           return False

