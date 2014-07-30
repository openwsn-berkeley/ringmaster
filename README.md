To start, run ringmaster.py (non-object version)
    RingMaster will communicate on port 5000

Start clients via 'client.py portNum' where portNum is any valid port
Start as many instances as you wish (each instance emulates a device)
Break the chain by killing a process and observe what happens!

BUG:
-unknown packet received when two motes connect fast

TODO (order of importance):
-moving simulation to CoAP
-unit tests on ringmaster/client + integration tests
-various error-handling strategies at ringmaster startup
-queue for incoming packets?

future:
-web visualization
 
7/22
ringmaster2 written in OOP

7/28
client as object

7/29
fixed some mote-purging bugs, better debugging
