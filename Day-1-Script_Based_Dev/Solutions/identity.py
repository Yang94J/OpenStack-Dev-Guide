# -------------------    Import Necessary Libs    ------------------------------------------------------
import os
import requests
import json
import logging
import sys

import util

# -------------------    identity_getToken    ----------------------------------------------------
# Get Project Scoped Token
def identity_getToken(username, password, user_domain_name , project_id, controller_ip,service_port):
    
    # Parameter Testing : Do parameter check before sending request
    logging.warn('start identity_getToken')
    
    # official api
    auth_url = "http://"+controller_ip+":"+service_port+"/v3/auth/tokens"

    payload = {
        "auth": {
            "identity": {
                "methods": [
                    "password"
                ],
                "password": {
                    "user": {
                        "name": username,
                        "domain": {
                            "name": user_domain_name
                        },
                        "password": password
                    }
                }
            },
            "scope": {
                "project" : {
                    "id": project_id
                }
            }
        }
    }
    response = requests.post(auth_url, data=json.dumps(payload))

    token_info = extractToken(response)

    return token_info

# Extract Token
def extractToken(response):

    # Exception cases : Authentication errors
    if (response.status_code != 201):
        logging.error("AuthenticationError : "+str(response.text))
        exit(1)

    # When we get correct status_code
    # Authentication token is in the header with key = "X-Subject-Token"
    token = response.headers['X-Subject-Token']

    # needs to return expire_date for future use
    expire_date = response.json()['token']['expires_at']

    return {"token": token, "expire_date":expire_date}
