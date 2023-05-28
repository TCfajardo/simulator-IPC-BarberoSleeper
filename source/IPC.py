import threading
import time
import random
import statistics

class Cliente:
    def __init__(self, id, tiempo_atencion):
        self.id = id
        self.tiempo_atencion = tiempo_atencion

class Barberia:
    def __init__(self, num_sillas):
        self.sala_espera = []
        self.num_sillas = num_sillas
        self.is_sleep = True
        self.activate = False
        self.mutex = threading.Semaphore(1)  # Semáforo para garantizar exclusión mutua en la sala de espera
        self.barbero_sem = threading.Semaphore(0)  # Semáforo para despertar al barbero cuando llega un cliente

    def stop(self):
         self.activate = False

    def atender_clientes(self):
        while self.activate:
            self.barbero_sem.acquire()  # El barbero espera a que llegue un cliente
            self.mutex.acquire()
            cliente = self.sala_espera.pop(0)
            self.mutex.release()

            self.is_sleep = False
            time.sleep(1)
            print(f"Barbero atendiendo al cliente {cliente.id} con un tiempo de atencion de {cliente.tiempo_atencion}")
            time.sleep(cliente.tiempo_atencion)
            print(f"Barbero terminó de atender al cliente {cliente.id}")
            self.is_sleep = True

    def llegada_clientes(self):
        id_cliente = 1
        while self.activate:
            tiempo_llegada = random.uniform(2, 4)
            tiempo_atencion = random.uniform(4, 7)
            time.sleep(tiempo_llegada)
            cliente = Cliente(id_cliente, tiempo_atencion)
            id_cliente += 1

            self.mutex.acquire()
            if len(self.sala_espera) < self.num_sillas:
                self.sala_espera.append(cliente)
                self.sala_espera.sort(key=lambda c: c.tiempo_atencion)  # Ordenar por tiempo de atención
                print(f"Cliente {cliente.id} llegó a la sala de espera con un tiempo de llegada de {tiempo_llegada}")
                self.mutex.release()  # Liberar el semáforo mutex antes de liberar al barbero
                self.barbero_sem.release()  # Despertar al barbero si estaba dormido\
                

            else:
                print(f"Cliente {cliente.id} se fue porque la sala de espera está llena")
                self.mutex.release()
            time.sleep(0.1)  # Pausa para permitir que el barbero atienda a los clientes

    def simular_barbero_dormilon(self,num_sillas):
        self.num_sillas = num_sillas  # Actualizar el número de sillas
        self.activate = True
        threading.Thread(target=self.atender_clientes).start()
        threading.Thread(target=self.llegada_clientes).start()


    def get_list(self):
        return len(self.sala_espera)

    def get_sleep(self):
        return self.is_sleep

