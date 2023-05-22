import random
from Client import Client
import time
from Barber import Barber

import unittest
from Waiting_Room import WaitingRoom

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
    print("LLega Cliente 4 - ID:", cliente4.get_cliente_id(), "Tiempo de llegada:", cliente4.get_tiempo_llegada(),"Tiempo de atención:", cliente4.get_tiempo_atencion())
    
    assert not barber.is_available()

    print("Estado barbero busy: ", barber.get_estado())
    print('atención/ejecución')
    barber.set_available()#se libera de la atencion y está disponible
    print("Estado barbero: ", barber.get_estado())
    # Verificar si el barbero está ocupado después de atender al cliente
    assert  barber.is_available()

    print("Test passed!")

#test_barber()


class WaitingRoomTests(unittest.TestCase):
    def test_ingresar_cliente(self):
        room = WaitingRoom(3)

        client1 = Client(10)
        client2 = Client(10)
        client3 = Client(10)
        client4 = Client(10)
        
        self.assertTrue(room.ingresar_cliente(client1))
        self.assertTrue(room.ingresar_cliente(client2))
        self.assertTrue(room.ingresar_cliente(client3))
        self.assertFalse(room.ingresar_cliente(client4))
        
    def test_siguiente_cliente(self):
        room = WaitingRoom(3)

        client1 = Client(10)
        client2 = Client(10)
        client3 = Client(10)
    
        room.ingresar_cliente(client1)
        room.ingresar_cliente(client2)
        room.ingresar_cliente(client3)

        print('TIEMPO DE ATENCÍON\ncl1: ',client1.get_tiempo_atencion(),
              '\ncl2: ',client2.get_tiempo_atencion(),'\ncl3: ',client3.get_tiempo_atencion())

        next_client = room.siguiente_cliente()
        print('proximo cliente ',next_client.get_tiempo_atencion())
        self.assertEqual(next_client.get_cliente_id(), client3.get_cliente_id())

        
    def test_eliminar_cliente(self):
        room = WaitingRoom(3)
        client1 = Client(10)
        client2 = Client(10)
        
        room.ingresar_cliente(client1)
        room.ingresar_cliente(client2)
        
        room.eliminar_cliente(client1)
        self.assertNotIn(client1, room._sillas_ocupadas)
        self.assertNotIn(client1, room._clientes_espera)
        
        room.eliminar_cliente(client2)
        self.assertNotIn(client2, room._sillas_ocupadas)
        self.assertNotIn(client2, room._clientes_espera)
        
if __name__ == '__main__':
    unittest.main()
