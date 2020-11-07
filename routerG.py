from router import Router
from profileManager import ProfileManager
import logging

logging.basicConfig(format='%(asctime)s - Router F:%(message)s', level=logging.INFO)

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['G']['ip'], profiles['G']['port'], 'G')
router.run()
# router.updateRoutingTable()
