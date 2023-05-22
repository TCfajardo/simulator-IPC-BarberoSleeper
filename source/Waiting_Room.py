class WaitingRoom:
    """Represents a waiting room in the barber shop."""
    def __init__(self, num_sillas):
        self._num_sillas = num_sillas
        self._sillas_ocupadas = []
        self._clientes_espera = []
    
    def ingresar_cliente(self, cliente):
        """Tries to add a client to the waiting room.
        If there are available chairs, the client is added to the waiting room.
        If all chairs are occupied, the client is not added and returns False.
        Args:
            cliente (Client): The client to be added.
        Returns:
            bool: True if the client was added, False if all chairs are occupied.
        """
        if len(self._sillas_ocupadas) < self._num_sillas:
            self._sillas_ocupadas.append(cliente)
            self._clientes_espera.append(cliente)
            return True
        else:
            return False

    def siguiente_cliente(self):
        """Selects the next client to be attended based on SPN algorithm.

    Returns:
        Cliente: The next client to be attended.
        """
        if len(self._clientes_espera) > 0:
        # Ordenar los clientes por tiempo de atención estimado de menor a mayor
            self._clientes_espera.sort(key=lambda c: c.get_tiempo_atencion())

            # Actualizar las sillas ocupadas para reflejar los clientes en espera
            self._sillas_ocupadas = self._clientes_espera[:]

            return self._clientes_espera[0]
        else:
            return None

    def eliminar_cliente(self, cliente):
        """Removes a client from the waiting room.

        Args:
            cliente (Cliente): The client to be removed.
        """
        self._sillas_ocupadas.remove(cliente)
        self._clientes_espera.remove(cliente)
