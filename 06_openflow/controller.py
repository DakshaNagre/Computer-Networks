import os
import six

from ryu.base import app_manager
from ryu.controller.handler import CONFIG_DISPATCHER, \
    MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.ofproto.ofproto_v1_3 import OFPG_ANY
from ryu.controller import ofp_event
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from ryu.lib.packet import arp
from ryu.lib.packet import ipv4
from ryu.lib.packet import ipv6

class MyController(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MyController, self).__init__(*args, **kwargs)
        self.datapaths = {}

        
    @set_ev_cls(ofp_event.EventOFPStateChange,
                [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.logger.debug('register datapath: %016x', datapath.id)
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                self.logger.debug('unregister datapath: %016x', datapath.id)
                del self.datapaths[datapath.id]

                
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # delete any flows that may already exist
        self.delete_flows(datapath)

        # pass ARP to the NORMAL host switching behavior
        match = parser.OFPMatch(eth_type=ether_types.ETH_TYPE_ARP)
        actions = [parser.OFPActionOutput(ofproto.OFPP_NORMAL,
                                          ofproto.OFPCML_NO_BUFFER),
                   parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 100, match, actions)

        # install table-miss flow entry (default packet-in to controller)
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

        # You will add your assignment routes in this method defined
        # at the end of the file
        if os.environ.get("RYUMODE",None) != "ARP": self.add_routes(datapath, ofproto, parser)


    # removes all flows in table 0
    def delete_flows(self, datapath):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        instructions = []
        mod = parser.OFPFlowMod(datapath, 0, 0, 0,
                                ofproto.OFPFC_DELETE, 0, 0,
                                1,
                                ofproto.OFPCML_NO_BUFFER,
                                ofproto.OFPP_ANY,
                                OFPG_ANY, 0,
                                match, instructions)
        datapath.send_msg(mod)
        
    
    # helper method to install flows to a given datapath (switch)
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)

            
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        
        # get Datapath ID to identify connected switches
        dpid = datapath.id

        # get the received port number from packet_in message
        in_port = msg.match['in_port']

        # analyze the received packets using the packet library
        pkt = packet.Packet(msg.data)

        # let's look at Ethernet packets
        eth_pkt = pkt.get_protocol(ethernet.ethernet)
        dst = eth_pkt.dst
        src = eth_pkt.src

        # out packet-in handler simply logs each packet arriving over the control channel
        self.logger.info("-------------------------------------")
        self.logger.info("DPID    : {}".format(dpid))
        self.logger.info("IN-PORT : {}".format(in_port))
        self.logger.info("SMAC    : {}".format(src))
        self.logger.info("DMAC    : {}".format(dst))
        self.logger.info("ETH-TYPE: {0:#x}".format(eth_pkt.ethertype))

        # see if there's IPv4 info
        v4_pkt = pkt.get_protocol(ipv4.ipv4)
        if v4_pkt:
            self.logger.info("IP-SRC  : {}".format(v4_pkt.src))
            self.logger.info("IP-DST  : {}".format(v4_pkt.dst))
            self.logger.info("IP-TTL  : {}".format(v4_pkt.ttl))
            self.logger.info("IP-PROTO: {}".format(v4_pkt.proto))
        self.logger.info("-------------------------------------")
        if os.environ.get("RYUMODE",None) == "ARP": self.learn_routes(msg, datapath, ofproto, parser)

    def add_routes(self, datapath, ofproto, parser):
        # This is where you will add flows to route IPv4 traffic
        # across your experiment testbed
        #
        # This method is invoked when new switches (datapaths) connect
        # to the controller. (From switch_features_handler() above)
        #
        # Any IPv4 traffic that does not match one of your installed
        # rules will be output in the packet_in_handler() above. You
        # can use the above methods, and example below, as a starting
        # point for creating your own rules.
        pass
    
    def learn_routes(self, msg, datapath, ofproto, parser):
        # This is where you will learn the IPv4 routes based on
        # incoming traffic
        #
        # This method will replace add_routes when the RYUMODE
        # environment variable is set to ARP
        pass
