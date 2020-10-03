import json

class ProfileManager:
  filename = 'profile.json'
  def __init__(self):
    return None

  # Adding new profile.
  def addAndUpdateProfile(self, name: str, ip: str, subnet: str, port: int, connList: [str]):
    profile = {}
    newObj = {
      'ip': ip,
      'port': port,
      'subnet': subnet,
      'neighbor': connList 
    }

    # Get previous profile
    with open(self.filename, 'r') as j:
      profile = json.loads(json.load(j))

    # Assignment new profile.
    profile[name] = newObj

    # Update profile as json
    with open(self.filename, 'w') as file:
      json.dump(json.dumps(profile), file)
    return profile

  def getProfileByName(self, name: str):
    with open(self.filename, 'r') as j:
      profile = json.loads(json.load(j))
      return profile[name]

  def getAllProfiles(self):
    with open(self.filename, 'r') as j:
      profile = json.loads(json.load(j))
      return profile
