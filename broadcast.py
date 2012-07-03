#!/usr/bin/env python
from ZeroconfService import ZeroconfService
import time
import json
import re
import sys
import random
import ConfigParser

parser=ConfigParser.SafeConfigParser()
parser.read(['config.ini'])
name = parser.get('cjdns','name')
ip = parser.get('cjdns','cjdnsIP')
adminPassword = parser.get('cjdns','adminPassword')
adminPort = parser.getint('cjdns','adminPort')
port = parser.getint('cjdns','peeringPort')
import_path = parser.get('cjdns','importPath')
public_key = parser.get('cjdns','publicKey')

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

service = ZeroconfService(name="Hyperboria Peer " + name, port=port,  stype="_cjdns._udp", text=["password=" + password, "key=" + public_key,"name=" + name,"cjdnsip=" + ip])
service.publish()
print "Service published!"
raw_input("Press enter to stop broadcasting")
print "Unpublishing service..."
service.unpublish()
