import LibreriaFunciones as funciones
from LibreriaFunciones import time
import RPi.GPIO as GPIO
from LibreriaFunciones import np
from LibreriaFunciones import truncate
from LibreriaFunciones import circular



mostrarPrints = False  # bandera para decidir si mostrar todos los prints o no
lstLDR = []
tiempoamedida = 5;
Luxs = 0;

# #####################################################################################################
def setearLDR():
    GPIO.setup(33, GPIO.OUT)  # carga el capacitor
    GPIO.setup(38, GPIO.OUT)  # tierra, durante la carga
    GPIO.setup(35, GPIO.IN)  # abierto
    GPIO.setup(36, GPIO.IN)  # mide el capacitor, esta abierto
    GPIO.output(33, 1)  # high
    GPIO.output(38, 0)  # low


def dischargeLDR():
    global tiempoamedida
    GPIO.setup(33, GPIO.IN)  # abro
    GPIO.setup(38, GPIO.IN)  # abro, era la tierra en carga
    GPIO.setup(35, GPIO.OUT)  # tierra
    GPIO.output(35, False)  # tierra seteada
    with open("TiempoDeMedida.txt", "r") as fp:  # tiempo entre medidas, traducido a descarga del capacitor
        data = fp.readline()
        tiempoamedida = int(data.strip(), 10)
    time.sleep(tiempoamedida)


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
    print("Tiempo  teorico =" + str((r2 + Rf) * (cons * Cap)))
    R = (time ) / (cons * Cap) 
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

    global lstLDR
    global Luxs
    try:
        while True:
            setearLDR()
            timer_b = time.time()

            while True:  # this will carry on until you hit CTRL+C

                if GPIO.input(36):  # if port 10 == 1 voltaje en capacitor
                    t = time.time()  # tiempo hasta ahi
                    GPIO.output(33, 0)  # paro el voltaje de entrada
                    GPIO.setup(33, GPIO.IN)  # abro el circuito
                    try:
                        a = ldr(t - timer_b, R2=0)
                        Imprimo(("temp =" + str(a)))
                        Imprimo(("t hasta llegar a high =" + str(t - timer_b)))
                        print("LUX MEDIDA " + str(a))
                        Luxs = circular(lstLDR, a)
                        dischargeLDR()  # esta es concurrente

                        break  # me lleva al primer while
                    except:
                        print("el tiempo no cumple la eq")
                        dischargeLDR()
                        break

    finally:  # this block will run no matter how the try block exits
        GPIO.cleanup()