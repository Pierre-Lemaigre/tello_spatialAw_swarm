"""
This module is a class wrapper
for the Tello drone
It implements connection and communication class with the drone

This module is inspired on the code of : hanker-lu
Code is available there : https://github.com/dji-sdk/Tello-Python/blob/master/Tello_Video/tello.py
The original code is in python 2.7 (So conversion to 3.7 by me)
"""
import socket
from direction import Direction, Clockwise


class Tello:
    '''Class wrapper around Tello communications
    '''
    def __init__(self, local_ip='', local_port=9000, tello_ip='192.168.10.1', tello_port=8889):
        '''
        Initialize Tello class : bind tello command and state sockets.

         :param local_ip: Local IP adress to bind. '' by default.
         :param local_port: Local IP adress to bind. (8890 by default)
         :param tello_ip: Tello IP.
         :param tello_port: Tello port.
         :type local_ip: str
         :type local_port: int
         :type tello_ip: str
         :type tello_port: str
        '''
        # Initilization of some parameters usefull for the future
        self.tello_adr = (tello_ip, tello_port)

        # Creation of the socket to send commands to the Tello drone
        self.socket_command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_command.bind((local_ip, local_port))

    def __del__(self):
        '''Destructor of the class
        Close the socket in order to avoid bug
        '''
        self.socket_command.close()

    def __str__(self):
        '''Representation of the Tello object
        :return: Representation of the object
        :rtype: str
        '''
        return "Adresse Tello {}, Socket du Tello : {}".format(self.tello_adr[0], self.socket_command)

    def send_command(self, command='command'):
        '''
        Send command to the Tello and wait for response

        :param command: Command to send. (Default_value'Command')
        :type command: String
        '''
        try:
            command_encoded = command.encode(encoding='utf-8')
        except UnicodeError:
            print('Error while converting Command : {}'.format(command))
        else:
            self.socket_command.sendto(command_encoded, self.tello_adr)

    def takeoff(self):
        '''Initiate the flight of the drone
        '''
        self.send_command('takeoff')

    def land(self):
        '''Land the drone automaticaly
        '''
        self.send_command('land')

    def emergency(self):
        '''In case of emergency, stop motors imediately
        '''
        self.send_command('emergency')

    def move_to(self, direction=Direction.DOWN, distance='20'):
        '''Command the drone to move in 3Dimensions of 'X' cm
        :param direction: Direction of the moove (Default value = down)
        :param distance: distance of the move in cm (Default value = 20)
        '''
        if isinstance(direction, Direction):
            arguments = (direction.value, str(distance))
            command = " ".join(arguments)
            self.send_command(command=command)

    def rotate(self, wise=Clockwise.CW, degre=90):
        '''Command the drone to rotate on himself. Rotation
        can be clockwise or counterclockwise
        :param wise: Direction of the rotation, clockwise or countercw (default value = Clockwise)
        '''
        if isinstance(wise, Clockwise):
            command = " ".join(wise.value, degre)
            self.send_command(command=command)

    def stop(self):
        '''Command the drone to hover in air
        '''
        self.send_command('stop')
