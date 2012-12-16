#!/usr/bin/env python
from ZeroconfService import ZeroconfService
import sys
import random
import ConfigParser

try:
    config = json.load(open(os.getenv("HOME") + '/.cjdnsadmin'))
except TypeError:
    print "Failed to load " + os.getenv("HOME") + "/.cjdnsadmin"
    print "Are it teh valid JSONz?"
    sys.exit(1)
except IOError:
    print "Failed to load " + os.getenv("HOME") + "/.cjdnsadmin"
    print "Maybe it doesn't exist?"
    sys.exit(1)
    
validconfig = True

try:
    name = config['name']
except KeyError:
    print "Name not defined in the config. Please name your node"
    validconfig = False
    
try:
    ip = config['ip']
except KeyError:
    print "IP not defined in the config. Please tell us your CJDNS IP"
    validconfig = False
    
try:
    adminPassword = config['password']
except KeyError:
    print "Admin password not defined in the config. What kinda ass backwards operation are you running?"
    validconfig = False

try:
    adminPort = config['port']
except KeyError:
    print "Admin connection port not defined in the config. Try 11234"
    validconfig = False

try:
    importpath = config['importPath']
    sys.path.append(importpath)
except KeyError:
    print "Import path not defined in the config. Assuming the cjdns python library is in the default path"
    
try:
    public_key = config['publicKey']
except KeyError:
    print "publicKey not defined in config"
    validconfig = False

try:
    autoadd = config['autoadd']
except KeyError:
    print "autoadd not defined, setting it to false"
    autoadd = False
    
if not validconfig:
    sys.exit(1)


def generatepass():
    letters = "1234567890abcdefghijklmnopqrstuvwxyz"
    length = 20
    out = ""
    while len(out) <= length:
        out += letters[random.randint(0, len(letters) - 1)]
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

service = ZeroconfService(name="Hyperboria Peer " + name, port=port, stype="_cjdns._udp",
    text=["password=" + password, "key=" + public_key, "name=" + name, "cjdnsip=" + ip])

service.publish()
print "Service published!"
raw_input("Press enter to stop broadcasting")
print "Unpublishing service..."
service.unpublish()
