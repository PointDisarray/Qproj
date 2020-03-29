-- MANUAL --
-- IMPORTANT -> this script clear all tables in stats schema
--
-- to run tests just source this file
--
-- Example
-- source /home/<user_name>/Desktop/Stats-XML/parsing-mysql/tests.sql;

use stats;

-- clean tables;
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE table items;
TRUNCATE table matches;
TRUNCATE table players;
TRUNCATE table powerups;
TRUNCATE table stats;
TRUNCATE table user_matches;
TRUNCATE table weapons;
SET FOREIGN_KEY_CHECKS = 1;

-- inset sample data to tables
insert into players(name) VALUES ('jan'), ('john'), ('mathewju'), ('lolo'), ('xd');
insert into matches(datetime, map, type, isTeamGame, duration) VALUES ('2020-04-04 15:45:45','map-12', 'test',TRUE, 12),
                                                                      ('2021-04-04 05:45:45','map-2', 'dev',TRUE, 12),
                                                                      ('2022-05-04 17:45:45','map-22', 'test2',FALSE, 45),
                                                                      ('2020-01-04 14:45:45','map-6', 'dev',FALSE, 23),
                                                                      ('2020-04-01 19:45:45','map-99', 'test',TRUE, 12);
insert into stats(name, value, players_id_player, matches_id_match) VALUES ('1234',5,1,1), ('5432',14,2,1), ('6578',20,2,1), ('4567',55,4,1), ('7890',2,5,1);
insert into items(name, pickups, players_id_player, matches_id_match) VALUES ('asd',1,1,1), ('xcv',2,2,3), ('xcv',3,3,3), ('xcv',4,4,1), ('xcv',5,5,1);
insert into powerups(name, pickups, time, players_id_player, matches_id_match) VALUES ('asfd',3,1000,2,2), ('cvbv',3,200,3,2), ('rthfg',3,500,1,4), ('fghb',3,800,1,2), ('uio',3,10,3,5);
insert into weapons(name, hits, shots, kills, players_id_player, matches_id_match) VALUES ('gun',5,4,3,1,1), ('rew',5,4,3,2,1), ('shotg',5,4,3,3,2), ('gu2n',5,4,3,4,5), ('asn',5,4,3,5,4);
insert into user_matches(players_id_player, matches_id_match) VALUES (1,1), (2,2), (3,3), (4,4), (5,5);

-- show inserted data
select * from players;
select * from matches;
select * from stats;
select * from items;
select * from powerups;
select * from weapons;
select * from user_matches;

-- join
select * from players left outer join items i on players.id_player = i.players_id_player;
select * from weapons right join stats s on weapons.name = s.name; -- tu beda nulle, bo nie maja wspolnych nazw
select * from user_matches left join players p on user_matches.players_id_player = p.id_player;

-- union
select * from powerups union all select * from powerups;
select * from items union distinct select * from stats;

-- nested select
select * from players where id_player = (select players_id_player from user_matches where id_user_relactions=1);