#! /usr/bin/env python
import sys
import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop
import ConfigParser


TYPE = '_cjdns._udp'


parser=ConfigParser.SafeConfigParser()
parser.read(['config.ini'])
name = parser.get('cjdns','name')
ip = parser.get('cjdns','cjdnsIP')
adminPassword = parser.get('cjdns','adminPassword')
adminPort = parser.getint('cjdns','adminPort')
import_path = parser.get('cjdns','importPath')
public_key = parser.get('cjdns','publicKey')
autoadd = parser.getboolean('cjdns','autoaddPeers')

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
