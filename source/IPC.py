import threading
import time
import random
import statistics


class Cliente:
    def __init__(self, id, tiempo_atencion):
        """
        Initializes a new instance of the Cliente class.

        Args:
            id (int): The unique identifier for the client.
            tiempo_atencion (float): The time required to attend to the client.
        """
        self.id = id
        self.tiempo_atencion = tiempo_atencion

class Barberia:
    def __init__(self, num_sillas):
        """
        Initializes an instance of the Barberia class.

        Args:
            num_sillas (int): The number of chairs in the waiting room.

        Attributes:
            log (list): A list to store the log of events.
            sala_espera (list): A list representing the waiting room.
            num_sillas (int): The number of chairs in the waiting room.
            is_sleep (bool): A flag indicating if the barber is sleeping or not.
            activate (bool): A flag indicating if the barber shop is active or not.
            mutex (threading.Semaphore): A semaphore for ensuring mutual exclusion in the waiting room.
            barbero_sem (threading.Semaphore): A semaphore for waking up the barber when a customer arrives.
            clientes_se_fueron (int): The count of customers who left without being served.
        """
        self.log = []
        self.waiting_room = []
        self.num_sillas = num_sillas
        self.is_sleep = True
        self.activate = False
        self.mutex = threading.Semaphore(1)  # Semáforo para garantizar exclusión mutua en la sala de espera
        self.barbero_sem = threading.Semaphore(0)  # Semáforo para despertar al barbero cuando llega un cliente
        self.customers_gone = 0

    def stop(self):
        """
        Stops the operation of the barber shop.

        Sets the `activate` flag to False, indicating that the barber shop should stop its operation.
        """
        self.activate = False

    def serve_customers(self):
        """
        Handles the process of attending customers in the barber shop.

        This method is executed by the barber thread to attend customers. It waits for a customer to arrive,
        retrieves the customer from the waiting room, performs the service, and updates the log accordingly.
        After attending a customer, it sets the barber's status to sleeping.

        Note:
        - This method should be executed in a separate thread.

        """
        while self.activate:
            self.barbero_sem.acquire()  # El barbero espera a que llegue un cliente
            self.mutex.acquire()
            cliente = self.waiting_room.pop(0)
            self.mutex.release()

            self.is_sleep = False
            time.sleep(1)
            self.log.append(
                "Barbero atendiendo al cliente " + str(cliente.id) + " con un tiempo de atencion de " + "{:.3}".format(
                    cliente.tiempo_atencion) + "\n")
            time.sleep(cliente.tiempo_atencion)
            self.log.append("Barbero terminó de atender al cliente " + str(cliente.id) + "\n")
            self.is_sleep = True

    def arrival_clients(self):
        """
        Simulates the arrival of customers to the barber shop.

        This method is executed by the customer arrival thread. It generates random arrival times and service durations
        for customers, adds them to the waiting room if there is space available, and updates the log accordingly.

        Note:
        - This method should be executed in a separate thread.

        """
        id_cliente = 1
        while self.activate:
            arrival_time = random.uniform(2, 4)
            attention_time = random.uniform(4, 7)
            time.sleep(arrival_time)
            customer = Cliente(id_cliente, attention_time)
            id_cliente += 1

            self.mutex.acquire()
            if len(self.waiting_room) < self.num_sillas:
                self.waiting_room.append(customer)
                self.waiting_room.sort(key=lambda c: c.tiempo_atencion)  # Ordenar por tiempo de atención
                self.log.append("Cliente " + str(
                    customer.id) + " llegó a la sala de espera con un tiempo de llegada de " + "{:.3}".format(
                    arrival_time) + "\n")
                self.mutex.release()  # Liberar el semáforo mutex antes de liberar al barbero
                self.barbero_sem.release()  # Despertar al barbero si estaba dormido
            else:
                self.customers_gone += 1
                self.log.append("Cliente " + str(customer.id) + " se fue porque la sala de espera está llena \n")
                self.mutex.release()
            time.sleep(0.1)  # Pausa para permitir que el barbero atienda a los clientes

    def simular_barbero_dormilon(self, num_sillas):
        """
        Simulates the sleepy barber problem.

        This method starts the simulation of the sleepy barber problem. It initializes the number of chairs in the waiting
        room, sets the activate flag to True, and starts two threads for customer arrival and barber service.

        Args:
            num_sillas (int): The number of chairs in the waiting room.

        """
        self.num_sillas = num_sillas  # Actualizar el número de sillas
        self.activate = True
        threading.Thread(target=self.serve_customers).start()
        threading.Thread(target=self.arrival_clients).start()

    def get_list(self):
        """
        Returns the number of customers in the waiting room.

        Returns:
            int: The number of customers in the waiting room.

        """
        return len(self.waiting_room)
    
    def get_clientes_se_fueron(self):
        """
        Returns the number of customers who left due to a full waiting room.

        Returns:
            int: The number of customers who left.

        """
        return self.customers_gone

    def get_sleep(self):
        """
        Returns the sleep status of the barber.

        Returns:
            bool: True if the barber is sleeping, False otherwise.

        """
        return self.is_sleep

    def get_logs(self):
        """
        Returns the log of events that occurred during the simulation.

        Returns:
            list: The list of log messages.

        """
        return self.log
