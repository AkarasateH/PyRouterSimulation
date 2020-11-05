from router import Router
from profileManager import ProfileManager
from helper import DisplayObjectTable
from routeTable import RoutingTable
import logging

logging.basicConfig(format='%(asctime)s - Main:%(message)s', level=logging.INFO)
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
  profileManager.addAndUpdateProfile('A', '192.168.0.164', ['192.168.1.0/24', '192.168.4.0/24'], 4000, ['B', 'D'])
  profileManager.addAndUpdateProfile('B', '192.168.0.164', ['192.168.2.0/24'], 4001, ['A', 'C', 'D'])
  profileManager.addAndUpdateProfile('C', '192.168.0.164', ['192.168.2.0/24', '192.168.3.0/24'], 4002, ['B', 'F'])
  profileManager.addAndUpdateProfile('D', '127.0.0.1', ['192.168.4.0/24'], 4003, ['A', 'B', 'E'])
  profileManager.addAndUpdateProfile('E', '127.0.0.1', ['192.168.6.0/24'], 4004, ['D', 'F'])
  profileManager.addAndUpdateProfile('F', '127.0.0.1', ['192.168.5.0/24'], 4005, ['C', 'E'])

  profileManager.getAllProfiles()

__createProfiles()
