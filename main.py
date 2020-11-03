import logging

logging.basicConfig(format='%(asctime)s - Main:%(message)s', level=logging.INFO)

from router import Router
from profileManager import ProfileManager
from helper import DisplayObjectTable
from routeTable import RoutingTable

def __createProfiles():
  profileManager = ProfileManager()
  # ------------- Minimal Network -------------
  # profileManager.removeProfile('D')
  # profileManager.removeProfile('E')
  # profileManager.removeProfile('F')
  # profileManager.addAndUpdateProfile('A', '127.0.0.1', ['192.168.1.0/24', '192.168.4.0/24'], 4000, ['B'])
  # profileManager.addAndUpdateProfile('B', '127.0.0.1', ['192.168.2.0/24'], 4001, ['A', 'C'])
  # profileManager.addAndUpdateProfile('C', '127.0.0.1', ['192.168.3.0/24', '192.168.2.0/24'], 4002, ['B'])
  # ------------- Large Network -------------
  profileManager.removeProfile('A')
  profileManager.removeProfile('B')
  profileManager.removeProfile('C')
  profileManager.addAndUpdateProfile('A', '127.0.0.1', ['192.168.1.0/24', '192.168.4.0/24'], 4000, ['B', 'D'])
  profileManager.addAndUpdateProfile('B', '127.0.0.1', ['192.168.2.0/24'], 4001, ['A', 'C', 'D'])
  profileManager.addAndUpdateProfile('C', '127.0.0.1', ['192.168.2.0/24', '192.168.3.0/24'], 4002, ['B', 'F'])
  profileManager.addAndUpdateProfile('D', '127.0.0.1', ['192.168.4.0/24'], 4003, ['A', 'B', 'E'])
  profileManager.addAndUpdateProfile('E', '127.0.0.1', ['192.168.6.0/24'], 4004, ['D', 'F'])
  profileManager.addAndUpdateProfile('F', '127.0.0.1', ['192.168.5.0/24'], 4005, ['C', 'E'])

  profileManager.getAllProfiles()

def __initRouters():
  profile = ProfileManager()
  profiles = profile.getAllProfiles()
  routers = {}

  for routerName in profiles.keys():
    print('Initial Router: ', routerName);
    if routerName != 'Z':
      routers[routerName] = Router(profiles[routerName]['ip'], profiles[routerName]['port'], routerName)
      routers[routerName].run()
  
  return routers

# __createProfiles()
routers = __initRouters()
routers['A'].updateRoutingTable()
routers['B'].updateRoutingTable()
routers['C'].updateRoutingTable()
routers['D'].updateRoutingTable()
routers['E'].updateRoutingTable()
routers['F'].updateRoutingTable()
# ProfileManager().addAndUpdateProfile('Z', '127.0.0.1', '192.168.99.0/24', 4099, [])
# ProfileManager().addNeighbor('A', 'Z')
# profiles = ProfileManager().getAllProfiles()
# DisplayObjectTable(['Name', 'IP', 'Port', 'Subnet', 'Neighbor'], profiles)
# routers['A'].checkAliveNeighbor()
