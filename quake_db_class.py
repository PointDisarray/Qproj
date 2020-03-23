#!/usr/bin/python3

import mysql.connector
from mysql.connector import errorcode
import os

class QuakeDatabase:

    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database

    def connect(self):
        try:
           print("Connecting to " + self.database + " database, please wait ...")
           os.system("sleep 2")
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
        print("Disconnect from " + self.database + " ...")
        os.system("sleep 2")

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
        self.cursor.execute("INSERT INTO players (name) VALUES (\""+player_name+"\");")
        self.mydb.commit()
        #__dbInfoUpdate__(player_name, self.database)
        print(player_name.upper()+" has been added to "+self.database.upper()+" database sucesfully")
        return self.cursor.lastrowid

    def addMap(self, matche_date, matche_map, matche_type, matche_isTeamGame, matche_duration):
        self.cursor.execute("INSERT INTO matches (datetime, map, type, isTeamGame, duration)\
                             VALUES (\""+matche_date+"\",\""+matche_map+"\",\""+matche_type+"\","+matche_isTeamGame+","+matche_duration+");")
        self.mydb.commit()
        return self.cursor.lastrowid        

    #def insertStats(self, stat_name, stat_value):
    #    self.cursor.execute("INSERT INTO players (
    
    #def insertStats(self, stat_name, stat_value):
