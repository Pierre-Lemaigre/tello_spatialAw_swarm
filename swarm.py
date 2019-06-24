"""This module is the controller of the application, use
model classes and functions and interact with the view
"""
from model.network import construct_network, construct_tello
from model.server_tellos import Server_state_tello
from os import sys
import re
import queue


def live_list_reload(drones=dict(), state_queue=queue.Queue()):
    while not state_queue.empty():
        state_tuple = state_queue.get()
        drones[state_tuple[0]] = 2


def main(network_address):
    tested_ip_addresses = construct_network()
    drones, blank_ip_addresses = construct_tello(tested_ip_addresses)
    drones_states_queue = queue.Queue()
    state_serveur = Server_state_tello()
    state_serveur.launch_activity(state_queue=drones_states_queue)


if __name__ == "__main__":
    regex = r"^((\d|1\d{1,2}|2[0-4]\d|25[0-5])\.){3}(\d|1\d{1,2}|2[0-4]\d|25[0-5])$"
    if len(sys.argv) >= 2 and re.match(regex, str(sys.argv[1])):
        network_address = sys.argv[1]
        main(network_address)
    else:
        exit("Error, network addresses not valid")
