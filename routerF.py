import logging

logging.basicConfig(format='%(asctime)s - Router F:%(message)s', level=logging.INFO)

from router import Router
from profileManager import ProfileManager
from helper import DisplayObjectTable
from routeTable import RoutingTable
from time import sleep

profile = ProfileManager()
profiles = profile.getAllProfiles()
router = Router(profiles['F']['ip'], profiles['F']['port'], 'F')
sleep(5)
router.run()
router.updateRoutingTable()
