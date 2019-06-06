"""This module handle return code from Tellos in the swarm
"""
import socket
import threading


class server_tello():
    """This Class handle response from Tellos and states messages
    """
    def __init__(self):
        self.local_address = ('', 8890)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.setblocking(False)
        self.socket_server.settimeout(5.0)
        self.last_message = str()

    def bind(self):
        """This function is a wrapper around binding socket
        """
        try:
            self.socket_server.bind(self.local_address)
        except socket.error as error:
            print("Bind failed. Error Code : {} | Message : {}".format(error[0], error[1]))

    def close(self):
        """Close the socket binded
        """
        self.socket_server.close()

    def _thread_listen_tello(self):
        pass