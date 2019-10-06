import subprocess
import json

def main():
    with open("ip_info.txt", "r") as f:
        info = json.loads(f.read())

    for i in info:
        cmd = "jexec {0} python3.7 /fika/core.py {0}".format(i)
        subprocess.Popen(cmd.split())
