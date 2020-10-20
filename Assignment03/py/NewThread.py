import threading
import sys


class NewThread(threading.Thread):
    def __init__(self, connect, udp):
        threading.Thread.__init__(self)
        self.connect = connect
        # self.udp = udp

    def run(self):
        # if udp:
        #     self.udpServer()
        # else:
        self.tcpServer()

    def tcpServer(self):
        while True:
            msg = self.connect.recv(2048).decode()
            if msg == 'hello':
                response = 'world'
                self.connect.send(response.encode())
            elif msg == 'goodbye':
                response = 'farewell'
                self.connect.send(response.encode())
                # Closing the existing socket
                self.connect.close()
                # break
                # Listening for new connection
                # connect, addr = serverSocket.accept()
            elif msg == 'exit':
                response = 'ok'
                self.connect.send(response.encode())
                self.connect.close()
                sys.exit(0)
            else:
                # Sending the msg as response
                response = msg
                self.connect.send(response.encode())



