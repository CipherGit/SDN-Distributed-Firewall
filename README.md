A Distrubuted Firewall Prototype for Software Defined Networks (SDN)
============

Introduction
------------
The traditional firewall is usually a physical hardware device
placed on the edge of a network in order to protect the inner network
from an outer one or the internet. In a large infrastructure, 
firewalls are also used internally as well to further protect a subdivision of the network.
The problem with this is that each of these firewalls would still have to be manually
configured and maintained which would be costly and time consuming. However, with the emergence
of SDN, it is now possible to centralize the control of network devices
due to the decoupling of the control structures from the physical.

The goal of this undergraduate thesis was to take advantage of the capabilities of an SDN
to develop a centralized distributed firewall which is different from the
hypervisor-based virtual distributed firewall of today. The OpenFlow protocol was used
to develop the prototypes with POX as the primary controller. The prototype was simulated
using mininet but no actual hardware implementation has been done as of writing. The source
codes can be downloaded from this repository.

