cjdnsAvahi
==========

Automatically connect with cjdns peers on the LAN, courtesy of avahi/zeroconf.

Requirements:
==========
`python-avahi`

(i think that's all, please let me know if there's anything else)

Running
==========
Run `python broadcast.py` to broadcast the service. For the time being it will broadcast until the enter key or ctrl-c is pressed

Run `python discover.py` to discover peers on the LAN. It doesn't actually add them quite yet, but that's coming very soon.


Please note that this is still in development and probably wont work.
