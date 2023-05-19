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
	
# Try creating a complex scenario
# Delete the previous scenario before starting a new one!!!
# You dont have to create server instance
def task_createComplexScenario():
	NETWORK_NAMES = ["young1","young2","young3","young4","young5","young6"]
	SUBNET_NAMES  = ["youngsubnet1","youngsubnet2","youngsubnet3","youngsubnet4","youngsubnet5","youngsubnet6"]
	CIDRS = ["192.168.111.0/24","192.168.112.0/24","192.168.113.0/24","192.168.114.0/24","192.168.115.0/24","192.168.116.0/24"]
	GATEWAYS = ["192.168.111.1","192.168.112.1","192.168.113.1","192.168.114.1","192.168.115.1","192.168.116.1"]
	START_ALLOS = ["192.168.111.2","192.168.112.2","192.168.113.2","192.168.114.2","192.168.115.2","192.168.116.2"]
	END_ALLOS = ["192.168.111.254","192.168.112.254","192.168.113.254","192.168.114.254","192.168.115.254","192.168.116.254"]
	ROUTER_NAMES = ["ROUTER1","ROUTER2","ROUTER3"]

# Try to perform static routing algo, change anything that is needed
# Delete the previous scenario before starting a new one!!!
def task_algo():
	pass

if __name__=='__main__':
	task_createScenario()
