import re
import subprocess

from shcommand import *

class Equipment:
    def __init__(self, jailname):
        self.name = jailname
        arg = "jls host.hostname".split()
        check_list = subprocess.check_output(arg).decode("utf-8").split()
        if jailname not in check_list:
            jailc(jailname)
            mt_devfs(jailname)
            mt_nullfs(jailname)
            jexec(jailname, "ifconfig lo0 127.0.0.1/24 up")
            jexec(jailname, "ipfw add allow ip from any to any")

    def destroy(self):
        print("destroy {0}".format(self.name))
        jname = self.name
        #
        arg = "jexec {0} ifconfig -l".format(jname).split()
        ifnames = subprocess.check_output(arg).decode("utf-8").split()
        #
        epairs = [i for i in ifnames if re.match("epair.*", i)]
        for epair in epairs:
            ifconfig("{0} -vnet {1}".format(epair, jname))
            ifconfig("{0} destroy".format(epair))
        bridges = [j for j in ifnames if re.match("vbridge.*", j)]
        for bridge in bridges:
            ifconfig("{0} -vnet {1}".format(bridge, jname))
            ifconfig("{0} destroy".format(bridge))
        print("do umount_nullfs {0}".format(jname))
        umt_nullfs(jname)
        print("done umount_nullfs {0}".format(jname))
        arg = "jail -r {0}".format(jname).split()
        subprocess.run(arg)
        print("do umount_devfs {0}".format(jname))
        umt_devfs(jname)
        print("done umount_devfs {0}".format(jname))

    def connect(self, epair):
        name = self.name
        ifconfig("{0} vnet {1}".format(epair, name))

    def disconnect(self, epair):
        name = self.name
        ifconfig("{0} -vnet {1}".format(epair, name))

    def assignip(self, epair, ip, mask):
        name = self.name
        jexec(name, "ifconfig {0} inet {1} netmask {2}".format(epair, ip, mask))

    def assigngw(self, gw):
        name = self.name
        jexec(name,"route add default {0}".format(gw))

    def up(self, epair):
        name = self.name
        jexec(name, "ifconfig {0} up".format(epair))

    def down(self, epair):
        name = self.name
        jexec(name, "ifconfig {0} down".format(epair))

    def start(self, program):
        name = self.name
        jexec(name, "/usr/local/etc/rc.d/{0} start".format(program))

class Router(Equipment):
    def __init__(self, jailname):
        super().__init__(jailname)
        subprocess.run("cp routing/bgp_sample.conf routing/{0}.conf".format(jailname).split())
        jexec(jailname, "sysctl -w net.inet.ip.forwarding=1")

    # Router setting 'AS' is AS number, 'network' is network address this router managing, 'neighbor' is dict consisted with neighbor AS number and IP address
    def register(self, AS, network, neighbor):
        with open("routing/{0}.conf".format(self.name), "a") as f:
            f.write("router bgp {0}\n".format(AS))
            f.write(" network {0}\n".format(network))
            f.write(" redistribute connected\n")
            for i, j in neighbor.items():
                f.write(" neighbor {0} remote-as {1}\n".format(i, j))
            f.write("log stdout\n")
        arg = "mv routing/{0}.conf /jails/{0}/usr/local/etc/quagga/bgpd.conf".format(self.name).split()
        subprocess.run(arg)

class Bridge(Equipment):
    def __init__(self, jailname):
        super().__init__(jailname)
        arg = "ifconfig bridge create".split()
        bridgename = subprocess.check_output(arg).decode()
        ifconfig("{0} vnet {1}".format(bridgename, jailname))
        jexec(jailname, "ifconfig {0} name vbridge0".format(bridgename))
        jexec(jailname, "ifconfig vbridge0 up")

    def connect(self, epair):
        ifconfig("{0} vnet {1}".format(epair, self.name))
        jexec(self.name, "ifconfig vbridge0 addm {0}".format(epair))

    def assignip(self, ip, mask):
        jexec(self.name, "ifconfig vbridge0 inet {0} netmask {1}".format(ip, mask))
