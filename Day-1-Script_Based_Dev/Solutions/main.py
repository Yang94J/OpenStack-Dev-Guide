# coding=utf-8

# Params needed
USERNAME = "admin"
PASSWORD = "<REPLACE WITH PASSWORD HERE>"
USER_DOMAIN_NAME= "Default"
PROJECT_ID = "<REPLACE WITH PROJECT ID>"

# Endpoint
CONTROLLER = "<REPLACE WITH OPENSTACK PLATFORM IP>"
KEYSTONE_PORT = "35357"
NEUTRON_PORT = "9696"
NOVA_PORT = "8774"

# ImageId
CIRROS_ID = "<REPLACE WITH IMAGE ID"

# FlavorId
FLAVOR_ID = "<REPLACE WITH FALVOR ID>"


import json
import identity
import neutron
import nova


# Guide : How to get Identity Token
def task_getToken():
    token = identity.identity_getToken(USERNAME,PASSWORD,USER_DOMAIN_NAME,PROJECT_ID,CONTROLLER,KEYSTONE_PORT)
    print("Get token")
    print(json.dumps(token,indent=4))

# Task1 : print out Network List
def task_printNetworkList():
	print("------------------------------------Task 1 Start ------------------------------")
	tokenId = identity.identity_getToken(USERNAME,PASSWORD,USER_DOMAIN_NAME,PROJECT_ID,CONTROLLER,KEYSTONE_PORT)['token']
	print("Get tokenId : {}".format(tokenId))
	networks = neutron.neutron_getNetworkList(tokenId,CONTROLLER,NEUTRON_PORT)
	print("NetworkList")
	print(json.dumps(networks,indent=4))
	print("------------------------------------Task 1 Finish------------------------------")
    
    
# Task2 : try to create a network, and create an instance in the network
# IMPORTANT : Please delete your instance and network after each test!!!!!!!!
def task_createInstance():

	NETWORK_NAME = "young"
	SUBNET_NAME = "youngsub"
	CIDR = "192.168.111.0/24"
	GATEWAY = "192.168.111.1"
	START_ALLO = "192.168.111.20"
	END_ALLO = "192.168.111.40"
	SERVER_NAME = "youngServer"

	print("------------------------------------Task 2 Start ------------------------------")
	tokenId = identity.identity_getToken(USERNAME,PASSWORD,USER_DOMAIN_NAME,PROJECT_ID,CONTROLLER,KEYSTONE_PORT)['token']
	print("Get tokenId : {}".format(tokenId))
	networkId = neutron.neutron_createNetwork(tokenId,NETWORK_NAME,CONTROLLER,NEUTRON_PORT)['network']['id']
	print("Created Network : {}".format(networkId))
	subNetworkId = neutron.neutron_createSubnet(tokenId,SUBNET_NAME,networkId,CIDR,GATEWAY,START_ALLO,END_ALLO,CONTROLLER,NEUTRON_PORT)['subnet']['id']
	print("Created SubNet {} attached to Network {}".format(networkId,subNetworkId))
	server = nova.compute_server_create(tokenId,SERVER_NAME,FLAVOR_ID,CIRROS_ID,networkId,CONTROLLER,NOVA_PORT)
	print("Created Server :")
	print(json.dumps(server,indent=4))
	serverId = server['server']['id']
	print("Created Server : {}".format(serverId));
	print("------------------------------------Task 2 Finish------------------------------")

# Task3 : try to create a scenario : 2 network, 1 router, 2 instances
# IMPORTANT : Please delete your network, router and instances after each test!!!!!!!!!
# PS : How to add a network(or subnet) to a router, a general method?
def task_createScenario():
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
	
	print("------------------------------------Task 3 Start ------------------------------")	
	tokenId = identity.identity_getToken(USERNAME,PASSWORD,USER_DOMAIN_NAME,PROJECT_ID,CONTROLLER,KEYSTONE_PORT)['token']
	print("Get tokenId : {}".format(tokenId))
	networkId1 = neutron.neutron_createNetwork(tokenId,NETWORK_NAME1,CONTROLLER,NEUTRON_PORT)['network']['id']
	networkId2 = neutron.neutron_createNetwork(tokenId,NETWORK_NAME2,CONTROLLER,NEUTRON_PORT)['network']['id']
	print("Created Network : {} , {}".format(networkId1,networkId2))
	subNetworkId1 = neutron.neutron_createSubnet(tokenId,SUBNET_NAME1,networkId1,CIDR1,GATEWAY1,START_ALLO1,END_ALLO1,CONTROLLER,NEUTRON_PORT)['subnet']['id']
	subNetworkId2 = neutron.neutron_createSubnet(tokenId,SUBNET_NAME2,networkId2,CIDR2,GATEWAY2,START_ALLO2,END_ALLO2,CONTROLLER,NEUTRON_PORT)['subnet']['id']
	print("Created subNetwork : {} , {}".format(subNetworkId1,subNetworkId2))
	routerId = neutron.neutron_createRouter(tokenId,ROUTERNAME,CONTROLLER,NEUTRON_PORT)['router']['id']
	print("Created Router : {}".format(routerId))
	portId1 = neutron.neutron_createPort(tokenId,networkId1,subNetworkId1,GATEWAY1,CONTROLLER,NEUTRON_PORT)['port']['id']
	portId2 = neutron.neutron_createPort(tokenId,networkId2,subNetworkId2,GATEWAY2,CONTROLLER,NEUTRON_PORT)['port']['id']
	print("Created Port : {} , {}".format(portId1,portId2))
	neutron.neutron_addRouterInterface(tokenId,routerId,portId1,CONTROLLER,NEUTRON_PORT)
	neutron.neutron_addRouterInterface(tokenId,routerId,portId2,CONTROLLER,NEUTRON_PORT)
	print("Already Connect ports to router")
	serverId1 = nova.compute_server_create(tokenId,SERVER_NAME1,FLAVOR_ID,CIRROS_ID,networkId1,CONTROLLER,NOVA_PORT)['server']['id']
	serverId2 = nova.compute_server_create(tokenId,SERVER_NAME2,FLAVOR_ID,CIRROS_ID,networkId2,CONTROLLER,NOVA_PORT)['server']['id']
	print("Created Server : {}, {}".format(serverId1,serverId2))
	print("------------------------------------Task 3 Finish ------------------------------")
if __name__=='__main__':
    #task_getToken()
    task_printNetworkList()
    #task_createInstance()
    #task_createScenario()
