from threading import Thread, Semaphore
import random
import threading

colaClientes = []




class Cliente:
    def __init__(self, identificador, duracion):
        self.identificador = identificador
        self.duracion = duracion

class Barbero:    
    def __init__(self):
      self.barbero = Semaphore(1)
    def sleep(self):
        self.barbero.acquire()
    def wakeUp(self):
        self.barbero.release()
    def work(self,time):
        print("El barbero está cortando el cabello.")
        time.sleep(time)  # Simula el tiempo que lleva cortar el cabello
        print("El barbero ha terminado de cortar el cabello.")

class Barberia:
    def __init__(self,sillasDisponibles):
      self.barbero = Barbero()
      self.salaEspera = Semaphore(sillasDisponibles)
      self.countClient = 0
      self.sillasDisponibles = sillasDisponibles
    
    def start(self):
        while True:
            hilo1 = threading.Thread(target= self.llegadaCliente)
            hilo1.start()
            
    def llegadaCliente(self):
        while True:
            self.countClient+= 1
            cliente = Cliente(self.countClient, random.uniform(0, 1))
            if(len(colaClientes)<self.sillasDisponibles):
                with self.barbero:
                    if(colaClientes == 0):
                        self.barbero.wakeUp()
                    else:
                        cliente espere
                        time.sleep(1) 
                    colaClientes.append(cliente)
    
    def cortar_cabello(self):
        while True:
            if len(colaClientes) > 0:
                cliente = min(colaClientes, key=lambda x: x.duracion)
                self.barbero.work(cliente.duracion)
                colaClientes.remove(cliente)
            else:
                self.barbero.sleep() # El barbero duerme hasta que llegue un cliente


# Crear una instancia de la barbería
barberia = Barberia()

# Iniciar el hilo de llegada de clientes
barberia.start()