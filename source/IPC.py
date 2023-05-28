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
        self.mutex = threading.Semaphore(1)  # Semáforo para garantizar exclusión mutua en la sala de espera
        self.barbero_sem = threading.Semaphore(0)  # Semáforo para despertar al barbero cuando llega un cliente

    def stop(self):
        """
        Stops the simulation.
        """
        self.activate = False

    def atender_clientes(self):
        """
        Barber's task to serve clients.
        """
        while self.activate:
            while self.activate:
                self.barbero_sem.acquire()  # El barbero espera a que llegue un cliente
                self.mutex.acquire()
                cliente = self.sala_espera.pop(0)
                self.mutex.release()

                self.is_sleep = False
                self.log.append(
                    "Barbero atendiendo al cliente " + str(cliente.id) + " con un tiempo de atencion de " + "{:.3}".format(
                        cliente.tiempo_atencion) + "\n")
                time.sleep(cliente.tiempo_atencion)
                self.log.append("Barbero terminó de atender al cliente " + str(cliente.id) + "\n")
                self.is_sleep = True


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

    def simular_barbero_dormilon(self, num_sillas):
        self.num_sillas = num_sillas  # Actualizar el número de sillas
        self.activate = True
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

            self.mutex.acquire()
            if len(self.sala_espera) < self.num_sillas:
                self.sala_espera.append(cliente)
                self.sala_espera.sort(key=lambda c: c.tiempo_atencion)  # Ordenar por tiempo de atención
                self.log.append("Cliente " + str(
                    cliente.id) + " llegó a la sala de espera con un tiempo de llegada de " + "{:.3}".format(
                    tiempo_llegada) + "\n")
                self.mutex.release()  # Liberar el semáforo mutex antes de liberar al barbero
                self.barbero_sem.release()  # Despertar al barbero si estaba dormido
            else:
                self.log.append("Cliente " + str(cliente.id) + " se fue porque la sala de espera está llena \n")
                self.mutex.release()
            time.sleep(0.1)  # Pausa para permitir que el barbero atienda a los clientes

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
