from socket import *

class Router:
  TIMEOUT = 4 # Timeout 4 sec
  
  message = 'Hello'
  myIP = ''
  myPort = 4000

  def __init__(self, ip: str, port: int):
    self.myIP = ip
    self.port = port

  def getInfo(self):
    info = dict()
    info['ip'] = self.myIP
    info['port'] = self.port
    return info

  # Server Process:
  def createServer(self):
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((self.myIP, self.port))

    while 1:
      try:
        print('The server is ready to receive')
        print('Receiving data . . .')
        receivedData, addr = serverSocket.recvfrom(1024)
        print('Received from client:', receivedData.decode())
        serverSocket.sendto(receivedData, addr)
      except Exception as err:
        print('ERR: ', err)
        pass

  def checkStatNeighbor(self, ip: str, port: int):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(self.TIMEOUT)
    try:
      clientSocket.sendto(str.encode(self.message), (ip, port))
      receivedMessage, addr = clientSocket.recvfrom(1024)
      print('Received message from ', addr, ':', receivedMessage.decode())
    except Exception as err:
      print('Check stat error: ', err)
      pass
    

