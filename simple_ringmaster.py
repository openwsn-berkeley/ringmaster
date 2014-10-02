import socket
import const
import os, sys
from utils import debug
here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))
from coap import coap

class Ringmaster:
    all_motes = []
    pointer = -1 #pointer to current mote
    c  = None

    action = None

    def __init__(self, action=const.BLINK):
        self.c = coap.coap()
        self.action = action
        self.all_motes = []
        self.pointer = -1

    def gen_ipv6_mote_addr(self, mote):
        MOTE_IP_BASE = 'bbbb::1415:92cc:0:' #primary IP address
        return 'coap://[{0}]/rt'.format(MOTE_IP_BASE + str(mote))

    def handle_incoming_packet(self,packet, addr_from):
        mssgtype = packet[5] #'D' - Discovery
        from_mote = addr_from[0].split(':')[-1]

        if (mssgtype == 'D'): #Discovery
            self.handle_discovery(from_mote)
        elif (mssgtype == 'P'): #Action performed
            self.handle_action_performed(from_mote)

    def handle_discovery(self,from_mote):
        self.all_motes.append(from_mote)
        print self.all_motes
        self.confirm_discovery(from_mote)
        if len(self.all_motes) == 1: #means this was the first mote
            self.pointer = 0 #set pointer to first element in mote list
            self.send_action(from_mote)

    def confirm_discovery(self,mote):
        #TODO - tell mote it is registered
        mote_addr = self.gen_ipv6_mote_addr(mote)
        p = self.c.PUT(
            mote_addr,
            payload = [ord('C')]
        )
        print "confirmed mote" + str(mote)

        
    def send_action(self,mote_port):
        print
        #TODO - tell mote_port to do action 

    def send_forwarding_msg(self, from_mote, next_mote):
        print
        #TODO - tell from mote to tell net_mote to do action

    def handle_action_performed(self, from_mote):
        self.advance_pointer()
        next_mote = self.all_motes[self.pointer]
        send_forwarding_msg(self, from_mote, next_mote)


    def advance_pointer(self):
        if (len(self.all_motes) == 0):
            self.pointer = -1
        else:
            self.pointer += 1
            if (self.pointer >= len(self.all_motes)):
                self.pointer = 0



    def start_ringmaster(self):
        sock = socket.socket(socket.AF_INET6, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind(('bbbb::1', 15000))
        sock.settimeout(10) #timeout of 5 seconds, for now

        while True:
            try:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                print data + " from " + addr[0]
                self.handle_incoming_packet(data, addr)
            except Exception, e:
                print e


def main():
    r = Ringmaster()
    r.start_ringmaster()

if __name__ == "__main__":
    main()

 
