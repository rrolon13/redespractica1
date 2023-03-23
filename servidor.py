import socket
import sys, os
import numpy as np
import time
HOST = "172.100.72.1"  # Direccion de la interfaz de loopback estándar (localhost)
PORT = 65432  # Puerto que usa el cliente  (los puertos sin provilegios son > 1023)
buffer_size = 1024

cont_serv = 0
cont_clie = 0

t = []

palabras1 = ["arbol", "avion", "barco", "moto", "casa", "compu", "tele", "mesa"]
palabras2 = ["arbol", "avion", "barco", "moto", "casa", "compu", "tele", "mesa"
             ,"silla", "banco", "cama", "sillon", "planta", "carro", "camion", 
             "celu", "libro", "vaso"]

tablero = [[]]



def tiro(size, tablero):
    tiro1 = []
    tiro2 = []
    tiro1.append(np.random.randint(0, size))
    tiro1.append(np.random.randint(0, size))
    while True:
        tiro2.append(np.random.randint(0, size))
        tiro2.append(np.random.randint(0, size))
        if tiro2[0] == tiro1[0] and tiro2[1] != tiro1[1]:
            break
        elif tiro1[0] != tiro2[0] and tiro1[1] == tiro2[1]:
            break
        elif tiro1[0] != tiro2[0] and tiro1[1] != tiro2[1]:
            break
    print(tablero [tiro1[0]] [tiro1[1]] )
    print(tablero[tiro2[0]] [tiro2[1]] )
    if  tablero[tiro1[0]][tiro1[1]] == tablero[tiro2[0]][tiro2[1]] and \
        tablero[tiro2[0]][tiro2[1]] != None and tablero[tiro1[0]][tiro1[1]] != None:
        global cont_serv
        cont_serv = cont_serv + 1
        global t
        t.clear()
        t.append(tiro1[0])
        t.append(tiro1[1])
        t.append(tiro2[0])
        t.append(tiro2[1])
        print(t)
        tablero[tiro1[0]][tiro1[1]] = None
        tablero[tiro2[0]][tiro2[1]] = None
        return 1
    else:
        return 0

def imprimeTablero(size, tablero):
    for i in range (0, size):
        for j in range(0, size):
            print(tablero[i][j], end="\t")      
        print("")   

def generador(size, palabras):
    valor = int(((size*size)/2))
    tablero = [[None]*size for _ in range (size)]
    #print("valor", valor)
    for j in range (0, valor):
        i = 0
        while i != 2:
            fila= np.random.randint(0,size)
            columna = np.random.randint(0, size)
            if tablero[fila][columna] == None:
                tablero[fila][columna] = palabras[j]
                i = i + 1 
    imprimeTablero(size, tablero)     
    return tablero


def validaTiro(data1, data2, tablero):
    tiro1 = []
    tiro2 = []
    data1 = str(data1, "utf-8")
    data1.split(',')
    data2 = str(data2, "utf-8")
    data2.split(',')
    tiro1.append(int(data1[0]))
    tiro1.append(int(data1[2]))
    tiro2.append(int(data2[0]))
    tiro2.append(int(data2[2]))
    print(tablero [tiro1[0]-1] [tiro1[1]-1] )
    print(tablero[tiro2[0]-1] [tiro2[1]-1] )
    if  tablero[tiro1[0]-1][tiro1[1]-1] == tablero[tiro2[0]-1][tiro2[1]-1] and \
        tablero[tiro2[0]-1][tiro2[1]-1] != None and tablero[tiro1[0]-1][tiro1[1]-1] != None:
        global cont_clie
        cont_clie = cont_clie + 1
        tablero[tiro1[0]-1][tiro1[1]-1] = None
        tablero[tiro2[0]-1][tiro2[1]-1] = None
        return 1
    else:
        return 0

                  
    
def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPServerSocket:
        TCPServerSocket.bind((HOST, PORT)) #se pone disponible el servidor
        TCPServerSocket.listen()
        print("El servidor TCP está disponible y en espera de solicitudes")
        #generador(4)

        Client_conn, Client_addr = TCPServerSocket.accept()
        with Client_conn:
            print("Conectado a", Client_addr)
            inicio = time.time()
            print("Esperando a recibir datos... ")
            data = Client_conn.recv(buffer_size)
            print("Dificultad ", int(data))
            if int(data) == 1:
                size = 4
                limite = ((size*size)/2)
                tablero = generador(size, palabras1)
            else:
                size = 6
                limite = ((size*size)/2)
                tablero = generador(size, palabras2)
            print("Enviando respuesta a", Client_addr)
            Client_conn.sendall(b"Tablero generado")
            while True:
                imprimeTablero(size, tablero)
                print("Esperando a recibir tiros... ")
                data1 = Client_conn.recv(buffer_size)
                if not data1:
                    break
                Client_conn.sendall(b"Primer tiro recibido")
                data2 = Client_conn.recv(buffer_size)
                if not data2:
                    break
                valida = validaTiro(data1, data2, tablero)
                #print("Prueba de retorno: ", valida)
                Client_conn.sendall(bytes(str(valida), "utf-8"))
                while valida == 0:
                    data = Client_conn.recv(buffer_size)
                    print(repr(data))
                    valor = tiro(size,tablero)
                    if valor == 1:
                        Client_conn.sendall(b"La computadora ha acertado, le toca otra vez")
                        data = Client_conn.recv(buffer_size)
                        valida == 0
                        Client_conn.sendall(bytes(str(valida), "utf-8"))
                        data = Client_conn.recv(buffer_size)
                        Client_conn.sendall(bytes(str(t[0]), "utf-8"))
                        data = Client_conn.recv(buffer_size)
                        Client_conn.sendall(bytes(str(t[1]), "utf-8"))
                        data = Client_conn.recv(buffer_size)
                        Client_conn.sendall(bytes(str(t[2]), "utf-8"))
                        data = Client_conn.recv(buffer_size)
                        Client_conn.sendall(bytes(str(t[3]), "utf-8"))

                    else:
                        Client_conn.sendall(b"La computadora ha fallado, es tu turno")
                        data = Client_conn.recv(buffer_size)
                        valida = 1
                        Client_conn.sendall(bytes(str(valida), "utf-8"))
                data = Client_conn.recv(buffer_size)
                print("contador servidor: ", cont_serv)
                print("contador cliente:", cont_clie)
                if cont_clie == limite or cont_serv == limite or cont_clie+cont_serv == limite:
                    break
                Client_conn.sendall(b"0")
            Client_conn.sendall(b"1")
            if cont_clie > cont_serv:
                Client_conn.sendall(b"Usted ha ganado!!!!!!!!!!!")
            elif cont_clie < cont_serv:
                Client_conn.sendall(b"Usted ha perdido ):")
            else:
                Client_conn.sendall(b"El juego ha quedado en empate")
            data = Client_conn.recv(buffer_size)
            fin = time.time()
            Client_conn.sendall(bytes(str(fin-inicio), "utf-8"))


if __name__ == '__main__':
        try:
            main()
        except KeyboardInterrupt:
            print('Servidor finalizado')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)
