from pox.core import core
from pox.lib.addresses import IPAddr, EthAddr
from pox.lib.util import dpidToStr
import pox.openflow.libopenflow_01 as of
import pox.lib.packet as pkt

log = core.getLogger()
#The following maps are used by the packet parser
opcode_map = {1:'REQUEST', 2:'REPLY', 3:'REV_REQUEST', 4:'REV_REPLY'}
ipv4_protocols = {4:'IPv4', 1:'ICMP_PROTOCOL', 6:'TCP_PROTOCOL', 17:'UDP_PROTOCOL', 2:'IGMP_PROTOCOL'}

class Switch (object):

  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Use this table to keep track of which ethernet address is on
    # which switch port (keys are MACs, values are ports).
    self.mac_to_port = {}

    log.info("Switch Active")

  def resend_packet (self, packet_in, out_port):
    """
    Instructs the switch to resend a packet that it had sent to us.
    "packet_in" is the ofp_packet_in object the switch had sent to the
    controller due to a table-miss.
    """
    msg = of.ofp_packet_out()
    msg.data = packet_in

    # Add an action to send to the specified port
    action = of.ofp_action_output(port = out_port)
    msg.actions.append(action)

    # Send message to switch
    self.connection.send(msg)

  def switchImplementation (self, packet, packet_in):
    """
    Implement switch-like behavior.
    """

    #Parse packet info to gain an idea of what is happening
    #if controller receives packet
    if packet.type == pkt.ethernet.IP_TYPE:
      ip_packet = packet.payload
      log.info("IP Packet detected")
      log.info("IP protocol: %s" % (ipv4_protocols[ip_packet.protocol]))
      log.info("Source IP: %s" % (ip_packet.srcip))
      log.info("Destination IP: %s" % (ip_packet.dstip))

    if packet.type == pkt.ethernet.ARP_TYPE:
      arp_packet = packet.payload
      log.info("ARP Packet detected")
      log.info("ARP opcode: %s" % (opcode_map[arp_packet.opcode]))
      log.info("Source MAC: %s" % (arp_packet.hwsrc))
      log.info("Destination MAC: %s" % (arp_packet.hwdst))

    # Learn the port for the source MAC
    self.mac_to_port[packet.src] = packet_in.in_port
    src_port = packet_in.in_port

    if packet.dst in self.mac_to_port:
        dst_port = self.mac_to_port[packet.dst]

        log.debug("Installing %s.%i -> %s.%i" % 
                  (packet.src, src_port, packet.dst, dst_port))
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 10
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port = dst_port))
        self.connection.send(msg)
        self.resend_packet(packet_in, dst_port)
    else:
      # Flood the packet out everything but the input port
      # This part looks familiar, right?
      self.resend_packet(packet_in, of.OFPP_ALL)

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.

    self.switchImplementation(packet, packet_in)

  #Used to construct and send an IP packet
  #This is primarily used as a secondary test option aside from ping
  #Could also have applications for multi-switch topology testing
  def send_IP_packet(self, src_ip, dst_ip):
    ip4_Packet = pkt.ipv4()
    ip4_Packet.srcip = IPAddr(src_ip)
    ip4_Packet.dstip = IPAddr(dst_ip)
    ether = pkt.ethernet()
    ether.type = pkt.ethernet.IP_TYPE
    ether.srcip = IPAddr(src_ip)
    ether.dstip = IPAddr(dst_ip)
    ether.payload = ip4_Packet
    msg = of.ofp_packet_out()
    msg.data = ether
    msg.actions.append(of.ofp_action_output(port = of.OFPP_ALL))
    self.connection.send(msg)

  def returnDPID(self):
    dpid = dpidToStr(self.connection.dpid)
    log.debug("DPID: %s" % (dpid))

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    switch = Switch(event.connection)
    core.Interactive.variables['switch'] = switch
  core.openflow.addListenerByName("ConnectionUp", start_switch)
