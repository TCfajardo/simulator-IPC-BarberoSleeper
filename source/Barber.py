import time
import random
from Client import Client

class Barber:
    """Represents a barber in the simulation.
    """
    def __init__(self):
        self._estado = "available"

    def is_available(self):
        """Checks if the barber is available to attend a client.
        Returns:
            bool: True if the barber is available, False otherwise.
        """
        return self._estado == "available"

    def is_asleep(self):
        """Checks if the barber is sleeping.

        Returns:
            bool: True if the barber is sleeping, False otherwise.
        """
        return self._estado == "asleep"

    def atender_cliente(self, time_atention):
        """Attends a client.
        Args:
            tiempo (int): The time atention of client to be attended.
        """
        self._estado = "busy"
        time.sleep(time_atention)
        
    def set_available(self):
        """Sets the barber's state to available."""
        self._estado = "available"

    def set_asleep(self):
        """Sets the barber's state to asleep."""
        self._estado = "asleep"

    def get_estado(self):
        """Returns the current state of the barber.

        Returns:
            str: The state of the barber ("available", "busy", or "asleep").
        """
        return self._estado