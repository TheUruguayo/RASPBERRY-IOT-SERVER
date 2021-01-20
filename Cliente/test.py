# cd Desktop/raspiproj
#!/usr/bin/python
import sys;sys.path.append(r'C:\Users\Ignac\.p2\pool\plugins\org.python.pydev.core_8.0.1.202011071328\pysrc')
#import pydevd
#pydevd.settrace()
import sys
sys.path.append(r'/home/pi/Desktop/pysrc')
#import pydevd
#pydevd.settrace('192.168.1.7') # replace IP with address
                                # of Eclipse host machine
                                
                                
#######################                                #####################
import LibreriaTemp
import socket
import sys
import threading
import time
import numpy as np
from time import sleep
import LibreriaFunciones


##
#import Libraria
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()
temperature="hola" ##auxiliares para probar

salida=10 ##auxiliar para probar es para los oops
conectado=False #bandera
############################TCP
def medirTEMPDigital():    
    
    while True:        
        try:
            global temperature 
            temperature = sensor.get_temperature()
            Envio(temperature,"T")
            print("SENSOR DIGITAL %s celsius" % temperature)        
            #temperatura = Libraria.circular(lstTEMP,temperature)
            #Envio(temperature)
            print(temperature)        
            time.sleep(LibreriaTemp.tiempoamedida)        
        except:
            print("error druante medicion")
            sensor = W1ThermSensor()
###############################cliente tcp

ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
# Connect the socket to the port where the server is listening
server_address = ("192.168.1.7", 5500)
#
#ms.connect(server_address)

############################GPIO#########################
import RPi.GPIO as GPIO

###############################################################
def Reconect():
    global conectado
    global ms
    while True:
      if(not conectado):
        try:
            sleep(1)
            print(sys.stderr, 'connecting to %s port %s' % server_address)
            ms.connect(server_address)
            print("Server connected") 
            LibreriaFunciones.ApagarLed()           
            conectado = True
        except:
            ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      else:
        try:
            sleep(5)
            res = bytes("Checkeo la Conexion", encoding='utf-8')
            #print(sys.stderr, 'sending "%s"' % enviar)
            ms.sendall(res) 
        except:
            print("Server not connected")
            ms = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conectado = False
            pass
        sleep(5)
    ms.close()
    
def Envio(dato,tipo): #pide dato a enviar en y el tipo
    global conectado
    if conectado:            
        try:        
            # HAY QUE LLAMAR A ALARMA
            #count+=1            
            sleep(5)    
            res = bytes(tipo+str(dato)[0:6], encoding='utf-8')
            #print(sys.stderr, 'sending "%s"' % enviar)
            ms.sendall(res)            
        except:
            print(sys.stderr)
            ms.close()
            conectado=False

    
def Recibir():
    global conectado
    while True:
        if conectado:
            
            while True and conectado:
                try:    
                    print("El server responde")
                    data = ms.recv(1000)
                    data=data.decode("utf-8")
                    LibreriaFunciones.Opciones(data)            
                    
                except:
                    print(sys.stderr)
                    print("Se cerro la conexion")
                    #ms.close()
                    conectado=False
                    break
        
        
def EnviarTempAnalogica():
    while True:
        print("loingitud del array",len(LibreriaTemp.lstTEMP))
        if len(LibreriaTemp.lstTEMP)==3:
            Envio(LibreriaTemp.TempTermistor, "A")
            
        sleep(LibreriaTemp.tiempoamedida) 
        
def EnviarLDR():
    while True:
        print("loingitud del array ldr",len(LibreriaTemp.lstLDR))
        if len(LibreriaTemp.lstTEMP)==3:
            Envio(LibreriaTemp.Luxs, "L")            
        sleep(LibreriaTemp.tiempoamedida)        

                 
#####################################################################################################################################        
if __name__ == "__main__":
    ## CREACION DE HILOS QUE SIMULAN BLOQUES, ACTUALMENTE UTILIZAMOS FUNCIONES TEORICAS DE SIMULACION, CAMBIAR MEDIRtemp POR MEDIR TEMP REAL QUE ESTA COMENTADA
    t0=threading.Thread(target=Reconect) 
    t1 = threading.Thread(target=LibreriaTemp.medirTEMP)  # funcion/clase modulo medir temperatura
    t2 = threading.Thread(target=medirTEMPDigital)  # funcion/clase modulo medir temperatura
    t3 = threading.Thread(target=EnviarTempAnalogica)  # funcion/clase modulo medir temperatura
    t4 = threading.Thread(target=Recibir)                # funcion/clase modulo medir temperatura
    t5 = threading.Thread(target=LibreriaTemp.alarmaTEMP)
    t6 = threading.Thread(target=LibreriaTemp.medirLDR)  # funcion/clase modulo medir temperatura
    t7=  threading.Thread(target=EnviarLDR)  # funcion/clase modulo medir temperatura
    
    t0.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    
    t0.join()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()      
    t7.join()           
