import socket
import sys
import const
from utils import send_message_to_mote, create_mssg_packet, print_packet

class Client:
    MOTE_PORT = -1
    MESSAGE = None
    discovered = False
    sock = None

    def __init__(self, self_port):
        self.MOTE_PORT = self_port
        self.MESSAGE = "Mote " + str(self.MOTE_PORT) + " online"
 

    def initialize(self):
        self.sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        self.sock.bind((const.UDP_IP, self.MOTE_PORT))

        self.print_intro()

        self.discover_ringmaster()

        while True:
            data, addr = self.sock.recvfrom(1024) #buffer size is 1024 bytes
            print_packet(data)
            self.handle_mssg(data)

    def print_intro(self):
        print "UDP target IP:", const.UDP_IP
        print "UDP target port:", self.MOTE_PORT
        print self.MESSAGE

    def discover_ringmaster(self):
        print "Discovering ringmaster mote..."
        self.discovered = False
        response = None
        while not self.discovered:
            send_message_to_mote(const.RINGMASTER_PORT, create_mssg_packet(const.DISCOVERY, self.MOTE_PORT, const.RINGMASTER_PORT))
            self.response = self.wait_for_response()
            if self.response is not None:
                #TODO check that response is the right one
                self.discovered = True

    def wait_for_response(self, time = 5):
        try:
            self.sock.settimeout(time)
            data, addr = self.sock.recvfrom(1024)
            self.sock.settimeout(None) #set timeout back to inf
            return data
        except Exception, e:
            print "No response from ringmaster after " + str(time) + " seconds"
            return None

    def handle_mssg(self, data):
        recvd_mssg = int(data.split(',')[0])
        from_mote = int(data.split(',')[1])
        if (recvd_mssg == const.FORWARD_MSG):
            to_mote = int(data.split(',')[2])
            action = int(data.split(',')[3])
            mssg = create_mssg_packet(action, self.MOTE_PORT, to_mote)
            send_message_to_mote(to_mote, mssg)
        elif (recvd_mssg == const.BLINK or const.BUZZ):
            self.perform_action(recvd_mssg)
            send_message_to_mote(const.RINGMASTER_PORT, create_mssg_packet(const.ACTION_PERFORMED, self.MOTE_PORT, const.RINGMASTER_PORT, recvd_mssg))

    def perform_action(self, action):
        if (action == const.BLINK):
            print "I'm blinking!"
        elif (action == const.BUZZ):
            print "I'm buzzing!"


def main(self_port):
    client = Client(self_port)
    client.initialize()

if __name__ == '__main__':
    self_port = int(sys.argv[1])
    main(self_port)
