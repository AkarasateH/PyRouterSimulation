from socket import *

class Router:
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
    serverSocket.bind(('', 4000))

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

    

