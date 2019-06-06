"""This module is the controller of the application, use
model classes and functions and interact with the view
"""
from model.tello import Tello
from model.network import construct_network
from os import sys
import re


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


def main(network_addresse):
    print("hello")
    sub_networks = construct_network()
    drones, blank_ip_addresses = construct_tello(sub_networks)


if __name__ == "__main__":
    regex = r"^((\d|1\d{1,2}|2[0-4]\d|25[0-5])\.){3}(\d|1\d{1,2}|2[0-4]\d|25[0-5])$"
    if len(sys.argv) >= 2 and (re.match(regex, str(sys.argv[1]))):
        network_addresse = sys.argv[1]
        main(network_addresse)
    else:
        exit("Error, network addresses not valid")
