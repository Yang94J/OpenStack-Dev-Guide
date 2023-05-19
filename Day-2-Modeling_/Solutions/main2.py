from modeling import *

# ImageId
CIRROS_ID = "<REPLACE WITH IMAGE ID>"

# FlavorId
FLAVOR_ID = "<REPLACE WITH FALVOR ID>"

# Try create a scenario using the given script
# Delete the previous scenario before starting a new one!!!
def task_createScenario():

	# mimic user input
	NETWORK_NAME1 = "young"
	SUBNET_NAME1 = "youngsub"
	CIDR1 = "192.168.111.0/24"
	GATEWAY1 = "192.168.111.1"
	START_ALLO1 = "192.168.111.2"
	END_ALLO1 = "192.168.111.254"
	SERVER_NAME1 = "youngServer1"
	NETWORK_NAME2 = "young2"
	SUBNET_NAME2 = "youngsub2"
	CIDR2 = "192.168.112.0/24"
	GATEWAY2 = "192.168.112.1"
	START_ALLO2 = "192.168.112.2"
	END_ALLO2 = "192.168.112.254"
	SERVER_NAME2 = "youngServer2"
	ROUTERNAME = "router_young"
	
	network1 = Network(NETWORK_NAME1).create()
	network2 = Network(NETWORK_NAME2).create()
	subnetwork1 = SubNetwork(
		network1,SUBNET_NAME1,CIDR1,GATEWAY1,START_ALLO1,END_ALLO1
	).create()
	subnetwork2 = SubNetwork(
		network2,SUBNET_NAME2,CIDR2,GATEWAY2,START_ALLO2,END_ALLO2
	).create()
	router = Router(ROUTERNAME).create()
	router.attachPort(Port(subnetwork1).create())
	router.attachPort(Port(subnetwork2).create())
	server1 = Server(network1,SERVER_NAME1,FLAVOR_ID,CIRROS_ID).create()
	server2 = Server(network2,SERVER_NAME2,FLAVOR_ID,CIRROS_ID).create()

# Try creating a complex scenario
# Delete the previous scenario before starting a new one!!!
# You dont have to create server instance
def task_createComplexScenario():

	#mimic user input
	NETWORK_NAMES = ["young1","young2","young3","young4","young5","young6"]
	SUBNET_NAMES  = ["youngsubnet1","youngsubnet2","youngsubnet3","youngsubnet4","youngsubnet5","youngsubnet6"]
	CIDRS = ["192.168.111.0/24","192.168.112.0/24","192.168.113.0/24","192.168.114.0/24","192.168.115.0/24","192.168.116.0/24"]
	GATEWAYS = ["192.168.111.1","192.168.112.1","192.168.113.1","192.168.114.1","192.168.115.1","192.168.116.1"]
	START_ALLOS = ["192.168.111.2","192.168.112.2","192.168.113.2","192.168.114.2","192.168.115.2","192.168.116.2"]
	END_ALLOS = ["192.168.111.254","192.168.112.254","192.168.113.254","192.168.114.254","192.168.115.254","192.168.116.254"]
	ROUTER_NAMES = ["ROUTER1","ROUTER2","ROUTER3"]
	
	
	n = len(NETWORK_NAMES)
	networks = []
	subnetworks = []
	routers = []
	for i in range(n):
		network = Network(NETWORK_NAMES[i]).create()
		subnetwork = SubNetwork(network,SUBNET_NAMES[i],CIDRS[i],GATEWAYS[i],START_ALLOS[i],END_ALLOS[i]).create()
		networks.append(network)
		subnetworks.append(subnetwork)
	n = len(ROUTER_NAMES)
	for i in range(n):
		router = Router(ROUTER_NAMES[i]).create()
		routers.append(router)
	routers[0].attachPort(Port(subnetworks[0]).create())
	routers[0].attachPort(Port(subnetworks[1]).create())	
	routers[0].attachPort(Port(subnetworks[2]).create())		
	routers[1].attachPort(Port(subnetworks[2]).create())	
	routers[1].attachPort(Port(subnetworks[3]).create())	
	routers[2].attachPort(Port(subnetworks[3]).create())
	routers[2].attachPort(Port(subnetworks[4]).create())	
	routers[2].attachPort(Port(subnetworks[5]).create())
	task_algo(subnetworks=subnetworks)
	
# Try to perform static routing algo, change anything that is needed
# Delete the previous scenario before starting a new one!!!
from typing import List

def task_algo(subnetworks : List[SubNetwork]) -> None:
    for subnet in subnetworks:
	    if len(subnet.portList) == 1:
		    port = subnet.portList[0]
		    dfsRouter(port,[])
		    
def dfsRouter(port : 'Port', visitedPortList : List[Port]):
	visitedPortList.append(port)
	list = []
	router = port.attachedRouter
	for nextPort in router.attachPortList:
		if nextPort not in visitedPortList:
			tmp = dfsSubnet(nextPort,visitedPortList)
			for tmpItem in tmp:
				tmpcidr = tmpItem[0]
				tmpPort = tmpItem[1]
				if not nextPort.subnet.subnetCidr == tmpcidr:
					router.addStaticRoute(tmpcidr,tmpPort)
				list.append((tmpcidr,port))
	return list
			
			

def dfsSubnet(port : 'Port', visitedPortList : List[Port]):
	visitedPortList.append(port)
	list = []
	subnet = port.subnet
	for nextPort in subnet.portList:
		if nextPort not in visitedPortList:
			tmp = dfsRouter(nextPort,visitedPortList)
			list.extend(tmp)
	list.append((subnet.subnetCidr,port))
	return list

if __name__=='__main__':
	#task_createScenario()
	task_createComplexScenario()
