import datetime
import smtplib
import threading
from datetime import datetime
import time
from time import sleep

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from numpy import random
import math
import math as np

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(26, GPIO.OUT)
GPIO.output(26, 0)

lstTEMP = []
lstLDR = []
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Todo.db'  # data base
app.config['SQLALCHEMY_BINDS'] = {'dbLDR': 'sqlite:///dbLDR.db',
                                  'three': 'sqlite:///dbextra.db'}
db = SQLAlchemy(
    app)

SQLALCHEMY_TRACK_MODIFICATIONS = False


# en la terminal hay que escribir en python, from "nombre de la .py,Server" import db y despues db.create_all()


class Todo(db.Model):  # database detemp

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id  # retorna la tas yla id

    def temperatura(self):
        return str(id)


class dbLDR(db.Model):  # database de LDR
    __bind_key__ = 'dbLDR'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r>' % self.id  # retorna la task yla id

    def lux(self):
        return str(id)


class Three(db.Model):
    __bind_key__ = 'three'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())


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


#############################  COMIENZA MEDICION REAL NO SIMULADA LDR ########################################################
def setear2():
    GPIO.setup(7, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(22, GPIO.IN)
    GPIO.setup(13, GPIO.IN)  # set GPIO24 as an input high or low (LED)
    GPIO.output(7, 1)
    GPIO.output(15, 0)


def discharge2():
    GPIO.setup(7, GPIO.IN)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, False)

    with open("TiempoDeMedida.txt", "r") as fp:  # lee el thigh
        data = fp.readline()
        tiempoDeMedida = int(data.strip(), 10)
    time.sleep(tiempoDeMedida)


def circular(lista, valor, database):
    lista.append(valor)
    a = len(lista)
    b = sum(lista) / a
    if a == 4:
        new_task = database(content=b)
        lista.pop(0)
        try:
            db.session.add(new_task)
            db.session.commit()
        except:
            return 'Error al guardar valores en la base de datos'

    return b


def ldr(time, r2):
    Rf = 330  # fijo
    # R2 = int(input("cuanto es la Rmedida n el LDR"))
    Cap = 0.0001  # fijo
    Vt = 1.10  # fijo, pero discutible, varia
    Vs = 3.27  # entrada, medido con voltimetro

    R0 = 10000;
    L0 = 300
    alpha = 0.8
    cons = -np.log(1 - Vt / Vs)

    print("Tiempo  teorico =" + str((r2 + Rf) * (cons * Cap)))

    R = (time - 0.10) / (cons * Cap) - Rf

    print("valor de la R al t medido =" + str(R))
    cons2 = np.log(L0, 10) - (1 / alpha) * np.log(R / R0, 10)
    L = 10 ** cons2
    print("L al t medido= " + str(L))

    # cons2 = np.log(L0, 10) - (1 / alpha) * np.log(R2 / R0, 10)
    # L2 = 10 ** cons2
    # print("valor teorico de L =" + str(L2))
    L = truncate(L, 2)
    return L


def medirLDR():  # VERSION REAL DE MEDICION LDR

    # os.nice(-18)
    try:
        while True:
            setear2()
            timer_b = time.time()

            while True:  # this will carry on until you hit CTRL+C

                if GPIO.input(10):  # if port 10 == 1 voltaje en capacitor
                    t = time.time()  # tiempo hasta ahi
                    GPIO.output(8, 0)  # paro el voltaje de entrada
                    GPIO.setup(8, GPIO.IN)  # abro el circuito

                    try:
                        a = ldr(t - timer_b, R2=0)
                        # sistema de alarma lee las alarmas
                        print("temp =" + str(a))
                        print("t hasta llegar a high =" + str(t - timer_b))
                        print(circular(lstLDR, a, dbLDR))  # promedio

                        discharge2()  # esta es concurrente

                        break  # me lleva al primer while
                    except:
                        print("el tiempo no cumple la eq")
                        discharge2()
                        break

    finally:  # this block will run no matter how the try block exits
        # GPIO.output(8, 0)
        GPIO.cleanup()


medirLDR()
