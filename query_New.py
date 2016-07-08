import sqlite3
import csv


conn = sqlite3.connect('/home/pi/ABC/abc.db')
cur = conn.cursor()
fhand = open('/home/pi/ABC/last_names.txt')



query = "SELECT * FROM ABC_data WHERE (county = 'LOS ANGELES' OR county = 'ORANGE' OR county = 'SAN DIEGO' OR county = 'RIVERSIDE') AND transfer_from IS NULL ORDER BY iso_date DESC LIMIT 200"
#print query
cur.execute(query)

rows = cur.fetchall()
#print rows
rows2 = []
for item in rows:
    item[4].rstrip()
    #print item[4],' ',item[2]
    
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

with open('/home/pi/ABC/new.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(rows4)

