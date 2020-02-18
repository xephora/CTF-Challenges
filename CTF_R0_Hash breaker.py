#!/usr/bin/env python
import requests
import hashlib
import urllib2
import re
from lxml import html
import binascii

#Challenge Information
#https://ringzer0ctf.com/challenges/56

#cookie storage
session_name = 'PHPSESSID'
session_value = '<CookieValue>'

#cookie session
session = requests.Session()
jar = requests.cookies.RequestsCookieJar()
jar.set(session_name, session_value)
session.cookies = jar

#request session
inspected_webpage = session.get('https://ringzer0ctf.com/challenges/56/')

#pull webcontent
tree = html.fromstring(inspected_webpage.content)

#scrape everything from class "message"
export_html = tree.xpath('string(//div[@class="message"])')
#Grab message of binary data

#remove spaces and dashes
export_rsad = re.sub("[^a-zA-Z0-9]", "", export_html)

#removing specific words (WORKS BUT REDUNDANT AND SLOPPY!!)
export_rbm = re.sub("BEGINHASH", "", export_rsad)
export_rbem = re.sub("ENDHASH", "", export_rbm)

print(export_rbem)