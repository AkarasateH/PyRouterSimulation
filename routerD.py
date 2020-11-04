from router import Router
from profileManager import ProfileManager
import logging

logging.basicConfig(format='%(asctime)s - Router D:%(message)s', level=logging.INFO)

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['D']['ip'], profiles['D']['port'], 'D')
router.run()
# router.updateRoutingTable()
