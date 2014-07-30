import socket
import const
import time, random


def create_mssg_packet(mssgtype, from_port, to_port=None, action_to_do=None):
    s = str(mssgtype)+","+str(from_port) + "," + str(to_port) + "," + str(action_to_do)
    return s

def split_packet(packet):
    return packet.split(',')

def send_message_to_mote(mote_port, mssg):
    time.sleep(random.uniform(0.8, 3))
    print_packet(mssg, "Sending: ")
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.sendto(mssg, (const.UDP_IP, mote_port))
    temp_sock.close()


def print_packet(packet, mssg = ""):
    mssgtype = int(packet.split(',')[0])
    from_mote = int(packet.split(',')[1])
    to_port = int(packet.split(',')[2])
    action_to_do = packet.split(',')[3]

    if (action_to_do != "None"):
        action_to_do = int(action_to_do)

    action_string = None
    if (action_to_do == const.BLINK):
        action_string = "blink"
    elif(action_to_do == const.BUZZ):
        action_string = "buzz"

    if len(mssg) > 0:
        mssg += " "

    if (mssgtype == const.DISCOVERY):
        print mssg + "Discovery from mote " + str(from_mote)
    elif (mssgtype == const.CONFIRM_DISCOVERY):
        print mssg + "Confirming discovery of mote " + str(to_port) + " from ringmaster"
    elif (mssgtype == const.ACTION_PERFORMED):
        print mssg + "Mote " + str(from_mote) + " performed action " + str(action_string)
    elif (mssgtype == const.FORWARD_MSG):
        print mssg + "Forward action " + action_string + " from " + str(from_mote) + " to " + str(to_port)
    elif (mssgtype == const.BLINK):
        print mssg + "Make " + str(to_port) + " blink"
    elif (mssgtype == const.BUZZ):
        print mssg + "Make " + str(to_port) + " buzz"

def debug(mssg, debug=False):
    if debug:
        print mssg
