#!/usr/bin/env python
import requests
import hashlib
import urllib2
import re
from lxml import html
import binascii

#Challenge Information
#https://ringzer0ctf.com/challenges/14

#cookie storage
session_name = 'PHPSESSID'
session_value = '61dvtl8oesr30k2rauqvq0v6j3'

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

#remove spaces and dashes
export_rsad = re.sub("[^a-zA-Z0-9]", "", export_html)

#removing specific words (WORKS BUT REDUNDANT AND SLOPPY!!)
export_rbm = re.sub("BEGINMESSAGE", "", export_rsad)
export_rbem = re.sub("ENDMESSAGE", "", export_rbm)

#Convertion from integer to ASCII
n = int(export_rbem, 2)
binary_ascii = binascii.unhexlify('%x' % n)

#ASCII to Sha512
enc_message = hashlib.sha512(binary_ascii)
enc_output = enc_message.hexdigest()

updated_webpage = session.get('https://ringzer0ctf.com/challenges/14/'+enc_output)

#Extract the flag
final_results = re.findall(r"FLAG.{0,30}", updated_webpage.text)
print(final_results)
