#!/usr/bin/python3

import nmap
import sys

network = sys.argv[1]

nm = nmap.PortScanner()
nm.scan(hosts=network, arguments='-sn') # no port scan - just host check

with open('discovered_hosts.txt', 'w') as f:
	for host in nm.all_hosts(): # all ips that respond
		if nm[host].state() == 'up': # only hosts that are alive == up
			f.write(host + '\n')
			print(host + ' added to the file')