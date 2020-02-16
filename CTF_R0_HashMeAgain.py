#!/usr/bin/env python
import requests
import hashlib
import webbrowser
import urllib2
import re
from bs4 import BeautifulSoup
from lxml import html

#Challenge Information
#https://ringzer0ctf.com/challenges/14

#cookie storage
session_name = 'INSERTCOOKIENAMEHERE'
session_value = 'INSERTCOOKIEVALUE'

#cookie session
session = requests.Session()
jar = requests.cookies.RequestsCookieJar()
jar.set(session_name, session_value)
session.cookies = jar

#request session
inspected_webpage = session.get('https://ringzer0ctf.com/challenges/14/')

#pull webcontent
tree = html.fromstring(inspected_webpage.content)

#scrape everything from class "message"
export_html = tree.xpath('string(//div[@class="message"])')
#Grab message of binary data

#convery binary string into ASCII
n = int(export_html, 2)
n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()
#Q&A Converting binary to ASCII
#https://stackoverflow.com/questions/7396849/convert-binary-to-ascii-and-vice-versa#7397689

#Encrypt message sha512
enc_message = hashlib.sha512()
enc_output = enc_message.hexdigest()

new_inspected_webpage = session.get('https://ringzer0ctf.com/challenges/14/'+enc_output

final_results = re.findall(r"FLAG.{0,30}", new_inspected_webpage.text)
print(final_results)






