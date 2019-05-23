"""This Module is a swarm creation around Tello class
This is used to recognize Tello connected to the Asus box
"""
import multiprocessing as mp
from ipaddress import ip_network
from network import search_for_tello
from tello import Tello
import sys


def construct_tello(tello_swarm):
    tello_construct = list()
    white_addresses = list()
    if isinstance(tello_swarm, list):
        for ip_address, state in tello_swarm:
            if isinstance(state, int):
                tello_construct.append(Tello(local_port=state, tello_ip=ip_address))
            else:
                white_addresses.append((ip_address, state))
    return tello_construct, white_addresses


def main(tello_address_checked):
    """Main function of the programm
    Normally useless in python to do this, but multiprocessing librairie
    put restrictions
    """
    drones, blank_ip_addresses = construct_tello(tello_address_checked)
    tello_drones = dict()
    for tello in drones:
        tello_drones[tello.tello_adr[0]] = [tello, ]


if __name__ == "__main__":
    tello_address_checked = list()
    network = ip_network('192.168.1.0/24')
    if len(sys.argv) >= 2:
        network = ip_network(sys.argv[1])
    pool = mp.Pool(mp.cpu_count()*8)
    tello_address_checked = pool.map(func=search_for_tello, iterable=network.hosts())
    print(tello_address_checked)
