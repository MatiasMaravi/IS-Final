from unittest import TestCase
from app import app, Cuenta, Operacion, cuentas, fecha_actual, get_nombre
#Creamos 3 test de error:
#test4: obtener_contactos
#test5: pagar
#test6: historial
class TestErrores(TestCase):
    def test_obtener_contactos(self):
        with app.test_client() as c:
            rv = c.get('/billetera/contactos?minumero=2134')
            json_data = rv.get_json()
            self.assertEqual(json_data, {'Error': 'No existe la cuenta'})
    def test_pagar(self):
        with app.test_client() as c:
            rv = c.post('/billetera/pagar?minumero=21345&numerodestino=123&valor=1000')
            json_data = rv.get_json()
            self.assertEqual(json_data, {'Error': 'No existe la cuenta'})
    def test_historial(self):
        with app.test_client() as c:
            rv = c.get('/billetera/historial?minumero=2134')
            json_data = rv.get_json()
            self.assertEqual(json_data, {'Error': 'No existe la cuenta'})