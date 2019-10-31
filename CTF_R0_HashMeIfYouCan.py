#!/usr/bin/env python
import requests
import hashlib
import webbrowser
import urllib2
import re
from bs4 import BeautifulSoup
from lxml import html

#cookie storage
session_name = 'INSERTCOOKIENAMEHERE'
session_value = 'INSERTCOOKIEVALUE'

#cookie session
session = requests.Session()
jar = requests.cookies.RequestsCookieJar()
jar.set(session_name, session_value)
session.cookies = jar

#request session
inspected_webpage = session.get('https://ringzer0ctf.com/challenges/13/')

#pull webcontent
tree = html.fromstring(inspected_webpage.content)

#scrape everything from class "message"
export_html = tree.xpath('string(//div[@class="message"])')

#remove spaces and dashes
export_rsad = re.sub("[^a-zA-Z0-9]", "", export_html)

#removing specific words (WORKS BUT REDUNDANT AND SLOPPY!!)
export_rbm = re.sub("BEGINMESSAGE", "", export_rsad)
export_rbem = re.sub("ENDMESSAGE", "", export_rbm)

#using sha512 against cleaned message
hash_process = hashlib.sha512(export_rbem)
hashoutput = hash_process.hexdigest()

#get session and include the sha512 encrypted hash 
new_inspected_webpage = session.get('https://ringzer0ctf.com/challenges/13/'+hashoutput)

#scrape the flag from the session
final_results = re.findall(r"FLAG.{0,30}", new_inspected_webpage.text)

#show flag
print(final_results)







