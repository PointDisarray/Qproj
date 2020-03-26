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

```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

**Insert data to database**

```ruby
require 'redcarpet'
markdown = Redcarpet.new("Hello World!")
puts markdown.to_html
```

*Authors*

Piotr Rejczak\
Yurii Lapenchuk\
Konrad Szpakowski

