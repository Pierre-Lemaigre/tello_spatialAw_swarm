'''This module search for Tello connection on the local network (192.168.1.1-254 addresses)
'''
from subprocess import check_output, STDOUT, TimeoutExpired, CalledProcessError
import socket

local_address = ('', 9010)
tello_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_socket.settimeout(2)
tello_socket.bind(local_address)


def search_for_tello(host):
    '''This function ping the given addresse (host from ipaddress module)
    If ping successful, it try to reach the device by sending command,
    If response is ok, device is Tello, else device is something else.
    '''
    res = "NTH"
    str_host = str(host)
    num = int(str_host.split('.')[3])
    try:
        check_output(['ping', '-c', '1', '-W', '1', str_host], stderr=STDOUT)
    except TimeoutExpired:
        res = [str_host, "DNAT"]
    except CalledProcessError:
        res = [str_host, "NHA"]
    else:
        tello_address = (str_host, 8889)
        tello_socket.sendto("command".encode(encoding="utf-8"), tello_address)
        try:
            response, ip_tello = tello_socket.recvfrom(128)
        except socket.timeout:
            res = [str_host, "DNRET"]
        else:
            if response.decode(encoding='utf-8') == 'ok':
                res = [str_host, 5000+num]
            else:
                res = [str_host, "TDCC"]
    return res
