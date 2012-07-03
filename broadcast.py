#!/usr/bin/env python
from ZeroconfService import ZeroconfService
import time
import json
import re
import sys
import random

## Configuration (eventually I'd like to parse the cjdroute.conf file and just pull this all out of there)
name = None 					# A public name for your node - shown to potential peers
ip = None                   	# Your cjdns public IP - shown to potential peers
adminPassword = None	        # Admin cjdns password
adminPort = 11234				# Port that cjdns admin interface is listening on
port = 10000					# Port cjdns is listening on
import_path = "/opt/cjdns/contrib/python"	# path to the latest cjdns python libraries
public_key = None           	# Your public key
#######

def generatepass():
    letters = "1234567890abcdefghijklmnopqrstuvwxyz"
    length = 20
    out = ""
    while len(out) <= length:
        out += letters[random.randint(0,len(letters)-1)]
    return out


password = generatepass()

print "Using password " + password

sys.path.append(import_path)
from cjdns import cjdns_connect
cjdns = cjdns_connect("127.0.0.1", adminPort, adminPassword)
addpass = cjdns.AuthorizedPasswords_add(password)
if addpass["error"] != "none":
    print "Adding password failed!"
    sys.exit()

service = ZeroconfService(name="Hyperboria", port=port,  stype="_cjdns._udp", text=["password=" + password, "key=" + public_key,"name=" + name,"cjdnsip=" + ip])
service.publish()
print "Service published!"
raw_input("Press enter to stop broadcasting")
print "Unpublishing service..."
service.unpublish()
