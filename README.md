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

How to Use the Files
-------------
1. Run the pox controller in interactive mode with the firewall_pt_fb file and 
your choice implementation for an l2 switch. In the sample command below, I'm using 
my own implementation for the l2 switch:

  <code>./pox.py py log.level --DEBUG firewall_pt_fb switch_pt</code>

2. In a separate console, you can create a mininet simulation of a network. For test purposes, 
I used an experimental topology wherein there is a central switch and the user may choose 
to add N number of switches to this central switch with each connected to thier own hosts:
    
  <code>./dynamic_host.py -s N</code>

3. At this point, you may opt to give the firewalls some commands by referring to
a particular firewall via the index i since each switch device practically doubles as a firewall. 

  To add a rule to a particular firewall:
  
  <code>fw[i].addRule(address, toAll=False, dl_type, nw_proto)</code>
  
  To remove a rule from a particular firewall:
  
  <code>fw[i].delRule(address, toAll=False, dl_type, nw_proto)</code>
  
  To show installed rules in a particular firewall:
  
  <code>fw[i].showRules()</code>
  
  Take not that if the toAll argument is true, then the rule would be added or removed in all firewalls

Tests and Results
-----------------
Using dynamic_host.py, I was able to test the firewall prototype with a ping test which pings every possible host
combination 4 times. I used 15 hosts with each connected to a switch and these switches are then connected a single central switch.
A total of three test parameters was done. The first involved no rules applied at all, the second involved
all the firewalls having the same rules and the last involved having only the central switch with the rules.

In order to recreate the test results, here are the steps:

**Case 1: No rules applied**

  1.) <code>./pox.py py log.level --DEBUG firewall_pt_fb switch_pt</code>

  2.) <code>./dynamic_host.py -s 15</code>

  3.) In the mininet console: press y and enter
  
  4.) Exit POX and mininet to reset
  
**Case 2: Rules applied to all**

  1.) <code>./pox.py py log.level --DEBUG firewall_pt_fb switch_pt</code>

  2.) <code>./dynamic_host.py -s 15</code>

  3.) In the pox console: <code>fw[0].addRule("10.0.0.1", True)</code>
  
  4.) In the mininet console: press y and enter
  
  5.) Exit POX and mininet to reset
  
**Case 3: Rules applied to central switch only**

  1.) <code>./pox.py py log.level --DEBUG firewall_pt_fb switch_pt</code>

  2.) <code>./dynamic_host.py -s 15</code>

  3.) In the pox console: <code>fw[0].addRule("10.0.0.1")</code>
  
  4.) In the mininet console: press y and enter
  
  5.) Exit POX and mininet to reset
