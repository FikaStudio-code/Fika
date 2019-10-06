# coding: utf-8

import json
import subprocess
import re
from shcommand import *
from equipment import *

class Operator:
    def __init__(self):
        self.daicho = dict()
        num = 0
        self.epair_num = num
        print("I'll do your job")

    def createpair(self):
        num = 0
        arg = "ifconfig epair create".split()
        output = subprocess.check_output(arg).decode("utf-8").split()
        output = [i for i in output if re.match("epair\d+a", i)][0]
        num = output.replace("epair", "").replace("a", "")
        ifconfig("epair{0}a link 02:c0:e4:00:{0}:0a".format(num))
        ifconfig("epair{0}b link 02:c0:e4:00:{0}:0b".format(num))
        self.num = num
        return "epair{0}a".format(num), "epair{0}b".format(num)

    def destroypair(epair):
        if re.match("epair\d+[ab]", epair) != False:
            epair = epair[:-1]
        ifconfig("{0}a destroy".format(epair))
        del self.daicho["{0}a".format(epair)]
        del self.daicho["{0}b".format(epair)]

    def register(self, epair, jailname, ip4 = None, mask = None, AS = None, ip6 = None, prefixlen = None):
        self.daicho[epair] = [jailname, ip4, mask, AS, ip6, prefixlen]

    def unregister(self, epair):
        del self.daicho[epair]

    def find(self, epair):
        return self.daicho[epair]

    def setupnode(self, jailname):
        exec("{0} = Equipment('{0}')".format(jailname),  globals())
        print("Setup node {0} done!".format(jailname))

    def setuprouter(self, jailname):
        exec("{0} = Router('{0}')".format(jailname), globals())
        print("Setup Router {0} done!".format(jailname))

    def setupbridge(self, jailname):
        exec("{0} = Bridge('{0}')".format(jailname), globals())

    def connect(self, obj, epair):
        exec("{0}.connect('{1}')".format(obj, epair))
        print("{0} is connected to {1}".format(epair, obj))

    def assignip(self, obj, epair, ip, mask, AS = None):
        exec("{0}.assignip('{1}', '{2}', '{3}')".format(obj, epair, ip, mask))
        print("{0} of {1} has {2}/{3}".format(epair, obj, ip, mask))

    def assigngw(self, obj, gw):
        exec("{0}.assigngw('{1}')".format(obj, gw))
        print("assign {0} as gateway of {1}".format(gw, obj))

    def up(self, obj, epair):
        exec("{0}.up('{1}')".format(obj, epair))
        print("{0} up".format(epair))

    def down(self, obj, epair):
        exec("{0}.down('{1}')".format(obj, epair))
        print("{0} down".format(epair))

    def start(self, obj, program):
        exec("{0}.start('{1}')".format(obj, program))
        print("{0} start {1}".format(obj, program))
