import os
import sys
here = sys.path[0]
sys.path.insert(0,os.path.join(here,'..','coap'))

from coap import coap

number_of_motes = int(sys.argv[1])
dag_mote = int(sys.argv[2])


motes_in_mesh = range(1,number_of_motes+1)

del motes_in_mesh[dag_mote-1]

print "Motes on network: "
print motes_in_mesh

MOTE_IP_BASE = 'bbbb::1415:92cc:0:' #primary IP address

c = coap.coap()


def coap_get(mote):
	mote_ip = MOTE_IP_BASE + str(mote)
	return c.GET('coap://[{0}]/rt'.format(mote_ip))


# read the information about the board status
for i in motes_in_mesh:
	p = coap_get(i)
	print ''.join([chr(b) for b in p])

# toggle debug LED
#p = c.PUT(
#    'coap://[{0}]/rt'.format(MOTE_IP),
#    payload = [ord('2')],
#)


raw_input("Done. Press enter to close.")
