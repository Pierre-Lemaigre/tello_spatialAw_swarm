"""
This module contain
- a class wrapper for the Tello drone
    It implements connection and communication class with the drone

    This module is inspired on the code of : hanker-lu
    Code is available there : https://github.com/dji-sdk/Tello-Python/blob/master/Tello_Video/tello.py
    The original code is in python 2.7 (So conversion to 3.7 by me)

- a class for the Tello representation in space and state (sleep or alive)

"""
import socket
from .direction import Direction, Clockwise
from .space import Coordinates, Speed, Velocity


class Tello:
    """Class wrapper around Tello communications.
    """
    def __init__(self, local_ip='', local_port=9000, tello_ip='192.168.10.1', tello_port=8889):
        """
        Initialize Tello class : bind tello command and state sockets.

         :param local_ip: Local IP adress to bind. '' by default.
         :type local_ip: str.
         :param local_port: Local IP adress to bind (8890 by default).
         :type local_port: int.
         :param tello_ip: Tello IP.
         :type tello_ip: str.
         :param tello_port: Tello port.
         :type tello_port: str.

        """
        self.local_port = local_port
        # Initilization of some parameters usefull for the future
        self.tello_adr = (tello_ip, tello_port)

        # Creation of the socket to send commands to the Tello drone
        self.socket_command = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket_command.bind((local_ip, self.local_port))

    def __del__(self):
        """Destructor of the class.
        Close the socket in order to avoid bug.
        """
        self.socket_command.close()

    def __str__(self):
        """Representation of the Tello object.
        :return: Representation of the object.
        :rtype: str.

        """
        return "Adresse Tello {}, Socket du Tello : {}".format(self.tello_adr[0], self.socket_command)

    def send_command(self, command='command'):
        """
        Send command to the Tello and wait for response.

        :param command: Command to send. (Default_value'Command').
        :type command: str.

        """
        try:
            command_encoded = command.encode(encoding='utf-8')
        except UnicodeError:
            print('Error while converting Command : {}'.format(command))
        else:
            self.socket_command.sendto(command_encoded, self.tello_adr)

    def takeoff(self):
        """Initiate the flight of the drone.

        """
        self.send_command('takeoff')

    def land(self):
        """Land the drone automaticaly.

        """
        self.send_command('land')

    def emergency(self):
        """In case of emergency, stop motors imediately.

        """
        self.send_command('emergency')

    def move_to(self, direction=Direction.DOWN, distance='20'):
        """Command the drone to move in 3Dimensions of 'X' cm.

        :param direction: Direction of the moove (Default value = down).
        :param distance: distance of the move in cm (Default value = 20).

        """
        if isinstance(direction, Direction):
            arguments = (direction.value, str(distance))
            command = " ".join(arguments)
            self.send_command(command=command)

    def rotate(self, wise=Clockwise.CW, degre=90):
        """Command the drone to rotate on himself. Rotation
        can be clockwise or counterclockwise.

        :param wise: Direction of the rotation, clockwise or countercw (default value = Clockwise).

        """
        if isinstance(wise, Clockwise):
            command = " ".join(wise.value, degre)
            self.send_command(command=command)

    def stop(self):
        """Command the drone to hover in air.
        """
        self.send_command('stop')

    def keep_drone_alive(self):
        """Tello drone fall asleep if during 15s they didn't receive a command
        This function "ping" the drone and act according to the response (notify programm if drone down)
        Also i'm using this function to check on battery level, so if battery to low, drone down to.
        """
        self.send_command('battery?')


class Tstate:
    """Class for Tello representation in space and state.
    """

    def __init__(self, sleep=False, mission_pad=-1, coordinates=Coordinates(), speed=Speed(), velocity=Velocity()):
        """Initialize Tello_state class.

        :param sleep: Tello state in real time (default value = False).
        :type sleep: bool.
        :param mission_pad: Mission pad detected by the Tello drone (default value = -1).
        :type mission_pad: int.
        :param coordinates: Representation of the Tello coordinates in space 3 dimensions (x, y , z).
        :type coordinates: Coordinates.
        :param speed: Tello speed state.
        :type speed: Speed.
        :param acceleration: Tello acceleration state.
        :type velocity: Velocity.

        """
        self.sleep = sleep
        self.mission_pad = mission_pad
        self.coordinates = coordinates
        self.speed = speed
        self.velocity = velocity

    def __str__(self):
        """Representation of the Tello state Object.

        :return: Representation of Tello state.
        :rtype: str.
        """
        return "Sleep : {} | Mission pad : {}\n[ Space : {}, {}, {} ]".format(self.sleep, self.mission_pad, self.coordinates, self.speed, self.velocity)
