"""This module handle data states and return code from Tellos in the swarm
"""
import socket
from queue import Queue
from threading import Thread
import sys
import time


class TcpServer_state():
    """This Class handle request from raspberrys
    """
    def __init__(self, port=9000, host='localhost'):
        self.states_queue = Queue()
        self.local_address = (host, port)
        self.socket_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.tcp_thread_running = False
        self.client_threads = []

    def socket_tcp_binding(self):
        """Wrapper around binding socket
        """
        try:
            self.socket_tcp_server.bind(self.local_address)
        except socket.error as error:
            sys.exit("Bind failed. Error code : {} | Message : {}".format(error[0], error[1]))

    def _thread_listen_port(self):
        """Listen to the 9000 port, open connection with each raspberry and create an instance for each connection (new thread for each connection)
        """
        self.socket_tcp_server.listen()
        while self.tcp_thread_running:
            conn, addr = self.socket_tcp_server.accept()
            client_thread = Thread(target=self._thread_listen_client, daemon=True, args=(conn, ))
            client_thread.start()
            self.client_threads.append(client_thread)

    def _thread_listen_client(self, conn):
        """Listen to one raspberry and put message in queue
        """
        while True:
            data = conn.recv(3000)
            self.states_queue.put(data.decode("utf-8"))
            time.sleep(0.1)
