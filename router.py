from socket import *
import threading
import logging
import re

from profileManager import ProfileManager
from routeTable import RoutingTable

from helper import ConvertJsonToString, ConvertStringToJson

logging.basicConfig(format='%(asctime)s - Router:%(message)s', level=logging.INFO)

class Router:
  TIMEOUT = 3 # Timeout 2 sec
  INTERVAL_TIME = 5 # Interval time 30 sec
  ALIVE_TIMEOUT = 6
  
  reqMessage = 'Hello'
  resMessage = 'Hi'

  def __init__(self, ip: str, port: int, name: str):
    self.myIP = ip
    self.myPort = port
    self.myName = name
    self.profileManager = ProfileManager()
    self.routingTable = RoutingTable(name, self.profileManager.getProfileByName(name)['subnets'])
    self.COUNTER_FAIL = {}

  def getInfo(self):
    info = dict()
    info['ip'] = self.myIP
    info['port'] = self.myPort
    return info
  
  def __getDeathRouters(self):
    delRouterNames = []
    for routerName in self.COUNTER_FAIL.keys():
      if self.COUNTER_FAIL[routerName].get(routerName, 0) == 6:
        delRouterNames.append(routerName)
    return delRouterNames

    e = threading.Event()
    while not e.wait(self.INTERVAL_TIME):
        if self.COUNTER_FAIL.get(routerName, 0) == self.ALIVE_TIMEOUT - 1:
          self.profileManager.removeNeighbor(self.myName, routerName)
          e.set()
        else:
          func(profile, routerName)

  # Server Process:
  def __createServer(self):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((self.myIP, self.myPort))

    pattern = re.compile("(sender)|(receiver)|(findSubnet)")

    while 1:
      try:
        logging.info('Server {} is ready to receive'.format(self.myName))
        logging.info('Server {} receiving data . . .'.format(self.myName))
        receivedData, addr = serverSocket.recvfrom(4096)
        decodedMessage = receivedData.decode()
        logging.info(f'{self.myName} received message: {decodedMessage} from {addr}')
        if decodedMessage == self.reqMessage:
          serverSocket.sendto(self.resMessage.encode(), addr)
        elif pattern.search(decodedMessage):
          logging.info(f'{self.myName} decoded message: {decodedMessage}')
          requestJson = ConvertStringToJson(decodedMessage)
          response = self.__findSubnetProcess(requestJson['findSubnet'], 0)
          serverSocket.sendto(response.encode(), addr)
      except Exception as err:
        # logging.info('ERR: ', err)
        pass

  # Multi tasks for server process.
  def run(self):
    job = threading.Thread(target=self.__createServer, args=[])
    job.start()
    # self.checkAliveNeighbor()
    # self.updateRoutingTable()

  def __advertiseProcess(self, profile: dict, routerName: str):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(self.TIMEOUT)
    try:
      # logging.info('Checking neighbor {}'.format(routerName))
      clientSocket.sendto(self.reqMessage.encode(), (profile['ip'], profile['port']))
      receivedMessage, addr = clientSocket.recvfrom(4096)

      if receivedMessage.decode() == self.resMessage:
        logging.info('{} is alive.'.format(routerName))

    except timeout as err:
      self.COUNTER_FAIL[routerName] = self.COUNTER_FAIL.get(routerName, 0) + 1
      logging.info('Neighbor {} timeout {}.'.format(routerName, self.COUNTER_FAIL.get(routerName, 0)))
      pass

  # Client process
  def checkAliveNeighbor(self):
    profile = self.profileManager.getProfileByName(self.myName)
    neighbors = profile['neighbor']
    logging.info(f'Check stat neighbors : {neighbors}')

    for neighbor in neighbors:
      neighborProfile = self.profileManager.getProfileByName(neighbor)
      thread = threading.Thread(target=self.__setInterval, args=[self.__advertiseProcess, neighborProfile, neighbor])
      thread.start()

  # RT (Routing Table)
  # Return the request as array.
  def __getRequestToUpdateRT(self, subnets: [str] = []):
    myNeighbors = self.profileManager.getProfileByName(self.myName)['neighbor']
    findingSubnets = []

    if len(subnets) == 0:
      findingSubnets = self.profileManager.getUniqueSubnets(self.myName)
    else:
      findingSubnets = subnets

    requests = []

    for findSubnet in findingSubnets:
      for neighbor in myNeighbors:
        neighborProfile = self.profileManager.getProfileByName(neighbor)
        request = {
          'sender': self.myName,
          'receiver': neighbor,
          'dest': {
            'ip': neighborProfile['ip'],
            'port': neighborProfile['port'],
          },
          'findSubnet': findSubnet
        }

        requests.append(request)

    return requests

  def __updatingRTProcess(self, requestMsg: dict):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(self.TIMEOUT)
    try:
      logging.info('{} Update Routing Table {}'.format(self.myName, requestMsg))
      requestMessage = ConvertJsonToString({
        'sender': requestMsg['sender'],
        'receiver': requestMsg['receiver'],
        'findSubnet': requestMsg['findSubnet'],
      })

      clientSocket.sendto(requestMessage.encode(), (requestMsg['dest']['ip'], requestMsg['dest']['port']))

      # Response format will be { rcvFrom: [neighbor-name], cost: [link-cost], subnet: [found-subnet], deathRouters:[router-name] }
      responseMessage, addr = clientSocket.recvfrom(4096)
      responseDict = ConvertStringToJson(responseMessage.decode())

      logging.info('Response message: {}'.format(responseDict))

      updatingData = {
        'subnet': responseDict['subnet'],
        'cost': responseDict['cost'] + 1,
        'owner': responseDict['rcvFrom']
      }

      # Remove neighbor from neighbor data returned
      for routerName in responseDict['deathRouters']:
        self.profileManager.removeNeighbor(self.myName, routerName)

      self.routingTable.updateTable(updatingData)

    except timeout as err:
      logging.info('Update Routing Table:Error: {}.'.format(err))
      pass

  def updateRoutingTable(self):
    logging.info('Router {} is getting all requests for updating routing table {}'.format(self.myName, self.myName))
    requests = self.__getRequestToUpdateRT()

    for request in requests:
      thread = threading.Thread(target=self.__updatingRTProcess, args=[request])
      thread.start()
      thread.join()

    return None

  def __findSubnetProcess(self, subnet: str, myCost: int = 0):
    logging.info('Finding subnet: {}'.format(subnet))
    cost = myCost + 1
    if self.routingTable.subnetIsFound(subnet):
      response = {
        'rcvFrom': self.myName,
        'cost': self.routingTable.getLinkDetailBySubnet(subnet)['linkDetail']['cost'],
        'subnet': subnet,
        'deathRouters': self.__getDeathRouters()
      }

      return ConvertJsonToString(response)
    else:
      requests = self.__getRequestToUpdateRT([subnet])

      for request in requests:
        thread = threading.Thread(target=self.__updatingRTProcess, args=[request])
        thread.start()
      return self.__findSubnetProcess(subnet, cost)
