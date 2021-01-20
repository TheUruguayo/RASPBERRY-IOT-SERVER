import math
import smtplib
import time
import RPi.GPIO as GPIO
import numpy as np
from time import sleep

###########################################LED
GPIO.setmode(GPIO.BOARD)
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, 0)
def BlinkLed():
    if GPIO.input(5):
        GPIO.output(5, 0)
    else:
        GPIO.output(5, 1)
        
        
############################Opciones
def ApagarLed():
    GPIO.output(5, 0)
    


def Opciones(cadena):
            bandera=True
            f = open("AlarmaTEMPHig.txt", "r")
            f.close()      
            print("ANTES DEL SPLIT",cadena) 
            cadena=cadena.split("x")
            print("entro en el loop con",cadena)
            for dato in cadena: 
                if len(dato)==0:
                   break
                if dato == "LED":
                    bandera=False
                    BlinkLed()                
                elif dato[0] == "H":#cambio de temperatura high                
                    print("ahora respuesta del server cambia Th")
                    salida = dato.replace("H", '')
                    f = open("AlarmaTEMPHig.txt", "w")
                elif dato[0] == "L":#cambio de temperatura low                
                    print("ahora respuesta del server cambia Tl")
                    salida = dato.replace("L", '')
                    f = open("AlarmaTEMPlow.txt", "w")
                elif dato[0] == "M":#cambio de tiempo de medida
                    salida = dato.replace("M", '')
                    f = open("TiempoDeMedida.txt", "w")
                    print("ahora respuesta del server cambia tiempo de medida") 
                elif dato[0] == "a":#alarma on off                
                    print("ahora respuesta del server alarma on/off")
                    salida = dato.replace("a", '')
                    f = open("AlarmaOn.txt", "w")      
                elif dato[0] == "t":#tiempo entre alarmas
                    salida = dato.replace("t", '')
                    print("ahora respuesta del server tiempo entre alarmas")
                    f = open("TiempoDeAlarma.txt", "w")  
                elif dato[0] == "D":#tiempo entre alarmas
                    print("ahora respuesta del server cambiar destino")
                    salida = dato.replace("D", '')
                    f = open("Destino.txt", "w")    
                else: bandera=False    
                if bandera:     
                    print("se guardo",salida)            
                    f.write(salida)
                    f.close()


################INPUT DE LOS SENSORES

##################################################MANDAR MAILS
######################################FUNCION QUE SE ENCARGA DE MANDAR UN MAIL #######################################
def mandaMail(body):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
    except:
        print('Something went wrong...')

    gmail_user = 'your email'
    gmail_password = 'your password'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:
        print('Something went wrong...')

    sent_from = gmail_user
    to = ['mail1', 'mail2']
    subject = 'Alarma, se te prende fuego la choza'
    # body = ("Hey, whats up?\n\n- You")

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        with open("Destino.txt", "r") as fp:  # cuando se activa la arlama duerme ese tiempo
            data = fp.readline()
            destino = str(data)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, destino, email_text)
        server.close()


    except:
        print('Something went wrong...')

########################################################################################################################
##################################### SECCION DE FUNCIONES LOGICAS AUXILIARES ##########################################
########################################################################################################################

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


def circular(lista, valor):
    # def circular(lista, valor, database):
    lista.append(valor)
    a = len(lista)
    b = sum(lista) / a
    if a == 4:
        ###esto va para el cerver
        # new_task = database(content=b)
        lista.pop(0)
        # try:
        #     db.session.add(new_task)
        #     db.session.commit()
        # except:
        #     return 'Error al guardar valores en la base de datos'

    return b
