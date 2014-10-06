import socket, select
import sys
import os
import const

here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

from coap import coap

PORT = int(sys.argv[1])
MOTE_IP_BASE = 'bbbb::1415:92cc:0:' #primary IP address

def sendConfrmToMote(mote):
    print "Sending confirmation to " + mote
    c = coap.coap()
    mote_ip = MOTE_IP_BASE + str(mote)
    p = c.PUT('coap://[{0}]/rt'.format(mote_ip), 
            payload = [ord('C')])
    c.close()


def initialize():
    sock = socket.socket(socket.AF_INET6, # Internet
                         socket.SOCK_DGRAM) # UDP

    sock.bind(('bbbb::1', PORT))
    sock.settimeout(None)

    while True:
        data, addr = sock.recvfrom(1024) #buffer size is 1024 bytes
        from_mote = addr[0].split(':')[-1]
        recvd_mssg = data[-1]
        print data
        for x in data:
            print x
        print addr


        if (recvd_mssg == 'D'):
            sendConfrmToMote(from_mote)

initialize()
