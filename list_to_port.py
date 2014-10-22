import socket, select
import sys
import os
import const
import time
import multiprocessing

here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

from coap import coap

PORT = int(sys.argv[1])
MOTE_IP_BASE = 'bbbb::1415:92cc:0:' #primary IP address
ACTION = 'B' #for now stick to one action - blink

all_motes = []
current_mote_idx = -1
waiting_for_response = False
waiting_for_response_from = -1

def sendMsgToMote(mote, msg):
    c = coap.coap()
    mote_ip = MOTE_IP_BASE + str(mote)
    payload = []
    for ch in msg:
        payload.append(ord(ch))

    print "PUTting " + msg + " to mote " + str(mote)
    p = c.PUT('coap://[{0}]/rt'.format(mote_ip), 
            payload = payload,
            confirmable = True)
    c.close()
    return p

def sendMsgWithThread(mote, msg):
    sendMsgToMote(mote, msg)
    '''
    t = multiprocessing.Process(target=sendMsgToMote, args=(mote, msg))
    t.start()
    time.sleep(1)
    t.terminate()
    '''

def sendConfrmToMote(mote):
    print "Sending confirmation to " + mote
    sendMsgWithThread(mote, 'C')

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
        sendMsgWithThread(waiting_for_response_from, 'B')


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
        new_mssg = "F" + str(waiting_for_response_from) + ACTION #format - F2B - forward to 2 blink
        sendMsgWithThread(from_mote, new_mssg)

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
        print data
        print addr

        handle_incoming_packet(recvd_mssg, from_mote)



initialize()
