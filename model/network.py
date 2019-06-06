"""This module search for Tello connection on the given network
"""
from subprocess import check_output, STDOUT, TimeoutExpired, CalledProcessError
import socket
import multiprocessing as mp
from ipaddress import ip_network

# Creation of a socket with some tweakings
local_address = ('', 9010)
tello_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
tello_socket.setblocking(False)
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


def construct_network(network_adress='192.168.1.0/24'):
    """This function use the multiprocessing librairy in order to make a
    faster build of the Tello drone list connected"""
    tello_address_checked = list()
    network_adress = ip_network(network_adress)
    pool = mp.Pool(mp.cpu_count()*8)
    tello_address_checked = pool.map(func=search_for_tello, iterable=network_adress.hosts())
    return tello_address_checked
