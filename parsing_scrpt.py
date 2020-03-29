#!/usr/bin/python

import sys,os,pdb
import xml.etree.ElementTree as ET

file_name = str(sys.argv[1])
print(file_name)
tree = ET.parse(file_name)
#root = tree.getroot()
f = open("parsed_file", 'w+')
f1 = open(file_name+".parsed", "w+")
f.write("Entity           Values\n\n")
ignore_elements = ['weapons', "items", "powerups"]
global_line = ""
k = 0
j = 0

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
        #print(child.tag, child.attrib)

# delete quotes from numbers
f.seek(0)
for line in f.readlines():
    i = 0
    if "matches" in line:
        line = line.replace("/", "-") # converting date to TIMESTAMP date format
    for i in range( len(line)):
        #print(i)
        if "\'" == line[i]:
                j = i-1
                k = i+1
                #print(k)
                #check if value in quotes is a number -> delete quote (right side)
                while k in range(len(line)-1):
                    if line[k].isdigit() or line[k] == '-':
                        #print("quote is not written in k")
                        k+=1
                    elif line[k] == "\'" or (line[k] == ',' and line[k+1] == ' '):
                        #print("break is made"
                        break
                    else:
                        #print("write quote in k")
                        f1.write(line[i])
                        break
                #check if value in quotes is a number -> delete quote (left side)
                while j in range(len(line)):
                    if line[j].isdigit() or line[j] == '-':
                        #print("quote is not written in j")
                        j-=1
                    elif line[j] == "\'" or line[j] == ' ':
                        #print("break is made in j")
                        break
                    else:
                        #print("write quote in j")
                        f1.write(line[i])
                        break

        else: f1.write(line[i])

f1.close()
f.close()
os.remove("parsed_file")




# while k in range(len(line)-1):
#     print(k)
#     if line[k].isdigit() or line[k] == '-':
#         print("quote is not written in k")
#         k+=1
#         print(k)
#     elif line[k] == "\'" or (line[k] == ',' and line[k+1] == ' '):
#         print("break is made")
#         break
#     else:
#         print(k)
#         print("write quote in k")
#         f1.write(line[i])
#         break
#
# while j in range(len(line)):
#     print(j)
#     if line[j].isdigit() or line[j] == '-':
#         print("quote is not written in j")
#         j-=1
#         print(j)
#     elif line[j] == "\'" or line[j] == ' ':
#         print("break is made in j")
#         break
#     else:
#         print(j)
#         print("write quote in j")
#         f1.write(line[i])
#         break
