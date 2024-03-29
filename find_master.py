#!/usr/bin/env python3

TEST = '''
Starting Nmap 7.60 ( https://nmap.org ) at 2019-06-13 13:26 CEST
Nmap scan report for raspberrypi-c8d4 (192.168.43.42)
Host is up (0.015s latency).

PORT     STATE  SERVICE
41278/tcp closed http-alt

Nmap scan report for nick1296-E6230-ce90 (192.168.43.182)
Host is up (0.0053s latency).

PORT     STATE SERVICE
41278/tcp open  http-alt

Nmap scan report for malweisse-6de6 (192.168.43.198)
Host is up (0.0010s latency).

PORT     STATE  SERVICE
41278/tcp closed http-alt

Nmap scan report for _gateway (192.168.43.238)
Host is up (0.0048s latency).

PORT     STATE  SERVICE
41278/tcp closed http-alt

Nmap done: 256 IP addresses (4 hosts up) scanned in 6.19 seconds
'''

import re
import os
import subprocess
import socket
import requests
import time
import feedback_db_helper
import json
import faces

SRV_PORT = 41278

def get_updates(ip):
    faces.restore()
    mt = faces.get_max_time()
    db = feedback_db_helper.FeedbackDBHelper()
    db.connect()
    mt = max(float(db.get_max_time()), mt)
    print(mt)
    
    r = requests.get("http://%s:%d/download_embeddings/%f" % (ip, SRV_PORT, mt))
    print(r.text)
    embs = json.loads(r.text)
    faces.bulk_add_b64(embs[0], embs[1])
    
    r = requests.get("http://%s:%d/download_feedbacks/%f" % (ip, SRV_PORT, mt))
    print(r.text)
    diff = json.loads(r.text)
    db.apply_diff(diff)
    db.close()

def get_lan_info():
    # get lan ip (works only with internet connection)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com", 80))
    lan_ip = s.getsockname()[0]
    s.close()
    # lan ip range (like 192.168.1.*)
    lan_range = lan_ip[:lan_ip.rfind(".") +1] + "0/24"
    # get gateway ip (assumed .1)
    #gateway_ip = lan_ip[:lan_ip.rfind(".") +1] + "1"
    return lan_range

while True:
    # The poor man master discovery
    r = subprocess.check_output(["nmap", "-p", str(SRV_PORT), get_lan_info()])
    r = str(r, "utf-8")

    rgx = re.compile("""Nmap scan report for .* \(([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)\)
Host is up .*\.

PORT[ ]+STATE SERVICE
""" + str(SRV_PORT) + """/tcp open  .*
""")

    #print(r)

    for ip in rgx.findall(r):
    #for ip in ["192.168.43.42"]:
        print("probing %s..." % ip)
        r = requests.get("http://%s:%d/i_am_the_master" % (ip, SRV_PORT))
        print(r,r.text)
        if r.text == "OK":
            print("master found")
            with open(os.path.expanduser("~/master_ip"), "w") as f:
                f.write(ip)
            
            get_updates(ip)
            
            exit(0)

    print("master not found, try again")
    time.sleep(1)

