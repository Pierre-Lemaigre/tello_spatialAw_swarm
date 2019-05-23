"""This module search for Tello connection on the local network (192.168.1.1-254 addresses)
"""
from subprocess import check_output, STDOUT, TimeoutExpired, CalledProcessError
import socket

local_address = ('', 9010)
tello_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_socket.setblocking(0)
tello_socket.settimeout(5.0)
tello_socket.bind(local_address)


def search_for_tello(host):
    """This function ping the given addresse (host from ipaddress module)
    If ping successful, it try to reach the device by sending command,
    If response is ok, device is Tello, else device is something else.
    """
    res = "NTH"
    str_host = str(host)
    num = int(str_host.split('.')[3])
    print("scanning : {}".format(host))
    try:
        check_output(['fping', '-c', '1', '-t', '300', str_host], stderr=STDOUT)
    except TimeoutExpired:
        res = (str_host, "DNAT")
    except CalledProcessError:
        res = (str_host, "NHA")
    else:
        tello_address = (str_host, 8889)
        tello_socket.sendto("command".encode(encoding="utf-8"), tello_address)
        try:
            response, ip_tello = tello_socket.recvfrom(1518)
        except socket.timeout:
            res = (str_host, "DNRT")
        else:
            if response.decode(encoding="utf-8") == 'ok':
                res = (str_host, 50000+num)
            else:
                res = (str_host, "TDCC")
    return res


def keep_drone_alive(tello_drone):
    """Tello drone fall asleep if during 15s they didn't receive a command
    This function "ping" the drone and act according to the response (notify programm if drone down)
    Also i'm using this function to check on battery level, so if battery to low, drone down to.
    """
