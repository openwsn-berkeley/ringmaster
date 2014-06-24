import socket
import sys
import const
from utils import send_message_to_mote, create_mssg_packet, print_packet

MOTE_PORT = int(sys.argv[1])
MESSAGE = "Mote " + str(MOTE_PORT) + " online"

discovered = False

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((const.UDP_IP, MOTE_PORT))

#wait for specific amount of time, return when receiving
def wait_for_response(time):
    try:
        sock.settimeout(time)
        data, addr = sock.recvfrom(1024)
        sock.settimeout(None) #set timeout back to infinity
        return data
    except Exception, e:
        print "No response from ringmaster"
        return None

def discover_ringmaster():
    print "Discovering ringmaster mote..."
    discovered = False
    response = None
    while not discovered:
        send_message_to_mote(const.RINGMASTER_PORT, create_mssg_packet(const.DISCOVERY, MOTE_PORT, const.RINGMASTER_PORT))
        response = wait_for_response(4)
        if response is not None:
            discovered = True

def handle_mssg(mssg):
    recvd_mssg = int(data.split(',')[0])
    from_mote = int(data.split(',')[1])
    if (recvd_mssg == const.BLINK):
        blink_mote()
        send_message_to_mote(const.RINGMASTER_PORT, create_mssg_packet(const.ACTION_PERFORMED, MOTE_PORT, const.RINGMASTER_PORT, recvd_mssg))
    elif (recvd_mssg == const.BUZZ):
        buzz_mote()
        send_message_to_mote(const.RINGMASTER_PORT, create_mssg_packet(const.ACTION_PERFORMED, MOTE_PORT, const.RINGMASTER_PORT, recvd_mssg))
    elif (recvd_mssg == const.FORWARD_MSG):
        to_mote = int(data.split(',')[2])
        action = int(data.split(',')[3])
        mssg = create_mssg_packet(action, MOTE_PORT, to_mote)
        send_message_to_mote(to_mote, mssg)
				
        



def blink_mote():
    print "I'm blinking!!"

def buzz_mote():
    print "I'm buzzing!!"
    




print "UDP target IP:", const.UDP_IP
print "UDP target port:", MOTE_PORT
print "message:", MESSAGE

discover_ringmaster()

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print_packet(data)
    handle_mssg(data)

