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
CIRROS_ID = "<REPLACE WITH IMAGE ID>"

# FlavorId
FLAVOR_ID = "<REPLACE WITH FALVOR ID>"


import json
import identity


# Guide : How to get Identity Token
def task_getToken():
    token = identity.identity_getToken(USERNAME,PASSWORD,USER_DOMAIN_NAME,PROJECT_ID,CONTROLLER,KEYSTONE_PORT)
    print("Get token")
    print(json.dumps(token,indent=4))

# Task1 : print out Network List
def task_printNetworkList():
    pass
    
# Task2 : try to create a network, and create an instance in the network
# IMPORTANT : Please delete your instance and network after each test!!!!!!!!
def task_createInstance():
	pass

# Task3 : try to create a scenario : 2 network, 1 router, 2 instances
# IMPORTANT : Please delete your network, router and instances after each test!!!!!!!!!
def task_createScenario():
	pass

if __name__=='__main__':
    task_getToken()
