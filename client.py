import socket
import sys, os
import time

#HOST = "192.168.1.80"  # The server's hostname or IP address
PORT = 65432  # The port used by the server
buffer_size = 1024

print("Ingresa la direccion IP del servidor")
HOST = input()


def actualizaTablero(data1, data2, tablero):
    tiro1 = []
    tiro2 = []
    data1.split(',')
    data2.split(',')
    tiro1.append(int(data1[0]))
    tiro1.append(int(data1[2]))
    tiro2.append(int(data2[0]))
    tiro2.append(int(data2[2]))
    tablero [tiro1[0]-1] [tiro1[1]-1] = "-"
    tablero[tiro2[0]-1] [tiro2[1]-1] = "-"

def imprimeTablero(size, tablero):
    num2 = 1
    print("\t", end="")
    for i in range(0,size):
        print(i+1, end="\t")
    print("")
    for i in range (0, size):
        print(num2, end="\t")
        for j in range(0, size):    
            print(tablero[i][j], end="\t")      
        num2 = num2+1
        print("") 

def main():
    tablero = [[]]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
        TCPClientSocket.connect((HOST, PORT))
        print("Ingresa la dificultad del juego:")
        print("1. Principiante: 4x4")
        print("2. Avanzado: 6x6")
        print("Escribir el numero entero de la opción")
        dificultad = input()
        size = 0
        print("Enviando dificultad...")
        TCPClientSocket.sendall(bytes(dificultad, "utf-8"))
        print("Esperando una respuesta...")
        data = TCPClientSocket.recv(buffer_size)
        print(repr(data))
        if int(dificultad) == 1:
            size = 4
            tablero = [["x"]*size for _ in range (size)]
        else:
            size = 6
            tablero = [["x"]*size for _ in range (size)]
        while True:
            print("Recuerda que las casillas que aparecen con - ya no estan disponibles")
            imprimeTablero(size, tablero)
            print("Ingresa la primer carta a voltear: ")
            print("Ejemplo: 1,1")
            tiro1 = input()
            print("Enviando el primer tiro...")
            TCPClientSocket.sendall(bytes(tiro1, "utf-8"))
            data = TCPClientSocket.recv(buffer_size)
            print(repr(data))
            print("Ingresa la segunda carta a voltear: ")
            print("Ejemplo: 1,1")
            tiro2 = input()
            print("Enviando el segundo tiro...")
            TCPClientSocket.sendall(bytes(tiro2, "utf-8"))
            data = TCPClientSocket.recv(buffer_size)
            valor = int(data)
            if valor == 0:
                print("Tiro erroneo....")
                print("Esperando tiro de la computadora.....")
            else:
                print("Tiro correcto")
                actualizaTablero(tiro1, tiro2, tablero)
            while valor == 0:
                TCPClientSocket.sendall(b"ok que entra al while")
                data = TCPClientSocket.recv(buffer_size)
                print(repr(data))
                TCPClientSocket.sendall(b"ok")
                data = TCPClientSocket.recv(buffer_size)
                valor = int(data)
                if valor == 0:
                    TCPClientSocket.sendall(b"ok, el servidor esta bien")
                    data1 = TCPClientSocket.recv(buffer_size)
                    TCPClientSocket.sendall(b"ok, el servidor esta bien")
                    data2 = TCPClientSocket.recv(buffer_size)
                    TCPClientSocket.sendall(b"ok, el servidor esta bien")
                    data3 = TCPClientSocket.recv(buffer_size)
                    TCPClientSocket.sendall(b"ok, el servidor esta bien")
                    data4 = TCPClientSocket.recv(buffer_size)
                    tablero[int(data1)][int(data2)] = "-"
                    tablero[int(data3)][int(data4)] = "-"


            TCPClientSocket.sendall(b"ok")
            data = TCPClientSocket.recv(buffer_size)
            if int(data) == 1:
                break
            print("Te toca otra vez!!")
        data = TCPClientSocket.recv(buffer_size)
        print(repr(data))
        TCPClientSocket.sendall(b"ok")
        data = TCPClientSocket.recv(buffer_size)
        print("Tiempo de ejecucion: ", float(data), " segundos")
        TCPClientSocket.close()
        #print("Recibido,", repr(data), " de", TCPClientSocket.getpeername())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Hasta luego')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

