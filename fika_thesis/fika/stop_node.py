import subprocess
import sys

check = subprocess.check_output("ps").decode()
check_list = check.split("\n")

for i in check_list:
    if "python3.7" in i.split():
        cmd = "kill -INT {0}".format(i.split()[0])
        subprocess.run(cmd.split())
