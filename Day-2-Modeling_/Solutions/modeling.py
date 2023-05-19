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

import logging
import identity
import neutron
import nova

tokenId = identity.identity_getToken(USERNAME,
                                     PASSWORD,
                                     USER_DOMAIN_NAME,
                                     PROJECT_ID,
                                     CONTROLLER,
                                     KEYSTONE_PORT)['token']
print("tokenId got : {}".format(tokenId))

class Network:
    def __init__(self,networkName) -> None:
        self.networkId = ""
        self.networkName = networkName
        self.subnetList = []
    
    def create(self) -> 'Network':
        self.networkId = neutron.neutron_createNetwork(
            tokenId,
            self.networkName,
            CONTROLLER,
            NEUTRON_PORT)['network']['id']
        
        logging.warn("Create Network : {}".format(self.networkName))

        return self
    
    def addSubnet(self,subnet : 'SubNetwork') -> None:
        self.subnetList.append(subnet)

class SubNetwork:
    def __init__(self, 
                 network : 'Network',
                 subnetName : str, 
                 subnetCidr : str,
                 gateway : str,
                 startAllo : str,
                 endAllo : str
                 ) -> None:
        if (network.networkId==""):
            raise Exception("Cant assign subnet to uncreated network")
        self.network = network
        self.subnetName = subnetName
        self.subnetCidr = subnetCidr
        self.gateway = gateway
        self.startAllo = startAllo
        self.endAllo = endAllo
        self.subnetId = ""
        self.portList = []
    
    def create(self) -> 'SubNetwork':
        self.subnetId = neutron.neutron_createSubnet(
            tokenId,
            self.subnetName,
            self.network.networkId,
            self.subnetCidr,
            self.gateway,
            self.startAllo,
            self.endAllo,
            CONTROLLER,
            NEUTRON_PORT)['subnet']['id']
        
        logging.warn("Create Subnet : {} in Network {}".format(self.subnetName,self.network.networkName))

        self.gatewayUsed = False
        self.allo = int(self.startAllo.split(".")[-1])+1

        self.network.addSubnet(self)
        return self
    
    def addPort(self, port : 'Port') -> None:
        if (self.subnetId == ""):
            raise Exception("cant add port to uncreated subnet")
        if (port.portId == ""):
            raise Exception("cant add uncreated port")
        self.portList.append(port)

    def generatePortIp(self) -> str:
        if not self.gatewayUsed:
            self.gatewayUsed = True
            return self.gateway
        
        generatedIp = ".".join(self.subnetCidr.split(".")[:-1])+"."+str(self.allo)
        self.allo += 1

        logging.warn("generate ip : {}".format(generatedIp))
        return generatedIp


class Port:
    def __init__(self,subnet : 'SubNetwork') -> None:
        if (subnet.subnetId==""):
            raise Exception("Cant assign port to uncreated network")
        self.subnet = subnet
        self.portId = ""
        self.ip = ""

    def create(self) -> 'Port':
        self.ip = self.subnet.generatePortIp()
        response = neutron.neutron_createPort(
            tokenId,
            self.subnet.network.networkId,
            self.subnet.subnetId,
            self.ip,
            CONTROLLER,
            NEUTRON_PORT
        )
        self.portId = response['port']['id']
        self.ip = response['port']['fixed_ips'][0]['ip_address']
        logging.warn("port {}:{} created in subnet {}".format(self.portId,self.ip,self.subnet.subnetName))
        self.attachedRouter = None
        self.subnet.addPort(self)
        return self
    
    def attachRouter(self, router:'Router') -> None:
        self.attachedRouter = router

class Router:
    def __init__(self,routerName):
        self.routerName = routerName
        self.routerId = ""
        self.attachPortList = []
        self.routingTable = {}
    
    def create(self) -> 'Router':
        self.routerId = neutron.neutron_createRouter(
            tokenId,
            self.routerName,
            CONTROLLER,
            NEUTRON_PORT
        )['router']['id']
        logging.warning("router {} created".format(self.routerId))
        return self
    
    def attachPort(self,port : 'Port') -> None:
        if (self.routerId == ""):
            raise Exception("Cant attach to uncreated Router")
        if (port.portId==""):
            raise Exception("Cant attach uncreated Port")
        if (port.attachedRouter!=None):
            raise Exception("Port already attached")

        neutron.neutron_addRouterInterface(
            tokenId,
            self.routerId,
            port.portId,
            CONTROLLER,
            NEUTRON_PORT
        )

        logging.warning("Port {}:{} attached to Router {}".format(port.portId,port.ip,self.routerName))

        self.attachPortList.append(port)
        port.attachRouter(self)
    
    def addStaticRoute(self,cidr : str,port : Port) -> None:
        if cidr not in self.routingTable:
            self.routingTable[cidr] = port
            logging.warning("Router {} add static Routing of cidr {} with {}".format(self.routerName,cidr,port.ip))
            neutron.neutron_addStaticRoute(
                tokenId,
                self.routerId,
                cidr,
                port.ip,
                CONTROLLER,
                NEUTRON_PORT
        )
            
class Server:
    def __init__(self,
                 network : 'Network',
                 serverName : str,
                 flavorId : str,
                 imageId : str) -> None:
        if (network.networkId == ""):
            raise Exception("cant init under uncreated network")
        self.network = network
        self.serverName = serverName
        self.flavorId = flavorId
        self.imageId = imageId
        self.serverId = ""
    
    def create(self) -> 'Server':
        self.serverId = nova.compute_server_create(
            tokenId,
            self.serverName,
            self.flavorId,
            self.imageId,
            self.network.networkId,
            CONTROLLER,
            NOVA_PORT
        )['server']['id']

        logging.warning("Server {} created in network {}".format(self.serverName, self.network.networkName))

        return self
