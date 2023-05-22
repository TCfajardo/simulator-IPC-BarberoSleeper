import random

class Client:
    """Represents a customer in the simulation.
    """
    current_id = 0

    def __init__(self, average_time):
        Client.current_id += 1
        self._cliente_id = Client.current_id
        self._tiempo_llegada = self._generate_time_arrival(average_time)
        self._time_attention = self._generate_time_atencion()

    def _generate_time_arrival(self, average_time):
        """Generate a random arrival time based on average time
        Args:
            average_time (int): average time entered by the user
        Returns:
            int: average time
        """
        tiempo_min = int(average_time * 0.5)  # Ejemplo: Tomar la mitad del tiempo promedio como mínimo
        tiempo_max = int(average_time * 1.5)  # Ejemplo: Tomar el 150% del tiempo promedio como máximo
        return random.randint(tiempo_min, tiempo_max)

    def _generate_time_atencion(self):
        """Generate a random attention time.
        Returns:
            int: Random attention time between 1 and 10.
        """
        return random.randint(1, 10)
    
    @classmethod
    def reset_ids(cls):
        """Reset the ID counter back to 0."""
        cls.current_id = 0

    def get_cliente_id(self):
        """Returns the ID of the client.
        Returns:
            int: The ID of the client.
        """
        return self._cliente_id

    def get_tiempo_llegada(self):
        """Returns the arrival time of the client.
        Returns:
            int: The arrival time of the client.
        """
        return self._tiempo_llegada
    
    def get_tiempo_atencion(self):
        """Returns the attention time for the client.
        Returns:
            int: The attention time for the client.
        """
        return self._time_attention
