import socket
import const
from utils import send_message_to_mote, create_mssg_packet, print_packet, split_packet

class Ringmaster:
    all_motes = []
    last_mssg_sent = None
    retry_count = 0
    pointer = -1 #pointer to current mote

    action = None

    def __init__(self, action=const.BLINK):
        self.action = action

    def handle_incoming_packet(self,packet):
        split_mssg = split_packet(packet)
        mssgtype = int(split_msg[0])
        from_mote = int(split_msg[1])

        if (mssgtype == const.DISCOVERY):
            handle_discovery(from_mote)
        elif (mssgtype == const.ACTION_PERFORMED):
            next_mote = advance_to_next_mote()
            last_mssg_sent = create_mssg_packet(const.FORWARD_MSG, const.RINGMASTER_PORT, next_mote, action)
            send_message_to_mote(from_mote, last_mssg_sent)

    def advance_to_next_mote(self):
        global pointer
        pointer += 1
        if (pointer >= len(all_motes)):
            pointer = 0
        return all_motes[pointer]


    def handle_discovery(self,from_mote):
        global last_mssg_sent
        if from_mote in all_motes:
            #already have this mote registered
            return
        else :
            all_motes.append(from_mote)
            print "all motes currently" + all_motes
            last_mssg_sent = create_mssg_packet(const.CONFIRM_DISCOVERY, const.RINGMASTER_PORT, from_mote)
            send_message_to_mote(from_mote, last_mssg_sent)
            if len(all_motes) == 1: #means this was first mote
                global pointer
                pointer = 0
                send_action_instruction(from_mote)

    def send_action_instruction(self,mote_port):
        global last_mssg_sent
        last_mssg_sent = create_mssg_packet(action, const.RINGMASTER_PORT, mote_port)

    def handle_packet_timeout(self):
        global retry_count
        split_mssg = split_packet(packet)
        mssgtype = int(split_msg[0])
        from_mote = int(split_msg[2])
        if (retry_count == 0):
            retry_count += 1
            send_message_to_mote(mote_to, last_mssg_sent)
        else:
            #TODO handle this error case
            retry_count = 0

    def start_ringmaster(self):
        sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
        sock.bind((const.UDP_IP, const.RINGMASTER_PORT))
        sock.settimeout(5) #timeout of 5 seconds, for now

        while True:
            try:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                print_packet(data)
                recvd_mssg = int(data.split(',')[0])
                from_mote = int(data.split(',')[1])
                self.handle_incoming_packet(data)
            except Exception, e:
                #handle_packet_timeout(last_mssg_sent)
                print e



def main():
    r = Ringmaster()
    r.start_ringmaster()

if __name__ == "__main__":
    main()

 
