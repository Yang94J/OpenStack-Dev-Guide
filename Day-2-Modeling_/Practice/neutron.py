# -------------------    Import Necessary Libs    ------------------------------------------------------
import os
import requests
import json
import logging
import sys

import util

# -------------------    neutron_getNetworkList    ----------------------------------------------------

def neutron_getNetworkList(token_id,controller_ip,service_port):

    logging.warn('start neutron_getNetworkList')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.0/networks"

    headers = {}
    headers['X-Auth-Token'] = token_id

    response = requests.get(auth_url, headers=headers)
        
    if (response.status_code != 200):
        logging.error("NetworkingError : "+str(response.text))
        exit(1)

    return response.json()

# -------------------    neutron_createNetwork    ----------------------------------------------------
def neutron_createNetwork (token_id,network_name,controller_ip,service_port):

    logging.warn('start networking_network_create')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.0/networks"

    headers = {}
    headers['X-Auth-Token'] = token_id

    # payload
    payload = {
        'network':{
            'name':network_name,
            'admin_state_up' : True,
            'shared' : True
        }
    }
    
    response = requests.post(auth_url, headers=headers, data=json.dumps(payload))
        
    if (response.status_code != 201):
        logging.error("NetworkingError : "+str(response.text))
        exit(1)

    return response.json()

# -------------------    neutron_createSubnet    ----------------------------------------------------
def neutron_createSubnet(token_id,subnet_name,network_id,cidr,gateway_ip,start_allo, end_allo,controller_ip,service_port):
    logging.warning('start neutron_createSubnet')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.0/subnets"

    headers = {}
    headers['X-Auth-Token'] = token_id

    # payload
    payload = {
        'subnet' : {
            'name' : subnet_name,
            'network_id' : network_id,
            'ip_version' : 4,
            'cidr' : cidr,
            'gateway_ip' : gateway_ip,
            'allocation_pools' : [
                {
                    'start' : start_allo,
                    'end'   : end_allo
                }
            ]
       }
    }
    
    response = requests.post(auth_url, headers=headers,data=json.dumps(payload))
    
    if (response.status_code != 201):
        logging.error("NetworkingError : "+str(response.text))
        exit(1)

    return response.json()


# -------------------    neutron_createRouter    ----------------------------------------------------

def neutron_createRouter(token_id,router_name,controller_ip,service_port):

    # Parameter Testing : Do parameter check before sending request
    logging.warning('start networking_routers_router_create')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.0/routers"

    headers = {}
    headers['X-Auth-Token'] = token_id

    #payload
    payload = {
        'router' : {
            'name' : router_name,
            'admin_state_up' : True
        }
    }
    
    response = requests.post(auth_url, headers=headers, data=json.dumps(payload))
        
    if (response.status_code != 201):
        logging.error("NetworkingError : "+str(response.text))
        exit(1)

    return response.json()

# -------------------    neutron_createPort    ----------------------------------------------------

def neutron_createPort(token_id,network_id,subnet_id,ip_address,controller_ip,service_port):

    # Parameter Testing : Do parameter check before sending request
    logging.warning('start networking_ports_port_create')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.0/ports"

    headers = {}
    headers['X-Auth-Token'] = token_id

    #payload
    payload = {
        'port' : {
            'fixed_ips' : [
                {
                    'subnet_id' : subnet_id,
                    'ip_address' : ip_address
                }
            ],
            'network_id' : network_id
         }
    }
    
    response = requests.post(auth_url, headers=headers, data=json.dumps(payload))
        
    if (response.status_code != 201):
        logging.error("NetworkingError : "+str(response.text))
        exit(1)

    return response.json()

# -------------------    neutron_addRouterInterface    ----------------------------------------------------
def neutron_addRouterInterface(token_id,router_id,port_id,controller_ip,service_port):

    # Parameter Testing : Do parameter check before sending request
    logging.warning('start neutron_addRouterInterface')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.0/routers/"+router_id+"/add_router_interface"

    headers = {}
    headers['X-Auth-Token'] = token_id

    #payload
    payload = {
        'port_id' : port_id
    }
    
    response = requests.put(auth_url, headers=headers, data=json.dumps(payload))
        
    if (response.status_code != 200):
        logging.error("NetworkingError : "+str(response.text))
        exit(1)

    return response.json()
