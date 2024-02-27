from os import popen
from platform import system
from socket import gethostname, gethostbyname

from ego.utils.shcmd import executable


def get_host_by_ipa():
    if system().lower() == "windows":
        for ip_info in popen("route print").readlines():
            if " 0.0.0.0 " in ip_info:
                return ip_info.split()[-2]

    command = "ip a"
    command = f"{command} | grep -E \"inet [0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+\""
    command = f"{command} | grep -Ev \"[0-9]+\\.[0-9]+\\.[0-9]+\\.1/\""
    command = f"{command} | awk -F \"[/ ]+\" '{{print $3}}'"

    response = executable.execute_commands(command=command)
    ip = ""
    for line in response.stdout:
        ip = line.decode("utf-8").strip()

    return ip


def get_host_by_ifconfig():
    if system().lower() == "windows":
        for ip_info in popen("route print").readlines():
            if " 0.0.0.0 " in ip_info:
                return ip_info.split()[-2]

    command = "ifconfig"
    command = f"{command} | grep -E \"inet [0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+\""
    command = f"{command} | grep -Ev \"[0-9]+\\.[0-9]+\\.[0-9]+\\.1/\""
    command = f"{command} | grep -v \"127\\.0\\.0\\.1\""
    command = f"{command} | awk -F \"[/ ]+\" '{{print $3}}'"

    response = executable.execute_commands(command=command)
    ip = ""
    for line in response.stdout:
        ip = line.decode("utf-8").strip()

    return ip


def queryhostname():
    return gethostname()


def queryhost():
    return gethostbyname(gethostname())


def check_ip_v4(ip):
    address = []
    for add in ip.split("."):
        address.append(int(add))

    if len(address) != 4:
        return False

    if address[0] < 1 or address[0] > 254:
        return False

    if address[1] < 0 or address[1] > 255:
        return False

    if address[2] < 0 or address[2] > 255:
        return False

    if address[3] < 2 or address[2] > 254:
        return False

    return True
