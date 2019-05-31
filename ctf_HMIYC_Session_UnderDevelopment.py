import requests
import hashlib
import webbrowser
import urllib2
from bs4 import BeautifulSoup
from lxml import html


session_name = 'PHPSESSID'
session_value = 'qii68gf760646req2fcgmtq195'

session = requests.Session()
jar = requests.cookies.RequestsCookieJar()
jar.set(session_name, session_value)
session.cookies = jar

inspected_webpage = session.get('https://ringzer0ctf.com/challenges/13/')

tree = html.fromstring(inspected_webpage.content)
export_html = tree.xpath('string(//div[@class="message"])')

print export_html

#hash_process = hashlib.sha512(export_html)
#hashoutput = hash_process.hexdigest()

#url = "https://ringzer0ctf.com/challenges/13/"+hashoutput
#webbrowser.open(url)

#-print(hashoutput)
#export_html = tree.xpath('string(//div[@class="message"])')
#-export_html = tree.xpath('//div[@class="message"]/text()')
#-export_html = tree.xpath('//div[@class="message"]r/n/t/t/r/n/t/t/text()')
#-parse_html = BeautifulSoup(inspected_webpage, 'html.parser')
#-export_html = urllib2.urlopen(inspected_webpage)
#-parse_html = BeautifulSoup(inspected_webpage, 'html.parser')
#-print export_html





