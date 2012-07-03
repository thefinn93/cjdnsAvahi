#! /usr/bin/env python
import sys
import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop


TYPE = '_cjdns._udp'


## Configuration (eventually I'd like to parse the cjdroute.conf file and just pull this all out of there)
adminPassword = "super_secure_password" # Admin cjdns password
adminPort = 11234 # Port that cjdns admin interface is listening on
port = 10000 # Port cjdns is listening on
import_path = "/opt/cjdns/contrib/python" # path to the latest cjdns python libraries
#######

def service_resolved(*args):
    record = {"hostname": str(args[5]),"ip": str(args[7]), "port": str(args[8])}
    for a in args[9]:
        current_record = ""
        for b in a:
            current_record += str(b)
        key,value = current_record.split("=")
        record[key] = value
    print "Discovered peer " + record['hostname'] + " (" + record['ip'] + ") on port " + record['port'] + ". Connecting..."
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
