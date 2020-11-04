from router import Router
from profileManager import ProfileManager
import logging

logging.basicConfig(format='%(asctime)s - Router B:%(message)s', level=logging.INFO)

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['B']['ip'], profiles['B']['port'], 'B')
router.run()
# router.updateRoutingTable()
