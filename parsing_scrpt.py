#!/usr/bin/python

import sys,os
import xml.etree.ElementTree as ET

file_name = str(sys.argv[1])
tree = ET.parse(file_name)
#root = tree.getroot()
f = open("parsed_file", 'w+')
f.write("Entity           Values\n\n")
ignore_elements = ['weapons', "items", "powerups"]

for child in tree.iter():
    if child.tag not in ignore_elements:
        switcher = {
            'match': "matches",
            'player': "players",
            'stat': "stats",
            'weapon': "weapons",
            'item': "items",
            'powerup': "powerups",
        }
        f.write(switcher.get(child.tag, "") + "           " +str(child.attrib.values())
                .replace('[', '').replace(']', '')
                .replace('dict_values(', '').replace(')', '') + "\n")
        #print(child.tag, child.attrib)

f.close()

#
# with open('parsed_file', 'w+') as f1:
#     for line in f1.readlines():
#         for char in line:
#             if char.isdigit() == true:
#                 print("this char: " + char + " is digit")
#
# f1.close()
