import socket
import const
import select
from utils import send_message_to_mote, create_mssg_packet, print_packet

all_motes = []
last_mssg_sent = None
retry_count=0
pointer = -1 #pointer to current mote

action = const.BLINK

def handle_packet(from_mote, recvd_mssg):
    global last_mssg_sent
    if (recvd_mssg == const.DISCOVERY):
        handle_discovery(from_mote)
    elif (recvd_mssg == const.ACTION_PERFORMED):
        advance_pointer()
        next_mote = all_motes[pointer]
        last_mssg_sent = create_mssg_packet(const.FORWARD_MSG, const.RINGMASTER_PORT, next_mote, action)
        send_message_to_mote(from_mote,last_mssg_sent)


def advance_pointer():
    global pointer
    pointer += 1
    if (pointer >= len(all_motes)):
        pointer = 0

def handle_discovery(from_mote):
    global last_mssg_sent
    if from_mote in all_motes:
				return
    else:
        all_motes.append(from_mote)
        print all_motes
        last_mssg_sent = create_mssg_packet(const.CONFIRM_DISCOVERY, const.RINGMASTER_PORT, from_mote)
        send_message_to_mote(from_mote, last_mssg_sent)
        if len(all_motes) == 1: #means this was the first mote
            global pointer
            pointer = 0 #set pointer to first element in mote list
            send_instruction(from_mote)
       
def send_instruction(mote_port):
    global last_mssg_sent
    last_mssg_sent = create_mssg_packet(action, const.RINGMASTER_PORT, mote_port)
    send_message_to_mote(mote_port, last_mssg_sent)


def handle_packet_timeout(last_mssg_sent):
    global retry_count
    mssg_sent = int(last_mssg_sent.split(',')[0])
    mote_to = int(last_mssg_sent.split(',')[2])
    if (retry_count == 0):
        retry_count += 1
        send_message_to_mote(mote_to, last_mssg_sent)
    else:
        retry_count = 0
        
   

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((const.UDP_IP, const.RINGMASTER_PORT))
sock.settimeout(5) #timeout of 5 seconds, for now

while True:
    try:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        retry_count = 0
        print_packet(data)
        recvd_mssg = int(data.split(',')[0])
        from_mote = int(data.split(',')[1])
        handle_packet(from_mote, recvd_mssg)
    except Exception, e:
        print last_mssg_sent
        #handle_packet_timeout(last_mssg_sent)
        print e
