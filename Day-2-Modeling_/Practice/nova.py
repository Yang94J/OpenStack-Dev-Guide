# -------------------    Import Necessary Libs    ------------------------------------------------------
import os
import requests
import json
import logging
import sys

# -------------------    nova_getFlavorList    ----------------------------------------------------
def nova_getFlavorList(token_id,controller_ip,service_port):

    logging.warning('start nova_getFlavorList')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.1/flavors"

    headers = {}
    headers['X-Auth-Token'] = token_id

    response = requests.get(auth_url, headers=headers)

    if (response.status_code != 200):
        logging.error("ComputeError : "+str(response.text))
        exit(1)

    return response.json()


# -------------------    nova_createServer    ----------------------------------------------------
def compute_server_create(token_id,server_name,flavor_id, image_id, network_id, controller_ip,service_port):

    logging.warning('start nova_createServer')
    
    auth_url = "http://"+controller_ip+":"+service_port+"/v2.1/servers"

    headers = {}
    headers['X-Auth-Token'] = token_id

    #payload
    payload = {
        'server':{
            'name' : server_name,
            'flavorRef' : flavor_id,
            'networks':[{
                'uuid' : network_id
            }],
            'imageRef' : image_id
        }
    }

    response = requests.post(auth_url, headers=headers, data=json.dumps(payload))

    if (response.status_code != 202):
        logging.error("ComputeError : "+str(response.text))
        exit(1)

    return response.json()
