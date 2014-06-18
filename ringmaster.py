import socket
import const
from utils import send_message_to_mote, create_mssg_packet

all_motes = []
pointer = -1 #pointer to current mote

action = const.BLINK

def send_message_to_mote(mote_port, mssg):
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.sendto(mssg, (const.UDP_IP, mote_port))
    temp_sock.close()

def handle_packet(from_mote, recvd_mssg):
    if (recvd_mssg == const.DISCOVERY):
        handle_discovery(from_mote)
		#elif (recvd_mssg == const.ACTION_PERFORMED):
    #    advance_pointer()
	#			next_mote = all_motes[pointer]
  #      mssg = create_mssg_packet(const.FORWARD_MSG, 


def handle_discovery(from_mote):
    if from_mote in all_motes:
        #mote already registered, do nothing
				return
    else:
        all_motes.append(from_mote)
        send_message_to_mote(from_mote, create_mssg_packet(const.CONFIRM_DISCOVERY, const.RINGMASTER_PORT))
        if len(all_motes) == 1: #means this was the first mote
            send_instruction(from_mote)
            pointer = 0 #set pointer to first element in mote list
       
def send_instruction(mote_port):
    print "Sending instruction to " + str(mote_port)
    mssg = create_mssg_packet(action, const.RINGMASTER_PORT)
    send_message_to_mote(mote_port, mssg)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((const.UDP_IP, const.RINGMASTER_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print "received message:", data
    recvd_mssg = int(data.split(',')[0])
    from_mote = int(data.split(',')[1])
    handle_packet(from_mote, recvd_mssg)

