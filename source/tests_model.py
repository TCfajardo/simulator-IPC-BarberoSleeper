import random
from Simulador import Client

def test_creacion_clientes():
    print('TEST VERIFICACION Y CREACIÓN DE CLIENTES')
    average_time = 10
    Client.reset_ids()

    cliente1 = Client(average_time)
    cliente2 = Client(average_time)
    cliente3 = Client(average_time)

    assert cliente1.get_cliente_id() == 1
    print("Cliente 1 - ID:", cliente1.get_cliente_id(), "Tiempo de llegada:", cliente1.get_tiempo_llegada())
    assert cliente2.get_cliente_id() == 2
    print("Cliente 2 - ID:", cliente2.get_cliente_id(), "Tiempo de llegada:", cliente2.get_tiempo_llegada())
    assert cliente3.get_cliente_id() == 3
    print("Cliente 3 - ID:", cliente3.get_cliente_id(), "Tiempo de llegada:", cliente3.get_tiempo_llegada())


    print("Test de creación de clientes: PASSED")

test_creacion_clientes()
