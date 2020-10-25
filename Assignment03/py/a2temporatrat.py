# Here is the starting point for your Assignment 02 definitions. Add the
# appropriate comment header as defined in the code formatting guidelines

from socket import *
import sys
import os
import threading


def tcpClient(host, port):
    serverName = '129.79.247.5'
    serverPort = port
    # serverPort = 1234
    # Creating client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Establishing tcp connection with server
    clientSocket.connect((serverName, serverPort))
    while True:
        msg = input('Enter message for server: ')
        clientSocket.send(msg.encode())
        response = clientSocket.recv(1024).decode()
        if len(response) > 0:
            print('Message from Server: ', response)
        if msg == 'goodbye' or msg == 'exit':
            clientSocket.close()
            sys.exit(0)


def tcpServer(host, port):
    # serverPort = 1234
    serverPort = int(port)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))

    while True:
        serverSocket.listen(3)
        # Creating dedicated socket for the client stored in connect
        connect, addr = serverSocket.accept()
        newThread = NewThread(connect, False)
        newThread.start()


# serverSocket.listen(3)
    # Creating socket for the client
   # connect, addr = serverSocket.accept()
#    while True:
#        msg = connect.recv(1024).decode()
#        if msg == 'hello':
#            response = 'world'
#            connect.send(response.encode())
#        elif msg == 'goodbye':
#            response = 'farewell'
#            connect.send(response.encode())
#            connect.close()
#            connect, addr = serverSocket.accept()
#        elif msg == 'exit':
# response = 'ok'
#            connect.send(response.encode())
#            connect.close()
#            sys.exit(0)
#        else:
            # Sending the msg as response
#            response = msg
 #           connect.send(response.encode())
    # newThread = NewThread(connect, False)
# newThread.start()


def udpClient(host, port):
    server = '129.79.247.5'
    # serverPort = 1235
    serverPort = port
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    while True:
        msg = input('Enter message for server: ')
        # Converting the message into bytes, attaching server address and port number and sending to server
        clientSocket.sendto(msg.encode(), (server, serverPort))
        # response, serverAdd = clientSocket.recvfrom(1025)
        response = clientSocket.recv(1025).decode()
        if len(response) > 0:
            print('Message freating client socket')
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Establishing tcp connection with server
    clientSocket.connect((serverName, serverPort))
    while True:
        msg = input('Enter message for server: ')
        clientSocket.send(msg.encode())
        response = clientSocket.recv(1024).decode()
        if len(response) > 0:
            print('Message from Server: ', response)
        if msg == 'goodbye' or msg == 'exit':
            clientSocket.close()
            sys.exit(0)


def tcpServer(host, port):
    # serverPort = 1234
    serverPort = int(port)
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))

    while True:
        serverSocket.listen(3)
        # Creating dedicated socket for the client stored in connect
        connect, addr = serverSocket.accept()
        newThread = NewThread(connect, False)
        newThread.start()
# serverSocket.listen(3)
    # Creating socket for the client
   # connect, addr = serverSocket.accept()
#    while True:
#        msg = connect.recv(1024).decode()
#        if msg == 'hello':
#            response = 'world'
#            connect.send(response.encode())
#        elif msg == 'goodbye':
#            response = 'farewell'
#            connect.send(response.encode())
#            connect.close()
#            connect, addr = serverSocket.accept()
#        elif msg == 'exit':
        if msg == 'goodbye' or msg == 'exit':
            clientSocket.close()
            sys.exit(0)


def udpServer(host, port):
    # serverPort = 1235
    serverPort = int(port)
    # Creating the UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Binding it to the port
    serverSocket.bind(('', serverPort))
    while True:
        # newThread = NewThread(connect=None, udp=True, serverSocket=serverSocket)
        # newThread.start()

        msg, clientAdd = serverSocket.recvfrom(1025)
        msg = msg.decode()
 if msg == 'hello':
            response='world'
            #  Converting the response into bytes and sending it to the client
            serverSocket.sendto(response.encode(), clientAdd)
        elif msg == 'goodbye':
            response='farewell'
            serverSocket.sendto(response.encode(), clientAdd)
            # In udp, server does not create a dedicated connection for each of the client like TCP.
            # So, there will be no close() being called.
        elif msg == 'exit':
            response='ok'
            serverSocket.sendto(response.encode(), clientAdd)
            sys.exit(0)
        else:
            # Sending the msg as response
            response=msg
            serverSocket.sendto(response.encode(), clientAdd)


class NewThread(threading.Thread):
    def __init__(self, connect, udp, serverSocket):
        threading.Thread.__init__(self)
        self.connect=connect
        self.udp=udp
        self.serverSocket=serverSocket

    def run(self):
    if self.udp:
            self.udpServer(serverSocket=self.serverSocket, )
        else:
            self.tcpServer()

    def tcpServer(self):
        while True:
            msg=self.connect.recv(2048).decode()
            if msg == 'hello':
                response='world'
                self.connect.send(response.encode())
            elif msg == 'goodbye':
                response='farewell'
                self.connect.send(response.encode())
                # Closing the existing socket
                self.connect.close()
                break
                # Listening for new connection
                # connect, addr = serverSocket.accept()
            elif msg == 'exit':
                response='ok'
                self.connect.send(response.encode())
                self.connect.close()
                os._exit(0)
            else:
                # Sending the msg as response
                response=msg
                self.connect.send(response.encode())

    def udpServer(self, serverSocket):
        while True:
            msg, clientAdd=serverSocket.recvfrom(2048)
            msg=msg.decode()
            if msg == 'hello':
                response='world'
                #  Converting the response into bytes and sending it to the client
                serverSocket.sendto(response.encode(), clientAdd)
            elif msg == 'goodbye':
                response='farewell'
                serverSocket.sendto(response.encode(), clientAdd)
                # In udp, server does not create a dedicated connection for each of the client like TCP.
                # So, there will be no close() being called.
            elif msg == 'exit':
                response='ok'
                serverSocket.sendto(response.encode(), clientAdd)
                os._exit(0)
            else:

 # Sending the msg as response
                response=msg
                self.connect.send(response.encode())

    def udpServer(self, serverSocket):
        while True:
            msg, clientAdd=serverSocket.recvfrom(2048)
            msg=msg.decode()
            if msg == 'hello':
                response='world'
                #  Converting the response into bytes and sending it to the client
                serverSocket.sendto(response.encode(), clientAdd)
            elif msg == 'goodbye':
                response='farewell'
                serverSocket.sendto(response.encode(), clientAdd)
                # In udp, server does not create a dedicated connection for each of the client like TCP.
                # So, there will be no close() being called.
            elif msg == 'exit':
                response='ok'
                serverSocket.sendto(response.encode(), clientAdd)
                os._exit(0)
            else:
                # Sending the msg as response
                response=msg
                serverSocket.sendto(response.encode(), clientAdd)
