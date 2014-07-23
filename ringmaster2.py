import socket
import const
from utils import send_message_to_mote, create_mssg_packet, print_packet, split_packet

class Ringmaster:
    all_motes = []
    mote_flags = []
    last_mssg_sent = None
    expecting_response_from = None
    pointer = -1 #pointer to current mote

    action = None

    def __init__(self, action=const.BLINK):
        self.action = action
        self.all_motes = []
        self.mote_flags = []
        self.last_mssg_sent = None
        self.expecting_response_from = None
        self.pointer = -1

    def handle_incoming_packet(self,packet):
        split_mssg = split_packet(packet)
        mssgtype = int(split_mssg[0])
        from_mote = int(split_mssg[1])

        if (mssgtype == const.DISCOVERY):
            self.handle_discovery(from_mote)
        elif (mssgtype == const.ACTION_PERFORMED):
            if (from_mote == self.expecting_response_from):
                self.reset_mote_flag(from_mote)
                self.advance_pointer()
                next_mote = self.all_motes[self.pointer]
                self.expecting_response_from = next_mote
                self.last_mssg_sent = create_mssg_packet(const.FORWARD_MSG, const.RINGMASTER_PORT, next_mote, self.action)
                send_message_to_mote(from_mote,self.last_mssg_sent)
            else: #unexpected packet received
                print "unexpected packet received from mote: " + str(from_mote) + " with message " + str(recvd_mssg) + ", expecting from: " + str(self.expecting_response_from)

    def advance_pointer(self):
        if (len(self.all_motes) == 0):
            self.pointer = -1
        else:
            self.pointer += 1
            if (self.pointer >= len(self.all_motes)):
                self.pointer = 0

    def handle_discovery(self,from_mote):
        if from_mote in self.all_motes:
            self.confirm_discovery(from_mote)
            self.reset_mote_flag(from_mote)
        else:
            self.all_motes.append(from_mote)
            self.mote_flags.append(0) 
            print self.all_motes
            self.confirm_discovery(from_mote)
            if len(self.all_motes) == 1: #means this was the first mote
                self.pointer = 0 #set pointer to first element in mote list
                self.send_instruction(from_mote)

    def reset_mote_flag(self,mote):
        self.mote_flags[self.all_motes.index(mote)] = 0

    def increase_mote_flag(self,mote):
        self.mote_flags[self.all_motes.index(mote)] += 1
     
    def get_mote_flag(self,mote):
        return self.mote_flags[self.all_motes.index(mote)]

    def purge_mote(mote):
        print "purging mote" + str(mote)
        mote_idx = self.all_motes.index(mote)
        del self.all_motes[mote_idx]
        del self.mote_flags[mote_idx]

    def send_action_instruction(self,mote_port):
        self.last_mssg_sent = create_mssg_packet(self.action, const.RINGMASTER_PORT, mote_port)

    def confirm_discovery(self,from_mote):
        #do not save to the last message
        mssg = create_mssg_packet(const.CONFIRM_DISCOVERY, const.RINGMASTER_PORT, from_mote)
        send_message_to_mote(from_mote, mssg)
        
    def send_instruction(self,mote_port):
        self.expecting_response_from = mote_port
        last_mssg_sent = create_mssg_packet(self.action, const.RINGMASTER_PORT, mote_port)
        send_message_to_mote(mote_port, last_mssg_sent)

    def handle_packet_timeout(self):
        if (self.last_mssg_sent == None):
            return

        mssg_sent = int(self.last_mssg_sent.split(',')[0])
        mote_to = int(self.last_mssg_sent.split(',')[2])

        if (mote_to not in self.all_motes):
            #TODO handle this case
            return
        
        increase_mote_flag(mote_to)
        if (get_mote_flag(mote_to) > 1): #TODO make a constant?
            purge_mote(mote_to)
        
        self.advance_pointer()
        if (self.pointer == -1):
            print "no motes registered, waiting"
        else:
            next_mote = self.all_motes[self.pointer]
            self.send_instruction(next_mote)

    def start_ringmaster(self):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind((const.UDP_IP, const.RINGMASTER_PORT))
        sock.settimeout(5) #timeout of 5 seconds, for now

        while True:
            try:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                print_packet(data)
                self.handle_incoming_packet(data)
            except Exception, e:
                print e
                self.handle_packet_timeout()
                print e



def main():
    r = Ringmaster()
    r.start_ringmaster()

if __name__ == "__main__":
    main()

 
