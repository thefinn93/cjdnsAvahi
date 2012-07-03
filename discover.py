import dbus, gobject, avahi
from dbus import DBusException
from dbus.mainloop.glib import DBusGMainLoop

# Looks for iTunes shares

TYPE = '_cjdns._udp'

def service_resolved(*args):
    record = {"hostname": str(args[5]),"ip": str(args[7]), "port": int(args[8])}
    for a in args[9]:
        current_record = ""
        for b in a:
            current_record += str(b)
        key,value = current_record.split("=")
        record[key] = value
    print record

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
