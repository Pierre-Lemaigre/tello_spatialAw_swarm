'''This Module is a swarm creation around Tello class
This is used to recognize Tello connected to the Asus box
'''
import multiprocessing as mp
from ipaddress import ip_network
from network import search_for_tello

tello_address_checked = list()

if __name__ == "__main__":
    network = ip_network('192.168.1.0/24')
    pool = mp.Pool(mp.cpu_count())
    tello_address_checked = pool.map(func=search_for_tello, iterable=network.hosts())

def construct_tello(tello_swarm):
    