#!/usr/bin/python3

import mysql.connector

class QuakeDatabase:

    def __init__(self, username, password, host, database):
        self.username = username
        self.password = password
        self. host = host
        self. database = database

    def __connect__(self):
        self.mydb = mysql.connector.connect(user=self.username, password=self.password,
                                       host=self.host, database=self.database)
        self.cursor = self.mydb.cursor()

    def __disconnect__(self):
        self.mydb.close()


    def showDatabase(self):
        self.__connect__()
        self.cursor.execute("SHOW DATABASES;")
        result = self.cursor.fetchall()
        for db in result:
            print(db)
        self.__disconnect__()

    def showTables(self):
        self.__connect__()
        self.cursor.execute("USE "+self.database+";")
        self.cursor.execute("SHOW TABLES;")
        result = self.cursor.fetchall()
        for db in result:
            print(db)
        self.__disconnect__()

