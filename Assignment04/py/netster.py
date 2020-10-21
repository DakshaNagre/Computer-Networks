import argparse
import logging as log

# Import the assignment modules.
# These imports can be specialized as necessary.
from a2 import *
from a3 import *

DEFAULT_PORT = 12345
timeout = 3

# If we are a server, launch the appropriate methods to handle server
# functionality based on the input arguments.
# NOTE: The arguments should be extended with a custom dict or **kwargs


def run_tcpServer(host, port):
    #log.info("Hello, I am a server")
    print("Hello, I am a server")
    if port == DEFAULT_PORT:
        port = 1234
    tcpServer(host, port)

# If we are a client, launch the appropriate methods to handle client
# functionality based on the input arguments
# NOTE: The arguments should be extended with a custom dict or **kwargs


def run_tcpClient(host, port):
    print("Hello, I am a client")
    if port == DEFAULT_PORT:
        port = 1234
    tcpClient(host, port)


def run_udpServer(host, port):
    print("Hello, I am a server")
    if port == DEFAULT_PORT:
        port = 1235
    udpServer(host, port)


def run_udpClient(host, port):
    print("Hello, I am a client")
    if port == DEFAULT_PORT:
        port = 1235
    udpClient(host, port)


def main():
    parser = argparse.ArgumentParser(description="SICE Network netster")
    parser.add_argument('-p', '--port', type=str, default=DEFAULT_PORT,
                        help='listen on/connect to port <port> (default={}'
                        .format(DEFAULT_PORT))
    parser.add_argument('-i', '--iface', type=str, default='0.0.0.0',
                        help='listen on interface <dev>')
    parser.add_argument('-f', '--file', type=str,
                        help='file to read/write')
    parser.add_argument('-u', '--udp', action='store_true',
                        help='use UDP (default TCP)')
    parser.add_argument('-r', '--rudp', type=int, default=0,
                        help='use RUDP (1=stopwait, 2=gobackN)')
    parser.add_argument('-m', '--mcast', type=str, default='226.0.0.1',
                        help='use multicast with specified group address')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Produce verbose output')
    parser.add_argument('host', metavar='host', type=str, nargs='?',
                        help='connect to server at <host>')

    args = parser.parse_args()

    # configure logging level based on verbose arg
    level = log.DEBUG if args.verbose else log.INFO

    # Testing Task 2 of Assignment 04

    # if args.host:
    #     udpClientTask2(1235)
    # else:
    #     udpServerTask2()
    #     exit(1)

    f = None
    # open the file if specified
    if args.file:
        try:
            mode = "rb"
            if args.host:
                f = open(args.file, mode)
                # Testing Task 2 of Assignment 04
                udpClientTask2(args.host, 1235, f)
                # f = open(args.file, mode)
                # udpClientA3(args.host, 1235, f)
            else:
                mode = "wb"
                f = open("tempServerWrites", "wb")
                # Testing Task 2 of Assignment 04
                udpServerTask2(1235, f)
                # f = open("tempServerWrites", "wb")
                # udpServerA3(1235, f)
                # f.close()
        except Exception as e:
            print("Could not open file: {}".format(e))
            exit(1)

        # Here we determine if we are a client or a server depending
        # on the presence of a "host" argument.
    elif args.host:
        # log.basicConfig(format='%(levelname)s:client: %(message)s',
        #                 level=level)
        if args.udp:
            run_udpClient(args.host, args.port)
        else:
            run_tcpClient(args.host, args.port)
    else:
        # log.basicConfig(format='%(levelname)s:server: %(message)s',
        #                 level=level)
        if args.udp:
            run_udpServer(args.host, args.port)
        else:
            run_tcpServer(args.host, args.port)

    # if args.file:
    #     f.close()


if __name__ == "__main__":
    main()
