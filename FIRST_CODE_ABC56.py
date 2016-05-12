"""
Grab new license data from CA ABC for sales leads
    CA seems to refresh data daily.

5/11/2016
    CA website had a bad link.
        added try-except(lic_number) right after tlst[] to skip these
    added iso date just in case it's needed later

"""



import urllib
from bs4 import BeautifulSoup
import json
#import xml.etree.ElementTree as ET
#import sys
import re
import unicodedata
import sqlite3
import dateutil.parser as dparser


#sql outside loop to create table.
conn = sqlite3.connect('abc.db')
    #update path after deciding where to put it
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS ABC_data(
    id INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
    license_number TEXT NOT NULL UNIQUE,
    owner_name TEXT,
    dba TEXT,
    contact_name TEXT,
    status_date TEXT,
    lic_type TEXT,
    street TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    county TEXT,
    census_tract TEXT,
    abc_region TEXT,
    transfer_from TEXT,
    iso_date TEXT)''')

url = "https://www.abc.ca.gov/datport/SubDlyNuRep.asp"
html = urllib.urlopen(url).read()

urlre = re.findall('(.*?/datport/)', url)
#print urlre

soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', {'class': 'report_column'})
#print table
#rows = table.findAll('td')
#print rows
links=[]
for l in soup.findAll('a', href=True):
    rlink = l['href']
    endl = re.findall('/datport/(.*[0-9])',rlink)
    if len(str(endl)) >2:
        link= urlre[0] + endl[0]
        links.append(link)
#print links

lcount = 0
#there must be a cleaner way to do this than a big for loop
for line in links:

    url2=links[lcount] #increase counter number to get next link

    html2 = urllib.urlopen(url2).read()
    soup2 = BeautifulSoup(html2, 'html.parser')

    #print soup2.prettify()
    text = soup2.findAll(text=True)
    clst = []
    for x in text:
        ax = unicodedata.normalize('NFKD',x).encode('ascii', 'ignore')
        ax = ax.replace('\n',"")
        ax = ax.replace('\r', "")
        ax = ax.strip("'")
        #ax = ax.replace(" ", "") #bad
        txt = ax.replace("\t", "")
        clst.append(txt)
        #bx = re.findall('[A-Za-z0-9:@,-]', ax) #bad
    #print clst

    #get usable data in a list
    tlst = []
    for x1 in clst:
        x2= re.findall('([0-9A-Za-z].*)', x1)
        if len(x2)>0:
            tlst.append(x2[0])

    #sorting through multiple possibilities to find a person
    officer_lst = []
    #print tlst
    try:
        lic_pos = int(tlst.index("License Number: ")+1)
    except:
        print "+++Error+++", line
        lcount +=1
        continue


    for officer in tlst:
        officer = re.findall("OFFICER: ?(.*)",officer)
        #member = re.findall("MEMBER: ?(.*)", officer)
        if len(officer)>0:
            officer_lst.append(officer[0])

    #trying to solve the issue of no data
    try:
        officer = officer_lst[0]
    except:
        for member in tlst:
            member = re.findall("MEMBER: ?(.*)", member)
            if len(member)>0:
                officer_lst.append(member[0])
    try:
        officer = officer_lst[0]
    except:
        officer = tlst[tlst.index("Licensee: ")+1]

    #print officer_lst
    #print tlst

    #used lic_pos in try except data return error filter.
    #lic_pos = int(tlst.index("License Number: ")+1)
    owner_pos=tlst.index("Primary Owner: ")+1
    office_pos = tlst.index("ABC Office of Application:  ")+1
    address_pos = tlst.index("Address: ")+1
    census_pos = tlst.index("Census Tract: ")+1
    city_pos = tlst.index("City: ")+1
    county_pos = tlst.index("County: ")+1
    state_pos = tlst.index("State: ")+1
    zip_pos = tlst.index("Zip Code: ")+1
    lic_type_pos = tlst.index("1) License Type:")+1
    sdate_pos = tlst.index("Status Date: ")+1

    #another sometimes no return value
    #if exists, it tells you it's not a new business but an owner xfer
    prev_pos = tlst.index("FROM: ")+1
    prev_txt = tlst[prev_pos]
    match = re.match("[0-9]{2}-[0-9]{6}",prev_txt) #throws a none if no pattern match
    #however printing match gives something that looks like memory position
    if match != None:
        prev = tlst[prev_pos]
    else:
        prev = None

    #this field also sometimes returns no data if no DBA
    try:
        dba_pos = tlst.index("Doing Business As: ")+1
        dba = tlst[dba_pos]
    except:
        dba = None

    license_number = tlst[lic_pos]
    owner_name = tlst[owner_pos]
    office = tlst[office_pos]
    address = tlst[address_pos]
    census = tlst[census_pos]
    city = tlst[city_pos]
    county = tlst[county_pos]
    state = tlst[state_pos]
    zipcode = tlst[zip_pos]
    lic_type = tlst[lic_type_pos]
    sdate = tlst[sdate_pos] #may need to re-format date


    print tlst[lic_pos-1], license_number
    print tlst[owner_pos -1], owner_name
    print "DBA: ", dba
    print tlst[office_pos-1], office
    print tlst[address_pos-1], address
    print tlst[census_pos-1], census
    print tlst[city_pos-1], city
    print tlst[county_pos-1], county
    print tlst[state_pos-1], state
    print tlst[zip_pos-1], zipcode
    print "Officer: ", officer
    print "License Type: ", lic_type
    print tlst[sdate_pos-1], sdate
    print "Transfer From: ", prev

    print "+Count+", lcount

    idate = dparser.parse(sdate)
    iso_date = idate.isoformat()
    print "ISO date" , iso_date, " type ", type(iso_date)
    print '========++++++====+++++'
    lcount += 1



    #inside loop

    cur.execute('''INSERT OR REPLACE INTO ABC_data(license_number, owner_name,
        dba, contact_name, status_date, street, city, state,
        zip, county, census_tract, abc_region, transfer_from, lic_type, iso_date)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (license_number, owner_name,
                dba, officer, sdate, address, city,
                state, zipcode, county, census, office,
                prev, lic_type, iso_date))
conn.commit()
conn.close()
