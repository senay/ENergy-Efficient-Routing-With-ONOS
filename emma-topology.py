from mininet.net import Mininet
from mininet.node import Controller,RemoteController,OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info
import random
import os
import time
import numpy as np
def topology():

        "Create a network."
        net = Mininet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
        c1 = net.addController( 'c1',controller=RemoteController,ip='192.168.56.1',port=6633 )
	c1.start()
	info( '*** Adding switches\n' )
        n = 10 #number of hosts per edge node
	lamda = 0.1 #flow arrival rate
	sw = 18 #total number of switches
	experimentDuration = 500  
	for s in range(sw):
                switch = net.addSwitch('s%s' % (s + 1))
		switch.start( [c1] )
        switches = net.switches
	
	info( '*** Creating links and adding hosts to edge switches\n' )
        j = 0
	noCore = 12#number of core switches
	CORE_SWITCHES = []#the set of core switche
        for s in switches:
                j = j + 1
                i = 0
                for ss in switches:
			i = i + 1
                        if i > j and i <= noCore and j <= noCore:#12 core switches
				if random.random() > 0.5:
                                	net.addLink(s, ss, bw = 10)
					CORE_SWITCHES.append(s)
					CORE_SWITCHES.append(ss)
			if j > noCore :# 6 edge switches
				net.addLink(s, CORE_SWITCHES[j-11], bw = 10)
		                net.addLink(s, CORE_SWITCHES[j-12], bw = 10)
				info( '*** Adding hosts to switch\n' )
		                for h in range(n):
                               		host = net.addHost('h%s' % (h + j * sw))
                              		net.addLink(host, s)
  				break
					
		        			
        net.start()
	flowCounter = 0
	mu = 0.05 # average flow duration 1/mu 20 s
	flowStartAfter = random.expovariate(lamda)
	flowStartTime = flowStartAfter
	print(flowStartAfter)
	while (experimentDuration > flowStartTime):
		time.sleep(flowStartAfter)
		hostPair = random.sample(net.hosts, 2)
		src, dst = hostPair  # a tuple of Mininet host objects
		flowDuration = random.expovariate(mu)
		print(flowDuration)
		x = 'c' + str(flowDuration)
		#src.cmd( 'ping -%s'%x, dst.IP(), '1> /tmp/h1.out 2>/tmp/h1.err &' )
		src.cmd('iperf -s &')
		dst.cmd('iperf -c', src.IP(),'-t %s &'%flowDuration)
		flowStartAfter = random.expovariate(lamda)
		flowStartTime = flowStartTime + flowStartAfter
		print(flowStartAfter)
        	print(flowStartTime)
		flowCounter = flowCounter + 1
	print(flowCounter)
	CLI( net )
if __name__ == '__main__':
	setLogLevel( 'info' )
	topology()

