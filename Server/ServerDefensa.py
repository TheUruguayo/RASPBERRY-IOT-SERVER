import datetime
import smtplib
import threading
from datetime import datetime
import time
from time import time
from time import sleep
from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from numpy import random
import math
import math as np
import Ploteador
import LibreriaServer as Server
import json
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbTDigital.db'  # data base
app.config['SQLALCHEMY_BINDS'] = {'dbLDR': 'sqlite:///dbLuxLDR.db',
                                  'dbTermistor': 'sqlite:///dbTTermistor.db'}
db = SQLAlchemy(app)

led1 = False
led2 = False
led3 = False
dbdatos = None
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


# en la terminal hay que escribir en python, from "nombre de la .py,Server" import db y despues db.create_all()

class Digital(db.Model):  # database detemp

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    raspberry = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id  # retorna la tas yla id

    def temperatura(self):
        return str(id)


class dbLDR(db.Model):  # database de LDR
    __bind_key__ = 'dbLDR'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    raspberry = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id  # retorna la task yla id

    def lux(self):
        return str(id)


class dbTermistor(db.Model):
    __bind_key__ = 'dbTermistor'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    raspberry = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id  # retorna la tas yla id

    def temperatura(self):
        return str(id)


def genericError(tipo, text):  # funcion que retorna 1 si hay error de ingreso de parametros por el usuario
    ret = 0  # inicializo el retorno en 0
    # Primero leo los th y tl actuales porque los voy a precisar.
    with open("AlarmaTEMPHig.txt", "r") as fp:
        data = fp.readline()
        thActual = int(data.strip(), 10)  ##leo th
    with open("AlarmaTEMPlow.txt", "r") as fp:
        data = fp.readline()
        tlActual = int(data.strip(), 10)  ##leo el tl anterior

    if len(text) == 0:  # si el largo de lo que el usuario ingreso es 0, entonces termina la funcion, con retorno 1
        ret = 1
        print("Error! no puedes ingresar campos vacios!")
    elif len(text) > 0:  # si el largo de lo que ingreso es mayor a 0, entonces debemos fijarnos cada caso
        if tipo == "th":  # control de error en th
            try:
                thNuevo = int(text.strip(), 10)
                if thNuevo < tlActual:  # si lllegue hasta aca, quiere decir que me ingresaron un entero, me fijo si es menor que el tl actual
                    ret = 1
                    print("Error! intentaste ingresar un th de ", text, "°C cuando el tl es: ", tlActual, "°C")
            except:
                print("Error de formato, se espera un entero")
                ret = 1

        elif tipo == "tl":  # control de error en tl
            try:
                tlNuevo = int(text.strip(), 10)
                if tlNuevo > thActual:
                    ret = 1
                    print("Error! intentaste ingresar un tl de: ", text, "°C cuando el th es: ", thActual, "°C")
            except:
                print("Error de formato, se espera un entero")
                ret = 1

        elif tipo == "ta":  # control de error en ta
            try:
                taNuevo = int(text.strip(), 10)
                if taNuevo < 10:
                    print("Error! intentaste ingresar un tiempo de alarma de: ", text,
                          "s cuando los tiempos de alarma no deben ser menmores a 10s")
                    ret = 1
            except:
                print("Error de formato, se espera un entero")
                ret = 1

        elif tipo == "tm":  # control en tiempos de medida
            try:
                tmNuevo = int(text.strip(), 10)
                if tmNuevo < 5:
                    ret = 1
                    print("Error! intentaste ingresar un tiempo de medida de: ", text,
                          "s cuando los tiempos de medida no deben ser menores a 5s")
            except:
                print("Error de formato, se espera un entero")
                ret = 1

        elif tipo == "sm":  # control de error en mails
            if ("." not in text and "@" not in text):
                ret = 1
                print("Error! intentaste ingresar la direccion: ", text, ", que no es valida")
        elif tipo == "FechaDesde" or tipo == "FechaHasta":  # control de fechas: necesito chequear que sean todos enteros, que esten bien y que encima los separadores esten bien, primero tienen que haber 2 separadores

            cantSeparadores = 0;
            for i in text:
                if i == "-":
                    cantSeparadores = cantSeparadores + 1
            if (cantSeparadores < 2):
                ret = 1;
                print("Error! debe ingresar la fecha con separadores")
            elif cantSeparadores == 2:  # ingreso correctamente los separadores, me tengo que fijar ahora los años y eso
                subString = text.split("-")
                try:
                    año = int(subString[0])
                    mes = int(subString[1])
                    dia = int(subString[2])
                    if año < 0 or año > 2021:
                        print("Ingrese un año valido")
                        ret = 1
                    if mes < 1 or mes > 12:
                        print("Ingrese un mes valido")
                        ret = 1
                    if dia < 1 or dia > 31:
                        print("Ingrese un dia valido")
                        ret = 1
                except:
                    print("Error, se esperan enteros")
                    ret = 1

    return ret


##################################
def EnvioSinRespuesta(dir, data):
    Server.Send(dir, data)


def leerYenviar():
    with open("AlarmaTEMPHig.txt", "r") as fp:
        data = fp.readline()
        th = int(data.strip(), 10)
        EnvioSinRespuesta(Server.RASP1, "H" + str(th) + "x")
        EnvioSinRespuesta(Server.RASP2, "H" + str(th) + "x")
        EnvioSinRespuesta(Server.RASP3, "H" + str(th) + "x")
    with open("AlarmaTEMPlow.txt", "r") as fp:
        data = fp.readline()
        tl = int(data.strip(), 10)
        EnvioSinRespuesta(Server.RASP1, "L" + str(tl) + "x")
        EnvioSinRespuesta(Server.RASP2, "L" + str(tl) + "x")
        EnvioSinRespuesta(Server.RASP3, "L" + str(tl) + "x")
    with open("TiempoDeMedida.txt", "r") as fp:
        data = fp.readline()
        tm = int(data.strip(), 10)
        EnvioSinRespuesta(Server.RASP1, "M" + str(tm) + "x")
        EnvioSinRespuesta(Server.RASP2, "M" + str(tm) + "x")
        EnvioSinRespuesta(Server.RASP3, "M" + str(tm) + "x")
    with open("TiempoDeAlarma.txt", "r") as fp:
        data = fp.readline()
        ta = int(data.strip(), 10)
        EnvioSinRespuesta(Server.RASP1, "t" + data + "x")
        EnvioSinRespuesta(Server.RASP2, "t" + data + "x")
        EnvioSinRespuesta(Server.RASP3, "t" + data + "x")
    with open("AlarmaOn.txt", "r") as fp:  # lee si esta alarma activada
        data = fp.readline()
        bandera = int(data.strip(), 10)
        EnvioSinRespuesta(Server.RASP1, "a" + data + "x")
        EnvioSinRespuesta(Server.RASP2, "a" + data + "x")
        EnvioSinRespuesta(Server.RASP3, "a" + data + "x")
    with open("Destino.txt", "r") as fp:  # lee si esta alarma activada
        data = fp.readline()
        destino = str(data)
        EnvioSinRespuesta(Server.RASP1, "D" + data + "x")
        EnvioSinRespuesta(Server.RASP2, "D" + data + "x")
        EnvioSinRespuesta(Server.RASP3, "D" + data + "x")
    return th, tl, tm, ta, bandera, destino


def cargarTemplate():
    global led1
    global led2
    global led3
    now = datetime.now()  # fecha actual en el servidor

    timeString = now.strftime("%Y-%m-%d %H:%M")  # estas variables se pasan al amigo index.html
    tasks = Digital.query.order_by(Digital.date_created).all()  # devuelve la base de datos ordenada por fecha
    tasks2 = dbLDR.query.order_by(dbLDR.date_created).all()  # devuelve la base de datos ordenada por fecha
    th, tl, tm, ta, bandera, destino = leerYenviar()
    str(tasks[-1].content) + "ºC " + tasks[-1].raspberry
    templateData = {

        'time': timeString,
        'temp': "Sensores ",
        'th': "Th:" + str(th),
        'tl': "Tl:" + str(tl),
        'LDR': str(tasks2[-1].content) + " LUX " + tasks2[-1].raspberry,
        'TAA': "Ta: " + str(ta),
        'TMM': "Tm: " + str(tm),
        'Alarma': "SI" if bandera == 1 else 'NO',
        'Destino': destino,
        'Rasp1': 'Conectada' if Server.BanderaRasp1 else 'Desconectada',
        'Rasp2': 'Conectada' if Server.BanderaRasp2 else 'Desconectada',
        'Rasp3': 'Conectada' if Server.BanderaRasp3 else 'Desconectada',
        ''
        'LED1': 'Prendida' if led1 else 'Apagada',
        'LED2': 'Prendida' if led2 else 'Apagada',
        'LED3': 'Prendida' if led3 else 'Apagada',
    }
    return templateData


@app.route('/plot.png')
def plot_png():
    global dbdatos
    fig = Ploteador.ploter(dbdatos)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


###################################PROGRAMACION DE LA PAGINA WEB############################################################
@app.route("/", methods=['POST', 'GET'])  # NOS DEJA MANDAR Y RECIIBR INFOR ADEMAS DEL LO NORMAL
def index():  # pagina principal
    # return render_template('ProbandoLive.html', **cargarTemplate())
    return render_template('index.html', **cargarTemplate())


###
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    global led1
    global led2
    global led3

    if deviceName == "temp" and action == "medir":
        redirect('/')
    if action == "BACK":
        redirect('/')
    if deviceName == "start" and action == "on":
        with open("AlarmaOn.txt", "r") as fp:
            data = fp.readline()
            valor = int(data.strip(), 10)
            fp.close()
            if valor == 1:
                valor = 0
            elif valor == 0:
                valor = 1
            f = open("AlarmaOn.txt", "w")
            f.write(str(valor))
            f.close()

        redirect('/')

    if deviceName == 'LED' and action == 'rasp1' and Server.BanderaRasp1:
        EnvioSinRespuesta(Server.RASP1, 'LED')
        led1 = not led1
    elif deviceName == 'LED' and action == 'rasp2' and Server.BanderaRasp2:
        EnvioSinRespuesta(Server.RASP2, 'LED')
        led2 = not led2
    elif deviceName == 'LED' and action == 'rasp3' and Server.BanderaRasp3:
        EnvioSinRespuesta(Server.RASP3, 'LED')
        led3 = not led3

    return render_template('index.html', **cargarTemplate())


count = 0


@app.route('/data', methods=["GET", "POST"])
def data():
    global count
    # Data Format
    # [TIME, Temperature, Humidity,RASP]
    tasks = Digital.query.order_by(Digital.date_created).all()  # devuelve la base de datos ordenada por fecha
    tasks2 = dbTermistor.query.order_by(dbTermistor.date_created).all()  # devuelve la base de datos ordenada por fecha
    Temperature = float(tasks[-1].content)
    Humidity = float(tasks2[-1].content)
    data = [time() * 1000, Temperature, Humidity, str(tasks[-1].raspberry)]
    # Temperature = random.random() * 100
    # Humidity = random.random() * 55
    # data = [time() * 1000, Temperature, Humidity,"RASP1"]
    count = count + 1
    response = make_response(json.dumps(data))

    response.content_type = 'application/json'

    return response


def getFechas():
    with open("FechaDesde.txt", "r") as fp:
        fechaDesde = fp.readline()
        separadosDesde = fechaDesde.split("-")
        añoDesde = int(separadosDesde[0])
        mesDesde = int(separadosDesde[1])
        diaDesde = int(separadosDesde[2])
    with open("FechaHasta.txt", "r") as fp:
        fechaHasta = fp.readline()
        separadosHasta = fechaHasta.split("-")
        añoHasta = int(separadosHasta[0])
        mesHasta = int(separadosHasta[1])
        diaHasta = int(separadosHasta[2])

    return añoDesde, mesDesde, diaDesde, añoHasta, mesHasta, diaHasta


ultimaDB = Digital.query.order_by(Digital.date_created.desc()).limit(100).all()


@app.route("/<basededatos>", methods=['POST', 'GET'])
def mostrardatos(basededatos):  # si llega mostrar entonces va a mostrar la base de datos
    global dbdatos
    cantidad = 100
    b = dbdatos
    pagina = 'index.html'
    if basededatos == 'FechaDesde':  # actualiazcion de th
        basededatos = 'mostrarDig'
        text = request.form['textFD']
        error = genericError(basededatos, text)
        if error == 0:  # control de errores generico de th
            f = open("FechaDesde.txt", "w")
            f.write(text)
            f.close()
        elif error == 1:
            print("error en fecha")
            return render_template('403.html')
    ###################################
    elif basededatos == 'FechaHasta':  # actualiazcion de th
        basededatos = 'mostrarDig'
        text = request.form['textFH']
        error = genericError(basededatos, text)
        print("llegue hasta antes de check error")
        if error == 0:  # control de errores generico de th
            f = open("FechaHasta.txt", "w")
            f.write(text)
            f.close()
            print("lescrbi puto mal dfaasdf")

        elif error == 1:
            print("error en fecha")
            return render_template('403.html')
        ##############################################################################
    if basededatos == 'FechaDesdeL':  # actualiazcion de th
        basededatos = 'mostrarLDR'
        text = request.form['textFD']
        error = genericError(basededatos, text)
        if error == 0:  # control de errores generico de th
            f = open("FechaDesde.txt", "w")
            f.write(text)
            f.close()
        elif error == 1:
           print("error en fecha")
           return render_template('403.html')
        ###################
    elif basededatos == 'FechaHastaL':  # actualiazcion de th
            basededatos = 'mostrarLDR'
            text = request.form['textFH']
            error = genericError(basededatos, text)
            print("llegue hasta antes de check error")
            if error == 0:  # control de errores generico de th
                f = open("FechaHasta.txt", "w")
                f.write(text)
                f.close()
                print(" dfaasdf")

            elif error == 1:
                print("error en fecha")
                return render_template('403.html')
            ######################################################################
    if basededatos == 'FechaDesdeT':  # actualiazcion de th
                basededatos = 'mostrarTer'
                text = request.form['textFD']
                error = genericError(basededatos, text)
                if error == 0:  # control de errores generico de th
                    f = open("FechaDesde.txt", "w")
                    f.write(text)
                    f.close()
                elif error == 1:
                    print("error en fecha")
                    return render_template('403.html')
            ############
    elif basededatos == 'FechaHastaT':  # actualiazcion de th
         basededatos = 'mostrarTer'
         text = request.form['textFH']
         error = genericError(basededatos, text)
         print("llegue hasta antes de check error")
         if error == 0:  # control de errores generico de th
                    f = open("FechaHasta.txt", "w")
                    f.write(text)
                    f.close()
                    print("mal dfaasdf")
         elif error == 1:
                    print("error en fecha")
                    return render_template('403.html')

    añoDesde, mesDesde, diaDesde, añoHasta, mesHasta, diaHasta = getFechas()

    if basededatos == 'plot.png':
        redirect('/plot.png')
        return dbdatos

    if basededatos == 'mostrarDig':  # = Digital.query.order_by(Digital.date_created.desc()).limit(cantidad).all()
        b = Digital.query.filter(Digital.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                              datetime(añoHasta, mesHasta, diaHasta))).order_by(
            Digital.date_created.desc()).limit(
            cantidad).all()
        pagina='mostrar.html'
    elif basededatos == 'mostrarLDR':
        b = dbLDR.query.filter(
            dbLDR.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                       datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbLDR.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarLDR.html'
        # dbLDR.query.filter(dbLDR.raspberry == 'Rasp1').order_by(dbLDR.date_created.desc()).limit(100).all()
        # b = dbLDR.query.filter(dbLDR.date_created.between('2020-10-10', '2020-10-22'))
        # return render_template('mostrarLDR.html', base=b)  # devuelve la base de datos

    elif basededatos == 'mostrarTer':
        # b = dbTermistor.query.order_by(dbTermistor.date_created.desc()).limit(cantidad).all()
        b = dbTermistor.query.filter(dbTermistor.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                                      datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbTermistor.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarTermistor.html'
    ############termistor
    if basededatos == 'RASP1T':
        b = dbTermistor.query.filter(dbTermistor.raspberry == 'RASP1',
                                     dbTermistor.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                                      datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbTermistor.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarTermistor.html'
    elif basededatos == 'RASP2T':
        b = dbTermistor.query.filter(dbTermistor.raspberry == 'RASP2',
                                     dbTermistor.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                                      datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbTermistor.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarTermistor.html'
    elif basededatos == 'RASP3T':
        b = dbTermistor.query.filter(dbTermistor.raspberry == 'RASP3',
                                     dbTermistor.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                                      datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbTermistor.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarTermistor.html'
    ############Digital
    if basededatos == 'RASP1D':
        b = Digital.query.filter(Digital.raspberry == 'RASP1',
                                 Digital.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                              datetime(añoHasta, mesHasta, diaHasta))).order_by(
            Digital.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrar.html'
    elif basededatos == 'RASP2D':
        b = Digital.query.filter(Digital.raspberry == 'RASP2',
                                 Digital.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                              datetime(añoHasta, mesHasta, diaHasta))).order_by(
            Digital.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrar.html'
    elif basededatos == 'RASP3D':
        b = Digital.query.filter(Digital.raspberry == 'RASP3',
                                 Digital.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                              datetime(añoHasta, mesHasta, diaHasta))).order_by(
            Digital.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrar.html'
    ###############################LDR
    if basededatos == 'RASP1L':
        b = dbLDR.query.filter(dbLDR.raspberry == 'RASP1',
                                 dbLDR.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                              datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbLDR.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarLDR.html'
    elif basededatos == 'RASP2L':
        b = dbLDR.query.filter(dbLDR.raspberry == 'RASP2',
                               dbLDR.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                          datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbLDR.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarLDR.html'
    elif basededatos == 'RASP3L':
        b = dbLDR.query.filter(dbLDR.raspberry == 'RASP3',
                               dbLDR.date_created.between(datetime(añoDesde, mesDesde, diaDesde),
                                                          datetime(añoHasta, mesHasta, diaHasta))).order_by(
            dbLDR.date_created.desc()).limit(
            cantidad).all()
        pagina = 'mostrarLDR.html'
    # try:
    #     largo = b.count()
    # except:
    #     largo = len(b)

    dbdatos = b

    templateData = {
        "base": b,
        #"largo": largo
    }
    return render_template(pagina, **templateData)  # devuelve la base de datos
    return render_template('mostrar.html', base=a)  # devuelve la base de datos


#################bloque para los textos
@app.route('/<cambio>/<tipo>', methods=['GET', 'POST'])
def update(cambio, tipo):  # modificar, n o agregue la templete de updat

    # if (request.method == 'POST' and cambio == 'cambiar'):
    #     #####################################################################################
    #     if (tipo == 'tm'):  # Actualizacion de tiempo de medida
    #         text = request.form['textTiempoDeMedida']
    #         processed_text = text
    #         # chequeo de errores
    #         if len(text) == 0:  # control de error de vacio
    #             return render_template('403.html')
    #         if float(processed_text) < 5:  # el tiempo de medida no puede ser menor a 5 segundos
    #             return render_template('403.html')
    #         f = open("TiempoDeMedida.txt", "w")
    #         f.write(processed_text)
    #         f.close()
    #     ########################################################################################
    #     elif (tipo == 'ta'):  # Acttualizacion de tiempo de alarma
    #         text = request.form['textTiempoDeAlarma']
    #         processed_text = text
    #         # chequeo de errores
    #         if len(text) == 0:
    #             return render_template('403.html')
    #         if int(text.strip(), 10) < 9:  # el tiempo de alarma no puede ser menor a 10 segundos
    #             return render_template('403.html')
    #         f = open("TiempoDeAlarma.txt", "w")
    #         f.write(processed_text)
    #         f.close()
    #         #####################################################################################
    #     elif (tipo == 'tl'):  # actualizacion de tl
    #         text = request.form['textTl']
    #         processed_text = text
    #         # chequeo de errores
    #         if len(text) == 0:  # tl no puede ser vacio
    #             return render_template('403.html')
    #         f = open("AlarmaTEMPlow.txt", "w")
    #         f.write(processed_text)
    #         f.close()
    #         #####################################################################################
    #     elif (tipo == 'th'):  # actualiazcion de th
    #         text = request.form['textTh']
    #         processed_text = text
    #         # chequeo de errores
    #         if len(text) == 0:  # th no puede ser vacio
    #             return render_template('403.html')
    #         f = open("AlarmaTEMPHig.txt", "w")
    #         f.write(processed_text)
    #         f.close()
    #         #####################################################################################
    #     elif (tipo == 'sm'):  # ACA LLAMAR A LA FUNCION CHECKMAIL
    #         text = request.form['textDestino']
    #         processed_text = text
    #         if len(text) == 0:  # th no puede ser vacio
    #             return render_template('403.html')
    #         # EN ESTA LINEA DE CODIGO LLAMA A LA FUNCION CHECKMAIL, UNA VEZ VERIFICADO QUE NO ES VACIO HAY QUE VER QUE SEA VALIDA LA DIRECCION
    #         f = open("Destino.txt", "w")
    #         f.write(processed_text)
    #         EnvioSinRespuesta(Server.RASP1, "D" + processed_text)
    #         EnvioSinRespuesta(Server.RASP2, "D" + processed_text)
    #         EnvioSinRespuesta(Server.RASP3, "D" + processed_text)
    #         f.close()
    #         #####################################################################################
    #
    #     return render_template('index.html', **cargarTemplate())
    if (request.method == 'POST' and cambio == 'cambiar'):
        print(tipo)
        #####################################################################################
        if tipo == 'tm':  # Actualizacion de tiempo de medida
            text = request.form['textTiempoDeMedida']
            # chequeo de errores
            error = genericError(tipo, text)
            if error == 0:  # control de error de tm
                f = open("TiempoDeMedida.txt", "w")
                f.write(text)
                f.close()
            elif error == 1:
                print("error en tiempo de medida")
                return render_template('403.html')
        ########################################################################################
        elif (tipo == 'ta'):  # Acttualizacion de tiempo de alarma
            text = request.form['textTiempoDeAlarma']
            # chequeo de errores
            error = genericError(tipo, text)
            if error == 0:  # control de errores de ta
                f = open("TiempoDeAlarma.txt", "w")
                f.write(text)
                f.close()
            elif error == 1:
                print("error en tiempo de  alarma")
                return render_template('403.html')
            #####################################################################################
        elif (tipo == "tl"):  # actualizacion de tl
            text = request.form['textTl']
            error = genericError(tipo, text)
            if error == 0:  # control de errores de tl
                f = open("AlarmaTEMPlow.txt", "w")
                f.write(text)
                f.close()
            elif error == 1:
                print("error en tl")
                return render_template('403.html')
            #####################################################################################
        elif tipo == 'th':  # actualiazcion de th
            text = request.form['textTh']
            error = genericError(tipo, text)
            if error == 0:  # control de errores generico de th
                f = open("AlarmaTEMPHig.txt", "w")
                f.write(text)
                f.close()
            elif error == 1:
                print("error en th")
                return render_template('403.html')
            #####################################################################################

            #####################################################################################
        elif tipo == 'sm':
            text = request.form['textDestino']
            error = genericError(tipo, text)
            if error == 0:  # control de errores generico de direccion
                f = open("Destino.txt", "w")
                f.write(text)
                f.close()
                EnvioSinRespuesta(Server.RASP1, "D" + text)
                EnvioSinRespuesta(Server.RASP2, "D" + text)
                EnvioSinRespuesta(Server.RASP3, "D" + text)
            elif error == 1:
                print("error")
                return render_template('403.html')

    return render_template('index.html', **cargarTemplate())


#####################################################
def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


############################# HILO DE ALARMAS ##########################################################################


############################################################################################################


if __name__ == "__main__":
    def Web():
        app.run(host='0.0.0.0', port=80, debug=True, threaded=True, use_reloader=False)  # server

    t2 = threading.Thread(target=Server.Server)
    t3 = threading.Thread(target=Web)
    t2.start()
    t3.start()
    t2.join()
    t3.join()
