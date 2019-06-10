"""This module handle data states and return code from Tellos in the swarm
"""
import socket
import threading
import queue


class ServerStatesTello():
    """This Class handle response from Tellos and states messages
    """
    def __init__(self):
        self.local_address = ('', 8890)
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_server.setblocking(False)
        self.socket_server.settimeout(5.0)
        self.last_message = str()
        self.last_ip = int()
        self.thread_running = False

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

    def _thread_listen_tello(self, state_queue=queue.Queue()):
        """This function listen to the port and put data in the Queue (state messages)
        """
        while self.thread_running:
            try:
                data, ip = self.socket_server.recvfrom(3000)
            except socket.error as error:
                print("Error on socket, Error code : {} | Message : {}".format(error[0], error[1]))
            else:
                self.last_message = data.decode(encoding="utf-8")
                self.last_ip = ip.decode(encoding="utf-8")
                state_queue.put((self.last_ip, self.last_message))

    def launch_activity(self, state_queue=queue.Queue()):
        """This function bind port and launch the thread
        """
        self.bind()
        self.thread_running = True
        self.state_thread = threading.Thread(target=self._thread_listen_tello, args=(state_queue,), daemon=True)
        self.state_thread.start()

    def end_ativity(self):
        """This function close socket and stop the thread
        """
        self.thread_running = False
        self.close()
