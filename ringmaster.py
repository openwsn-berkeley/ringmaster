import socket, select
import sys
import os
import time

'''
fairly simple ringmaster client that runs in tandem with openwsn-fw code

https://openwsn.atlassian.net/wiki/display/OW/Ring-of-Things

author: Oleksiy Budilovsky, 2014
'''

here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

from coap import coap, coapUtils

if len(sys.argv) > 1: #if a port is passed, use it
    PORT = int(sys.argv[1])
else:
    PORT = 15000 #default port, as defined in opendefs.h file on firmware side

    
ACTION = 'B' #for now stick to one action - blink
CONFIRMATION = 'C'

all_motes = []
current_mote_idx = -1
waiting_for_response = False
waiting_for_response_from = -1

def sendMsgToMote(ipv6ip_mote, msg, mote_to_fwd_to_addr=None):
    c = coap.coap()
    payload = []
    for ch in msg:
        payload.append(ord(ch))

    if mote_to_fwd_to_addr is not None:
        for ipByte in ipv6ToHexArray(mote_to_fwd_to_addr):
            payload.append(ipByte)

    print "PUTting " + msg + " to mote " + str(ipv6ip_mote)
    p = c.PUT('coap://[{0}]/rt'.format(ipv6ip_mote), 
            payload = payload,
            confirmable = True)
    c.close()
    return p

def sendConfrmToMote(mote):
    print "Sending confirmation to " + mote
    sendMsgToMote(mote, CONFIRMATION)

def registerMote(mote):
    if (mote not in all_motes):
        all_motes.append(mote)

def requestAction():
    global current_mote_idx
    global waiting_for_response
    global waiting_for_response_from
    if (len(all_motes) <= 0):
        return
    
    if (current_mote_idx < 0):
        current_mote_idx = 0
    
    if (waiting_for_response == False):
        waiting_for_response = True
        waiting_for_response_from = all_motes[current_mote_idx]
        sendMsgToMote(waiting_for_response_from, ACTION)


def advance_mote_pointer():
    global current_mote_idx
    current_mote_idx += 1
    if (current_mote_idx >= len(all_motes)):
        current_mote_idx = 0

def forward_mote(from_mote):
    global waiting_for_response
    global waiting_for_response_from
    if (waiting_for_response == True and from_mote == waiting_for_response_from):
        #means we got the right packet
        advance_mote_pointer()
        waiting_for_response_from = all_motes[current_mote_idx]
        new_mssg = "F" + ACTION #format - FB[ipv6] - forward to [ipv6] to blink
        sendMsgToMote(from_mote, new_mssg, waiting_for_response_from)

def handle_incoming_packet(recvd_mssg, from_mote):
    if (recvd_mssg == 'D'):
        sendConfrmToMote(from_mote)
        registerMote(from_mote)
        requestAction()
    if (recvd_mssg == ACTION): #mean ACTION was performed
        print "acion recvd"
        forward_mote(from_mote)

        

def initialize():
    sock = socket.socket(socket.AF_INET6, # Internet
                         socket.SOCK_DGRAM) # UDP

    sock.bind(('bbbb::1', PORT))
    sock.settimeout(None)
    
    resp = None

    while True:
        time.sleep(3)
        data, addr = sock.recvfrom(1024) #buffer size is 1024 bytes
        from_mote = addr[0].split(':')[-1]
        recvd_mssg = data[-1]

        #ipv6from_addr = coapUtils.ipv6AddrString2Bytes(addr[0])
        ipv6from_addr = addr[0]

        handle_incoming_packet(recvd_mssg, ipv6from_addr)

def ipv6ToHexArray(ipv6):
    return coapUtils.ipv6AddrString2Bytes(ipv6)
    

initialize()
