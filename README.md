Quake Project
---

This project consist of three parts.
-  First part - create schema to store data
-  Second part - parsing, data extracting
-  Third part - insert parsed data to database

**Database schema**

###

Tables
```
 Table 'players' stores:
    - id_player
    - name

 Table 'powerups' stores players powerups:
    - id_powerups
    - name
    - pickups
    - time
    - players_id (foregin key 'players')
    - matches_id ( foregin key 'matches')

 Table 'weapons' stores players weapons:
    - id_weapons
    - name
    - hits
    - shots
    - kills
    - players_id (foregin key 'players')
    - matches_id ( foregin key 'matches')

 Table 'items' stores players items:
    - id_item
    - name
    - pickups
    - players_id (foregin key 'players')
    - matches_id ( foregin key 'matches')

 Table 'stats' stores players statistics:
    - id_stats
    - name
    - value
    - players_id (foregin key 'players')
    - matches_id ( foregin key 'matches')

 Table 'matches' stored information about players matches:
    - id_match
    - datetime
    - map
    - type
    - isteamGame
    - duration

 Table 'user_matches' stores information which players played in particular match:
    - id_user_relations
    - players_id (foregin key 'players')
    - matches_id ( foregin key 'matches')
```

###

*Relations*

###

```
 Table players is main table, has relations one to many with every table in schema.

 Table players has 4 tables ('powerups', 'weapons', 'items', 'stats') which stores information about players. 
 Those tables are connected with 'players' table many to one relations

 Table 'user_matches' stores informations about which player played in particular match. 
 Table has two many to one realtions between 'players' table and 'matches' table.

 Table 'matches' stored data about matches.
 It has got 4 one to many relations with 'powerups', 'weapons', 'items', 'stats' and 'user_matches' table.
```

###

**Parsing data**

This part has two tasks. First task is to create parser that will transform .xml file into simple data file.
Second task is to extract data from the data file and insert that data into specific methods of database
class. 

*parsing_scrpt.py - is a parsing script of this project*

This script can take only one argument - filename of the file you want to parse. Script can handle both 
absolute path and relative path of the file. So correct execution of the script looks like this:

```./parsing_scrpt.py text.xml```    or    ```./parsing_scrpt.py /home/burnley/stats/text.xml```

As you can see in the code example down below, script uses xml.etree python module to iterate through each element in the .xml file. After that script 
will ignore elements mentioned in 'ignore_elements' list. The next step is to modify element string and 
write it into a new-created file line by line.

```python
for child in tree.iter():
    if child.tag not in ignore_elements:
        switcher = {
            'match': "matches,",
            'player': "players,",
            'stat': "stats,",
            'weapon': "weapons,",
            'item': "items,",
            'powerup': "powerups,",
        }
        f.write(switcher.get(child.tag, "") + "           " +str(child.attrib.values())
                .replace('[', '').replace(']', '')
                .replace('dict_values(', '').replace(')', '') + "\n")
```
After that script removes all quotes from the elements with numeric values. Uses ```file.seek(0)``` function
in order to put pointer back at the start of the file. This allows to start the process of removing specific
quotes in each line. Once all lines are verified or modified, script closes all files. Now you have a parsed
file you can use in the next steps.

Second task is based on extracting data from parsed file. So the main.py script was created.

*main.py - is a script that will use all insert methods in database class.*

This script takes two arguments:

- absolute path to the directory with .xml files (f.e.: /home/burnley/stats)
- absolute path to the parser script (f.e.: /home/burnley/project/parsing_scrpt.py)

!!!This script will not work with relative paths!!!

Correct usage of the main.py script looks as follows:

```./main.py /home/burnley/stats /home/burnley/project/parsing_scrpt.py```

You should change database credentials in main.py: 

```dbQuake = QuakeDatabase('eridan', 'forfun', '127.0.0.1', 'stats')```

After execution script will use recursive_insert function which will recursively visit each directory in 
order to find .xml files that match special regexp. Script will perform this action only in the ```rootdir``` which
you have passed as the first argument. After the file match script executes parsing_scrpt.py with matched 
filename as an argument.

```python
def recursive_insert(rootdir):
    subprocess.call(['tar', '-zcvf', root_dir+"_backup.tar.gz", rootdir])
    print("inside rec func")
    for path, dirs, files in os.walk(rootdir):
        for filename in files:
            if re.search('^[0-2][0-9]_[0-5][0-9]_[0-5][0-9]\.xml$',filename):
                # print("inside if")
                filename_string = path+"/"+filename
                subprocess.call([parser_path, filename_string])
                string_handler(filename_string+".parsed")
                os.remove(filename_string+".parsed")
                os.rename(filename_string, path+"/"+"_INSERTED_"+filename)
```
The next step is to use another main.py function - string_handler(filename). That function will read all
lines of the parsed file one by one and will look for matches in if statements. All if statements look for
a certain pattern in line. When the match is found database functions will use that line as the parameter
for insert, select etc. The part of string_handler() function is presented below:

```python
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
```

After that parsed file is removed and original .xml file gets renamed with '_INSERTED_' prefix addition. 
So the next time script will be executed it will ignore file with that prefix, since all the records of 
that file have been already inserted. Sometimes you will need to insert all that data into another database.
Script main.py creates tar with rootdir backup. All files inside will not have 'INSERTED' prefix, so can be
added to another database. 

###

**Insert data to database**

###

Python class quake_db_class include all methods to work with database.

Method to store data about database connection.
```
 def __init__(self, username, password, host, database):
    self.username = username
    self.password = password
    self.host = host
    self.database = database
```

Method to connect to the database
```
 def connect(self):
    try:
       print("Connecting to " + self.database + " database, please wait ...")
       os.system("sleep 1")
       # connect to database
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
```

Method to disconnect from database
```
 def disconnect(self):
     self.mydb.close()
     print("Disconnect from " + self.database + " database ...")
     os.system("sleep 1")
```

Method to switch database
```
 def switch_database(self):
     self.cursor.execute("USE " + self.database + ";")
```

Method to show databases
```
 def showDatabase(self):
     self.cursor.execute("SHOW DATABASES;")
     result = self.cursor.fetchall()
     for db in result:
         print(db)
```

Method to show tables
```
 def showDatabase(self):
     self.cursor.execute("SHOW DATABASES;")
     result = self.cursor.fetchall()
     for db in result:
         print(db)
```

Method to add player
```
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
```

Method to add map
```
 # add values to matches table
 def addMap(self, match_date, match_map, match_type, match_isTeamGame, match_duration):
     try:
        query = "INSERT INTO matches (datetime,map,type,isTeamGame,duration) VALUES (\"%s\",\"%s\",\"%s\",%s,%d)" % (match_date, match_map,match_type,match_isTeamGame,match_duration)

        self.cursor.execute(query)
        self.mydb.commit()
        print("Record has been added successfully")
        return True
     except Error as e:
        print("Error:", e)
        self.mydb.rollback()
        return False
```

Method to show selected player
```
 def getUserIDbyName(self, player_name):
     try:
         query = "SELECT id_player FROM players WHERE players.name = \'%s\'" % player_name     #  = \'%s\'" % player_name
         self.cursor.execute(query)
         # self.mydb.commit()
         row = self.cursor.fetchone()
         return row
     except Error as e:
         print("Error:", e)
         self.mydb.rollback()
         return "Exception has occured, SELECT query failed"
```

Method to show which player played in particular time
```
 def getMatchIDbyDate(self, date):
     try:
         query = "SELECT id_match FROM matches WHERE matches.datetime = \'%s\'" % date
         self.cursor.execute(query)
         # save output to variable, in this case that is a row from table
         row = self.cursor.fetchone()
         # return that row
         return row
     except Error as e:
         print("Error:", e)
         self.mydb.rollback()
         return "Exception has occured, SELECT query failed"
```

Method to add items
```
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
```

Method to add player stats
```
 def addStats(self, stat_name, stat_value, item_player_id, item_match_id):
     try:
        query = "INSERT INTO stats (name, value, players_id_player, matches_id_match) VALUES (\"%s\",%d,%d,%d)" % (stat_name, stat_value, item_player_id, item_match_id)

        self.cursor.execute(query)
        self.mydb.commit()
        print("Record has been added successfully")
        return True
     except Error as e:
        print("Error:", e)
        self.mydb.rollback()
        return False
```

Method to add weapons
```
 def addWeapons(self, weapon_name, weapon_hit, weapon_shot, weapon_kill, item_player_id, item_match_id):
     try:
        query = "INSERT INTO weapons (name, hits, shots, kills, players_id_player, matches_id_match) VALUES (\"%s\",%d,%d,%d,%d,%d)" % (weapon_name, weapon_hit, weapon_shot, weapon_kill, item_player_id, item_match_id)

        self.cursor.execute(query)
        self.mydb.commit()
        print("Record has been added successfully")
        return True
     except Error as e:
        print("Error:", e)
        self.mydb.rollback()
        return False
```

Method to add powerup player
```
 def addPowerUps(self, power_name, power_pick, power_time, item_player_id, item_match_id):
     try:
        query = "INSERT INTO powerups (name, pickups, time, players_id_player, matches_id_match) VALUES (\"%s\",%d,%d,%d,%d)" % (power_name, power_pick, power_time, item_player_id, item_match_id)

        self.cursor.execute(query)
        self.mydb.commit()
        print("Record has been added successfully")
        return True
     except Error as e:
        print("Error:", e)
        self.mydb.rollback()
        return False
```

Method to insert player_id and matches_id into one table
```
def addUserMatches(self, item_player_id, item_match_id):
    try:
       query = "INSERT INTO user_matches (players_id_player, matches_id_match) VALUES (%d,%d)" % (item_player_id, item_match_id)

       self.cursor.execute(query)
       self.mydb.commit()
       print("Record has been added successfully")
       return True
    except Error as e:
       print("Error:", e)
       self.mydb.rollback()
       return False
```

###

*Authors*

Piotr Rejczak\
Yurii Lapenchuk\
Konrad Szpakowski

