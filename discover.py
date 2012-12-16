#! /usr/bin/env python
import sys
import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
import PyZenity
import os
import json

TYPE = '_cjdns._udp'

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

def service_resolved(*args):
    record = {"hostname": str(args[5]),"ip": str(args[7]), "port": str(args[8])}
    for a in args[9]:
        current_record = ""
        for b in a:
            current_record += str(b)
        key,value = current_record.split("=")
        record[key] = value
    print "Discovered peer " + record['hostname'] + " (" + record['ip'] + ") on port " + record['port']

    if public_key != record["key"]:     # Make sure we're not adding ourself
        if autoadd:
            addPeer(record)
        elif PyZenity.Question("Would you like to add " + record["name"] + " (" + record["ip"] + ":" + record["port"] +") as a peer on CJDNS?"):
            addPeer(record)
        else:
            print "Not adding peer"
    else:
        print "Discovered ourself. Ignoring..."


def addPeer(record):
    print "Adding peer..."
    sys.path.append(import_path)
    from cjdns import cjdns_connect
    cjdns = cjdns_connect("127.0.0.1", adminPort, adminPassword)
    cjdns.UDPInterface_beginConnection(record["key"],record["ip"] + ":" + record["port"],0,record["password"])

def print_error(*args):
    print 'error_handler'
    print args[0]
    
def myhandler(interface, protocol, name, stype, domain, flags):
    if flags & avahi.LOOKUP_RESULT_LOCAL:
            # local service, skip
            pass

    server.ResolveService(interface, protocol, name, stype, 
        domain, avahi.PROTO_UNSPEC, dbus.UInt32(0), 
        reply_handler=service_resolved, error_handler=print_error)

loop = DBusGMainLoop()

bus = dbus.SystemBus(mainloop=loop)

server = dbus.Interface( bus.get_object(avahi.DBUS_NAME, '/'),
        'org.freedesktop.Avahi.Server')

sbrowser = dbus.Interface(bus.get_object(avahi.DBUS_NAME,
        server.ServiceBrowserNew(avahi.IF_UNSPEC,
            avahi.PROTO_UNSPEC, TYPE, 'local', dbus.UInt32(0))),
        avahi.DBUS_INTERFACE_SERVICE_BROWSER)

sbrowser.connect_to_signal("ItemNew", myhandler)

gobject.MainLoop().run()
