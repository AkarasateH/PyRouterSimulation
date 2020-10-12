from socket import *
from profileManager import ProfileManager
import threading
import logging

logging.basicConfig(format='%(asctime)s - Router:%(message)s', level=logging.INFO)

class Router:
  TIMEOUT = 1 # Timeout 30 sec
  INTERVAL_TIME = 5 # Interval time 30 sec
  COUNTER_FAIL = {}
  ALIVE_TIMEOUT = 6
  
  reqMessage = 'Hello'
  resMessage = 'Hi'
  myIP = ''
  myPort = 4000
  myName = ''

  def __init__(self, ip: str, port: int, name: str):
    self.myIP = ip
    self.myPort = port
    self.myName = name
    self.profileManager = ProfileManager()
    self.COUNTER_FAIL

  def getInfo(self):
    info = dict()
    info['ip'] = self.myIP
    info['port'] = self.myPort
    return info

  def __setInterval(self, func, profile, routerName):
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

    while 1:
      try:
        logging.info('Server {} is ready to receive'.format(self.myName))
        logging.info('Server {} receiving data . . .'.format(self.myName))
        receivedData, addr = serverSocket.recvfrom(1024)
        if receivedData.decode() == self.reqMessage:
          serverSocket.sendto(self.resMessage.encode(), addr)
      except Exception as err:
        logging.info('ERR: ', err)
        pass

  # Multi tasks for server process.
  def runServer(self):
    job = threading.Thread(target=self.__createServer, args=[])
    job.start()

  def __advertiseProcess(self, profile: dict, routerName: str):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(self.TIMEOUT)
    try:
      logging.info('Checking neighbor {}'.format(routerName))
      clientSocket.sendto(self.reqMessage.encode(), (profile['ip'], profile['port']))
      receivedMessage, addr = clientSocket.recvfrom(1024)

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
