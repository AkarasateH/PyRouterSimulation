from router import Router
from profileManager import ProfileManager
import logging

logging.basicConfig(format='%(asctime)s - Router F:%(message)s', level=logging.INFO)

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['F']['ip'], profiles['F']['port'], 'F')
router.run()
# router.updateRoutingTable()
