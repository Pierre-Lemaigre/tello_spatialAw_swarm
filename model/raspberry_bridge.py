"""This module is the server/client that transform UDP network messages in TCP messages
"""
from socket import socket
from threading import Thread
from queue import Queue
import time
import sys
import re


class BridgeRaspberry():
    """This Class handle response from Tellos and states messages
    """
    def __init__(self, server_ip, server_port=9000):
        self.states_queue = Queue()

        self.local_address = ('', 8890)
        self.socket_udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_udp_server.setblocking(False)
        self.socket_udp_server.settimeout(5.0)
        self.udp_thread_running = False

        self.tcp_server_address = (server_ip, server_port)
        self.socket_tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_thread_running = False

    def socket_upd_binding(self):
        """This function is a wrapper around binding socket
        """
        try:
            self.socket_udp_server.bind(self.local_address)
        except socket.error as error:
            sys.exit("Bind failed. Error Code : {} | Message : {}".format(error[0], error[1]))

    def socket_tcp_connecting(self):
        """This function is a wrapper around connecting
        """
        try:
            self.socket_tcp_client.connect(self.tcp_server_address)
        except socket.error as error:
            sys.exit("Connection failed. Error Code : {} | Message : {}".format(error[0], error[1]))

    def _thread_listen_tello(self):
        """This function listen to the port and put data in the Queue (state messages)
        """
        while self.udp_thread_running:
            try:
                data, ip = self.socket_udp_server.recvfrom(3000)
            except socket.error as error:
                print("Error on socket, Error code : {} | Message : {}".format(error[0], error[1]))
            else:
                self.last_message = data.decode(encoding="utf-8")
                print("Message tello in UDP server from : {}".format(ip))
                self.states_queue.put(self.last_message)
            time.sleep(0.2)

    def _thread_client_tcp(self):
        """This function convert message to TCP communications with main server (state messages)
        """
        while self.tcp_thread_running:
            states_data = self.states_queue.get()
            self.socket_tcp_client.sendall(states_data.encode(encoding="utf-8"))
            print("Message sended to TCP server !")
            time.sleep(0.1)

    def launch_bridge(self):
        """This function bind ports and launch threads
        """
        self.socket_tcp_connecting()
        self.socket_upd_binding()

        self.udp_thread_running = True
        self.udp_state_thread = Thread(target=self._thread_listen_tello, daemon=True)
        self.udp_state_thread.start()

        self.tcp_thread_running = True
        self.tcp_state_thread = Thread(target=self._thread_client_tcp, daemon=True)
        self.tcp_state_thread.start()

    def __del__(self):
        """This function close socket and stop the thread
        """
        self.udp_thread_running = False
        self.udp_state_thread.join()
        self.socket_udp_server.close()

        self.tcp_thread_running = False
        self.tcp_state_thread.join()
        self.socket_tcp_client.close()


if __name__ == "__main__":
    regex = r"^((\d|1\d{1,2}|2[0-4]\d|25[0-5])\.){3}(\d|1\d{1,2}|2[0-4]\d|25[0-5])$"
    if len(sys.argv) >= 2 and re.match(regex, str(sys.argv[1])):
        network_address = sys.argv[1]
    bridge = BridgeRaspberry(network_address)
    bridge.launch_bridge()
