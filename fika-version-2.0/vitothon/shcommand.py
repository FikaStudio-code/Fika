import subprocess

global jails
jails = '/jails'


#
# primitive command
#

def ifconfig(param):
    arg = param.split()
    arg.insert(0, "ifconfig")
    subprocess.run(arg)

def jexec(name, param):
    arg = param.split()
    arg.insert(0, name)
    arg.insert(0, "jexec")
    subprocess.run(arg)

def ifalias(interface, ip):
    arg = "ifconfig {0} alias {1}".format(interface, ip).split()
    subprocess.run(arg)

def jailc(name):
    arg = "jail -c vnet host.hostname={0} name={0} path={1}/{0} persist".format(name, jails).split()
    subprocess.run(arg)

def mt_devfs(path):
    arg = "mount -t devfs devfs {0}/{1}/dev".format(jails, path).split()
    subprocess.run(arg)

def umt_devfs(path):
    arg = "umount {0}/{1}/dev".format(jails, path).split()
    subprocess.run(arg)

def mt_nullfs(path):
    arg = "mount_nullfs {0}/basejail {0}/{1}/basejail".format(jails, path).split()
    subprocess.run(arg)


def umt_nullfs(path):
    arg = "umount {0}/{1}/basejail".format(jails, path).split()
    subprocess.run(arg)
