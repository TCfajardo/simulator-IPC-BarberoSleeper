import random
from Client import Client
import time
from Barber import Barber

def test_creacion_clientes():
    print('TEST VERIFICACION Y CREACIÓN DE CLIENTES')
    average_time = 10
    Client.reset_ids()

    cliente1 = Client(average_time)
    cliente2 = Client(average_time)
    cliente3 = Client(average_time)

    assert cliente1.get_cliente_id() == 1
    print("Cliente 1 - ID:", cliente1.get_cliente_id(), "Tiempo de llegada:", cliente1.get_tiempo_llegada(),"Tiempo de atención:", cliente1.get_tiempo_atencion())
    assert cliente2.get_cliente_id() == 2
    print("Cliente 2 - ID:", cliente2.get_cliente_id(), "Tiempo de llegada:", cliente2.get_tiempo_llegada(),"Tiempo de atención:", cliente2.get_tiempo_atencion())
    assert cliente3.get_cliente_id() == 3
    print("Cliente 3 - ID:", cliente3.get_cliente_id(), "Tiempo de llegada:", cliente3.get_tiempo_llegada(),"Tiempo de atención:", cliente3.get_tiempo_atencion())

    print("\nTest de creación de clientes: PASSED")

#test_creacion_clientes()


def test_barber():
    print('\nTEST CREACIÓN Y ATENCIÓN DEL BARBERO')
    # Crear instancia del barbero
    barber = Barber()

    # Verificar si el barbero está inicialmente disponible
    assert barber.is_available()
    print("Estado barbero: ", barber.get_estado())

    # Verificar si el barbero no está inicialmente dormido
    assert not barber.is_asleep()
    print("Estado barbero: ", barber.get_estado())

    # Crear instancia de un cliente
    cliente4 = Client(10)

    # Atender al cliente por parte del barbero
    barber.atender_cliente(cliente4.get_tiempo_atencion())
    print("Cliente 4 - ID:", cliente4.get_cliente_id(), "Tiempo de llegada:", cliente4.get_tiempo_llegada(),"Tiempo de atención:", cliente4.get_tiempo_atencion())
    
    assert not barber.is_available()

    print("Estado barbero busy: ", barber.get_estado())
    
    barber.set_available()
    print("Estado barbero: ", barber.get_estado())
    # Verificar si el barbero está ocupado después de atender al cliente
    assert  barber.is_available()

    print("Test passed!")

test_barber()
