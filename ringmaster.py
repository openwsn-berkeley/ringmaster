import socket
import const
from utils import send_message_to_mote, create_mssg_packet, print_packet

all_motes = []
mote_flags = []
last_mssg_sent = None
expecting_response_from = None
pointer = -1 #pointer to current mote

action = const.BLINK

def handle_packet(from_mote, recvd_mssg):
    global last_mssg_sent
    global expecting_response_from
    if (recvd_mssg == const.DISCOVERY):
        handle_discovery(from_mote)
    elif (recvd_mssg == const.ACTION_PERFORMED):
        if (from_mote == expecting_response_from):
            reset_mote_flag(from_mote)
            advance_pointer()
            next_mote = all_motes[pointer]
            expecting_response_from = next_mote
            last_mssg_sent = create_mssg_packet(const.FORWARD_MSG, const.RINGMASTER_PORT, next_mote, action)
            send_message_to_mote(from_mote,last_mssg_sent)
        else: #unexpected packet received
            print "error"
            print "unexpected packet received from mote: " + str(from_mote) + " with message " + str(recvd_mssg) + ", expecting from: " + str(expecting_response_from)


def advance_pointer():
    global pointer
    if (len(all_motes) == 0):
        pointer = -1
    else:
        pointer += 1
        if (pointer >= len(all_motes)):
            pointer = 0

def handle_discovery(from_mote):
    if from_mote in all_motes:
        confirm_discovery(from_mote)
        reset_mote_flag(from_mote)
    else:
        all_motes.append(from_mote)
        mote_flags.append(0) 
        print all_motes
        confirm_discovery(from_mote)
        if len(all_motes) == 1: #means this was the first mote
            global pointer
            pointer = 0 #set pointer to first element in mote list
            send_instruction(from_mote)

       
def reset_mote_flag(mote):
    mote_flags[all_motes.index(mote)] = 0

def increase_mote_flag(mote):
    mote_flags[all_motes.index(mote)] += 1
 
def get_mote_flag(mote):
    return mote_flags[all_motes.index(mote)]

def purge_mote(mote):
    print "purging mote"
    mote_idx = all_motes.index(mote)
    del all_motes[mote_idx]
    del mote_flags[mote_idx]

def confirm_discovery(from_mote):
    #do not save to the last message
    mssg = create_mssg_packet(const.CONFIRM_DISCOVERY, const.RINGMASTER_PORT, from_mote)
    send_message_to_mote(from_mote, mssg)
    
def send_instruction(mote_port):
    global last_mssg_sent
    global expecting_response_from
    expecting_response_from = mote_port
    last_mssg_sent = create_mssg_packet(action, const.RINGMASTER_PORT, mote_port)
    send_message_to_mote(mote_port, last_mssg_sent)


def handle_packet_timeout(last_mssg_sent):
    global pointer
    if (last_mssg_sent == None):
        return

    mssg_sent = int(last_mssg_sent.split(',')[0])
    mote_to = int(last_mssg_sent.split(',')[2])

    if (mote_to not in all_motes):
        #TODO handle this case
        return
    
    increase_mote_flag(mote_to)
    print mote_to
    print get_mote_flag(mote_to)
    if (get_mote_flag(mote_to) > 1): #TODO make a constant?
        purge_mote(mote_to)
    
    advance_pointer()
    if (pointer == -1):
        print "no motes registered, waiting"
    else:
        next_mote = all_motes[pointer]
        send_instruction(next_mote)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((const.UDP_IP, const.RINGMASTER_PORT))
sock.settimeout(5) #timeout of 5 seconds, for now

while True:
    print all_motes
    print mote_flags
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print_packet(data)
        recvd_mssg = int(data.split(',')[0])
        from_mote = int(data.split(',')[1])
        handle_packet(from_mote, recvd_mssg)
    except Exception, e:
        print last_mssg_sent
        print "HERE"
        handle_packet_timeout(last_mssg_sent)
