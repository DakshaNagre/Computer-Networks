# Here is the starting point for your Assignment 02 definitions. Add the
# appropriate comment header as defined in the code formatting guidelines

from socket import *
import sys
import threading
import os


def tcpClient(host, port):
    # serverName = '129.79.247.5'
    serverName = host
    serverPort = int(port)
    # serverPort = 1234
    # Creating client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # Establishing tcp connection with server
    clientSocket.connect((serverName, serverPort))
    while True:
        msg = input('Enter message for server: ')
        clientSocket.send(msg.encode())
        # 2048 is size of buffer
        response = clientSocket.recv(2048).decode()
        if len(response) > 0:
            print(response)
        if msg == 'goodbye' or msg == 'exit':
            clientSocket.close()
            sys.exit(0)


def tcpServer(host, port):
    serverPort = int(port)
    # serverPort = 1234
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET,
                            SO_REUSEADDR, 1)
    serverSocket.bind(('', serverPort))
    counter = -1
    hs = set()

    while True:
        serverSocket.listen(30)
        # Creating dedicated socket for the client stored in connect
        connect, addr = serverSocket.accept()
        if addr not in hs:
            hs.add(addr)
            counter += 1
        print("connection ", counter, "from", addr)
        newThread = NewThread(connect=connect, addr=addr)
        newThread.start()


def udpClient(host, port):
    # server = '129.79.247.5'
    server = host
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)

    while True:
        msg = input('Enter message for server: ')
        # Converting the message into bytes, attaching server address and port number and sending to server
        clientSocket.sendto(msg.encode(), (server, serverPort))
        # response, serverAdd = clientSocket.recvfrom(1025)
        # 2048 is size of buffer
        response = clientSocket.recv(2048).decode()
        if len(response) > 0:
            print(response)
        if msg == 'goodbye' or msg == 'exit':
            clientSocket.close()
            sys.exit(0)


def udpServer(host, port):
    serverPort = int(port)
    # serverPort = 1235
    # Creating the UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Binding it to the port
    serverSocket.bind(('', serverPort))
    while True:
        msg, clientAdd = serverSocket.recvfrom(2048)
        msg = msg.decode()
        # print("got message from", clientAdd, "<port_", counter, ">")
        print("got message from", clientAdd)
        if msg == 'hello':
            response = 'world'
            #  Converting the response into bytes and sending it to the client
            serverSocket.sendto(response.encode(), clientAdd)
        elif msg == 'goodbye':
            response = 'farewell'
            serverSocket.sendto(response.encode(), clientAdd)
            # In udp, server does not create a dedicated connection for each of the client like TCP.
            # So, there will be no close() being called.
        elif msg == 'exit':
            response = 'ok'
            serverSocket.sendto(response.encode(), clientAdd)
            sys.exit(0)
        else:
            # Sending the msg as response
            response = msg
            serverSocket.sendto(response.encode(), clientAdd)


class NewThread(threading.Thread):

    def __init__(self, connect, addr):
        threading.Thread.__init__(self)
        self.connect = connect
        self.addr = addr

    def run(self):
        self.tcpServer()

    def tcpServer(self):
        while True:
            msg = self.connect.recv(2048).decode()
            print("got message from", self.addr)
            if msg == 'hello':
                response = 'world'
                # print("got message from", self.addr)
                self.connect.send(response.encode())
            elif msg == 'goodbye':
                response = 'farewell'
                self.connect.send(response.encode())
                # Closing the existing socket
                self.connect.close()
                break
            elif msg == 'exit':
                response = 'ok'
                # print("got message from", self.addr)
                self.connect.send(response.encode())
                self.connect.close()
                os._exit(0)
            else:
                # Sending the msg as response
                response = msg
                # print("got message from", self.addr)
                self.connect.send(response.encode())


# To understand how to write tcp nad udp function, I have taken references from following sources:
# 1. Computer Networking A Top-Down Approach Seventh Edition
# 2. https: // docs.python.org/3/howto/sockets.html
# 3. https: // docs.python.org/3/library/socket.html
