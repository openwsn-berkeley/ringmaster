import os
import sys
here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

from coap import coap

mote = int(sys.argv[1])


MOTE_IP_BASE = 'bbbb::1415:92cc:0:' #primary IP address



def coap_get(mote):
    c = coap.coap()
    mote_ip = MOTE_IP_BASE + str(mote)
    p = c.GET('coap://[{0}]/rt'.format(mote_ip))

    return p


p = coap_get(mote)
print p
print ''.join([chr(b) for b in p])

p = coap_get(mote)
print p
print ''.join([chr(b) for b in p])

c.close()

raw_input("Done. Press enter to close.")
