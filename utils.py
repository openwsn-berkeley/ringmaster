import socket
import const
import time, random

def create_mssg_packet(mssgtype, mote_port):
    s = str(mssgtype)+","+str(mote_port)
    return s


def send_message_to_mote(mote_port, mssg):
    time.sleep(random.uniform(0.8, 3))
    print "Sending message to mote " + str(mote_port) + ", mssg: " + mssg
    temp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    temp_sock.sendto(mssg, (const.UDP_IP, mote_port))
    temp_sock.close()
