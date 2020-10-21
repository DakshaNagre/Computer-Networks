# Here is the starting point for your Assignment 03 definitions. Add the
# appropriate comment header as defined in the code formatting guidelines
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

    print("Hello, I am a UDP Client Task 1")
    data = file.read(buffersize)
    while data:
        clientSocket.sendto(data, (server, serverPort))
        data = file.read(buffersize)
        # time.sleep(0.02)


def udpServerA3(port, file):
    serverPort = int(port)
    serverPort = 1235
    timeout = 3
    # Creating the UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    # Binding it to the port
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 1")
    while True:
        data, addr = serverSocket.recvfrom(1024)
        if data:
            file.write(data)
        else:
            file.close()
            break

# Task 2


def udpClientTask2(host, port, file):
    server = 'localhost'
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    buffersize = 1019
    seq = "0"

    print("Hello, I am a UDP Client Task 2")

    data = file.read(buffersize)
    while data:
        sendPacket(clientSocket, data, server, serverPort, seq)

        # wait for ACK
        time.sleep(0.05)

        ackPacket, addr = clientSocket.recvfrom(1024)
        ackPacket = ackPacket.decode("utf-8")
        pktseq = ackPacket[0:1]
        print("ACK packet received, seq is :", pktseq)

        #  Check if correct ACK is received
        if pktseq != seq:
            sendPacket(clientSocket, data, server, serverPort, seq)
        else:
            if seq == "0":
                seq = "1"
            else:
                seq = "0"
            data = file.read(buffersize)


def sendPacket(clientSocket, data, server, serverPort, seq):
    print("Creating packet to send to server, data is", data, " seq is", seq)
    packet = seq + "NACK"
    packet = packet.encode() + data
    clientSocket.sendto(packet, (server, serverPort))

# sending ACK packet to client


def sendAckPacket(seq, socket, addr, data):
    print("Creating ACK packet seq is :", seq, " data is", data)
    packet = (str(seq) + data).encode()
    socket.sendto(packet, addr)


def udpServerTask2(port, file):
    serverPort = 1235
    timeout = 3
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 2")
    while True:
        data, addr = serverSocket.recvfrom(1024)
        data = data.decode()
        seq = data[0:1]
        data = data[5:len(data)]
        data = data.encode()
        if data:
            file.write(data)

            sendAckPacket(seq, serverSocket, addr, "ACK")
        else:
            file.close()
            break

# References:
# https://stackoverflow.com/questions/57794550/sending-large-files-over-udp
# https://chuanjin.me/2016/08/03/transfer-file/
