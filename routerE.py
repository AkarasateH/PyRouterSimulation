from router import Router
from profileManager import ProfileManager
import logging

logging.basicConfig(format='%(asctime)s - Router E:%(message)s', level=logging.INFO)

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['E']['ip'], profiles['E']['port'], 'E')
router.run()
# router.updateRoutingTable()
