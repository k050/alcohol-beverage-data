import sqlite3
import csv


conn = sqlite3.connect('abc.db')
cur = conn.cursor()
fhand = open('last_names.txt')


names_lst = []
match_lst = []
rows2=[]
for line in fhand:
    line = line.rstrip()
    #print line
    names_lst.append(line)
for i in names_lst:
    i = i.upper()
    my_string = i+","
    #print my_string
    query = "SELECT * FROM ABC_data WHERE (county = 'LOS ANGELES' OR county = 'ORANGE' OR county = 'SAN DIEGO' OR county = 'RIVERSIDE') AND contact_name LIKE '%"+i+"%' ORDER BY iso_date DESC LIMIT 200"
    #print query
    cur.execute(query)

    rows = cur.fetchall()
    #print rows
    for item in rows:
        item[4].rstrip()
        #print item[4],' ',item[2]
        if item[4].startswith(my_string):
            print '===',item[4],'===', item[2]
            if item not in rows2:
                rows2.append(item) #taking out repeats
#print rows2
rows3 = []
header_lst = []
for i in cur.description: #putting header in final list
    header_lst.append(i[0])
rows3.append(header_lst)

for i in rows2:  #adding list to header
    rows3.append(i)

rows4 = []
for i in rows3:
    if i[14] == None:
        temp_row3 = i[15],"Not A Transfer",i[2],i[3],i[4],i[7],i[8],i[9],i[10],i[11],i[6]
    else:
        temp_row3 = i[15],i[14],i[2],i[3],i[4],i[7],i[8],i[9],i[10],i[11],i[6]

    rows4.append(temp_row3)
#print rows4

with open('koreanLaOc.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(rows4)
