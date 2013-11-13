#!/usr/bin/python

import sys
import argparse
from itertools import combinations
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.node import RemoteController
from mininet.log import setLogLevel

parser = argparse.ArgumentParser(description='Creates a central switch connected to n number of switches which are in turn connected to hosts')
parser.add_argument('-s', '--switches', dest='n', default=3, type=int,
	help='creates the topology based on the number specified (default: 3 switches connected to central switch)')
args = parser.parse_args()

net = Mininet(controller=RemoteController, link=TCLink)
s = list() #This is the list of switches
h = list() #This is the list of hosts

def createTopo(nSwitch):
	#create nodes
	c0 = net.addController()
	s.append(net.addSwitch('s0'))

	for i in range(0, nSwitch):
		s.append(net.addSwitch('s'+str(i+1)))
		h.append(net.addHost('h'+str(i)))
		net.addLink(s[0], s[i+1], bw=10, delay='10ms')
		net.addLink(h[i],s[i+1], bw=10, delay='10ms')

def pingTest():
	global h
	for x in combinations(h, 2):
		pingLabel = str(x[0]) + " --> " + str(x[1])
		pingCommand = "ping -c4 -q " + str(x[1].IP())
		print "Pinging: " + pingLabel
		x[0].cmd("echo "+str(x[0])+","+str(x[1])+" >> results.txt")
		x[0].cmd(pingCommand + " >> results.txt")

setLogLevel('info')
createTopo(args.n)
net.start()
startTest = raw_input("Start ping test (y/n)?")

if startTest == "y":
	pingTest()
	net.stop()
else:
	net.stop()