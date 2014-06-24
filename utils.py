import socket
import const
import time, random


def create_mssg_packet(mssgtype, from_port, to_port=None, action_to_do=None):
    s = str(mssgtype)+","+str(from_port) + "," + str(to_port) + "," + str(action_to_do)
    return s


def send_message_to_mote(mote_port, mssg):
    time.sleep(random.uniform(0.8, 3))
    print_packet(mssg)
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.sendto(mssg, (const.UDP_IP, mote_port))
    temp_sock.close()


def print_packet(packet):
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

    if (mssgtype == const.DISCOVERY):
        print "Sending discovery from mote " + str(from_mote)
    elif (mssgtype == const.CONFIRM_DISCOVERY):
        print "Confirming discovery of mote " + str(to_port) + " from ringmaster"
    elif (mssgtype == const.ACTION_PERFORMED):
        print "Mote " + str(from_mote) + " performed action " + str(action_string)
    elif (mssgtype == const.FORWARD_MSG):
        print "Forward action " + str(action_string) + " from " + str(from_mote) + " to " + str(to_port)
    elif (mssgtype == const.BLINK):
        print "Make " + str(to_port) + " blink"
    elif (mssgtype == const.BUZZ):
        print "Make " + str(to_port) + " buzz"
