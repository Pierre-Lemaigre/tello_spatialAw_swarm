"""This module is here to map the space for the Tello
"""


class Coordinates:
    """Class for representation of coordinates in 3 dimensions.
    """

    def __init__(self, x_axis=0, y_axis=0, z_axis=0):
        """3 coordinates to create representation of the tello in space.

        :param x_axis: X axis in space (default value = 0).
        :type x_axis: int.
        :param y_axis: Y axis in space (default value = 0).
        :type y_axis: int.
        :param z_axis: Z axis in space (default value = 0).
        :type z_axis: int.

        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.z_axis = z_axis

    def __str__(self):
        """Representation of the Coordinate Object.

        :return: Representation of the Coordinates.
        :rtype: str.

        """
        return "Coordinates : | X : {} | Y : {} | Z : {} |".format(self.x_axis, self.y_axis, self.z_axis)


class Speed:
    """Class for representation of speed states.
    """

    def __init__(self, x_speed=0, y_speed=0, z_speed=0):
        """Representation of the speed of the Tello.

        :param x_speed: X speed state in space (default value = 0).
        :type x_speed: int.
        :param y_speed: Y speed state in space (default value = 0).
        :type y_speed: int.
        :param z_speed: Z speed state in space (default value = 0).
        :type z_speed: int.

        """
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.z_speed = z_speed

    def __str__(self):
        """Representation of the Speed state Object.

        :return: Representation of the speed.
        :rtype: str.

        """
        return "Speed states (cm.s⁻¹): | X axis : {} | Y axis : {} | Z axis : {} |".format(self.x_speed, self.y_speed, self.z_speed)


class Velocity:
    """Class for representation of the velocity of the Tello drones
    """

    def __init__(self, x_velocity=0, y_velocity=0, z_velocity=0):
        """Representation of the velocity of the Tello drones.

        :param x_velocity: Velocity of the X axis.
        :type x_velocity: int.
        :param y_velocity: Velocity of the y axis.
        :type y_velocity: int.
        :param z_velocity: Velocity of the Z axis.
        :type z_velocity: int.
        """
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.z_velocity = z_velocity

    def __str__(self):
        """Representation of the Velocity Object

        :return: Representation of the Velocity.
        :rtype: str.

        """
        return "Velocity states (cm.s⁻²)| X : {} | Y : {} | Z : {} |".format(self.x_velocity, self.y_velocity, self.z_velocity)
