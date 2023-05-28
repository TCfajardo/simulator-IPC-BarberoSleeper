import threading
import time
import random
import statistics


class Cliente:
    """
    Represents a client in the barbershop.

    Attributes:
        id (int): The ID of the client.
        tiempo_atencion (float): The time it takes to serve the client.
    """

    def __init__(self, id, tiempo_atencion):
        self.id = id
        self.tiempo_atencion = tiempo_atencion


class Barberia:
    """
    Represents a barbershop.

    Attributes:
        log (list): A log of events in the barbershop.
        sala_espera (list): A list of clients in the waiting room.
        num_sillas (int): The number of chairs in the waiting room.
        is_sleep (bool): Indicates whether the barber is sleeping.
        activate (bool): Indicates whether the simulation is active.
        mutex (Semaphore): A semaphore to ensure mutual exclusion in the waiting room.
        barbero_sem (Semaphore): A semaphore to wake up the barber when a client arrives.
    """

    def __init__(self, num_sillas):
        self.log = []
        self.sala_espera = []
        self.num_sillas = num_sillas
        self.is_sleep = True
        self.activate = False
        self.waiting_room_mutex = threading.Semaphore(1)  # Semaphore to guarantee mutual exclusion in the waiting room
        self.barber_semaphore = threading.Semaphore(0)  # Semaphore to wake up the barber when a client arrives

    def stop(self):
        """
        Stops the simulation.
        """
        self.activate = False

    def simular_barbero_dormilon(self, num_sillas):
        """
        Starts the simulation of the sleeping barber problem.

        Args:
            num_sillas (int): The number of chairs in the waiting room.
        """
        self.num_sillas = num_sillas  # Update the number of chairs
        self.activate = True #run
        threading.Thread(target=self.atender_clientes).start()
        threading.Thread(target=self.llegada_clientes).start()


    def llegada_clientes(self):
        """
        Task to handle the arrival of clients.
        """
        id_cliente = 1
        while self.activate:
            tiempo_llegada = random.uniform(1, 6)
            tiempo_atencion = random.uniform(2, 6)
            time.sleep(tiempo_llegada)
            cliente = Cliente(id_cliente, tiempo_atencion)
            id_cliente += 1

            self.waiting_room_mutex.acquire()
            if len(self.sala_espera) < self.num_sillas:
                self.sala_espera.append(cliente)
                self.sala_espera.sort(key=lambda c: c.tiempo_atencion)  # Sort by service time
                self.log.append("Client " + str(
                    cliente.id) + " arrived in the waiting room with an arrival time of " + "{:.3}".format(
                    tiempo_llegada) + "\n")
                self.waiting_room_mutex.release()  # Release the mutex semaphore before releasing the barber
                self.barber_semaphore.release()  # Wake up the barber if sleeping
            else:
                self.log.append("Client " + str(cliente.id) + " left because the waiting room is full \n")
                self.waiting_room_mutex.release()
            time.sleep(0.1)  # Pause to allow the barber to serve clients

    def atender_clientes(self):
        """
        Barber's task to serve clients.
        """
        while self.activate:
            self.barber_semaphore.acquire()  # The barber waits for a client to arrive
            self.waiting_room_mutex.acquire() # ensure mutual exclusion in the waiting room.
            cliente = self.sala_espera.pop(0)
            self.waiting_room_mutex.release()

            self.is_sleep = False
            self.log.append(
                "Barber serving client " + str(cliente.id) + " with a service time of " + "{:.3}".format(
                    cliente.tiempo_atencion) + "\n")
            time.sleep(cliente.tiempo_atencion)
            self.log.append("Barber finished serving client " + str(cliente.id) + "\n")
            self.is_sleep = True

    

    def get_list(self):
        """
        Returns the number of clients in the waiting room.
        """
        return len(self.sala_espera)

    def get_sleep(self):
        """
        Returns the sleep status of the barber.
        """
        return self.is_sleep

    def get_logs(self):
        """
        Returns the log of events in the barbershop.
        """
        return self.log
