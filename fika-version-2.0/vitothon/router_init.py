#!/usr/local/bin/python3.7

import subprocess
import sys

name = sys.argv[-1]
conf_list = ["bgpd", "ospfd", "ripd", "zebra", "vtysh"]

for i in conf_list:
    cmd = "cp /jails/{0}/usr/local/share/examples/quagga/{1}.conf.sample /jails/{0}/usr/local/etc/quagga/{1}.conf".format(name, i)
    subprocess.run(cmd.split())

# rc.conf edit!!!
with open("/jails/{0}/etc/rc.conf".format(name), "a") as f:
    f.write('quagga_enable="YES"\n')
    f.write('quagga_daemons="zebra bgpd ospfd"\n')
