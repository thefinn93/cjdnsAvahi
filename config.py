#! /usr/bin/env python
import json
import ConfigParser
import os.path
from json_minify import json_minify

configpath = raw_input("Where is your cjdroute.conf file? ")
parser=ConfigParser.SafeConfigParser()
parser.add_section("options")
parser.add_section("cjdns")

try:
    config = json.loads(json_minify(open(configpath).read()))
    parser.set("cjdns","adminpassword", config["admin"]["password"])
    parser.set("cjdns","adminport",config["admin"]["bind"].split(":")[1])
    parser.set("cjdns","cjdnsip",config["ipv6"])
    parser.set("cjdns","publicKey",config["publicKey"])
    parser.set("cjdns","peeringport",config["interfaces"]["UDPInterface"]["bind"].split(":")[1])
    print "CJDNS setting detected! Congrats, you just skipped most of the boring parts."
except:
    print "Failed to parse " + configpath + ". Are you sure it's proper JSON?"
    print "Hit ctrl-c to quit if you wanna try and re-type that. If it's just invalid JSON, edit the config file yourself."
    raw_input("Hit enter if you know it's bad JSON and just wanna config it manually (this will create a blankish config file)")
    parser.set("cjdns","adminpassword","")
    parser.set("cjdns","adminport","11234")
    parser.set("cjdns","cjdnsip","Your CJDNS IP address")
    parser.set("cjdns","publicKey","Your public key")
    parser.set("cjdns","peeringport","Port that CJDNS listens for connections from peers on")

importpath = raw_input("Where are the cjdns python libraries stored (hint: <cjdns git>/contrib/python): ")
name = raw_input("What is your machine's name? Displayed to people nearby: ")
autoaddpeers = str(raw_input("Would you like to automatically add peers you find nearby? [y/n] ") == "y")

parser.set("cjdns","importpath",importpath)
parser.set("options","name",name)
parser.set("options","autoAddPeers",autoaddpeers)

if os.path.isfile("config.ini"):
    raw_input("This will overwrite your existing config.ini - press enter to continue or ctrl-c to cancel")
parser.write(open("config.ini","wb"))
