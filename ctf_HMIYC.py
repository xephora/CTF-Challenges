import requests
import hashlib
import webbrowser
import urllib2
from bs4 import BeautifulSoup

inspected_webpage = 'https://ringzer0ctf.com/challenges/13/'
export_html = urllib2.urlopen(inspected_webpage)
parse_html = BeautifulSoup(export_html, 'html.parser')
scrape_process = parse_html.find('br', attrs={'class': 'message'})
hashinput = scrape_process.text.strip()
hash_process = hashlib.sha512(hashinput)
hashoutput = hash_process.hexdigest()

url = "https://ringzer0ctf.com/challenges/13/"+hashoutput

webbrowser.open(url)