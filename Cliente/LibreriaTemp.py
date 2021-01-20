import LibreriaFunciones as funciones
from LibreriaFunciones import time
import RPi.GPIO as GPIO
from LibreriaFunciones import np
from LibreriaFunciones import truncate
from LibreriaFunciones import circular
from LibreriaFunciones import mandaMail

GPIO.setmode(GPIO.BOARD)

mostrarPrints=True  # bandera para decidir si mostrar todos los prints o no
lstTEMP = []
tiempoamedida=5;
TempTermistor=0;

def Imprimo(funcprint):
    global imprimo
    if mostrarPrints:
        print(funcprint)

# #####################################################################################################
def setear():
    GPIO.setup(8, GPIO.OUT) #carga el capacitor
    GPIO.setup(18, GPIO.OUT) #tierra, durante la carga
    GPIO.setup(16, GPIO.IN)  #abierto
    GPIO.setup(10, GPIO.IN)  #mide el capacitor, esta abierto
    GPIO.output(8, 1) #high
    GPIO.output(18, 0) #low


def discharge():
    global tiempoamedida
    GPIO.setup(8, GPIO.IN) #abro
    GPIO.setup(18, GPIO.IN) #abro, era la tierra en carga
    GPIO.setup(16, GPIO.OUT) #tierra
    GPIO.output(16, False) #tierra seteada
    with open("TiempoDeMedida.txt", "r") as fp:  # tiempo entre medidas, traducido a descarga del capacitor
        data = fp.readline()
        tiempoamedida = int(data.strip(), 10)
    time.sleep(tiempoamedida)


####################################################################################################
def temp(time):
    Rf = 9030
    # R2 = int(input("cuanto es la Rmedida"))
    Cap = 0.0001
    Vt = 1.10
    Vs = 3.27
    t = 0
    # b = 3799
    b = 3977
    A = 3.354016 * 10 ** (-3)
    B = 2.569850 * 10 ** (-4)
    C = 2.620131 * 10 ** (-6)
    D = 6.383091 * 10 ** (-8)
    Rt = 10000

    cons = -np.log(1 - Vt / Vs)
    Imprimo(("constante es " + str(cons)))
    R = (time - 0.10) / (cons * Cap) - Rf
    Imprimo(("valor de la R al t medido =" + str(R)))
    temp = (A + B * np.log(R / Rt) + C * (np.log(R / Rt)) ** 2 + D * (np.log(R / Rt)) ** 3) ** (-1)
    Imprimo(("temperatura al t medido= " + str(temp - 273)))
    # temp2 = (A + B * np.log(r2 / Rt) + C * (np.log(r2 / Rt)) ** 2 + D * (np.log(r2 / Rt)) ** 3) ** (-1)
    # print("valor practico de la temperatura =" + str(temp2 - 273.15))
    temp = truncate(temp, 2)
    return temp - 273.15

def alarmaTEMP():  ###
    global lstTEMP
    while True:  # si esta uno esta activada la arlma:
        try:
            with open("AlarmaOn.txt", "r") as fp:  # lee si esta alarma activada
                data = fp.readline()
                bandera = int(data.strip(), 10)
    
            if len(lstTEMP) > 0 and bandera == 1:
                print("entro a alarma")
    
                with open("TiempoDeAlarma.txt", "r") as fp:  # cuando se activa la arlama duerme ese tiempo
                    data = fp.readline()
                    tiempoalarma = int(data.strip(), 10)
                with open("AlarmaTEMPHig.txt", "r") as fp:  # lee el thigh
                    data = fp.readline()
                    th = int(data.strip(), 10)
                with open("AlarmaTEMPlow.txt", "r") as fp:  # lee el thigh
                    data = fp.readline()
                    tl = int(data.strip(), 10)
                print("th,tl y ultimo valor",th,tl,lstTEMP[-1])    
                if th <= lstTEMP[-1]:
                    print("Mail, mandado T alta, esprando t")
                    if th > tl:  # SOLO ENVIO ALARMAS SI TH ES MAYOR QUE TL
                        mandaMail("Alerta por temperatura alta")
                        time.sleep(tiempoalarma)  # leer de txt
    
                if tl >= lstTEMP[-1]:
                    print("Mail, mandado T low, esprando t")
                    if th > tl:  # SOLO ENVIO ALARMAS SI TH ES MAYOR QUE TL
                        mandaMail("Alerta por temperatura baja")
                        time.sleep(tiempoalarma)  # leer de txt
        except:
            print("error en alarma algo fallo")                        

# os.nice(-18)
def medirTEMP():
    global TempTermistor
    try:
        while True:
            setear()
            timer_b = time.time()

            while True:  # this will carry on until you hit CTRL+C

                if GPIO.input(10):  # if port 16 == 1
                    t = time.time()
                    GPIO.output(8, 0)  # set port/pin value to 0/LOW/False
                    GPIO.setup(8, GPIO.IN)

                    try:
                        a = temp(t - timer_b)
                        Imprimo(("temp =" + str(a)))
                        Imprimo(("t hasta llegar a high =" + str(t - timer_b)))
                        print("temperatura promedio " + str(a))
                        TempTermistor=circular(lstTEMP, a)
                        print(TempTermistor)
                        discharge()

                        break
                    except:
                        print("el tiempo no cumple la eq")
                        discharge()
                        break

    finally:  # this block will run no matter how the try block exits
        # GPIO.output(8, 0)
        GPIO.cleanup()  # clean up after yourse
###########################
lstLDR = []
tiempoamedida = 5;
Luxs = 0;

# #####################################################################################################
def setearLDR():
    GPIO.setup(19, GPIO.OUT)  # carga el capacitor
    GPIO.setup(23, GPIO.OUT)  # tierra, durante la carga
    GPIO.setup(15, GPIO.IN)  # abierto
    GPIO.setup(22, GPIO.IN)  # mide el capacitor, esta abierto
    GPIO.output(19, 1)  # high
    GPIO.output(23, 0)  # low


def dischargeLDR():
    global tiempoamedida
    GPIO.setup(19, GPIO.IN)  # abro
    GPIO.setup(23, GPIO.IN)  # abro, era la tierra en carga
    GPIO.setup(15, GPIO.OUT)  # tierra
    GPIO.output(15, False)  # tierra seteada
    with open("TiempoDeMedida.txt", "r") as fp:  # tiempo entre medidas, traducido a descarga del capacitor
        data = fp.readline()
        tiempoamedida = int(data.strip(), 10)
    time.sleep(tiempoamedida)


# def ldr(time, r2):
#     Rf = 0  # fijo
#     # R2 = int(input("cuanto es la Rmedida n el LDR"))
#     Cap = 0.0001  # fijo
#     Vt = 1.10  # fijo, pero discutible, varia
#     Vs = 3.27  # entrada, medido con voltimetro
#     R0 = 12300
#     L0 = 110
#     alpha = 0.7
#     cons = -np.log(1 - Vt / Vs)
#     print("LDR Tiempo  teorico =" + str((r2 + Rf) * (cons * Cap)))
#     R = (time ) / (cons * Cap) - Rf
#     print("lDR valor de la R al t medido =" + str(R))
#     #cons2 = np.log(L0, 10) - (1 / alpha) * np.log(R / R0, 10)
#     #L = 10 ** cons2
#     L = 1.25 * pow(10, 7) * pow(R, -1.4059)
#     print("LDR L al t medido= " + str(L))
#     # cons2 = np.log(L0, 10) - (1 / alpha) * np.log(R2 / R0, 10)
#     # L2 = 10 ** cons2
#     # print("valor teorico de L =" + str(L2))
#     #L = truncate(L, 2)
#     return L

def ldr(time, r2):
    Rf = 8920  # fijo
    # R2 = int(input("cuanto es la Rmedida n el LDR"))
    Cap = 0.0001  # fijo
    Vt = 1.10  # fijo, pero discutible, varia
    Vs = 3.27  # entrada, medido con voltimetro
    R0 = 12300
    L0 = 110
    alpha = 0.7
    cons = -np.log(1 - Vt / Vs)
    print("Tiempo  teorico =" + str((r2 ) * (cons * Cap)))
    R = (time ) / (cons * Cap) 
    print("valor de la R al t medido =" + str(R))
    cons2 = np.math.log(L0, 10) - (1 / alpha) * np.math.log(R / R0, 10)
    L = 10 ** cons2
    print("L al t medido= " + str(L))
    # cons2 = np.log(L0, 10) - (1 / alpha) * np.log(R2 / R0, 10)
    # L2 = 10 ** cons2
    # print("valor teorico de L =" + str(L2))
    L = truncate(L, 2)
    return L

def medirLDR():  # VERSION REAL DE MEDICION LDR
    dischargeLDR()
    global lstLDR
    global Luxs
    try:
        while True:
            setearLDR()
            timer_b = time.time()

            while True:  # this will carry on until you hit CTRL+C

                if GPIO.input(22):  #
                    t = time.time()  # tiempo hasta ahi
                    GPIO.output(19, 0)  # paro el voltaje de entrada
                    GPIO.setup(19, GPIO.IN)  # abro el circuito
                    a = ldr(t - timer_b, 0)  #le paso el tiempo que transcurrio mientras media
                    try:
                       
                        Imprimo(("LUX =" + str(a)))
                        Imprimo(("t hasta llegar a high LDR =" + str(t - timer_b)))
                        print("LUX MEDIDA " + str(a))
                        Luxs = circular(lstLDR, a)
                        dischargeLDR()  # esta es concurrente

                        break  # me lleva al primer while
                    except:
                        print("el tiempo no cumple la eq LDR")
                        dischargeLDR()
                        break

    finally:  # this block will run no matter how the try block exits
        GPIO.cleanup()