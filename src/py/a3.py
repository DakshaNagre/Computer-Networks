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


def udpClientA3(host, port, file, filename):
    server = 'localhost'
    # server = host
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    buffersize = 1024
    file = open(filename, "rb")

    print("Hello, I am a UDP Client Task 1")
    data = file.read(buffersize)
    while data:
        clientSocket.sendto(data, (server, serverPort))
        data = file.read(buffersize)

    file.close()


def udpServerA3(port, file, filename):
    serverPort = int(port)
    serverPort = 1235
    timeout = float(10)
    # Creating the UDP socket
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    # Binding it to the port
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 1")
    file = open("tempServerWrites", "wb")
    data, addr = serverSocket.recvfrom(1024)
    try:
        while data:
            file.write(data)
            serverSocket.settimeout(6)
            data, addr = serverSocket.recvfrom(1024)
    except Exception as e:
        print("file transfer successful")
        file.close()
        serverSocket.close()

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

        # ACK
        try:
            ackPacket, addr = clientSocket.recvfrom(1024)
            ackPacket = ackPacket.decode("utf-8")
            pktseq = ackPacket[0:1]
            print("ACK packet received, seq is :",
                  pktseq, " Required seq is :", seq)
        except Exception as e:
            print("Timed out")

            #  Check if correct ACK is received
        if pktseq != seq:
            sendPacket(clientSocket, data, server, serverPort, seq)
        else:
            if seq == "0":
                seq = "1"
            else:
                seq = "0"
            data = file.read(buffersize)
    clientSocket.close()

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
    timeout = 6
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 2")
    try:
        while True:
            data, addr = serverSocket.recvfrom(1024)
            data = data.decode()
            pktseq = data[0:1]
            data = data[5:len(data)]
            data = data.encode()
            print("Received packet with seq",
                  pktseq, " Expected is", seq)
            serverSocket.settimeout(6)
            if data and pktseq == seq:
                file.write(data)
                sendAckPacket(seq, serverSocket, addr, "ACK")
                if seq == '0':
                    seq = '1'
                else:
                    seq = '0'
            elif not data:
                file.close()
                serverSocket.close()
                break
    except Exception as e:
        print("file transfer successful")
        file.close()
        serverSocket.close()


# Task 3:


def udpClientTask3(host, port, file):
    defaultwindowsize = 4
    # stores the window start
    base = 0
    windowsize = 0
    server = 'localhost'
    serverPort = int(port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    buffersize = 1019
    packetlist = []
    sentpacketlist = []
    seq = 0
    nextseq = 0
    timeout = 0.05
    print("Hello, I am a UDP Client Task 3")

    # Reading data, creating packets and storing in packetlist
    while True:
        data = file.read(buffersize)
        if not data:
            break
        packet = str(seq) + "NACK"
        packet = packet.encode() + data
        packetlist.append(packet)
        seq += 1

    packetlistsize = len(packetlist)
    print(packetlistsize, "packets to send")

    windowsize = min(defaultwindowsize, packetlistsize)
    while base < packetlistsize:
        counter = 0
        # sending packets
        while nextseq < base + windowsize:
            sendPacketTask3(
                clientSocket, packetlist[nextseq], server, serverPort, nextseq)
            print("Sent packet, seq no. :", nextseq)
            sentpacketlist.insert(counter, nextseq)
            counter += 1
            nextseq += 1

        startTime = float(time.time())
        ackpktlist = receiveACK(clientSocket, startTime,
                                timeout, windowsize, sentpacketlist)

        if len(ackpktlist) != windowsize:
            # ACK packets were not received.
            # Hence, resetting nextseq to base and sending packets again.
            # nextseq = base
            findMissingPacketsAndRetransmit(
                clientSocket, packetlist, server, serverPort, sentpacketlist, ackpktlist)
            base = nextseq
        else:
            base = nextseq
            windowsize = min(defaultwindowsize, packetlistsize - nextseq)

        # sendPacketTask3(
        #     clientSocket, packetlist[nextseq-1], server, serverPort, nextseq)

    # while (not timeoutfun(startTime, timeout)):
    #     time.sleep(sleeptime)

    #     if timeoutfun(startTime, timeout):
    #         ackpktlist = receiveACK(clientSocket, startTime, timeout)

    #         print("!!!!!!!!!!!! TIMED OUT !!!!!!!!!!!!")
    #         if len(ackpktlist) != windowsize:
    #             # ACK packets were not received.
    #             # Hence, resetting nextseq to base and sending packets again.
    #             nextseq = base
    #     else:
    #         base = nextseq
    #         windowsize = min(defaultwindowsize, packetlistsize - base)
    clientSocket.close()
    file.close()


def udpServerTask3(port, file):

    seq = 0
    serverPort = 1235
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))
    print("Hello, I am a UDP Server Task 3")
    while True:
        data, addr = serverSocket.recvfrom(1024)
        if not data:
            serverSocket.close()
            break
        data = data.decode()

        if seq <= 9:
            pktseq = int(data[0:1])
            data = data[5:len(data)]
        elif seq > 9 and seq <= 99:
            pktseq = int(data[0:2])
            data = data[6:len(data)]
        elif seq > 99 and seq <= 999:
            pktseq = int(data[0:3])
            data = data[7:len(data)]
        elif seq > 999 and seq <= 9999:
            pktseq = int(data[0:4])
            data = data[8:len(data)]

        data = data.encode()
        print("Received packet with seq",
              pktseq, " Expected is", seq)
        if pktseq == seq:
            sendAckPacket(seq, serverSocket, addr, "ACK")
            seq += 1
            file.write(data)
            data = None
        else:
            print("Received wrong packet, seq :", pktseq)
            sendAckPacket(seq, serverSocket, addr, "NACK")
            # break
    print("file transfer successful")
    serverSocket.close()
    file.close()


def timeoutfun(start, duration):
    if float(time.time()) - float(start) >= float(duration):
        print("Time is : " + time.time())
        return True
    else:
        return False


def findMissingPacketsAndRetransmit(clientSocket, packetlist, server, serverPort, sentpacketlist, ackpktlist):

    for i in range(len(ackpktlist)):
        if ackpktlist[i] != sentpacketlist[i]:
            sendPacketTask3(
                clientSocket, packetlist[i], server, serverPort, i)
            print("Sent Missing ACK packet again, seq is :", i)


def receiveACK(clientSocket, startTime, timeout, pktcount, sentpacketlist):
    counter = 0
    ackpktlist = []
    while pktcount > 0 and not timeoutfun(startTime, timeout):
        ackPacket, addr = clientSocket.recvfrom(1024)
        ackPacket = ackPacket.decode("utf-8")

        if sentpacketlist[counter] <= 9:
            pktseq = int(ackPacket[0:1])
        elif 9 < sentpacketlist[counter] <= 99:
            pktseq = int(ackPacket[0:2])
        elif 99 < sentpacketlist[counter] <= 999:
            pktseq = int(ackPacket[0:3])
        elif 999 < sentpacketlist[counter] <= 9999:
            pktseq = int(ackPacket[0:4])

        print("ACK packet received, seq is :", pktseq)
        pktcount -= 1
        counter += 1
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
