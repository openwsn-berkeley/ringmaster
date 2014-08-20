/**
\brief A CoAP resource which indicates the board its running on.
*/

#include "openwsn.h"
#include "rrt.h"
#include "opencoap.h"
#include "openqueue.h"
#include "packetfunctions.h"
#include "openserial.h"
#include "openrandom.h"
#include "board.h"
#include "idmanager.h"

//=========================== defines =========================================

const uint8_t rrt_path0[] = "rt";

//=========================== variables =======================================

rrt_vars_t rrt_vars;

uint8_t * tmp_payload;

//=========================== prototypes ======================================

owerror_t     rrt_receive(
   OpenQueueEntry_t* msg,
   coap_header_iht*  coap_header,
   coap_option_iht*  coap_options
);

void          rrt_sendDone(
   OpenQueueEntry_t* msg,
   owerror_t error
);

uint8_t *  getIPFromPayload(
	uint8_t* payload,
	int      ip_to_get 
);

void rotateState();

//=========================== public ==========================================

/**
\brief Initialize this module.
*/
void rrt_init() {
   
   // do not run if DAGroot
   if(idmanager_getIsDAGroot()==TRUE) return; 
   
   // prepare the resource descriptor for the /rt path
   rrt_vars.desc.path0len             = sizeof(rrt_path0)-1;
   rrt_vars.desc.path0val             = (uint8_t*)(&rrt_path0);
   rrt_vars.desc.path1len             = 0;
   rrt_vars.desc.path1val             = NULL;
   rrt_vars.desc.componentID          = COMPONENT_RRT;
   rrt_vars.desc.callbackRx           = &rrt_receive;
   rrt_vars.desc.callbackSendDone     = &rrt_sendDone;

   //initialize state
   rrt_vars.STATE                     = 0;
   
   // register with the CoAP module
   opencoap_register(&rrt_vars.desc);
}

//=========================== private =========================================

/**
\brief Called when a CoAP message is received for this resource.

\param[in] msg          The received message. CoAP header and options already
   parsed.
\param[in] coap_header  The CoAP header contained in the message.
\param[in] coap_options The CoAP options contained in the message.

\return Whether the response is prepared successfully.
*/

owerror_t rrt_receive(
      OpenQueueEntry_t* msg,
      coap_header_iht* coap_header,
      coap_option_iht* coap_options
   ) {
   
   OpenQueueEntry_t* pkt;
   owerror_t outcome;
   
   switch (coap_header->Code) {
      case COAP_CODE_REQ_GET:
         rotateState(&rrt_vars.STATE);
         
         //=== reset packet payload (we will reuse this packetBuffer)
         msg->payload                     = &(msg->packet[127]);
         msg->length                      = 0;
         
         //=== prepare  CoAP response
         
	    //ip from
         packetfunctions_reserveHeaderSize(msg,4);
         msg->payload[0] = '0' + rrt_vars.STATE;
         msg->payload[1] = 'f';
         msg->payload[2] = 'f';
         msg->payload[3] = 'f';

         // payload marker
         packetfunctions_reserveHeaderSize(msg,1);
         msg->payload[0] = COAP_PAYLOAD_MARKER;
         
         // set the CoAP header
         coap_header->Code                = COAP_CODE_RESP_CONTENT;
         
         outcome                          = E_SUCCESS;
         break;
			case COAP_CODE_REQ_PUT:
			case COAP_CODE_REQ_POST:
				 tmp_payload = getIPFromPayload(msg->packet, COAP_GET_FROM_IP);

				 msg->payload 										= &(msg->packet[127]);
				 msg->length											= 0;

				 packetfunctions_reserveHeaderSize(msg, 4);
				 msg->payload[0] = 'y';
				 msg->payload[1] = 'x';
				 msg->payload[2] = tmp_payload[0];
				 msg->payload[3] = tmp_payload[1];
				 msg->payload[4] = tmp_payload[2];
				 msg->payload[5] = tmp_payload[3];
				 msg->payload[6] = tmp_payload[4];
				 msg->payload[7] = tmp_payload[5];
				 msg->payload[8] = tmp_payload[6];
				 msg->payload[9] = tmp_payload[7];

                 //SEND CODE HERE
                 pkt->creator   = COMPONENT_RRT;
                 pkt-owner      = COMPONENT_RRT;

                 packetfunctions_reserveHeaderSize(pkt, PAYLOADLEN);
                 for (i=0; i<PAYLOADLEN; i++) {
                    pkt->payload[i] = i;
                 }
                 //metada
                 pkt->l4_destination_port   = WKP_UDP_COAP; //5683
                 pkt->l3_destinationAdd.addr_128b[0],&ipAddr_motesEecs, 16);
                 //send
                 outcome = opencoap_send(pkt,
                                         COAP_TYPE_NON,
                                         COAP_CODE_REQ_PUT,
                                         numOptions,
                                         &rex_vars.desc) //change port dest here?
                 //END

                 // payload marker
                 packetfunctions_reserveHeaderSize(msg,1);
                 msg->payload[0] = COAP_PAYLOAD_MARKER;

                 // set the CoAP header
                 coap_header->Code                = COAP_CODE_RESP_CONTENT;

				 outcome													= E_SUCCESS;
				 break;
      default:
         // return an error message
         outcome = E_FAIL;
   }
   
   return outcome;
}

//add more states as needed
//TODO
void rotateState(uint8_t * state) {
    
   switch(*state) {
        case 0:
            *state = 1;
            break;
        case 1:
            *state = 2;
            break;
        case 2:
            *state = 0;
            break;
        default:
            *state = 0;
            break;
   } 

}

uint8_t * getIPFromPayload(uint8_t* payload, int msg) {
	uint8_t * newPtr = payload;
	switch (msg) {
		case COAP_GET_FROM_IP:
			newPtr = newPtr + 0;
			break;
		case COAP_GET_TO_IP:
			newPtr = newPtr + 1;
			break;
		case COAP_GET_NEXT_IP:
			newPtr = newPtr + 2;
			break;
		case COAP_GET_MSG:
			newPtr = newPtr + 3;
			break;
		default:
			break;
	}

	return newPtr;
}

/**
\brief The stack indicates that the packet was sent.

\param[in] msg The CoAP message just sent.
\param[in] error The outcome of sending it.
*/
void rrt_sendDone(OpenQueueEntry_t* msg, owerror_t error) {
   openqueue_freePacketBuffer(msg);
}
