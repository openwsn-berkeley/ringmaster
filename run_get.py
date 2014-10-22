import os
import sys
here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

from coap import coap

mote = int(sys.argv[1])

MOTE_IP_BASE = 'bbbb::1415:92cc:0:' #primary IP address



def coap_get(mote, conf = True):
    print "running get on mote " + str(mote) + " with confirmable " + str(conf)
    c = coap.coap()
    mote_ip = MOTE_IP_BASE + str(mote)

    p = c.GET('coap://[{0}]/rt'.format(mote_ip),
            confirmable=conf
            )

    print "done"
    print ''.join([chr(b) for b in p])

    c.close()

    return p

def coap_put(mote, conf = True):
    print "running put on mote " + str(mote) + " with confirmable " + str(conf)
    c = coap.coap()
    mote_ip = MOTE_IP_BASE + str(mote)

    p = c.PUT('coap://[{0}]/l'.format(mote_ip), 
            payload = [ord('C')], 
            confirmable=conf
            )
    print "done"
    print ''.join([chr(b) for b in p])
    c.close()

    return p

def coap_post(mote, conf = True):
    print "running post on mote " + str(mote) + " with confirmable " + str(conf)
    c = coap.coap()
    mote_ip = MOTE_IP_BASE + str(mote)

    p = c.POST('coap://[{0}]/l'.format(mote_ip), 
            payload = [ord('C')],
            confirmable=conf
            )
    print "done"
    print ''.join([chr(b) for b in p])
    c.close()

    return p
    

coap_get(mote)

coap_put(mote)

#coap_post(mote)

coap_get(mote, False)

coap_put(mote, False)

#coap_post(motei, False)
raw_input("Done. Press enter to close.")
