import json
import logging
from helper import DisplayObjectTable

logging.basicConfig(format='%(asctime)s - ProfileManager:%(message)s', level=logging.INFO)

class ProfileManager:
  filename = 'profile.json'
  def __init__(self):
    return None

  # Get profiles from file
  def __loadProfiles(self):
    with open(self.filename, 'r') as j:
     return json.loads(json.load(j))

  # Update profiles in the json file
  def __updateProfiles(self, profiles: dict):
    with open(self.filename, 'w') as file:
      json.dump(json.dumps(profiles), file)

  # Get all subnets in the network
  def __getAllSubnets(self):
    profiles = self.__loadProfiles()
    subnets = []

    for profileName in profiles.keys():
      for subnet in profiles[profileName]['subnets']:
        subnets.append(subnet) if (not subnet in subnets) else subnets

    return subnets

  # Get unique subnet with the router.
  def getUniqueSubnets(self, routerName: str):
    routerSubnets = self.__loadProfiles()[routerName]['subnets']
    set_router = set(routerSubnets)
    set_network = set(self.__getAllSubnets())
    return list(set_network - set_router)

  # Add Neighbor
  def addNeighbor(self, routerName: str, neighborName: str):
    logging.info(f'Adding neighbor {neighborName} to {routerName}.')
    profiles = self.__loadProfiles()
    if not (neighborName in profiles[routerName]['neighbor']):
      profiles[routerName]['neighbor'].append(neighborName)
    self.__updateProfiles(profiles)
    return profiles[routerName]

  # Remove Neighbor
  def removeNeighbor(self, routerName: str, neighborName: str):
    logging.info(f'Removing neighbor {neighborName} from {routerName}.')
    profiles = self.__loadProfiles()
    profiles[routerName]['neighbor'].remove(neighborName)
    self.__updateProfiles(profiles)
    return profiles[routerName]

  # Removing profile.
  def removeProfile(self, profileName: str):
    # Get current profile
    logging.info(f'Removing profile {profileName}.')
    profile = self.__loadProfiles()

    # Pop profile [profileName] out.
    profile.pop(profileName)

    # Update profile as json
    self.__updateProfiles(profile)

    return profile

  # Adding new profile.
  def addAndUpdateProfile(self, name: str, ip: str, subnets: [str], port: int, neighbor: [str]):
    logging.info(f'Adding new profile {name}.')
    profile = {}
    newObj = {
      'ip': ip,
      'port': port,
      'subnets': subnets,
      'neighbor': neighbor
    }

    # Get previous profile
    profile = self.__loadProfiles()

    # Assignment new profile.
    profile[name] = newObj

    # Update profile as json
    self.__updateProfiles(profile)
    return profile

  def getProfileByName(self, name: str):
    logging.info(f'Getting information of profile by name {name}.')
    profile = self.__loadProfiles()
    return profile[name]

  def getAllProfiles(self):
    logging.info(f'Getting information of all profiles.')
    profiles = self.__loadProfiles()
    DisplayObjectTable(['Router Name', 'IP', 'Port', 'Subnets', 'Neighbors'], profiles, 'Profiles Table')
    return profiles
