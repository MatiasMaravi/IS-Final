from unittest import TestCase
from app import app, Cuenta, Operacion, cuentas, fecha_actual, get_nombre
#Creamos 3 test de exito:
#test1: obtener_contactos
#test2: pagar
#test3: historial
class Test(TestCase):
    #Verifico que el metodo obtener_contactos funcione correctamente
    def test_obtener_contactos(self):
        with app.test_client() as c:
            rv = c.get('/billetera/contactos?minumero=21345')
            json_data = rv.get_json()
            self.assertEqual(json_data, {'123': 'Luisa', '456': 'Andrea'})
    #Verifico que el metodo pagar funcione correctamente
    def test_pagar(self):
        with app.test_client() as c:
            rv = c.post('/billetera/pagar?minumero=21345&numerodestino=456&valor=100')
            json_data = rv.get_json()
            self.assertEqual(json_data, {'Realizado en: ': fecha_actual()})
    #Verifico que el metodo historial funcione correctamente
    def test_historial(self):
        with app.test_client() as c:
            rv = c.get('/billetera/historial?minumero=123')
            json_data = rv.get_json()
            self.assertEqual(json_data, {'Operaciones realizadas': [], 'Pago recibido': [],'Saldo de Luisa': 400})

