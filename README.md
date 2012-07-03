cjdnsAvahi
==========

Automatically connect with cjdns peers on the LAN, courtesy of avahi/zeroconf.

Requirements:
========
`python-avahi`

(i think that's all, please let me know if there's anything else)

Running
========
First rename `config.ini.example` to `config.ini`

Run `python broadcast.py` to broadcast the service. For the time being it will broadcast until the enter key or ctrl-c is pressed

Run `python discover.py` to discover peers on the LAN. Note that it will automatically add any peers found on the LAN at this point in time

Please note that this is still in development and probably wont work. You're on your own.

Future
========
Some ideas I've had, please feel free to submit pull requests for these or other features:

* GUI to display local peers
* Autohiding to the task bar
* Suggested by rainfly_x: [Notify when new peers are found via PyNotify](https://github.com/thefinn93/cjdnsAvahi/issues/1)
