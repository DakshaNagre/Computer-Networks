# Here is the starting point for your Assignment 03 definitions. Add the
# appropriate comment header as defined in the code formatting guidelines

from socket import *
import sys
import threading
import os
import time
from select import *


def udpClientA3(host, port, file):
    server = 'localhost'
    # server = host
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    buffersize = 1024

    data = file.read(buffersize)
    print("Hello, I am a UDP Client")
    while data:
        clientSocket.sendto(data, (server, serverPort))
        data = file.read(buffersize)


def udpServerA3(port, file):
    serverPort = int(port)
    serverPort = 1235
    timeout = 3
    # Creating the UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    # serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    # Binding it to the port
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server")
    while True:
        data, addr = serverSocket.recvfrom(1024)
        if data:
            file.write(data)

        while True:
            ready = select([serverSocket], [], [], timeout)
            if ready[0]:
                data, addr = serverSocket.recvfrom(1024)
                file.write(data)
            else:
                file.close()
                break

# References:
# https://stackoverflow.com/questions/57794550/sending-large-files-over-udp
# https://chuanjin.me/2016/08/03/transfer-file/
