from flask import Flask, request, jsonify, render_template
#Creamos fechas con la fecha actual, ejemplo: 11/07/2023
from datetime import datetime
def fecha_actual():
    now = datetime.now()
    return now.strftime("%d/%m/%Y")
def get_nombre(numero):
    for i in cuentas:
        if numero == i.numero:
            return i.nombre
    return "SinNombre"
class Cuenta:
    def __init__(self, numero, nombre, saldo, contactos):
        self.numero = numero
        self.nombre = nombre
        self.saldo = saldo
        self.contactos = contactos
        self.operacionesPropias = []
    
    def historial(self):
        text = ""
        text += f"Saldo actual: {self.saldo}\n"
        text += f"Operaciones realizadas: \n"
        recibidos = []
        enviados = []
        for i in cuentas:
            if i.nombre != self.nombre:
                for j in i.operacionesPropias:
                    if j.NumeroDestino == self.numero:
                        recibidos.append((i.nombre,j.fecha,j.valor))
        for i in self.operacionesPropias:
            enviados.append((get_nombre(i.NumeroDestino),i.fecha,i.valor))
        return self.saldo,recibidos,enviados
        
    def pagar(self,destino, valor):
        self.saldo -= int(valor)
        self.operacionesPropias.append(Operacion(destino,fecha_actual(),valor))
    
    def obtener_contactos(self):
        return self.contactos

class Operacion:
    def __init__(self, NumeroDestino, fecha, valor):
        self.NumeroDestino = NumeroDestino
        self.fecha = fecha
        self.valor = valor
        for i in cuentas:
            if i.numero == NumeroDestino:
                i.saldo += int(valor)
    def obtener_numeroDestino(self):
        return self.NumeroDestino
    def obtener_valor(self):
        return self.valor
        
cuentas = []
c1 = Cuenta("21345", "Arnaldo",200,["123","456"])
c2 = Cuenta("123", "Luisa", 400, ["456"])
c3 = Cuenta("456", "Andrea", 300, ["21345"])
cuentas.append(c1)
cuentas.append(c2)
cuentas.append(c3)
app = Flask(__name__)
#/billetera/contactos?minumero=XXXX -> ruta flask
@app.route('/billetera/contactos', methods=['GET'])

def obtener_contactos():
    numero = request.args.get('minumero')
    flag = False
    lista = []
    diccionario = {}
    for cuenta in cuentas:
        if cuenta.numero == numero:
            lista = cuenta.obtener_contactos()
            flag = True
            break
    if flag == False:
        return jsonify({"Error":"No existe la cuenta"})
    
    for cuenta in cuentas:
        if cuenta.numero in lista:
            diccionario[cuenta.numero] = cuenta.nombre
    return jsonify(diccionario)

#/billetera/pagar?minumero=21345&numerodestino=123&valor=100
@app.route('/billetera/pagar', methods=['POST'])
def pagar():
    numero = request.args.get('minumero')
    numerodestino = request.args.get('numerodestino')
    valor = request.args.get('valor')
    flag = False
    for cuenta in cuentas:
        if cuenta.numero == numero:
            cuenta.pagar(numerodestino, valor)
            flag = True
            break
    if flag == False:
        return jsonify({"Error":"No existe la cuenta"})
    return jsonify({"Realizado en: ": fecha_actual()})

#/billetera/historial?minumero=123
@app.route('/billetera/historial', methods=['GET'])
def historial():
    numero = request.args.get('minumero')
    flag = False
    saldo = 0
    recibidos = []
    enviados = []
    for cuenta in cuentas:
        if cuenta.numero == numero:
            saldo,recibidos,enviados = cuenta.historial()
            flag = True
            break
    if flag == False:
        return jsonify({"Error":"No existe la cuenta"})
    diccionario = {}
    diccionario[f"Saldo de {get_nombre(numero)}"] = saldo
    diccionario["Operaciones realizadas"] = []
    diccionario["Pago recibido"] = []
    for i in recibidos:
        diccionario["Operaciones realizadas"].append({i[0]:i[2]})
    for i in enviados:
        diccionario["Pago recibido"].append({i[0]:i[2]})
    return jsonify(diccionario)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
