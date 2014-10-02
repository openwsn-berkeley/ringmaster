import socket, select
import sys
import os
import const
from utils import send_message_to_mote, create_mssg_packet, print_packet

here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

PORT = int(sys.argv[1])

def initialize():
    sock = socket.socket(socket.AF_INET6, # Internet
                         socket.SOCK_DGRAM) # UDP

    sock.bind(('bbbb::1', PORT))
    sock.settimeout(None)

    while True:
        data, addr = sock.recvfrom(1024) #buffer size is 1024 bytes
        print data
        for x in data:
            print x
        print addr


initialize()
