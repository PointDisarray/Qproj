#!/usr/bin/python3

import mysql.connector
from mysql.connector import errorcode

class QuakeDatabase:

    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self.host = host
        self.database = database

    def __connect__(self):
        try:
           self.mydb = mysql.connector.connect(user=self.username, password=self.password,
                                          host=self.host, database=self.database)
           self.cursor = self.mydb.cursor()
        except mysql.connector.Error as err:
           print("Something went wrong: {}".format(err))
           exit(1)

    def __disconnect__(self):
        self.mydb.close()

    def __switch_database__(self):
        self.cursor.execute("USE " + self.database + ";")

    def showDatabase(self):
        self.__connect__()
        self.cursor.execute("SHOW DATABASES;")
        result = self.cursor.fetchall()
        for db in result:
            print(db)
        self.__disconnect__()
    
    def showTables(self):
        self.__connect__()
        self.__switch_database__()
        self.cursor.execute("SHOW TABLES;")
        result = self.cursor.fetchall()
        for db in result:
            print(db)
        self.__disconnect__()
    
    def insertPlayer(self,player_name):
        self.__connect__()
        self.__switch_database__()
        self.cursor.execute("INSERT INTO players (name) VALUES (\""+player_name+"\");")
        self.mydb.commit()
        self.__disconnect__()
