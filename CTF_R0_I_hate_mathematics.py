#!/usr/bin/env python
import requests
import hashlib
import urllib2
import re
from lxml import html
import binascii

#Challenge Information
#https://ringzer0ctf.com/challenges/32

#cookie storage
session_name = 'PHPSESSID'
session_value = '<CookieValue>'

#cookie session
session = requests.Session()
jar = requests.cookies.RequestsCookieJar()
jar.set(session_name, session_value)
session.cookies = jar

#request session
inspected_webpage = session.get('https://ringzer0ctf.com/challenges/32/')

#pull webcontent
tree = html.fromstring(inspected_webpage.content)

#scrape everything from class "message"
export_html = tree.xpath('string(//div[@class="message"])')
#Grab message of binary data

#removing specific words
export_rbm = re.sub("BEGINMESSAGE", "", export_html)
export_rbem = re.sub("ENDMESSAGE", "", export_rbm)

#message
message = export_rbem

#Splitting of string
splitstr = message.split( )

#grabbing substrings
x = splitstr[4]
y = splitstr[6]
z = splitstr[8]

#Conversion to Integer
x = int(x)
y = int(y, base=16)
z = int(z, 2)

#Calculation
xyz = x + y - z

updated_webpage = session.get('https://ringzer0ctf.com/challenges/32/'+str(xyz))

final_results = re.findall(r"FLAG.{0,30}", updated_webpage.text)

print(final_results)

#Math Breakdown
"""
#String
math = "2309 + 0x242b - 111111001111 = ?"

#Splitting of string
splitstr = math.split( )

#confirming array
print(splitstr)
print('\n')

#grabbing substrings
x = splitstr[0]
y = splitstr[2]
z = splitstr[4]

#Confirming grabbed substrings
print('Confirming Substrings')
print(x)
print(y)
print(z)
print('\n')

#Conversion to Integer
x = int(x)
y = int(y, base=16)
z = int(z, 2)

#Confirming Int values
print('Int Converted')
print(x)
print(y)
print(z)

#Calculation
xyz = x + y - z

#Results
print('\n')
print('Calculated')
print(xyz)

"""
