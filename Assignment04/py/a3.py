# Here is the starting point for your Assignment 03 definitions. Add the
# appropriate comment header as defined in the code formatting guidelines
# Here is the starting point for your Assignment 03 definitions. Add the
# appropriate comment header as defined in the code formatting guidelines

from socket import *
import sys
import threading
import os
import time
import _thread
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
        print("ACK packet received, seq is :",
              pktseq, " Required seq is :", seq)

        #  Check if correct ACK is received
        if pktseq != seq:
            sendPacket(clientSocket, data, server, serverPort, seq)
        else:
            if seq == "0":
                seq = "1"
            else:
                seq = "0"
            data = file.read(buffersize)

# Used by Task 2


def sendPacket(clientSocket, data, server, serverPort, seq):
    print("Creating packet to send to server, seq is", seq)
    packet = seq + "NACK"
    packet = packet.encode() + data
    clientSocket.sendto(packet, (server, serverPort))

# sending ACK packet to client


def sendAckPacket(seq, socket, addr, data):
    print("Creating ACK packet seq is :", seq, " data is", data)
    packet = (str(seq) + data).encode()
    socket.sendto(packet, addr)


def udpServerTask2(port, file):

    seq = '0'
    serverPort = 1235
    timeout = 3
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 2")
    while True:
        data, addr = serverSocket.recvfrom(1024)
        data = data.decode()
        pktseq = data[0:1]
        data = data[5:len(data)]
        data = data.encode()
        print("Received packet with seq",
              pktseq, " Expected is", seq)
        if data and pktseq == seq:
            file.write(data)
            sendAckPacket(seq, serverSocket, addr, "ACK")
            seq += 1
        elif not data:
            file.close()
            break

# Task 3:


def clientTask3(file, host, port):
    defaultwindowsize = 4
    # stores the window start
    base = 0
    windowsize = 0
    server = 'localhost'
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    buffersize = 1019
    packetlist = []
    seq = 0
    nextseq = 0
    sleeptime = 0.5
    # timeout = 0.5

    # Reading data, creating packets and storing in packetlist
    while True:
        data = file.read(buffersize)
        if not data:
            break
        packet = seq + "NACK"
        packet = packet.encode() + data
        packetlist.append(packet)
        seq += 1

    packetlistsize = len(packetlist)
    print(packetlistsize, " to send")

    windowsize = min(defaultwindowsize, packetlistsize)

    # _thread.start_new_thread(receiveACK, (clientSocket, timeout, hs))

    while base < packetlistsize:
        _thread.allocate_lock().acquire()

        # sending packets
        while nextseq < base + windowsize:
            sendPacketTask3(
                clientSocket, packetlist[nextseq], server, serverPort, seq)
            print("Sending packet, seq no. :", nextseq)
            nextseq += 1

        startTime = time.time()

        while (not timeoutfun(startTime, timeout)):
            # _thread.allocate_lock().release()
            time.sleep(sleeptime)
            # _thread.allocate_lock().acquire()

            if timeoutfun(startTime, timeout):
                ackpktlist = receiveACK(clientSocket, startTime, timeout)

                print("!!!!!!!!!!!! TIMED OUT !!!!!!!!!!!!")
                if len(ackpktlist) != windowsize:
                    # ACK packets were not received.
                    # Hence, resetting nextseq to base and sending packets again.
                    nextseq = base
            else:
                base = nextseq
                windowsize = min(defaultwindowsize, packetlistsize - base)
    file.close()


def udpServerTask3(port, file):

    seq = 0
    serverPort = 1235
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 2")
    while True:
        data, addr = serverSocket.recvfrom(1024)
        data = data.decode()
        pktseq = data[0:1]
        data = data[5:len(data)]
        data = data.encode()
        print("Received packet with seq",
              pktseq, " Expected is", seq)
        if data and pktseq == seq:
            file.write(data)
            sendAckPacket(seq, serverSocket, addr, "ACK")

        elif not data:
            file.close()
            break


def timeoutfun(start, duration):
    if time.time() - start >= duration:
        return True
    else:
        return False


def receiveACK(clientSocket, startTime, timeout):
    ackpktlist = []

    while True and not timeoutfun(startTime, timeout):
        ackPacket, addr = clientSocket.recvfrom(1024)
        ackPacket = ackPacket.decode("utf-8")
        pktseq = int(ackPacket[0:1])
        print("ACK packet received, seq is :", pktseq)
        ackpktlist.append(pktseq)

    return ackpktlist


def sendPacketTask3(clientSocket, packet, server, serverPort, seq):
    print("Sending packet to server with seq :", seq)
    clientSocket.sendto(packet, (server, serverPort))

    # References:
    # https://stackoverflow.com/questions/57794550/sending-large-files-over-udp
    # https://chuanjin.me/2016/08/03/transfer-file/
    # https://www.baeldung.com/cs/networking-go-back-n-protocol
    # https://github.com/haseeb-saeed/go-back-N/blob/master/
    # https://pypi.org/project/packet-python/
    # https://www.tutorialspoint.com/python3/python_multithreading.htm
    # https://stackoverflow.com/questions/52228001/basic-timer-in-python-3-7
