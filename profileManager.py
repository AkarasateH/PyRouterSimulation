import json

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

  # Add Neighbor
  def addNeighbor(self, routerName, neighborName):
    profiles = self.__loadProfiles()
    if not (neighborName in profiles[routerName]['neighbor']):
      profiles[routerName]['neighbor'].append(neighborName)
    self.__updateProfiles(profiles)
    return profiles[routerName]

  # Remove Neighbor
  def removeNeighbor(self, routerName, neighborName):
    profiles = self.__loadProfiles()
    profiles[routerName]['neighbor'].remove(neighborName)
    self.__updateProfiles(profiles)
    return profiles[routerName]

  # Removing profile.
  def removeProfile(self, name: str):
    # Get current profile
    profile = self.__loadProfiles()

    # Pop profile [name] out.
    profile.pop(name)

    # Update profile as json
    self.__updateProfiles(profile)

    return profile

  # Adding new profile.
  def addAndUpdateProfile(self, name: str, ip: str, subnet: str, port: int, neighbor: [str]):
    profile = {}
    newObj = {
      'ip': ip,
      'port': port,
      'subnet': subnet,
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
    profile = self.__loadProfiles()
    return profile[name]

  def getAllProfiles(self):
    return self.__loadProfiles()
