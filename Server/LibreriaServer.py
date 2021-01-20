import selectors
import socket
import types
from ServerDefensa import db
from ServerDefensa import leerYenviar
from ServerDefensa import SQLAlchemy
from ServerDefensa import Digital, dbTermistor, dbLDR
from ServerDefensa import datetime

mostrarPrints = True  # bandera para decidir si mostrar todos los prints o no
HOST = '192.168.1.9'  # Standard loopback interface address (localhost)
PORT = 5500  # Port to listen on (non-privileged ports are > 1023)
RASP1 = '192.168.1.14'
RASP2 = '192.168.1.3'
RASP3 = '192.168.1.2'

def Imprimo(funcprint):
    global imprimo
    if mostrarPrints:
        print(funcprint)


def queDatoEs(dato, rasp):  # a este hay que pasarle la rasp que fue detectada tambien asi queda pronto

    if dato[0] == "T":  # temperatura digital
        salida = 'T'
        dato = dato.replace(salida, '')
        try:
            new_task = Digital(content=dato, raspberry=rasp, date_created=datetime.now())
            print("adentro del digital", new_task.date_created.strftime("%Y-%m-%d %H:%M:%S"))
            db.session.add(new_task)
            db.session.commit()

        except:
            print('Error al guardar T digital en la base de datos')
            return
    elif dato[0] == "L":  # me mandaron luz
        salida = 'L'
        dato = dato.replace(salida, '')
        try:
            new_task = dbLDR(content=dato, raspberry=rasp, date_created=datetime.now())
            db.session.add(new_task)
            db.session.commit()
        except:
            print('Error al guardar Luxs digital en la base de datos')
            return
    elif dato[0] == "A":  # me mandaron Temperatura analogica
        salida = 'A'
        dato = dato.replace(salida, '')

        try:
            new_task = dbTermistor(content=dato, raspberry=rasp, date_created=datetime.now())
            db.session.add(new_task)
            db.session.commit()
        except:
            print('Error al guardar T termistor en la base de datos')
            return
    else:
        salida = "z"
        dato = "none"

    return salida, dato


def ConexionRasp(addr, conn):
    global ConnRasp1
    global ConnRasp2
    global ConnRasp3
    global PORTRASP1
    global PORTRASP2
    global PORTRASP3
    global BanderaRasp1
    global BanderaRasp2
    global BanderaRasp3

    if addr[0] == RASP1:
        PORTRASP1 = addr[1]
        ConnRasp1 = conn
        BanderaRasp1 = True
        mensaje = "hola te conectaste Rasp1"
    elif addr[0] == RASP2:
        PORTRASP2 = addr[1]
        ConnRasp2 = conn
        BanderaRasp2 = True
        mensaje = "hola te conectaste Rasp2"
    elif addr[0] == RASP3:
        PORTRASP3 = addr[1]
        ConnRasp3 = conn
        BanderaRasp3 = True
        mensaje = "hola te conectaste Rasp3"

    #Enviar(conn, addr, mensaje)
    leerYenviar()
    leerYenviar()
    Imprimo(print("la rasp 1 esta conectada?", BanderaRasp1))


def DesconectarRasp(addr):
    global BanderaRasp1
    global BanderaRasp2
    global BanderaRasp3
    Imprimo(print("desconectar a ver que diec", addr[0]))
    if addr[0] == RASP1:
        BanderaRasp1 = False
        mensaje = "Adios Rasp1"
    elif addr[0] == RASP2:
        BanderaRasp2 = False
        mensaje = "Adios Rasp2"
    elif addr[0] == RASP3:
        BanderaRasp3 = False
        mensaje = "Adios Rasp3"

    Imprimo(print("Tiene que decir false la rasp 1 esta conectada?", BanderaRasp1))


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    Imprimo(('accepted connection from', addr, conn))
    ConexionRasp(addr, conn)
    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)



def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        dispositivo = "NINGUNO"
        if data.addr[0] == RASP1:
            Imprimo(("esta info es de la RASP1 aca se tiene que agarrar los datos y guardar"))
            dispositivo = "RASP1"
        elif data.addr[0] == RASP2:
            Imprimo(("esta info es de la RASP2 aca se tiene que agarrar los datos y guardar"))
            dispositivo = "RASP2"
        elif data.addr[0] == RASP3:
            Imprimo(("esta info es de la RASP3 aca se tiene que agarrar los datos y guardar"))
            dispositivo = "RASP3"
        if recv_data:
            data.outb += recv_data
        else:
            Imprimo(('closing connection to', data.addr))
            DesconectarRasp(data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            Imprimo(('echoing', repr(data.outb), 'to', data.addr))
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]
            Imprimo(((queDatoEs(recv_data.decode("utf-8"), dispositivo))))


def Enviar(conn, addr, data):
    Imprimo(('Envio a:', addr, str(data)))
    mensaje = bytes(str(data), encoding='utf-8')
    conn.sendall(mensaje)


def Send(addr, data):
    global BanderaRasp1
    global BanderaRasp2
    global BanderaRasp3
    if addr == RASP1 and BanderaRasp1:
        Enviar(ConnRasp1, RASP1, data)
    elif addr == RASP2 and BanderaRasp2:
        Enviar(ConnRasp2, RASP2, data)
    elif addr == RASP3 and BanderaRasp3:
        Enviar(ConnRasp3, RASP3, data)



PORTRASP1 = ''
PORTRASP2 = ''
PORTRASP3 = ''
ConnRasp1 = None
ConnRasp2 = None
ConnRasp3 = None
BanderaRasp1 = False
BanderaRasp2 = False
BanderaRasp3 = False

sel = selectors.DefaultSelector()
lsock = None
# ...

if lsock is None:
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("entre a init")
    lsock.bind((HOST, PORT))
    lsock.listen()
    print('Server en', (HOST, PORT))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)


def Server():
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
